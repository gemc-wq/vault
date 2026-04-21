#!/usr/bin/env python3
"""
Brain Memory Layer - Sync Script
Scans Google Drive Brain/ folder, chunks & embeds docs, upserts to Supabase.

Usage:
    OPENAI_API_KEY=sk-... python sync_brain.py [--dry-run] [--force]

Requirements:
    pip install openai requests
    rclone configured with 'gdrive' remote
"""

import os
import sys
import json
import hashlib
import subprocess
import tempfile
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

# ── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL = "https://auzjmawughepxbtpwuhe.supabase.co"
SUPABASE_KEY = os.environ.get(
    "SUPABASE_SERVICE_KEY",
    "[REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc"
)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GDRIVE_PATH = "gdrive:Clawdbot Shared Folder/Brain"
EXCLUDE_DIRS = ["Assets", "_archive", "Credentials"]
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMS = 1536
BATCH_SIZE = 20  # embed N chunks at a time

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}


# ── Embedding ─────────────────────────────────────────────────────────────────
def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts using OpenAI text-embedding-3-small."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is not set. Export it before running:\n"
            "  export OPENAI_API_KEY=sk-..."
        )
    resp = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": EMBEDDING_MODEL, "input": texts},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    data.sort(key=lambda x: x["index"])
    return [item["embedding"] for item in data]


# ── Chunking ──────────────────────────────────────────────────────────────────
def chunk_markdown(content: str) -> list[str]:
    """Split markdown by ## headers. Falls back to paragraph split."""
    sections = re.split(r"\n(?=## )", content)
    chunks = []
    for section in sections:
        section = section.strip()
        if section:
            chunks.append(section)
    return chunks if chunks else chunk_by_paragraphs(content)


def chunk_by_paragraphs(content: str, max_tokens: int = 500) -> list[str]:
    """Split text by double-newline paragraphs."""
    paragraphs = re.split(r"\n\s*\n", content)
    chunks = []
    current = []
    current_len = 0
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para_len = len(para.split())
        if current_len + para_len > max_tokens and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def chunk_content(content: str, file_type: str) -> list[str]:
    if file_type == ".md":
        return chunk_markdown(content)
    else:
        return chunk_by_paragraphs(content)


# ── rclone helpers ────────────────────────────────────────────────────────────
def rclone_ls(remote_path: str) -> list[dict]:
    """List all files recursively, return list of {path, name, size, modtime}."""
    result = subprocess.run(
        ["rclone", "lsjson", "--recursive", remote_path],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        print(f"rclone lsjson error: {result.stderr}", file=sys.stderr)
        return []
    items = json.loads(result.stdout)
    return [i for i in items if not i.get("IsDir")]


def rclone_cat(remote_path: str) -> Optional[str]:
    """Download and return file content as string."""
    result = subprocess.run(
        ["rclone", "cat", remote_path],
        capture_output=True, timeout=120,
    )
    if result.returncode != 0:
        print(f"rclone cat error for {remote_path}: {result.stderr.decode()}", file=sys.stderr)
        return None
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return result.stdout.decode("utf-8", errors="replace")


# ── Supabase helpers ──────────────────────────────────────────────────────────
def get_existing_hashes() -> dict[str, str]:
    """Return {path: content_hash} for all indexed documents."""
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/brain_documents",
        headers=HEADERS,
        params={"select": "path,content_hash", "limit": "10000"},
        timeout=30,
    )
    resp.raise_for_status()
    return {row["path"]: row["content_hash"] for row in resp.json()}


def upsert_document(doc: dict) -> str:
    """Upsert a document record, return its UUID."""
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/brain_documents",
        headers={**HEADERS, "Prefer": "resolution=merge-duplicates,return=representation"},
        json=doc,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()[0]["id"]


def delete_chunks(document_id: str):
    """Delete existing chunks for a document (for re-indexing)."""
    requests.delete(
        f"{SUPABASE_URL}/rest/v1/brain_chunks",
        headers=HEADERS,
        params={"document_id": f"eq.{document_id}"},
        timeout=30,
    )


def upsert_chunks(chunks: list[dict]):
    """Batch insert chunk records."""
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/brain_chunks",
        headers={**HEADERS, "Prefer": "resolution=merge-duplicates"},
        json=chunks,
        timeout=60,
    )
    resp.raise_for_status()


# ── Path parsing ──────────────────────────────────────────────────────────────
def parse_path_metadata(rel_path: str) -> dict:
    """Extract project and category from path structure."""
    parts = Path(rel_path).parts
    project = parts[0] if len(parts) > 1 else None
    category = parts[1] if len(parts) > 2 else None
    title = Path(rel_path).stem.replace("-", " ").replace("_", " ")
    return {"project": project, "category": category, "title": title}


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Sync Brain docs to Supabase")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to Supabase")
    parser.add_argument("--force", action="store_true", help="Re-index unchanged files")
    args = parser.parse_args()

    print(f"🔍 Listing files in {GDRIVE_PATH} ...")
    all_files = rclone_ls(GDRIVE_PATH)

    # Filter to .md and .txt only, excluding dirs
    files = [
        f for f in all_files
        if Path(f["Path"]).suffix.lower() in {".md", ".txt"}
        and not any(
            part in EXCLUDE_DIRS
            for part in Path(f["Path"]).parts
        )
    ]
    print(f"   Found {len(files)} .md/.txt files (excluded: Assets/, _archive/, Credentials/)")

    if not files:
        print("No files found. Check rclone gdrive remote config.")
        return

    existing_hashes = {} if args.dry_run else get_existing_hashes()
    print(f"   {len(existing_hashes)} documents already indexed\n")

    stats = {"new": 0, "updated": 0, "skipped": 0, "errors": 0}

    for file_info in files:
        rel_path = file_info["Path"]
        full_remote = f"{GDRIVE_PATH}/{rel_path}"
        file_type = Path(rel_path).suffix.lower()
        mod_time = file_info.get("ModTime", "")

        print(f"📄 {rel_path}")

        try:
            # Download content
            content = rclone_cat(full_remote)
            if content is None:
                stats["errors"] += 1
                continue
        except Exception as e:
            print(f"   ❌ Error downloading: {e}")
            stats["errors"] += 1
            continue

        content_hash = hashlib.sha256(content.encode()).hexdigest()

        # Skip if unchanged
        if not args.force and existing_hashes.get(rel_path) == content_hash:
            print(f"   ⏭  unchanged")
            stats["skipped"] += 1
            continue

        is_new = rel_path not in existing_hashes
        stats["new" if is_new else "updated"] += 1

        if args.dry_run:
            chunks = chunk_content(content, file_type)
            print(f"   [DRY RUN] would index {len(chunks)} chunks")
            continue

        # Parse metadata
        meta = parse_path_metadata(rel_path)

        # Build chunks
        raw_chunks = chunk_content(content, file_type)
        raw_chunks = [c for c in raw_chunks if c.strip()]
        print(f"   ✂️  {len(raw_chunks)} chunks → embedding...")

        # Embed in batches
        all_embeddings = []
        for i in range(0, len(raw_chunks), BATCH_SIZE):
            batch = raw_chunks[i:i + BATCH_SIZE]
            try:
                embeddings = embed_texts(batch)
                all_embeddings.extend(embeddings)
            except Exception as e:
                print(f"   ❌ Embedding error: {e}", file=sys.stderr)
                stats["errors"] += 1
                break
        else:
            # Upsert document
            try:
                doc_record = {
                    "path": rel_path,
                    "title": meta["title"],
                    "content": content,
                    "content_hash": content_hash,
                    "file_type": file_type,
                    "project": meta["project"],
                    "category": meta["category"],
                    "last_modified": mod_time or None,
                    "indexed_at": datetime.now(timezone.utc).isoformat(),
                }
                doc_id = upsert_document(doc_record)

                # Delete old chunks
                delete_chunks(doc_id)

                # Insert new chunks
                chunk_records = [
                    {
                        "document_id": doc_id,
                        "chunk_index": idx,
                        "content": chunk_text,
                        "token_count": len(chunk_text.split()),
                        "embedding": embedding,
                    }
                    for idx, (chunk_text, embedding) in enumerate(
                        zip(raw_chunks, all_embeddings)
                    )
                ]
                upsert_chunks(chunk_records)
                print(f"   ✅ {'Created' if is_new else 'Updated'} ({len(chunk_records)} chunks)")
            except Exception as e:
                print(f"   ❌ Supabase error: {e}", file=sys.stderr)
                stats["errors"] += 1

    print(f"\n{'='*50}")
    print(f"📊 Sync complete:")
    print(f"   New:     {stats['new']}")
    print(f"   Updated: {stats['updated']}")
    print(f"   Skipped: {stats['skipped']}")
    print(f"   Errors:  {stats['errors']}")


if __name__ == "__main__":
    main()
