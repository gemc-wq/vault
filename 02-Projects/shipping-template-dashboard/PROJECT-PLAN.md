# PROJECT-PLAN: Shipping Template Gap Analysis & Bulk Fix Engine
**Date:** 2026-04-14 | **Owner:** Ava | **Advisor Review:** Opus-level (Ava direct)
**Status:** READY FOR CEM REVIEW before any execution

---

## Critical Context: What We Know Is Wrong Right Now

Before the plan, an honest inventory of the problems:

| Problem | Impact | Root Cause |
|---------|--------|------------|
| Hermes used Business Report, not Active Listings | 9,778 vs 2,198,998 SKUs — completely different scope | Wrong data source |
| Hermes mixed template gap + SFP analysis | Incorrect methodology — two separate datasets needed | Conceptual error |
| Existing BQ table is stale (4.08M rows vs 3.6M today) | Cannot trust any existing BQ data | Old load, no custom=true |
| 937 Nationwide Prime listings in US file | Unknown — contamination or misconfiguration | Not yet investigated |
| SP-API Product Listing role not granted | Blocks all PATCH execution | Cem action required |

**Nothing moves to execution until Phase 0 passes.**

---

## PHASE 0: Data Validation
**Owner:** Codex (Python) | **Timeline:** Same day | **Blocker for:** Everything else

### Task 0.1 — Confirm File Is US-Only
**Why:** 937 Nationwide Prime listings (UK template) in a supposed US file is a red flag. Either the file contains mixed marketplace data, or 937 US listings are misconfigured with a UK template.

**Method:**
```python
# For each Nationwide Prime listing, check:
# 1. Does the ASIN start with B0 (US format)?
# 2. Is the seller-sku pattern consistent with US SKUs?
# 3. Sample 10 ASINs and look them up on amazon.com vs amazon.co.uk

# Pass criteria: >99.9% of rows have US-format ASINs
# Fail criteria: Non-US ASINs found → file is contaminated, start over with clean download
```

**Action if PASS:** File is US-only, 937 Nationwide Prime are misconfigured US listings → fix them too (change to Reduced template)
**Action if FAIL:** Do not proceed. Cem must re-download US Active Listings from US Seller Central account only (ecell accessorize), ensuring single-marketplace selection.

### Task 0.2 — Investigate the 937 Nationwide Prime SKUs
```python
# Extract all SKUs where merchant-shipping-group = 'Nationwide Prime'
# Output: seller_sku, asin1, fulfillment_channel, price, quantity
# Questions to answer:
# - Are they FBM or FBA?
# - What product types are they? (HLBWH? HTPCR?)
# - Are their ASINs US ASINs?
# Decision: if US FBM with wrong UK template → add to wrong-template fix list
# Decision: if non-US → exclude and flag for separate investigation
```

### Task 0.3 — Duplicate SKU Check
```python
# Count: len(df) vs df['seller-sku'].nunique()
# If duplicates exist: are they same ASIN different marketplace? Same SKU listed twice?
# Rule: deduplicate by keeping row with most recent open-date
```

### Task 0.4 — Row Count Sanity Check
- File has 3,605,361 rows. Previous BQ table had 4,087,163.
- Delta of ~480K rows needs explanation before proceeding.
- Acceptable explanations: listings deleted/suppressed since last load, marketplace scope difference
- If unexplained: investigate before loading to BQ

### Phase 0 Pass Criteria (ALL must be true before Phase 1):
- [ ] File confirmed US-only (or Cem confirms single-marketplace download)
- [ ] 937 Nationwide Prime SKUs classified (US misconfigured vs foreign)
- [ ] No unexplained duplicate SKUs at scale (>0.1%)
- [ ] Row count delta explained

**Estimated time:** 30-60 minutes of Codex work

---

## PHASE 1: Clean BigQuery Foundation
**Owner:** Codex (Python) + Ava oversight | **Timeline:** After Phase 0 passes

### Task 1.1 — Drop the Stale BQ Table
```sql
-- The existing table is wrong. Drop it.
DROP TABLE IF EXISTS amazon_reports.merchant_listings_all_data_us;
-- Do NOT try to merge or append — start clean
```

### Task 1.2 — Create Staging Table (Raw Data)
```sql
CREATE TABLE amazon_reports.listings_raw_us_20260414 (
  -- Core identity
  seller_sku STRING NOT NULL,
  asin1 STRING,
  listing_id STRING,
  
  -- Pricing & inventory
  price FLOAT64,
  quantity INTEGER,
  open_date TIMESTAMP,
  
  -- Fulfillment
  fulfillment_channel STRING,  -- DEFAULT (MFN) or AMAZON_NA (FBA)
  
  -- THE KEY COLUMN
  merchant_shipping_group STRING,  -- "Default Amazon Template", "Reduced Shipping Template", "Nationwide Prime"
  
  -- Provenance (MANDATORY — never load without these)
  _source_file STRING,          -- filename of the source file
  _source_marketplace STRING,   -- 'US' (explicit, set at load time)
  _report_date DATE,            -- date the file was downloaded
  _loaded_at TIMESTAMP,         -- when we loaded to BQ
  _row_number INTEGER           -- original row number in source file for debugging
)
PARTITION BY _report_date
CLUSTER BY merchant_shipping_group, fulfillment_channel;
```

### Task 1.3 — Create Curated Table (Filtered, Classified)
```sql
CREATE TABLE amazon_reports.listings_flagged_us (
  -- All staging columns plus:
  product_type STRING,          -- parsed from SKU (HTPCR, HLBWH, etc.)
  device STRING,                -- parsed from SKU (IPH17, IPAD102, etc.)
  design STRING,                -- parsed from SKU
  base_sku STRING,              -- product_type + device (for FL stock matching)
  
  -- Classification flags
  is_fba BOOL,                  -- true if AFN or F-prefix (with exceptions)
  is_fba_exception BOOL,        -- true if FLAG, F1309, FRND, FKFLOR
  is_expired_license BOOL,      -- true if NFL design code
  fl_stock BOOL,                -- from Supabase cross-reference
  fl_stock_qty INTEGER,         -- quantity in FL warehouse
  
  -- Template classification
  template_status STRING,       -- 'wrong' | 'correct' | 'uk_template' | 'unknown'
  target_template STRING,       -- what it should be changed to
  price_adjustment FLOAT64,     -- 0.0 for Reduced, 11.0 for SFP Prime
  
  -- Eligibility
  is_eligible_for_fix BOOL,     -- final flag: passes ALL filter rules
  eligibility_reason STRING,    -- why eligible or why excluded
  
  -- Execution tracking
  update_status STRING,         -- NULL | 'pending' | 'success' | 'failed' | 'skipped'
  update_attempted_at TIMESTAMP,
  update_result STRING,
  pre_update_snapshot STRING    -- JSON of original values for rollback
)
PARTITION BY _report_date
CLUSTER BY is_eligible_for_fix, product_type, device;
```

### Task 1.4 — Load Pipeline
```
Source File (6.7GB)
  → Codex Python script (streaming, 500K rows/checkpoint)
  → listings_raw_us_20260414 (WRITE_TRUNCATE)
  → Apply classification logic
  → listings_flagged_us (WRITE_TRUNCATE)
  → Validation query (row counts, template distribution)
  → STOP if validation fails
```

**Validation query after load:**
```sql
SELECT 
  merchant_shipping_group,
  fulfillment_channel,
  COUNT(*) as count,
  COUNT(DISTINCT seller_sku) as unique_skus
FROM amazon_reports.listings_raw_us_20260414
GROUP BY 1, 2
ORDER BY 3 DESC;
-- Expected: matches Codex analysis output from today
```

---

## PHASE 2: Two Separate Analysis Tracks

### ⚠️ What Hermes Got Wrong

Hermes conflated two completely different analyses:

| Analysis | Correct Data Source | Hermes Used | Result |
|----------|--------------------|-----------|----|
| Template Gap (which listings are on wrong template) | Active Listings report | Business Report | 9,778 vs 2.2M — 99.6% of the problem missed |
| SFP Prime Candidates (who already pays for speed) | Orders data (ship-service-level) | Business Report (session data) | Wrong signal — sessions ≠ willingness to pay for shipping |

These are permanently separate pipelines. Never mix them.

---

### Track A: Template Gap Analysis (Active Listings Source)

**Question:** Which FBM listings are on the wrong template?
**Data source:** `listings_flagged_us` (built in Phase 1)
**Filters:**
1. `fulfillment_channel = 'DEFAULT'` (FBM only)
2. `is_fba = FALSE`
3. `merchant_shipping_group = 'Default Amazon Template'`
4. `is_expired_license = FALSE` (exclude NFL)
5. `fl_stock = TRUE` (for Reduced template eligibility)

**Output:** List of eligible SKUs sorted by price DESC (highest revenue impact first)

**Note on scope:** 
- With FL stock filter: ~9,778 SKUs (Hermes's number — actionable immediately)
- Without FL stock filter: ~2,198,998 SKUs (full universe — fix over time as stock moves)
- **Start with FL-stocked items only.** Other warehouses have different 2-day capabilities.

---

### Track B: SFP Prime Candidate Analysis (Orders Source)

**Question:** Which products do customers already pay extra to get fast?
**Data source:** `~/Downloads/AmazonUSLast90day_Sales_Combined.txt`
**Key field:** `ship-service-level` = "SecondDay" | "NextDay" | "Priority"
**Method:**
```python
# Load orders file
# Filter: ship-service-level IN ('SecondDay', 'NextDay', 'Priority')
# Group by: base_sku (product_type + device)
# Count: number of orders where customer paid for fast shipping
# Cross-reference with: Track A eligible list
# Result: SKUs where customer already wants speed but doesn't see Prime badge
# These are your highest-ROI SFP Prime candidates
```

**Output:** Ranked list of base SKUs by "willingness to pay for speed" score
**Price change rule:** +$11 only for SFP Prime path, after confirmed SFP enrollment

**Never mix Track A and Track B outputs.**

---

## PHASE 3: Dashboard Design
**Owner:** Athena → Forge | **Depends on:** Phase 1 complete, Phase 2 analysis done

### Views Required

**View 1: Executive Gap Summary**
- Cards: Total FBM | Wrong template | Correct template | Wrong % | Revenue at risk est.
- Bar chart: Wrong template count by product type
- Bar chart: Wrong template count by device family (top 20)

**View 2: Eligible Fix List (FL-stocked)**
- Table: SKU | ASIN | Product Type | Device | Design | Price | Current Template | FL Stock Qty
- Sortable by: price, revenue (if session data available), product type
- Filter by: product type, device family, price range

**View 3: SFP Prime Candidates** (separate tab, separate data source)
- Based on orders analysis only
- Shows: base_sku | fast_shipping_orders | total_orders | speed_preference_pct | current_price | proposed_price

**View 4: Nationwide Prime Anomalies**
- The 937 SKUs on UK template
- Shows: SKU | ASIN | Classification (US misconfigured vs foreign) | Recommended action

### Action Buttons

**Button 1: "Convert to Reduced Shipping" (FL-stocked items)**
- Pre-condition: SP-API Product Listing role granted
- Confirmation modal: "You are about to change [N] listings to Reduced Shipping Template. No price changes. This cannot be automatically reversed. Type CONFIRM to proceed."
- Execution: SP-API PATCH in batches (see Phase 4)
- Log: every result to BQ `template_updates` table

**Button 2: "Convert to SFP Prime + Price Adjust"**
- Pre-condition: SFP enrollment confirmed, Product Listing role granted
- Separate confirmation: "You are changing [N] listings to Prime template AND increasing price by $11. Confirm?"
- NEVER run in same batch as Button 1

**Button 3: "Export CSV"** — always available, no confirmation needed

**Button 4: "Preview Changes"** — show exactly what will change before any PATCH

**Button 5: "Rollback"** — re-apply `pre_update_snapshot` values (30-day window)

---

## PHASE 4: Safe Bulk Execution
**Blocker:** SP-API Product Listing role (Cem + Patrick — Seller Central action)
**Owner:** Ava coordinates, Codex executes

### Pre-Execution Checklist (ALL required)
- [ ] Phase 0 passed (data validated)
- [ ] Phase 1 complete (BQ clean, curated table ready)
- [ ] Manual test confirmed: `HSTWH-L-WWE2JCEN-ICO` changed in Seller Central, "Reduced Shipping Template" is exact string, conversion observed
- [ ] SP-API Product Listing role granted
- [ ] Rollback snapshot captured in BQ before first PATCH

### Batch Strategy (5-night rollout)

| Night | Batch | SKUs | Selection Logic |
|-------|-------|------|----------------|
| 1 (test) | 39 | iPhone 17 family — highest value, tight group |
| 2 | 500 | Top 500 by price across all product types |
| 3 | 1,500 | Next 1,500 by price |
| 4 | 3,000 | Next 3,000 |
| 5 | ~4,739 | Remainder of FL-stocked eligible |

**Between each batch:** 48-hour monitoring window. Check:
- Were any listings suppressed?
- Did conversion rate change on updated SKUs?
- Any Amazon account alerts?
- Only proceed to next batch if no issues

### Rate Limiting
- SP-API Listings PATCH: 5 req/sec sustained, 10 burst
- Implementation: `time.sleep(0.2)` between calls
- 9,778 SKUs at 5/sec = ~33 minutes per batch
- Run at 11PM ET (off-peak)
- Cloud Run timeout = 600s → use resume-from-checkpoint pattern

### Failure Handling
```python
for sku in batch:
    # Re-verify current template before patching (prevent stale data issues)
    current = get_listing_status(sku)
    if current.template == target_template:
        log(sku, 'SKIPPED', 'already_correct')
        continue
    if current.status != 'Active':
        log(sku, 'SKIPPED', 'not_active')
        continue
    
    result = patch_template(sku, target_template)
    log(sku, result.status, result.error)
    
    if result.status == 'rate_limited':
        sleep(60)  # back off 1 minute
        retry once
    
    if result.status == 'error':
        log and continue — never abort entire batch
```

### Logging Schema
```sql
CREATE TABLE amazon_reports.template_updates (
  seller_sku STRING,
  asin STRING,
  old_template STRING,
  new_template STRING,
  old_price FLOAT64,
  new_price FLOAT64,
  batch_number INTEGER,
  status STRING,  -- success | failed | skipped
  error_code STRING,
  attempted_at TIMESTAMP,
  api_request_id STRING
);
```

---

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Amazon flags account for mass changes | HIGH | Graduated batches over 5 nights, not 9,778 at once |
| "Reduced Shipping Template" exact string mismatch | HIGH | Manual test first — do NOT skip |
| Nationwide Prime applied to US listing | CRITICAL | Phase 0 must classify all 937 before any execution |
| SFP enrollment required before SFP PATCH | HIGH | Confirm SFP program enrollment separately |
| Stale data — listing suppressed between analysis and PATCH | MEDIUM | Re-verify status inline before each PATCH |
| BQ contamination from old stale data | HIGH | Phase 1 DROP TABLE + rebuild from scratch |
| Partial batch failure leaves inconsistent state | MEDIUM | Resume-from-checkpoint, log every result |
| Price increase (+$11) applied to wrong listings | CRITICAL | SFP actions on completely separate button/batch/log |

---

## Open Actions Required from Cem

| Action | Owner | Urgency |
|--------|-------|---------|
| Confirm Active Listings file was US-only download | Cem | NOW — gates Phase 0 |
| Add Product Listing role to SP-API app (Patrick) | Cem | Before Phase 4 |
| Confirm SFP program enrollment status | Cem | Before Track B |
| Manual test: change HSTWH-L-WWE2JCEN-ICO in Seller Central | Cem | Before Phase 4 |

---

## What Is NOT In This Plan (Explicitly Out of Scope)

- UK/EU template management (separate project, separate file, separate rules)
- Auto-fix without human approval (always manual confirmation)
- Conversion attribution tracking (needs Brand Analytics — blocked on SP-API permissions)
- FBA listing template changes (Amazon manages these, not us)
- Price optimization beyond the SFP +$11 rule

---

*Plan authored by Ava | Advisor-level review applied | 2026-04-14*
*Ready for Cem sign-off before any Phase 1 work begins*
