# Mac Studio Build Handoff — Listings Data Pipeline

> ⚠️ **STATUS: SUPERSEDED (2026-04-16)**
> The build was executed on the **laptop**, not the Mac Studio. This handoff
> is preserved for historical reference but is no longer the active plan.
> Current authoritative docs: [[LISTINGS_PIPELINE_PRD]] v1.2 + [[LISTINGS_PIPELINE_SOP]] v1.2.
>
> **What actually shipped (as of 2026-04-16):**
> - Pipeline runs on **laptop** at `~/Desktop/Repos/amazon-listings-pipeline/`
> - Full Next.js web UI at `localhost:3001` (5 pages, Modern Style Guide 2.0)
> - Inventory cache pluggable: Supabase (default) or BigQuery (fallback)
> - Verified end-to-end on 6.7 GB / 3.1M-row US catalog in 150 sec
> - Identified 1,888,789 wrong-template listings (60% of catalog)
> - Repo: github.com/gemc-wq/amazon-listings-pipeline
>
> Mac Studio may still take this over later for unattended cron runs;
> if so, the handoff steps below are still valid but the "build from scratch"
> framing no longer applies — it's now a `git clone` + `pip install -e .` job.

---

> **From:** Laptop session (Cem + Claude, 2026-04-15)
> **To:** Mac Studio Claude Code session (originally — see above)
> **What to build:** The listings data pipeline per the PRD + SOP in this folder

---

## Read These First (in order)

1. [[LISTINGS_PIPELINE_PRD]] — full spec (v1.1, all 6 Codex conditions addressed)
2. [[CODEX_AUDIT_REPORT]] — Codex gave 78/100, verdict "proceed_with_conditions", all conditions now addressed
3. [[LISTINGS_PIPELINE_SOP]] — operator runbook (how Cem will actually use this)
4. [[HARRY_HANDOFF_LISTINGS_DELTA_DB]] — Ava's earlier spec (reference only — this PRD supersedes it, but her SQLite schema + delta script are the starting point)
5. [[02-Projects/procurement/LAYER0_COMPLIANCE_INTEGRATION]] — how this pipeline feeds the procurement-system

## Why Mac Studio (not laptop)

- The 6–10 GB source files are downloaded on Mac Studio
- SQLite snapshot files live at `~/.openclaw/workspace/data/` on Mac Studio
- DuckDB bulk load needs local disk I/O to the same machine as the source files
- Harry's existing work is on Mac Studio (SSH: 100.91.149.92)
- Supabase + BigQuery pushes go over the network from either machine — no difference

## What Already Exists on Mac Studio

Check these before building from scratch:

- `~/.openclaw/workspace/data/listings.db` — Ava's earlier SQLite file (may contain contaminated data — do NOT reuse, but check if the schema matches)
- `~/.openclaw/workspace/scripts/sync_listings_delta.py` — Ava's delta script (reference for SKU parsing, chunked loading)
- Harry may have built parts of Phase 1 per [[HARRY_HANDOFF_LISTINGS_DELTA_DB]] — check with Cem

## What to Build (3–5 days estimated)

### Day 1: Bootstrap + load engine
- `bootstrap.sh --region {US|UK}` — atomic DB init per PRD §4.4
- DuckDB bulk loader for 6–10 GB TSV → SQLite
- Validation gates 1–23 per PRD §6
- 10 guardrails (G1–G10) per PRD §6.0

### Day 2: Delta detection + compliance scan
- SHA-256 row hashing
- Delta classification (NEW/UPDATED/UNCHANGED/REMOVED) per PRD §9
- Shipping template compliance scan vs `blank_inventory`
- Output: `shipping_issues_*.csv`, `compliance_flags_*.csv`

### Day 3: Downstream sync
- Supabase push (`active_listings`, `listings_delta`, `listings_shipping_issues`)
- BigQuery MERGE (`listings_master`, `listings_history`)
- Dead-letter handling per PRD §5.4
- Region lockfile per PRD §4.5

### Day 4: CLI + operator UX
- `load.sh --region {MP} --file {path}` — full pipeline entry point
- `load.sh --resume {cycle_id}` — resume from last checkpoint
- `rollback.sh --region {MP} --cycle {cycle_id}`
- `approve.sh {cycle_id}`
- `status.sh` — show current state of all marketplace DBs
- Pipeline report JSON emission

### Day 5: Testing + benchmark
- Unit tests for guardrails, hashing, delta detection
- Integration test with a real 9 GB file
- Benchmark: target ≤ 20 min per marketplace (Codex said 15–20 min realistic)
- Failure-path testing: truncated file, wrong marketplace, concurrent runs

## Key Technical Decisions (already made)

| Decision | Choice | Rationale |
|---|---|---|
| Load engine | DuckDB | ~6 min for 9 GB vs pandas ~30 min; no server like MySQL |
| Persistent store | SQLite (one file per marketplace) | Ava's choice, crash-safe, portable, no daemon |
| Marketplace isolation | Per-file DB + `_meta_marketplace` CHECK + lockfiles | Prevents Ava's contamination failure structurally |
| Downstream hot | Supabase (same project as procurement) | Shared with procurement-system, RLS-enabled |
| Downstream cold | BigQuery `amazon_listings` dataset | Historical + analytics |
| State tracking | `listing_snapshots_meta.status` column | 10-state lifecycle per PRD §4.3 |

## Credentials Needed

- Supabase service key — should already be in `~/.openclaw/workspace/.env` on Mac Studio
- BigQuery service account — should already be configured for GCP project `instant-contact-479316-i4`
- If either is missing, ask Cem

## Do NOT

- Do NOT edit the PRD/SOP from the Mac Studio session — those are owned by the laptop session and live in Obsidian
- Do NOT touch the procurement-system repo — that's a separate session
- Do NOT touch the amazon-unified-score repo — Layer 0 will be added after this pipeline is operational
- Do NOT reuse Ava's `listings.db` file — it has contaminated US/UK/DE data mixed together
- Do NOT use SP-API to pull listings reports — manual download only (Cem's explicit decision)

## Success Criteria

Pipeline is "done" when:

1. `bootstrap.sh --region US` and `bootstrap.sh --region UK` create clean per-marketplace DBs
2. `load.sh --region US --file ~/Downloads/US_ALL_LISTINGS_*.txt` completes in ≤ 20 min
3. All 10 guardrails (G1–G10) fire correctly on deliberately wrong inputs
4. Delta detection produces plausible NEW/UPDATED/UNCHANGED/REMOVED counts
5. Supabase `active_listings` is populated with US + UK rows (verifiable via Supabase dashboard)
6. BigQuery `listings_master` has the delta rows (verifiable via BQ console)
7. `shipping_issues_us_*.csv` and `shipping_issues_uk_*.csv` are emitted with correct contract format
8. `rollback.sh` successfully reverts a cycle
9. Concurrent `load.sh US` + `load.sh US` correctly blocks the second invocation
10. A second cycle produces a meaningful delta (not all-NEW)
