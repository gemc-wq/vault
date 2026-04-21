# Product Requirements Document
## Amazon Report Middleware
**Automated SP-API & Ads Reporting Pipeline**

| Field | Value |
|-------|-------|
| Document Version | 1.0 |
| Date | April 14, 2026 |
| Author | Cem (gemc@ecellglobal.com) |
| Status | Production |
| GCP Project | `instant-contact-479316-i4` |
| Service URL | `amazon-report-middleware-175143437106.europe-west1.run.app` |

---

## 1. Executive Summary

The Amazon Report Middleware is a cloud-hosted FastAPI service that acts as a secure gateway between Amazon's Selling Partner API (SP-API), Amazon Ads API, and Head Case Designs' internal data infrastructure. It automates the extraction, transformation, and loading of 28+ report types across 6 marketplaces (UK, DE, FR, IT, ES, US) into Google BigQuery for analytics and business intelligence.

The system runs on Google Cloud Run with Secret Manager for credentials, Cloud Scheduler for automated weekly execution, and BigQuery for data warehousing. It supports three consumption patterns: cron-driven automation, AI agent integration, and manual API access via Swagger UI.

---

## 2. Problem Statement

Head Case Designs operates across 6 Amazon marketplaces, selling phone cases, tablet cases, gaming skins, and licensed merchandise. Prior to this system:

- Sales and traffic reports were downloaded manually from Seller Central, one marketplace at a time
- No centralized data warehouse existed for cross-marketplace analytics
- Brand Analytics reports required manual configuration with specific `reportOptions`
- FBA inventory, fee, and reimbursement data was siloed in per-marketplace dashboards
- No automated alerting or monitoring of customer service metrics

---

## 3. Goals & Success Metrics

### 3.1 Primary Goals

1. Automate weekly extraction of all critical Amazon reports across 6 marketplaces
2. Centralize data in BigQuery for cross-marketplace querying and dashboards
3. Provide a secure, rate-limited API for AI agents and internal tools
4. Enable Brand Analytics with proper `reportOptions` (CHILD ASIN, daily granularity)

### 3.2 Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Weekly reports auto-collected | 28 per cycle | 28 jobs configured |
| Marketplaces covered | 6 (UK, DE, FR, IT, ES, US) | 6 |
| Report types supported | 21 SP-API + 27 Ads API | 21 SP-API active |
| API uptime | >99.5% | Cloud Run managed |
| Data freshness | <24h from report availability | Weekly Monday 6AM UTC |

---

## 4. Architecture

### 4.1 System Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Gateway | FastAPI on Cloud Run | Secure REST API with auth, rate limiting, CORS |
| Credential Store | Google Secret Manager | SP-API & Ads API keys, LWA tokens, AWS creds |
| Scheduler | Cloud Scheduler (28 jobs) | Weekly cron triggers every Monday 6 AM UTC |
| Data Warehouse | BigQuery (EU region) | Dataset: `amazon_reports`, auto-schema tables |
| Auth Layer | API Key + OIDC | Dual auth: API key for app, OIDC for Cloud Run IAM |

### 4.2 Request Flow

**Cron Path:**
```
Cloud Scheduler (OIDC token)
  -> Cloud Run IAM gate
    -> FastAPI (API key check)
      -> SP-API / Ads API
        -> BigQuery load
          -> HTTP 200 with file + BQ metadata
```

**Manual/Agent Path:**
```
User or AI Agent (API key + Identity token)
  -> Cloud Run IAM
    -> FastAPI
      -> SP-API
        -> BigQuery
          -> Streaming response
```

### 4.3 Marketplace Configuration

| Code | Marketplace ID | Region | Endpoint |
|------|---------------|--------|----------|
| UK | A1F83G8C2ARO7P | EU | sellingpartnerapi-eu.amazon.com |
| DE | A1PA6795UKMFR9 | EU | sellingpartnerapi-eu.amazon.com |
| FR | A13V1IB3VIYZZH | EU | sellingpartnerapi-eu.amazon.com |
| IT | APJ6JRA9NG5V4 | EU | sellingpartnerapi-eu.amazon.com |
| ES | A1RKKUPIHCS9HS | EU | sellingpartnerapi-eu.amazon.com |
| US | ATVPDKIKX0DER | NA | sellingpartnerapi-na.amazon.com |

---

## 5. API Specification

### 5.1 Authentication

All endpoints (except `/health`) require dual authentication:

- **X-API-Key header:** One of three issued keys (live, claude, cron)
- **OIDC Identity Token:** Required by Cloud Run IAM gate (GCP org policy blocks `allUsers`)

### 5.2 Endpoints

| Method | Path | Rate Limit | Description |
|--------|------|-----------|-------------|
| GET | `/health` | None | Health check (no auth) |
| GET | `/api/v1/marketplaces` | 60/min | List available marketplaces |
| GET | `/api/v1/report-types` | 60/min | Catalog of SP-API and Ads report types |
| POST | `/api/v1/reports/request` | 30/min | Submit a report request to Amazon |
| GET | `/api/v1/reports/{id}/status` | 120/min | Poll report processing status |
| GET | `/api/v1/reports/{id}/download` | 20/min | Download completed report |
| POST | `/api/v1/reports/request-and-wait` | 10/min | All-in-one: submit + poll + BQ load (cron) |
| GET | `/api/v1/data/tables` | 60/min | List BigQuery tables with row counts |
| POST | `/api/v1/data/query` | 30/min | Query BigQuery data with SQL-like params |
| GET | `/api/v1/data/tables/{name}/latest` | 60/min | Get latest rows from a report table |
| POST | `/api/v1/data/load` | 10/min | Manual download + BQ load |

### 5.3 Request Body (ReportRequest)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `marketplace` | string | Yes | UK, DE, FR, IT, ES, or US |
| `report_type` | string | Yes | SP-API report type or Ads type ID |
| `start_date` | string | No | YYYY-MM-DD format |
| `end_date` | string | No | YYYY-MM-DD format |
| `is_ads` | boolean | No | True for Ads API reports (default: false) |
| `report_options` | dict | No | SP-API reportOptions (e.g., Brand Analytics) |

---

## 6. Report Types

### 6.1 SP-API Reports (21 types)

| Category | Report Types | Marketplaces |
|----------|-------------|-------------|
| Sales & Orders | `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL`, `GET_SALES_AND_TRAFFIC_REPORT`, + 3 more | All 6 |
| Inventory | `GET_MERCHANT_LISTINGS_ALL_DATA`, `GET_AFN_INVENTORY_DATA`, + 2 more | All 6 |
| FBA | `GET_AFN_INVENTORY_DATA`, `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA`, + 4 more | US only |
| Financial | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2`, + 2 more | All 6 |
| Tax | `SC_VAT_TAX_REPORT`, `GET_VAT_TRANSACTION_DATA`, + 1 more | EU only |

### 6.2 Amazon Ads Reports (27 types)

> **Note:** Ads API credentials (`ADS_*` secrets) are currently empty/placeholder. These must be populated in Secret Manager before Ads reports can be used.

| Category | Count | Examples |
|----------|-------|---------|
| Sponsored Products | 8 | sp_campaigns, sp_keywords, sp_targeting, sp_search_term |
| Sponsored Brands | 6 | sb_campaigns, sb_keywords, sb_search_term |
| Sponsored Display | 6 | sd_campaigns, sd_targeting, sd_product_ads |
| DSP | 4 | dsp_campaigns, dsp_inventory, dsp_audience |
| Attribution | 3 | attribution_performance, attribution_products |

---

## 7. Cloud Scheduler Configuration

28 cron jobs configured to run every Monday at 6:00 AM UTC:

| Job Group | Count | Report Type | Marketplaces |
|-----------|-------|------------|-------------|
| Sales Traffic 14d | 6 | `GET_SALES_AND_TRAFFIC_REPORT` | UK, DE, FR, IT, ES, US |
| Sales Traffic 30d | 6 | `GET_SALES_AND_TRAFFIC_REPORT` | UK, DE, FR, IT, ES, US |
| Active Listings | 6 | `GET_MERCHANT_LISTINGS_ALL_DATA` | UK, DE, FR, IT, ES, US |
| FBA Reports | 4 | Inventory, Fees, Reimbursements, Restock | US only |
| Settlements | 6 | `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` | UK, DE, FR, IT, ES, US |

- **Schedule:** `0 6 * * 1` (Every Monday, 06:00 UTC)
- **Auth:** OIDC token via compute service account + `X-API-Key: sk_live_cron_2026`
- **Timeout:** 600s attempt deadline, 540s internal poll timeout

---

## 8. BigQuery Data Architecture

- **Project:** `instant-contact-479316-i4`
- **Dataset:** `amazon_reports` (EU region)
- **Table naming:** `{report_type_snake_case}_{marketplace_lower}`
- **Metadata columns:** `_report_id`, `_marketplace`, `_loaded_at`, `_report_type`

Tables are auto-created on first data load with schema inferred from report data.

---

## 9. Security Model

### 9.1 API Keys

| Key Name | Purpose | Rate Tier |
|----------|---------|-----------|
| `sk_live_ecell_2026` | Production use (manual/dashboard) | Standard |
| `sk_live_claude_2026` | AI agent integration | Standard |
| `sk_live_cron_2026` | Cloud Scheduler automation | Standard |

### 9.2 Credential Storage

All sensitive credentials stored in Google Secret Manager (16 secrets total):

- **EU SP-API:** `EU_LWA_APP_ID`, `EU_LWA_CLIENT_SECRET`, `EU_REFRESH_TOKEN`, `EU_AWS_ACCESS_KEY`, `EU_AWS_SECRET_KEY`
- **US SP-API:** `US_LWA_APP_ID`, `US_LWA_CLIENT_SECRET`, `US_REFRESH_TOKEN`, `US_AWS_ACCESS_KEY`, `US_AWS_SECRET_KEY`
- **Ads API:** `ADS_CLIENT_ID`, `ADS_CLIENT_SECRET`, `ADS_EU_PROFILE_ID`, `ADS_EU_REFRESH_TOKEN`, `ADS_US_PROFILE_ID`, `ADS_US_REFRESH_TOKEN`
- **API Keys:** `API_KEYS` (JSON array of `{key, name, active}`)

---

## 10. Future Roadmap

| Priority | Feature | Description |
|----------|---------|-------------|
| P0 | Populate Ads API credentials | Add real `ADS_*` secrets to enable 27 Ads report types |
| P1 | Customer Service Metrics | Add `GET_FLAT_FILE_CUSTOMER_METRICS_REPORT` to cron schedule |
| P1 | GCS Archival | Archive raw report files to Cloud Storage for audit trail |
| P2 | Dashboard UI | Build Looker Studio or custom dashboard on BigQuery data |
| P2 | Alerting | Cloud Monitoring alerts for failed cron jobs or data anomalies |
| P3 | CSV Export to Mac Studio | Sync BigQuery data to local Mac Studio for offline analysis |
