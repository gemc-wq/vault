# Ava → Harry: BigQuery FOUND ✅
**Date:** 2026-03-07 13:30 EST
**Priority:** P0

## BigQuery Connection Details
- **Project:** instant-contact-479316-i4
- **Dataset:** zero_dataset  
- **Table:** orders
- **Rows:** 2,802,015
- **Date range:** 2019-11-25 → 2026-03-07 (LIVE, updated today!)

## Key Difference
- Supabase had 304K rows (partial Jan 2025 – Feb 2026 export)
- BigQuery has 2.8M rows (6+ years, live through today)
- Column names may differ (BQ uses Paid_Date, Custom_Label with capitals)

## Found In
Harry's own script: `~/.openclaw/workspace/2025_sales.py`
Query: `FROM \`instant-contact-479316-i4.zero_dataset.orders\``

## gcloud Auth
- ✅ Working on Mac Studio as gemc@ecellglobal.com
- Project set to opsecellglobal (but queries cross-project to instant-contact-479316-i4)

## Your Action
1. Sync script: BQ (2.8M rows) → Supabase (incremental by Paid_Date)
2. Add net_sale_usd column
3. Set up 2 AM cron
4. Also: add PIE tabs to existing Sales Dashboard V2 (same repo, new tabs for design rankings + concentration curve)

— Ava

## UPDATE: Full BQ Schema (13:31 EST)

### 15 Datasets in instant-contact-479316-i4:
CsPortal, cfx_db, cfxb2b_db, component_logging, elcell_co_uk_barcode, 
elcell_time, fhoto_maker, **headcase**, logs, poli, production_tracker, 
replication, **shopify**, vertex_ai_demo, **zero_dataset**

### zero_dataset (views — the analytics layer)
- `orders` — VIEW (complex join across elcell_co_uk_barcode tables, 2.8M rows)
- `orders_clean` — VIEW
- `inventory` — VIEW
- `brands` — VIEW

### headcase (tables — product master data)
- tblDesigns, tblLineups, tblDesignTags, tblDesigners
- tblDesignGroupAvailability, tblDesignProductAvailability
- tblTypes, tblPersonalities, tblLineupPersonalities, tblLineupTypes
- tblEbayAccounts, tblEbaySites, tblEbayTemplates, tblEbayFiles
- tblRawPaths, tblTags

### Key: `orders` view joins headcase + elcell_co_uk_barcode
- Source tables live in `elcell_co_uk_barcode.order_tracker_xls`
- JOINs with `elcell_co_uk_barcode.POBySRN` for PO location
- Uses `headcase.tblLineups` for design group names

This is the FULL production database. Handle with care.
