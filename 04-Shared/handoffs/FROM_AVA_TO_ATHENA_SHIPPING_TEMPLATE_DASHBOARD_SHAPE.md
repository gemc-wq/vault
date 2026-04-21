# Project Shape: Shipping Template Gap Dashboard + Bulk Fix Engine
**Date:** 2026-04-14 | **Owner:** Ava | **Status:** SHAPING COMPLETE — ready for planning
**Requestor:** Cem | **Builder:** Athena → Forge/Codex

---

## Problem Statement

9,778 FBM listings are on "Default Amazon Template" instead of our Reduced Shipping template. These listings are **selling** — $39,429/month in revenue — but without the Prime/Reduced badge, they're converting at a fraction of what they should. We know shipping template is the single highest-impact conversion driver we can control.

Hermes identified this with two CSVs of FL-stocked, wrong-template SKUs. The data is real. The fix is mechanical. We just need the tooling.

---

## Scope

### IN SCOPE:
- **Stage 1: Gap Dashboard** — visual view of which SKUs are on wrong template, segmented by product type, device, design
- **Stage 2: Bulk Update Engine** — select SKUs from dashboard, push template change via SP-API Listings PATCH
- **Stage 3: Weekly Delta Monitor** — cron that flags newly-listed SKUs that defaulted to wrong template

### OUT OF SCOPE (Phase 2):
- UK/EU template management (US only for now)
- Auto-fix without human approval (always manual confirm before bulk push)
- Conversion attribution tracking (needs Brand Analytics — blocked on SP-API permissions)

---

## Data Sources

### Already Available (Hermes CSVs)
| File | SKUs | Sales/mo | Key finding |
|------|------|----------|-------------|
| `fbm_wrong_template_fl_stock.csv` | 9,778 | $39,429 | HLBWH dominates (86%) |
| `iphone17_wrong_template_fl_stock.csv` | 39 | $1,471 | iPhone 17 converting at 9.4% FBM — likely 12-15% with Prime |

### Future (when SP-API Active Listings flows with custom=true)
- `merchant-shipping-group` column from `GET_MERCHANT_LISTINGS_ALL_DATA`
- BigQuery table: `amazon_reports.merchant_listings_all_data_us`
- This becomes the live data source once the `custom=true` cron fix is deployed

---

## Revenue Opportunity

| Segment | Sessions/mo | Current Sales | Est. uplift (+1.5pp conv) |
|---------|------------|---------------|--------------------------|
| All FBM wrong template | ~180,000 est | $39,429 | ~$8,850/mo |
| iPhone 17 family | 1,248 | $1,471 | ~$441/mo |
| HLBWH (leather wallets) | ~90,000 est | $28,123 | ~$6,300/mo |

**Conservative estimate: $8-10K/mo additional revenue from fixing templates.**
Based on Hermes's prior analysis: Reduced shipping converts at 4.12% vs Standard at 3.11% — a full percentage point gap.

---

## Architecture

```
Data Layer:
  Hermes CSVs (current) → uploaded to BQ staging table
  OR
  Active Listings BQ table (future, when custom=true cron fixed)
       ↓
Dashboard (FastAPI + simple HTML/JS OR embed in existing ecell.app)
       ↓
  Gap View: SKUs by product type × device × template status
  Priority ranking: by sessions × conversion delta × revenue
  Bulk select → confirm → execute
       ↓
SP-API Listings PATCH
  PATCH /listings/2021-08-01/items/{sellerId}/{sku}
  Body: { "patches": [{ "op": "replace", "path": "/attributes/merchant_shipping_group_name", "value": [{"value": "Reduced Shipping Template"}] }] }
  Rate limit: 5 requests/sec
  Batch: up to 1 SKU per PATCH call (not bulk — must loop with rate limiting)
       ↓
Execution log → BQ table `template_updates` (sku, old_template, new_template, status, timestamp)
```

---

## Key Edge Cases

1. **Out-of-stock SKUs** — Do NOT update template if FL stock = 0. Already filtered in Hermes's output (fl_stock flag in filename).
2. **NFL expired SKUs** — NFL license expired Mar 31. Flag for exclusion or separate treatment.
3. **Rate limiting** — SP-API Listings API: 5 req/sec, burst 10. 9,778 SKUs = ~33 minutes at max rate. Run overnight.
4. **Partial failures** — API may reject individual SKUs (wrong ASIN, suppressed, etc.). Log all failures, retry once, report remainder.
5. **Template name exact match** — Must use exact template name as it appears in Seller Central. Hermes confirmed "Default Amazon Template" is the wrong one. Need to confirm exact target template name ("Reduced Shipping Template" or region-specific variant).
6. **UK vs US** — This data is US only. UK has different template names. Scope US first.
7. **SP-API permissions** — Listings PATCH requires "Product Listing" role (separate from Reports role). Cem needs to add this in Seller Central. **BLOCKER until resolved.**

---

## Success Metrics

1. **Coverage:** 9,778 SKUs updated to correct template within 48 hours of execution
2. **Zero wrong updates:** No SKU updated that shouldn't be (out-of-stock, expired license, already correct)
3. **Conversion lift visible:** Within 2 weeks of fix, Amazon Business Reports show improved conversion on affected ASINs
4. **Monitoring:** Weekly cron flags any new wrong-template SKUs within 7 days of listing

---

## Dependencies / Blockers

| Blocker | Owner | Impact |
|---------|-------|--------|
| SP-API "Product Listing" role needed | Cem + Patrick | Blocks Stage 2 (bulk update) |
| Active Listings with `custom=true` | Athena (cron update) | Enables live data source vs CSV |
| Exact target template name | Cem to confirm | Need "Reduced Shipping Template" exact string |
| BQ `template_updates` table creation | Athena/Hermes | For execution logging |

---

## Build Plan (2 weeks)

### Week 1 — Stage 1: Dashboard
- Load Hermes CSVs into BQ staging table
- Build simple dashboard: gap by product type, device, revenue impact
- Show top 50 highest-value SKUs to fix first
- No SP-API calls yet — read-only

### Week 2 — Stage 2: Bulk Update
- Wire SP-API Listings PATCH
- Add selection UI + confirmation modal
- Rate-limited batch executor (overnight run)
- Execution log

### Week 3 — Stage 3: Monitor (optional)
- Weekly cron: pull Active Listings, flag new wrong-template SKUs
- Alert to Slack #ai_workflow if >100 new gaps found

---

## Template

**Hermes has the data. Athena builds. Cem approves before any bulk push.**

For Athena:
- Source CSVs: `Vault/03-Agents/Hermes/` or inbound media path
- SP-API credentials: Secret Manager (`US_LWA_APP_ID`, `US_REFRESH_TOKEN`, etc.)
- Middleware can be extended OR build standalone script
- Prioritise iPhone 17 family first (39 SKUs, 9.4% conversion, high-value)

---

## SHAPING SIGN-OFF
- [x] Cem reviewed (verbal — Apr 14)
- [x] Data confirmed (Hermes CSVs analyzed)
- [ ] Ready to move to planning (pending: Cem confirm template name + SP-API Listings role)

**One thing Cem needs to confirm:** What is the exact name of the target shipping template in Seller Central? ("Reduced Shipping Template"? "Reduced Rate Shipping"? exact string matters for the API call.)
