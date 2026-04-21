# Harry — Brain Memory Layer Build (Priority)

## Context
You keep losing context after compaction. This fixes it permanently.
Full spec: `gdrive:Clawdbot Shared Folder/Brain/Projects/brain-memory-layer/BRAIN_MEMORY_LAYER_SPEC.md`

## Your Tasks (Phase 1 — Today)

1. **Create tables** in existing Supabase project (`auzjmawughepxbtpwuhe`):
   - `brain_documents` — one row per file
   - `brain_chunks` — one row per semantic chunk, with `vector(1536)` column
   - Schema is in the spec

2. **Write sync script** (Python):
   - `rclone lsjson` Brain/ recursively
   - Download .md/.txt files (skip Assets/, _archive/, Credentials/, binaries)
   - Chunk by ## headers for .md, paragraphs for .txt
   - Embed with OpenAI `text-embedding-3-small`
   - Upsert to Supabase
   - Use content_hash (SHA256) for change detection

3. **Deploy Edge Function**: `brain-search`
   - POST endpoint accepting `{query, project?, category?, limit?}`
   - Embeds query → cosine similarity search → returns top N chunks with metadata

4. **Run initial sync** — index everything in Brain/ (excluding Assets, _archive, Credentials)

## Credentials You Need
- Supabase URL: `https://auzjmawughepxbtpwuhe.supabase.co`
- Supabase service_role key: already in your TOOLS.md
- OpenAI API key: for embeddings (text-embedding-3-small)

## When Done
- Ava will create the OpenClaw skill wrapper + wire into all SOUL.md files
- Nightly cron syncs delta changes at 5 AM

## Also
- Read and add `gdrive:Clawdbot Shared Folder/Brain/Handoffs/harry-soul-patch.md` to your SOUL.md
- This is a memory protocol to prevent context loss — add it today

— Ava
