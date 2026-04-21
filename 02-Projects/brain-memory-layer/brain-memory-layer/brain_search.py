#!/usr/bin/env python3
"""
Brain Memory Layer - Search Function
Semantic search across indexed Brain documents via pgvector.

Usage:
    OPENAI_API_KEY=sk-... python brain_search.py "query string" [--top 5]
    
    Or import as a module:
        from brain_search import brain_search
        results = brain_search("what is our brand strategy?", top_n=5)

Requirements:
    pip install openai requests
"""

import os
import sys
import json
import argparse
from typing import Optional

import requests

# ── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL = "https://auzjmawughepxbtpwuhe.supabase.co"
SUPABASE_KEY = os.environ.get(
    "SUPABASE_SERVICE_KEY",
    "[REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc"
)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBEDDING_MODEL = "text-embedding-3-small"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


# ── Embedding ─────────────────────────────────────────────────────────────────
def embed_query(query: str) -> list[float]:
    """Embed a single query string."""
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
        json={"model": EMBEDDING_MODEL, "input": query},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["data"][0]["embedding"]


# ── Search ────────────────────────────────────────────────────────────────────
def brain_search(
    query: str,
    top_n: int = 5,
    project_filter: Optional[str] = None,
    category_filter: Optional[str] = None,
    min_score: float = 0.0,
) -> list[dict]:
    """
    Semantic search across brain documents.
    
    Args:
        query: Natural language query
        top_n: Number of results to return
        project_filter: Optional project name to restrict search
        category_filter: Optional category to restrict search
        min_score: Minimum cosine similarity score (0-1)
    
    Returns:
        List of result dicts: {path, project, category, chunk_index, score, content}
    """
    # Embed the query
    embedding = embed_query(query)

    # Call the match_brain_chunks RPC function
    payload = {
        "query_embedding": embedding,
        "match_count": top_n,
        "match_threshold": min_score,
    }
    if project_filter:
        payload["filter_project"] = project_filter
    if category_filter:
        payload["filter_category"] = category_filter

    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/match_brain_chunks",
        headers=HEADERS,
        json=payload,
        timeout=30,
    )

    if resp.status_code == 404 or (
        resp.status_code != 200 and "Could not find the function" in resp.text
    ):
        # Fallback: client-side vector search (slower, no true cosine sort)
        print(
            "⚠️  match_brain_chunks RPC not found. Run setup_search_fn.sql in Supabase SQL editor.",
            file=sys.stderr,
        )
        return _fallback_search(embedding, top_n, project_filter, category_filter)

    resp.raise_for_status()
    return resp.json()


def _fallback_search(
    embedding: list[float],
    top_n: int,
    project_filter: Optional[str],
    category_filter: Optional[str],
) -> list[dict]:
    """
    Fallback: fetch docs metadata + chunks, compute cosine similarity client-side.
    Only practical for small indexes (<1K chunks).
    """
    import math

    params = {
        "select": "id,content,chunk_index,document_id,brain_documents(path,project,category)",
        "limit": "1000",
    }
    if project_filter:
        params["brain_documents.project"] = f"eq.{project_filter}"

    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/brain_chunks",
        headers=HEADERS,
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    chunks = resp.json()

    def cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        return dot / (na * nb) if na * nb else 0.0

    # We don't have embeddings in the fallback (too large to fetch all)
    # Return empty with explanation
    print(
        "Fallback search requires embeddings. Please create match_brain_chunks function.",
        file=sys.stderr,
    )
    return []


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Search the Brain knowledge base")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--project", help="Filter by project name")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--min-score", type=float, default=0.0, help="Min similarity score")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    print(f'🔍 Searching: "{args.query}"', file=sys.stderr)
    results = brain_search(
        query=args.query,
        top_n=args.top,
        project_filter=args.project,
        category_filter=args.category,
        min_score=args.min_score,
    )

    if args.json:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print("No results found.")
        return

    print(f"\n{'='*60}")
    for i, r in enumerate(results, 1):
        score = r.get("similarity", r.get("score", 0))
        path = r.get("path", r.get("document_path", "unknown"))
        project = r.get("project", "")
        category = r.get("category", "")
        content = r.get("content", "")

        print(f"\n#{i}  [{score:.3f}]  {path}")
        if project:
            print(f"     Project: {project}  |  Category: {category}")
        print(f"     {content[:300]}{'...' if len(content) > 300 else ''}")
    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
