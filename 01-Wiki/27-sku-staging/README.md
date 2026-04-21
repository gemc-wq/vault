# SKU Staging Pipeline
> **Owner:** Ava | **Status:** Active | **Updated:** 2026-03-18

## Purpose
Curate the GoHeadCase Shopify catalog (~200K SKUs from 1.9M BigCommerce) and stage products for marketplace expansion (Walmart, OnBuy, Kaufland).

## Architecture
- **Product = 1 design** (for Walmart: device + case type as variants)
- **Product = 1 design × 1 device** (for Shopify/GoHeadCase: case type as variant)
- **Content generated from SKU components** — not stored per-SKU

## Key Components
- **PULSE elbow analysis** → identifies optimal design × device matrix
- **BigCommerce API** → product data, images, custom fields (store: otle45p56l)
- **EAN database** → 480K mappings (Target master list + PH database + auto-assigned)
- **SEO content framework** → templated titles, descriptions, bullets per case type
- **Walmart Lister tool** → generates Shopify CSV or Walmart multi-variant CSV

## EAN Management
- Local SQLite: `data/local_listings.db` → `ean_database` + `ean_assignments` tables
- 600K total records, 473K assigned, 44K valid unassigned available
- Auto-assignment engine assigns from unassigned pool for new SKUs
- Combined lookup: `data/ean/combined_ean_lookup.json` (480K mappings)

## Product Specs (corrected Mar 15)
- HTPCR: TPU bumper + PC hard back + integrated MagSafe magnetic ring ($17.95)
- HB401: TPU bumper + PC hard back + integrated MagSafe magnetic ring ($19.95)
- HLBWH: Leather Wallet Case ($24.95)
- HB6CR: Clear MagSafe Case ($24.95)
- HB7BK: Black MagSafe Case ($24.95)
- ⚠️ NOT "soft gel" — corrected from original BigCommerce descriptions

## Key Files
- `wiki/SKU_PARSING_RULES.md` — definitive SKU rules
- `projects/sku-staging/SEO_CONTENT_FRAMEWORK.md` — content templates
- `projects/sku-staging/MARKETPLACE_EXPANSION_PLAN.md` — full rollout plan
- `projects/walmart-lister/walmart_lister.py` — CSV generator
- `research/competitor-copy-analysis.md` — Casetify/ESR feature comparison
- `research/casetify-shopify-structure.md` — product architecture research
