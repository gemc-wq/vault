# BigQuery Setup & Data Architecture — Drew Ramos Handover
*Source: Email thread between Drew and Cem, Jan 14-26 2026*
*Subject: Big Query resolved*

## BigQuery Structure
- **Project:** instant-contact-479316-i4
- **Dataset:** zero_dataset
- **Orders view:** `zero_dataset.orders` — this is a VIEW, not a raw table
- **Raw orders table:** `elcell_co_uk_barcode.order_tracker_xls`
- **Data refresh:** Updates every 24 hours (live sync from Zero)

## Key Insight
- `zero_dataset.orders` is a view that Drew updated to match Zero BI report queries
- The raw table `order_tracker_xls` lacks brand, product, and unit info that the view includes
- Drew created a `zero_orders_agent` in Conversational Analytics that uses the updated view

## Working Query Example
```sql
SELECT Buyer_Country, SUM(CAST(Quantity AS BIGNUMERIC))
FROM `instant-contact-479316-i4.zero_dataset.orders`
WHERE Paid_Date >= '2026-01-01'
GROUP BY Buyer_Country;
```
Note: Queries need a date filter to avoid timeouts on the full dataset.

## Amazon Merchant Token
- **Amazon US account:** A22QQRQRS0T6NJ
- Source: Drew email, Jan 28 2026

## Related
- [[wiki/02-sales-data/SCHEMA_DESIGN|Schema Design]] — How sales data is structured
- [[wiki/02-sales-data/SALES_ANALYSIS_2025|Sales Analysis 2025]] — Analysis built on BQ data
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE_MAP|Zero Infrastructure Map]] — BQ connects to Zero DB
- [[wiki/11-product-intelligence/PROJECT_BRIEF|PIE Project Brief]] — Uses BQ data for SKU selection
