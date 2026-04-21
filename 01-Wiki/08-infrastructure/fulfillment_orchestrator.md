# fulfillment orchestrator
*Auto-created by vault compiler on 2026-04-13*

- **Technical Specifications:**
- **Stack:** Next.js 14.
- **Core Engine:** 3-layer routing engine with BigQuery order integration.
- **Operational Features:** Supports manual overrides for printer downtime, holidays, peak mode, and "force-to-PHL" scenarios.
- **Data Sync:** A worker polls for updates every 2 minutes, caching results to `data/orders-cache.json`.
