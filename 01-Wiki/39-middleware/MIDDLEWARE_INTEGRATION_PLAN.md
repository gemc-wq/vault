# Amazon Report Middleware — App Integration Plan
**Date:** 2026-04-05
**Status:** Planning

---

## The Model

```
Amazon SP-API + Ads API
        ↓
Amazon Report Middleware (Cloud Run, europe-west1)
https://amazon-report-middleware-175143437106.europe-west1.run.app
        ↓ loads data into ↓
BigQuery (amazon_reports dataset)
instant-contact-479316-i4
        ↓ read by ↓
┌─────────────────────────────────────────────┐
│  ecell.app (home dashboard)                 │
│  PULSE Dashboard                            │
│  Sales Dashboard V1                         │
│  FBA Planner (Streamlit)                    │
│  Royalty Report Converter                   │
│  Inventory Alert System (Harry)             │
│  Hermes (Amazon Ads analysis)               │
└─────────────────────────────────────────────┘
```

**One data source. All apps read from BQ. Middleware is the only writer.**

---

## BQ Tables (to be created by middleware, once BQ loader is fixed)

| Table name | Source report | Refresh | Used by |
|-----------|---------------|---------|---------|
| `active_listings_us` | GET_MERCHANT_LISTINGS_ALL_DATA | Weekly Sat | PULSE, Sales Dashboard, Inventory |
| `active_listings_uk` | GET_MERCHANT_LISTINGS_ALL_DATA | Weekly Sat | PULSE, Sales Dashboard |
| `active_listings_de` | GET_MERCHANT_LISTINGS_ALL_DATA | Weekly Sat | PULSE |
| `orders_us` | GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL | Daily 2 AM | Sales Dashboard, Royalty |
| `orders_uk` | GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL | Daily 2 AM | Sales Dashboard, Royalty |
| `fba_inventory_us` | GET_AFN_INVENTORY_DATA | Daily 3 AM | FBA Planner, Inventory Alerts |
| `fba_inventory_uk` | GET_AFN_INVENTORY_DATA | Daily 3 AM | FBA Planner |
| `sales_traffic_us` | GET_SALES_AND_TRAFFIC_REPORT | Weekly | PULSE CVR page |
| `sales_traffic_uk` | GET_SALES_AND_TRAFFIC_REPORT | Weekly | PULSE CVR page |
| `sp_campaigns_us` | spCampaigns | Daily | Hermes |
| `sp_search_terms_us` | spSearchTerm | Weekly | Hermes |
| `settlement_uk` | GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2 | Monthly | Royalty, Xero |

---

## App Integration Map

### 1. PULSE Dashboard
- **Currently:** reads from Supabase (orders) + local SQLite (listings)
- **After:** reads `active_listings_*` + `sales_traffic_*` from BQ `amazon_reports`
- **Impact:** no more manual Active Listings downloads, CVR data auto-refreshes

### 2. Sales Dashboard V1
- **Currently:** reads from BQ `zero_dataset.orders` (live ZERO sync)
- **After:** supplement with `orders_us` + `orders_uk` for faster/cleaner data
- **Note:** zero_dataset stays as source of truth for ops; amazon_reports = analytics layer

### 3. FBA Planner (Streamlit)
- **Currently:** unknown data source (Streamlit app)
- **After:** reads `fba_inventory_us` + `fba_inventory_uk` from BQ
- **Impact:** daily FBA inventory snapshots instead of manual pulls

### 4. Royalty Report Converter
- **Currently:** manual upload/convert tool
- **After:** auto-populates from `orders_*` + `settlement_*` tables
- **Impact:** eliminates manual royalty report assembly

### 5. ecell.app (home dashboard)
- **Currently:** tiles pointing to individual apps
- **After:** add "Data Freshness" tile showing last middleware run per marketplace
- **Impact:** instant visibility into data staleness

### 6. Inventory Alert System (Harry - Mon build)
- **Currently:** reads Supabase blank_inventory (PH MySQL sync)
- **After:** cross-references with `fba_inventory_us/uk` for FBA stock layer
- **Impact:** complete picture: FBM stock (Supabase) + FBA stock (BQ)

### 7. Hermes (Amazon Ads)
- **Currently:** manual analysis requests
- **After:** reads `sp_campaigns_us` + `sp_search_terms_us` daily
- **Impact:** fully automated ad performance monitoring

---

## Blockers Before Integration

### P0 — Fix BQ Loader (Harry, Monday)
The middleware BQ load step OOM-crashes on large files (5M+ row listings).
**Fix:** Stream-insert in chunks of 10K rows rather than loading full file.
**Code location:** Cloud Run service `amazon-report-middleware`, bigquery_loader module.

### P1 — Create BQ tables with correct schema
Once loader is fixed, run first full loads to establish table schemas.

### P2 — Update app data sources
Each app needs its BQ queries updated to point at `amazon_reports` dataset.

---

## API Keys for Apps

Keys are stored in `.env` on each machine. **Never commit to files, GDrive, or markdown.**

| Key name | Use |
|----------|-----|
| `AMAZON_MIDDLEWARE_KEY` (ecell) | General use (dashboards, Ava) |
| `AMAZON_MIDDLEWARE_KEY_CLAUDE` | AI agents (Hermes, Prism, Atlas) |
| `AMAZON_MIDDLEWARE_KEY_CRON` | Cron jobs (Pixel, automation) |

Base URL: `https://amazon-report-middleware-175143437106.europe-west1.run.app`
Auth header: `X-API-Key: $AMAZON_MIDDLEWARE_KEY` + `Authorization: Bearer $(gcloud auth print-identity-token)`

---

## Cron Schedule (once BQ loader fixed)

| Time | Job | Marketplace | Report |
|------|-----|-------------|--------|
| Sat 11 PM EST | Active Listings | US + UK + DE | GET_MERCHANT_LISTINGS_ALL_DATA |
| Daily 2 AM EST | Orders (24h) | US + UK | GET_FLAT_FILE_ALL_ORDERS_DATA... |
| Daily 3 AM EST | FBA Inventory | US + UK | GET_AFN_INVENTORY_DATA |
| Mon 5 AM EST | Sales & Traffic | US + UK | GET_SALES_AND_TRAFFIC_REPORT |
| Mon 5 AM EST | Ads Reports | US | spCampaigns + spSearchTerm |

All crons use `AMAZON_MIDDLEWARE_KEY_CRON` env var via Pixel agent (Gemini Flash, free).

---

*Written by Ava | 2026-04-05*
