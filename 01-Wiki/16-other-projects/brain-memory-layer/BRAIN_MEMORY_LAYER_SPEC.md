# Brain Memory Layer — Project Spec

> **Goal**: Give all OpenClaw agents instant semantic search over every project spec, decision, handoff, and daily note in Brain/ — eliminating compaction amnesia.

## Problem Statement

Agents lose context after session compaction. They re-ask questions, restart work, and waste Cem's time. The Brain/ folder on Google Drive contains 19 project folders, daily notes, handoffs, SOPs, credentials, and research — but agents can only access it via slow rclone reads. There's no way to **search by meaning** ("what did we decide about Target+ store architecture?").

## Architecture

```
Google Drive (Brain/)          Supabase (pgvector)           OpenClaw Agents
┌─────────────────┐           ┌──────────────────┐          ┌──────────────┐
│ Projects/        │──sync──▶ │ brain_documents    │◀──query──│ Ava (SOUL.md)│
│ Daily/           │          │ brain_chunks       │          │ Harry         │
│ Handoffs/        │          │ brain_embeddings   │          │ Sven          │
│ SOPs/            │          │  (pgvector)        │          │ All agents    │
│ Research/        │          └──────────────────┘          └──────────────┘
│ Org/             │                  ▲
│ Collaboration/   │                  │
│ Templates/       │           Nightly sync cron
└─────────────────┘           (rclone → chunk → embed)
```

## Database Schema (Supabase pgvector)

```sql
-- Documents table (one row per file)
CREATE TABLE brain_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  path TEXT NOT NULL UNIQUE,          -- 'Projects/goheadcase/strategy/...'
  title TEXT,                          -- extracted or filename
  content TEXT NOT NULL,               -- full text content
  content_hash TEXT NOT NULL,          -- SHA256 for change detection
  file_type TEXT,                      -- md, txt, csv, json
  project TEXT,                        -- parsed from path: 'goheadcase', 'sales-analytics'
  category TEXT,                       -- 'project_spec', 'handoff', 'daily', 'sop', 'research'
  last_modified TIMESTAMPTZ,
  indexed_at TIMESTAMPTZ DEFAULT NOW(),
  metadata JSONB                       -- flexible: {author, tags, related_projects}
);

-- Chunks table (one row per semantic chunk)
CREATE TABLE brain_chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES brain_documents(id) ON DELETE CASCADE,
  chunk_index INT NOT NULL,
  content TEXT NOT NULL,
  token_count INT,
  embedding vector(1536),              -- OpenAI text-embedding-3-small
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX ON brain_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON brain_documents (project);
CREATE INDEX ON brain_documents (category);
CREATE INDEX ON brain_documents (content_hash);
```

## Search API

Supabase Edge Function: `brain-search`

```
POST /functions/v1/brain-search
{
  "query": "what did we decide about Target+ store architecture?",
  "project": "microsites",      // optional filter
  "category": "project_spec",   // optional filter
  "limit": 5
}

Response:
{
  "results": [
    {
      "path": "Projects/microsites/ARCHITECTURE.md",
      "chunk": "2-Store Setup... Walmart + Target + OnBuy unified...",
      "score": 0.92,
      "project": "microsites",
      "category": "project_spec"
    }
  ]
}
```

## Sync Pipeline (Nightly Cron)

1. `rclone lsjson` Brain/ recursively (fast metadata scan)
2. Compare `content_hash` against `brain_documents` — identify new/changed files
3. Download only changed files
4. Chunk: split by headers (## sections) for .md, paragraphs for .txt, skip binaries
5. Embed: OpenAI `text-embedding-3-small` ($0.02/1M tokens — Brain/ is probably <5M tokens total = ~$0.10/full reindex)
6. Upsert to Supabase

**Cost estimate**: ~$0.10 per full reindex, ~$0.01 for delta updates. Negligible.

## SOUL.md Integration

Add to EVERY agent's SOUL.md:

```markdown
## Brain Memory (MANDATORY)

Before starting any project work or answering questions about past decisions:

1. Query brain-search: `curl -s "$SUPABASE_URL/functions/v1/brain-search" -H "Authorization: Bearer $SUPABASE_KEY" -d '{"query": "<your question>"}'`
2. Read the top 3 results for context
3. If a project folder exists in results, reference it — don't start from scratch

This replaces manual rclone reads. Use it FIRST, rclone SECOND.
```

Better: wrap this in an OpenClaw skill (`brain-search`) so agents call it naturally.

## What Gets Indexed

| Source | Category | Est. Files |
|--------|----------|-----------|
| Brain/Projects/**/**.md | project_spec | ~100 |
| Brain/Daily/*.md | daily | ~30 |
| Brain/Handoffs/*.md | handoff | ~15 |
| Brain/SOPs/*.md | sop | ~10 |
| Brain/Research/*.md | research | ~10 |
| Brain/Org/*.md | org | ~5 |
| Brain/Collaboration/*.md | collaboration | ~10 |
| Brain/Templates/*.md | template | ~5 |
| Agent memory/*.md files | agent_memory | ~60 |
| Agent MEMORY.md files | agent_memory | ~3 |

**Excluded**: Assets/ (binary), _archive/, *.csv, *.xlsx, *.zip, *.psd

Total estimate: ~250 documents, ~1000 chunks, ~2M tokens = **$0.04 to embed**

## What Does NOT Get Indexed

- Credentials (Brain/Credentials/) — security risk
- Binary assets (PSD, PNG, CSV, XLSX)
- Archive folder

## Implementation Plan

### Phase 1: Core (Day 1) — Harry builds
- [ ] Create `brain_documents` + `brain_chunks` tables in existing Supabase project
- [ ] Write sync script (Python): rclone → chunk → embed → upsert
- [ ] Deploy as Supabase Edge Function: `brain-search`
- [ ] Test with 5 project folders

### Phase 2: Wire to Agents (Day 2) — Ava builds
- [ ] Create OpenClaw skill: `brain-search` (wraps the Edge Function)
- [ ] Add SOUL.md directive to Ava, Harry, Sven
- [ ] Test: "what did we decide about the Shopify store architecture?" → should return ARCHITECTURE.md

### Phase 3: Nightly Sync (Day 2) — Ava cron
- [ ] OpenClaw cron job: `0 5 * * *` (5 AM EST, before project status + morning brief)
- [ ] Delta sync: only re-embed changed files
- [ ] Also index agent memory/ files (Ava + Harry + Sven workspaces)

### Phase 4: Agent Memory Writes (Week 2)
- [ ] Agents can POST new documents to Brain via Edge Function
- [ ] Auto-index on write (no waiting for nightly sync)
- [ ] Cross-agent visibility: Harry writes a spec → Ava can search it instantly

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Vector DB | Supabase pgvector | Already have it, free tier sufficient |
| Embeddings | OpenAI text-embedding-3-small | Best retrieval quality per dollar |
| Sync | Python + rclone | Already working on both machines |
| Search API | Supabase Edge Function | Zero infra, auto-scales |
| Skill wrapper | OpenClaw skill | Native agent integration |

## Cost

| Item | Monthly Cost |
|------|-------------|
| Embeddings (daily delta) | ~$0.30/mo |
| Supabase pgvector | Free (existing project) |
| Edge Function calls | Free tier (500K/mo) |
| **Total** | **~$0.30/month** |

## Success Criteria

1. No agent ever asks Cem "what project is this?" or "where is the spec?"
2. Query "NBCU PO automation" returns the spec + FedEx CSV format within 2 seconds
3. All 3 agents (Ava, Harry, Sven) can search Brain from their SOUL.md startup
4. New documents indexed within 24 hours (nightly sync) or instantly (Phase 4)

---

*Scoped by Ava, 2026-03-05*
*Estimated build time: 2 days (Harry Phase 1, Ava Phase 2-3)*
*Cost: ~$0.30/month ongoing*
