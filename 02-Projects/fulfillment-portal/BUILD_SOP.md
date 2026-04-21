# Fulfillment Portal — Build SOP
**Version:** 1.0
**Date:** 2026-03-28
**Owner:** Ava (Strategy) + Harry (Architecture) + Jay Mark (Builder)
**Status:** APPROVED FOR BUILD

---

## 1. Project Overview

Cloud-based fulfillment portal replacing Zero's local dispatch workflow, IREN print file generation, and manual CSV label uploads. Accessible from all three offices (PH, UK, FL) with office-specific label generation and configurable routing rules.

**Core deliverable:** A ShipStation-like web app where each office can view their orders, generate picking lists, print carrier labels, trigger print file generation, and track shipments — all from one portal.

---

## 2. Architecture (Approved)

```
AWS Aurora (ZERO — system of record)
    ↓ Google Datastream (CDC sync, every 2 min, ALREADY RUNNING)
BigQuery
    ├── zero_dataset.orders              ← order status + financials (4,020/week)
    └── elcell_co_uk_barcode.order_tracker_xls  ← address data (2.8M rows)
    ↓ JOIN on Sales_Record_Number
    ↓ Sync to Supabase (cron every 15 min)
Supabase (PostgreSQL — operational DB)
    ├── fulfillment_orders     ← enriched order queue
    ├── fulfillment_rules      ← configurable carrier routing
    ├── shipments              ← tracking numbers + dispatch log
    ├── packaging_profiles     ← weight/dimensions by product type
    └── sync_log               ← audit trail
    ↓ read/write
FastAPI Backend (Google Cloud Run)
    ├── Rules engine
    ├── Carrier API integrations
    ├── Print file orchestration
    └── Tracking writeback
    ↓
Next.js Frontend (Vercel)
    ↓
Carrier APIs → Labels + Tracking Numbers
    ↓
Writeback → Aurora (tracking) → Zero → Marketplace updates
```

**Tech Stack:**
| Layer | Tech | Reason |
|-------|------|--------|
| Backend | FastAPI (Python) | Carrier APIs, rules engine, future AI vision |
| Frontend | Next.js 14 + Tailwind + shadcn/ui | Consistent with Ecell apps |
| Operational DB | Supabase (Postgres) | Already in stack |
| Data source | BigQuery | Live order data via Datastream |
| File storage | Google Cloud Storage | Labels, print files |
| Deploy | Cloud Run (backend) + Vercel (frontend) | Scalable, no infra management |
| Auth | Supabase Auth + RBAC | Office-based roles |

---

## 3. Data Layer (VERIFIED)

### BigQuery Tables
- `zero_dataset.orders` — 4,020 orders/week, current to today
- `elcell_co_uk_barcode.order_tracker_xls` — 2.8M rows, full address data

### Join Key
`Sales_Record_Number` — confirmed 100% match rate between tables (last 7 days: 4,020/4,020)

### Address Completeness (verified Mar 27)
- Buyer name: 100%
- Address: 100%
- Zip: 100%
- Phone: 88% (normal — some marketplaces don't provide)

### BQ Query (Harry's, verified working)
```sql
SELECT
  o.Sales_Record_Number,
  o.Paid_Date,
  o.Custom_Label,
  CAST(o.Quantity AS INT64) AS Quantity,
  o.Buyer_Country,
  o.Status,
  o.Currency,
  CAST(o.Net_Sale AS FLOAT64) AS Net_Sale,
  o.Marketplace,
  x.Buyer_Fullname,
  COALESCE(x.Buyer_Address_1, '') AS Buyer_Address_1,
  COALESCE(x.Buyer_Address_2, '') AS Buyer_Address_2,
  COALESCE(x.Buyer_City, '') AS Buyer_City,
  COALESCE(x.Buyer_State, '') AS Buyer_State,
  COALESCE(x.Buyer_Zip, '') AS Buyer_Zip,
  COALESCE(x.Buyer_Country_Code, '') AS Buyer_Country_Code,
  COALESCE(x.Buyer_Phone, '') AS Buyer_Phone,
  COALESCE(x.Email_Address, '') AS Email_Address,
  x.Postage_Service
FROM `instant-contact-479316-i4.zero_dataset.orders` o
LEFT JOIN `instant-contact-479316-i4.elcell_co_uk_barcode.order_tracker_xls` x
  ON o.Sales_Record_Number = x.Sales_Record_Number
WHERE o.Dispatch_Date IS NULL
  AND o.Status = 'Pending'
  AND o.Paid_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY o.Paid_Date ASC
```

---

## 4. Carrier Integration Strategy (HYBRID)

### By Order Source

| Order Source | Label Method | Why |
|-------------|-------------|-----|
| **Amazon (all)** | Amazon Buy Shipping API (SP-API) | MANDATORY — A-to-Z claim protection, seller protection, 31% discounted rates. Non-negotiable. |
| **eBay US** | Stamps.com API | Existing account, USPS + UPS + DHL support |
| **eBay UK** | Royal Mail API or Evri (ShipStation) | Royal Mail for domestic UK, Evri for EU |
| **Walmart** | Stamps.com API (US) | FedEx/USPS via Stamps.com |
| **Shopify/Website** | Stamps.com (US) / Royal Mail (UK) | Based on buyer country |
| **OnBuy UK** | Evri (ShipStation API) | EU destinations |

### Carrier API Details

| Carrier | API Available | Integration Method | Status |
|---------|--------------|-------------------|--------|
| **Amazon Buy Shipping** | ✅ SP-API Shipping section | Direct API — getRates, purchaseShipment | Need SP-API roles enabled |
| **Stamps.com** | ✅ SOAP API | Direct integration — labels, rates, tracking | Have account, need API credentials |
| **Royal Mail** | ✅ API Shipping | Direct API — 100+ items/day required | Need business API account — Cem to request |
| **Evri** | ✅ via ShipStation/ShipEngine | Corporate account required | Need corporate Evri credentials |
| **FedEx** | ✅ REST API | Direct or via Amazon Buy Shipping | Linked to Amazon Buy Shipping account |
| **USPS** | ✅ via Stamps.com | Through Stamps.com integration | Already active |

### Critical Rule: Amazon Orders
```
IF marketplace == "Amazon":
    USE Amazon Buy Shipping API
    → Tracking auto-uploaded to Amazon
    → A-to-Z protection active
    → Seller account health protected
    DO NOT use direct carrier APIs for Amazon orders
```

---

## 5. Routing Rules Engine

### Rules Extracted from Zero + Cem's Directives

**Location Rules:**
| Rule | Logic | Source |
|------|-------|--------|
| H89 (Gaming Skins) | NEVER route to PH | Zero PHP hardcoded |
| HST (Sticker) | NEVER route to PH | Zero PHP hardcoded |
| HDM (Desk Mat) | NEVER route to PH | Zero PHP hardcoded |
| Saturday/Monday orders | PH handles ALL eligible products | Zero PHP + Cem directive |
| Default routing | Based on stock availability by warehouse | Zero PHP |
| Printer down override | Divert to alternate location | Manual override (dynamic) |

**PO Wave Timing:**
| Wave | Time | Location | Priority |
|------|------|----------|----------|
| Wave 1 | PH morning (8 AM PHT / 8 PM ET) | Philippines | Print PH labels first → PH starts printing |
| Wave 2 | UK afternoon (~2 PM GMT) | UK | UK labels for same-day cutoff |
| Wave 3 | US afternoon (~2-3 PM ET) | Florida | US labels for same-day cutoff |

**Country → Carrier Routing:**
| Buyer Country | Carrier | Service |
|--------------|---------|---------|
| US | Stamps.com (USPS/FedEx) or Amazon Buy Shipping | Priority/Ground |
| UK | Royal Mail or Evri | 1st/2nd class or Standard |
| EU (DE, FR, IT, etc.) | Evri | International |
| JP, AU, etc. | Stamps.com (USPS International) or DHL | International |

### Remaining Extraction Needed
- Full product type → location routing table from `zero_POFiltering.php`
- Stock-based routing logic (check inventory → route to location with stock)
- Multi-location split logic (partial from PH, partial from FL)

**Action:** Jay Mark to extract all routing rules from Zero PHP codebase into structured JSON/pseudocode format.

---

## 6. App Pages (ShipStation-Style)

### 6.1 Dashboard (`/`)
- Stat cards: Pending | Dispatched Today | Awaiting Tracking | Overdue (>48h)
- Orders by country bar chart
- Orders by product type breakdown
- Recent activity feed

### 6.2 Order Queue (`/orders`)
- Table: SRN | SKU | Product Type | Buyer | Country | City | Value | Paid Date | Carrier | Status
- **Filters:** Country, Carrier, Marketplace, Product Type, Date range, Status, Office
- **Sort:** By SKU, by product type (group all HTPCR, then all HB401, then all skins)
- **Bulk select** → Generate labels / Generate picking list / Mark dispatched
- Color coding: today = highlighted, overdue >48h = red
- **Office filter:** Each office sees ONLY their orders based on routing rules

### 6.3 Picking List Generator (`/picking`)
- Select orders → Generate printable picking list
- Group by product type (HTPCR together, HB401 together, skins together)
- Include: SKU, quantity, bin location, product image from S3 CDN
- Print-friendly layout
- Option to "Send to IREN" (triggers print file generation)

### 6.4 Dispatch Wizard (`/dispatch`)
- Step 1: Select orders (filtered by carrier/country, or manual selection)
- Step 2: Review — confirm packaging weights, carrier assignment
- Step 3: Generate — purchase labels via carrier API (or download CSV for Evri)
- Step 4: Tracking numbers auto-populated (from API) or manual entry (for CSV)
- Step 5: Confirm dispatch → writes to Supabase → triggers writeback

### 6.5 Rules Engine (`/rules`)
- Table: Country → Carrier → Service → Weight range → Product type restrictions → Active
- Inline edit: toggle active, change carrier/service
- Add new rule
- **Test rule:** Enter a country + product type → see which rule fires
- **Override mode:** Printer down / holiday / peak mode toggles

### 6.6 Tracking Monitor (`/tracking`)
- All shipments from last 48 hours
- Status: Label Created → Acceptance Scan → In Transit → Delivered
- 🔴 Flag: No acceptance scan after 24 hours
- 🟡 Flag: In transit > 5 days
- Daily summary auto-posted to Telegram #customer-service + Slack #cs-daily

### 6.7 Settings (`/settings`)
- Shipper details per office (company, EORI, reg number)
- Carrier API credentials (stored in Secret Manager, not env vars)
- Packaging profiles by product type
- Sync schedule configuration
- User management + RBAC

---

## 7. Security Requirements

### API Key Management
- All carrier API keys stored in **Google Secret Manager** (NOT environment variables, NOT git)
- Backend-only credential access — never exposed to browser
- Separate credentials per office/carrier account where needed
- Key rotation support

### Authentication & Authorization
| Role | Access |
|------|--------|
| PH Ops | View PH orders, generate PH labels, trigger print files |
| UK Ops | View UK orders, generate UK labels (Evri, Royal Mail) |
| US Ops | View US orders, generate US labels (Stamps.com, FedEx) |
| Admin | All offices, rules engine, settings, user management |
| Finance/Audit | Read-only access to all dispatch logs and tracking |

### Audit Trail
- Log every: label creation, void/cancel, manifest, tracking writeback, rule change, credential rotation
- Include: user, office, order, carrier, timestamp
- Immutable shipment records after purchase (controlled void/reissue only)

### Build Environment
- **Claude Code project** — sandboxed, no public git repo
- API keys injected via environment, never committed
- No accidental exposure risk

---

## 8. Tracking Writeback Flow

### Amazon Orders
```
Amazon Buy Shipping API → Label + Tracking Number
    → Auto-uploaded to Amazon (handled by API)
    → Record tracking in Supabase for our dashboard
    → No Zero writeback needed (Amazon handles marketplace update)
```

### Non-Amazon Orders
```
Carrier API (Stamps.com/Royal Mail/Evri) → Label + Tracking Number
    → Update marketplace directly via API:
        - eBay: eBay Trading API → add tracking
        - Walmart: Walmart API → update shipment
        - Shopify: Shopify API → fulfill order
    → Write tracking to Supabase (our record)
    → Write tracking to Aurora RDS (Zero's record)
        → Zero syncs to BigQuery via Datastream
```

### Aurora Writeback (Requires)
- Aurora RDS write credentials (from Chad/IT)
- Exact table + column mapping for tracking number insertion
- Shadow mode validation before production writes

---

## 9. Print File Generation (IREN Replacement — Phase 2)

### Current State
- IREN = Java app on local PH PC
- Generates print files from order data + design images
- No API, no cloud access, no thumbnails

### Cloud Replacement
- Python service on Cloud Run
- Inputs: SKU (parsed → product type, device, design, variant) + design images from S3 CDN
- Outputs: Print-ready files (PNG/PDF) stored in Cloud Storage
- Templates: configurable per product type (phone case, skin, desk mat, etc.)
- Triggered from fulfillment portal "Send to Print" button

### Action Required
- Chad's IREN codebase analysis (sent Mar 23) → extract print composition logic
- Map IREN's input/output format
- Build cloud equivalent that reads same design assets

---

## 10. Vision QC (Phase 3)

### Concept
- Packer photographs printed product with phone/tablet
- Gemini Vision API identifies the design
- Matches against S3 product images + order's expected SKU
- Pass/Fail with confidence score
- Low-confidence items flagged for human review

### Architecture
- Separate microservice (NOT embedded in fulfillment portal)
- Portal sends QC request (order_id, image)
- QC service returns match result
- Designed as hooks in Phase 1, built in Phase 3

---

## 11. Exception Reports (Daily Automated)

| Check | What It Does | Alert Channel |
|-------|-------------|---------------|
| **SRN Reconciliation** | Compare orders table vs tracker table — flag mismatches | Telegram #customer-service |
| **Stale Pending** | Orders pending >48 hours without dispatch | Telegram #customer-service |
| **Missing Acceptance Scan** | Labels printed but no carrier scan after 24h | Telegram #customer-service + Slack #cs-daily |
| **Duplicate SRN** | Detect duplicate sales record numbers | Telegram to Cem |
| **Address Completeness** | Orders missing address, zip, or country code | Slack #cs-daily |

---

## 12. Build Phases

### Phase 1 — MVP (Weeks 1-4)
**Goal:** Working order queue + Evri CSV generation for UK office

- [ ] Supabase schema (fulfillment_orders, fulfillment_rules, shipments, sync_log, packaging_profiles)
- [ ] BQ → Supabase sync script (every 15 min + manual trigger)
- [ ] `/orders` page — filterable order queue with office filter
- [ ] `/picking` — picking list generator grouped by product type
- [ ] `/dispatch` — Evri CSV generation for selected orders
- [ ] `/rules` — view and edit carrier routing rules
- [ ] Manual tracking number entry → Supabase
- [ ] Daily SRN reconciliation cron
- [ ] Basic Supabase auth (email/password per office)

### Phase 2 — Carrier APIs + Writeback (Weeks 5-8)
- [ ] Amazon Buy Shipping API integration
- [ ] Stamps.com API integration (USPS/UPS/DHL)
- [ ] Royal Mail API integration
- [ ] Evri API via ShipStation (replace CSV)
- [ ] Tracking writeback to Aurora RDS
- [ ] Marketplace API tracking updates (eBay, Walmart, Shopify)
- [ ] Tracking monitor dashboard
- [ ] Multi-office RBAC

### Phase 3 — Print Files + Vision QC (Weeks 9-12)
- [ ] Cloud print file generation service (IREN replacement)
- [ ] "Send to Print" workflow from portal
- [ ] Vision QC microservice (Gemini Vision)
- [ ] Packing verification camera integration

---

## 13. Team Assignments

| Person | Responsibility |
|--------|---------------|
| **Ava** | Overall spec, rules engine logic, exception reports, QA review |
| **Harry** | Architecture review, Supabase schema, deployment |
| **Jay Mark** | PRIMARY BUILDER — FastAPI backend + carrier integrations + Zero PHP extraction |
| **Chad** | IREN analysis, Aurora RDS access/credentials, Zero infrastructure support |
| **Cem** | Carrier account setup (Royal Mail API, Stamps.com API credentials), AWS access |

---

## 14. Prerequisites (Cem Action Required)

| Item | Status | Action |
|------|--------|--------|
| Royal Mail Business API account | ❌ Not started | Cem to apply at royalmail.com/business |
| Stamps.com API credentials | ❌ Need to extract | From existing Stamps.com account settings |
| Evri corporate account credentials | ❌ Need from Drew/team | For ShipStation API integration |
| Aurora RDS write credentials | ❌ Need from Chad | For tracking writeback |
| Amazon SP-API Shipping role | ❌ Need in Seller Central | Add Shipping role to SP-API app |
| FedEx API key | ❌ Optional (covered by Amazon Buy Shipping + Stamps.com) | Only if direct FedEx needed |
| GCP Service Account JSON | ✅ Available | ADC on Mac Studio |

---

## 15. Known Data Quirks

- **Character encoding:** EU addresses have garbled special chars (`ß` → `StraÃ?e`) — MySQL latin-1 issue in Zero. Accept for now; clean in Supabase on ingest.
- **Ghost records:** Historical pending orders going back to 2020 in tracker — always filter `Paid_Date >= 30 days`.
- **Ireland timezone:** Some orders arrive with yesterday's `Paid_Date` — use 7-day window.
- **`Buyer_Country_Code`:** Often NULL — derive from country name using ISO lookup.
- **zero_dataset.orders metadata shows 0 rows** but queries return data — stale BQ metadata cache, not a real issue.

---

*This SOP is the single source of truth for the fulfillment portal build.*
*Cross-ref: Harry's SPEC.md (GDrive), GPT-5.4 architecture research, Zero infrastructure map*
*Build environment: Claude Code project (sandboxed, no public git)*
