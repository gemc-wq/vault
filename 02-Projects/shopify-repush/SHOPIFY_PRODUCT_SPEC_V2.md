# Shopify Product Re-Push Spec v2
**Date:** 2026-03-31 | **Owner:** Ava (spec) + Forge (build)
**Store:** yabfxs-zd.myshopify.com | **Token:** [REDACTED_SHOPIFY_ADMIN_TOKEN]

---

## Architecture (Cem-approved, Mar 14)
- **Product** = 1 design × 1 device
- **Variant** = case type (HTPCR / HB401 / HLBWH / HB6CR / HB7BK)
- **Pricing:** HTPCR $19.95, HB401 $19.95, HLBWH $24.95, HB6CR $24.95, HB7BK $24.95

## Data Sources
1. **Champions list:** Supabase orders (90d, combined back case revenue) — 590 designs
2. **Product data:** BigCommerce API (store otle45p56l) — titles, descriptions, images
3. **EANs:** EAN lookup engine (480K mappings) at `projects/sku-staging/output/`
4. **Images:** S3 CDN primary + BC CDN fallback (see Image Rules below)
5. **Device codes:** Jessie's Device Codes spreadsheet (8 sheets, all product types)

## Image Source Rules (confirmed by Jessie Morales, Mar 31)

### S3 CDN (primary)
- **Base URL:** `https://elcellonline.com/atg/{DESIGN}/{VARIANT}/{CASE_PREFIX}-{DEVICE}-{POSITION}.jpg`
- **Case prefixes:** TP-CR, HY-BK (HB401→B4-01), B1-BK, LB-WH, HC-CR, B6-CR, B7-BK
- **Positions:** Old style = position 1 only. New style (NBA etc.) = positions 1-6
- **Device codes:** Same as SKU codes (confirmed)
- **Variant folder:** From design variant code in SKU (NOT always first 3 chars — lookup required)
- **Coverage:** TP-CR widest. 2,132 device codes mapped in Coverage sheet.

### Case Prefix → Product Type mapping
| Product Type | Case Prefix (S3) | Case Prefix (SKU) |
|---|---|---|
| HTPCR | TP-CR | HTPCR |
| HB401 | B4-01 | HB401 |
| HC | HC-CR | HC |
| HLBWH | LB-WH | HLBWH |
| HB6CR | B6-CR | HB6CR |
| HB7BK | B7-BK | HB7BK |
| HB1BK | B1-BK | HB1BK |

### Variant Code Lookup (from Jessie's spreadsheet)
Located at: `projects/fulfillment-portal/evri-docs/S3_Image_URL_.xlsx` → sheet "Variant Naming Rules"
47 variants mapped. Examples:
- AKA = Akatsuki, NUZ = Naruto Uzumaki, SAS = Sasuke
- Leather variants have L prefix: LAKA, LNUZ, LSAS

### BigCommerce CDN (fallback)
- API: `https://api.bigcommerce.com/stores/otle45p56l/v3/catalog/products?include=images`
- Token: `9n6n0jq99ms69sda4d8hhg57p88c05i`
- URL format: `cdn11.bigcommerce.com/s-otle45p56l/products/{id}/images/{img_id}/{filename}`
- 1.97M products with images available

### Image Upload Strategy (CRITICAL — learned from March failure)
**Images MUST be uploaded to Shopify, not linked by URL.**
- Target Plus syncs images FROM Shopify — external URLs don't render
- Codisto/Marketplace Connect reads Shopify images for Walmart
- Process: Download from S3/BC → upload to Shopify product via API → Shopify hosts

## Shopify Product Fields (for Codisto mapping)

### Required fields per product:
| Field | Source | Example |
|---|---|---|
| title | SEO template | "Naruto Shippuden Akatsuki Soft Gel Case for iPhone 17 Pro Max" |
| body_html | SEO content framework | Generated from design + device + product type templates |
| vendor | Fixed | "Head Case Designs" |
| product_type | Fixed | "Phone Case" |
| tags | Generated | "lineup:NARUICO, device:IPH17PMAX, pulse-champion, brand:NARU, type:HTPCR" |
| barcode (per variant) | EAN lookup | 13-digit, no dashes |
| sku (per variant) | Standard format | "HTPCR-IPH17PMAX-NARUICO-AKA" |
| price (per variant) | Tiered | $19.95 or $24.95 |
| weight | Per product type | HTPCR: 0.1kg, HB401: 0.15kg, HLBWH: 0.2kg |
| images | S3/BC CDN → upload | Min 1 hero, max 6 |

### Metafields for Codisto attribute mapping:
| Metafield | Namespace | Key | Example |
|---|---|---|---|
| Brand/License | custom | brand_name | "Naruto Shippuden" |
| Compatible Device | custom | compatible_device | "Apple iPhone 17 Pro Max" |
| Case Type | custom | case_type | "Hybrid MagSafe Case" |
| Design Name | custom | design_name | "Akatsuki" |

### Package dimensions (per product type):
| Product Type | Length (cm) | Width (cm) | Height (cm) | Weight (kg) |
|---|---|---|---|---|
| HTPCR | 19 | 12 | 2 | 0.10 |
| HB401 | 19 | 12 | 2.5 | 0.15 |
| HLBWH | 20 | 14 | 3 | 0.20 |
| HB6CR | 19 | 12 | 2 | 0.10 |
| HB7BK | 19 | 12 | 2 | 0.10 |

## Push Process

### Phase 1: Top 50 Champions (validation batch)
1. Pull top 50 designs from PULSE champion list
2. For each design × top 10 devices:
   a. Check S3 CDN for images (HTTP HEAD, positions 1-6)
   b. Fallback to BC API images if S3 404s
   c. Look up EAN from lookup table
   d. Generate title/description from SEO template
   e. Create Shopify product via API
   f. Upload images to Shopify (download → POST to product images endpoint)
   g. Set metafields for Codisto
3. Validate: all products visible in Shopify admin, images rendering, barcodes present
4. Test Codisto sync to Target Plus (1 product)

### Phase 2: Full champion push (500 products)
After Phase 1 validated, expand to full 590 champion designs × priority devices.

### Phase 3: Ongoing automation
Saturday cron detects new champion designs → auto-push to Shopify.
