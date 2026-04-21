# PULSE Unified Product DB — Research Brief for Analyst Agent

## Mission
Review ALL existing documentation, schemas, and data sources to produce a UNIFIED PRODUCT DATABASE SPEC that becomes the foundation for:
1. Gap analysis (what's selling but not listed on each marketplace)
2. Marketplace listing deployment (push products to Walmart, Target+, etc.)
3. Revenue intelligence (velocity, signals, priority scoring)

## Your Deliverables
1. **DATA_SOURCE_MAP.md** — Every data source we have, what it contains, how current it is, what's missing
2. **UNIFIED_SCHEMA.md** — The target Supabase schema for the centralized product DB
3. **MIGRATION_PLAN.md** — Step-by-step to get from current state → unified DB
4. **GAP_REPORT.md** — What data we're missing and how to get it

## Context

### Business
- Ecell Global sells licensed phone cases, skins, desk mats, etc. across Amazon, Walmart, eBay, BigCommerce (GoHeadCase), Target+, TikTok Shop, Etsy
- Amazon is ~76% of revenue (3.44M active SKUs, ALL FBM)
- Walmart has 95,640 active SKUs
- SKU format: `{product_type}-{device}-{design}-{variant}` (e.g., HTPCR-IPH16PM-PNUTSNF-COL)
- The "headcase" database in the Philippines is the PRODUCT MASTER (designs, lineups, devices, availability)

### SKU Anatomy
- product_type_code: HTPCR (snap case), HC (hard case), HDMWH (desk mat), HB6CR (soft gel), H8939 (vinyl skin), HLBWH (wallet), etc.
- device_code: IPH16PM (iPhone 16 Pro Max), SAMGS25U (Samsung Galaxy S25 Ultra), etc.
- design_code: PNUTSNF (Peanuts Snoopy), NARUGRAT (Naruto), NCFCCKT (Newcastle FC Kit), etc.
- design_variant: COL (color variant), specific character names, etc.

### Current Data Sources

#### BigQuery (instant-contact-479316-i4)

**headcase dataset** (PRODUCT MASTER mirror):
- tblDesigns (110,635 rows): DesignID, DesignLabel, DesignName, LineupID, ImageURL, DesignerID, DesignStatus, WithLogo
- tblDesignProductAvailability (1,230,108 rows): DesignID, DesignProductID, BrandBatchID, IsApproved, ProductColorID, Status
- tblDesignGroupAvailability (71,185 rows)
- tblDesignTags (445 rows)
- tblDesigners (83 rows)
- tblDesignsSellingBatch
- tblLineups: LineupID, Lineup, LineupLabel, DateAdded, DesignerID, LineupStatus, RawPathID
- tblLineupPersonalities
- tblLineupTypes
- tblPersonalities
- tblTypes: TypeID, Type, Description
- tblRawPaths
- tblTags
- tblEbayAccounts, tblEbayFiles, tblEbaySites, tblEbayTemplates

**zero_dataset** (ORDERS + MARKETPLACE DATA):
- orders (2,802,015 rows): Sales_Record_Number, Transaction_Id, Paid_Date, Custom_Label, Net_Sale, Currency, Marketplace, Status, Is_Refunded, Brand, Product, etc.
- amazon_active_listings (3,441,323 rows): seller_sku, asin1, item_name, price, quantity, open_date, fulfillment_channel, product_id
- walmart_active_listings (95,640 rows): sku, item_id, product_name, lifecycle_status, publish_status, price, currency, gtin, upc, brand, product_type, reviews_count, variant_group_id, primary_variant, buy_box_eligible, average_rating
- brands (VIEW)
- inventory (VIEW)
- Various other views

#### Supabase (auzjmawughepxbtpwuhe.supabase.co)
Tables with data:
- orders (305,053 rows): Partial BQ mirror, has parsed columns (product_type_code, device_code, design_code, design_variant), net_sale_usd added
- inventory (9,805 rows): Warehouse stock levels
- walmart_listings (201 rows): STALE — only 201 of 95K
- fx_rates_daily: Currency conversion rates
- brain_documents + brain_chunks: Memory layer (partially populated)
- cc_decisions, cc_projects, cc_metrics: Command center tables

Tables that EXIST but are EMPTY (0 rows):
- amazon_listings
- active_listings  
- amazon_inventory
- asin_bridge

#### Local Files
- Amazon Active Listings Report (6.4GB TSV, 3.44M rows) — already loaded to BQ
- Walmart Item Report (94MB CSV, 95,640 rows) — already loaded to BQ
- Amazon Child ASIN Business Report (80K rows XLSX)
- Royalty Advance Summary (license obligations)

### Zero Infrastructure (PHP/PH Network)
- Master DB: 192.168.20.160 (MySQL, PH local)
- UK source: 192.168.20.168
- US source: 192.168.20.66
- Views: `uv_get_amazon_active_listings_*_regen`
- REGEN app generates Active Listings reports
- Amazon MWS creds hardcoded in PHP
- BQ sync may be broken (hardcoded 2014 dates in ETL scripts)

## Wiki Files to Review
Read ALL of these for context on prior discussions, decisions, and specs:

### Product Intelligence / PULSE
- wiki/11-product-intelligence/*.md
- projects/product-intelligence-engine/PULSE_SCOPE_V3.md
- projects/product-intelligence-engine/EXECUTION_PLAN.md
- projects/product-intelligence-engine/PROJECT_BRIEF.md

### Sales & Data
- wiki/02-sales-data/*.md
- wiki/02-sales-data/SOP_SALES_ANALYTICS.md

### Listings & Amazon
- wiki/10-listingforge/*.md
- wiki/17-harry-workspace/projects/hcd-listing-generator/*.md
- wiki/17-harry-workspace/projects/amazon-sp-api/*.md

### Infrastructure
- wiki/08-infrastructure/*.md
- wiki/23-drew-handover/*.md (Zero infrastructure maps)
- wiki/17-harry-workspace/projects/fulfillment-orchestrator/*.md

### Design & Production
- wiki/06-design-automation/*.md
- wiki/03-production/*.md
- wiki/09-creative-pipeline/*.md

### Inventory & Shipping
- wiki/05-inventory/*.md
- wiki/04-shipping/*.md

### Prior Analysis Results
- results/pie-phase1.1-design-revenue-rankings.md
- results/pie-phase1.2-gap-analysis.md
- results/pie-phase1.2-product-type-gap-analysis.md
- results/walmart_gap_analysis.json
- results/PULSE_PRIORITY_BRIEF_2026-03-10.md

## Key Questions to Answer
1. What is the COMPLETE product entity model? (Design × Device × Product Type × Brand/Lineup × Variant)
2. How do BigCommerce product IDs map to the headcase DesignID system?
3. What's the ASIN → SKU → DesignID bridge?
4. What product attributes are needed for each marketplace (Walmart, Amazon, Target+)?
5. Where are product IMAGES stored? (headcase ImageURL? BigCommerce? S3?)
6. How are UPCs/GTINs generated and assigned?
7. What's the minimum viable unified schema that supports gap analysis + listing deployment?
8. What can we build TODAY with existing data vs what needs new data ingestion?
