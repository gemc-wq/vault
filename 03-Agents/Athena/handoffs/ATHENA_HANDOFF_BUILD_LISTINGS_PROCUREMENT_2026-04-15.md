# Handoff to Athena — Listings Pipeline + Procurement App Build

**From:** Ava (Strategy Agent)  
**To:** Athena (Master Orchestrator / Claude Opus 4.6 + Claude Code CLI)  
**Date:** 2026-04-15  
**Priority:** P1 (blocking Layer 0 compliance validator, shipping template fixes, procurement priority system)

---

## Overview

Two production systems are ready for build via Claude Code CLI:

1. **Listings Data Pipeline** — Ingests 6–10 GB Amazon All Listings Reports, detects deltas, pushes to Supabase + BigQuery
2. **Procurement Priority Overrides System** — Enriches reorder priorities based on Layer 0 compliance + stock risk

Both are critical path for Q2 2026 roadmap. Listings Pipeline unblocks Layer 0, which unblocks Procurement. Procurement unblocks the smart reorder queue.

---

## Project 1: Listings Data Pipeline

### Documentation
- **PRD v1.0:** `/Users/openclaw/Vault/02-Projects/listings-db/LISTINGS_PIPELINE_PRD.md`
  - Architecture (DuckDB + SQLite local snapshot → Supabase + BigQuery)
  - Schema (per-marketplace DBs, validation gates, delta detection)
  - Failure modes & recovery procedures
  - Integration contracts with Layer 0 + procurement

- **SOP v1.0:** `/Users/openclaw/Vault/02-Projects/listings-db/LISTINGS_PIPELINE_SOP.md`
  - Biweekly operational runbook
  - File download + validation steps
  - Pre-flight checklist
  - Recovery procedures (§9)

- **Codex Audit Report:** `/Users/openclaw/Vault/02-Projects/listings-db/CODEX_AUDIT_REPORT.md`
  - Adversarial review of PRD/SOP
  - 6 critical conditions for build (now integrated into PRD §5.x, §6.x, §10.x)
  - Build-readiness score: 78/100 → 90/100 (conditions now addressed)
  - Estimated build time: 3–5 days + 1–2 days testing

### Build Scope
**Claude Code CLI should deliver:**

1. **Python pipeline script** (`sync_listings_delta.py`)
   - Read 6–10 GB TSV files from `~/Downloads/`
   - Validate file naming, headers, encoding, currency, marketplace isolation
   - Parse via DuckDB for speed
   - Compute SHA-256 row hashes for delta detection
   - Write full snapshot to SQLite (one DB per marketplace)
   - Emit delta rows to CSV (NEW, UPDATED, REMOVED, UNCHANGED)
   - Push delta to Supabase (US + UK only, not DE)
   - Push delta to BigQuery (all Tier 1/Tier 2 marketplaces)
   - Generate compliance report for Layer 0

2. **SQLite schema** (`listings_us.db`, `listings_uk.db`, `listings_de.db`)
   - Per-marketplace file isolation (structural defense against contamination)
   - Tables: `amazon_listings_snapshot`, `listing_snapshots_meta`, `validation_log`
   - Constraints: NOT NULL on key fields, CHECK for marketplace isolation
   - Indexes: (seller_sku, cycle_id), (asin), (row_hash), (load_batch_id)
   - Materialized view: `current_snapshot` for latest cycle only

3. **Validation gates** (8 hard gates, from Codex audit conditions)
   - File naming: must match `{MP}_ALL_LISTINGS_{YYYY-MM-DD}.txt`
   - Header schema: validate against known columns
   - Encoding: UTF-8 or Latin-1, auto-convert
   - Row count sanity: flag if delta > ±20% from baseline
   - Currency cross-check: US prices should be USD range, UK in GBP range
   - Duplicate SKU detection: flag duplicates within same marketplace/cycle
   - Suppression spike detection: flag if REMOVED rate >2% or new SUPPRESSED >5%
   - Blank template spike: flag if merchant_shipping_group null/blank >0.5%

4. **Concurrency & recovery** (from Codex audit conditions)
   - Per-region lockfile at `~/.openclaw/workspace/locks/{marketplace}.lock`
   - Startup: verify DB filename matches meta row (prevent accidental region mixing)
   - Resume semantics: `--resume` flag to re-push delta to cloud only (skip local load)
   - State machine: validated → loaded_local → compliance_emitted → supabase_synced → bigquery_synced → approved

5. **Dead-letter handling** (from Codex audit conditions)
   - `dead_letter_listings_sync` table in each SQLite DB
   - Track batch number, retry count, last cursor, error details
   - Idempotent upsert keys for Supabase/BigQuery
   - Log failed payloads with timestamp for operator review

6. **CSV export contracts** (from Codex audit conditions)
   - Exact contracts defined with ordered headers, types, sample rows
   - `shipping_issues_{marketplace}_{cycle_id}.csv` for Layer 0
   - `delta_{marketplace}_{cycle_id}.csv` for analytics
   - `compliance_report_{cycle_id}.txt` for operator approval

7. **Test suite**
   - Unit tests for validation gates (each gate has test fixtures)
   - Integration test: load mock 1 GB file, verify delta, check Supabase sync
   - Failure test: simulate mid-load crash, test resume
   - Benchmarks: measure load time per GB, validate <15 min per marketplace

### Downstream Dependencies
- **Layer 0 Compliance Validator** — needs `amazon_listings_snapshot` + `merchant_shipping_group` per SKU to flag template violations
- **Procurement Priority System** — needs `blank_inventory` join against active listings to detect "stock at risk"
- **Shipping Template Bulk Fix** — needs `shipping_issues_*.csv` with wrong-template list for Jay Mark's upload

### Success Criteria
- ✅ Loads 6.7 GB US file in <15 minutes
- ✅ Detects delta correctly (NEW/UPDATED/REMOVED)
- ✅ Syncs to Supabase + BigQuery without errors
- ✅ All 8 validation gates pass on real data
- ✅ Compliance report emitted for Layer 0
- ✅ Zero marketplace contamination on test run

### Acceptance Test
Once built, Ava will:
1. Run pipeline against real US file (`~/Downloads/US Amazon Active+Listings+Report_04-14-2026.txt`, 6.7 GB)
2. Validate SQLite snapshot + delta
3. Run Layer 0 compliance validator against output
4. Report results to Cem

---

## Project 2: Procurement Priority Overrides System

### Documentation
- **PRD v1.0:** `/Users/openclaw/Vault/02-Projects/procurement/PROCUREMENT_SYSTEM_SPEC.md`
  - Business rules (FBA > FBM, Layer 0 compliance > velocity, stock at risk raises priority)
  - Schema (priority_queue, override_rules, audit_log)
  - Integration with Layer 0 compliance flags + blank inventory data

- **SOP v1.0:** `/Users/openclaw/Vault/02-Projects/procurement/PRIORITY_OVERRIDES_SOP.md`
  - Weekly reorder cycle trigger
  - Manual override procedures (for Cem/Harry)
  - Audit trail for all priority changes

- **Scope doc:** `/Users/openclaw/Vault/02-Projects/procurement/PRIORITY_OVERRIDES_SCOPE.md`
  - Defines what's in (priority enrichment, override rules, audit)
  - What's out (actual PO creation, payment, carrier integration)
  - Depends on: listings pipeline (for template compliance), Layer 0 (for stock risk)

### Build Scope
**Claude Code CLI should deliver:**

1. **Supabase schema** (already created, but Claude Code validates + improves)
   - `priority_overrides` table: (sku, priority_tier, reason, applied_by, applied_at, expires_at)
   - `override_rules` table: rule definitions (condition, priority_boost, audit_reason)
   - `priority_audit_log` table: immutable log of all changes
   - Constraints: FBA > FBM, Layer 0 compliance flags, stock_days_of_supply < threshold
   - Indexes: (sku), (priority_tier, updated_at), (applied_by, applied_at)

2. **Python scoring engine** (`calculate_priority.py`)
   - Input: blank inventory SKU + Layer 0 compliance status + sales velocity
   - Scoring rules:
     - FBA: base_priority = 2
     - FBM: base_priority = 1
     - Layer 0 compliance issue: +10 (urgent)
     - Stock at risk (days_of_supply < 7): +5
     - High velocity (sessions_30d > median): +2
   - Output: priority_tier (1–10) + reason_code
   - Upsert to `priority_overrides` table

3. **Weekly trigger** (cron integration with Cem's heartbeat or scheduled job)
   - Refresh priority scores for all active SKUs every Monday
   - Emit a report of top 50 SKUs by priority change
   - Notify Harry + Cem of urgent (tier 8+) overrides

4. **Manual override UI** (Supabase PostgREST API)
   - Endpoint: `POST /priority_overrides` (Cem approves override)
   - Endpoint: `GET /priority_queue?tier=8&limit=50` (view urgent SKUs)
   - All changes logged immutably to audit_log

5. **Integration with Layer 0**
   - Read `compliance_report_{cycle_id}.txt` emitted by listings pipeline
   - Parse Layer 0 flags (wrong template, SFP ineligible, etc.)
   - Map to SKUs and boost priority

6. **Test suite**
   - Unit tests for scoring logic (each rule has fixtures)
   - Integration test: load mock Layer 0 compliance data, verify scores
   - API test: POST override, verify audit log
   - Weekly trigger test: simulate cron execution

### Downstream Dependencies
- **Listings Pipeline** — needs compliance report for Layer 0 flags
- **Blank Inventory** — needs current stock levels to assess "at risk"
- **Reorder workflow** (Harry) — reads `priority_queue` weekly and acts

### Success Criteria
- ✅ Scores all SKUs based on compliance + inventory
- ✅ FBA prioritized over FBM
- ✅ Layer 0 compliance issues flagged urgent
- ✅ Weekly report accurate
- ✅ Manual overrides logged immutably
- ✅ Zero cross-marketplace contamination (US/UK/DE isolation)

### Acceptance Test
Once built, Ava will:
1. Load mock Layer 0 compliance data + blank inventory
2. Run scoring engine
3. Verify priority_queue output
4. Spot-check 10 SKUs manually
5. Report results to Cem

---

## Build Order & Dependencies

**Sequential (Listings Pipeline must finish first):**

```
Phase A: Listings Pipeline (3–5 days)
  ├─ DuckDB + SQLite + validation gates
  ├─ Supabase + BigQuery sync
  ├─ CSV exports (compliance report, shipping issues)
  └─ Test against 6.7 GB US file

Phase B: Procurement System (2–3 days, can start once Phase A is done)
  ├─ Scoring engine (depends on Layer 0 format from Phase A)
  ├─ Supabase schema + API
  ├─ Weekly cron trigger
  └─ Test with Layer 0 output from Phase A
```

**Parallel possible after Phase A is in code review:**
- Athena can read Listings Pipeline code while Claude Code builds Procurement
- But Procurement testing depends on Listings Pipeline delivery

---

## Files & References

### Vault locations (source of truth)
- `/Users/openclaw/Vault/02-Projects/listings-db/` — all listings pipeline docs
- `/Users/openclaw/Vault/02-Projects/procurement/` — all procurement docs
- `/Users/openclaw/Vault/03-Agents/Ava/LISTINGS_DATA_PIPELINE_ARCHITECTURE_v1.1.md` — earlier detailed architecture (reference only; PRD supersedes)

### GDrive backup
- `gdrive:Clawdbot Shared Folder/Brain/Projects/listings-db/`
- `gdrive:Clawdbot Shared Folder/Brain/Projects/procurement/`

### Test data
- **US Real Listings:** `/Users/openclaw/Downloads/US Amazon Active+Listings+Report_04-14-2026.txt` (6.7 GB, keep for testing)
- **BigCommerce prod DB:** `instant-contact-479316-i4` (BigQuery, for schema validation)
- **Supabase test project:** `auzjmawughepxbtpwuhe` (EU region, ready for sync testing)

### Credentials
- Supabase API key: in `~/.openclaw/workspace/.env` (OpenClaw will load)
- BigQuery service account: in `~/.openclaw/workspace/.env` (OpenClaw will load)
- No new credentials needed; all existing

### Cem's contact
- Primary: cem@ecellglobal.com (Telegram for urgent escalation)
- Escalation for build blockers: Cem + Harry

---

## Handoff Expectations

### What Athena will deliver:

1. ✅ **Listings Pipeline** (complete, tested, documented)
   - Python scripts ready to run
   - SQLite schemas created
   - Test suite passing
   - Codex audit conditions satisfied (78/100 → 90/100)

2. ✅ **Procurement System** (complete, tested, documented)
   - Scoring engine implemented
   - Supabase schema finalized
   - API endpoints documented
   - Weekly cron ready

3. ✅ **Documentation**
   - Implementation notes for each component
   - How to run, how to monitor, how to debug
   - Known limitations and workarounds

### What Ava will do next:

1. ✅ **Test Listings Pipeline** with real US 6.7 GB file
2. ✅ **Validate Layer 0** compliance output
3. ✅ **Test Procurement scoring** with Layer 0 output
4. ✅ **Run both systems end-to-end** before going live
5. ✅ **Report to Cem** on success + any issues

### Timeline

- **Athena build:** 5–7 days (3–5 for listings + 2–3 for procurement, with some overlap)
- **Ava testing & validation:** 2–3 days after delivery
- **Go-live:** Following Monday (2026-04-28 target)

---

## Questions for Athena

1. Can you estimate the exact build time once you read the docs?
2. Do you need Cem to clarify any scope items before starting?
3. Any blockers on environment access or credentials?

---

**Ready for Athena to begin.**

*Prepared by: Ava | Approved by: (awaiting Cem confirmation)*
