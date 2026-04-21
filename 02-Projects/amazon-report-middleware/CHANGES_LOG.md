# Middleware & API Changes Log

**Date range:** April 2026 (recent sessions)
**Repos affected:**
- `Claude Code FBA/fba-management-app/` (Streamlit app)
- `amazon-report-middleware/` (Cloud Run FastAPI service)

---

## 1. Middleware: New Endpoints Added

### 1.1 Listings Sync (Two-Step Pattern)

The previous single-call sync would time out (Cloud Run / load balancer 60s idle timeout) when downloading and processing the full 6GB+ `GET_MERCHANT_LISTINGS_ALL_DATA` report. Replaced with a two-step async pattern:

**Step 1 -- Submit** `POST /api/v1/listings/sync`
- Submits an SP-API `GET_MERCHANT_LISTINGS_ALL_DATA` report request
- Returns immediately with a `report_id`
- Body: `{ "marketplace": "US" }`

**Step 2 -- Complete** `POST /api/v1/listings/sync/complete`
- Polls Amazon for report status
- If `DONE`: streams compressed report to GCS, then loads GCS to BigQuery
- If still processing: returns `{ "status": "processing" }` -- caller retries in 30-60s
- Body: `{ "marketplace": "US", "report_id": "<id from step 1>" }`

### 1.2 Listings Lookup `POST /api/v1/listings/lookup`
- Batch ASIN-to-SKU lookup from BigQuery `merchant_listings_all_data_us` table
- Max 500 ASINs per request
- Returns: `seller_sku`, `item_name`, `fulfillment_channel`, `price`, `has_fba_twin`
- FBA twin detection uses F-prefix SKU convention and base-SKU grouping
- Rate limit: 60/minute

---

## 2. Middleware: GCS Streaming for Large Reports

**Problem:** The full US merchant listings report (~6GB uncompressed) caused Cloud Run OOM (exceeded 8GB memory limit at 8855MB).

**Solution:** Stream compressed report directly to GCS, let BigQuery decompress natively:

- **`report_engine.py` -- `sp_download_report_to_gcs()`**
  - Streams SP-API report download in 8MB chunks directly to GCS
  - If Amazon provides GZIP compression, uploads the compressed file as-is
  - GCS bucket: `gs://ecell-bq-import/reports/merchant_listings_all_data/`
  - Zero in-memory decompression -- never holds the full file

- **`bigquery_loader.py` -- `load_gcs_to_bigquery()`**
  - Loads TSV (or gzip TSV) from GCS URI into BigQuery
  - BigQuery natively decompresses gzip during load
  - Config: `WRITE_TRUNCATE` (full table replace), `allow_jagged_rows=True`, `max_bad_records=100`
  - Schema: auto-detected from TSV headers (34 columns)

**Result:** `merchant_listings_all_data_us` table: **4,087,163 rows / 7.7 GB** loaded successfully.

---

## 3. Middleware: Authentication

No credential changes were made. Existing dual-auth pattern remains:

| Layer | Header | Source |
|-------|--------|--------|
| GCP Identity Token | `Authorization: Bearer <token>` | `gcloud auth print-identity-token` |
| API Key | `X-API-Key: sk_live_ecell_2026` | GCP Secret Manager (`API_KEYS`) |

**API keys** are stored as JSON in Secret Manager under `API_KEYS`:
```json
{ "sk_live_ecell_2026": { "name": "ecell", "ips": [] } }
```

**SP-API credentials** are stored individually in Secret Manager:
- `US_LWA_APP_ID`, `US_LWA_CLIENT_SECRET`, `US_REFRESH_TOKEN`
- `US_AWS_ACCESS_KEY`, `US_AWS_SECRET_KEY`
- (Same pattern for `EU_` prefix)

### SP-API Permission Limitation (Unresolved)

The current SP-API developer app credentials only have the **Listings** role. Attempting to fetch Analytics reports (`GET_SALES_AND_TRAFFIC_REPORT`) or Inventory reports (`GET_AFN_INVENTORY_DATA`) returns:

```
Access to the resource is forbidden
```

**Action required:** In Seller Central > Developer Apps, add the following roles:
- **Analytics** -- for Sales & Traffic reports
- **Inventory** -- for FBA inventory reports

---

## 4. FBA Management App: BigQuery Direct Lookup

### Before (broken)
- `asin_sku_lookup.py` queried a local SQLite database at `/Users/openclaw/.openclaw/workspace/data/local_listings.db`
- This file didn't exist, so all lookups failed

### Intermediate (slow)
- Rewired to call middleware `POST /api/v1/listings/lookup` endpoint
- Required gcloud identity token + HTTP round-trip to Cloud Run + Cloud Run queries BigQuery
- Caused app to freeze on upload (blocking HTTP call during Streamlit render)

### Current (direct BigQuery)
- `asin_sku_lookup.py` queries BigQuery directly using `google-cloud-bigquery` client
- Table: `instant-contact-479316-i4.amazon_reports.merchant_listings_all_data_us`
- Batch size: 5000 ASINs per query (BigQuery handles large IN clauses natively)
- Performance: ~3s for 500 ASINs (including BigQuery cold start)
- No middleware dependency for enrichment

---

## 5. FBA Management App: SKU Enrichment Flow

### Problem
Amazon Business Reports downloaded manually (Child ASIN granularity) have no SKU column. The app's column mapper was incorrectly treating `(Child) ASIN` as a SKU column.

### Fix Applied

1. **`config/defaults.py`** -- Removed ASIN variants from SKU column candidates:
   ```python
   # Before:
   'sku': ['SKU', 'sku', 'Seller SKU', ..., 'ASIN', '(Child) ASIN']
   # After:
   'sku': ['SKU', 'sku', 'Seller SKU', 'seller sku', 'seller_sku', 'seller-sku']
   ```

2. **`src/data_loader.py`** -- Fallback when no SKU column exists:
   - Removed `sku` from `required_columns` (now only `['units', 'revenue']`)
   - If no SKU column found, uses `(Child) ASIN` column and sets `_needs_sku_enrichment = True`

3. **`app.py`** -- Auto-enrichment on upload:
   - Detects `_needs_sku_enrichment` flag after parsing
   - Shows spinner: "Enriching X ASINs with SKU data from BigQuery..."
   - Queries BigQuery directly (no middleware)
   - Displays match stats: "matched X ASINs, Y not found"

4. **`app.py`** -- Prevents re-processing on Streamlit reruns:
   - Tracks uploaded filename in `st.session_state['_loaded_file_long']` etc.
   - Skips processing if the same file is already loaded

---

## 6. Middleware: Infrastructure Summary

| Component | Value |
|-----------|-------|
| Service URL | `https://amazon-report-middleware-175143437106.europe-west1.run.app` |
| Region | `europe-west1` |
| GCP Project | `instant-contact-479316-i4` |
| BigQuery Dataset | `instant-contact-479316-i4.amazon_reports` |
| Listings Table (US) | `merchant_listings_all_data_us` (4.08M rows) |
| GCS Bucket | `gs://ecell-bq-import/reports/` |
| Memory | 512Mi (Cloud Run default) |
| Timeout | 600s |
| Min/Max Instances | 0 / 5 |
| Deploy Command | `./deploy.sh` |

### All Middleware Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/reports/request` | Submit any SP-API report |
| GET | `/api/v1/reports/{id}/status` | Check report status |
| GET | `/api/v1/reports/{id}/download` | Download completed report |
| POST | `/api/v1/reports/request-and-wait` | Synchronous submit + poll + download |
| POST | `/api/v1/listings/sync` | Step 1: Submit listings report |
| POST | `/api/v1/listings/sync/complete` | Step 2: Stream to GCS + load to BQ |
| POST | `/api/v1/listings/lookup` | Batch ASIN-to-SKU lookup |
| GET | `/health` | Health check |

---

## 7. Environment Variables (FBA App)

File: `fba-management-app/.env`

| Variable | Purpose |
|----------|---------|
| `AMAZON_MIDDLEWARE_KEY` | API key for middleware (`sk_live_ecell_2026`) |

The app also uses **Google Application Default Credentials** for direct BigQuery access (via `gcloud auth application-default login`).

---

## 8. Known Issues / TODO

- **SP-API permissions** -- Add Analytics + Inventory roles in Seller Central for auto-fetch to work
- **UK marketplace** -- Only US listings table exists; UK sync not yet configured
- **Middleware not redeployed** -- Local changes to `main.py`, `report_engine.py`, `bigquery_loader.py`, and `requirements.txt` may need `./deploy.sh` to push to Cloud Run
