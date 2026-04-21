# Apr 10 — Cloud Run Amazon Reports API Investigation

**Blockers**
- **Technical Verification Needed:** Need Codex to inspect Cloud Run to determine if `PutListingsItem` or `UpdateListingItem` is supported, and to verify if SP-API credentials/refresh tokens are active.
- **Service Ambiguity:** Unclear if Amazon Reports API is hosted in `ecell-dashboard` or `sales-dashboard-v2`.
- **Pending Decision:** Awaiting Cem's direction on whether to prioritize listing edit capability (shipping templates) or report automation.

**Knowledge**
- **Amazon Reports API Status:** **RUNNING** on Cloud Run (ref: `TOOLS.md`).
- **Cloud Run Service Inventory:** `ecell-dashboard` (Apr 9), `fba-planner` (Apr 9), `procurement-system` (Apr 7), `sales-dashboard` (Mar 4), `sales-dashboard-v2` (Mar 3), `nbcu-po-app` (Mar 20).
- **Potential Report IDs (Sales Traffic by Child ASIN):** `GET_SALES_AND_TRAFFIC_BY_ASIN`, `GET_MERCHANT_LISTINGS_ALL_DATA`, `GET_SALES_AND_TRAFFIC_REPORT`.
- **API Implementation Flow:** `CreateReport