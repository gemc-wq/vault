# Fulfillment Orchestrator (Phase 1 MVP)

ShipStation replacement for Head Case Designs (Ecell Global). Reads orders from BigQuery, routes them to the correct fulfillment site, generates **label batches** + **print-file placeholders**, reconciles, then writes dispatch logs back to BigQuery.

## Tech
- Next.js 14 (App Router), TypeScript, Tailwind
- BigQuery: `@google-cloud/bigquery` (ADC auth)
- Google Drive delivery: `rclone` CLI
- Label PDF batching: `pdf-lib`

## Setup
1. Copy env:
```bash
copy .env.example .env.local
```

2. Ensure Google ADC credentials:
```bash
gcloud auth application-default login
```

3. Install:
```bash
npm install
```

## Run
Dev UI:
```bash
npm run dev
```
Open http://localhost:3000/fulfillment

Worker (optional background poll/cache):
```bash
npm run worker
```

## What’s implemented (Phase 1)
- **Order Queue**: polls `instant-contact-479316-i4.zero_dataset.orders_clean` for `Status='ready_to_ship'`.
- **Routing Engine**:
  - Hard constraints: H89/HST/HDM never routed to PHL.
  - Saturday or Monday: PHL handles all eligible products.
  - Stock check: `zero_dataset.inventory` warehouse stock.
  - Manual overrides stored locally (printer downtime, holiday, peak mode).
- **Labels**: EasyPost stub (or TODO if key missing) → one PDF per site per batch → upload to GDrive.
- **Print files**: SKU parser + BigQuery design lookup attempt (headcase dataset) + placeholder output → upload to GDrive.
- **Reconciliation**: blocks dispatch until both forks done and SKU matches.
- **Writeback**: inserts to `zero_dataset.dispatch_log`.

## Local state
This MVP persists small state files under `./data/`:
- `overrides.json`
- `order-status.json`
- `reconciliation-log.jsonl`

## Drive paths
- Labels: `gdrive:/Fulfillment Orchestrator/Labels/{site}/{YYYY-MM-DD}/batch_<timestamp>.pdf`
- Print files: `gdrive:/Fulfillment Orchestrator/Print Files/{site}/{YYYY-MM-DD}/...`

