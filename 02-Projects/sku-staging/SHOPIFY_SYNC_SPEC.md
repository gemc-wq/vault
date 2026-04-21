# Shopify Sync Spec: BigCommerce Champions → Shopify → Walmart

> **Owner:** Ava | **Created:** 2026-03-14 | **Status:** Draft (ready to execute once UPCs resolved)
> **Dependency:** UPC Acquisition Plan must complete first
> **Goal:** Load ~200 PULSE champion designs into GoHeadCase Shopify as draft products, then publish to push via connector to Walmart

---

## Scope

| Metric | Value |
|--------|-------|
| Champion designs | 200 (193 in BC, 7 missing) |
| Total BC SKUs across champions | 239,618 |
| Target: top devices per design | ~20-50 (top-selling, not all 1,200+) |
| Estimated Shopify products | 200 (1 product per design, variants = devices) |
| Estimated Shopify variants | 4,000-10,000 |
| Revenue represented | $1.43M / 90 days |

### Device Filtering Strategy

Loading ALL 239K SKUs is impractical and unnecessary. Strategy:
1. **Top devices by revenue** — for each champion design, include only device variants that generated revenue in the last 90 days
2. **Minimum threshold** — device variant must have ≥$50 revenue in 90d to be included
3. **Always include** — iPhone 16 series, iPhone 15 series, Samsung Galaxy S25/S24 (current generation)
4. **Fallback** — if a design has <5 qualifying variants, include top 20 by historical volume

---

## Data Flow

```
Step 1: Extract champion product data from BigCommerce API
        → GET /v3/catalog/products?sku:in=HTPCR-{device}-{design}
        → Fields: title, description, images[], variants[], price, gtin
        
Step 2: Enrich with PULSE velocity data
        → Join on design_code from BQ/Supabase
        → Add tags: velocity tier, license, revenue rank
        
Step 3: Filter devices using revenue threshold
        → Keep only variants with 90d revenue ≥ $50
        → Ensure current-gen devices always included
        
Step 4: Map to Shopify product schema
        → See field mapping below
        
Step 5: Create products via Shopify Admin API
        → POST /admin/api/2024-01/products.json
        → Status: DRAFT (review before publishing)
        
Step 6: Upload images
        → POST /admin/api/2024-01/products/{id}/images.json
        → Use BC image URLs (Shopify will cache/re-host)
        
Step 7: Verify & publish
        → Manual review in Shopify admin
        → Publish → auto-syncs to Walmart via connector
```

## Field Mapping: BigCommerce → Shopify

| Shopify Field | Source | Notes |
|---------------|--------|-------|
| `title` | BC `name` | May need reformatting for Walmart SEO |
| `body_html` | BC `description` | Clean up any BC-specific markup |
| `vendor` | "Head Case Designs" | Static |
| `product_type` | "Phone Case" | Static for HTPCR |
| `tags` | Generated | `pulse-champion`, `velocity:{tier}`, `license:{brand}`, `rank:{1-200}` |
| `status` | "draft" | Always draft initially |
| `variants[].sku` | BC `sku` | Keep identical (HTPCR-{device}-{design}-{finish}) |
| `variants[].barcode` | BC `gtin` OR Zero EAN | Critical — Walmart requires this |
| `variants[].price` | BC `price` | Review for Walmart competitiveness |
| `variants[].option1` | Device name | Parsed from SKU device code |
| `variants[].option2` | Finish/Material | e.g., Soft Gel, Hard Back |
| `variants[].inventory_quantity` | 999 | POD model — always in stock |
| `variants[].inventory_management` | null | Don't track inventory (POD) |
| `variants[].fulfillment_service` | "manual" | Veeqo handles fulfillment |
| `images[].src` | BC image URLs | Shopify re-hosts automatically |
| `images[].alt` | Generated | `{design_name} {device_name} Phone Case` |

## Tagging Convention

```
pulse-champion          — all champion products
velocity:surging        — 30d > 90d average
velocity:accelerating   — 30d growing but < surging
rank:1                  — revenue rank (1 = highest)
license:peanuts         — license/brand family
region:us               — primary selling region
region:uk               — also sells in UK
region:de               — also sells in DE
missing-from:walmart    — gap indicator
```

## Implementation Options

### Option A: Script (Recommended)
Python script using BigCommerce + Shopify REST APIs:
1. Fetch champion products from BC API (paginated, filtered by SKU prefix)
2. Join with PULSE data from BQ/Supabase
3. Transform to Shopify schema
4. Create via Shopify Admin API
5. Log results to `projects/sku-staging/sync-log.json`

**Pros:** Full control, auditable, repeatable, handles edge cases
**Cons:** Need Shopify Admin API token (write access)

### Option B: CSV Import
Generate Shopify-format CSV, upload via Shopify admin UI:
1. Same data extraction as Option A
2. Output as Shopify CSV format
3. Manual upload in Shopify admin → Products → Import

**Pros:** No API token needed, visual review before import
**Cons:** Manual step, image handling is clunky, variant limits per CSV

### Recommendation: **Option A** for scale, with CSV as fallback for initial test batch of 10 designs.

## Test Batch (First 10)

Start with top 10 champions by revenue to validate the pipeline:

| # | Design | Revenue (90d) | BC SKUs | License |
|---|--------|---------------|---------|---------|
| 1 | NARUICO | $57,835 | 1,034 | Naruto |
| 2 | LFCLVBRD | $54,091 | 2,082 | Liverpool FC |
| 3 | AFCLOGOS | $42,601 | 1,072 | Arsenal FC |
| 4 | PNUTCHA | $39,895 | 1,753 | Peanuts |
| 5 | PNUTBOA | $27,139 | 1,257 | Peanuts |
| 6 | FCBCRE | $25,081 | 1,323 | FC Barcelona |
| 7 | ADVEGRA | $22,970 | 1,630 | Adventure Time |
| 8 | PNUTCBR | $22,746 | 593 | Peanuts |
| 9 | NARUCHA | $21,713 | 752 | Naruto |
| 10 | MCBDKIT25 | $21,100 | 1,078 | Man City |

**4 of these 10 already have UPCs** (NARUICO, PNUTBOA, PNUTCBR, NARUCHA) — can be pushed to Shopify immediately as proof of concept.

## Pre-Requisites Checklist

- [ ] UPC/EAN acquisition complete (or at least for test batch)
- [ ] Shopify Admin API token (write access to GoHeadCase store)
- [ ] Confirm Shopify→Walmart connector is still active
- [ ] Confirm pricing strategy (BC prices vs. Walmart-specific pricing)
- [ ] Image quality review (BC images may need resizing for Walmart specs)
- [ ] License check — all 10 test designs cleared for Walmart specifically?

## Walmart-Specific Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| UPC/EAN barcode | 🟡 Partial | 27/200 have EANs, rest pending |
| Product images ≥ 1000x1000px | ❓ Check BC | Walmart min spec |
| Category mapping | ❓ TBD | Cell Phone Cases → Electronics > Cell Phones & Accessories |
| Brand registration | ✅ Assumed | Head Case Designs already on Walmart (95K SKUs) |
| Shipping template | ✅ | Via Veeqo |
| Returns policy | ✅ | Walmart standard |

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Walmart rejects without UPC | 🔴 High | UPC acquisition plan in progress |
| Shopify→Walmart connector lag | 🟡 Med | Test with 1 product first, monitor sync time |
| Image quality too low | 🟡 Med | Check BC image dimensions before bulk push |
| Duplicate listings on Walmart | 🔴 High | Check existing 95K Walmart SKUs for overlap before creating |
| License restrictions per marketplace | 🟡 Med | Verify license agreements allow Walmart distribution |
| Price undercutting own Amazon listings | 🟡 Med | Price parity check before publishing |

## Duplicate Prevention

**Critical:** Ecell already has 95K listings on Walmart. Before creating any Shopify product:
1. Query `walmart_active_listings` in BQ for matching design codes
2. If already listed on Walmart → skip (tag as `already-on-walmart`)
3. Only create products that are genuine gaps

---

## Timeline (estimated, starts after UPC resolution)

| Day | Action |
|-----|--------|
| 1 | Write BC→Shopify sync script, test with 4 UPC-ready designs |
| 2 | Verify 4 products appear on Walmart, check listing quality |
| 3 | Fix any issues, run test batch of 10 |
| 4-5 | Scale to full 200 champions (with UPCs) |
| 6-7 | Monitor Walmart listing health, fix rejections |

---

*Drafted by Ava during heartbeat 2026-03-14 06:05 EST*
