# SKU Staging Pipeline: PULSE Champions → Shopify → Walmart

> **Owner:** Ava | **Created:** 2026-03-12 | **Status:** Planning
> **Goal:** Get top-performing HTPCR designs from PULSE onto Shopify, then push to Walmart

---

## Pipeline Overview

```
PULSE Champions (BQ velocity data)
    ↓ ranked child designs by revenue
BigCommerce API (product data, GTINs, images)
    ↓ match champions → pull full product records
EAN/UPC Check
    ↓ flag missing barcodes (Walmart requires them)
Shopify CSV Generation
    ↓ formatted for Shopify import
Shopify Backend Upload
    ↓ via Shopify Admin API or CSV import
Walmart Push
    ↓ via Shopify→Walmart connector (already configured)
```

## Phase 1: Data Collection & Matching

### 1A. PULSE Champion Export
- **Source:** PULSE Champions tab (`pulse-dashboard-v2.vercel.app/?tab=champions`)
- **Filter:** Product type = HTPCR (phone cases)
- **Output:** Ranked list of child design codes + device codes + 90-day revenue
- **Count:** ~106 "champion designs" from outside top 50 lineups (per Mar 10 analysis), plus top-50 lineup designs
- **Format:** CSV with columns: `design_code`, `device_code`, `lineup_label`, `revenue_90d`, `velocity_category`

### 1B. BigCommerce Product Lookup
- **Source:** BigCommerce API (preferred) OR 50GB TSV export (fallback)
- **API approach (preferred):** Query by SKU pattern `HTPCR-{device}-{design}*` — pull only champions
- **TSV fallback:** Parse 50GB file, extract HTPCR rows, build lookup table
- **Fields needed:** SKU, title, description, GTIN (EAN/UPC), images, price, categories, options
- **API credentials:** ⚠️ NEEDED FROM CEM — store hash + API token (read-only Products scope)

### 1C. EAN/UPC Coverage Check
- **Requirement:** Walmart requires UPC or EAN for every listing
- **Sources for barcodes:**
  1. BigCommerce `gtin` field (primary)
  2. Amazon Active Listings `external-id` field (3.44M rows, backup)
- **Output:** Coverage report — X% have barcodes, Y champions missing barcodes
- **Action for missing:** Flag for manual barcode assignment or GS1 lookup

## Phase 2: Shopify Staging

### 2A. Generate Shopify Import CSV
- Map BC fields → Shopify CSV format:
  - `Handle`, `Title`, `Body (HTML)`, `Vendor`, `Type`, `Tags`
  - `Variant SKU`, `Variant Barcode`, `Variant Price`
  - `Image Src`, `Image Alt Text`
- Add tags: `pulse-champion`, `velocity:{surging|accelerating}`, license name
- Set status: `draft` (review before publishing)

### 2B. Upload to Shopify
- **Method:** Shopify Admin API bulk import or CSV upload
- **Store:** GoHeadCase Shopify (already connected to Veeqo US)
- **Status:** Draft until reviewed

## Phase 3: Walmart Push

### 3A. Publish & Push
- Review drafts in Shopify admin
- Publish approved items
- Shopify→Walmart connector syncs automatically
- Verify listings appear on Walmart within 24-48h

## Data Sources

| Source | Size | Key Fields | Status |
|--------|------|------------|--------|
| BQ orders (PULSE) | 319K orders | velocity, revenue, design_code | ✅ Live |
| BigCommerce API | ~1.89M SKUs | title, GTIN, images, price | ⚠️ Need API creds |
| BigCommerce TSV export | 50GB, 1.89M SKUs | gtin, title, images | ✅ On disk (may be stale) |
| Amazon Active Listings US | 3.44M rows | UPC, ASIN, SKU | ✅ On disk |
| Supabase unified products | 90K products | device, design, lineup | ✅ Live |

## Blockers
1. **BigCommerce API credentials** — need store hash + API token from Cem
2. **Shopify Admin API access** — need to confirm we have write access (not just storefront)
3. **EAN gaps** — unknown % of champions missing barcodes until we check

## Open Questions
- How many HTPCR champions total? (estimated 200-500 SKUs)
- Do we want ALL devices for each champion design, or only top-selling devices?
- Price mapping: use BC prices or reprice for Walmart?
- Image quality: BC images good enough or need regeneration?

---

*This plan implements the Shopify-hub architecture confirmed Mar 10: PULSE identifies gaps → generates Shopify-ready data → connectors push to Walmart/Target+/OnBuy/Kaufland.*
