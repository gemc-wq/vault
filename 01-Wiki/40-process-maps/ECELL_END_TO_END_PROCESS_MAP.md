# Ecell Global — End-to-End Process Map
**Version:** 1.0 | **Date:** 2026-04-07
**Owner:** Ava (Strategy)
**Status:** CURRENT — incorporating all active projects

---

## Overview

This is the canonical process map from **license signing → design creation → listing → sale → fulfillment → finance**. Every active project plugs into one of these stages. One Piece is the pilot that will prove the full loop.

---

## THE FULL LOOP

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ECELL GLOBAL PROCESS                            │
│                                                                         │
│  LICENSE          CREATIVE         LISTING PREP      GO LIVE            │
│  ─────────        ────────         ────────────      ───────            │
│  Contract    →    Design      →    SKU + Content →   Marketplaces  →   │
│  Signed           Created          Ready              Live               │
│                                                                         │
│  FULFILLMENT      FINANCE          INTELLIGENCE                         │
│  ───────────      ───────          ────────────                         │
│  Order       →    Revenue    →     PULSE +                              │
│  Dispatched        Recorded         Hermes                              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## STAGE 1: LICENSE ONBOARDING
**App:** `ecell.app/licenses` (to build — Harry)
**Supabase table:** `licenses` (Jay Mark creating)

```
Cem signs license contract
        ↓
Human enters in ecell.app/licenses:
  • License name (e.g. One Piece)
  • Licensor (Toei Animation)
  • Design code prefix (ONEP)
  • Royalty % (15%)
  • Territory (US, UK, EU)
  • Expiry date (Mar 2028)
  • Allowed product types (select from list)
  • Upload contract PDF → stored in GDrive Brain/licenses/
        ↓
System auto-creates:
  • SKU prefix registered in database
  • Launch tracker card created
  • Royalty accrual tracker initialised
  • Notification to Sven: "New license — create design brief"
```

**Supabase tables (Jay Mark):**
- `licenses` — master license record
- `license_designs` — design codes registered under each license
- `launch_tasks` — tracker cards per phase

---

## STAGE 2: CREATIVE
**App:** `ecell.app/licenses/[id]` → Creative tab
**Agents:** Sven (brief), PH Creative Team (execution)
**Supabase table:** `license_designs`

```
Creative Director (Sven) reviews license
        ↓
Generates creative brief:
  • Character priority list (top 10)
  • Style guide (hex codes, art direction)
  • Reference images (Casetify teardown, social research)
  • Gamma presentation → shared to Slack #creative
        ↓
PH Creative Team creates designs:
  • PSD/EPS artwork per character
  • Jay Mark uploads to S3: /atg/{DESIGN_CODE}/{VARIANT}/
        ↓
Human enters design codes in ecell.app:
  • Design code: ONEPGR5 (Gear 5 Luffy)
  • Character name: Gear 5 Luffy
  • Variant: e.g. BLK, WHT, NAT
  • Upload design file path
  • Status: [draft → approved]
        ↓
Cem/Sven approves → status = "approved"
→ Triggers: SKU generation (Stage 3)
```

**Design code format:**
`{LICENSE_PREFIX}{CHARACTER_CODE}` → e.g. ONEPGR5 = One Piece Gear 5

---

## STAGE 3: SKU GENERATION + EAN ASSIGNMENT
**App:** `ecell.app/licenses/[id]` → SKU Generator tab
**Supabase tables:** `license_skus`, `ean_assignments`

```
Design approved
        ↓
System auto-generates SKU matrix:
  For each approved design × product type × device:
  HTPCR-IPH17PMAX-ONEPGR5-BLK
  HTPCR-IPH16PMAX-ONEPGR5-BLK
  HB401-IPH17PMAX-ONEPGR5-BLK
  etc.
        ↓
EAN assignment engine auto-assigns:
  • Pulls from unassigned EAN pool (44K remaining)
  • Writes to ean_assignments table
  • Links EAN → SKU → design_code
        ↓
SKU list exported to CSV
→ Feeds into Stage 4 (ListingForge images) in parallel
→ Feeds into Stage 5 (content generation) in parallel
```

**Priority devices (One Piece launch):**
iPhone 16/17 Pro Max → Samsung S24/S25 Ultra → full range

---

## STAGE 4: LISTING IMAGE CREATION (ListingForge)
**App:** ListingForge pipeline (Mac Studio, scripts/)
**Agent:** Forge/Codex (builder)
**Jig data:** t_jig_devices_full.csv + t_jigs_full.csv (in GDrive)

```
Design file + SKU list
        ↓
ListingForge (Lane 1 — phone cases):
  1. Look up device in t_jig_devices → find jig template
  2. Look up jig template in t_jigs → get canvas dimensions
  3. Composite: design artwork + device frame + jig grid
  4. Output: 1000×1000px listing image per SKU
        ↓
Images uploaded to S3:
  https://elcellonline.com/atg/{DESIGN}/{VARIANT}/{PREFIX}-{DEVICE}-1.jpg
        ↓
Also generate supporting images:
  • Position 2 (secondary angle)
  • Position 1b (with background)
  • Feature shot (staticimages/features/)
        ↓
Image URLs written to license_skus table
→ Ready for Stage 5
```

**Status:** ListingForge Lane 1 POC built and tested. Jig data now available for iPhone 13–17, Samsung S21–S25. Jay Mark to validate modern device rows.

---

## STAGE 5: CONTENT GENERATION
**Agent:** Echo (Sonnet 4.6)
**Source:** SEO Content Framework (wiki/27-sku-staging/)

```
SKU + design_code + product_type + device
        ↓
Echo generates per design (one call per design, replicated across devices):
  • Title: "{License} {Design} Official {Case Type} for {Device} | Military Grade Protection"
    e.g. "One Piece Gear 5 Luffy Official Hybrid MagSafe Case for iPhone 17 Pro Max"
  • Description HTML: hero copy + feature bullets + about the design
  • 5 bullet points (for Amazon/Walmart)
  • SEO meta title + description
  • Tags: license name, character, device, case type
        ↓
Content written to license_skus table
        ↓
QA check (Ava spot-check 10%):
  • No design codes in titles
  • Full brand name used
  • Device name in full (not IPH17PMAX)
  • Inventory set to 9999 in all outputs
```

---

## STAGE 6: LISTING UPLOAD
**App:** Shopify API + Amazon SP-API (via middleware)
**Supabase table:** `license_skus` → status: [staged → live]

```
Content + Images + EANs all ready
        ↓
Shopify upload (GoHeadCase):
  • Bulk CSV generated from license_skus
  • Uploaded via Shopify Admin API
  • Product type, vendor, tags, inventory = 9999
  • Status: published
  • → Auto-flows to Target Plus (Shopify = Target hub)
        ↓
Amazon upload (via middleware API):
  • POST /api/v1/reports/request-and-wait
  • Feed type: JSON_LISTINGS_FEED (requires Product Listing scope — pending)
  • Marketplace: US first, then UK, DE
        ↓
Walmart staging:
  • CSV generated per Walmart format
  • GTIN-14 format (leading zero on EAN-13)
  • Via Codisto/Shopify Marketplace Connect
        ↓
Status updated in license_skus: "live"
→ Notification to Cem: "X SKUs live on Y marketplaces"
```

---

## STAGE 7: PRINT FILE MONITORING
**App:** ecell.app (new tile — Jay Mark building)
**Supabase tables:** Jay Mark's new tables (in progress)

```
Order comes in (via Veeqo/Zero)
        ↓
Print file check:
  • Does IREN/DRECO have the print file for this SKU?
  • If YES → auto-queue for production
  • If NO → flag to PH team to create print file
        ↓
Production tracking:
  • PH team marks print file as created
  • Status: [needed → created → approved → in-production]
        ↓
Integration with IREN (PH):
  • IREN reads from Zero DB for production queue
  • ListingForge images → also used as print file source (same composite)
```

**Status:** Jay Mark creating Supabase tables today. IREN/DRECO reverse-engineered (wiki/35-iren-dreco/).

---

## STAGE 8: ORDER FULFILLMENT
**App:** Fulfillment Portal (Harry — spec complete, pending build)
**Supabase tables:** `fulfillment_orders`, `fulfillment_rules`, `shipments`

```
Order received (BQ → Supabase sync nightly)
        ↓
Fulfillment Portal (ecell.app/fulfillment or standalone):
  • UK/PH/FL teams see their wave queue
  • Carrier routing rules auto-assign carrier:
    EU → Evri | UK domestic → Royal Mail | US → Stamps.com/USPS
    Amazon orders → Amazon Buy Shipping (mandatory)
        ↓
Dispatch:
  • Generate Evri CSV or trigger carrier API
  • Enter tracking numbers
  • Write-back to Aurora order_tracking table (new)
  • Mark dispatched in Supabase
        ↓
Zero/Veeqo picks up tracking → updates all marketplaces
```

**Status:** Spec complete (Brain/vault/harry/projects/FULFILLMENT_PORTAL_SPEC.md). Blocked on Jay Mark (tester) + build.

---

## STAGE 9: FINANCE
**App:** Xero Finance App (Harry — scope complete)
**External:** Xero UK + Xero US

```
Sale confirmed
        ↓
Revenue recorded:
  • Amazon settlements → Xero via settlement report feed
  • Shopify revenue → Xero via webhook
  • Walmart revenue → Xero via report
        ↓
COGS + Royalty tracking:
  • Per-sale royalty calculated (design_code → license → royalty %)
  • Royalty accrual updated in Supabase
  • Alert if royalty pace is below MG target
        ↓
Supplier invoices:
  • PH/UK/FL receive stock from suppliers
  • Harry's Xero app: invoice upload → OCR → draft bill → post to Xero
  • 3-way match: PO → packing list → invoice
        ↓
Harry generates monthly royalty statement
→ Sent to licensor (Toei/Viz for One Piece)
```

**Status:** Xero app scope complete. Blocked on Xero OAuth credentials (UK + US).

---

## STAGE 10: INTELLIGENCE & OPTIMISATION
**Apps:** PULSE Dashboard, Hermes, Conversion Dashboard
**Agents:** Hermes (ads/pricing), Atlas (analysis), Prism (data)

```
Listings live + sales flowing
        ↓
PULSE (weekly):
  • Velocity signals: which designs are surging?
  • Coverage gaps: which devices/markets are missing?
  • FBA opportunity: which designs should go FBA?
        ↓
Hermes (Amazon Ads):
  • Search term data via middleware API
  • Sponsored Products campaigns per character
  • FBA priority scoring: search volume × FBA uplift × current FBM revenue
        ↓
Conversion Dashboard:
  • Sessions → orders CVR by product type
  • HB401 vs HTPCR conversion comparison
  • Price elasticity signals
        ↓
Feedback loop → back to Stage 2:
  • High-velocity designs → create more variants
  • Low-performing → PRUNE list
  • New license opportunities identified
```

---

## TOOL & APP MAP

| Stage | App/Tool | Builder | Status |
|-------|----------|---------|--------|
| License onboarding | ecell.app/licenses | Harry | 🔴 Build needed |
| Creative brief | Sven + Gamma | Sven | ✅ Live |
| Design code entry | ecell.app (Jay Mark) | Jay Mark | 🟡 Supabase tables in progress |
| Print file monitoring | ecell.app (Jay Mark) | Jay Mark | 🟡 In progress |
| SKU generation | ecell.app auto + CSV | Harry | 🔴 Build needed |
| EAN assignment | scripts/assign_eans.py | ✅ Built | ✅ Live (44K pool) |
| ListingForge images | scripts/listing-forge/ | Forge | 🟡 POC built, jig data ready |
| Content generation | Echo + SEO framework | Echo | ✅ Framework ready |
| Shopify upload | Shopify Admin API | Pixel/Forge | 🟡 API connected, SOP written |
| Amazon upload | Middleware + Feeds API | Harry | 🔴 Needs Product Listing scope |
| Walmart upload | Codisto/Marketplace Connect | Cem/Harry | 🟡 Subscribed |
| Fulfillment Portal | ecell.app/fulfillment | Harry | 🔴 Spec done, build needed |
| Xero Finance App | Xero UK + US | Harry | 🔴 Scope done, OAuth needed |
| PULSE Dashboard | pulse-dashboard-v2.vercel.app | ✅ Live | ✅ Live |
| Amazon Middleware API | Cloud Run (europe-west1) | ✅ Live | ✅ Live (BQ loader needs chunking) |

---

## SUPABASE TABLES NEEDED (Jay Mark)

**Existing:**
- `orders` (304K rows)
- `blank_inventory` (5,193 SKUs)
- `amazon_conversion_data` (457K rows)
- `walmart_listings`

**New (Jay Mark building now):**
- `licenses` — license master
- `license_designs` — design codes per license
- `launch_tasks` — phase tracker per design
- `license_skus` — generated SKUs with content + image URLs
- `fulfillment_orders` — dispatch queue (Harry spec)
- `fulfillment_rules` — carrier routing (Harry spec)
- `shipments` — tracking numbers

**Harry's finance tables (already built):**
- `purchase_orders`, `po_line_items`
- `packing_lists`, `supplier_invoices`, `goods_receipts`
- `stock_out_alerts`, `inventory_snapshots`

---

## ONE PIECE LAUNCH SEQUENCE (WEEKS 1-4)

```
Week 1:
  Mon: Jay Mark creates Supabase tables + prints to ecell.app
  Tue: Enter One Piece license details in ecell.app
  Wed: Enter 10 design codes (ONEPGR5, ONEPZON, etc.)
  Thu: ListingForge generates images for top 5 designs × iPhone 16/17
  Fri: Echo generates content for all SKUs

Week 2:
  Mon: Shopify bulk upload (1,803 HB401 + new One Piece)
  Tue: Amazon upload via middleware (US first)
  Wed: Samsung + iPad SKUs added
  Thu: UK + DE live
  Fri: GoHeadCase One Piece collection page live

Week 3:
  Mon: Sponsored Products ads running (Hermes)
  Wed: Fulfillment Portal tested by Jay Mark (UK + PH wave)
  Fri: Review CVR and velocity (PULSE)

Week 4:
  Walmart submitted via Codisto
  Target Plus auto-flowing from Shopify
  First royalty accrual calculated
```

---

*Process map v1.0 | 2026-04-07 | Upload to Brain/Projects/process-maps/*
