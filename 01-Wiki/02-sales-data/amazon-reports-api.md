# amazon-reports-api
*Auto-created by vault compiler on 2026-04-13*

- **Status:** Confirmed **RUNNING** on Cloud Run.
- **Implementation Flow:** `CreateReport` $\rightarrow$ Poll `GetReport` (status: DONE) $\rightarrow$ `GetReportDocument` $\rightarrow$ Store in Supabase/Trigger analysis.
- **Potential Amazon Report IDs for "Sales Traffic by Child ASIN":**
- `GET_SALES_AND_TRAFFIC_BY_ASIN`
- `GET_MERCHANT_LISTINGS_ALL_DATA`
- `GET_SALES_AND_TRAFFIC_REPORT`
