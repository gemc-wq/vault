# Fulfillment Orchestrator — Phase 1 Build Log
**Date:** 2026-02-22

## What was built
A Next.js 14+ (App Router) MVP that:
- Pulls `ready_to_ship` orders from BigQuery (`instant-contact-479316-i4.zero_dataset.orders_clean`).
- Applies Phase 1 priority sorting (expedited/Amazon first → latest `Dispatch_Date` → FIFO).
- Routes each order with a 3-layer routing engine (hard constraints + stock check + manual overrides).
- Runs two forks:
  - **Labels (stub)**: Generates a single **batch PDF per site** (UK/FL/PHL) via `pdf-lib` and uploads to Google Drive using `rclone`.
  - **Print files (stub)**: Parses SKU + attempts design lookup from `headcase` dataset; produces placeholder `.tiff` files and uploads to Google Drive using `rclone`.
- Reconciles the two forks (blocks if either missing / mismatch) and logs reconciliation events.
- Writes tracking + dispatch metadata to BigQuery table `zero_dataset.dispatch_log` (created if missing).

## Project location
`C:\Users\gemc\clawd\projects\fulfillment-orchestrator\`

## Key UI
- Dashboard: `http://localhost:3000/fulfillment`
  - Order queue table (SRN, SKU, Buyer_Country, routed_site, flags, reasons)
  - Manual overrides panel (printer downtime, holiday, peak mode, force-to-PHL)
  - **Process Batch** button to trigger full pipeline

## Key API routes
- `GET /api/orders?limit=...` → routed queue + overrides
- `POST /api/process` → triggers routing + label/print stubs + reconciliation + dispatch_log insert
- `GET/POST /api/overrides` → read/update overrides
- `GET /api/status` → current local processing status map

## Local state files
Stored under `./data/`:
- `overrides.json`
- `order-status.json`
- `reconciliation-log.jsonl`
- (optional worker cache) `orders-cache.json`

## Worker
Added `npm run worker` which polls every 2 minutes and writes a cache file (`data/orders-cache.json`).

## Environment
- `.env.example` added with GCP + rclone + worker settings.
- Uses Google ADC credentials (`gcloud auth application-default login`).

## Phase 1 stubs / TODOs
- Real EasyPost purchase + label PDF retrieval (currently a placeholder label page per order).
- Real TIFF/EPS rendering pipeline (currently placeholder `.tiff` files containing metadata text).
- Inventory table/warehouse naming may require tuning (Phase 1 uses `zero_dataset.inventory`).

