# Ecell Global — End-to-End Process Map V4
*Created: 2026-04-07 | Author: Athena | Source: Blueprint V3, project specs, email threads*
*Incorporates: ecell.app, ListingForge, Fulfillment Portal, Xero Finance App, Inventory Ordering App, Procurement System*
*Pilot: One Piece — first license through the full loop*

---

## THE FULL LOOP

```
LICENSE    →  CREATIVE  →  SKU SETUP   →  IMAGES    →  CONTENT   →  LISTINGS
(ecell.app)   (PH+Sven)    (ecell.app)    (LForge)     (Echo)       (APIs)
     │                                                                  │
     │    ┌─────────────────────────────────────────────────────────────┘
     │    ▼
     │  ORDERS     →  FULFILLMENT  →  PRINT FILES  →  DISPATCH  →  TRACKING
     │  (BQ+Supa)     (Portal)        (ecell.app)     (Carriers)   (Aurora)
     │                                                                  │
     │    ┌─────────────────────────────────────────────────────────────┘
     │    ▼
     │  FINANCE    →  INTELLIGENCE
     │  (Xero App)    (PULSE+Hermes)
     │                      │
     └──────────────────────┘ ← feedback loop: velocity → reorder → new designs
```

---

## STAGE 1: LICENSE ONBOARDING
**App:** `ecell.app/licenses` | **Builder:** Jay Mark | **DB:** Supabase `licenses`

```
Cem signs license contract
        │
        ▼
ecell.app/licenses — Human enters:
┌────────────────────────────────────────────┐
│  License name:        One Piece            │
│  Licensor:            Toei Animation       │
│  Design code prefix:  ONEP                 │
│  Royalty %:           15%                  │
│  Territory:           US, UK, EU           │
│  Expiry date:         Mar 2028             │
│  Product types:       ☑ HTPCR ☑ HB401     │
│                       ☑ HLBWH ☑ HB6CR     │
│                       ☑ HB7BK ☑ HDMWH     │
│                       ☑ H8939              │
│  Contract PDF:        → GDrive/licenses/   │
└────────────────────────────────────────────┘
        │
        ▼ System auto-creates:
• SKU prefix ONEP registered in `license_designs` table
• Launch tracker card in `launch_tasks`
• Royalty accrual tracker initialised → feeds Stage 10 (Finance)
• Notification to Sven: "New license — create design brief"
```

**Supabase tables (Jay Mark building):**
| Table | Purpose | Key Fields |
|-------|---------|------------|
| `licenses` | Master license record | name, licensor, prefix, royalty_pct, territory[], expiry, product_types[], contract_url |
| `license_designs` | Design codes per license | license_id, design_code, character_name, variants[], status (draft→approved) |
| `launch_tasks` | Phase tracker per design | design_code, phase, status, assigned_to, due_date |

---

## STAGE 2: CREATIVE DIRECTION
**App:** `ecell.app/licenses/[id]` → Creative tab | **Agents:** Sven + PH Team (Bea)

```
Sven generates creative brief:
  • Character priority list (top 10-20)
  • Style guide (hex codes, art direction)
  • Competitive teardown (e.g. Casetify)
  • Gamma presentation → #creative Slack
        │
        ▼
PH Creative Team (Bea manages):
  1. Designer creates 1 raw PSD on 1-1 canvas template
  2. Creates .jpg submission → "FOR UPLOADING" Teams group
  3. Bea inputs manual product coding into trackers
  4. Submits to licensor for approval (online/email)
  5. Once approved: designer prepares 13 canvas templates
     (covers all device model categories)
  6. Notifies via "FOR REPLICATION / LISTING" Teams group
        │
        ▼ [THIS IS WHAT'S CHANGING]
CURRENT: Bea emails replication team with tracker links
NEW:     Bea enters design codes in ecell.app → DB-driven pipeline
```

**What ecell.app replaces:**
| Old (Email) | New (ecell.app) |
|---|---|
| Bea emails replication team | Bea enters design_code in app, uploads image link |
| Tracker spreadsheet for codes | `license_designs` table with status workflow |
| Manual title collation | Auto-generated from design_code + brand lookup |
| Teams group notification | App status change triggers next stage |

---

## STAGE 3: DESIGN CODE ENTRY + SKU GENERATION
**App:** `ecell.app/licenses/[id]` → Designs tab | **Builder:** Jay Mark

```
Bea/Creative enters in ecell.app:
┌────────────────────────────────────────────┐
│  Design code:    ONEPGR5                   │
│  Character:      Gear 5 Luffy             │
│  Variants:       BLK, WHT, NAT            │
│  Image link:     s3://atg/ONEPGR5/...     │
│  Canvas files:   ☑ 1-1  ☑ 1-2  ☑ 2-1 ... │
│  Status:         [Draft] → [Approved ✓]    │
└────────────────────────────────────────────┘
        │
        ▼ On Cem/Sven approval (status = "approved"):
System auto-generates SKU matrix:
  For each: design × product_type × device
  
  HTPCR-IPH17PMAX-ONEPGR5-BLK
  HTPCR-IPH16PMAX-ONEPGR5-BLK
  HB401-IPH17PMAX-ONEPGR5-BLK
  HLBWH-GALSA256-ONEPGR5-BLK
  HDMWH-DM250X300-ONEPGR5-BLK
  ... (hundreds of combinations)
        │
        ▼
EAN Assignment Engine:
  • Pulls from unassigned EAN pool (44K remaining)
  • Writes to `ean_assignments` table
  • Links: EAN → SKU → design_code → license
        │
        ▼
`license_skus` table populated with:
  sku, design_code, product_type, device, ean, image_url (null), 
  content (null), status: "sku_generated"
        │
        ▼ Parallel triggers:
  → Stage 4 (ListingForge images)
  → Stage 5 (Content generation)
```

**Priority device order (One Piece launch):**
iPhone 17/16 Pro Max → Samsung S25/S24 Ultra → iPad → desk mats → full range

---

## STAGE 4: LISTING IMAGE CREATION (ListingForge)
**App:** ListingForge pipeline (Mac Studio) | **Agent:** Forge/Iris | **Data:** t_jig_devices (8,199 rows)

```
license_skus (status: "sku_generated")
        │
        ▼
ListingForge reads:
  • Design artwork from S3: /atg/{DESIGN_CODE}/{VARIANT}/
  • Device jig data from t_jig_devices → dimensions, padding, rotation
  • Jig template from t_jigs → canvas size, grid layout
        │
        ▼
Image Composite Pipeline:
  1. PSD/JPEG → Pillow loads design artwork
  2. Apply rotation + corner radius (from jig data)
  3. Composite onto device frame at correct dimensions
  4. Generate grid layouts (4x5 jig, 2x3 showcase, etc.)
  5. Output: 1000×1000px listing images per SKU
        │
        ▼
Upload to S3:
  Position 1:  https://elcellonline.com/atg/{DESIGN}/{VARIANT}/{PREFIX}-{DEVICE}-1.jpg
  Position 2:  Secondary angle
  Position 1b: With background
  Features:    staticimages/features/{DESIGN}.jpg
        │
        ▼
Update license_skus: image_url = S3 path, status → "images_ready"
```

**S3 URL Rules (from Jessie, Mar 31):**
- Image positions: 1, 2, 1b, features
- Path: `atg/{design_code}/{variant}/{product_type}-{device}-{position}.jpg`
- Naming conventions per product type in spreadsheet

---

## STAGE 5: CONTENT GENERATION
**Agent:** Echo (Sonnet 4.6) | **Source:** Shopify SOP + SEO framework

```
license_skus (status: "images_ready" OR "sku_generated")
        │
        ▼
Echo generates per design (one call per design, replicated across devices):

TITLE (MANDATORY RULES):
  ✅ "One Piece Gear 5 Luffy Official Hybrid MagSafe Case for iPhone 17 Pro Max"
  ❌ "ONEPGR5 HTPCR IPH17PMAX" ← NEVER use raw codes in titles
  
  Format: "{License} {Character} Official {Case Type} for {Device} | {Feature}"

DESCRIPTION:
  • Hero copy + feature bullets + about the design
  • 5 Amazon/Walmart bullet points
  • SEO meta title + description

TAGS:
  • License name, character, device, case type

QA CHECK (Ava spot-check 10%):
  ☑ No design codes in titles (brand names only)
  ☑ Full device name (not IPH17PMAX)
  ☑ Inventory set to 9999
        │
        ▼
Update license_skus: title, description, bullets, tags, status → "content_ready"
```

---

## STAGE 6: LISTING UPLOAD
**App:** Shopify Admin API + Amazon SP-API (middleware) + Walmart | **Agent:** Pixel/Forge

```
license_skus (status: "content_ready" + "images_ready")
        │
        ├──► SHOPIFY (GoHeadCase DTC + Target Plus feed):
        │      Bulk CSV from license_skus
        │      Shopify Admin API upload
        │      vendor: "Head Case Designs"
        │      inventory: 9999
        │      Auto-flows to Target Plus (Shopify = hub)
        │
        ├──► AMAZON (via Middleware API):
        │      POST /api/v1/reports/request-and-wait
        │      JSON_LISTINGS_FEED
        │      ⚠️ BLOCKED: needs "Product Listing" scope from Cem
        │      Marketplace order: US → UK → DE
        │
        └──► WALMART:
               CSV per Walmart format
               GTIN-14 (leading zero on EAN-13)
               Via Codisto / Shopify Marketplace Connect
        │
        ▼
Update license_skus: status → "live", marketplace_status: {shopify: true, amazon: true, ...}
Notification to Cem: "X SKUs live on Y marketplaces"
```

---

## STAGE 7: PRINT FILE MONITORING
**App:** `ecell.app/print-files` (Jay Mark building) | **DB:** Jay Mark's new Supabase tables

```
Order comes in (via Veeqo/Zero/marketplace)
        │
        ▼
ecell.app Print File Monitor:
┌────────────────────────────────────────────┐
│  Order SKU: HTPCR-IPH17PMAX-ONEPGR5-BLK   │
│  Print file exists? ☑ YES / ☐ NO          │
│                                            │
│  If YES → auto-queue for production        │
│  If NO  → flag to PH team to create       │
│           Status: [needed] → [created]     │
│                   → [approved] → [in-prod] │
└────────────────────────────────────────────┘
        │
        ▼
DRECO/IREN Integration (current PH process):
  1. Photoshop ExtendScript converts PSD canvas → JPEG
  2. Codes from tracker → ExtendScript Toolkit
  3. Dreco1 creates listing images from JPEGs + DB lineup data
  4. IREN renders high-res print files using jig measurements
     (width, height, padding from t_jig_measurement)
  5. Output uploaded to S3 and PH print servers
     \\192.168.20.187\d\sdd2\Shares\Images\RawImages
     \\192.168.20.108\LeatherWallet\Dreco2\RawImages
        │
        ▼
[FUTURE — IREN2 cloud replacement]:
  • Cloud-based per office (UK/PH/FL each run own waves)
  • Web-based app, same jig data
  • Eliminates single point of failure on PH server
  • Jay Mark + Forge building replacement
```

**Key technical facts (from Bea + Jessie emails Apr 7):**
- 13 canvas templates per design (cover all device categories)
- PSD → JPEG conversion via Photoshop script (not direct PSD to Dreco)
- Red rectangle layer = camera/device hole safe zone guide
- PSDs stored on 5TB drive, organised by license folders
- DB: `elcell_co_uk_barcode` on 192.168.20.160 (local) + AWS RDS
- IREN creds: `config.properties` (db155_* and dbrds_* keys)
- Dreco creds: `Configuration.java` (hardcoded in getDefault())
- Device mapping: e.g. TP-IPH17PRO → 2-1 category
- `t_jig_devices` can bypass measurements when image prep shortcuts needed

---

## STAGE 8: ORDER FULFILLMENT
**App:** Fulfillment Portal (`ecell.app/fulfillment` or standalone) | **Builder:** Jay Mark | **Spec:** Harry

```
BQ → Supabase nightly sync
  zero_dataset.orders + order_tracker_xls
        │
        ▼
Fulfillment Portal — per-office wave queue:
┌────────────────────────────────────────────┐
│  UK Wave 1  │  PH Wave 1  │  FL Wave 1    │
│─────────────│─────────────│───────────────│
│  Order #    │  Order #    │  Order #      │
│  SKU        │  SKU        │  SKU          │
│  Carrier    │  Carrier    │  Carrier      │
│  Status     │  Status     │  Status       │
│  [Print ☑]  │  [Print ☑]  │  [Print ☐]   │
└────────────────────────────────────────────┘
        │
        ▼
Carrier Routing (auto-assigned from fulfillment_rules):
  EU orders      → Evri (CSV MVP → ShipStation Phase 2)
  UK domestic    → Royal Mail 24 / Buy Shipping
  US orders      → Stamps.com (USPS/UPS/DHL)
  Amazon orders  → Amazon Buy Shipping (MANDATORY)
  ⚠️ DHL dropped from UK routing (Jay Mark confirmed Apr 7)
        │
        ▼
Dispatch:
  1. Generate carrier CSV / trigger API
  2. Enter tracking numbers
  3. Write-back to Aurora `order_tracking` table (NEW, write-only)
     ⚠️ Portal NEVER touches Zero's core tables
  4. Mark dispatched in Supabase `shipments`
        │
        ▼
Zero/Veeqo picks up tracking → updates all marketplaces
```

**Architecture:**
```
BQ (orders) → Supabase (fulfillment_orders, fulfillment_rules, shipments)
                → Next.js Portal (multi-office, RBAC)
                    → FastAPI backend (Jay Mark)
                        → Evri CSV / RM API / Stamps.com / Amazon Buy Shipping
                            → Aurora order_tracking (write-back)
```

---

## STAGE 9: FINANCE
**App:** Xero Finance App | **Owner:** Harry (Finance Agent) | **External:** Xero UK + US

```
Sales confirmed across all marketplaces
        │
        ├──► REVENUE RECORDING:
        │      Amazon settlements → Xero via settlement report feed
        │      Shopify revenue → Xero via webhook
        │      Walmart revenue → Xero via report
        │
        ├──► ROYALTY TRACKING:
        │      Per-sale royalty calculated:
        │        license_skus.design_code → licenses.royalty_pct
        │        e.g. One Piece sale $24.95 × 15% = $3.74 accrual
        │      Running accrual updated in Supabase
        │      Alert if royalty pace below MG target
        │        ⚠️ NBA: $200K MG vs $13K rev (danger)
        │        ✅ One Piece: new, no MG pressure yet
        │
        ├──► AP DOCUMENT INTAKE:
        │      Supplier invoices (email/PDF/upload)
        │      OCR → field extraction
        │      Supplier matching (auto from supplier table)
        │      Draft bill → review → post to Xero
        │      3-way match: PO → packing list → invoice
        │
        ├──► COGS & JOURNAL POSTING:
        │      Inventory usage reports → journal entries
        │      COGS adjustments per product type:
        │        HTPCR: ¥3.50 RMB (XINTAI)
        │        HB401: ¥6.50 RMB (ECELLSZ)
        │        HLBWH phone: ¥7 RMB (JIZHAN/SHENG)
        │        HLBWH Kindle: ¥14 RMB (JIZHAN)
        │        HB6/HB7 MagSafe: $1.90 USD (TOKO)
        │      Currency-aware (RMB/USD/GBP)
        │
        └──► QUERY/REPORTING:
               Invoices, bills, receipts, payments, journals
               Org switching (UK / US)
               Monthly royalty statement → licensor
        │
        ▼
Harry generates monthly royalty statement per license
→ Sent to licensor (Toei/Viz for One Piece)
```

**Supabase tables (Harry built):**
| Table | Purpose |
|-------|---------|
| `purchase_orders` | PO headers |
| `po_line_items` | PO lines with qty, price, currency |
| `packing_lists` | Received goods |
| `supplier_invoices` | Matched invoices |
| `goods_receipts` | Receipt confirmations |
| `stock_out_alerts` | Velocity-based alerts |
| `inventory_snapshots` | Point-in-time stock levels |

---

## STAGE 10: INVENTORY & PROCUREMENT
**App:** Inventory Ordering App | **Owner:** Harry (Finance) | **Data:** BQ inventory views

```
Inventory Ordering App — per-office view:
┌───────────────────────────────────────────────────┐
│  UK TOP 50 ITEMS          │ Status │ Days │ Order │
│───────────────────────────│────────│──────│───────│
│  HTPCR-IPH17PMAX          │  🔴    │  8   │  500  │
│  HB401-IPH16PMAX          │  🟡    │  18  │  200  │
│  HLBWH-GALSA256           │  🟢    │  34  │  —    │
│  HDMWH-DM250X300          │  🟡    │  19  │  100  │
└───────────────────────────────────────────────────┘

Traffic light thresholds (Cem confirmed):
  🔴 RED    = < 14 days stock
  🟡 AMBER  = < 21 days stock  
  🟢 GREEN  = 21+ days stock

Velocity model:
  • 7-day weighted 70% + 30-day weighted 30%
  • Flag anomalies: 7d vs 30d velocity diff > 35%
        │
        ▼
Auto-generates PO recommendations:
  • Split by destination: 70% PH / 15% UK / 15% FL (pending Cem approval)
  • Separate PO per destination (clean invoicing)
  • Currency-aware: RMB for CN suppliers, USD for TOKO, GBP for UK
  • Skip EOL items (11 flagged for removal)
        │
        ▼
PO approval flow:
  1. System generates draft PO
  2. Cem reviews in app or via daily digest
  3. Approved → sent to supplier (Ben at Foxmail for CN)
  4. Supplier ships → tracking entered (Ben emails UPS/FedEx/DHL numbers)
  5. Chris Yunun (PH procurement) receives → updates stock
  6. Stock levels refresh → velocity recalculates
```

**Active CN supplier shipments (from Ben, Apr 1):**
| Route | Carrier | Tracking | Contents |
|-------|---------|----------|----------|
| CN→PH | UPS HK | 1Z3153V10445842447 | Cases |
| CN→UK | UPS HK | 1Z3153V10443305709 | Cases |
| CN→US | FedEx | 870106564699 | Plastic sheets + cases |
| CN→US | FedEx | 889956990728 | Desk mats + cases |

---

## STAGE 11: INTELLIGENCE & FEEDBACK LOOP
**Apps:** PULSE Dashboard, Hermes, Conversion Dashboard

```
Listings live + sales flowing
        │
        ├──► PULSE (weekly):
        │      Velocity signals: which designs surging?
        │      Coverage gaps: which devices/markets missing?
        │      Top movers: 30d vs 90d momentum
        │      Cross-region gaps: US/UK/DE cross-sell
        │
        ├──► HERMES (ongoing):
        │      Search term data via middleware API
        │      Sponsored Products campaigns per character
        │      FBA priority scoring: volume × uplift × current rev
        │      Amazon ads optimisation
        │
        ├──► CONVERSION DASHBOARD:
        │      Sessions → orders CVR by product type
        │      HB401 vs HTPCR conversion comparison
        │      Price elasticity signals
        │
        └──► FEEDBACK → back to Stage 1:
               High-velocity designs → create more variants (→ Stage 2)
               Low-performing → PRUNE list (→ archive)
               New license opportunities identified (→ Stage 1)
               Reorder triggers from velocity (→ Stage 10)
```

---

## TOOL & APP MAP (ALL PROJECTS)

| Stage | App/Tool | Builder | Status | Blocker |
|-------|----------|---------|--------|---------|
| 1 | ecell.app/licenses | Jay Mark | 🟡 Tables in progress | App UI needed |
| 2 | Sven + Gamma + PH Team | Sven/Bea | ✅ Brief live | FigJam board in progress |
| 3 | ecell.app/designs + EAN engine | Jay Mark + scripts | 🔴 Not built | Needs Stage 1 tables |
| 4 | ListingForge (Mac Studio) | Forge/Iris | 🟡 POC built | Needs 5 approved designs |
| 5 | Echo + SEO framework | Echo | ✅ Ready | Waiting for SKUs |
| 6a | Shopify Admin API | Pixel/Forge | 🟡 Connected | SOP written, needs Cem go-ahead |
| 6b | Amazon SP-API (middleware) | Forge | 🔴 Blocked | Needs "Product Listing" scope from Cem |
| 6c | Walmart (Codisto) | Cem/Harry | 🟡 Subscribed | Pending |
| 7 | ecell.app/print-files | Jay Mark | 🟡 Starting | Supabase tables today |
| 8 | Fulfillment Portal | Jay Mark | 🟡 Spec done | Building + testing |
| 9 | Xero Finance App | Harry (Finance) | 🔴 Scope done | Xero OAuth from Cem |
| 10 | Inventory Ordering App | Harry (Finance) | 🟢 Building | 11 tables, alerts needed |
| 11a | PULSE Dashboard | ✅ Live | ✅ | pulse-dashboard-v2.vercel.app |
| 11b | Hermes (ads/pricing) | Hermes | ✅ Active | — |
| 11c | Conversion Dashboard | ✅ Live | ✅ | — |
| ∞ | Vault Librarian | Athena → Hermes | 🟢 First compile done | Nightly cron Phase 2 |

---

## SUPABASE TABLE MAP (FULL)

### Jay Mark — Building Now
| Table | Stage | Purpose |
|-------|-------|---------|
| `licenses` | 1 | License master record |
| `license_designs` | 2-3 | Design codes per license |
| `launch_tasks` | 1-3 | Phase tracker per design |
| `license_skus` | 3-6 | Generated SKUs + content + images + marketplace status |
| `ean_assignments` | 3 | EAN → SKU → design_code links |

### Jay Mark — Fulfillment
| Table | Stage | Purpose |
|-------|-------|---------|
| `fulfillment_orders` | 8 | Enriched order queue from BQ |
| `fulfillment_rules` | 8 | Carrier routing rules |
| `shipments` | 8 | Tracking numbers + dispatch log |

### Harry — Finance (Already Built)
| Table | Stage | Purpose |
|-------|-------|---------|
| `purchase_orders` | 10 | PO headers |
| `po_line_items` | 10 | PO lines (qty, price, currency) |
| `packing_lists` | 10 | Received goods |
| `supplier_invoices` | 9 | Matched invoices |
| `goods_receipts` | 10 | Receipt confirmations |
| `stock_out_alerts` | 10 | Velocity-based alerts |
| `inventory_snapshots` | 10 | Point-in-time stock levels |

### Existing
| Table | Stage | Rows |
|-------|-------|------|
| `orders` | 8-11 | 304K |
| `blank_inventory` | 10 | 5,193 |
| `amazon_conversion_data` | 11 | 457K |
| `walmart_listings` | 6 | 95K |

---

## OWNERSHIP MATRIX

| Stage | Owner | Backup | Human |
|-------|-------|--------|-------|
| 1. License Onboarding | Jay Mark | Ava | Cem (signs) |
| 2. Creative | Sven | — | Bea (PH Creative Mgr) |
| 3. SKU Generation | Jay Mark + Forge | Ava | Bea (enters codes) |
| 4. ListingForge Images | Forge + Iris | Jay Mark | — |
| 5. Content | Echo | Ava (QA) | — |
| 6. Listing Upload | Pixel/Forge | Jay Mark | — |
| 7. Print File Monitor | Jay Mark | — | Jessie (PH IT), PH print team |
| 8. Fulfillment | Jay Mark (build) | — | UK: Ant, PH: Jeric, FL: Jenny |
| 9. Finance | **Harry (Finance)** | — | — |
| 10. Inventory/Procurement | **Harry (Finance)** | — | Chris Yunun (PH procurement) |
| 11. Intelligence | Hermes + PULSE | Atlas | — |
| ∞. Vault/Librarian | Athena → Hermes | Ava (vault owner) | — |
| ★. Orchestration | **Athena** (Stages 1-6) | Ava | Cem (decisions) |

---

## ONE PIECE LAUNCH: WEEK-BY-WEEK

| Week | Stages Active | Key Deliverables |
|------|--------------|-----------------|
| **1 (Apr 7-11)** | 1, 2, 3 | Jay Mark: Supabase tables live. Bea: FigJam board + first 10 design codes entered. EANs assigned. |
| **2 (Apr 14-18)** | 3, 4, 5, 6 | ListingForge: images for top 5 × iPhone 16/17. Echo: content. Shopify bulk upload. Amazon US (if scope granted). |
| **3 (Apr 21-25)** | 6, 7, 8, 11 | UK + DE listings live. Print file monitoring active. Fulfillment Portal tested (Jay Mark). Hermes: Sponsored Products ads. |
| **4 (Apr 28+)** | 8, 9, 10, 11 | Walmart via Codisto. Target Plus auto-flow. First royalty accrual. PULSE velocity review. Procurement reorder if needed. |

---

*V4 — incorporates all open projects, email intelligence (Bea/Jessie Apr 7), and Harry Finance repurpose.*
*Pilot: One Piece. What works here scales to every future license.*
