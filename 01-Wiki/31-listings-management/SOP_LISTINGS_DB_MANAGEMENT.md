# SOP: Listings Database Management
**Version:** 1.0 DRAFT — For Cem Review
**Owner:** Ava | **Date:** 2026-04-05
**Status:** 🟡 DRAFT — awaiting Cem approval before implementation

---

## 1. Overview

The Listings DB is a local SQLite file (`data/local_listings.db`) on Mac Studio that holds all Amazon Active Listings snapshots for US and UK. It is the source of truth for:
- Weekly delta analysis (new/removed/changed SKUs)
- Product type breakdown by marketplace
- FBA penetration tracking
- HTPCR → HB401 coverage gap analysis

**Core principle:** One file, two snapshots per marketplace. Current week and prior week. Delta is always current minus prior.

---

## 2. Database Structure

```
data/local_listings.db
├── listings_current          ← US Active Listings, latest snapshot
├── listings_previous         ← US Active Listings, prior week snapshot
├── listings_uk_current       ← UK Active Listings, latest snapshot
├── listings_uk_previous      ← UK Active Listings, prior week snapshot
└── delta_log                 ← Load history: date, file, +new, -removed, ~changed
```

### Table schema (all listing tables identical):
| Column | Type | Notes |
|--------|------|-------|
| seller_sku | TEXT | Primary key. Format: TYPE-DEVICE-DESIGN-VARIANT |
| asin | TEXT | Amazon ASIN |
| item_name | TEXT | Listing title |
| price | REAL | Listed price |
| quantity | INTEGER | Available quantity |
| open_date | TEXT | Listing creation date (ISO format) |
| image_url | TEXT | Primary image URL |
| fulfillment_channel | TEXT | DEFAULT = FBM, AMAZON_NA = FBA |
| product_id | TEXT | EAN/GTIN |
| product_id_type | TEXT | EAN, GCID, etc. |

---

## 3. Weekly Load Process

### 3.1 Who runs it
**Executor:** Pixel agent (Gemini Flash — free)
**Triggered by:** Manual command from Cem or Ava, or Saturday night cron (once automated)

### 3.2 Step-by-step

**Step 1 — Download Active Listings reports**
- Source: Amazon Seller Central → Reports → Inventory → Active Listings Report
- Download: US + UK (separate accounts/regions)
- Report type: `GET_MERCHANT_LISTINGS_DATA` (active only — smaller than ALL_DATA)
- Filename format: `US Active+Listings+Report_MM-DD-YYYY.txt` and `UK Active+Listings+Report_MM-DD-YYYY.txt`
- Save to: `/Users/openclaw/.openclaw/workspace/data/downloads/`

> ⚠️ Once middleware BQ loader is fixed, Step 1 is automated via Cloud Run cron. Until then: manual download.

**Step 2 — Rotate snapshots (CRITICAL — do this BEFORE loading)**
```sql
DROP TABLE IF EXISTS listings_previous;
CREATE TABLE listings_previous AS SELECT * FROM listings_current;

DROP TABLE IF EXISTS listings_uk_previous;
CREATE TABLE listings_uk_previous AS SELECT * FROM listings_uk_current;
```
If this step is skipped, current and previous will be identical → delta = zero. This was the bug in the Apr 4 report.

**Step 3 — Load new snapshots**
```bash
python3 scripts/refresh_listings.py \
  --us "data/downloads/US Active+Listings+Report_MM-DD-YYYY.txt" \
  --uk "data/downloads/UK Active+Listings+Report_MM-DD-YYYY.txt" \
  --delete-after
```
The `--delete-after` flag removes source files after successful load (large file policy).

**Step 4 — Script computes and writes delta_log**
Script compares current vs previous, writes to delta_log:
```
run_date | file_name | total_rows | new_listings | removed_listings | changed_listings | runtime_seconds
```

**Step 5 — Run weekly report**
```bash
python3 scripts/weekly_listings_report.py
```
Executor: Pixel (Gemini Flash). Outputs to `results/weekly_listings_YYYY-MM-DD.md`.

**Step 6 — Post to Slack**
Pixel posts sanitised summary (no revenue) to `#eod-listings`.

---

## 4. Delta Calculation Rules

### Primary method: snapshot diff
```sql
-- New SKUs (in current but not in previous)
SELECT COUNT(*) FROM listings_current c
WHERE NOT EXISTS (SELECT 1 FROM listings_previous p WHERE p.seller_sku = c.seller_sku)

-- Removed SKUs (in previous but not in current)
SELECT COUNT(*) FROM listings_previous p
WHERE NOT EXISTS (SELECT 1 FROM listings_current c WHERE c.seller_sku = p.seller_sku)

-- Changed SKUs (same SKU, different price or quantity)
SELECT COUNT(*) FROM listings_current c
JOIN listings_previous p ON c.seller_sku = p.seller_sku
WHERE c.price != p.price OR c.quantity != p.quantity
```

### Secondary method: open_date (use when snapshots are identical)
```sql
-- New this week (created since last Saturday)
SELECT COUNT(*) FROM listings_current WHERE open_date >= '2026-MM-DD'
```
Use this as fallback only. It does not capture removals or price changes.

### Ground truth: delta_log
The delta_log is always correct — written at load time based on actual file comparison. When in doubt, trust delta_log over derived queries.

---

## 5. SKU Parsing Rules Applied

All analysis uses canonical parsing per `wiki/SKU_PARSING_RULES.md`:

```
seller_sku = TYPE-DEVICE-DESIGN-VARIANT
parts = seller_sku.split('-', 3)
```

| Position | Field | Rule |
|----------|-------|------|
| parts[0] | Product type | Strip F prefix → canonical type (except FLAG, F1309, FRND, FKFLOR) |
| parts[1] | Device code | Map via device_code_map.json for display name |
| parts[2] | Design code | Map via design_code_brand_map.json for license/brand |
| parts[3] | Variant | Display as-is |

**FBA detection:** `fulfillment_channel = 'AMAZON_NA'` OR product type starts with F (minus exceptions). Always combine FBA+FBM under canonical type for totals.

---

## 6. Report Output Format

Every weekly report must include these sections in this order:

1. **Executive summary** — 3-line snapshot: total listings, net change, highlight
2. **Delta by marketplace** — US and UK, new/removed/changed with % change WoW
3. **New listings by product type** — canonical types, count, % of new, brief note on any anomaly
4. **Catalog totals US vs UK** — side by side, flag where one market materially leads the other
5. **FBA penetration by type** — FBA%, flag any type below 1% that should be a priority
6. **Top 10 new design codes** — with license identified (NARUICO = Naruto Iconic etc.)
7. **Flags & actions** — anything requiring human decision

---

## 7. Anomaly Flags (auto-detect in script)

| Condition | Flag |
|-----------|------|
| Net new > 200K in one week | 🔴 Spike — check for data mixing or mass upload |
| Net removed > 50K in one week | 🔴 Mass delisting — investigate |
| Current and previous row counts identical | 🔴 Rotation bug — snapshots not rotated before load |
| New product type appearing for first time | 🟡 New type — confirm with Cem |
| FBA% on HTPCR > 5% or < 0.1% | 🟡 FBA shift — flag for Hermes review |
| UK total > 2× US total on any type | 🟡 Distribution imbalance |

---

## 8. Model Routing

| Task | Model | Rationale |
|------|-------|-----------|
| Run refresh_listings.py | Pixel (Gemini Flash) | Free, mechanical |
| Run weekly_listings_report.py | Pixel (Gemini Flash) | Free, mechanical |
| Post Slack summary | Pixel (Gemini Flash) | Free |
| Anomaly investigation | Gemma 4 local / Codex | Free |
| Strategic decisions on anomalies | Ava (Sonnet) | Only when human decision needed |

**Rule: Ava does not run scripts or generate reports. Ava reviews output and makes decisions.**

---

## 9. Known Issues & Fixes Applied

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Apr 4 report showed 0 delta | listings_previous was overwritten with same file as current | Always rotate snapshot BEFORE loading new file (Step 2) |
| 172K spike appeared inflated | Two weeks of loads (Mar 28 + Apr 4) done on same day — delta_log counted both | Future: load once per week, on schedule. Never backfill two weeks in same run. |
| UK data appeared to inflate US delta | UK file loaded after US on same day, confusion in reporting | US and UK are separate tables — no mixing. Spike was real HB1BK rollout. |
| BQ load OOM crash | Active Listings files are 5M+ rows, exceeds Cloud Run 4GB RAM | Fix: stream-insert in chunks of 10K rows (Harry — pending) |

---

## 10. Automation Roadmap

| Phase | What | When | Blocker |
|-------|------|------|---------|
| Now (manual) | Download → rotate → load → report | Weekly, Saturday | None |
| Phase 2 | Auto-download via middleware API | Once BQ loader fixed | Harry: chunked BQ insert |
| Phase 3 | Full pipeline: cron → download → delta → Supabase → report → Slack | Q2 | Phase 2 complete |

---

**⚠️ This SOP is DRAFT. Do not implement until Cem has reviewed and approved.**

*Draft by Ava | 2026-04-05*
