# Vault Schema — Ecell Global Knowledge Base
*Pattern: LLM Wiki (Karpathy/Tobi Lutke). LLM maintains the wiki. Human curates sources and asks questions.*

## Structure

```
Vault/
├── 00-Company/          # Canonical docs (Cem approves changes)
│   └── compiled/        # Auto-generated: PROJECT_BOARD, BLOCKERS, VAULT_HEALTH
├── 01-Wiki/             # LLM-maintained topic pages (YOU write/update these)
│   ├── 01-customer-service/
│   ├── 02-sales-data/
│   ├── 03-production/
│   ├── 04-shipping/
│   ├── 05-inventory/
│   ├── 06-design-automation/
│   ├── 08-infrastructure/
│   ├── 09-creative-pipeline/
│   ├── 10-listingforge/
│   ├── 11-product-intelligence/
│   ├── 12-org/
│   ├── 13-saas-spinoff/
│   └── 14-goheadcase/
├── 02-Projects/         # Project specs, briefs, deliverables
├── 03-Agents/           # Raw agent memory logs (NEVER modify these)
│   ├── Ava/memory/      # Ava's daily logs
│   ├── Harry/memory-imac/  # Harry's logs (synced from iMac)
│   ├── Hermes/          # Hermes operational data
│   ├── Athena/          # Athena/ZEUS logs
│   └── Sentinel/        # Infrastructure monitoring specs
├── Raw/                 # Imported documents (immutable)
├── INDEX.md             # Master index — update on every ingest
└── CLAUDE.md            # THIS FILE — the schema
```

## Three Layers

| Layer | Who Writes | Who Reads | Rule |
|-------|-----------|-----------|------|
| **Raw** (03-Agents/, Raw/) | Agents automatically | LLM during ingest | NEVER modify. Append-only. |
| **Wiki** (01-Wiki/) | LLM (you) | Everyone | Update freely. Cross-reference with [[wikilinks]]. |
| **Compiled** (00-Company/compiled/) | vault_compiler.py | Everyone | Auto-generated nightly. Don't edit manually. |

## Operations

### Ingest (when processing a new source or agent log)
1. Read the source completely
2. Identify durable facts worth keeping (decisions, process knowledge, technical details, corrections from Cem)
3. For each fact, find the right wiki topic page in 01-Wiki/
4. Update existing pages (add under "## Recent Updates" section) or create new ones
5. Add [[wikilinks]] to cross-reference related pages
6. Update INDEX.md with any new pages
7. Append to 00-Company/compiled/CHANGE_LOG.md

### Query (when answering a question about Ecell)
1. Read INDEX.md to find relevant wiki pages
2. Read those pages
3. Synthesise answer with citations to wiki pages
4. If the answer contains reusable knowledge, file it as a new wiki page or update an existing one
5. **Don't let good answers disappear into chat history**

### Lint (periodic health check)
1. Pages not updated in 30+ days — flag as potentially stale
2. Claims that newer sources contradict — flag and update
3. Orphan pages with no inbound [[wikilinks]] — add links or merge
4. Important concepts mentioned but lacking their own page — create stubs
5. Duplicate information across pages — consolidate

## What Makes Good Wiki Content

**KEEP (durable knowledge):**
- Decisions made by Cem and why
- How processes work (fulfillment flow, design pipeline, SKU parsing)
- Technical facts (schemas, API details, credentials locations, config)
- Business metrics and benchmarks
- Corrections — when someone was wrong and what's actually true
- Agent roles, responsibilities, and boundaries

**SKIP (transient noise):**
- "Working on X today" status updates
- Debugging logs and error traces
- Session start/end timestamps
- Anything that will be false next week

## Ecell Global Context
- Licensed tech accessories, POD/DTC, $5.5-6M revenue
- 1.89M SKUs, 3.44M Amazon US listings, 38 PH staff
- NFL, NBA, One Piece, Naruto, Harry Potter, Peanuts, Ubisoft
- North Star: #1 licensed tech accessories company
- 3 Metrics: Coverage, Speed, Intelligence
- CEO: Cem Celikkol
