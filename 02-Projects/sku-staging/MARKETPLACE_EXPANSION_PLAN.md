# Marketplace Expansion Pipeline — Project Plan

> **Owner:** Ava | **Created:** 2026-03-15 | **Updated:** 2026-03-15 (scope expanded per Cem)
> **Status:** Active
> **Goal:** Curate GoHeadCase Shopify catalog (~200K SKUs from 1.9M BC) → feed marketplace connectors (Walmart, OnBuy, Kaufland) + headless goheadcase.com + microsites

## ⚠️ Scope Change (Mar 15)
- **NOT just phone cases** — includes ALL product groups: HTPCR, HB401, HLBWH, HB6, HB7, desk mats (HDM), gaming skins (H89)
- **NOT just Walmart** — this IS the GoHeadCase Shopify catalog curation
- **SEO + content rewrite BEFORE any Shopify upload** — no raw BC data
- **Conversion data required** — sessions + conversion rates inform the curation, not just velocity
- **GoHeadCase headless site feeds from this Shopify** → anime microsites, sports microsites, marketplace connectors
- **Target: <200K SKUs** — best sellers + best opportunity from 1.9M BC catalog

---

## Executive Summary

Three-phase expansion using PULSE velocity data + BigCommerce product catalog + Amazon conversion data to identify, stage, and push champion phone case SKUs to new marketplaces. Each marketplace gets a fresh product-group-filtered champion analysis — no cross-product contamination (desk mats ≠ phone cases).

---

## Phase 1: Walmart US (NOW — Target: March 2026)

### 1A. Gap Analysis (HTPCR-only)
- [x] PULSE champions extracted (200 designs, US buyers, 90d)
- [ ] **Fix: Filter by product group** — run champions per product type (HTPCR, HB401, HLBWH, HB6, HB7) separately
- [ ] Cross-reference against existing Walmart listings (via Veeqo/Active Listings)
- [ ] Identify net-new SKUs to list (champion designs NOT on Walmart)
- **Output:** Ranked gap-fill list per product type

### 1B. Product Data Enrichment
- [x] BigCommerce API connected — titles, descriptions, images, custom fields
- [x] Target master list EAN lookup — 35,541 barcodes
- [ ] **Content Writing Layer (Echo agent, Sonnet 4.6):**
  - Take raw BC description + Amazon title + product specs
  - Generate: Shopify-optimized description, Walmart-optimized title, bullet points
  - Batch process: 50 designs per run
  - Clean up multi-language HTML blocks (BC has EN/DE/FR/IT crammed together)
- [ ] **SEO Title Standardization Skill:**
  - Format: `{License Name} {Design Name} Official {Case Type} for {Full Device Name} — {Key Features}`
  - Example: "Naruto Shippuden Akatsuki Official Soft Gel Case for iPhone 17 Pro Max — Military Grade Protection"
  - Must include: license, design, device (full name not code), case type, differentiator
- [ ] **Image Quality Review (Sven agent):**
  - Review hero images from BigCommerce CDN
  - Flag low-quality, wrong device mockup, or outdated images
  - Priority: top 50 champions get image QA before upload
  - Note: Shopify downloads images once from URL at import — does NOT auto-refresh
  - Therefore: fix images BEFORE CSV import, not after

### 1C. Shopify Staging
- [x] Product architecture decided: Product = 1 design × 1 device, Variant = case type
- [x] 5 case types: HTPCR ($17.95), HB401 ($19.95), HLBWH ($24.95), HB6 ($24.95), HB7 ($24.95)
- [x] Test CSV generated (10 designs, 100 products) — sent to Cem for import test
- [x] Full CSV generated (50 designs, 750 products)
- [ ] Cem imports test CSV to Shopify — validate format
- [ ] Get Shopify Admin API token for automated uploads
- [ ] Integrate content-rewritten descriptions before final import
- [ ] Integrate QA'd images before final import

### 1D. Walmart Push
- [ ] Install Shopify Marketplace Connect app (free, $99/mo cap)
- [ ] Map Shopify products to Walmart categories
- [ ] Publish draft products → connector syncs to Walmart
- [ ] Verify listings appear on Walmart (24-48h)
- [ ] Monitor: orders flowing through Veeqo?

### 1E. Data Dependencies
- [ ] **Latest US All Listings Report** — Cem downloading (fixes stale ASIN→SKU bridge)
- [ ] PH EAN database query — fills remaining 42% of champions without barcodes
- [ ] UPC/GTIN mandatory for Walmart — 58% covered, need 100%

---

## Phase 2: OnBuy UK (Next — Target: April 2026)

### Requirements
- **Greenfield:** Zero existing listings → fresh top-seller matrix
- **Product group filter:** Phone cases only (HTPCR, HB401, HLBWH)
- **Region:** UK buyers only (from BQ `Buyer_Country = 'United Kingdom'`)
- **EAN coverage:** Target master list should cover UK products well (EAN-13 format is native)
- **Content:** UK-English descriptions (no "colors" → "colours", etc.)
- **Pricing:** GBP pricing from BigCommerce (already has UK descriptions)
- **Fulfillment:** UK warehouse (Veeqo UK instance)

### Steps
1. Run PULSE UK-only champions (phone cases)
2. Generate OnBuy product feed (OnBuy has its own CSV format)
3. Content pass: UK-English optimization
4. Upload via OnBuy Seller Portal or API
5. Connect to Veeqo UK for order routing

---

## Phase 3: Kaufland DE (Following — Target: May 2026)

### Requirements
- **Greenfield:** Zero existing listings
- **Product group filter:** Phone cases only
- **Region:** DE/EU buyers
- **Content:** German-language descriptions (BigCommerce already has DE descriptions in custom fields)
- **EAN:** Required (same Target master list)
- **Pricing:** EUR pricing
- **Fulfillment:** UK warehouse (ships to EU)

### Steps
1. Run PULSE EU-only champions (phone cases)
2. Generate Kaufland product feed
3. Content pass: German description optimization
4. Upload via Kaufland Seller Portal
5. Order routing: Veeqo UK or manual

---

## Amazon Conversion Intelligence Layer

### Problem
PULSE currently uses **order velocity** only. We need to add **traffic and conversion data** to identify:
- **Accelerating products:** High sessions + improving conversion = rising stars (e.g., NBA with new images)
- **Underperforming listings:** High sessions + low conversion = fix the listing
- **Hidden gems:** Low sessions + high conversion = needs more visibility/PPC

### Data Sources
| Source | Key | Rows | Status |
|--------|-----|------|--------|
| Amazon Business Report (Sessions) | ASIN | 457K loaded | ✅ In Supabase |
| Amazon All Listings Report (US) | SKU→ASIN bridge | 3.44M | ⚠️ Stale (Mar 5) — Cem downloading latest |
| Amazon All Listings Report (UK) | SKU→ASIN bridge | 9.4GB | ⚠️ On GDrive, not processed |
| Amazon All Listings Report (DE) | SKU→ASIN bridge | TBD | ❌ Not downloaded |
| BQ Orders (PULSE velocity) | Custom_Label (SKU) | 320K+ | ✅ Syncing nightly |

### Architecture
```
Amazon Sessions Report (ASIN-keyed)
    ↓ ASIN→SKU bridge (from All Listings)
Supabase `amazon_conversion_data` (SKU-keyed)
    ↓ join on design_code + device_code
PULSE velocity data (orders table)
    ↓ combined view
Conversion-Velocity Matrix
    → Quadrant: Stars / Cash Cows / Question Marks / Dogs
```

### Key Constraint
- Sessions report is **ASIN-keyed**, not SKU-keyed
- One ASIN can map to multiple SKUs (variations)
- Bridge accuracy: US 95%+, UK/DE 80-85% (need regional All Listings files for 95%+)
- NBA revised images = recent uploads → short lookback may not capture lift yet
- Use longer baseline (6-12mo) for "before" picture, 30-day rolling for "after"

### Deliverables
- [ ] Load latest US All Listings Report (when Cem provides)
- [ ] Refresh ASIN→SKU bridge
- [ ] Build conversion-velocity view in Supabase
- [ ] Add "Conversion" tab to PULSE dashboard
- [ ] Quadrant analysis: Stars (high velocity + high conversion) → prioritize for Walmart

---

## Agent Assignments

| Agent | Task | Model | Priority |
|-------|------|-------|----------|
| **Ava** | Project management, gap analysis queries, CSV generation | Opus | Lead |
| **Echo** | Content rewriting — Shopify/Walmart descriptions | Sonnet 4.6 | P1 |
| **Sven** | Image QA, hero image review, mockup quality | Gemini 3.1 Pro | P1 |
| **Bolt** | SEO keyword research, title optimization research | Flash | P2 |
| **Pixel** | Data processing — EAN matching, conversion data ETL | Flash | P1 |
| **Forge/Spark** | PULSE dashboard updates (conversion tab) | Codex GPT-5.3 | P2 |

---

## Key Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Walmart listings (phone cases) | ~existing (unknown) | +750 champions |
| OnBuy UK listings | 0 | Top 200 UK champions |
| Kaufland DE listings | 0 | Top 100 DE champions |
| EAN coverage (US champions) | 58% | 95%+ |
| Content quality (rewritten) | 0% | 100% before upload |
| Image QA'd | 0% | Top 50 before upload |

---

## Timeline

| Week | Milestone |
|------|-----------|
| **Mar 15-21** | Fix product group filter, content pipeline spec, Shopify test import, SEO skill |
| **Mar 22-28** | Content rewriting batch (50 designs), image QA, full Shopify import |
| **Mar 29-Apr 4** | Walmart connector setup, first listings live, conversion tab in PULSE |
| **Apr 5-18** | OnBuy UK champion analysis + listing prep |
| **Apr 19-30** | OnBuy UK launch, Kaufland DE analysis begins |
| **May** | Kaufland DE launch |

---

*This plan implements the Shopify-hub architecture: PULSE identifies gaps → content pipeline enriches → Shopify stages → connectors push to Walmart/OnBuy/Kaufland.*
*Approved by Cem: Mar 15, 2026*
