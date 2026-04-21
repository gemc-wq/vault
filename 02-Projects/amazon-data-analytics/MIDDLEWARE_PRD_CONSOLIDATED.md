# Amazon Report Middleware — Consolidated PRD
**Version:** 1.0 | **Date:** 2026-04-14 | **Author:** Athena | **Status:** DRAFT
**Sources:** Handoff doc (Cem), PRD (Cem), Changes log (Claude Code), Athena audit

---

## 1. System Overview

Secure FastAPI gateway between Amazon SP-API/Ads API and Ecell's data infrastructure. Automates extraction of 28+ report types across 6 marketplaces into BigQuery.

| Component | Technology | Status |
|-----------|-----------|--------|
| API Gateway | FastAPI on Cloud Run (europe-west1) | ✅ Running (rev 00034) |
| Credential Store | Google Secret Manager (16 secrets) | ✅ Active |
| Scheduler | Cloud Scheduler (28 jobs) | ✅ Configured |
| Data Warehouse | BigQuery (`amazon_reports` dataset) | ⚠️ Partial |
| Report Streaming | GCS (`gs://ecell-bq-import/reports/`) | ✅ Working |
| Auth | OIDC + API Key (dual layer) | ✅ Working |

**Service URL:** `https://amazon-report-middleware-175143437106.europe-west1.run.app`
**GCP Project:** `instant-contact-479316-i4`
**Source Code:** `/Users/cem/Desktop/Repos/amazon-report-middleware/` (local only, no remote)

---

## 2. Codebase

| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | ~510 | FastAPI routes, models, auth, BQ endpoints |
| `report_engine.py` | ~350 | SP-API/Ads API: create, check, download, GCS streaming |
| `config.py` | ~156 | Settings, Secret Manager loader, marketplace config |
| `auth.py` | ~50 | API key verification middleware |
| `bigquery_loader.py` | ~120 | BQ table creation, GCS→BQ loading, query helpers |
| `Dockerfile` | ~20 | Python 3.12 slim, uvicorn |
| `deploy.sh` | ~30 | Deployment helper |

---

## 3. API Endpoints

| Method | Path | Rate | Purpose |
|--------|------|------|---------|
| GET | `/health` | None | Health check (no auth) |
| GET | `/api/v1/marketplaces` | 60/min | List marketplaces |
| GET | `/api/v1/report-types` | 60/min | Catalog of report types |
| POST | `/api/v1/reports/request` | 30/min | Submit report to Amazon |
| GET | `/api/v1/reports/{id}/status` | 120/min | Poll report status |
| GET | `/api/v1/reports/{id}/download` | 20/min | Download completed report |
| POST | `/api/v1/reports/request-and-wait` | 10/min | All-in-one: submit + poll + BQ load |
| POST | `/api/v1/listings/sync` | — | Step 1: Submit listings report |
| POST | `/api/v1/listings/sync/complete` | — | Step 2: GCS stream + BQ load |
| POST | `/api/v1/listings/lookup` | 60/min | Batch ASIN→SKU from BQ (max 500) |
| GET | `/api/v1/data/tables` | 60/min | List BQ tables |
| POST | `/api/v1/data/query` | 30/min | Query BQ data |
| GET | `/api/v1/data/tables/{name}/latest` | 60/min | Latest rows from table |
| POST | `/api/v1/data/load` | 10/min | Manual download + BQ load |

---

## 4. Marketplaces

| Code | Marketplace ID | Region | Endpoint |
|------|---------------|--------|----------|
| US | ATVPDKIKX0DER | NA | sellingpartnerapi-na.amazon.com |
| UK | A1F83G8C2ARO7P | EU | sellingpartnerapi-eu.amazon.com |
| DE | A1PA6795UKMFR9 | EU | sellingpartnerapi-eu.amazon.com |
| FR | A13V1IB3VIYZZH | EU | sellingpartnerapi-eu.amazon.com |
| IT | APJ6JRA9NG5V4 | EU | sellingpartnerapi-eu.amazon.com |
| ES | A1RKKUPIHCS9HS | EU | sellingpartnerapi-eu.amazon.com |

---

## 5. Report Types & Cron Schedule

### 28 Configured Jobs (Monday 06:00 UTC)

| Group | Count | Report Type | Marketplaces | SP-API Role Needed |
|-------|-------|-------------|-------------|-------------------|
| Sales & Traffic 14d | 6 | `GET_SALES_AND_TRAFFIC_REPORT` | All 6 | **Analytics** ❌ |
| Sales & Traffic 30d | 6 | `GET_SALES_AND_TRAFFIC_REPORT` | All 6 | **Analytics** ❌ |
| Active Listings | 6 | `GET_MERCHANT_LISTINGS_ALL_DATA` | All 6 | Listings ✅ |
| FBA Reports (US) | 4 | Inventory, Fees, Reimbursements, Restock | US | **Inventory** ❌ |
| Settlements | 6 | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` | All 6 | **Finance** ❌ |

### Cron Status After custom=true Update (2026-04-14)

| Job | `report_options` | Status |
|-----|-----------------|--------|
| Active Listings (all 6) | `{"custom": "true"}` | ✅ Updated — shipping template column included |
| All others | No options / Brand Analytics options | Unchanged |

### Missing Reports (Not Yet Scheduled)

| Report Type | Purpose | Priority |
|-------------|---------|----------|
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL` | Daily order tracking | P1 |
| Customer Service Metrics | CS performance | P2 |

---

## 6. Authentication & Credentials

### Dual Auth Pattern

| Layer | Header | Source |
|-------|--------|--------|
| GCP Identity Token | `Authorization: Bearer <token>` | `gcloud auth print-identity-token` |
| API Key | `X-API-Key` | Secret Manager (`API_KEYS`) |

### API Keys

| Key | Name | Use Case |
|-----|------|----------|
| `sk_live_ecell_2026` | ecell | Swagger UI, manual, dashboards |
| `sk_live_claude_2026` | claude | AI agent integration |
| `sk_live_cron_2026` | cron | Cloud Scheduler |

### SP-API Credentials (Secret Manager)

| Secret | Status |
|--------|--------|
| US SP-API (LWA + AWS) | ✅ 5 secrets active |
| EU SP-API (LWA + AWS) | ✅ 5 secrets active |
| Ads API (6 secrets) | ❌ ALL EMPTY |

### SP-API Permission Gap (P0 BLOCKER)

Current developer app ("Reporting for UK, US, DE") only has **Listings** role.

| Role | Status | Unblocks |
|------|--------|----------|
| Listings | ✅ Active | Active Listings reports |
| Analytics | ❌ Missing | Sales & Traffic (12 cron jobs) |
| Inventory | ❌ Missing | FBA reports (4 cron jobs) |
| Finance | ❌ Missing | Settlement reports (6 cron jobs) |

**Fix:** Seller Central → Developer Apps → Add roles. Requires seller account owner (PH staff — Patrick). Requested 2026-04-14.

---

## 7. Data Pipeline

### Current Flow

```
Amazon SP-API
  → Middleware (Cloud Run)
    → GCS streaming (8MB chunks, gzip)
      → BigQuery (auto-schema, WRITE_TRUNCATE)
```

### BigQuery Tables (as of 2026-04-14)

| Table | Rows | Size | Last Updated |
|-------|------|------|-------------|
| `merchant_listings_all_data_us` | 4,087,163 | 7.56 GB | Apr 13 |
| `listings` | 0 | 0 | Empty |
| `listings_staging` | 0 | 0 | Empty |

### GCS Bucket

- `gs://ecell-bq-import/reports/merchant_listings_all_data/`
- Used for large report streaming (>512MB)
- BigQuery loads directly from GCS with native gzip decompression

---

## 8. Consumers

| Consumer | Access Method | What They Use |
|----------|-------------|---------------|
| FBA Management App | Direct BigQuery + Middleware HTTP | Listings, ASIN→SKU lookup |
| Hermes (analytics) | Via OpenClaw → Middleware API | Weekly reports, PULSE |
| Cloud Scheduler | HTTP + OIDC + API key | Automated Monday pulls |
| Manual (Swagger UI) | Browser + identity token | Ad-hoc testing |

---

## 9. Deployment

```bash
cd /Users/cem/Desktop/Repos/amazon-report-middleware
./deploy.sh
# or manually:
gcloud run deploy amazon-report-middleware \
  --project=instant-contact-479316-i4 \
  --region=europe-west1 --source=. \
  --no-allow-unauthenticated \
  --memory=512Mi --timeout=600 \
  --min-instances=0 --max-instances=3 --quiet
```

**No CI/CD.** No GitHub remote. Deploy from Cem's laptop only.

---

## 10. Ownership

| Domain | Owner | Rule |
|--------|-------|------|
| Middleware code + deployment | Athena (pending repo transfer) | Single writer, no multi-agent edits |
| Report strategy & priorities | Ava | Requests changes via handoff template |
| Data analysis & dashboards | Hermes | Consumes data, doesn't modify pipeline |
| BigQuery schema & tables | Athena | Owns tables, loaders, GCS bucket |
| SP-API credentials | Cem | Stays on Cem's laptop, Secret Manager only |

---

## 11. Known Issues

| Issue | Severity | Status | Fix |
|-------|----------|--------|-----|
| SP-API roles missing (Analytics, Inventory, Finance) | P0 | ⏳ Waiting on PH (Patrick) | Seller Central role addition |
| Middleware source not on Mac Studio | P1 | ⏳ Needs `scp` from Cem | LAN transfer |
| Ads API secrets empty | P2 | Not started | Populate from Amazon Ads console |
| No GitHub remote / CI/CD | P2 | Not started | Create private repo after credential audit |
| UK/DE listings tables missing | P2 | Not started | Run sync for UK/DE marketplaces |
| Orders report not scheduled | P2 | Not started | Add cron job after permissions fixed |

---

## 12. Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-04-14 | Initial consolidated PRD from 3 source docs | Athena |
| 2026-04-14 | Updated 6 Active Listings crons with `custom=true` | Athena |
