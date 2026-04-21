# PULSE v2 — Product Uplift & Listing Signal Engine
*Version: 2.0 | Date: 2026-03-10 | Owner: Ava (CPSO)*

---

## What PULSE Is
A **listing deployment tool** — not an analytics dashboard. PULSE finds what's selling but missing from channels, and pushes those products to market via Shopify.

## Architecture: Shopify as Central Hub

```
[BigQuery: headcase + zero_dataset]
        ↓ ETL
[Supabase: Unified Product DB]
        ↓ Gap Analysis
[PULSE: identifies missing listings]
        ↓ Generates product data
[Shopify: central product catalog]
        ↓ Connectors
[Walmart] [Target+] [OnBuy] [Kaufland] [Microsites]
```

**Why Shopify:** One source of truth for product data. Connectors handle marketplace-specific formatting (titles, GTINs, categories). No per-marketplace API headaches. Already connected to Target+ and GoHeadCase.

## Three Screens Only

### Screen 1: Gap Report
**Purpose:** Show what's selling on Amazon but missing on other channels.

| Column | Source |
|--------|--------|
| Design × Product Type | Unified products table |
| Amazon Revenue (90d) | BQ orders |
| Amazon Velocity (2mo vs 6mo) | BQ orders |
| Listed on Walmart? | marketplace_listings |
| Listed on Shopify? | marketplace_listings |
| Listed on Target+? | marketplace_listings |
| Opportunity Score | Calculated: revenue × velocity × channel_gaps |

**Filters:** Brand/License, Product Type, Device Family, Min Revenue, Channel missing from.

**Default view:** Sorted by Opportunity Score DESC. Top = highest revenue designs missing from most channels.

### Screen 2: Action Queue
**Purpose:** Review and approve listings before push.

For each gap item:
- Pre-generated title (per channel rules)
- Pre-generated description
- Price (from Amazon baseline ± margin rules)
- UPC/GTIN (from ean_registry or auto-assigned)
- Image URL (from headcase.tblDesigns.ImageURL)
- Shopify product type mapping

**Actions:**
- ✅ Approve (add to publish queue)
- ✏️ Edit (modify title/price/description)
- ❌ Skip (with reason)
- 🔄 Regenerate (re-run title generation with different rules)

### Screen 3: Publish Dashboard
**Purpose:** Track what's been pushed, what's live, what failed.

| Column | Data |
|--------|------|
| SKU | The product |
| Pushed to Shopify | Date + Shopify product ID |
| Walmart Status | Pending / Live / Error |
| Target+ Status | Pending / Live / Error |
| OnBuy Status | Pending / Live / Error |
| Revenue Since Listed | From orders (when available) |

## Data Model (Supabase)

### Core Tables (from UNIFIED_PRODUCT_DB_SPEC)
- `product_types` — HTPCR, HDMWH, HB6CR, etc.
- `devices` — IPH16PM, SAMGS25U, etc.
- `lineups` — Brand/license (from headcase.tblLineups)
- `designs` — Individual designs (from headcase.tblDesigns)
- `products` — Unified: design × device × product_type (the sellable item)
- `marketplace_listings` — Per-channel listing state (Amazon, Walmart, Shopify, etc.)

### New Tables for PULSE v2
```sql
-- EAN/UPC registry for marketplace listings
CREATE TABLE ean_registry (
    id SERIAL PRIMARY KEY,
    ean TEXT UNIQUE NOT NULL,
    gtin TEXT, -- 14-digit (leading zero + EAN)
    assigned_to_product_id UUID REFERENCES products(id),
    source TEXT, -- 'walmart_import', 'target_import', 'pool', 'manual'
    assigned_at TIMESTAMPTZ DEFAULT NOW()
);

-- Publish queue — items approved for push
CREATE TABLE publish_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id),
    target_channel TEXT NOT NULL, -- 'shopify', 'walmart', 'target', 'onbuy', 'kaufland'
    generated_title TEXT,
    generated_description TEXT,
    price NUMERIC(10,2),
    ean TEXT,
    image_url TEXT,
    status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'pushed', 'live', 'error'
    approved_by TEXT,
    approved_at TIMESTAMPTZ,
    pushed_at TIMESTAMPTZ,
    shopify_product_id BIGINT,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Channel connectors config
CREATE TABLE channel_connectors (
    id SERIAL PRIMARY KEY,
    channel TEXT UNIQUE NOT NULL,
    connector_type TEXT, -- 'cedcommerce', 'codisto', 'native', 'manual'
    config JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMPTZ
);
```

### Key View: Marketplace Gaps
```sql
CREATE VIEW v_marketplace_gaps AS
SELECT
    p.id as product_id,
    p.sku_fragment,
    d.name as design_name,
    d.code as design_code,
    l.name as lineup_name,
    pt.code as product_type_code,
    pt.description as product_type_name,
    dev.code as device_code,
    dev.name as device_name,
    -- Channel presence
    MAX(CASE WHEN ml.marketplace = 'amazon_us' THEN 1 ELSE 0 END) as on_amazon,
    MAX(CASE WHEN ml.marketplace = 'walmart_us' THEN 1 ELSE 0 END) as on_walmart,
    MAX(CASE WHEN ml.marketplace = 'shopify' THEN 1 ELSE 0 END) as on_shopify,
    MAX(CASE WHEN ml.marketplace = 'target_us' THEN 1 ELSE 0 END) as on_target,
    -- Gap count
    4 - (
        MAX(CASE WHEN ml.marketplace = 'amazon_us' THEN 1 ELSE 0 END) +
        MAX(CASE WHEN ml.marketplace = 'walmart_us' THEN 1 ELSE 0 END) +
        MAX(CASE WHEN ml.marketplace = 'shopify' THEN 1 ELSE 0 END) +
        MAX(CASE WHEN ml.marketplace = 'target_us' THEN 1 ELSE 0 END)
    ) as channel_gaps
FROM products p
JOIN designs d ON p.design_id = d.id
JOIN lineups l ON d.lineup_id = l.id
JOIN product_types pt ON p.product_type_id = pt.id
JOIN devices dev ON p.device_id = dev.id
LEFT JOIN marketplace_listings ml ON p.id = ml.product_id
GROUP BY p.id, p.sku_fragment, d.name, d.code, l.name, pt.code, pt.description, dev.code, dev.name;
```

## Title Generation Rules

### Amazon (Brand Registry compliant)
`Head Case Designs Officially Licensed {brand} {design_group} {product_type} Compatible with {device}`

### Shopify / DTC
`{brand} {product_type} - {design_group} | {device}`

### Walmart / Target+
`{brand} {design_group} {product_type} for {device} - Officially Licensed`

## Listing Push Flow

1. **Gap Analysis** runs nightly (or on-demand) → populates `v_marketplace_gaps`
2. **PULSE UI** shows gaps sorted by opportunity score
3. **User approves** items → moves to `publish_queue` with status `approved`
4. **Push to Shopify** → creates product in Shopify store → saves `shopify_product_id`
5. **Connectors sync** → CedCommerce/Codisto picks up Shopify products → pushes to Walmart/Target/OnBuy
6. **Status tracking** → PULSE polls connector status → updates `publish_queue` to `live` or `error`

## Shopify Connector Research Needed
| Connector | Channels | Pricing | Notes |
|-----------|----------|---------|-------|
| CedCommerce | Walmart, OnBuy, Kaufland | $19-99/mo | Most marketplace coverage |
| Codisto | Walmart, eBay, Amazon | $29-299/mo | Strong Walmart integration |
| LitCommerce | Walmart, eBay, Etsy, TikTok | $29-89/mo | Multi-channel |
| Native Shopify | Target+ (Marketplace Connect) | Free | Already connected |

**Decision needed from Cem:** Which connector to use for Walmart. CedCommerce is the broadest.

## Priority Metrics
- **Opportunity Score** = `(90d_revenue × velocity_ratio × channel_gaps) / listed_channel_count`
- **Velocity Ratio** = `2mo_revenue / (6mo_revenue / 3)` — values >1.0 = accelerating
- Revenue thresholds: Tier 1 (>$10K/90d), Tier 2 ($1-10K), Tier 3 (<$1K)

## Build Plan
| Phase | What | ETA | Owner |
|-------|------|-----|-------|
| 1 | Supabase tables (DDL) + BQ→Supabase ETL | Day 1 (blocked: DB password) | Ava |
| 2 | Gap analysis view + opportunity scoring | Day 2 | Ava |
| 3 | PULSE UI — Screen 1 (Gap Report) | Day 3-4 | Forge (Codex) |
| 4 | Title generation functions | Day 4 | Ava + Echo |
| 5 | PULSE UI — Screen 2 (Action Queue) | Day 5-6 | Forge |
| 6 | Shopify API integration (create products) | Day 7-8 | Forge + Spark |
| 7 | PULSE UI — Screen 3 (Publish Dashboard) | Day 9 | Forge |
| 8 | Connector setup (Walmart via Shopify) | Day 10 | Cem + Ava |

**Total: 10 working days from DB password → Walmart listings live.**

## Success Metrics
- 750 Walmart gaps filled within 30 days of launch
- $750K annualized opportunity captured (based on gap analysis)
- Time-to-list: <5 minutes per product (vs current manual process)
- Zero manual marketplace API work — all through Shopify connectors

---
*Replaces: PULSE_SCOPE_V3.md (analytics dashboard version)*
*Architecture: Shopify-hub (Cem directive 2026-03-10)*
