# Listings Data Pipeline — PRD v1.2

> **Owner:** Cem | **Author:** amazon-unified-score session (Cem + Claude)
> **Date:** 2026-04-16 | **Status:** v1.2 — enriched with implementation findings
> **Builds on:** [[HARRY_HANDOFF_LISTINGS_DELTA_DB]] (Ava, 2026-03-30) and [[SHIPPING_TEMPLATE_BULK_FIX_BRIEF]] (Ava, 2026-03-30)
> **Related:** [[02-Projects/procurement/PROCUREMENT_SYSTEM_SPEC]], [[02-Projects/procurement/LAYER0_COMPLIANCE_INTEGRATION]]
>
> **Changelog**
> - **v1.2 (2026-04-16):** Documented inventory cache subsystem (§5.6), validation gate refinements G5/G8 (§6.7), real performance numbers from production runs (§7.5), CLI inventory commands (§8.4), known-issues callout for editable-install PYTHONPATH (§13.2), Web UI 4-leaderboard layout + In Stock filter (§16.7). Added open questions on snapshot history dedupe and inventory source preference (§15).
> - **v1.1 (2026-04-16):** Added §16 — Web UI specification (Listings Compliance Manager, Next.js 15).
> - **v1.0 (2026-04-15):** Initial PRD post Codex adversarial audit (responses preserved in §15).

---

## 1. Executive Summary

Head Case Designs downloads 6–10 GB Amazon All Listings Reports manually from Seller Central (US + UK every cycle, DE ad-hoc, FR/IT/ES never). These files are the **only authoritative source** for shipping template assignments, and they contain ~4 million rows per marketplace. Without a structured pipeline, every analytical or operational job that needs listings data either (a) re-parses the full 9 GB file from `~/Downloads/` or (b) operates on stale data.

This PRD specifies a pipeline that:

1. **Ingests** the 9 GB tab-delimited files efficiently from `~/Downloads/`
2. **Stores** a full per-marketplace snapshot locally for reproducibility
3. **Computes** a row-level delta against the previous cycle (SHA-256 hash) so only changed rows propagate downstream
4. **Pushes** the delta to Supabase (for procurement, dashboards, Jay Mark, and the Layer 0 validator) and BigQuery (for historical analytics)
5. **Validates** every input file before loading to prevent cross-marketplace contamination
6. **Emits** a shipping-template compliance report on every run for the Layer 0 / unified-score consumer

The pipeline is the **foundation for three downstream systems** that already exist or are being built:

- **procurement-system** (Harry, Phase 1 live) — needs `blank_inventory` cross-checks against active listings
- **amazon-unified-score Layer 0** (this session) — needs current shipping template per SKU to validate compliance
- **shipping template bulk fix** (Jay Mark, P1 urgent) — needs a clean wrong-template list to drive flat-file uploads

**Critical constraint:** No SP-API pulls for listings reports. Cem has explicitly chosen to keep the orders pull intact and not risk Amazon throttling by introducing additional report polling. Manual download is the ingress.

---

## 2. Context & Problem Statement

### 2.1 Why this exists

Three concurrent problems converge on listings data:

| Problem | Source Doc | Magnitude |
|---|---|---|
| ~122,000 listings on the wrong shipping template across US + UK | SHIPPING_TEMPLATE_BULK_FIX_BRIEF | 76k US + 45k UK + ~1.5k edge cases |
| Layer 0 compliance validator can't run without per-listing template + warehouse stock joined | This PRD | Blocks Layer 0 build |
| Procurement reorder priority can't be boosted for "Prime promise at risk" SKUs without listings data | LAYER0_COMPLIANCE_INTEGRATION §3 | Blocks procurement priority enrichment |

All three need the same primary data: a clean, current, queryable per-marketplace listings snapshot. None of them want to re-parse the 9 GB file each time.

### 2.2 What exists today (do NOT rebuild)

Ava handed off a Phase 1 brief on 2026-03-30 (`HARRY_HANDOFF_LISTINGS_DELTA_DB.md`) that specifies:

- SQLite on Mac Studio at `~/.openclaw/workspace/data/listings.db` (a **single shared file**, see §2.2.1 below for why this is changed in v1)
- `amazon_listings_snapshot` and `listing_snapshots_meta` tables (full schema in §5.1 below)
- `listings_delta` and `listings_shipping_issues` tables in Supabase (full schema in §5.2)
- Python script `sync_listings_delta.py` using `pandas.read_csv(chunksize=50000)` for chunked ingestion
- A working SKU parser that strips F-prefix and extracts product_type / device_code / design_code

**Status of Phase 1:** Unconfirmed. Owner = Harry. Cem to verify whether the script is built, partially built, or not yet started, before this PRD's implementation phase begins.

### 2.2.1 Critical lesson from Ava's earlier attempt — marketplace contamination

Per Cem (2026-04-15): **Ava's earlier listings ingestion attempt failed** because US/UK/DE data ended up written on top of each other in the same table with no enforceable separation. The result was unusable because:

- Same `seller_sku` exists in multiple marketplaces with different prices, currencies, and shipping templates
- A US row would be overwritten by a UK row (or vice versa) on the next load
- The data was structurally indistinguishable after the load — no recovery path

This PRD treats marketplace contamination as the **#1 failure mode to design out**, not just to validate against. See §6.0 (Guardrails — Marketplace Isolation) for the structural defences. The schema design in §5.1 is changed from Ava's brief to enforce isolation at the file system level: **one SQLite file per marketplace**, not one shared file with a region column. A bug, a typo, or a confused operator cannot accidentally mix marketplaces because the target database literally does not contain the wrong marketplace's data.

### 2.3 What's missing from the Phase 1 brief (what this PRD adds)

| Gap | Why It Matters | Where Addressed |
|---|---|---|
| File validation (naming, headers, encoding, currency cross-check) | Wrong file in wrong DB = silent cross-marketplace corruption | §6 Validation |
| Performance target & alternative backends | 9 GB through pandas takes 20–40 min — may not be acceptable | §7 Performance |
| Failure modes (mid-load crash, Supabase 500, disk full) | No recovery path defined → manual cleanup | §10 Failure Modes |
| Marketplace tier model | DE/FR/IT/ES treatment ambiguous | §3 Scope |
| Layer 0 integration contract | Required for compliance flag emission | §11 Integration |
| Restricted-prefix awareness (HB6/HB7/HDMWH/HSTWH/H89/H90) | PH equipment gap creates a "no overflow" severity | §11 Integration |
| Disaster recovery | Mac Studio dies → rebuild from scratch? | §13 Disaster Recovery |
| Schema fields missing from current spec (asin, fulfillment_channel, item_condition, row_hash) | Layer 0 + procurement need these | §5.1 Schema |
| Cron / trigger automation | Manual invocation per file is OK now but should be scriptable | §8 SOP entry point |
| Data retention policy | SQLite will grow forever | §12 Storage |

### 2.4 The 6–10 GB file challenge

Per Cem's confirmation (2026-04-15) and Ava's brief, raw All Listings Reports are 6–10 GB tab-delimited text files per marketplace, ~4 million rows each. This is at the edge of what's tractable with simple tools:

| Approach | Time on 9 GB | Pros | Cons |
|---|---|---|---|
| `pandas.read_csv(chunksize=50000)` | ~20–40 min | Pure Python, no extra deps, Ava's existing choice | Slow; high memory pressure on Mac Studio |
| `LOAD DATA INFILE` (MySQL 8) | ~3–5 min | Native bulk load, designed for this size | Requires running MySQL locally; new dependency |
| DuckDB `read_csv_auto` | ~5–8 min | Single binary, no server, columnar engine, Python API | New dependency, less battle-tested in this team |
| `sqlite3` `.import` CLI | ~10–15 min | Stays within Ava's chosen backend | No header validation; less ergonomic for delta |
| Apache Spark / Polars | ~3–6 min | Engineered for this scale | Overkill, new dependency |

**This PRD recommends DuckDB** as the load engine while keeping SQLite as the persistent snapshot store. Rationale: DuckDB reads CSV/TSV at ~1.5 GB/s on Apple Silicon, has a Python API that integrates cleanly with Ava's script structure, and can write directly to a SQLite-compatible file. It's a single binary install with zero infrastructure (no server, no daemon).

This is **a deviation from Ava's brief** and needs Codex/Cem review. The alternatives are:

- **(a)** Stay with chunked pandas (Ava's choice) — slow but simple, no new dep
- **(b)** Switch to DuckDB (this PRD's recommendation) — fast, single binary
- **(c)** Switch to MySQL + LOAD DATA INFILE (Perplexity doc's choice) — fast, more complex

Codex should evaluate trade-offs in §7.

---

## 3. Scope

### 3.1 In Scope

- Manual file ingestion from `~/Downloads/` (no API automation for listings)
- Per-marketplace data isolation at every layer (file → DB → table → query)
- Validation gates: file naming, header schema, encoding, row count sanity, currency cross-check
- SHA-256 row hashing for delta detection
- Local persistent snapshot (full catalog, all rows)
- Cloud delta push (Supabase + BigQuery)
- Shipping template compliance report emission
- Restricted-prefix detection (PH equipment gap)
- Failure recovery and rollback procedures
- Marketplace tier model (Tier 1 automated, Tier 2 ad-hoc, Tier 3 manual)
- Integration contracts with procurement-system, unified-score, and the bulk-fix workflow

### 3.2 Out of Scope

- SP-API automation of listings report generation (explicit Cem decision)
- Real-time listing updates (the pipeline is biweekly batch by design)
- Listing content quality (titles, bullets, images) — that's `listing-forge` / `listings-intelligence`
- Order data ingestion (separate pipeline, owned by procurement / Hermes)
- Inventory data ingestion (owned by `procurement-system` via `zero_dataset.inventory`)
- The bulk shipping-template upload itself (Jay Mark's flat-file upload via Seller Central)
- Listing creation / suppression / IP takedown response (manual, human-only)
- Translation / localisation (DE/FR/IT/ES — listings are read as-is)

### 3.3 Marketplace Tier Model

| Tier | Marketplaces | Treatment | Owner Justification |
|---|---|---|---|
| **Tier 1** | US, UK | Full pipeline every cycle: download → validate → load → delta → push to Supabase + BQ | Primary revenue, Layer 0 validator depends on these, biweekly cadence |
| **Tier 2** | DE | Same pipeline, monthly or on-demand cycle, BQ destination only (no Supabase push) | DE has stock but limited sales velocity; Cem reviews ad-hoc |
| **Tier 3** | FR, IT, ES | Manual download only when needed; same scripts but no scheduled run | Negligible revenue contribution; pipeline exists for parity |

---

## 4. Architecture

### 4.1 Overview

```
                    ┌────────────────────────┐
                    │  Cem manually downloads │
                    │  from Seller Central    │
                    │  (US + UK biweekly,     │
                    │   DE monthly, others    │
                    │   ad-hoc)               │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  ~/Downloads/           │
                    │  {MP}_ALL_LISTINGS_     │
                    │  {YYYY-MM-DD}.txt       │
                    │  (6-10 GB tab TSV)      │
                    └───────────┬────────────┘
                                │
                                │ ./load.sh US YYYY-MM-DD
                                │ (or watched-folder trigger)
                                ▼
                ┌─────────────────────────────────┐
                │  TIER 1 — Local staging          │
                │  Mac Studio                      │
                │                                  │
                │  ┌─────────────────────────┐    │
                │  │ Step 1: Validation gate │    │
                │  │  - filename pattern     │    │
                │  │  - header schema        │    │
                │  │  - encoding (utf8/latin1)│    │
                │  │  - row count vs prev    │    │
                │  │  - currency range check │    │
                │  └────────────┬────────────┘    │
                │               │ pass            │
                │               ▼                  │
                │  ┌─────────────────────────┐    │
                │  │ Step 2: Bulk load       │    │
                │  │  DuckDB read_csv_auto   │    │
                │  │  → raw_listings_{MP}    │    │
                │  │  ~5-8 min for 9 GB      │    │
                │  └────────────┬────────────┘    │
                │               │                  │
                │               ▼                  │
                │  ┌─────────────────────────┐    │
                │  │ Step 3: Hash + parse    │    │
                │  │  SHA-256 per row        │    │
                │  │  SKU decompose          │    │
                │  │  F-prefix flag          │    │
                │  │  base_sku derivation    │    │
                │  └────────────┬────────────┘    │
                │               │                  │
                │               ▼                  │
                │  ┌─────────────────────────┐    │
                │  │ Step 4: Delta classify  │    │
                │  │  vs amazon_listings_    │    │
                │  │      snapshot (SQLite)  │    │
                │  │  → NEW/UPDATED/         │    │
                │  │    UNCHANGED/REMOVED    │    │
                │  └────────────┬────────────┘    │
                │               │                  │
                │               ▼                  │
                │  ┌─────────────────────────┐    │
                │  │ Step 5: Persist         │    │
                │  │  SQLite snapshot append │    │
                │  │  + meta row             │    │
                │  └────────────┬────────────┘    │
                │               │                  │
                │               ▼                  │
                │  ┌─────────────────────────┐    │
                │  │ Step 6: Compliance      │    │
                │  │  scan vs blank_inventory│    │
                │  │  + restricted-prefix    │    │
                │  │  Output: queue CSVs     │    │
                │  └────────────┬────────────┘    │
                └────────────────┼────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
   ┌──────────────────┐ ┌─────────────────┐ ┌──────────────────┐
   │ TIER 2 — BigQuery│ │ TIER 3 — Supabase│ │  Local CSVs       │
   │  Cold archive    │ │  Hot operational │ │  ~/.openclaw/out/ │
   │                  │ │                  │ │                   │
   │  delta only      │ │  delta + active  │ │  fix_template_    │
   │  ~1-3 GB         │ │  US+UK only      │ │  {mp}_{date}.csv  │
   │                  │ │                  │ │  for Jay Mark     │
   │  amazon_listings │ │  listings_delta  │ │                   │
   │  .listings_master│ │  active_listings │ │  layer0_flags_    │
   │  .listings_      │ │  listings_       │ │  {mp}_{date}.csv  │
   │   history (SCD2) │ │   shipping_issues│ │  for procurement  │
   │                  │ │  compliance_flags│ │                   │
   └──────────────────┘ └─────────────────┘ └──────────────────┘
              │                  │                  │
              └──────────────────┴──────────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  Downstream consumers         │
                  │  - procurement-system (read)  │
                  │  - amazon-unified-score       │
                  │  - openclaw / Hermes / Ava    │
                  │  - Jay Mark (template fixes)  │
                  │  - Wednesday cron audit       │
                  └──────────────────────────────┘
```

### 4.2 Why three storage tiers (and not fewer)

| Tier | Tool | Purpose | Why this tool |
|---|---|---|---|
| **1 — Local snapshot** | SQLite (Ava's choice) | Full catalog persistence, source of truth for delta computation | Already specced; no server; portable; queryable from any tool that reads SQLite |
| **2 — Cold archive** | BigQuery `amazon_listings` dataset | Historical record (SCD2), cross-marketplace analytics, audit trail | Already exists in stack; partitioned + clustered storage handles 24M+ rows efficiently; cheap at delta-only volumes |
| **3 — Hot operational** | Supabase (project `auzjmawughepxbtpwuhe`) | Live operational data for procurement, dashboards, Layer 0, Jay Mark | Already shared with procurement-system; row-level security; REST API; only delta + active subset stays here |

DuckDB is the **load engine for Tier 1**, not a fourth storage tier. It reads the raw TSV → writes directly to SQLite.

### 4.3 Deviation from the Perplexity pipeline doc

The Perplexity `listings-data-pipeline-architecture` doc proposed MySQL + `LOAD DATA INFILE` for Tier 1. This PRD substitutes **DuckDB → SQLite** because:

1. SQLite is already Ava's chosen persistence layer — keeps one DB file, no MySQL daemon to manage
2. DuckDB does the bulk-load heavy lifting at MySQL-comparable speed without requiring a server
3. Mac Studio can run DuckDB as a single binary; no service to start, stop, or monitor
4. Single-file SQLite is trivially backed up to iCloud/Time Machine; MySQL data dirs are not

**Codex challenge:** Is DuckDB → SQLite materially worse than MySQL → MySQL for delta detection on 4M rows? Bench both in the audit phase.

### 4.3 Cycle State Machine (Codex condition 1)

Every pipeline run for a single marketplace follows a deterministic state machine. Each state is persisted in `listing_snapshots_meta.status` so that a crash at any point can be resumed from the last successful checkpoint without re-running completed phases.

```
  ┌────────────┐
  │  INITIATED │  load.sh invoked; lockfile acquired; meta row created
  └──────┬─────┘
         │ validation gates pass
         ▼
  ┌────────────┐
  │ VALIDATED  │  source file passes all G0–G5 guardrails + gates 1–17
  └──────┬─────┘
         │ DuckDB bulk load + hash + parse + delta classify complete
         ▼
  ┌──────────────┐
  │ LOADED_LOCAL │  SQLite snapshot committed (authoritative success boundary)
  └──────┬───────┘
         │ compliance scan vs blank_inventory
         ▼
  ┌──────────────────┐
  │ COMPLIANCE_DONE  │  shipping_issues + compliance_flags CSVs emitted locally
  └──────┬───────────┘
         │ Supabase upsert of active_listings, listings_delta, listings_shipping_issues
         ▼
  ┌──────────────────┐
  │ SUPABASE_SYNCED  │  operational tables updated; dead-letter captured if partial failure
  └──────┬───────────┘
         │ BigQuery MERGE of delta into listings_master + history append
         ▼
  ┌──────────────────┐
  │ BIGQUERY_SYNCED  │  cold archive updated
  └──────┬───────────┘
         │ output CSVs written + pipeline report emitted
         ▼
  ┌────────────┐
  │ COMPLETED  │  lockfile released; Slack notification posted
  └──────┬─────┘
         │ operator runs approve.sh
         ▼
  ┌────────────┐
  │ APPROVED   │  operator confirms sanity checks passed; Slack summary posted
  └────────────┘

  ERROR STATES (any phase can transition here):
  ┌──────────────────────┐
  │ FAILED               │  generic failure; logged with error detail
  ├──────────────────────┤
  │ FAILED_CONTAMINATION │  G8 or any contamination gate fired; zero state committed
  ├──────────────────────┤
  │ ROLLED_BACK          │  operator or script explicitly rolled back a completed cycle
  └──────────────────────┘
```

**Key invariants:**

1. **`LOADED_LOCAL` is the only authoritative success boundary.** Everything before it can be retried by re-running `load.sh`. Everything after it is an asynchronous sync stage that can be resumed independently.
2. **Resume semantics:** `./load.sh --resume {cycle_id}` reads the current status from `listing_snapshots_meta` and continues from the next uncompleted phase. It NEVER re-runs VALIDATED or LOADED_LOCAL — those require a fresh `load.sh` invocation with a source file.
3. **State transitions are monotonic** — a cycle can only move forward or to an error state. There is no path from COMPLETED back to LOADED_LOCAL.
4. **Each state transition is a single SQLite UPDATE** on the meta row, committed atomically.

### 4.4 Bootstrap / Init Procedure (Codex condition 3)

Creating a new marketplace DB must be atomic. If the script crashes between table creation and `_meta_marketplace` insertion, the file exists with no anchor row and all subsequent loads fail with a confusing CHECK error.

```bash
./bootstrap.sh --region US
```

The script:

1. Checks if `listings_us.db` already exists — if yes, refuses to overwrite (prevents accidental re-init)
2. Creates a temporary file `listings_us.db.tmp`
3. Runs ALL schema DDL + the `_meta_marketplace` INSERT in **one SQLite transaction**:

```sql
BEGIN EXCLUSIVE;
  CREATE TABLE _meta_marketplace (...);
  INSERT INTO _meta_marketplace (region, db_filename) VALUES ('US', 'listings_us.db');
  CREATE TABLE amazon_listings_snapshot (...);
  CREATE TABLE listing_snapshots_meta (...);
  CREATE TABLE dead_letter_sync (...);  -- see §5.4
  -- all indexes
COMMIT;
```

4. On successful commit, renames `listings_us.db.tmp` → `listings_us.db` (atomic on POSIX filesystems)
5. On any error, deletes `listings_us.db.tmp` — no half-initialised file remains
6. Writes an audit log entry: `bootstrap --region US exit=0`

**The rename trick is the safety net.** If the transaction commits but the process dies before rename, the `.tmp` file exists but the canonical path does not — next bootstrap detects no canonical file and can retry safely. If the rename succeeds, the file is fully initialised. There is no intermediate state where a partially-valid DB exists at the canonical path.

### 4.5 Region Lockfile & Concurrency Control (Codex condition 6)

Every `load.sh` invocation acquires an exclusive filesystem lock before touching any storage:

```
~/.openclaw/workspace/locks/
├── listings_us.lock
├── listings_uk.lock
└── listings_de.lock
```

**Lock protocol:**

1. `load.sh --region US` attempts `flock --nonblock ~/.openclaw/workspace/locks/listings_us.lock`
2. If lock acquired → proceed
3. If lock already held → exit with code 20 and message `ERROR: listings_us is already being loaded by PID {pid}. Wait or investigate.`
4. Lock is released automatically when the process exits (success, failure, or crash) via POSIX `flock` semantics
5. The lock file contains the PID, start time, and source filename for diagnostics:

```
PID=12345
STARTED=2026-04-15T09:01:02
FILE=US_ALL_LISTINGS_2026-04-15.txt
```

**What this prevents:**

- Cem runs `load.sh US` from his terminal; Harry SSHes in and accidentally runs it again → blocked by lock
- A cron job fires while a manual run is in progress → blocked
- Two `load.sh US` processes racing each other → impossible; one acquires, one exits immediately

**Cross-marketplace concurrency is allowed:** `load.sh US` and `load.sh UK` CAN run in parallel on separate DB files (no shared state), though the SOP recommends sequential to manage memory pressure (see SOP §4.2). The lockfiles are per-marketplace, not global.

**DB filename verification on startup (Codex condition 6b):**

After acquiring the lock, `load.sh` verifies that the DB file it's about to open matches expectations:

```python
meta = conn.execute("SELECT region, db_filename FROM _meta_marketplace").fetchone()
assert meta['region'] == args.region, f"DB {args.db_path} claims region={meta['region']} but --region={args.region}"
assert meta['db_filename'] == os.path.basename(args.db_path), f"DB internal name={meta['db_filename']} but file is {args.db_path}"
```

This catches the rename-attack scenario (operator renames `listings_uk.db` to `listings_us.db`).

---

## 5. Data Model

### 5.1 SQLite (local snapshot — Tier 1) — ONE FILE PER MARKETPLACE

**Hard rule (per §6.0 guardrails):** Each marketplace has its own SQLite file at `~/.openclaw/workspace/data/listings_{mp}.db` where `{mp}` is one of `us`, `uk`, `de`, `fr`, `it`, `es`. There is no shared database. Cross-marketplace queries happen only at the BigQuery layer (Tier 2) where the `region` partition column is mandatory.

| File | Marketplace | Tier | Cadence |
|---|---|---|---|
| `listings_us.db` | US | 1 | Biweekly |
| `listings_uk.db` | UK | 1 | Biweekly |
| `listings_de.db` | DE | 2 | Monthly / ad-hoc |
| `listings_fr.db` | FR | 3 | Manual only |
| `listings_it.db` | IT | 3 | Manual only |
| `listings_es.db` | ES | 3 | Manual only |

Each file contains the same schema. The `region` column inside is technically redundant (every row in `listings_us.db` is region='US' by construction) but is retained for two reasons:

1. **Triple-belt-and-braces against contamination.** If an operator accidentally points the script at the wrong DB file, the `region` column won't match the file name and Gate 0 (file/DB sanity check) catches it.
2. **Easy export to Tier 2 (BigQuery).** When the delta is pushed to BigQuery's unified `listings_master` table, the `region` column is already populated.

```sql
-- Identical schema in EVERY listings_{mp}.db file
CREATE TABLE amazon_listings_snapshot (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    region                  TEXT NOT NULL CHECK (region = (SELECT region FROM _meta_marketplace LIMIT 1)),
    seller_sku              TEXT NOT NULL,
    asin                    TEXT,                     -- asin1 from Amazon column
    listing_id              TEXT,
    item_name               TEXT,

    -- Parsed SKU components
    is_fba                  INTEGER NOT NULL,         -- 0/1, true if SKU starts with F (with exceptions)
    product_type            TEXT,                     -- e.g. HTPCR, HDMWH, HB6
    device_code             TEXT,                     -- e.g. IPH17PMAX, 900X400X4
    design_code             TEXT,                     -- e.g. NARUGRAT
    variant_code            TEXT,                     -- e.g. PAT
    base_sku                TEXT NOT NULL,            -- product_type-device_code (join key for blank_inventory)

    -- Pricing & inventory (as reported by Amazon — not authoritative for blank stock)
    price                   REAL,
    currency                TEXT,                     -- USD/GBP/EUR (derived from region)
    quantity                INTEGER,                  -- Amazon's quantity field; ≥0 = active

    -- Fulfilment & shipping
    fulfillment_channel     TEXT,                     -- 'AMAZON_NA' (FBA) | 'DEFAULT' (FBM)
    merchant_shipping_group TEXT,                     -- THE shipping template name
    item_condition          TEXT,
    open_date               TEXT,                     -- ISO date string

    -- Status tracking
    status                  TEXT DEFAULT 'ACTIVE',    -- ACTIVE | INACTIVE | SUPPRESSED | REMOVED
    is_active               INTEGER DEFAULT 1,

    -- Cycle tracking
    snapshot_date           TEXT NOT NULL,            -- ISO date string, batch identifier
    row_hash                TEXT NOT NULL,            -- SHA-256 of mutable fields (see below)
    loaded_at               TEXT DEFAULT (datetime('now')),

    UNIQUE(region, seller_sku, snapshot_date)
);

CREATE INDEX idx_snapshot_region_date  ON amazon_listings_snapshot(region, snapshot_date);
CREATE INDEX idx_snapshot_sku          ON amazon_listings_snapshot(seller_sku);
CREATE INDEX idx_snapshot_base_sku     ON amazon_listings_snapshot(base_sku, region);
CREATE INDEX idx_snapshot_template     ON amazon_listings_snapshot(merchant_shipping_group, region);
CREATE INDEX idx_snapshot_hash         ON amazon_listings_snapshot(row_hash);
CREATE INDEX idx_snapshot_design       ON amazon_listings_snapshot(design_code, region);
CREATE INDEX idx_snapshot_fba          ON amazon_listings_snapshot(is_fba, region);

-- Marketplace identity table — exactly one row, set at DB creation, immutable
-- This is the structural anchor that the CHECK constraint above references
CREATE TABLE _meta_marketplace (
    region              TEXT PRIMARY KEY CHECK (region IN ('US','UK','DE','FR','IT','ES')),
    db_filename         TEXT NOT NULL,
    created_at          TEXT DEFAULT (datetime('now')),
    -- ensure exactly one row
    singleton           INTEGER UNIQUE DEFAULT 1 CHECK (singleton = 1)
);

-- Populated once at DB initialisation:
-- INSERT INTO _meta_marketplace (region, db_filename) VALUES ('US', 'listings_us.db');

CREATE TABLE listing_snapshots_meta (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    region              TEXT NOT NULL,
    snapshot_date       TEXT NOT NULL,
    filename            TEXT NOT NULL,
    file_size_bytes     INTEGER,
    file_sha256         TEXT,                     -- hash of the source file itself
    total_rows          INTEGER,
    valid_rows          INTEGER,
    rejected_rows       INTEGER,
    load_duration_sec   REAL,
    delta_new           INTEGER,
    delta_updated       INTEGER,
    delta_unchanged     INTEGER,
    delta_removed       INTEGER,
    loaded_at           TEXT DEFAULT (datetime('now')),
    completed_at        TEXT,
    status              TEXT DEFAULT 'in_progress' -- in_progress | completed | failed | rolled_back
);
```

#### Row hash definition

The row hash MUST be deterministic and cover only the fields whose changes require re-scoring or re-validation. Excluded fields: `loaded_at`, `snapshot_date` (these change every cycle by design).

```python
def compute_row_hash(row: dict) -> str:
    parts = [
        str(row.get('seller_sku') or ''),
        str(row.get('price') or ''),
        str(row.get('quantity') or ''),
        str(row.get('fulfillment_channel') or ''),
        str(row.get('merchant_shipping_group') or ''),
        str(row.get('item_condition') or ''),
        str(row.get('status') or ''),
        str(row.get('asin') or ''),
    ]
    return hashlib.sha256('|'.join(parts).encode('utf-8')).hexdigest()
```

### 5.2 Supabase (hot operational — Tier 3)

Three tables, isolated by RLS. US + UK only in the automated pipeline. DE only on ad-hoc pull.

```sql
-- Active listings — replaces the full catalog every cycle, US + UK only
CREATE TABLE active_listings (
    region                  CHAR(2) NOT NULL,
    seller_sku              VARCHAR(100) NOT NULL,
    asin                    VARCHAR(20),
    base_sku                VARCHAR(50) NOT NULL,
    item_name               TEXT,
    price                   DECIMAL(10,2),
    currency                CHAR(3),
    quantity                INTEGER,
    is_fba                  BOOLEAN,
    fulfillment_channel     VARCHAR(20),
    merchant_shipping_group VARCHAR(200),
    status                  VARCHAR(20),
    open_date               DATE,
    last_changed_date       DATE,
    last_seen_at            TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (region, seller_sku)
);

CREATE INDEX idx_active_base_sku  ON active_listings (base_sku, region);
CREATE INDEX idx_active_template  ON active_listings (merchant_shipping_group, region);
CREATE INDEX idx_active_fba       ON active_listings (is_fba, region);

ALTER TABLE active_listings ENABLE ROW LEVEL SECURITY;
CREATE POLICY marketplace_isolation ON active_listings
    USING (region = current_setting('app.current_region')::text);

-- Delta log — append-only audit trail
CREATE TABLE listings_delta (
    id                  BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    region              CHAR(2) NOT NULL,
    seller_sku          VARCHAR(100) NOT NULL,
    asin                VARCHAR(20),
    base_sku            VARCHAR(50),
    change_type         VARCHAR(20) NOT NULL,        -- NEW | UPDATED | REMOVED
    field_changed       VARCHAR(50),                  -- price | quantity | template | status | ...
    old_value           TEXT,
    new_value           TEXT,
    snapshot_date       DATE NOT NULL,
    cycle_id            VARCHAR(20),                  -- e.g. '2026-W16'
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_delta_region_cycle ON listings_delta (region, cycle_id);
CREATE INDEX idx_delta_change       ON listings_delta (change_type, snapshot_date);
CREATE INDEX idx_delta_template     ON listings_delta (field_changed, change_type)
    WHERE field_changed = 'merchant_shipping_group';

-- Shipping template issues — current open issues only, refreshed each cycle
CREATE TABLE listings_shipping_issues (
    id                  BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    region              CHAR(2) NOT NULL,
    seller_sku          VARCHAR(100) NOT NULL,
    asin                VARCHAR(20),
    base_sku            VARCHAR(50),
    current_template    VARCHAR(200),
    required_template   VARCHAR(200),
    issue_type          VARCHAR(50) NOT NULL,
        -- One of:
        -- 'wrong_template_has_stock'  (upgrade to fast template)
        -- 'fast_template_no_stock'    (downgrade — can't deliver promise)
        -- 'restricted_critical'       (HB6/HB7/HDMWH/HSTWH/H89/H90 + low stock)
        -- 'unfulfillable'             (zero stock + no PH overflow path)
    severity            VARCHAR(10) NOT NULL,         -- CRITICAL | HIGH | MEDIUM | LOW
    blank_stock_units   INTEGER,
    days_of_cover       INTEGER,
    is_restricted_prefix BOOLEAN DEFAULT FALSE,
    first_detected      DATE NOT NULL,
    last_seen            DATE NOT NULL,
    resolved_date       DATE,
    status              VARCHAR(20) DEFAULT 'OPEN',   -- OPEN | RESOLVED | IGNORED
    UNIQUE (region, seller_sku, issue_type)
);

CREATE INDEX idx_issues_open         ON listings_shipping_issues (severity, region) WHERE status = 'OPEN';
CREATE INDEX idx_issues_first_detected ON listings_shipping_issues (first_detected);
```

The `compliance_flags` table from `LAYER0_COMPLIANCE_INTEGRATION.md` is created in the same Supabase project as a separate concern owned by the procurement-session. This pipeline writes `listings_shipping_issues` (a superset, scoped to listings); procurement reads `compliance_flags` (a subset, scoped to actionable PO priority signals). The two tables are deliberately separate to avoid coupling concerns.

### 5.3 BigQuery (cold archive — Tier 2)

Mirrors the Supabase active table but adds full historical retention and SCD2 history.

```sql
CREATE TABLE `instant-contact-479316-i4.amazon_listings.listings_master` (
    region                  STRING NOT NULL,
    marketplace_id          STRING NOT NULL,
    seller_sku              STRING NOT NULL,
    asin                    STRING,
    base_sku                STRING NOT NULL,
    item_name               STRING,
    price                   FLOAT64,
    currency                STRING,
    quantity                INT64,
    is_fba                  BOOL,
    fulfillment_channel     STRING,
    merchant_shipping_group STRING,
    item_condition          STRING,
    status                  STRING,
    open_date               DATE,
    row_hash                STRING,
    first_seen_date         DATE,
    last_seen_date          DATE,
    last_changed_date       DATE,
    change_type             STRING,
    cycle_id                STRING,
    loaded_at               TIMESTAMP
)
PARTITION BY DATE(last_seen_date)
CLUSTER BY region, base_sku;

CREATE TABLE `instant-contact-479316-i4.amazon_listings.listings_history` (
    region              STRING NOT NULL,
    seller_sku          STRING NOT NULL,
    field_changed       STRING NOT NULL,
    old_value           STRING,
    new_value           STRING,
    changed_at          TIMESTAMP,
    cycle_id            STRING
)
PARTITION BY DATE(changed_at)
CLUSTER BY region, seller_sku;
```

### 5.4 Dead-Letter Sync Table (Codex condition 5)

When a Supabase or BigQuery push fails persistently (>5 retries with exponential backoff), the failed batch is logged to a local dead-letter table rather than silently dropped. This preserves the data for manual replay once the downstream issue is resolved.

**Location:** Inside each per-marketplace SQLite file (e.g. `listings_us.db`).

```sql
CREATE TABLE dead_letter_sync (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_id            TEXT NOT NULL,              -- e.g. '2026-W16'
    snapshot_date       TEXT NOT NULL,
    target              TEXT NOT NULL,              -- 'supabase' | 'bigquery'
    target_table        TEXT NOT NULL,              -- 'active_listings' | 'listings_delta' | 'listings_master'
    batch_number        INTEGER NOT NULL,           -- which batch (0-based, batches of 500 rows)
    batch_size          INTEGER NOT NULL,           -- rows in this batch
    batch_hash          TEXT NOT NULL,              -- SHA-256 of the batch payload (for dedup on replay)
    payload_path        TEXT NOT NULL,              -- path to JSON file with the batch rows
                                                    -- stored at ~/.openclaw/workspace/dead_letter/{cycle_id}/{target}_{batch}.json
    retry_count         INTEGER DEFAULT 0,
    last_error          TEXT,                       -- most recent error message
    last_retry_at       TEXT,                       -- ISO timestamp
    status              TEXT DEFAULT 'pending',     -- 'pending' | 'replayed' | 'abandoned'
    created_at          TEXT DEFAULT (datetime('now')),
    replayed_at         TEXT                        -- set when status changes to 'replayed'
);

CREATE INDEX idx_dead_letter_pending ON dead_letter_sync (status, target) WHERE status = 'pending';
```

**Replay semantics:**

```bash
./replay_dead_letter.sh --region US --cycle 2026-W16
```

1. Reads all `status = 'pending'` rows for the specified cycle
2. For each batch: loads the JSON payload from `payload_path`, re-attempts the upsert/merge
3. On success: sets `status = 'replayed'`, records `replayed_at`
4. On persistent failure (>5 additional retries): sets `status = 'abandoned'`, logs to Slack `#data-pipeline-alerts`
5. Abandoned batches require manual intervention (export the JSON, inspect, fix, re-push manually)

**Idempotent upsert keys (for safe replay):**

| Target | Table | Upsert Key | Strategy |
|---|---|---|---|
| Supabase | `active_listings` | `(region, seller_sku)` | `UPSERT ON CONFLICT (region, seller_sku)` — replaying an already-pushed batch overwrites with the same data (safe) |
| Supabase | `listings_delta` | `(id)` — auto-generated | Deduplicate by `batch_hash` before insert; skip if hash already exists in `listings_delta` for this cycle |
| Supabase | `listings_shipping_issues` | `(region, seller_sku, issue_type)` | `UPSERT ON CONFLICT` — same semantics as active_listings |
| BigQuery | `listings_master` | `(region, seller_sku)` | `MERGE ON T.region = S.region AND T.seller_sku = S.seller_sku` — replaying an already-merged batch is a no-op (WHEN MATCHED updates to same values) |
| BigQuery | `listings_history` | None (append-only) | Deduplicate by `(region, seller_sku, field_changed, cycle_id)` before append |

**Payload file storage:**

Dead-letter JSON files are stored at `~/.openclaw/workspace/dead_letter/{cycle_id}/` and retained for 90 days. After 90 days, abandoned payloads are archived to BigQuery's `amazon_listings.dead_letter_archive` table (JSON column) and deleted locally.

### 5.5 Output CSV Contracts (Codex condition 4)

Every output CSV follows these conventions:

| Property | Value |
|---|---|
| Encoding | UTF-8 (no BOM) |
| Delimiter | Comma `,` |
| Quoting | RFC 4180 — quote any field containing comma, newline, or double-quote |
| Date format | ISO 8601: `YYYY-MM-DD` |
| Timestamp format | ISO 8601: `YYYY-MM-DDTHH:MM:SSZ` (UTC) |
| Null representation | Empty string (not "NULL", not "None") |
| Boolean representation | `true` / `false` (lowercase) |
| Header row | Always present, first row |
| Line endings | `\n` (Unix) |

#### Contract: `listings_delta_{mp}_{date}.csv`

Consumer: BigQuery loader, Hermes, OpenClaw

| # | Column | Type | Example | Description |
|---|---|---|---|---|
| 1 | `region` | CHAR(2) | `US` | Marketplace code |
| 2 | `seller_sku` | VARCHAR | `HTPCR-IPH17-NARUICO-AKA` | Full SKU as Amazon reports it |
| 3 | `asin` | VARCHAR | `B0FQNMFQNN` | ASIN from Amazon |
| 4 | `base_sku` | VARCHAR | `HTPCR-IPH17` | First two hyphen-delimited segments (FBM form) |
| 5 | `is_fba` | BOOL | `false` | F-prefix detection result |
| 6 | `change_type` | ENUM | `UPDATED` | One of: `NEW`, `UPDATED`, `REMOVED` |
| 7 | `field_changed` | VARCHAR | `merchant_shipping_group` | For UPDATED: which field; for NEW/REMOVED: empty |
| 8 | `old_value` | VARCHAR | `Default Amazon Template` | Previous value (empty for NEW) |
| 9 | `new_value` | VARCHAR | `Reduced Shipping Template` | Current value (empty for REMOVED) |
| 10 | `price` | DECIMAL | `26.95` | Current listing price (0 for REMOVED) |
| 11 | `quantity` | INT | `1` | Amazon-reported quantity |
| 12 | `merchant_shipping_group` | VARCHAR | `Reduced Shipping Template` | Current template |
| 13 | `snapshot_date` | DATE | `2026-04-15` | Cycle date |
| 14 | `cycle_id` | VARCHAR | `2026-W16` | Cycle identifier |

Sample row:

```csv
region,seller_sku,asin,base_sku,is_fba,change_type,field_changed,old_value,new_value,price,quantity,merchant_shipping_group,snapshot_date,cycle_id
US,HTPCR-IPH17-NARUICO-AKA,B0FQNMFQNN,HTPCR-IPH17,false,UPDATED,merchant_shipping_group,Default Amazon Template,Reduced Shipping Template,26.95,1,Reduced Shipping Template,2026-04-15,2026-W16
```

#### Contract: `shipping_issues_{mp}_{date}.csv`

Consumer: Jay Mark (template fix operator), Layer 0 validator

| # | Column | Type | Example | Description |
|---|---|---|---|---|
| 1 | `region` | CHAR(2) | `US` | Marketplace |
| 2 | `seller_sku` | VARCHAR | `HTPCR-IPH17-NARUICO-AKA` | Full SKU |
| 3 | `asin` | VARCHAR | `B0FQNMFQNN` | ASIN |
| 4 | `base_sku` | VARCHAR | `HTPCR-IPH17` | Join key for blank_inventory |
| 5 | `item_name` | VARCHAR | `Naruto Akatsuki iPhone 17 Case` | Product name (for human readability) |
| 6 | `current_template` | VARCHAR | `Default Amazon Template` | Current shipping template |
| 7 | `required_template` | VARCHAR | `Reduced Shipping Template` | What it should be |
| 8 | `issue_type` | ENUM | `wrong_template_has_stock` | One of: `wrong_template_has_stock`, `fast_template_no_stock`, `restricted_critical`, `unfulfillable` |
| 9 | `severity` | ENUM | `MEDIUM` | One of: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| 10 | `is_restricted_prefix` | BOOL | `false` | true if HB6/HB7/HDMWH/HSTWH/H89/H90 |
| 11 | `blank_stock_units` | INT | `45` | Current blank stock at primary warehouse |
| 12 | `days_of_cover` | INT | `22` | Stock / daily velocity |
| 13 | `price` | DECIMAL | `26.95` | Listing price |
| 14 | `first_detected` | DATE | `2026-03-30` | When this issue was first seen |
| 15 | `snapshot_date` | DATE | `2026-04-15` | Current cycle date |

Sample row:

```csv
region,seller_sku,asin,base_sku,item_name,current_template,required_template,issue_type,severity,is_restricted_prefix,blank_stock_units,days_of_cover,price,first_detected,snapshot_date
US,HTPCR-IPH17-NARUICO-AKA,B0FQNMFQNN,HTPCR-IPH17,Naruto Akatsuki iPhone 17 Case,Default Amazon Template,Reduced Shipping Template,wrong_template_has_stock,MEDIUM,false,45,22,26.95,2026-03-30,2026-04-15
```

#### Contract: `compliance_flags_{mp}_{date}.csv`

Consumer: procurement-system (priority boost), Layer 0 (scoring gate)

| # | Column | Type | Example | Description |
|---|---|---|---|---|
| 1 | `item_code` | VARCHAR | `HTPCR-IPH17` | Base SKU (join key for blank_inventory) |
| 2 | `marketplace` | CHAR(2) | `US` | Marketplace |
| 3 | `warehouse` | CHAR(2) | `FL` | Primary warehouse for this marketplace |
| 4 | `flag_type` | ENUM | `prime_promise_risk` | Per LAYER0_COMPLIANCE_INTEGRATION §3 enum |
| 5 | `severity` | ENUM | `CRITICAL` | CRITICAL / HIGH / MEDIUM |
| 6 | `current_template` | VARCHAR | `Reduced Shipping Template` | What the listing has now |
| 7 | `required_template` | VARCHAR | `Default Amazon Template` | What it should be (if stock insufficient) |
| 8 | `days_of_cover` | INT | `3` | Current stock / velocity |
| 9 | `velocity_7d` | DECIMAL | `2.14` | 7-day rolling velocity |
| 10 | `listings_affected` | INT | `47` | How many full SKUs share this base_sku |
| 11 | `snapshot_date` | DATE | `2026-04-15` | Cycle date |

Sample row:

```csv
item_code,marketplace,warehouse,flag_type,severity,current_template,required_template,days_of_cover,velocity_7d,listings_affected,snapshot_date
HDMWH-900X400X4,US,FL,restricted_critical,CRITICAL,Reduced Shipping Template,Default Amazon Template,3,2.14,12,2026-04-15
```

#### Enum vocabularies (frozen)

| Enum | Valid values |
|---|---|
| `change_type` | `NEW`, `UPDATED`, `REMOVED` |
| `issue_type` | `wrong_template_has_stock`, `fast_template_no_stock`, `restricted_critical`, `unfulfillable` |
| `severity` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `flag_type` | `prime_promise_risk`, `restricted_critical`, `template_mismatch`, `blank_oos_unfulfillable`, `blank_oos_overflow_ok` |
| `status` (meta) | `initiated`, `validated`, `loaded_local`, `compliance_done`, `supabase_synced`, `bigquery_synced`, `completed`, `approved`, `failed`, `failed_contamination`, `rolled_back` |
| `status` (dead_letter) | `pending`, `replayed`, `abandoned` |
| `status` (shipping_issues) | `OPEN`, `RESOLVED`, `IGNORED` |

### 5.6 Inventory Cache (added v1.2)

The pipeline maintains a **local SQLite cache of `blank_inventory`** so the dashboard's "In Stock Only" filter, the compliance scan's restricted-prefix logic, and the Layer 0 actionable-count join all run against a single warm dataset without round-tripping to Supabase or BigQuery on every page load.

**Location:** `~/.openclaw/workspace/data/inventory_cache.db` (or `<data-dir>/inventory_cache.db` via `--data-dir`).

**Why a separate file (not a table inside `listings_us.db`):**
1. Inventory is **not marketplace-scoped** — the same blank stock pool serves US and UK listings (FL warehouse → US, UK warehouse → UK). Embedding it in a per-marketplace file would require duplication.
2. The G2 `_meta_marketplace` CHECK constraint applies to the listings file only; mixing inventory in would either need a parallel guard or a relaxed schema. A separate file sidesteps the question.
3. Inventory refreshes on its own cadence (24h TTL, refresh-on-demand from the UI) independently of the biweekly listings cycle.

#### 5.6.1 Schema

```sql
CREATE TABLE blank_inventory (
    item_code           TEXT NOT NULL,           -- joins to amazon_listings_snapshot.base_sku
    warehouse           TEXT NOT NULL,           -- canonicalised: FL | UK | PH | DE | TRANSIT | CN
    free_stocks         REAL NOT NULL DEFAULT 0,
    sales_last_7d       REAL DEFAULT 0,
    sales_last_30d      REAL DEFAULT 0,
    ave_daily_sales     REAL DEFAULT 0,
    reorder_level       REAL DEFAULT 0,
    on_order            REAL DEFAULT 0,
    days_of_cover       REAL DEFAULT 0,          -- derived: free_stocks / ave_daily_sales (9999 if no velocity but stock>0)
    product_group       TEXT,                    -- excludes 'DISC' on load
    alert_level         TEXT,                    -- only populated by Supabase source; null from BQ
    snapshot_date       TEXT,                    -- only populated by Supabase source; null from BQ
    PRIMARY KEY (item_code, warehouse)
);

CREATE INDEX idx_inv_warehouse ON blank_inventory (warehouse);
CREATE INDEX idx_inv_item      ON blank_inventory (item_code);
CREATE INDEX idx_inv_alert     ON blank_inventory (alert_level) WHERE alert_level IS NOT NULL;

CREATE TABLE cache_meta (
    id              INTEGER PRIMARY KEY CHECK (id = 1),  -- singleton
    refreshed_at    TEXT NOT NULL,                       -- ISO8601 UTC
    row_count       INTEGER NOT NULL,
    duration_sec    REAL NOT NULL,
    source          TEXT NOT NULL                        -- 'supabase' | 'bigquery'
);
```

#### 5.6.2 Pluggable source

The cache loader supports two sources, selected at refresh time:

| Source | URL / Table | Auth | Typical row count | Typical refresh time | Notes |
|---|---|---|---|---|---|
| **Supabase** (default) | `https://auzjmawughepxbtpwuhe.supabase.co/rest/v1/blank_inventory` | `SUPABASE_SERVICE_KEY` env var | ~3,005 (filtered to free_stocks > 0, non-DISC) | ~1 second | Operational source — what procurement reads. Snake-case columns, includes `alert_level` and `snapshot_date`. Synced daily by Harry's job from BQ. |
| **BigQuery** (fallback) | `instant-contact-479316-i4.zero_dataset.inventory` | Application Default Credentials (`gcloud auth application-default login`) | ~6,445 (Florida + UK + PH + TRANSIT, free_stocks > 0, non-DISC) | ~3 seconds | Live VIEW on Sage. CamelCase columns. Use when Supabase is stale or unavailable. |

The dispatcher in `inventory_cache.refresh_cache(data_dir, source=...)` picks the backend; both write the same canonical schema so downstream consumers don't care which source last ran.

#### 5.6.3 Refresh contract

- **TTL:** 24 hours. The dashboard reads `cache_meta.refreshed_at` and shows the age in the header. If older than 24h, the UI prompts the operator to refresh; the API surfaces a `stale: true` flag on `/api/inventory/status`.
- **Atomic replace:** The loader runs `BEGIN IMMEDIATE; DELETE FROM blank_inventory; INSERT ... ; UPDATE cache_meta; COMMIT;` so concurrent readers either see the previous snapshot in full or the new snapshot in full. There is no half-loaded state.
- **Pagination (Supabase):** Uses Postgrest `Range` header (1000 rows/page) rather than `offset/limit` — `offset` paths hit a cap at the service-role tier and silently return an empty page beyond ~3000 rows. The Range-based loop drains the result set deterministically and exits when a short page returns.
- **DISC filter:** `product_group = 'DISC'` is filtered server-side (`product_group=neq.DISC` for Supabase; `WHERE Product_Group != 'DISC'` for BQ). Discontinued blanks are irrelevant to compliance.
- **Stock filter:** `free_stocks > 0` is the default. The dashboard's "In Stock Only" filter relies on a JOIN that drops listings whose `base_sku` does not appear in this cache.

#### 5.6.4 Warehouse canonicalisation

The source data has both `'FL'` and `'Florida'` (Harry's normalisation UPDATE in progress) plus `'Transit'` in mixed case. The loader collapses all variants to short codes via `WAREHOUSE_MAP`:

```
FL / Florida / florida   → FL
UK / England             → UK
PH / Philippines         → PH
DE / Germany             → DE
TRANSIT / Transit / transit → TRANSIT
CN                       → CN
```

This canonicalisation happens **before** the dedupe step so two source rows that differ only in warehouse spelling collapse to a single primary-key row.

#### 5.6.5 Snapshot dedupe

The Supabase source contains snapshot history (the same `(item_code, warehouse)` pair appears multiple times across `snapshot_date`). The loader keeps the row with the latest `snapshot_date` per canonical key. See §15 open question for the design rationale on "always-latest" vs strict snapshot-pinning.

#### 5.6.6 Roll/sheet-based prefix override

Some product types are printed on raw vinyl/sheet rolls rather than per-device blanks: `H8939`, `HSTWH`, `H9039`, `H7805`, `HDMWH`. The compliance scan's restricted-prefix logic treats these as **always in stock** for shipping-template purposes — a missing row in `blank_inventory` for a roll-based SKU does NOT downgrade the listing to "fast template, no stock" because the constraint is print capacity, not blank availability.

The list lives in `inventory_cache.ROLL_BASED_PREFIXES` and `SHEET_BASED_PREFIXES` and is the same list referenced in §11 restricted-prefix logic. The two sets exist as separate constants because the operational meaning differs (rolls = vinyl wrap; sheets = die-cut backing) even though the compliance treatment is identical today.

---

## 6. Guardrails & Validation Rules

### 6.0 Guardrails — Marketplace Isolation (NON-NEGOTIABLE)

> **Historical context:** Ava's earlier listings ingestion attempt (pre-2026-04-15) failed because US, UK, and DE rows were written into the same table without enforceable separation. The data was unusable and had to be discarded. This section exists specifically to make that failure mode structurally impossible, not just unlikely.

The principle: **marketplace contamination must be impossible at the file system layer, not just at the validation layer.** A bug in the loader, a confused operator, a script invoked with the wrong argument, a renamed file — none of these can result in data from one marketplace landing in another marketplace's storage. Cross-contamination is treated as a P0 severity event and cannot pass silently.

#### G1 — Per-marketplace SQLite files (physical isolation)

Each marketplace has its own SQLite file. Period. There is no shared `listings.db` and no shared `amazon_listings_snapshot` table. The script literally cannot write US data to the UK file because it opens a different file descriptor.

```
~/.openclaw/workspace/data/
├── listings_us.db       # contains ONLY US rows
├── listings_uk.db       # contains ONLY UK rows
├── listings_de.db       # contains ONLY DE rows (when populated)
├── listings_fr.db       # ad-hoc only
├── listings_it.db       # ad-hoc only
└── listings_es.db       # ad-hoc only
```

#### G2 — `_meta_marketplace` anchor + CHECK constraint (schema isolation)

Every SQLite file has a single-row `_meta_marketplace` table containing the region code that file was created for. The `amazon_listings_snapshot` table has a CHECK constraint that prevents inserts where `region != _meta_marketplace.region`. An accidental wrong-marketplace insert raises a SQLite constraint violation immediately, before the row is committed.

The `_meta_marketplace` table also enforces `singleton = 1 UNIQUE` so a malicious or buggy script cannot relabel the file mid-life.

#### G3 — Mandatory marketplace argument with cross-validation

`load.sh` requires three things that must all agree:

1. The `--region` flag (operator-supplied, e.g. `--region US`)
2. The filename pattern (e.g. `US_ALL_LISTINGS_2026-04-15.txt` → extracted region `US`)
3. The target SQLite file (e.g. `listings_us.db` → `_meta_marketplace.region` = `US`)

If any of the three disagree, the script exits with code 9 ("marketplace mismatch") and does not touch any storage layer. There is no `--force` flag.

#### G4 — Currency cross-check on row sample

After loading raw rows into a temporary in-memory DuckDB table (before any persistent write), the script samples 1000 rows and computes the mean and median price. If the values are outside the marketplace's expected currency range, the load aborts:

| Region | Expected price range | Currency |
|---|---|---|
| US | $0.50 – $999 | USD |
| UK | £0.50 – £999 | GBP |
| DE / FR / IT / ES | €0.50 – €999 | EUR |

A US file accidentally placed in the UK queue would have prices in dollars — the script sees mean ≈ $25 and aborts because that's an unrealistic GBP value for a phone case (would suggest items priced at £25 average in a catalog full of £15–£30 items — could pass) — **so the currency check alone is not enough**. Combined with G5 (template name check), it becomes deterministic.

#### G5 — Shipping template name cross-check on row sample

Each marketplace has known-valid shipping template names. Any row whose `merchant_shipping_group` matches a known foreign template causes immediate file rejection.

| Region | Valid templates | Foreign templates (rejection triggers) |
|---|---|---|
| US | `Reduced Shipping Template`, `Default Amazon Template` | `Nationwide Prime`, `Standardvorlage Amazon` |
| UK | `Nationwide Prime`, `Reduced Shipping Template`, `Default Amazon Template` | `Standardvorlage Amazon` |
| DE | `Standardvorlage Amazon`, `Reduced Shipping Template` | `Nationwide Prime` |

> Note: `Reduced Shipping Template` exists in both US and UK Seller Central but means different things (US: 2-day FedEx; UK: tracked Royal Mail, see [[02-Projects/procurement/LAYER0_COMPLIANCE_INTEGRATION]] §5). It does NOT cause rejection in either marketplace; only the marketplace-exclusive templates do.

If even one row contains a foreign template name, the entire file is rejected. A US file accidentally renamed to `UK_ALL_LISTINGS_*.txt` would contain `Reduced Shipping Template` rows mixed with `Default Amazon Template` rows but **zero `Nationwide Prime` rows**, while a real UK file would contain mostly `Nationwide Prime` — the script computes the percentage and rejects if the file claims to be UK but has < 5% Nationwide Prime usage.

#### G6 — Output directory isolation

Output CSVs are written to per-marketplace folders, never a shared `out/` directory:

```
~/.openclaw/workspace/out/
├── us/
│   ├── 2026-W16/
│   │   ├── pipeline_report.json
│   │   ├── listings_delta.csv
│   │   └── shipping_issues.csv
├── uk/
│   ├── 2026-W16/
│   │   ├── pipeline_report.json
│   │   └── ...
└── de/
    └── ...
```

Even if the loader is buggy, the output paths are derived from the marketplace argument (G3) and cannot collide.

#### G7 — Supabase RLS + region-scoped writes

Every write to Supabase tables (`active_listings`, `listings_delta`, `listings_shipping_issues`) MUST set `region` explicitly. Supabase Row-Level Security policies enforce that no row with one region can be modified by a session claiming another region. The Supabase client used by this pipeline opens a fresh connection per marketplace with `app.current_region` set, and never reuses a session across marketplaces.

#### G8 — Post-load contamination test (mandatory CI gate)

After every successful load, a **separate sanity check job** runs against the just-written SQLite file:

```sql
-- Run inside listings_us.db
SELECT COUNT(*) FROM amazon_listings_snapshot
WHERE region != 'US';
-- Must return 0. Any non-zero result triggers immediate rollback + Slack alert.

-- Cross-check no UK templates leaked
SELECT COUNT(*) FROM amazon_listings_snapshot
WHERE merchant_shipping_group IN ('Nationwide Prime', 'Standardvorlage Amazon');
-- Must return 0 in listings_us.db.
```

This is run automatically as the final step of every load. Any failure rolls back the entire cycle (deletes the just-loaded snapshot rows) and notifies the operator.

#### G9 — Loud failure, no warnings

There are no "warning, possible contamination, continuing anyway" code paths. If guardrails detect contamination, the load:

1. Does NOT commit any rows to SQLite
2. Does NOT push anything to Supabase
3. Does NOT push anything to BigQuery
4. Does NOT write any output CSVs
5. Sets `listing_snapshots_meta.status = 'failed_contamination'`
6. Posts a HIGH-severity Slack alert
7. Exits with non-zero code

The operator must manually investigate before re-running. There is no auto-retry on contamination failures because the source of the problem is upstream (wrong file, wrong rename, wrong argument).

#### G10 — Append-only, never DELETE+INSERT for cross-marketplace

The delta detection algorithm (§9) NEVER does a `DELETE FROM amazon_listings_snapshot WHERE region = ?` followed by a fresh insert. Even though that would be semantically equivalent to "replace the snapshot", it creates a window where the DB has zero rows for that marketplace, and a concurrent reader would see incomplete data. Instead, deltas are computed via JOIN against the previous snapshot and applied as targeted UPDATE / INSERT operations. The full snapshot is rebuilt logically, never physically truncated.

### 6.1 File-level gates

| # | Gate | Rule | Failure Action |
|---|---|---|---|
| 1 | Filename pattern | Matches `^(US|UK|DE|FR|IT|ES)_ALL_LISTINGS_\d{4}-\d{2}-\d{2}\.txt$` | Reject. Log filename. Operator must rename. |
| 2 | File exists | Path is readable by the script user | Reject. Log error. |
| 3 | File size sanity | ≥ 100 MB (catches truncated downloads) | Reject. Re-download. |
| 4 | File size upper bound | ≤ 15 GB (catches concatenated or duplicated files) | Reject. Investigate. |
| 5 | File SHA-256 hash | Compute and compare against previous cycle's hash | If identical: warn ("same file as last cycle"), still load to refresh `last_seen_date`, but skip delta push |
| 6 | Encoding detection | UTF-8 or Latin-1 (per `chardet`) | Convert to UTF-8 in-place during load |
| 7 | First-line BOM | Strip `\uFEFF` if present | Auto-fix |

### 6.2 Header schema gates

| # | Gate | Rule | Failure Action |
|---|---|---|---|
| 8 | Required columns present | `seller-sku`, `asin1`, `price`, `quantity`, `fulfillment-channel`, `merchant-shipping-group`, `item-name`, `open-date`, `item-condition`, `status` | Reject. Amazon may have changed schema. Alert operator. |
| 9 | No unexpected columns | Warn (don't reject) on new columns; log them for future schema updates | Warn |
| 10 | Column count matches header count | Each row's tab count = header tab count | Reject row, count rejections, fail file if rejections > 1% |

### 6.3 Row-level gates (sampled, not exhaustive)

| # | Gate | Rule | Failure Action |
|---|---|---|---|
| 11 | SKU format | `seller_sku` is non-empty and ≤ 100 chars | Reject row |
| 12 | Price plausibility | If price > 0 and currency = USD → 0.01 ≤ price ≤ 9999.99 | Reject row, count |
| 13 | Currency cross-check | If region = US, mean price across sample of 1000 rows must be in USD range ($5–$60); if region = UK, in GBP range (£5–£60); if region = DE/FR/IT/ES, EUR range (€5–€60) | If mean is wildly out of range → REJECT FILE (almost certainly wrong file in wrong DB) |
| 14 | Shipping template not from wrong marketplace | US file's `merchant_shipping_group` must NOT contain "Nationwide Prime" (UK-only); UK file must NOT contain "Reduced Shipping" pre-Apr 2026 | Reject row, count, fail file if > 5% |
| 15 | Fulfillment channel valid | Must be `AMAZON_NA`, `DEFAULT`, or empty | Reject row |

### 6.4 Cross-cycle gates

| # | Gate | Rule | Failure Action |
|---|---|---|---|
| 16 | Row count delta | `abs(this_cycle_rows - last_cycle_rows) / last_cycle_rows ≤ 20%` | Warn at 10%; abort at 20% (almost certainly partial download or schema break) |
| 17 | Active row count delta | Active rows (`quantity > 0`) shouldn't drop > 5% in one cycle | Warn at 5%, no abort |

### 6.5 Data integrity gates (Codex condition 2)

These gates run **after** bulk load into the DuckDB staging table but **before** commit to SQLite. They catch semantic corruption that file-level and row-level gates miss.

| # | Gate | Rule | Failure Action |
|---|---|---|---|
| 18 | Duplicate seller_sku within snapshot | `COUNT(*) != COUNT(DISTINCT seller_sku)` in the loaded batch | ABORT. Log the duplicates. Amazon should not emit duplicates — if it does, the file is malformed or concatenated. |
| 19 | Null/blank merchant_shipping_group spike | `COUNT(*) WHERE merchant_shipping_group IS NULL OR merchant_shipping_group = ''` > 5% of rows | ABORT. Template data is the primary output of this pipeline. A file with >5% blank templates is either corrupted or a different report type. |
| 20 | Abnormal REMOVED rate | `delta_removed / previous_total_rows > 10%` | ABORT. More than 10% of last cycle's listings disappearing in one cycle is almost certainly a truncated download, a mass suppression event, or Amazon reclassifying the catalog. Operator must investigate before proceeding. |
| 21 | Empty ASIN spike | `COUNT(*) WHERE asin IS NULL OR asin = ''` > 2% of rows | WARN (do not abort). Some listings legitimately lack ASINs (suppressed, pending catalog match), but a spike suggests data quality issues. Logged for operator review. |
| 22 | Null price spike | `COUNT(*) WHERE price IS NULL OR price = 0` > 10% of rows | WARN. Many inactive/suppressed listings have no price, but >10% suggests a parsing issue. |
| 23 | SKU casing normalization | Check if any `seller_sku` differs from a previous cycle's version only by casing (e.g. `HTPCR-IPH17-NARUICO-aka` vs `HTPCR-IPH17-NARUICO-AKA`) | WARN. Log the affected SKUs. Do NOT normalize — treat as UPDATED (hash will differ due to case change). Layer 0 downstream must handle case-insensitive matching. |

### 6.6 Failure response

Any reject triggers:

1. Set `listing_snapshots_meta.status = 'failed'`
2. Set `listing_snapshots_meta.completed_at = now()`
3. Write reason to a `failure_reason` field
4. Roll back any partial inserts
5. Emit Slack notification to `#data-pipeline` with file, gate, rejection rate, and operator action required
6. Do NOT touch downstream tables (Supabase, BigQuery)

The next pipeline run treats the failed batch as if it had not happened. Operator must re-download or fix the source file.

### 6.7 Validation Gate Refinements (v1.2 — from production findings)

The first end-to-end runs of the pipeline against real US/UK files surfaced two cases where the **zero-tolerance** interpretation of the original PRD spec rejected legitimate files. Both gates were retightened to the **percentage-based** interpretation that PRD §6.0 G5 actually describes ("the script computes the percentage and rejects if the file claims to be UK but has < 5% Nationwide Prime usage"). The implementation now matches the spec.

#### 6.7.1 G5 (foreign template check) — percentage-based

**Symptom:** A genuine US All Listings Report was rejected on G5 because it contained ~30,000 rows (≈1% of the catalog) with `merchant_shipping_group = 'Nationwide Prime'`. These are exactly the **mis-tagged listings the pipeline exists to detect and fix** — rejecting the file at the gate prevented them from ever reaching the compliance scan.

**Fix:** `gate_template_crosscheck` now treats foreign templates as ABORT only when their share of the file is `≥ 5%`. Below 5% → log informational, allow through, defer to the compliance scan to flag each row individually. The fast-template minimum check (`fast_template_min_pct`) is unchanged.

```python
# src/listings_pipeline/validator.py
foreign_pct = (foreign_total / max(total_rows, 1)) * 100
if foreign_pct >= 5.0:
    return ABORT(...)
# else: tolerate as fixable mis-tagging
```

**Why 5%:** A genuinely wrong-marketplace file (UK file mistakenly placed in US queue) would have foreign templates dominate at 80–95%. Real mis-tagging maxes out around 1–2% in any of our marketplaces. 5% is comfortably above the worst observed mis-tag rate and well below the floor of a true contamination event.

#### 6.7.2 G8 (post-load contamination test) — split tolerance

**Symptom:** Same root cause as G5 but at the post-load gate. After commit, `gate_contamination_post_load` was counting any foreign-template row as contamination and triggering the §10.1 rollback procedure on every legitimate cycle.

**Fix:** G8 now splits the tolerance:

| Check | Tolerance | Rationale |
|---|---|---|
| `wrong_region_count > 0` | **Zero tolerance** | The G2 `_meta_marketplace` CHECK constraint should make this impossible. If it fires, there is a structural bug in the loader and the cycle MUST roll back. |
| `foreign_template_count / total_rows ≥ 5%` | **Abort** | Same threshold as G5 — file is almost certainly the wrong marketplace. |
| `foreign_template_count / total_rows < 5%` | **Pass** | Mis-tagged listings are valid input for the compliance scan, not contamination. |

```python
# src/listings_pipeline/validator.py
if wrong_region_count > 0:
    issues.append(...)              # always
if foreign_template_count > 0 and total_rows > 0:
    pct = (foreign_template_count / total_rows) * 100
    if pct >= 5.0:
        issues.append(...)          # only if dominant
```

#### 6.7.3 Compliance scan — Default → Reduced is an opportunity, not noise

**Symptom:** The compliance scan was reporting ~543k actionable issues but a random sample showed many obvious wrong-template listings (Default Amazon Template on US listings with stock at FL) were missing. Investigation: the previous scan logic had an `else` branch that excluded `template == 'Default Amazon Template'` from upgrade recommendations, on the (incorrect) assumption that "Default" meant "intentionally unfulfilled".

**Fix:** The scan now flags **any non-fast template** (Default included) as a LOW-severity upgrade opportunity when stock exists. This unlocked **1.9M Default → Reduced opportunities** across the US catalog that the previous logic was silently hiding. The severity hierarchy is now:

| Current template | Stock state | Severity | Suggested action |
|---|---|---|---|
| Foreign / wrong-marketplace | any | CRITICAL | Manual review (file may be wrong) |
| Fast template, no stock | OOS at primary | HIGH | Downgrade to Default (can't deliver) |
| Restricted-prefix on fast template | low stock | HIGH | Manual review (no overflow path) |
| Reduced/Default in catch-all | has stock | MEDIUM | Upgrade to fast template |
| **Default Amazon Template** | **has stock** | **LOW** | **Upgrade to Reduced (or NWP for UK)** |

The LOW severity is what surfaces the previously-hidden 1.9M opportunities. Operator can filter by severity in the dashboard if the volume is overwhelming.

#### 6.7.4 Why these were missed in the original spec

All three are PRD-spec-compliant fixes — the spec was right, the first implementation was overly cautious. The pattern is "treat fixable mis-tagging as input, not as contamination". Codex did not flag these in the v1.0 audit because the audit assumed the compliance scan was the place to flag mis-tags; the implementation accidentally hard-rejected at the gate before the scan could see them. Future gates should default to **percentage-based, never zero-tolerance** unless the failure indicates a structural bug (like a CHECK constraint firing).

---

## 7. Performance & Capacity

### 7.1 Targets

| Metric | Target | Acceptable | Unacceptable |
|---|---|---|---|
| Single 9 GB file load (validation + load + hash + delta) | ≤ 10 min | ≤ 20 min | > 30 min |
| US + UK biweekly run (sequential) | ≤ 25 min | ≤ 45 min | > 60 min |
| Delta push to Supabase | ≤ 3 min | ≤ 8 min | > 15 min |
| BigQuery delta merge | ≤ 5 min | ≤ 10 min | > 20 min |
| Mac Studio peak RAM during load | ≤ 8 GB | ≤ 16 GB | > 24 GB |
| SQLite snapshot file size growth per cycle | ≤ 50 MB (delta only) | ≤ 200 MB | > 1 GB |

### 7.2 Backend selection criteria

The PRD recommends DuckDB for the bulk-load step, but the final selection should be benchmarked against the targets above on a real 9 GB file before commit. Codex audit should validate:

- Does DuckDB meet the 10-min target for a 9 GB TSV on Mac Studio?
- What's the memory ceiling under load?
- Does the SQLite write phase become the bottleneck?
- Is `pandas.read_csv(chunksize=)` actually unacceptable, or is it fine for biweekly cadence?

### 7.3 Capacity planning (24 months)

Assuming biweekly cycles for US + UK:

- 26 cycles/year × 2 marketplaces = 52 snapshots/year
- ~4M rows per snapshot, ~10K delta rows per cycle
- **SQLite growth:** ~5 GB/year if storing all snapshots; ~250 MB/year if only storing latest 4 snapshots per marketplace and pruning the rest
- **BigQuery growth:** ~520K delta rows/year; well under 1 GB; cost negligible
- **Supabase growth:** ~520K delta rows/year + ~1.4M `active_listings` rows refreshed each cycle; under free-tier limits

### 7.4 Retention policy

- **SQLite local snapshot:** Keep most recent 6 snapshots per marketplace. Older snapshots pruned monthly. (Reasoning: 6 cycles = 12 weeks of trend data, sufficient for delta verification and rollback.)
- **BigQuery `listings_master`:** Indefinite retention. Partitioned by `last_seen_date`, so per-partition cost is bounded.
- **BigQuery `listings_history`:** Indefinite retention. Append-only SCD2 audit trail.
- **Supabase `active_listings`:** Always reflects most recent snapshot only. Old rows replaced via UPSERT.
- **Supabase `listings_delta`:** Keep 90 days; older rows archived to BigQuery or deleted.
- **Supabase `listings_shipping_issues`:** Keep all OPEN forever; RESOLVED rows kept 90 days then deleted.

### 7.5 Real numbers (v1.2 — measured, not estimated)

The targets in §7.1 were sized conservatively before the first end-to-end run. Three rounds of perf work brought the 9 GB target well under budget. Numbers below are from the **2026-04-16 production run** on the 6.7 GB / 3,144,188-row US All Listings Report (Mac Studio, 64 GB, M2 Ultra):

| Phase | Time | Notes |
|---|---|---|
| Validation gates (G1–G5, G18–G20) | < 1 s | All file/header/sample gates run before bulk load |
| Bulk load (DuckDB `read_csv_auto` → file-backed at `/tmp/...`) | **17.1 s** | File-backed, not in-memory — see §7.5.1 |
| Hash + enrich (SQL-based SHA-256 + SKU parse) | **12.3 s** | Was 47 min before §7.5.2 fix |
| Delta classify (NEW / UPDATED / UNCHANGED / REMOVED) | 1.5 s | DuckDB JOIN against previous snapshot |
| Commit to SQLite | **94.1 s** | Now the dominant cost; bounded by SQLite single-writer write rate |
| Compliance scan + CSV emit | < 20 s | Includes the 1.9M Default→Reduced fix from §6.7.3 |
| **Total wall clock** | **~150 s** | Was 50+ minutes before perf fixes |

For comparison, §7.1 target was ≤10 min for "validation + load + hash + delta" — actual is **~31 seconds**, ~20× under budget. The §7.1 table is preserved as the contractual ceiling; these are the operating numbers.

**Output volume from the same run:**
- 1,888,789 shipping-template issues detected (60% of catalog non-compliant)
- After "In Stock Only" filter (join against `inventory_cache.blank_inventory`, FL warehouse): 543,082 actionable (29% of catalog)
- Top non-compliant product types:
  - `HLBWH` — 1,136,253 listings (60% of all wrong-template rows)
  - `HTPCR` — 477,538
  - `HC` — 244,371

#### 7.5.1 Loader: file-backed DuckDB (not in-memory)

**Bug:** The first implementation used `duckdb.connect(":memory:")`. On the 6.7 GB US file this OOMed Mac Studio at the bulk-load stage — DuckDB held the raw rows plus the parsed columns plus the hash buffer entirely in RAM, peaking past 40 GB before the OS killed it.

**Fix:** Switched to a file-backed temp DB at `/tmp/listings_load_<cycle_id>.duckdb`, deleted on success/failure. DuckDB now spills its buffer pool to disk under memory pressure. Peak RAM dropped to ~6 GB; throughput unchanged (still 17 s for the 6.7 GB load) because the dominant cost is still TSV parsing, not the staging write.

#### 7.5.2 Hashing: SQL not Python

**Bug:** The first row-by-row Python `hashlib.sha256()` loop took **47 minutes** for 3.1M rows. Even with `multiprocessing.Pool`, the GIL plus the cross-process serialisation cost dominated.

**Fix:** Rewrote the hash phase as a single DuckDB SQL statement using `sha256(string_split(...))` — DuckDB hashes all rows in one multi-threaded pass. **47 minutes → 12.3 seconds** (~225× speedup). The SQL form also enabled the `lower(hex(...))` wrapper (see §7.5.4) without an extra pass.

#### 7.5.3 Enrichment: explicit DROP COLUMN before CREATE OR REPLACE

**Bug:** The enrichment step used `CREATE OR REPLACE TABLE staging AS SELECT * EXCLUDE (parsed_cols), ... FROM staging`. DuckDB's `EXCLUDE` clause does not deduplicate when the same column appears in both the `*` expansion and the explicit projection list, so the resulting table had duplicate `product_type` / `device_code` columns and the subsequent JOIN exploded.

**Fix:** Replaced with explicit `ALTER TABLE staging DROP COLUMN ... ; ALTER TABLE staging ADD COLUMN ...; UPDATE staging SET ...` so the schema is unambiguous before the next phase reads it.

#### 7.5.4 Hash storage: hex string not BLOB

**Bug:** DuckDB's `sha256(...)` returns a `BLOB` by default. Stored that way, the row_hash column was `\xde\xad\xbe\xef\x...` while the previous-cycle hashes (computed by Python `hashlib.sha256(...).hexdigest()`) were lowercase hex strings — every single row classified as UPDATED on the second cycle because the hash representations didn't match.

**Fix:** Wrapped as `lower(hex(sha256(...)))` so the column always contains a 64-char lowercase hex string regardless of the producing path. The schema constraint `row_hash TEXT NOT NULL` is enforced; existing snapshots from the BLOB era were re-hashed in a one-off migration.

#### 7.5.5 API timeout: 20 min → 90 min

The first run that exceeded the 20-minute Next.js subprocess default timed out partway through the SQLite commit (which was the long pole before §7.5.2 sped up the rest). Bumped to 90 minutes with `maxBuffer: 100MB` to safely cover the worst-case scenario (first-cycle full bootstrap on a fresh DB where everything is NEW). Today's full-run wall clock is ~150 s, so the 90-min budget is overprovisioned 36× — that's intentional for the rare bootstrap and the eventual DE/FR/IT/ES first-runs.

---

## 8. Operational Trigger

### 8.1 Cadence

| Marketplace tier | Cadence | Owner |
|---|---|---|
| Tier 1 (US, UK) | Biweekly, every other Monday | Cem downloads, script runs |
| Tier 2 (DE) | Monthly or on-demand | Cem decides |
| Tier 3 (FR, IT, ES) | Manual only | Ad-hoc |

### 8.2 Entry point

Two modes (operator chooses):

**Mode A — Manual invocation (recommended for Phase 1)**

```bash
# After Cem drops file in ~/Downloads/
cd ~/.openclaw/workspace
./load.sh US ~/Downloads/US_ALL_LISTINGS_2026-04-15.txt
./load.sh UK ~/Downloads/UK_ALL_LISTINGS_2026-04-15.txt
```

**Mode B — Watched folder (Phase 2)**

A `watchexec` or `fswatch` daemon monitors `~/Downloads/` for files matching `{MP}_ALL_LISTINGS_*.txt` and auto-fires `load.sh` with the correct marketplace argument extracted from the filename.

The script must be **idempotent** — re-running with the same file MUST produce the same result and not duplicate rows. The file SHA-256 check (Gate 5) handles this.

### 8.3 Output deliverables per run

Every successful run emits the following to `~/.openclaw/workspace/out/{cycle_id}/`:

| File | Contents | Consumer |
|---|---|---|
| `pipeline_report_{cycle_id}.json` | Row counts, delta summary, validation results, timing | Operator + Slack |
| `listings_delta_{mp}_{date}.csv` | All NEW + UPDATED + REMOVED rows | BigQuery loader |
| `shipping_issues_{mp}_{date}.csv` | Wrong-template + unfulfillable + restricted-critical | Jay Mark + Layer 0 |
| `compliance_flags_{mp}_{date}.csv` | Subset of shipping_issues that warrant procurement priority boost | procurement-system |
| `validation_failures_{mp}_{date}.csv` | Rejected rows with reasons | Operator review |

### 8.4 Inventory CLI commands (added v1.2)

The pipeline now exposes two commands for managing the local inventory cache (§5.6) independently of the listings load cycle. The web UI's "Refresh Inventory" button calls these as subprocesses.

```bash
listings-pipeline inventory-refresh \
    --source supabase \
    [--force] \
    [--max-age-hours 24]
```

| Flag | Default | Behaviour |
|---|---|---|
| `--source` | `supabase` | One of `supabase` (operational source, ~1s) or `bigquery` (live Sage view, ~3s — fallback) |
| `--force` | off | Refresh even if the cache is younger than `--max-age-hours` |
| `--max-age-hours` | `24` | TTL — skip refresh if cache is fresher than this |
| `--data-dir` | `~/.openclaw/workspace/data` | Where `inventory_cache.db` lives |

Exit codes: 0 on success, 1 on auth/credential error, 2 on source unreachable, 3 on cache write failure.

```bash
listings-pipeline inventory-status
```

Prints the cache `refreshed_at`, age in hours, total row count, and a per-warehouse breakdown:

```
Inventory cache: ~/.openclaw/workspace/data/inventory_cache.db
  Refreshed:  2026-04-16T14:22:08Z (0.3 hours ago) — source: supabase
  Total rows: 3,005
  Per warehouse:
    FL       1,847 items   147,233 units
    UK         812 items    61,902 units
    PH         284 items    18,510 units
    TRANSIT     62 items     3,418 units
```

---

## 9. Delta Detection Algorithm

Identical conceptually to the Perplexity doc's algorithm, but run inside SQLite (not MySQL) using DuckDB as the comparison engine for speed.

```
GIVEN: raw_listings_us (just-loaded, with row_hash) and amazon_listings_snapshot (previous cycle)

STEP 1 — Mark NEW
  Insert rows where (region, seller_sku) does not exist in amazon_listings_snapshot
  Set change_type = 'NEW', first_seen_date = today, last_seen_date = today

STEP 2 — Mark UPDATED
  For each (region, seller_sku) that exists in both:
    If row_hash differs:
      Update amazon_listings_snapshot with new field values
      Set change_type = 'UPDATED', last_changed_date = today
      Append a row to listings_history per changed field

STEP 3 — Mark UNCHANGED
  For each (region, seller_sku) that exists in both with matching row_hash:
    Set change_type = 'UNCHANGED', last_seen_date = today
    (No history row, no Supabase push, no BigQuery push)

STEP 4 — Mark REMOVED
  For each (region, seller_sku) in amazon_listings_snapshot but not in raw_listings:
    Set change_type = 'REMOVED', last_changed_date = today, status = 'REMOVED'
    Append history row
```

### 9.1 Distinguishing REMOVED from SUPPRESSED

`REMOVED` from the All Listings Report means one of:

1. The listing was deleted (intentional)
2. The listing was suppressed by Amazon (policy / IP / catalog issue)
3. The listing was inactivated (set quantity = 0 + status = INACTIVE)
4. Amazon merged or split the ASIN

This pipeline cannot distinguish these states from the All Listings Report alone. To distinguish, the **Suppressed Listings Report** (`GET_MERCHANTS_LISTINGS_FYP_REPORT`) would also be needed — but per Cem's no-API constraint, that requires a manual download too. Out of scope for v1; flag for v2.

For v1, all `REMOVED` rows are flagged as **status = 'REMOVED'** with no further classification. Layer 0 / procurement may want to investigate any high-revenue REMOVED row manually.

---

## 10. Failure Modes & Recovery

| # | Failure | Detection | Recovery |
|---|---|---|---|
| 1 | Source file truncated mid-download | Gate 3 (file size < 100 MB) or Gate 10 (column count mismatch) > 1% | Re-download from Seller Central |
| 2 | Source file in wrong marketplace folder | Gate 1 (filename pattern) or Gate 13 (currency cross-check) | Operator renames or moves file |
| 3 | Mac Studio runs out of disk during load | DuckDB throws error | Free space; truncate old SQLite snapshots; re-run |
| 4 | Mac Studio runs out of RAM during load | OS kills DuckDB process | Reduce DuckDB memory limit setting; re-run |
| 5 | Script crashes mid-load | `listing_snapshots_meta.status = 'in_progress'` past expected duration | Manual rollback: delete partial rows for that cycle from `amazon_listings_snapshot`; rerun |
| 6 | Supabase push fails on some rows but not others | HTTP 4xx/5xx response captured per batch | Retry failed batches with exponential backoff (max 5 retries); if still failing, log to dead-letter table |
| 7 | BigQuery merge fails | `client.query()` exception | Retry once; if still failing, leave in staging; manual triage |
| 8 | Amazon changes column schema mid-cycle | Gate 8 (header validation) | Schema change requires PRD update + script update; manual operator escalation |
| 9 | Two cycles loaded with same date | UNIQUE constraint on `(region, seller_sku, snapshot_date)` | Earlier cycle wins; later load fails Gate 5 (file hash duplicate) |
| 10 | Supabase RLS misconfigured | Operator can't read their own data | Set `app.current_region` per session; document in SOP |
| 11 | SQLite database file corrupted | Integrity check on startup fails | Restore from latest backup; rebuild from most recent good snapshot file |
| 12 | DuckDB and SQLite version mismatch | Library version warning | Pin versions in `requirements.txt`; rebuild venv |
| 13 | **Cross-marketplace contamination — wrong file in wrong DB** | G3 (mandatory args) + G4 (currency) + G5 (template names) + G8 (post-load check) | Abort with code 9; no rollback needed (writes blocked); operator investigates upstream |
| 14 | **Cross-marketplace contamination — bug in loader writes wrong region** | G2 (CHECK constraint) raises SQLite IntegrityError on first row | Abort with code 10; no rollback needed (constraint blocks commit); fix loader |
| 15 | **Cross-marketplace contamination — silent leak (rare race / concurrent run)** | G8 (post-load contamination test) detects after the fact | Trigger §10.1 rollback procedure; mark `status = 'failed_contamination'`; HIGH severity Slack |
| 16 | **`_meta_marketplace` row tampered with** | G2 CHECK constraint references it; subsequent inserts will fail | Manually inspect DB; rebuild from previous good snapshot |
| 17 | **Filename renamed to wrong marketplace prefix** | G3 (filename pattern) extracts wrong region; if `--region` flag also wrong → G4/G5 catch it; if `--region` correct → mismatch with filename → exit code 9 | Operator renames or re-downloads |

### 10.1 Rollback procedure

If a load is committed to SQLite but later determined to be bad (e.g. file was actually wrong-marketplace and slipped past Gate 13):

```sql
BEGIN;
DELETE FROM amazon_listings_snapshot
  WHERE region = ?
    AND snapshot_date = ?;

UPDATE listing_snapshots_meta
  SET status = 'rolled_back',
      completed_at = datetime('now')
  WHERE region = ? AND snapshot_date = ?;

-- Then revert Supabase upserts (harder — needs delta replay against previous cycle)
-- And revert BigQuery merge (use timetravel within 7 days)
COMMIT;
```

For Supabase rollback, reload the prior snapshot's `active_listings` content — this is why Tier 1 keeps 6 snapshots, not just the current one.

---

## 11. Integration Contracts

### 11.1 procurement-system

**This pipeline writes:**
- `active_listings` (Supabase) — full active US + UK catalog, joinable to `blank_inventory` via `base_sku` = `item_code`
- `listings_shipping_issues` (Supabase) — informational; procurement reads if it wants visibility

**This pipeline reads:**
- `blank_inventory` (Supabase) — to determine `restricted_critical` and `unfulfillable` issue types

**Procurement-side action expected:**
- procurement-system should optionally write `compliance_flags` based on its own join of `blank_inventory + active_listings`, per `LAYER0_COMPLIANCE_INTEGRATION.md` §3
- This is an asynchronous handoff; procurement's session decides when to implement

### 11.2 amazon-unified-score (Layer 0)

**This pipeline writes:**
- `active_listings` (Supabase) — Layer 0 reads `merchant_shipping_group` per SKU
- `listings_shipping_issues` (Supabase) — Layer 0 reads CRITICAL severity to gate scoring

**This pipeline reads:**
- (none — Layer 0 doesn't write back to listings)

**unified-score-side action expected:**
- Layer 0 validator reads `active_listings` joined to `blank_inventory` and decides whether to score a SKU or quarantine it in `FIX_TEMPLATE` queue
- Layer 0 does not modify the listings pipeline's tables

### 11.3 Jay Mark — bulk shipping template fix

**This pipeline writes:**
- `shipping_issues_{mp}_{date}.csv` — exported every cycle, with columns: `seller_sku`, `asin`, `current_template`, `required_template`, `severity`, `is_restricted_prefix`, `blank_stock_units`
- Sorted by severity DESC, then by `last_changed_date` DESC

**Jay Mark workflow:**
1. Open the latest `shipping_issues_us_{date}.csv` and `shipping_issues_uk_{date}.csv`
2. Filter for `severity = CRITICAL` and `is_restricted_prefix = false` (these are the safe upgrades)
3. Generate Amazon flat-file inventory upload with corrected `merchant_shipping_group`
4. Upload via Seller Central → Inventory → Add Products via Upload
5. Wait 24 hours, spot-check 10 random ASINs

**Critical rule:** Jay Mark MUST NOT auto-upload `severity = CRITICAL AND is_restricted_prefix = true` rows — these need manual review (the listing is on a fast template but the SKU type can't reliably ship from primary, so the fix is to remove the fast template, not assign one).

### 11.4 Hermes / Ava / OpenClaw

**This pipeline writes:**
- All Supabase tables — Hermes and OpenClaw query these directly via Supabase REST or PostgREST

**Hermes-side action expected:**
- None new; Hermes already queries Supabase. The new tables (`active_listings`, `listings_delta`, `listings_shipping_issues`) become available in the same project.

### 11.5 Wednesday cron audit

A separate cron job (already proposed in Ava's brief) runs every Wednesday:

1. Reads `listings_shipping_issues` WHERE status = 'OPEN' AND severity IN (CRITICAL, HIGH)
2. Posts a Slack summary to `#shipping-template-audit`
3. Tags Jay Mark if critical count > 50
4. Tags Cem if any `restricted_critical` exists

This is owned by the Hermes session, not this pipeline. The pipeline just keeps the table fresh.

---

## 12. Storage & Cost

| Component | Size | Cost (current) | Notes |
|---|---|---|---|
| SQLite local DB | ~3 GB after 6 cycles, both marketplaces | $0 | Local file, backed up to Time Machine |
| BigQuery `listings_master` | ~5 GB after 12 months | ~$0.10/month storage | Partitioned, cluster-pruned |
| BigQuery `listings_history` | ~10 MB / cycle | ~$0.05/month storage | Append-only |
| Supabase `active_listings` | ~150 MB | $0 (within free tier) | Replaced each cycle |
| Supabase `listings_delta` | ~50 MB | $0 | 90-day retention |
| Supabase `listings_shipping_issues` | ~5 MB | $0 | Mostly OPEN rows |
| BigQuery query cost | ~$0.50/month | ~$6/year | First 1 TB free |
| **Total** | — | **< $5/month** | Negligible |

---

## 13. Disaster Recovery

| Disaster | Impact | Recovery Procedure | RTO | RPO |
|---|---|---|---|---|
| Mac Studio dies | All local SQLite snapshots lost | Re-download last cycle's file from Seller Central → re-run pipeline → first cycle's all rows are NEW (no false delta), subsequent cycles work normally | 4 hours | 0 (Amazon is source of truth) |
| Supabase project deleted | All operational tables lost | Recreate schema from `supabase/migrations/` → next pipeline run repopulates | 2 hours | 0 (BQ has full history) |
| BigQuery dataset dropped | All historical data lost | Recreate schema → backfill from SQLite snapshots → resume | 1 day | 0 if SQLite intact |
| Source file corrupted in Downloads | One cycle skipped | Re-download from Seller Central; rerun | 30 min | 1 cycle |
| Operator credentials revoked (Seller Central) | Pipeline can't continue | Restore credentials; resume | hours | 1 cycle |

### 13.1 Backup strategy

- SQLite DB backed up to Time Machine + iCloud (encrypted)
- BigQuery + Supabase have provider-side daily backups
- No additional backup infrastructure needed

### 13.2 Known issues (v1.2 — track in operator handover)

#### 13.2.1 Editable-install PYTHONPATH not honoured by Next.js subprocess

**Symptom:** `pip install -e .` writes a `.pth` file to the venv's `site-packages` that should put `src/` on `sys.path` for any Python subprocess. In practice, when the Next.js API routes spawn `python -m listings_pipeline ...`, the `.pth` file is **not** picked up — `ModuleNotFoundError: listings_pipeline` is raised.

**Workaround:** All Next.js API routes that spawn the pipeline explicitly set `PYTHONPATH=<repo>/src` in the subprocess environment (`/api/process`, `/api/status`, `/api/inventory/refresh`, `/api/inventory/status`, `/api/list-files`, `/api/dashboard`, `/api/leaderboards`). The CLI works fine when invoked from a shell — only the Node-spawned subprocess path needs the override.

**Root cause:** Not yet identified. Hypothesis: Next.js inherits a sanitised `PATH` and possibly clobbers `PYTHONPATH` from the parent shell, or the `python` resolved is a non-venv interpreter that doesn't see the venv's `.pth` file. Future operators investigating this should `printenv` from inside one of the spawned processes to confirm what's actually getting through.

**Action item:** A future cycle should fix the root cause and remove the explicit `PYTHONPATH=...` from each API route. Not urgent — current workaround works deterministically.

---

## 14. Security

| Concern | Mitigation |
|---|---|
| Supabase service role key exposure | Stored in `~/.openclaw/workspace/.env` (mode 600); never committed to git; not logged |
| Seller Central credentials | Not used by this pipeline (manual operator login only) |
| BigQuery service account key | Stored in same `.env`; restricted to specific dataset only |
| Source files contain ASINs (not PII) | No special handling required; ASINs are public catalog identifiers |
| Customer data in source files | None — All Listings Report has no buyer information |
| Restricted-prefix product info | Internal only; no external sharing |
| Mac Studio physical access | Local network only; SSH key auth; FileVault enabled |

---

## 15. Open Questions for Codex Audit

These are the questions the audit should answer before implementation:

1. **Backend choice (DuckDB vs pandas vs MySQL).** Is the recommendation in §7 defensible, or should the audit force a benchmark?

2. **SQLite at this scale.** Does SQLite handle 4M rows × 6 snapshots with the indexes specified in §5.1 without performance degradation? Or should the persistent store be BigQuery instead and SQLite skipped entirely?

3. **Validation gates.** Are gates 1–17 sufficient? What's missing? Specifically: should there be a gate for detecting if the source file is from the wrong account (multi-seller-account contamination)?

4. **Delta detection edge cases.** What if Amazon changes the SKU casing (lowercase → uppercase) without changing anything else? Currently this would be classified UPDATED. Is that correct, or should normalization happen first?

5. **Schema fidelity vs operational simplicity.** The schemas in §5 add fields beyond what Ava's brief had. Is the addition justified, or is it scope creep?

6. **Restricted-prefix logic in this pipeline vs Layer 0.** Currently the pipeline writes the `is_restricted_prefix` flag; Layer 0 reads it. Should the responsibility be reversed (Layer 0 derives it)?

7. **Tier 2 vs Tier 3 boundary.** Should DE flow into Supabase (Tier 1 treatment) or stay BQ-only? Today it's BQ-only; that's a debatable call given DE's growth potential.

8. **The 122k vs 9,778 wrong-template count discrepancy.** What's the correct number? Both come from internal docs dated 2 weeks apart with very different filtering criteria. Audit should reconcile.

9. **Watched-folder vs cron vs manual trigger.** Is the Phase 1 manual-only entry point safe, or should Phase 1 already include a watched-folder trigger to prevent operator forgetfulness?

10. **Recovery from a partial Supabase push.** §10 row 6 says "retry with backoff, dead-letter on persistent failure". Is the dead-letter table specced? It isn't in §5 — should be added.

11. **What happens when a SKU's `is_fba` flag flips between cycles?** (FBA listing converted to FBM, or vice versa.) Today this would be classified UPDATED. Layer 0 cares because FBA listings have no shipping template — should the change be elevated to a higher severity?

12. **Concurrent runs.** What if `load.sh US` and `load.sh UK` are launched at the same time? SQLite has a single-writer lock — does this serialise correctly, or do we need explicit locking?

13. **The bulk fix path itself.** Jay Mark's flat-file upload (§11.3) is described but not specced in detail. Is it in scope for this PRD or a separate one?

14. **GDPR / data residency.** Are we storing EU customer ASINs / item descriptions in a US-based GCP project (BigQuery `instant-contact-479316-i4`)? If so, does that need legal review?

15. **Failure notification.** §6.5 says "Slack notification". Is `#data-pipeline` set up? If not, fallback to email?

16. **Guardrails sufficiency (CRITICAL — directly addresses Ava's prior failure).** §6.0 specifies 10 guardrails (G1–G10) designed to make marketplace contamination structurally impossible. Codex should specifically attempt to bypass each:
    - G1: Can the loader be tricked into writing to the wrong file? Race conditions? Symbolic links? File permissions?
    - G2: Can the `_meta_marketplace` CHECK constraint be defeated? UPDATE on the meta row? PRAGMA changes?
    - G3: Can the three-way agreement (CLI flag / filename / DB file) be forged?
    - G4 + G5: Are the currency and template heuristics robust against a marketplace with unusual data (e.g. a UK file with mostly Reduced Shipping Template before bulk fix)?
    - G6: Can output paths be manipulated via filename injection in the marketplace argument?
    - G7: If Supabase RLS is misconfigured, what's the blast radius?
    - G8: Can the post-load test be skipped under any failure path?
    - G9 + G10: Is there any code path that proceeds past contamination detection without rolling back?

17. **Bootstrap problem.** When a fresh `listings_us.db` is created for the first time, `_meta_marketplace` must be populated atomically with the table creation. If the script crashes between `CREATE TABLE _meta_marketplace` and the `INSERT INTO _meta_marketplace` statement, the file exists with no anchor row and the next run's CHECK constraint will fail oddly. Should the schema migration use a single transaction, or should there be a separate "init" command?

18. **DB file rename / move attack.** What if an operator renames `listings_uk.db` to `listings_us.db` (e.g. trying to "merge" them)? The CHECK constraint still references `_meta_marketplace.region = 'UK'` so any subsequent insert fails — but reads continue to work, which could fool a downstream consumer. Should the script verify the file name matches the meta row at startup?

### 15.1 New questions surfaced by the v1.2 implementation

19. **Snapshot-history dedupe — latest vs strict pinning.** The Supabase `blank_inventory` table contains snapshot history (same `(item_code, warehouse)` repeated across `snapshot_date`). The cache loader (§5.6.5) keeps the row with the latest `snapshot_date`. Is "always-latest" correct, or should the loader honour a pinned `snapshot_date` (e.g. "give me yesterday's stock for reproducibility")? Today the answer is always-latest because the dashboard's actionable-count must reflect current reality — but a backfill or audit replay scenario might need the pinned form.

20. **Inventory source preference — Supabase as primary.** v1.2 made Supabase the default source and BQ the fallback. The trade-off: Supabase is faster (~1s vs ~3s) and includes `alert_level` + `snapshot_date`, but it depends on Harry's daily sync job from BQ. If that job stalls, the operational data goes stale by N days while the cache happily refreshes from a stale source. Should the loader cross-check `cache_meta.refreshed_at` against the **source's own freshness signal** (e.g. `MAX(snapshot_date)` in the response) and warn if that's > 48h old?

21. **Roll/sheet-based prefix list — where should it live?** §5.6.6 hard-codes `H8939, HSTWH, H9039, H7805, HDMWH` in `inventory_cache.py`. The same list is referenced by Layer 0's restricted-prefix logic. Should it move to a config file or a Supabase table so both pipelines share a single source of truth, or is the duplication acceptable given how rarely it changes?

22. **Compliance scan severity calibration — is LOW too noisy?** §6.7.3 unlocked 1.9M Default → Reduced LOW-severity opportunities. That's a real backlog, but the volume may overwhelm Jay Mark's workflow. Should LOW-severity items be batched into a separate "long-tail" CSV that's processed on a different cadence (e.g. monthly bulk upload during a quiet week)?

23. **Web UI subprocess timeout — 90 min is overprovisioned.** §7.5.5 set the API timeout to 90 minutes against current ~150-second wall clock. Is the 36× headroom right, or should it shrink to e.g. 30 min once the bootstrap edge case is better understood? A tighter timeout would surface hung pipelines faster but risks killing a legitimately-slow first DE/FR run.

24. **Editable-install PYTHONPATH (§13.2.1).** Worth a one-day investigation in a future cycle to understand why `pip install -e .` doesn't propagate `sys.path` through Next.js subprocesses. Removing the explicit `PYTHONPATH=...` override from each API route is a small cleanup; understanding the cause is the larger payoff (it likely affects other Node-spawned-Python integrations in the codebase).

---

## 16. Web UI — Listings Compliance Manager (Added 2026-04-16)

The CLI pipeline is wrapped in a **Next.js web application** that provides a dashboard, filtering, and listing revision capabilities. The operator no longer interacts with the CLI directly — the UI calls the Python pipeline via API routes.

### 16.1 Architecture

```
Next.js App (localhost:3001)
├── /                    Page 1: Process Data (file picker + run)
├── /dashboard           Page 2: Compliance Dashboard (hierarchy + cards)
├── /listings            Page 3: Fix Listings (bulk selection)
├── /sfp                 Page 5: SFP Conversion (cascading filter chain)
├── /revisions           Page 4: Revision Builder (template + price + submit)
├── /api/process         POST: triggers Python pipeline via subprocess
├── /api/status          GET: reads pipeline status from SQLite meta table
├── /api/inventory-check POST: joins listings against blank_inventory
├── /api/export          GET: generates and downloads CSV
└── /api/revision        POST: submits to Amazon via middleware API or generates flat file
```

**Stack:** Next.js 15, Tailwind CSS 4, Recharts, App Router
**Design system:** Modern Ecell Style Guide 2.0 (glassmorphism, Cobalt gradient, ambient backgrounds)
**Location:** `amazon-listings-pipeline/web/`

### 16.2 Page Specifications

#### Page 1: Process Data (`/`)

- **First-run blank screen** — no data loaded state
- Marketplace dropdown (US / UK / DE)
- File path text input with `~/Downloads/` placeholder
- `[Process Data]` button triggers `POST /api/process`
- Real-time progress display with 7 steps (validation → load → hash → delta → commit → compliance → output)
- On completion: shows summary (total rows, shipping issues, duration) + link to Dashboard

#### Page 2: Compliance Dashboard (`/dashboard`)

- **4 summary cards** (Total Listings / Compliant / Non-Compliant / Actionable) with traffic-light colours
- **4-level hierarchy drill-down** of non-compliant listings:
  1. Product Type (canonical, F-stripped) — e.g. HTPCR, HDMWH, HB6
  2. Product Type × Device Model — e.g. HTPCR-IPH17PMAX
  3. Design Parent = Licence/Brand — derived from design code prefix (NARU→Naruto, PNUT→Peanuts)
  4. Design Child = Collection — full design code (NARUICO, NARUGRAT)
- Each level shows: total count, compliant count, non-compliant count, severity dot
- `[Run Inventory Check]` — joins against `blank_inventory`, updates actionable counts (removes SKUs with no stock)
- `[Export CSV]` — downloads non-compliant actionable SKUs
- `[Fix Listings →]` and `[SFP Conversion →]` navigation buttons

#### Page 3: Fix Listings (`/listings`)

- Full table of non-compliant SKUs from the compliance scan
- **Filters:** product type, device model, severity, current template
- **Columns:** SKU (mono), Product Name, Current Template (red badge), Required Template (green badge), Price, Severity (traffic light dot)
- Multi-select checkboxes + `[Select All]` + `[Select Filtered]`
- `[Send for Revision →]` navigates to Page 4 with selected SKUs

#### Page 4: Revision Builder (`/revisions`)

- Shows selected SKUs in a table with per-row controls
- **Bulk actions:**
  - Shipping Template dropdown (Reduced / Nationwide Prime / Default) + `[Apply to All]`
  - Price Adjustment field (+$0.00) + `[Apply to All]`
- **Per-row:** current template → new template, price → adjustment → new price
- **Two submit paths:**
  1. **API Update (recommended):** `POST /api/revision` → submits to Amazon via `amazon-report-middleware` SP-API. Batched (200 SKUs/batch). Waits for Amazon confirmation before sending next batch. Per-batch status display (queued / submitted / confirmed / failed).
  2. **Flat File Export:** generates Amazon Inventory Loader format CSV (tab-delimited, `seller-sku` + `merchant-shipping-group` + `price` columns) for manual upload via Seller Central.

#### Page 5: SFP Conversion (`/sfp`)

- **Separate page from Fix Listings** — this is for upgrading Reduced Shipping → Nationwide Prime (UK SFP), an infrequent on-demand action
- **Source pool:** listings already on `Reduced Shipping Template` with UK stock available
- **Cascading searchable filter chain:**
  1. Product Type — combobox with type-to-search, shows count per option
  2. Device Model — populated after product type selected, type-to-search
  3. Design/Licence — populated after device selected, shows design code + parent licence + count
- Each dropdown is virtualised for long lists (100+ design codes)
- `[Show Matching Listings]` loads the filtered results
- `[Send to Revision Builder →]` takes selected SKUs to Page 4

### 16.3 API Route Details

| Route | Method | Input | Action | Output |
|---|---|---|---|---|
| `/api/process` | POST | `{marketplace, filePath}` | Auto-bootstraps DB if needed, runs `listings-pipeline load` via subprocess | Pipeline report JSON |
| `/api/status` | GET | — | Reads `listing_snapshots_meta` from SQLite | Per-marketplace status |
| `/api/inventory-check` | POST | `{marketplace}` | Joins `active_listings` × `blank_inventory` via Supabase | Updated compliance counts |
| `/api/export` | GET | `?format=csv&marketplace=US` | Reads shipping issues from latest cycle output | CSV file download |
| `/api/revision` | POST | `{skus, template, priceAdj, method}` | If method=api: submits batch to middleware API; if method=csv: generates flat file | Batch status or file download |

### 16.4 Design System Reference

Per `01-Wiki/33-design-system/ECELL_STYLE_GUIDE.md` and `02-Projects/ecell-app/MODERN_STYLE_GUIDE.md`:

| Element | Specification |
|---|---|
| Background | `bg-gradient-to-br from-slate-50 to-blue-50` (ambient gradient, not flat white) |
| Cards | `rounded-2xl border border-zinc-200/60 bg-white/80 backdrop-blur-sm shadow-sm` with glassmorphic hover |
| Primary button | `bg-gradient-to-r from-[#0047AB] to-[#0ea5e9]` with hover glow `shadow-[0_0_15px_rgba(0,71,171,0.4)]` |
| Status dots | Pulse-animated ping (emerald/amber/red) |
| Loading states | Skeleton loaders (`animate-pulse bg-zinc-200/50 rounded-xl`), never blocking spinners |
| Typography | Inter/Geist Sans, `tabular-nums` for metrics, `text-3xl font-semibold tracking-tight` for titles |
| Sidebar | `w-56`, glassmorphic (`bg-white/70 backdrop-blur-lg`), cobalt gradient active state |
| Micro-interactions | `transition-all duration-300 ease-out`, `hover:-translate-y-1 hover:shadow-xl` on cards |
| Charts | Recharts with smooth animation, glassmorphic tooltips |

### 16.5 Revision Submission via SP-API (Page 4, Option 1)

When the operator chooses "API Update", the flow is:

1. UI splits selected SKUs into batches of 200 (Amazon SP-API feed batch limit)
2. `POST /api/revision` with batch payload
3. API route calls `amazon-report-middleware` endpoint to submit a **Listings Items** feed:
   - Endpoint: `POST /api/v1/listings/update` (to be added to middleware)
   - Payload: `{marketplace, items: [{sku, merchant_shipping_group, price}]}`
   - Middleware uses SP-API `patchListingsItem` or submits a flat-file feed via `createFeedDocument` + `createFeed`
4. Middleware polls Amazon for feed processing result
5. On Amazon confirmation → UI marks batch as "confirmed", proceeds to next batch
6. On failure → UI marks batch as "failed", pauses remaining batches, shows error detail

**This requires a new endpoint on `amazon-report-middleware`.** The middleware currently handles reports (read) but not listings updates (write). The Listings Items API or Feeds API must be added. This is a separate middleware enhancement, not part of this project's build scope — but the UI assumes it will exist.

### 16.6 Out of Scope for the Web UI

- User authentication (single-operator tool, localhost only)
- Mobile responsive layout (desktop-first, sidebar pattern)
- Dark mode (light mode only for v1; style tokens support dark mode for v2)
- Real-time WebSocket updates (polling on `/api/status` is sufficient for biweekly cadence)
- Multi-user concurrent access (single operator)

### 16.7 As-built deltas vs the v1.1 spec (added v1.2)

The Web UI shipped largely per §16.1–§16.6 but with the following deviations:

#### 16.7.1 Dashboard layout — 4 leaderboards, not the hierarchy tree

The §16.2 Page 2 spec called for a "4-level hierarchy drill-down" (Product Type → Product×Device → Design Parent → Design Child). The first version of that landed (commit `e225086`) with lazy-loaded SQLite reads, but operator review found the tree was hard to scan — the operator's actual question is "which categories have the worst non-compliance ratio" not "drill down from a specific node".

The shipped layout (commit `2c5feaf`) replaces the tree with **four parallel leaderboards** on the same screen:

| Leaderboard | Group-by | Sort | Top N |
|---|---|---|---|
| Product Type | `product_type` | non-compliant count DESC | 20 |
| Device | `device_code` | non-compliant count DESC | 20 |
| Product × Device | `product_type \|\| '-' \|\| device_code` | non-compliant count DESC | 20 |
| Licence | `design_parent` (derived from `design_code` prefix) | non-compliant count DESC | 20 |

Each card shows: rank, group label, total listings, non-compliant count, non-compliant %, and a severity dot. Click-through navigates to a filtered Fix Listings view. The data source is `/api/leaderboards?marketplace=US&inStockOnly={bool}`.

#### 16.7.2 In Stock Only filter (re-rank)

A single toggle at the top of the dashboard re-ranks all four leaderboards based on a JOIN against the `inventory_cache.blank_inventory` table (§5.6). When enabled:

- Listings whose `base_sku` has zero stock at the relevant warehouse (FL for US, UK for UK) are excluded
- Counts and rankings recompute server-side
- The operator sees only the **actionable** subset (29% of catalog in the US run, per §7.5)

The toggle state is stored in URL search params so a refresh preserves it. The compliance scan output itself is unchanged — the filter is a presentation-layer concern.

#### 16.7.3 Inventory source dropdown + Refresh button

Top-right of the dashboard:

- **Source dropdown:** `Supabase ▼ | BigQuery` — selects which source the next refresh uses
- **Refresh Inventory button:** triggers `POST /api/inventory/refresh?source={selected}` → spawns `listings-pipeline inventory-refresh --source {selected} --force` as a subprocess
- **Status pill:** shows cache age (e.g. "Fresh (0.3h)" green, "Stale (28h)" amber, "Missing" red) — pulses if currently refreshing
- **Refresh time estimate:** ~1 s for Supabase, ~3 s for BigQuery (per §5.6.2)

#### 16.7.4 File selector — searchable dropdown, not free-text input

The §16.2 Page 1 spec called for a "file path text input". The shipped version (commit `7129ee6`) replaces this with a **searchable dropdown** that lists real `.txt` and `.csv` files in `~/Downloads/`, `~/Desktop/`, and `~/Documents/`, sorted by modification time (most recent first). The dropdown is virtualised (40+ files in ~/Downloads is normal) and supports type-to-filter.

This eliminates two operator-error classes:
1. Typos in the file path (the §16.2 input was raw text, with no validation until the pipeline ran)
2. Forgetting which file was just downloaded (the operator can pick the top item by date)

The text input is preserved as a fallback for files outside the three search roots.

#### 16.7.5 Modern Ecell Style Guide 2.0

Per `01-Wiki/33-design-system/MODERN_STYLE_GUIDE.md` (referenced in §16.4): the shipped UI uses the **white background** variant (commit `4f47958`) per Cem's late-stage call rather than the gradient `bg-gradient-to-br from-slate-50 to-blue-50` originally specced in §16.4. Glassmorphic cards, Cobalt gradient buttons, and pulse-animated status pills are all in. Sidebar is the `w-56` glassmorphic spec from §16.4 with the cobalt active state.

#### 16.7.6 Full API route inventory (as-built)

Updates to the §16.3 table:

| Route | Method | Notes (vs §16.3) |
|---|---|---|
| `/api/process` | POST | As specced. Subprocess timeout bumped to 90 min (§7.5.5); explicit `PYTHONPATH` (§13.2.1). |
| `/api/status` | GET | As specced. |
| `/api/list-files` | GET | **New.** Backs the file selector dropdown (§16.7.4). Returns files from ~/Downloads/, ~/Desktop/, ~/Documents/ with mtime. |
| `/api/dashboard` | GET | **New.** Returns the 4 summary cards (Total / Compliant / Non-Compliant / Actionable). |
| `/api/leaderboards` | GET | **New.** Returns the 4-leaderboard payload (§16.7.1). Honours `inStockOnly` query param. |
| `/api/inventory/status` | GET | **New.** Returns `cache_meta` + per-warehouse breakdown for the dashboard pill (§16.7.3). |
| `/api/inventory/refresh` | POST | **New.** Triggers `inventory-refresh --source {supabase\|bigquery} --force`. |
| `/api/inventory-check` | POST | As specced — but largely superseded by the dashboard's `inStockOnly` toggle, kept for backward compat with the §16.2 flow. |
| `/api/export` | GET | As specced. |
| `/api/revision` | POST | Specced; awaiting middleware endpoint (§16.5). |

---

## 17. Out of Scope (Explicit)

To constrain Codex audit scope, the following are NOT subject to review:

- Listing content quality (titles, bullets, images, A+ Content) — owned by `listing-forge`
- Listing creation, suppression handling, or IP takedown response — manual / human only
- Translation / localisation of listing content — manual
- Order data ingestion — owned by procurement / Hermes
- Inventory data ingestion — owned by procurement-system
- Pricing / repricing / coupon strategy — owned by `30-autopricer` and pricing team
- Bulk template upload to Seller Central — owned by Jay Mark (manual workflow)
- The Layer 0 scoring engine itself — owned by `amazon-unified-score`
- The procurement reorder engine — owned by `procurement-system`
- Shipping template UPLOAD via SP-API feed — out of scope per Cem's no-API constraint

---

## 17. References

- [[HARRY_HANDOFF_LISTINGS_DELTA_DB]] — Phase 1 spec from Ava (2026-03-30)
- [[SHIPPING_TEMPLATE_BULK_FIX_BRIEF]] — Jay Mark's urgent fix brief (2026-03-30)
- [[02-Projects/procurement/PROCUREMENT_SYSTEM_SPEC]] — procurement data model (Ava, 2026-03-20)
- [[02-Projects/procurement/HARRY_HANDOFF]] — procurement Phase 1 handoff
- [[02-Projects/procurement/LAYER0_COMPLIANCE_INTEGRATION]] — the Layer 0 ↔ procurement contract (this session, 2026-04-15)
- `~/Downloads/listings-data-pipeline-architecture (1).md` — Perplexity LLM council pipeline doc (referenced for §4 architecture rationale and §6 validation rules)
- `~/Downloads/layer0-shipping-template-validation (1).md` — Perplexity Layer 0 doc
- `~/Desktop/Repos/amazon-unified-score/PROJECT_BRIEF.md` — sibling project brief
- `~/.claude/plans/polymorphic-knitting-hippo.md` — this session's plan addendum
- The actual Amazon Seller Central All Listings Reports in `~/Downloads/` (sample names: `Amazn US last 90 days BusinessReport-4-11-26.csv`, etc.)

---

## 18. Definition of Done

This PRD is "done" when:

1. ✅ All sections written (this document)
2. ⏳ Codex adversarial review complete and questions §15 answered
3. ⏳ Cem reviews and approves backend choice (DuckDB / MySQL / pandas)
4. ⏳ Harry confirms Phase 1 status (built / partial / not started)
5. ⏳ Jay Mark reviews §11.3 bulk fix workflow
6. ⏳ procurement-session reviews [[LAYER0_COMPLIANCE_INTEGRATION]] (separate document)
7. ⏳ SOP document (`LISTINGS_PIPELINE_SOP.md`) approved alongside this PRD

Implementation does not start until all 7 are checked.

---

*This PRD intentionally produces operational decisions, not just documentation. Every section is something the implementer needs to act on or defend in audit. Sections marked with ⏳ above are blockers for the build phase.*
