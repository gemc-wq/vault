# Apr 10 — Cloud Run Amazon Reports API Investigation

**Blockers**
- **Code Access:** Need Codex to inspect Cloud Run service details to determine if `PutListingsItem` or `UpdateListingItem` is supported.
- **Service Ambiguity:** Unclear if the Amazon Reports API is embedded in `ecell-dashboard` or `sales-dashboard-v2`.
- **Credential Verification:** Need to confirm if SP-API credentials and refresh tokens are currently active in the Cloud Run environment.
- **Priority Definition:** Awaiting direction from Cem on whether to prioritize listing edit capability (shipping templates) or report automation.

**Knowledge**
- **Amazon Reports API Status:** Confirmed **RUNNING** on Cloud Run (per `TOOLS.md`).
- **Cloud Run Service Inventory:**
    - `ecell-dashboard` (deployed Apr 9)
    - `fba-planner` (deployed Apr 9)
    - `procurement-system` (deployed Apr 7)
    - `sales-dashboard` (deployed Mar 4)
    - `sales-dashboard-v2` (deployed Mar 3)
    - `nbcu-po-app` (deployed Mar 20)
- **Potential Amazon Report IDs for "Sales Traffic by Child ASIN":**
    - `GET_SALES_AND_TRAFFIC_BY_ASIN`
    - `GET_MERCHANT_LISTINGS_ALL_DATA`
    - `GET_SALES_AND_TRAFFIC_REPORT`
- **API Implementation Flow:** `CreateReport` $\rightarrow$ Poll `GetReport` (status: DONE) $\rightarrow$ `GetReportDocument` $\rightarrow$ Store in Supabase/Trigger analysis.
- **Reference Documentation:**
    - `TOOLS.md`: Amazon Reports API status.
    - `SOP_WEEKLY_REPORTS.md`: Current manual download process.
    - `SP-API-GUIDE.md`: SP-API capabilities.

**Carry-forwards**
- **Codex Task:** Inspect Cloud Run source code for SP-API scope permissions and identify the exact "Sales Traffic by Child ASIN" report ID.
- **Implementation Plan:** 
    - If listing edits are possible: Implement bulk shipping template updates.
    - If report API is available: Automate weekly pulls and analysis.
- **Workflow/Ownership:** Ava (strategy) $\rightarrow$ Codex (investigation) $\rightarrow$ Harry (implementation).