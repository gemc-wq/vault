# Brain Memory Layer

Semantic search over Ava's Google Drive Brain documents, powered by Supabase + pgvector + OpenAI embeddings.

## Architecture

```
Google Drive (Brain/)
    ↓ rclone
sync_brain.py
    ↓ OpenAI text-embedding-3-small
Supabase (brain_documents + brain_chunks)
    ↓ pgvector cosine search
brain_search.py
```

## Status

- ✅ `brain_documents` table — created
- ✅ `brain_chunks` table (with `vector(1536)` embedding column) — created
- ⚠️ `match_brain_chunks` RPC — **needs manual SQL run** (see below)

## Setup

### 1. Create the search function in Supabase

Go to: https://supabase.com/dashboard/project/auzjmawughepxbtpwuhe/sql/new

Paste and run the contents of `setup_search_fn.sql`.

### 2. Install Python dependencies

```bash
pip install openai requests
```

### 3. Set your OpenAI API key

```bash
export OPENAI_API_KEY=sk-...
```

### 4. Run sync

```bash
# Dry run first
python sync_brain.py --dry-run

# Full sync
python sync_brain.py

# Force re-index all
python sync_brain.py --force
```

### 5. Search

```bash
# CLI
python brain_search.py "what is our brand positioning?"
python brain_search.py "amazon ad strategy" --top 10
python brain_search.py "licensing deals" --project MIRROR --top 5

# JSON output
python brain_search.py "product roadmap" --json
```

### 6. Import as module

```python
from brain_search import brain_search

results = brain_search("brand strategy", top_n=5)
for r in results:
    print(f"[{r['similarity']:.2f}] {r['path']}\n{r['content'][:200]}\n")
```

## Tables

### brain_documents
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| path | TEXT UNIQUE | Relative path from Brain/ |
| title | TEXT | Derived from filename |
| content | TEXT | Full file content |
| content_hash | TEXT | SHA256 for change detection |
| file_type | TEXT | .md or .txt |
| project | TEXT | First path component |
| category | TEXT | Second path component |
| last_modified | TIMESTAMPTZ | From Drive metadata |
| indexed_at | TIMESTAMPTZ | Last sync time |
| metadata | JSONB | Extra metadata |

### brain_chunks
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| document_id | UUID FK | → brain_documents |
| chunk_index | INT | Order within document |
| content | TEXT | Chunk text |
| token_count | INT | Approximate word count |
| embedding | vector(1536) | OpenAI text-embedding-3-small |
| created_at | TIMESTAMPTZ | |

## Chunking Strategy

- **Markdown (.md):** Split by `## ` headers — preserves semantic sections
- **Text (.txt):** Split by double-newline paragraphs, max ~500 tokens per chunk

## Excluded Paths

- `Assets/`
- `_archive/`
- `Credentials/`
