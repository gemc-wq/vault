# Fulfillment Orchestrator — Phase 1 Progress

## Status
- [x] Project scaffold (Next.js 14 App Router, TS, Tailwind)
- [x] Module 1: Order Queue (BigQuery query + sort)
- [x] Module 2: Routing Engine (3-layer w/ overrides + stock check)
- [x] Module 3: Label Gen (EasyPost stub + PDF batch per site + Drive upload)
- [x] Module 4: Print File (SKU parse + design lookup attempt + placeholder upload)
- [x] Module 5: Reconciliation (blocking + mismatch log)
- [x] Module 6: Operator UI (/fulfillment dashboard + overrides + process batch)
- [x] Module 7: Tracking writeback (BigQuery dispatch_log insert)

## How to run (dev)
```bash
npm run dev
```

## How to run worker
```bash
npm run worker
```

## Notes
- EasyPost + real TIFF rendering intentionally stubbed in Phase 1.
- Google Drive delivery via `rclone copy`.
