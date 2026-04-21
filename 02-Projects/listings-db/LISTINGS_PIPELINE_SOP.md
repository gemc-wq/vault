# Listings Data Pipeline — SOP v1.2

> **Operator's runbook for the biweekly listings ingestion cycle**
>
> **Owner:** Cem (downloads + runs via UI), Harry (script maintenance), Jay Mark (template fixes)
> **Date:** 2026-04-16 | **Status:** v1.2 — enriched with implementation findings
> **Companion doc:** [[LISTINGS_PIPELINE_PRD]] — PRD v1.2 (read first for architecture, see §16 for Web UI)
> **Previous failure context:** See PRD §2.2.1. This SOP is designed so marketplace contamination is structurally impossible; every step below exists to uphold that invariant.
>
> **Changelog**
> - **v1.2 (2026-04-16):** Added inventory cache pre-flight (§2.4), inventory refresh step (§5A.0), 4-leaderboard dashboard walkthrough (§5A.1.1), real-numbers dashboard expectations (§5.1.1), CLI inventory commands (§13.1), known issue PYTHONPATH/inventory-source diagnostics (§13.2).
> - **v1.1 (2026-04-16):** The operator now uses the **Listings Compliance Manager web UI** (`localhost:3001`) instead of CLI commands. The underlying Python pipeline is unchanged — the UI wraps it. CLI references below are kept for fallback/debugging but the primary workflow is UI-driven.

---

## 0. Cadence

| Marketplace | Frequency | Day | Time | Owner |
|---|---|---|---|---|
| US | Biweekly | Monday | 09:00 local | Cem downloads, script runs |
| UK | Biweekly | Monday | 09:30 local (after US completes) | Cem downloads, script runs |
| DE | Monthly | First Monday of month | 11:00 local | Cem (ad-hoc) |
| FR / IT / ES | Manual only | — | — | On request |

The US+UK cycle takes ~40 minutes end-to-end. Block 90 minutes on the Monday calendar for operator availability during the load, in case manual intervention is required.

### 0.1 Starting the UI

Before each cycle, ensure the web app is running:

```bash
cd ~/Desktop/Repos/amazon-listings-pipeline/web
npm run dev -- --port 3001
```

Then open `http://localhost:3001` in the browser. The sidebar shows 5 pages:
1. **Process Data** — where you start each cycle
2. **Dashboard** — compliance overview after processing
3. **Fix Listings** — bulk template fix selection
4. **SFP Conversion** — Reduced → Nationwide Prime upgrade (on-demand)
5. **Revisions** — submit changes via API or flat file

---

## 1. Roles

| Role | Responsibility | Escalation target |
|---|---|---|
| **Operator** (Cem) | Downloads files, runs script, approves pipeline reports | Harry |
| **Script maintainer** (Harry) | Fixes script bugs, handles Amazon schema changes | Cem |
| **Template fix operator** (Jay Mark) | Consumes `shipping_issues_*.csv`, executes bulk upload | Ava or Cem |
| **Audit reviewer** (Ava) | Reviews Wednesday audit report, flags anomalies | Cem |
| **Incident responder** (Harry → Cem) | Handles failed loads and contamination alerts | — |

---

## 2. Pre-Flight Checklist

Before starting a cycle, verify:

### 2.1 System state

- [ ] Mac Studio is powered on and unlocked
- [ ] `~/Downloads/` has at least 30 GB free
- [ ] `~/.openclaw/workspace/data/` has at least 10 GB free
- [ ] Internet connection stable (Supabase + BigQuery pushes need it)
- [ ] Previous cycle's `listing_snapshots_meta.status = 'completed'` (if in doubt: `sqlite3 ~/.openclaw/workspace/data/listings_us.db "SELECT * FROM listing_snapshots_meta ORDER BY id DESC LIMIT 3;"`)

### 2.2 Credentials

- [ ] `~/.openclaw/workspace/.env` exists and contains current Supabase + BigQuery keys (never committed to git)
- [ ] Seller Central login for `sellercentral.amazon.com` works
- [ ] Seller Central login for `sellercentral.amazon.co.uk` works

### 2.3 Previous cycle completion

- [ ] Run `./status.sh` to confirm previous cycle for each marketplace completed successfully
- [ ] If previous cycle status is `in_progress` → it crashed mid-load. Run recovery before starting new cycle (§9.1)
- [ ] If previous cycle status is `failed_contamination` → do NOT start new cycle. Escalate to Harry; investigate the source file first

### 2.4 Inventory cache freshness (added v1.2)

The dashboard's "In Stock Only" filter and the compliance scan's restricted-prefix logic both join against the local `inventory_cache.db` (PRD §5.6). If the cache is older than 24 hours, the actionable counts in the post-cycle dashboard will be wrong. Refresh **before** running the listings pipeline so the join sees fresh stock.

- [ ] Open the dashboard pill (top-right of `/dashboard` in the UI) — it shows cache age
  - **Green "Fresh (Nh)":** under 24h — no action
  - **Amber "Stale (Nh)":** 24–48h — refresh before proceeding
  - **Red "Missing":** no cache exists — refresh required
- [ ] Or run `listings-pipeline inventory-status` from the shell (see §13.1)
- [ ] If stale or missing: click **Refresh Inventory** (default source: Supabase, ~1s) or run `listings-pipeline inventory-refresh --source supabase`
- [ ] On Supabase failure (e.g. service-key issue): switch the source dropdown to **BigQuery** and refresh again (~3s, requires `gcloud auth application-default login` to be current)

The inventory cache is **shared across marketplaces** (one file, not one per marketplace) so a single refresh covers both US and UK loads. Do not refresh between US and UK if the second load is starting within 24 hours.

---

## 3. Phase 0 — File Acquisition

### 3.1 Download the US All Listings Report

1. Open `sellercentral.amazon.com` in a browser
2. Navigate: **Reports → Inventory Reports → All Listings Report**
3. Click **Request Download**
4. Wait 2–5 minutes (Amazon generates the report asynchronously)
5. When ready, click **Download**
6. The browser saves the file to `~/Downloads/` with a name like `All+Listings+Report-MM-DD-YYYY.txt`
7. **Immediately rename the file** to `US_ALL_LISTINGS_{YYYY-MM-DD}.txt` using today's date
   - Example: `US_ALL_LISTINGS_2026-04-15.txt`
   - **This rename is mandatory.** The script will reject any file that doesn't match the naming pattern (G3 in PRD §6.0).

### 3.2 Download the UK All Listings Report

1. Open a **new browser tab** (do NOT close the US Seller Central tab)
2. Open `sellercentral.amazon.co.uk`
3. Same navigation: **Reports → Inventory Reports → All Listings Report**
4. Request, wait, download
5. Rename to `UK_ALL_LISTINGS_{YYYY-MM-DD}.txt`

### 3.3 Verify file sanity (manual, quick)

Before running the script, eyeball each file:

```bash
# File size (should be between 100 MB and 15 GB per PRD §6.1 gates 3 & 4)
ls -lh ~/Downloads/US_ALL_LISTINGS_*.txt
ls -lh ~/Downloads/UK_ALL_LISTINGS_*.txt

# First line should be the header row
head -n 1 ~/Downloads/US_ALL_LISTINGS_*.txt
# Expected: item-name, item-description, listing-id, seller-sku, ...

# Count rows (should be in the millions, not hundreds)
wc -l ~/Downloads/US_ALL_LISTINGS_*.txt
```

If any of these look wrong (file too small, header missing, row count unexpectedly low), **stop and re-download**. Do not proceed with a suspicious file.

### 3.4 DANGER — what NOT to do

- ❌ Do NOT open the file in Excel — it will truncate at ~1M rows and may save back with a corrupted format
- ❌ Do NOT unzip or modify the file in any way
- ❌ Do NOT rename a US file to `UK_*` "to save time" — this is exactly the failure mode §6.0 prevents
- ❌ Do NOT move the file out of `~/Downloads/` until the load is complete (the meta row stores the path)
- ❌ Do NOT concatenate multiple marketplace files into one
- ❌ Do NOT run two loads for the same marketplace on the same day with different files — the first load's snapshot date will clash

---

## 4. Phase 1 — Run the Pipeline

### 4.1 Run US load (via UI — primary method)

1. Open `http://localhost:3001` in the browser
2. On the **Process Data** page:
   - Select **United States (US)** from the Marketplace dropdown
   - Enter the file path: `~/Downloads/US_ALL_LISTINGS_2026-04-15.txt`
   - Click **`[Process Data]`**
3. The UI shows a step-by-step progress display:
   - Validating file (guardrails G1-G10)
   - Bulk loading via DuckDB
   - Enriching SKU fields + computing hashes
   - Detecting delta (NEW/UPDATED/REMOVED)
   - Committing to SQLite
   - Running compliance scan
   - Writing output files
4. On completion, the UI shows: total rows, shipping issues count, duration, and a **"View Dashboard →"** link

**CLI fallback** (if UI is unavailable):
```bash
cd ~/.openclaw/workspace
./load.sh --region US --file ~/Downloads/US_ALL_LISTINGS_2026-04-15.txt
```

What the script does (matching PRD §6.0 guardrails):

1. **G3 check (three-way agreement):**
   - Parses filename → extracts `US`
   - Compares to `--region US` flag → ✅ match
   - Opens `listings_us.db` → reads `_meta_marketplace.region` → `US` → ✅ match
   - If any mismatch: exits code 9 with message `ERROR: marketplace mismatch (filename=X, flag=Y, db=Z)`
2. **Validation gates 1–10** (PRD §6.1–6.2): filename pattern, encoding, headers, file size
3. **Bulk load into temporary DuckDB table** (in-memory, not persisted yet)
4. **G4 + G5 checks:** currency cross-check and shipping template cross-check on 1000-row sample
   - Mean price in USD range? ✅
   - Contains only `Reduced Shipping Template` / `Default Amazon Template` templates? ✅
   - If any foreign template found: exits code 11 with `ERROR: foreign shipping template detected — possible cross-marketplace contamination`
5. **Row hashing** (SHA-256 per row)
6. **Delta classification** (NEW / UPDATED / UNCHANGED / REMOVED)
7. **Commit to `listings_us.db`** via transaction — if the CHECK constraint in `amazon_listings_snapshot` fires on ANY row, the transaction is rolled back entirely (G2)
8. **G8 post-load contamination test:** runs the two sanity queries from PRD §6.0 G8 against the just-committed data
9. **Push delta to Supabase** (`active_listings`, `listings_delta`, `listings_shipping_issues` — all scoped to region='US')
10. **Push delta to BigQuery** (`listings_master` MERGE)
11. **Emit output CSVs** to `~/.openclaw/workspace/out/us/{cycle_id}/`
12. **Update `listing_snapshots_meta.status = 'completed'`**

Expected output on the terminal:

```
[2026-04-15 09:01:02] START US cycle 2026-W16
[2026-04-15 09:01:02] G3: filename=US, flag=US, db=US → MATCH
[2026-04-15 09:01:03] Validation gates 1-10: PASS
[2026-04-15 09:01:04] Bulk load: 9.2 GB → 4,087,163 rows (5 min 43 sec)
[2026-04-15 09:06:47] G4 currency check: mean=$24.12 (in USD range) → PASS
[2026-04-15 09:06:48] G5 template check: 87% Default, 13% Reduced, 0% foreign → PASS
[2026-04-15 09:06:50] Hash + parse: DONE (2 min 18 sec)
[2026-04-15 09:09:08] Delta: 8,412 NEW, 41,803 UPDATED, 4,032,491 UNCHANGED, 4,457 REMOVED
[2026-04-15 09:11:32] Commit to listings_us.db: OK
[2026-04-15 09:11:35] G8 contamination test: 0 rows with region != US → PASS
[2026-04-15 09:11:35] G8 contamination test: 0 foreign templates → PASS
[2026-04-15 09:11:40] Supabase push: 54,672 delta rows (3 min 12 sec)
[2026-04-15 09:14:52] BigQuery merge: completed (2 min 05 sec)
[2026-04-15 09:16:57] Output CSVs: ~/.openclaw/workspace/out/us/2026-W16/
[2026-04-15 09:16:58] ✅ US cycle 2026-W16 COMPLETED in 15 min 56 sec
```

#### 4.1.1 Expected wall-clock — real numbers from 2026-04-16 (added v1.2)

The §0 estimate of "~40 minutes end-to-end" was sized before the perf fixes in PRD §7.5. Today's reality is much faster:

| Phase | 2026-04-16 actual (US 6.7 GB / 3.1M rows) |
|---|---|
| Validation gates G1–G5, G18–G20 | < 1 s |
| Bulk load (DuckDB, file-backed) | 17.1 s |
| Hash + enrich (SQL-based) | 12.3 s |
| Delta classify | 1.5 s |
| Commit to SQLite | 94.1 s ← dominant cost |
| Compliance scan + CSV emit | < 20 s |
| **Wall clock total** | **~150 s (2.5 min)** |

A full US + UK cycle therefore completes in ~5 minutes today, not 40. **Continue to block 90 minutes on the calendar** because:
1. The first run on a fresh DB (no previous snapshot to diff) takes longer due to every row being NEW
2. Supabase / BigQuery push timings are not yet measured at full volume — assume worst case
3. Operator time for sanity checks + dashboard review + Jay Mark handoff is unchanged

If the operator sees wall-clock > 10 min on a normal cycle, treat as a perf regression and check the §13.2 known-issues list before raising an alert.

### 4.2 Run UK load (sequentially, NOT in parallel)

```bash
./load.sh --region UK --file ~/Downloads/UK_ALL_LISTINGS_2026-04-15.txt
```

**Why sequentially and not in parallel:** SQLite supports multiple reader files but the pipeline's DuckDB load phase is memory-intensive. Running both at once would push Mac Studio beyond its RAM budget and risk OOM kills. Sequential takes ~35 min total; parallel would take ~25 min but risks both cycles crashing. The 10 min saved isn't worth the recovery time.

### 4.3 Monitor the run

Open a second terminal and tail the log:

```bash
tail -f ~/.openclaw/workspace/logs/load_$(date +%Y%m%d)_*.log
```

Watch for:

- **Green:** `PASS`, `OK`, `COMPLETED`
- **Yellow:** `WARN` (non-abort issues, worth noting but pipeline continues)
- **Red:** `ERROR`, `ABORT`, `FAILED_CONTAMINATION` — STOP and go to §9

---

## 5. Phase 2 — Review the Output

### 5.1 Pipeline report

After each marketplace completes, read the report:

```bash
cat ~/.openclaw/workspace/out/us/2026-W16/pipeline_report.json | jq .
```

Expected fields:

```json
{
  "region": "US",
  "cycle_id": "2026-W16",
  "snapshot_date": "2026-04-15",
  "source_file": "~/Downloads/US_ALL_LISTINGS_2026-04-15.txt",
  "file_sha256": "a1b2c3...",
  "total_rows": 4087163,
  "valid_rows": 4087159,
  "rejected_rows": 4,
  "delta": {
    "new": 8412,
    "updated": 41803,
    "unchanged": 4032491,
    "removed": 4457
  },
  "validation_gates_passed": 17,
  "validation_gates_failed": 0,
  "g8_contamination_test": "pass",
  "supabase_push": { "rows": 54672, "duration_sec": 192 },
  "bigquery_merge": { "rows": 54672, "duration_sec": 125 },
  "output_files": [
    "listings_delta_us_2026-04-15.csv",
    "shipping_issues_us_2026-04-15.csv",
    "compliance_flags_us_2026-04-15.csv"
  ],
  "status": "completed",
  "duration_sec": 956
}
```

**Sanity checks to perform manually:**

| Field | Acceptable range | If outside range |
|---|---|---|
| `total_rows` | Within ±20% of previous cycle | Investigate before approving |
| `delta.new` | 0–50,000 | > 50K suggests a bulk listing upload happened; confirm with team |
| `delta.removed` | 0–10,000 | > 10K suggests bulk suppression or Amazon policy action; escalate |
| `rejected_rows` | 0–4,000 (< 0.1% of total) | > 4K means validation rules are catching real issues — investigate |
| `g8_contamination_test` | `pass` | `fail` = HARD STOP, see §9.2 |

### 5.2 Delta CSV

Spot-check a handful of changed rows:

```bash
head -n 20 ~/.openclaw/workspace/out/us/2026-W16/listings_delta_us_2026-04-15.csv
```

Verify you recognise the SKUs and the changes look plausible (no prices dropping to $0.01, no templates suddenly changing to `Nationwide Prime` in a US file).

### 5.3 Shipping issues CSV — handoff to Jay Mark

```bash
wc -l ~/.openclaw/workspace/out/us/2026-W16/shipping_issues_us_2026-04-15.csv
```

Expected: a few thousand rows for the first cycle (backlog of wrong-template listings), fewer each subsequent cycle as Jay Mark works through them.

Copy the two CSVs (US + UK) to Jay Mark's handoff folder:

```bash
cp ~/.openclaw/workspace/out/us/2026-W16/shipping_issues_us_2026-04-15.csv \
   ~/Dropbox/Shared/jay_mark/weekly_inbox/
cp ~/.openclaw/workspace/out/uk/2026-W16/shipping_issues_uk_2026-04-15.csv \
   ~/Dropbox/Shared/jay_mark/weekly_inbox/
```

Then send Jay Mark a short Slack message: `Weekly template fixes ready in your inbox: US=X rows, UK=Y rows. Critical+restricted rows flagged — skip those per SOP.`

### 5.4 Compliance flags CSV — procurement handoff

The `compliance_flags_*.csv` file does NOT go to Jay Mark. It goes to whoever runs the procurement-system session when it next picks up [[LAYER0_COMPLIANCE_INTEGRATION]]. For now, just confirm the file exists and has non-zero rows:

```bash
wc -l ~/.openclaw/workspace/out/us/2026-W16/compliance_flags_us_2026-04-15.csv
```

---

## 5A. Phase 2A — Dashboard Review + Inventory Check (via UI, added v1.1)

After processing completes, the operator reviews compliance in the web UI instead of manually reading JSON files.

### 5A.0 Inventory cache check (added v1.2)

Before reading any compliance number on the dashboard, glance at the **inventory cache pill** in the top-right of `/dashboard`:

- **Green "Fresh (Nh)":** under 24h — the actionable count below it is trustworthy
- **Amber "Stale (Nh)":** 24–48h — still readable but the actionable count may slightly overstate (some "in stock" SKUs may have been depleted since the last refresh)
- **Red "Missing":** no cache exists — actionable count is undefined; refresh before drawing any conclusions

If amber or red: click **Refresh Inventory** (next to the pill). Source dropdown defaults to Supabase (~1s); switch to BigQuery (~3s) only if Supabase fails. The dashboard auto-refreshes when the cache update completes. See PRD §5.6 for what's in the cache.

### 5A.1 Dashboard review

1. Click **"View Dashboard →"** from the process completion screen (or navigate to `/dashboard` in the sidebar)
2. Review the 4 summary cards:
   - **Total Listings Loaded** — should match expected row count (±20%)
   - **Compliant** — listings on the correct shipping template
   - **Non-Compliant** — listings on the wrong template (this is the backlog to fix)
   - **Actionable** — populated after inventory check (see §5A.0)
3. Toggle **In Stock Only** to re-rank the leaderboards based on the inventory cache JOIN — this drops non-compliant listings whose blanks are out of stock at the primary warehouse (FL for US, UK for UK). The Actionable card and all leaderboard counts recompute server-side.

#### 5A.1.1 Reading the four leaderboards

The dashboard shows **four parallel leaderboards** (PRD §16.7.1) instead of the earlier hierarchy tree. Each card lists the top 20 groups by non-compliant count:

| Leaderboard | What it tells you | When to act on it |
|---|---|---|
| **Product Type** | Which product line is bleeding compliance (HLBWH, HTPCR, HC, …) | Use this to plan a Jay Mark batch — one product type at a time keeps the flat-file upload coherent |
| **Device** | Which device model has the most wrong-template listings (IPH17PMAX, GP9PRO, …) | Cross-reference with new device launches — a freshly-listed device often has all-Default templates that need a one-shot upgrade |
| **Product × Device** | Specific intersection (HTPCR-IPH17PMAX) | Highest-leverage single fix — usually shows the biggest concrete batch you can ship to Jay Mark today |
| **Licence** | Brand/IP grouping (Naruto, Peanuts, Disney) derived from `design_code` prefix | Tells you whether wrong templates correlate with a specific licensor's catalog — useful for prioritising during a rights renewal |

Each card row shows: rank, group label, total listings, non-compliant count, non-compliant %, severity dot. **Click any row** → navigates to Fix Listings (`/listings`) pre-filtered to that group.

#### 5A.1.2 Sanity-check the dashboard against §5.1 ranges

Before clicking through to fix anything, glance at the totals:

| Card | Sanity expectation | Investigate if |
|---|---|---|
| Total Listings Loaded | Within ±20% of previous cycle | Outside band → check `pipeline_report.json` row counts |
| Non-Compliant | Slowly decreasing cycle-over-cycle (Jay Mark is fixing them) | Increasing → either Amazon bulk-changed templates, or a new product type was launched on Default |
| Actionable (with In Stock Only) | < Non-Compliant (stock filter strictly subsets) | Equal → inventory cache is empty/missing, refresh per §5A.0 |
| Top product type % non-compliant | Typically 30–80% for HLBWH-class types | < 5% → scan ran on partial data; > 95% → scan logic regression, escalate to Harry |

For reference, the 2026-04-16 US run produced (per PRD §7.5):
- 1,888,789 non-compliant
- 543,082 actionable (29% of catalog)
- Top types: HLBWH 1,136,253 / HTPCR 477,538 / HC 244,371

### 5A.2 Run Inventory Check (legacy button — superseded by §5A.0/5A.1)

> **v1.2 note:** The original `[Run Inventory Check]` button is still present on the dashboard for backward compatibility, but its job is done by the §5A.0 cache pill + the §5A.1 "In Stock Only" toggle. The button now triggers an inventory cache refresh and then re-applies the In Stock filter. Use the toggle in normal operation; only use the button if the toggle is greyed out (which means the cache is missing entirely).

1. Click **`[Run Inventory Check]`** on the dashboard
2. The system refreshes the inventory cache (Supabase by default) and joins all non-compliant listings against `blank_inventory`
3. SKUs with **no stock at the primary warehouse** are filtered out (can't fix what we can't ship)
4. The **Actionable** card updates to show only SKUs that are both non-compliant AND in-stock
5. All four leaderboards update to reflect actionable counts

### 5A.3 Export CSV (if needed for offline review)

Click **`[Export CSV]`** to download the non-compliant + in-stock SKUs as a CSV file.

### 5A.4 Navigate to fix workflow

Two paths from the dashboard:

- **`[Fix Listings →]`** → Page 3 (bulk template fix, Default → Reduced or Default → Nationwide Prime)
- **`[SFP Conversion →]`** → Page 5 (selective upgrade, Reduced → Nationwide Prime, on-demand)

---

## 5B. Phase 2B — Fix Listings (via UI, added v1.1)

### 5B.1 Bulk template fix

1. Navigate to **Fix Listings** (`/listings`)
2. Use the filters to narrow down by product type, device, severity, or current template
3. Review the table — each row shows current template (red badge) and required template (green badge)
4. Select SKUs using checkboxes:
   - `[Select All]` — selects all visible rows
   - Individual checkboxes for fine-grained selection
5. Click **`[Send for Revision →]`** — takes selected SKUs to the Revision Builder (Page 4)

### 5B.2 Submit revisions

1. On the **Revisions** page (`/revisions`):
   - Use **bulk actions** to set template and price adjustment for all selected SKUs at once
   - Or adjust per-row if some SKUs need different treatment
2. Choose a submission method:
   - **API Update (recommended):** Click `[Submit Batch]` — submits to Amazon via the middleware. Batched at 200 SKUs. Waits for Amazon confirmation before sending the next batch. Monitor the batch status display.
   - **Flat File Export:** Click `[Download CSV]` — generates an Amazon Inventory Loader format file. Hand off to Jay Mark for manual upload via Seller Central.
3. For API submission: **wait for all batches to show "Confirmed by Amazon"** before closing the page. Failed batches will be highlighted and can be retried.

---

## 5C. Phase 2C — SFP Conversion (via UI, on-demand, added v1.1)

This is a separate workflow from the bulk fix. Use it when upgrading specific product/device/licence combinations from Reduced Shipping to Nationwide Prime (UK SFP).

1. Navigate to **SFP Conversion** (`/sfp`)
2. Use the **cascading filter chain**:
   - Select **Product Type** (type to search, e.g. "HTPCR")
   - Select **Device Model** (narrows to devices under that product type)
   - Select **Design/Licence** (narrows to designs under that device, shows licence name + count)
3. Click **`[Show Matching Listings]`**
4. Review the matching SKUs — greyed-out rows have no UK stock and cannot be upgraded
5. Select the SKUs to upgrade
6. Click **`[Send to Revision Builder →]`** — takes them to Page 4 with template pre-set to "Nationwide Prime"
7. Adjust price if needed (SFP may require absorbing shipping cost into the listing price)
8. Submit via API or flat file (same as §5B.2)

---

## 6. Phase 3 — Approve the Cycle

Once both US and UK reports are reviewed and sanity checks pass (either via dashboard or CLI):

```bash
./approve.sh 2026-W16
```

This command:

1. Updates `listing_snapshots_meta.status = 'approved'` on both DB files
2. Posts a cycle summary to Slack `#data-pipeline`
3. Triggers the Wednesday audit's input — it now has fresh data to audit
4. Archives the old output folder from 12 weeks ago (rotating retention)

If approval is skipped or forgotten, downstream consumers continue to work (they read `status = 'completed'` as well), but the cycle is flagged "unreviewed" in the next report.

---

## 7. Phase 4 — Handoff to Downstream Consumers

No explicit action needed — all downstream reads happen via Supabase and BigQuery, which are now populated. The following systems pick up the new data automatically:

| Consumer | Data source | Pickup timing |
|---|---|---|
| procurement-system dashboard | Supabase `active_listings` + `blank_inventory` | On next user page load |
| amazon-unified-score Layer 0 | Supabase `active_listings` + `listings_shipping_issues` | On next scheduled scoring run (Monday afternoon) |
| Wednesday audit cron | Supabase `listings_shipping_issues` | Wednesday 09:00 local |
| Jay Mark | Dropbox inbox CSV | Whenever he starts work |
| Hermes / OpenClaw | Supabase REST API | On demand |

---

## 8. Phase 5 — Post-Cycle Cleanup

### 8.1 Source file archival

After 24 hours (once you're sure the cycle doesn't need to be re-run from the source), move the source files out of `~/Downloads/`:

```bash
mkdir -p ~/.openclaw/workspace/archive/2026-W16/
mv ~/Downloads/US_ALL_LISTINGS_2026-04-15.txt \
   ~/.openclaw/workspace/archive/2026-W16/
mv ~/Downloads/UK_ALL_LISTINGS_2026-04-15.txt \
   ~/.openclaw/workspace/archive/2026-W16/
```

Archived files are compressed after 30 days:

```bash
find ~/.openclaw/workspace/archive/ -name "*.txt" -mtime +30 -exec gzip {} \;
```

### 8.2 SQLite snapshot pruning

Run monthly (separate cron):

```bash
./prune_snapshots.sh --keep 6
```

Keeps the most recent 6 snapshots per marketplace file; deletes older rows from `amazon_listings_snapshot`. Preserves `listing_snapshots_meta` entries (metadata is tiny).

### 8.3 Output CSV retention

Output CSVs are kept for 12 weeks, then archived to iCloud / Time Machine. No manual action — the `approve.sh` script handles rotation.

---

## 9. Failure Procedures

### 9.1 Previous cycle status = `in_progress`

The previous cycle crashed partway through. Recover before starting a new cycle.

```bash
# For each marketplace that has an in-progress row:
./rollback.sh --region US --cycle 2026-W15

# Verify clean state
sqlite3 ~/.openclaw/workspace/data/listings_us.db \
  "SELECT * FROM listing_snapshots_meta WHERE status = 'in_progress';"
# Should return 0 rows
```

`rollback.sh` performs:

1. DELETE all rows from `amazon_listings_snapshot` where `snapshot_date` matches the failed cycle
2. Update `listing_snapshots_meta.status = 'rolled_back'`
3. Delete any partial output CSVs
4. Does NOT touch Supabase or BigQuery (the crash happened before they were written)

### 9.2 G8 contamination test FAILED

This is the P0 event. DO NOT PROCEED.

Script behaviour:

1. Transaction rolled back automatically (nothing committed)
2. Meta row set to `status = 'failed_contamination'`
3. HIGH-severity Slack alert posted to `#data-pipeline`
4. Exit code 12

Operator procedure:

1. **Stop.** Do not re-run the pipeline.
2. **Verify the file** — is it really the right marketplace? Check filename, open it in `less` and grep for marketplace-exclusive templates:
   ```bash
   grep -c "Nationwide Prime" ~/Downloads/US_ALL_LISTINGS_2026-04-15.txt
   # If > 0, this is actually a UK file renamed to US
   ```
3. **If the file is wrong:** delete it, re-download the correct file, rename correctly, retry
4. **If the file appears correct:** escalate to Harry — this is a script bug, not an operator error
5. **Never try to "force" the load past the contamination check** — there is no `--force` flag because there should be no situation in which it's safe to bypass this

### 9.3 Validation gate failures (non-contamination)

| Exit code | Failed gate | Operator action |
|---|---|---|
| 1 | Generic script error | Read logs, escalate to Harry |
| 2 | Gate 1 (filename pattern) | Rename file to `{MP}_ALL_LISTINGS_{YYYY-MM-DD}.txt` |
| 3 | Gate 2 (file exists / readable) | Check file path; check permissions |
| 4 | Gate 3 (file too small) | Re-download; previous download was truncated |
| 5 | Gate 4 (file too large) | Investigate — may be concatenated or duplicated |
| 6 | Gate 8 (header validation) | Amazon may have changed schema. Escalate to Harry URGENTLY |
| 7 | Gate 10 (row-level column count) | Data quality issue; investigate sample rows |
| 8 | Gate 16 (row count delta > 20%) | Confirm with team whether a bulk upload or mass suppression happened |
| 9 | G3 (marketplace mismatch) | File/flag/db don't agree; check all three |
| 10 | G2 (CHECK constraint fired) | Script bug; escalate to Harry |
| 11 | G5 (foreign shipping template) | File is contaminated or wrong marketplace; investigate |
| 12 | G8 (post-load contamination test) | See §9.2 |
| 13 | Supabase push failed | Check `.env` credentials; retry with `./load.sh --resume` |
| 14 | BigQuery merge failed | Check GCP credentials; retry with `./load.sh --resume` |

### 9.4 Rollback procedure (manual)

If you need to roll back an already-approved cycle (e.g. discovered 24 hours later that the source file was bad):

```bash
./rollback.sh --region US --cycle 2026-W16 --confirm
```

This deletes the snapshot rows from SQLite, reverts Supabase to the prior cycle's state (via the retained previous snapshot), and uses BigQuery time-travel to recover `listings_master`.

BigQuery time-travel is only available for 7 days — after that, rollback requires manual reconstruction from SQLite (whichever snapshots still exist per retention policy).

---

## 10. Monitoring & Alerts

### 10.1 Slack channels

| Channel | Purpose | Severity |
|---|---|---|
| `#data-pipeline` | All pipeline status messages | INFO / WARN / CRITICAL |
| `#data-pipeline-alerts` | Page-worthy alerts only | CRITICAL |
| `#shipping-template-audit` | Wednesday audit output | INFO |

### 10.2 Alert conditions

| Condition | Channel | Action |
|---|---|---|
| Cycle completed | `#data-pipeline` | Informational summary |
| Rejected rows > 1% | `#data-pipeline` | Operator review |
| Contamination test failed | `#data-pipeline-alerts` | Incident response (Harry on-call) |
| Load duration > 30 min | `#data-pipeline` | Performance regression investigation |
| Supabase push failed | `#data-pipeline` | Retry from next operator step |
| No cycle run in 16 days | `#data-pipeline-alerts` | Biweekly cadence slipping; escalate |

---

## 11. Recovery from Mac Studio Loss

If Mac Studio is unavailable (hardware failure, theft, iCloud restore needed):

1. Provision new Mac Studio with latest macOS
2. Restore `~/.openclaw/workspace/` from Time Machine if available
3. If Time Machine not available: clone the pipeline repo, run `./bootstrap.sh` to recreate empty SQLite files and the bootstrap `_meta_marketplace` rows
4. Re-download the most recent US + UK All Listings Reports from Seller Central
5. Run the normal pipeline — the first cycle after recovery will classify every row as NEW (no previous snapshot to diff against), which is correct behaviour
6. Subsequent cycles work normally

RTO: 4 hours (provisioning new machine + re-downloading is the slow step)
RPO: 0 (Amazon is the source of truth; no data is actually "lost")

---

## 12. Audit Log

Every invocation of `load.sh`, `approve.sh`, and `rollback.sh` writes an audit row to `~/.openclaw/workspace/audit/audit.log`:

```
2026-04-15T09:01:02  cem  load.sh --region US --file US_ALL_LISTINGS_2026-04-15.txt  exit=0
2026-04-15T09:16:58  cem  (internal) G8 contamination test  result=pass
2026-04-15T09:17:00  cem  load.sh completed                                          exit=0
2026-04-15T09:20:12  cem  load.sh --region UK --file UK_ALL_LISTINGS_2026-04-15.txt  exit=0
2026-04-15T09:36:41  cem  load.sh completed                                          exit=0
2026-04-15T09:37:15  cem  approve.sh 2026-W16                                        exit=0
```

The audit log is append-only, readable to everyone, writable only by the pipeline scripts. Useful for:

- Post-incident review (when did this cycle start, what was the file, what was the exit code?)
- Weekly operator hours tracking (how long did the cycle take?)
- Codex audit evidence trail

---

## 13. Appendix A — Common Error Messages

| Error | Meaning | Fix |
|---|---|---|
| `ERROR: marketplace mismatch (filename=UK, flag=US, db=US)` | You renamed the file but forgot to update the `--region` flag, or vice versa | Make all three agree; no `--force` option |
| `ERROR: foreign shipping template detected` | The file contains templates that don't belong in this marketplace **at ≥ 5%** (per PRD §6.7.1) | This is almost certainly a wrong-marketplace file; re-verify upstream. If the percentage is < 5% the gate now passes — these are mis-tags the compliance scan will flag for fixing |
| `sqlite3.IntegrityError: CHECK constraint failed: region` | A row was being inserted with the wrong region → G2 fired | Script bug; escalate to Harry |
| `ERROR: file hash matches previous cycle` | You're trying to load the same file twice | Re-download a fresh report, or skip this cycle if the source is unchanged |
| `ERROR: header validation failed — unexpected column 'x-new-col'` | Amazon added a new column | Harry updates the script schema to accommodate; may require PRD update |
| `ERROR: row count delta > 20%` (from Gate 16) | Previous cycle had Y rows, this cycle has significantly more/fewer | Check with team — did anyone do a bulk upload or mass suppression? |
| `ERROR: Supabase 500 on batch N` | Transient Supabase issue | Wait 5 minutes, retry with `./load.sh --resume 2026-W16` |
| `ModuleNotFoundError: No module named 'listings_pipeline'` (from Next.js subprocess) | Editable install `.pth` not picked up — see PRD §13.2.1 | Confirm `PYTHONPATH=<repo>/src` is set in the API route's spawn env. CLI from shell is unaffected |
| `SUPABASE_SERVICE_KEY not set` (from `inventory-refresh`) | `.env` file not loaded or key missing | Confirm `~/.openclaw/workspace/.env` exists with `SUPABASE_SERVICE_KEY=...`; restart the Next.js dev server so it re-reads `.env` |
| `google.auth.exceptions.DefaultCredentialsError` (from BQ inventory refresh) | gcloud ADC expired or never set | Run `gcloud auth application-default login` and retry |
| Inventory pill stuck on **Red "Missing"** after refresh | Cache file written but `cache_meta` row not committed (e.g. crash mid-write) | Delete `~/.openclaw/workspace/data/inventory_cache.db` and refresh again; the loader recreates the schema |
| Dashboard shows **0 actionable** with stock filter on, but Non-Compliant is non-zero | Inventory cache is empty or every base_sku missing | Run `listings-pipeline inventory-status` to confirm row count > 0; if 0, refresh; if > 0, escalate to Harry (likely a join key mismatch — `base_sku` vs `item_code` casing) |

### 13.1 Inventory CLI commands (added v1.2)

The web UI's Refresh Inventory button wraps these CLI commands. Use them directly when debugging or when the UI is unavailable.

```bash
# Refresh from Supabase (default, ~1s)
listings-pipeline inventory-refresh

# Refresh from BigQuery (~3s, fallback)
listings-pipeline inventory-refresh --source bigquery

# Force refresh even if cache is fresh
listings-pipeline inventory-refresh --force

# Override TTL
listings-pipeline inventory-refresh --max-age-hours 6

# Show current cache state
listings-pipeline inventory-status
```

`inventory-status` output example:
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

If the per-warehouse breakdown looks off (e.g. FL has 0 items), the source has a problem — switch to the other source and refresh.

### 13.2 Known issues — long-running diagnostics (added v1.2)

These don't block operations today but are worth knowing about:

#### 13.2.1 PYTHONPATH not propagated through Next.js subprocess

**What you'll see:** Direct CLI calls from the shell work, but the same command spawned by the Next.js API route (Process Data button, Refresh Inventory button) fails with `ModuleNotFoundError: listings_pipeline`.

**Workaround in place:** Every API route under `web/src/app/api/` explicitly sets `PYTHONPATH=<repo>/src` in the subprocess env before spawning. This is brittle — adding a new API route that forgets to set it will break in this exact way.

**Don't:** Try to "fix" this by reinstalling the venv or rerunning `pip install -e .` — it's not an install issue, it's an env-propagation issue between Node and Python.

**If you need to investigate:** Add a temporary `printenv` call inside the spawned process and check what the API route is actually passing through. Likely culprits: a `PATH` sanitisation by Next.js dev server, or a system Python being resolved before the venv.

#### 13.2.2 Supabase inventory source can be silently stale

The Supabase `blank_inventory` table is synced daily by Harry's job from the BigQuery view. If that sync stalls, the cache loader (using Supabase as the default source) will happily refresh from a stale snapshot and `cache_meta.refreshed_at` will look fresh while the underlying numbers are days old.

**Detection:** Run `listings-pipeline inventory-refresh --source bigquery` and compare row counts against the previous Supabase refresh. A material divergence (> 10%) indicates Supabase is stale; switch to BigQuery as the default until Harry's sync is restored.

**Long-term fix:** PRD §15 open question 20 — make the loader cross-check the source's own freshness signal and warn.

---

## 14. Appendix B — Useful Diagnostic Queries

### 14.1 How many listings per marketplace right now?

```sql
-- Run against listings_us.db
SELECT COUNT(*), region FROM amazon_listings_snapshot
WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM amazon_listings_snapshot)
GROUP BY region;
-- Should return a single row with region='US' (never multiple — that would indicate contamination)
```

### 14.2 How many wrong-template listings in the latest snapshot?

```sql
-- US
SELECT COUNT(*) FROM amazon_listings_snapshot
WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM amazon_listings_snapshot)
  AND fulfillment_channel = 'DEFAULT'
  AND merchant_shipping_group != 'Reduced Shipping Template';
```

### 14.3 How has the shipping template backlog evolved?

```sql
SELECT snapshot_date,
       COUNT(*) FILTER (WHERE merchant_shipping_group = 'Reduced Shipping Template') AS correct,
       COUNT(*) FILTER (WHERE merchant_shipping_group != 'Reduced Shipping Template'
                        AND fulfillment_channel = 'DEFAULT') AS wrong
FROM amazon_listings_snapshot
WHERE region = 'US'
GROUP BY snapshot_date
ORDER BY snapshot_date DESC
LIMIT 10;
```

### 14.4 Which high-revenue SKUs suddenly REMOVED in the last cycle?

```sql
SELECT seller_sku, item_name, price, quantity, last_changed_date
FROM amazon_listings_snapshot
WHERE change_type = 'REMOVED'
  AND snapshot_date = (SELECT MAX(snapshot_date) FROM amazon_listings_snapshot)
  AND price > 20
ORDER BY price DESC
LIMIT 50;
```

Review for potential IP takedowns or suppressions worth escalating.

---

## 15. Definition of Done (for operator)

A cycle is "done" when:

1. ✅ Both US and UK `load.sh` exit with code 0
2. ✅ Pipeline reports for both marketplaces show `status: completed`, `g8_contamination_test: pass`
3. ✅ Sanity checks in §5.1 all within acceptable ranges
4. ✅ Shipping issues CSVs delivered to Jay Mark's inbox
5. ✅ `approve.sh 2026-W{NN}` run successfully
6. ✅ Slack summary posted to `#data-pipeline`

If any step fails, the cycle is NOT done. Do not mark it complete in the weekly operator log until all 6 pass.

---

## 16. Open Questions for Codex Audit (SOP-specific)

These complement the PRD's §15 questions but focus on operational risk:

1. **Is sequential US→UK loading really better than parallel?** PRD §4.2 argues yes for memory reasons. Codex should check whether the memory concern is real on a 64GB Mac Studio or whether parallel would be safe.

2. **Operator forgetfulness.** What if Cem downloads both files but only runs `load.sh US` and forgets UK? No gate catches this — the UK cycle just silently doesn't happen. Should there be a "paired cycle" enforcement?

3. **Concurrent operator sessions.** What if Cem runs `load.sh US` from his Mac Studio while Harry SSHes in and runs it from a second shell? Two concurrent writes to `listings_us.db` — does SQLite's single-writer lock handle this gracefully, or is explicit locking required?

4. **Timestamp skew.** If Mac Studio's clock is wrong, `snapshot_date` will be wrong, and delta detection might classify a current row as "older than" a future row. Should the script verify against NTP before starting?

5. **"Same file twice" edge case.** §13 exit code "file hash matches previous cycle" — is warning-and-skip correct, or should the script offer a `--force-refresh` path that re-runs downstream pushes without re-loading SQLite?

6. **Jay Mark workflow handoff.** §5.3 copies the CSVs to Dropbox. Is that the right path, or should it be direct-to-Slack-upload, or emailed, or put in a Supabase-backed web portal? Depends on Jay Mark's current workflow.

7. **Retry semantics.** `./load.sh --resume 2026-W16` is mentioned in §13 but not specced. What exactly does it resume — from the last completed phase, or from scratch skipping already-loaded rows?

8. **Audit log rotation.** `audit/audit.log` is append-only forever. When does it rotate? Should it be compressed / shipped to BigQuery for long-term storage?

9. **Bootstrap first run.** On a fresh install, `listings_us.db` doesn't exist yet. Does `load.sh` auto-create it, or must the operator run `./bootstrap.sh --region US` first? §11 mentions bootstrap but not where it's explicitly required.

10. **What's "approved" status used for?** §6 says `approve.sh` sets status to 'approved'. But §7 says downstream consumers read `status = 'completed'`. Is 'approved' actually used anywhere, or is it ceremonial?

---

## 17. References

- [[LISTINGS_PIPELINE_PRD]] — companion PRD, read first
- [[HARRY_HANDOFF_LISTINGS_DELTA_DB]] — Ava's original handoff (2026-03-30)
- [[SHIPPING_TEMPLATE_BULK_FIX_BRIEF]] — Jay Mark's fix brief (2026-03-30)
- [[02-Projects/procurement/LAYER0_COMPLIANCE_INTEGRATION]] — downstream consumer spec
- `~/.openclaw/workspace/scripts/sync_listings_delta.py` — existing Python implementation (pre-v1, superseded when this SOP is approved)

---

*This SOP is the operator's Monday runbook. Every deviation from these steps should be logged in the audit trail and justified in a post-cycle Slack message. The guardrails exist because contamination happened before; they are not optional.*
