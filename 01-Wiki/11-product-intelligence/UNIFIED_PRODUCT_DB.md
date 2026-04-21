# Unified Product Database — Technical Documentation

> Owner: Ava | Created: 2026-03-10 | Status: **Building**

---

## Overview

The Unified Product Database is the centralized product intelligence layer for Ecell Global. It replaces scattered marketplace exports with a single queryable source of truth for:
- **What products exist** (design × device × product type combinations)
- **Where they're listed** (Amazon, Walmart, Shopify, etc.)
- **What's missing** (gap analysis across channels)

## Architecture

```
BigQuery (headcase master)  ──→  Supabase (Unified Product DB)  ──→  PULSE Dashboard
BQ (orders + marketplace)   ──→       ↓                              Gap Reports
                                 marketplace_listings                  Shopify Push
```

**Source of truth:** BigQuery `headcase` dataset (mirror of PH MySQL master)
**Operational layer:** Supabase `auzjmawughepxbtpwuhe`
**Downstream:** PULSE dashboard, gap analysis queries, Shopify listing pipeline

## Schema

### Dimension Tables (loaded ✅)

#### `lineups` — Brands & Licenses
| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT PK | From headcase.tblLineups.LineupID |
| name | TEXT | Brand/license name (e.g., "Peanuts", "Liverpool FC") |
| created_at | TIMESTAMPTZ | |

- **Source:** `headcase.tblLineups`
- **Rows:** 10,279
- **Examples:** Peanuts, Dragon Ball Z, Liverpool FC, Harry Potter, WWE

#### `designs` — Creative Assets
| Column | Type | Description |
|--------|------|-------------|
| id | BIGINT PK | From headcase.tblDesigns.DesignID |
| lineup_id | BIGINT FK→lineups | Parent brand/license |
| code | TEXT (indexed) | Design code from SKU (e.g., "PNUTSNF", "DRGBZICO") |
| name | TEXT | Human-readable name (e.g., "Snoopy", "Iconic Goku") |
| image_url | TEXT | URL to design image asset |
| status | INT | Design status flag |
| created_at | TIMESTAMPTZ | |

- **Source:** `headcase.tblDesigns`
- **Rows:** 110,634
- **Note:** `code` is NOT unique — some design codes are reused across lineups. Index is non-unique.

#### `product_types` — Case/Accessory Styles
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment |
| code | TEXT UNIQUE | SKU prefix (e.g., "HTPCR", "HDMWH", "HB6CR") |
| description | TEXT | Human name (to be populated) |
| created_at | TIMESTAMPTZ | |

- **Source:** Supabase `orders.product_type_code` + BQ `Custom_Label` parsing
- **Rows:** 146
- **Key codes:** HTPCR (Snap Case), HDMWH (Desk Mat), HB6CR (Soft Gel), HLBWH (Leather Wallet), H7805 (AirPods)

#### `devices` — Phones, Consoles, Gadgets
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment |
| code | TEXT UNIQUE | Device code from SKU (e.g., "IPH16PM", "SAMGS25U") |
| name | TEXT | Human name (to be populated) |
| family | TEXT | Device family (e.g., "iPhone 16") |
| brand | TEXT | Manufacturer (e.g., "Apple", "Samsung") |
| created_at | TIMESTAMPTZ | |

- **Source:** Supabase `orders.device_code` + BQ `Custom_Label` parsing
- **Rows:** 1,322

### Fact Tables (building 🔧)

#### `products` — Unified Product Combinations
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Auto-generated |
| product_type_id | INT FK→product_types | |
| device_id | INT FK→devices | |
| design_id | BIGINT FK→designs | |
| sku_fragment | TEXT (indexed) | Generated: `{pt_code}-{dev_code}-{design_code}` |
| created_at | TIMESTAMPTZ | |

- **Unique constraint:** (product_type_id, device_id, design_id)
- **Source:** Will be generated from BQ orders (distinct combinations that have actually sold)
- **Status:** Table created, not yet populated

#### `marketplace_listings` — Channel Presence
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Auto-generated |
| product_id | UUID FK→products | Links to unified product |
| marketplace | TEXT (indexed) | Channel: "amazon_us", "walmart_us", "shopify", etc. |
| sku | TEXT (indexed) | Full seller SKU |
| marketplace_product_id | TEXT | ASIN (Amazon), Item ID (Walmart), etc. |
| shopify_product_id | BIGINT (indexed) | Shopify product ID (hub for multi-channel push) |
| variant_info | TEXT | SKU variant segment |
| title | TEXT | Listing title |
| price | NUMERIC(10,2) | |
| currency | TEXT | |
| gtin | TEXT | GTIN/barcode |
| upc | TEXT | UPC |
| url | TEXT | Listing URL |
| status | TEXT | ACTIVE, INACTIVE, etc. |
| is_buy_box_eligible | BOOLEAN | Amazon Buy Box status |
| last_synced_at | TIMESTAMPTZ | |

- **Unique constraint:** (product_id, marketplace)
- **Source:** BQ `amazon_active_listings` + `walmart_active_listings`
- **Status:** Table created, not yet populated

## ETL Process

### Step 1: Dimension Tables (DONE ✅)
```
headcase.tblLineups       → lineups (10,279 rows)
headcase.tblDesigns       → designs (110,634 rows)
orders.product_type_code  → product_types (146 rows)
orders.device_code        → devices (1,322 rows)
```

### Step 2: Products Table (NEXT)
```sql
-- Generate from historical orders (known-good combinations)
SELECT DISTINCT product_type_code, device_code, design_code
FROM orders
WHERE all three are NOT NULL
-- Join to dimension tables for FK IDs
-- Insert into products with generated sku_fragment
```

### Step 3: Marketplace Listings (AFTER STEP 2)
```sql
-- Amazon: Parse seller_sku from BQ amazon_active_listings
-- Walmart: Parse sku from BQ walmart_active_listings
-- Match to products table via sku_fragment
-- Insert with marketplace-specific fields (ASIN, Item ID, GTIN, etc.)
```

### Step 4: Gap Analysis Queries
```sql
-- Example: Top Amazon sellers missing from Walmart
SELECT p.sku_fragment, d.name as design, dev.code as device, pt.code as product_type,
       ml_amz.price as amazon_price
FROM products p
JOIN designs d ON p.design_id = d.id
JOIN devices dev ON p.device_id = dev.id
JOIN product_types pt ON p.product_type_id = pt.id
JOIN marketplace_listings ml_amz ON p.id = ml_amz.product_id AND ml_amz.marketplace = 'amazon_us'
LEFT JOIN marketplace_listings ml_wmt ON p.id = ml_wmt.product_id AND ml_wmt.marketplace = 'walmart_us'
WHERE ml_wmt.id IS NULL
ORDER BY ml_amz.price DESC;
```

## Connection Details
- **Host:** db.auzjmawughepxbtpwuhe.supabase.co
- **Port:** 5432
- **Database:** postgres
- **User:** postgres
- **SSL:** require
- **Note:** Direct connection works; Session Pooler returns "Tenant not found" (may need IPv4 add-on for pooler)

## Indexes
| Index | Table | Column(s) |
|-------|-------|-----------|
| idx_designs_code | designs | code |
| idx_designs_lineup | designs | lineup_id |
| idx_products_sku_fragment | products | sku_fragment |
| idx_products_design | products | design_id |
| idx_products_device | products | device_id |
| idx_products_type | products | product_type_id |
| idx_marketplace_product | marketplace_listings | product_id |
| idx_marketplace_sku | marketplace_listings | sku |
| idx_marketplace_channel | marketplace_listings | marketplace |
| idx_marketplace_shopify | marketplace_listings | shopify_product_id |

## Known Issues
1. **Design code not unique** — Multiple designs share the same code (e.g., "BLU"). The `code` column has a non-unique index. Design ID is the true primary key.
2. **Orphan lineup references** — ~500 designs reference lineup IDs not in tblLineups. FK constraint set to `NOT VALID` to allow these.
3. **Device/product_type descriptions empty** — Codes loaded but human-readable names need population (from headcase tblTypes or manual mapping).
4. **BQ sync freshness** — Orders data in Supabase is stale (ends Feb 17, 2026). BQ orders are live. Product types/devices derived from both sources.

## Refresh Strategy
- **Dimension tables:** Weekly full refresh from BQ headcase
- **Products table:** Daily delta from new orders
- **Marketplace listings:** Daily refresh from BQ amazon_active_listings + walmart_active_listings
- **Target:** Cron job at 3 AM ET

---

*Document: wiki/11-product-intelligence/UNIFIED_PRODUCT_DB.md*
*Last updated: 2026-03-10 by Ava*
