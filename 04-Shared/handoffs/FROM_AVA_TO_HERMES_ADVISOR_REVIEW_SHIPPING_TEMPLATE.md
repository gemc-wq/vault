# Advisor Review: Shipping Template Dashboard
**Date:** 2026-04-14 | **Reviewed by:** Ava (Opus-level reasoning)
**For:** Cem review before passing to Hermes for plan

---

## Q1: Critical Path — CSV Now vs Wait for Live Data?

**Recommendation: YES, build Stage 1 dashboard off CSV now. Minimal rework.**

Reasoning:
- The dashboard schema (SKU, ASIN, product_type, device, design, sessions, units, conversion, sales, current_template) is identical whether the source is CSV or BQ live table. We're just swapping the data source later.
- Build the dashboard to read from a BQ curated table. Load the CSV into that table today. When live data flows, the loader just overwrites the same table.
- The UI, filters, and action buttons don't change at all between CSV and live source.
- **Only rework:** Adding a "data freshness" indicator and the automated refresh trigger. That's 30 minutes of work, not a rebuild.
- **Do NOT** skip the staging table even for CSV data. Load CSV → staging → curated is the right pattern regardless of source.

**Action:** Load the two Hermes CSVs into `amazon_reports.listings_staging_csv_apr14` immediately. This lets us demo Stage 1 to Cem within days.

---

## Q2: Data Validity — 24-48h Stale CSVs

**Risk: LOW for Reduced template changes. MEDIUM for any price changes.**

Why low for template changes:
- A listing being on wrong template yesterday is very likely still on wrong template today. Templates don't change themselves.
- The risk is: listing went out of stock or got suppressed since Apr 13. We'd waste an API call but cause no harm — Amazon will reject the PATCH and we log the error.
- Suppressed listings return an error on PATCH, they don't get damaged.

**Validation strategy before bulk PATCH:**
1. **Re-check status via SP-API** — Before each PATCH, call `GET /listings/2021-08-01/items/{sellerId}/{sku}` to confirm listing is still active and still on wrong template. Add 500ms overhead per SKU but eliminates stale data problem entirely.
2. **OR** — Pull fresh Active Listings report day-of, re-run filters, then execute. This is cleaner but takes 1-2 hours for report to generate.
3. **Recommended:** Do status check inline during PATCH execution. If `merchant-shipping-group` already shows correct template → skip and log "already fixed". If listing suppressed → skip and log.

**For price changes (+$11 SFP Prime path):** Higher risk. Price changes are immediately visible to customers and harder to roll back quickly. Require fresh data (< 6 hours) before any price PATCH.

---

## Q3: Architecture — Extend Middleware vs Standalone Script

**Recommendation: EXTEND the existing middleware for Stage 2 PATCH operations. Standalone Python for one-off validation.**

Extend middleware because:
- SP-API auth (LWA token refresh, AWS SigV4) is already wired in `report_engine.py` and `config.py`
- Secret Manager integration already works
- Cloud Run gives us retry, logging, scaling automatically
- New endpoints are simple: `POST /api/v1/listings/template-update` accepting a list of SKUs
- Consistent with how we handle all Amazon API operations

Standalone script only for:
- One-time data validation/CSV load to BQ (run locally, done)
- Emergency rollback (simpler to have a standalone script than route through Cloud Run)

**New middleware endpoints needed:**
```
POST /api/v1/listings/template-update   # PATCH merchant_shipping_group_name
POST /api/v1/listings/price-update      # PATCH price (for SFP path)
GET  /api/v1/listings/template-status   # Verify current template for a list of SKUs
```

---

## Q4: Minimum BQ Staging Table Schema

```sql
CREATE TABLE amazon_reports.listings_staging_us (
  -- Identity
  seller_sku STRING NOT NULL,
  asin STRING NOT NULL,
  
  -- Classification (parsed from SKU)
  product_type STRING,     -- HTPCR, HLBWH, H8939, etc.
  device STRING,           -- IPH17, IPAD102, etc.
  design STRING,           -- NARUICO-AKA, etc.
  base_sku STRING,         -- SKU without variant (for FBA twin detection)
  
  -- Listing state
  current_template STRING,  -- "Default Amazon Template" etc.
  price FLOAT64,
  quantity INTEGER,          -- MFN stock
  status STRING,             -- Active / Inactive / Suppressed
  fulfillment_channel STRING, -- MFN or AFN
  
  -- Business signals
  sessions INTEGER,
  units INTEGER,
  conversion FLOAT64,
  sales FLOAT64,
  
  -- Eligibility flags (computed during staging)
  fl_stock BOOL,
  is_fba_prefix BOOL,       -- SKU starts with F (with exceptions)
  is_expired_license BOOL,  -- NFL etc.
  is_eligible BOOL,         -- Final inclusion flag (all rules applied)
  
  -- Action fields
  target_template STRING,   -- "Reduced Shipping Template" or Prime
  price_adjustment FLOAT64, -- 0.0 for Reduced, 11.0 for Prime
  
  -- Execution tracking
  update_status STRING,     -- PENDING / SUCCESS / FAILED / SKIPPED
  update_attempted_at TIMESTAMP,
  update_error STRING,
  
  -- Metadata
  data_source STRING,       -- "csv_apr14" or "api_live"
  loaded_at TIMESTAMP,
  report_date DATE
)
PARTITION BY report_date
CLUSTER BY product_type, device;
```

---

## Q5: Risk — What Could Blow Up the Account

**Flagging three real risks, ranked by severity:**

### 🔴 Risk 1: Amazon rate limiting causing partial execution (HIGH probability)
- SP-API Listings PATCH: 5 req/sec sustained. At this rate, 9,778 SKUs = ~33 minutes.
- **Risk:** If the batch dies halfway through (Cloud Run timeout = 600s), you have a partial state: some SKUs updated, some not. Dashboard shows stale data.
- **Mitigation:** Log every result to BQ in real-time. Dashboard re-reads BQ to show true current state. Resume from last successful SKU on retry.

### 🟡 Risk 2: Amazon account flag for mass listing changes (MEDIUM probability)
- Amazon's systems watch for unusual listing activity. 9,778 changes in one night is unusual.
- **Risk:** Seller account gets flagged for review, listings temporarily suppressed while Amazon checks.
- **Mitigation:** Spread the batch. Don't do 9,778 in one night. Do:
  - Night 1: 500 SKUs (iPhone 17 + top 461 by revenue)
  - Night 2: 1,000 SKUs
  - Night 3: 2,000 SKUs
  - Night 4: remaining ~6,278
  - Monitor for suppression after each batch before continuing.

### 🟡 Risk 3: Template name mismatch causing silent failure (MEDIUM probability)
- The exact string "Reduced Shipping Template" must match your Seller Central template exactly (case-sensitive).
- If the actual template name is "Reduced Rate Shipping" or has a space variant, all 9,778 PATCHes will fail silently or with a confusing error.
- **Mitigation:** Test the API call on ONE SKU manually (HSTWH-L-WWE2JCEN-ICO) via Swagger first. Confirm the PATCH succeeds and listing shows new template in Seller Central within 15 minutes. Only then scale up.

### 🟢 Risk 4: Price change on wrong SKUs (LOW if controlled)
- SFP Prime path (+$11) must be a separate, explicitly confirmed action. Never bundle with Reduced template changes.
- Different confirmation modal, different audit log, different batch execution.

---

## Q6: Sequencing Recommendation

**Optimal sequence:**

```
Batch 0 (Manual test — 1 SKU):
  → HSTWH-L-WWE2JCEN-ICO (manual Seller Central change)
  → Monitor 72h for conversion lift
  → Confirms "Reduced Shipping Template" works before any API calls

Batch 1 (API test — 39 SKUs):
  → iPhone 17 family (highest unit value, 9.4% conversion baseline)
  → Run via API, monitor 48h
  → This validates the PATCH mechanism end-to-end

Batch 2 (500 SKUs):
  → Top 500 by revenue from the 9,778 (cross product types)
  → Spreads across product types for broader signal
  → Monitor 48h, check for account flags

Batch 3 (2,000 SKUs):
  → HLBWH phone cases (not iPad — phones are higher-value per unit)
  → Monitor 24h

Batch 4 (remaining ~7,239 HLBWH iPad cases):
  → iPad leather wallets — lowest unit revenue, lowest risk
  → Run as final overnight batch
```

**Why NOT iPad cases first despite their volume:**
- iPad leather wallets have lower revenue per SKU and lower sessions
- Phone cases have higher unit value — faster to see conversion signal
- If something goes wrong with iPad cases (wrong template name, suppression), the business impact is lower while you diagnose

---

## Summary: Recommended Next Steps for Hermes Plan

1. **Today:** Load CSVs into BQ staging table. Apply filters. Create curated table with 9,778 eligible SKUs.
2. **This week:** Build Stage 1 dashboard (read-only) off curated table. Show gap by product type, device, revenue.
3. **Blocker for Stage 2:** Cem to get "Product Listing" role added by Patrick in Seller Central.
4. **Before any bulk run:** Manual test on `HSTWH-L-WWE2JCEN-ICO` in Seller Central to confirm template name.
5. **Batch strategy:** 5 nights, escalating batch sizes, with 48h monitoring between batches.
6. **Never:** Run SFP Prime (+$11) changes in same batch as Reduced template changes.

**Estimated timeline:**
- Stage 1 Dashboard: 3-4 days
- Stage 2 Bulk Update (after permission fix): 1 day to build + 5 nights to execute safely
- Stage 3 Monitor cron: 1 day (add to existing cron infrastructure)

**Total: ~2 weeks from permission fix to all 9,778 SKUs updated.**
