# Handoff: Centralized Product Rules Engine — Harry

> From: Ava (Head of Sales & Marketing)
> To: Harry (COO) — build via Codex Engineer
> Date: 2026-03-04
> Priority: HIGH — blocks microsite launches + marketplace expansion

---

## Context

We're launching 4 microsites (Anime, Sports, Entertainment, Fantasy) + GoHeadCase umbrella, all feeding from one product system. Products need different titles per channel (Amazon = brand-registry compliant, DTC = keyword-first SEO, Walmart/Target = hybrid). Rather than backfilling a massive product database, we build a **rules engine** that generates listings from SKU components.

You already built `parse_sku()` in Supabase Project 2 — that's the foundation. This spec extends it.

## Architecture: Rules Engine + Lightweight Product Tracker

### Core Concept
The SKU IS the database. `HTPCR-IPH16PM-DRGBZICO-GOK` contains all the information — we just need lookup tables to decode each segment into human-readable titles and descriptions.

### Four Lookup Tables (Supabase Project 2)

#### 1. `product_types`
```sql
CREATE TABLE product_types (
  code TEXT PRIMARY KEY,           -- HTPCR, HLBWH, HDMWH, H7805, etc.
  name TEXT NOT NULL,              -- "Snap Case", "Leather Wallet", "Desk Mat", "AirPods Case"
  description TEXT NOT NULL,       -- "Military-grade TPU gel bumper with hard back. MagSafe compatible. 10ft drop tested."
  short_desc TEXT,                 -- "Snap Case" (for compact displays)
  category TEXT,                   -- "phone_case", "desk_mat", "airpods", "console_skin"
  created_at TIMESTAMPTZ DEFAULT now()
);
```

Source: SKU prefix codes from `Sku Parsing by Brand.txt` + existing product knowledge.
Known codes: HTPCR (Snap/TPU), HLBWH (Leather Wallet), HDMWH (Desk Mat), H7805 (AirPods), plus console skins, laptop skins, etc.

#### 2. `devices`
```sql
CREATE TABLE devices (
  code TEXT PRIMARY KEY,           -- IPH16PM, S925U, IPHAIR4, PS5CON, etc.
  name TEXT NOT NULL,              -- "iPhone 16 Pro Max"
  brand TEXT,                      -- "Apple", "Samsung", "Sony", "Microsoft", "Nintendo"
  type TEXT,                       -- "phone", "tablet", "airpods", "watch", "console", "desk_mat_size"
  generation TEXT,                 -- "current", "previous", "legacy"
  is_active BOOLEAN DEFAULT true,  -- Only current-gen for microsites
  sort_order INT,                  -- For display ordering
  created_at TIMESTAMPTZ DEFAULT now()
);
```

Source: Device codes from BigQuery orders, cross-ref with SKU parsing.
Flag `generation='current'` for latest devices only (iPhone 16 series, Galaxy S25 series, PS5, Xbox Series X, etc.)

#### 3. `brands_designs`
```sql
CREATE TABLE brands_designs (
  code TEXT PRIMARY KEY,           -- DRGBZICO, LFCKIT25, AFCCRE, etc.
  brand_code TEXT NOT NULL,        -- DRGBZ, LFC, AFC (the license code)
  brand_name TEXT NOT NULL,        -- "Dragon Ball Z", "Liverpool FC", "Arsenal FC"
  design_group TEXT NOT NULL,      -- "Iconic", "Kit 25/26", "Crest"
  category TEXT NOT NULL,          -- "anime", "sports", "entertainment", "fantasy"
  is_active_license BOOLEAN DEFAULT true,  -- FALSE if license expired/discontinued
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Separate table for individual designs within a group
CREATE TABLE designs (
  code TEXT PRIMARY KEY,           -- GOK, CREST, LKRA, etc.
  parent_code TEXT REFERENCES brands_designs(code),
  name TEXT NOT NULL,              -- "Goku", "Club Crest", "Liverbird"
  created_at TIMESTAMPTZ DEFAULT now()
);
```

Source: `Sku Parsing by Brand.txt` (861 brand codes) + `BRAND_CATEGORIES.md` (category mapping) + `headcase.tblLineups` (design group names) + `headcase.tblDesigns` (individual design names).

#### 4. `ean_registry`
```sql
CREATE TABLE ean_registry (
  sku TEXT PRIMARY KEY,
  ean TEXT UNIQUE NOT NULL,        -- 13-digit EAN
  gtin TEXT,                       -- 14-digit GTIN (leading zero + EAN)
  gs1_prefix TEXT,                 -- Which GS1 batch it came from
  assigned_at TIMESTAMPTZ DEFAULT now(),
  source TEXT                      -- "walmart_import", "target_import", "manual", "auto_assigned"
);
```

Source: Walmart listings (95K with GTINs), Target assortment (35,541 with barcodes), GS1 owned prefixes.
**NOTE:** Cem is getting updated EAN pool numbers — some batches weren't renewed. Wait for his input before mass-assigning. Current pool is ~200-300K.

### Title Generation Functions

```sql
-- Generate DTC title (keyword-first, SEO optimized)
CREATE OR REPLACE FUNCTION generate_title_dtc(input_sku TEXT)
RETURNS TEXT AS $$
DECLARE
  parsed RECORD;
  brand TEXT;
  design TEXT;
  product TEXT;
  device TEXT;
BEGIN
  -- Parse SKU
  parsed := parse_sku(input_sku);
  
  -- Look up components
  SELECT bd.brand_name, bd.design_group INTO brand, design
    FROM brands_designs bd WHERE bd.code = parsed.design_code;
  SELECT pt.short_desc INTO product FROM product_types pt WHERE pt.code = parsed.product_type_code;
  SELECT d.name INTO device FROM devices d WHERE d.code = parsed.device_code;
  
  -- Keyword-first: "Naruto Shippuden Snap Case - Iconic Goku | iPhone 16 Pro Max"
  RETURN COALESCE(brand, '') || ' ' || COALESCE(product, '') || ' - ' || COALESCE(design, '') || ' | ' || COALESCE(device, '');
END;
$$ LANGUAGE plpgsql;

-- Generate Amazon title (brand-registry compliant)
CREATE OR REPLACE FUNCTION generate_title_amazon(input_sku TEXT)
RETURNS TEXT AS $$
DECLARE
  parsed RECORD;
  brand TEXT;
  design TEXT;
  product TEXT;
  device TEXT;
BEGIN
  parsed := parse_sku(input_sku);
  SELECT bd.brand_name, bd.design_group INTO brand, design
    FROM brands_designs bd WHERE bd.code = parsed.design_code;
  SELECT pt.name INTO product FROM product_types pt WHERE pt.code = parsed.product_type_code;
  SELECT d.name INTO device FROM devices d WHERE d.code = parsed.device_code;
  
  -- "Head Case Designs Officially Licensed Naruto Shippuden Iconic Goku Snap Case Compatible with iPhone 16 Pro Max"
  RETURN 'Head Case Designs Officially Licensed ' || COALESCE(brand, '') || ' ' || COALESCE(design, '') || ' ' || COALESCE(product, '') || ' Compatible with ' || COALESCE(device, '');
END;
$$ LANGUAGE plpgsql;

-- Generate marketplace title (Walmart/Target)
CREATE OR REPLACE FUNCTION generate_title_marketplace(input_sku TEXT)
RETURNS TEXT AS $$
DECLARE
  parsed RECORD;
  brand TEXT;
  design TEXT;
  product TEXT;
  device TEXT;
BEGIN
  parsed := parse_sku(input_sku);
  SELECT bd.brand_name, bd.design_group INTO brand, design
    FROM brands_designs bd WHERE bd.code = parsed.design_code;
  SELECT pt.name INTO product FROM product_types pt WHERE pt.code = parsed.product_type_code;
  SELECT d.name INTO device FROM devices d WHERE d.code = parsed.device_code;
  
  -- "Naruto Shippuden Iconic Goku Snap Case for iPhone 16 Pro Max - Officially Licensed"
  RETURN COALESCE(brand, '') || ' ' || COALESCE(design, '') || ' ' || COALESCE(product, '') || ' for ' || COALESCE(device, '') || ' - Officially Licensed';
END;
$$ LANGUAGE plpgsql;
```

### Product Tracker (Lightweight)

For products actually LIVE on channels:

```sql
CREATE TABLE live_products (
  sku TEXT PRIMARY KEY,
  shopify_microsite_id BIGINT,     -- Product ID in microsite Shopify store
  shopify_ghc_id BIGINT,           -- Product ID in GoHeadCase store
  shopify_target_id BIGINT,        -- Product ID in Target+ store
  channels JSONB DEFAULT '{}',     -- {"amazon_us":true, "walmart":true, "dtc_anime":true}
  ean TEXT REFERENCES ean_registry(sku),
  status TEXT DEFAULT 'active',
  listed_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### Pipeline Stages (Future — Product Creation Workflow)

```sql
CREATE TABLE product_pipeline (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sku TEXT,                         -- Generated or proposed SKU
  stage TEXT CHECK (stage IN ('idea', 'proposed', 'content_ready', 'images_ready', 'listed', 'live')),
  brand_code TEXT,
  design_code TEXT,
  notes TEXT,                       -- "Variation of DRGBZICO - new colorway"
  assigned_to TEXT,                 -- Agent name: "Echo", "Iris", etc.
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

## Data Population Plan

### Immediate (populate lookup tables):
1. **product_types**: Manual — ~15-20 known product type codes. Quick job.
2. **devices**: Extract from BigQuery `zero_dataset.orders` — distinct device codes with sales volume. Flag current-gen.
3. **brands_designs**: Import from `Sku Parsing by Brand.txt` (861 codes) + merge with `BRAND_CATEGORIES.md` (category mapping) + `headcase.tblLineups` (readable names).
4. **ean_registry**: Import from Walmart listings (95K) + Target assortment (35.5K). Dedupe on SKU.

### Later (when Cem provides EAN pool):
5. Pre-assign EANs to top 500 products not already covered by Walmart/Target imports.

## Cross-Channel Gap Analysis

Build a weekly cron (or add to Ava's Monday Momentum Brief):

```sql
-- Find top sellers missing from channels
WITH top_sellers AS (
  SELECT 
    Custom_Label AS sku,
    SUM(SAFE_CAST(Quantity AS INT64)) AS units_90d
  FROM zero_dataset.orders
  WHERE PO_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    AND Is_Refunded != 'true'
  GROUP BY 1
  ORDER BY 2 DESC
  LIMIT 500
)
SELECT 
  ts.sku,
  ts.units_90d,
  lp.channels,
  -- Flag missing channels
  CASE WHEN lp.channels->>'walmart' IS NULL THEN 'MISSING' ELSE 'OK' END AS walmart,
  CASE WHEN lp.channels->>'dtc_anime' IS NULL THEN 'MISSING' ELSE 'OK' END AS dtc_anime
FROM top_sellers ts
LEFT JOIN live_products lp ON ts.sku = lp.sku
WHERE lp.sku IS NULL  -- Not tracked at all
   OR lp.channels::text NOT LIKE '%walmart%'  -- Missing from Walmart
ORDER BY ts.units_90d DESC;
```

## What Ava Will Provide
- Category mapping per brand (done: `BRAND_CATEGORIES.md`)
- Active device list for microsites (done: in PRODUCT_DATABASE_SPEC.md)
- Device inclusion rules (if PS5 sells, add Xbox, etc.)
- Weekly gap analysis report format

## What Harry Builds (Codex)
1. Four lookup tables + seed data
2. Title generation functions (3 channels)
3. `live_products` tracker
4. `product_pipeline` stages table
5. API endpoints or Edge Functions for title generation
6. Walmart full import (fix pagination — currently 201/95K, needs cursor pagination)

## Existing Assets to Reference
- `parse_sku()` function already in Project 2 ✅
- `inventory` table (9,805 rows) ✅
- `orders` table (304,778 rows) ✅
- `walmart_listings` table (201 rows, needs pagination fix) ✅
- `Sku Parsing by Brand.txt` on Drive (861 brand codes)
- `headcase.tblLineups` in BigQuery (10,265 lineup codes → names)
- `headcase.tblDesigns` in BigQuery (110,469 designs)
- `BRAND_CATEGORIES.md` in workspace (750 codes → 18 categories)

---

*Handoff by: Ava*
*Date: 2026-03-04*
*Save location: Brain/Handoffs/harry-product-db-handoff.md*
