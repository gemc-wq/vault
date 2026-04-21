# Ava → Harry: Amazon Data Pipeline
**Date:** 2026-03-07 17:37 EST
**Priority:** P1

## 1. Amazon Active Listings → Supabase or BigQuery
- File: `gdrive:Clawdbot Shared Folder/Brain/Projects/Amazon/Active+Listings+Report_03-05-2026.txt`
- ~3.44M SKUs, US marketplace
- Was in the Walmart folder, moved to new Amazon folder
- **Your call:** Supabase table (`amazon_listings`) or BQ table — whichever works best for the dashboard queries
- Key columns needed: ASIN, SKU, title, price, quantity, status, fulfillment channel (FBM/FBA)
- Parse SKU into: product_type_code, device_code, design_code, design_variant

## 2. Weekly SP-API Cron (Future)
- Cem wants automated weekly pulls of Amazon Active Listings
- Markets: US first, then UK and Germany
- SP-API keys available (check your credentials file)
- Cron: once per week, pull active listings → upsert into Supabase/BQ
- This replaces manual XLSX uploads

## 3. Context
- Conversion metrics are now a core PIE layer (Layer 7)
- Key insight: HB401 converts at 2.5x HTPCR rate but has 0.68% listing share — under-distributed
- Gap analysis needs: Amazon active listings (what's live) × BQ orders (what sells) × BC catalog (what exists)
- Dashboard needs to show: listings by product type, conversion benchmarks, gap ratios

## 4. GDrive Amazon Folder
New folder created: `Brain/Projects/Amazon/`
Contains:
- Active+Listings+Report_03-05-2026.txt (US listings)
- BusinessReportbychildAmazonUS_Jan1_Feb24 1.xlsx (US sessions)
- More data coming from Cem (UK sessions, keyword reports)

— Ava

## 5. CRITICAL: ASIN → SKU Bridge Table
Amazon session reports (standard "by parent" version) only contain ASIN, NOT SKU.
The Active Listings file is the ASIN→SKU lookup.
Without it loaded, session data is unactionable.

**The join:** session_report.ASIN → active_listings.ASIN → active_listings.SKU → parse into design_code/device_code/product_type

The "by child" report Cem uploaded this time happened to include SKU, but that's not guaranteed for future pulls. The Active Listings table must be the canonical ASIN→SKU bridge.

Priority: load Active Listings FIRST, then session reports JOIN against it.
