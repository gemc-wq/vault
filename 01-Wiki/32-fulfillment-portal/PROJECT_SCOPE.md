# Fulfillment Portal — Full Project Scope

> **Purpose:** Cross-channel research document for LLM Council validation (Perplexity, Claude, GPT-5.4)
> **Created:** 2026-03-28 | **Author:** Ava
> **Company:** Ecell Global — licensed tech accessories, 200K+ SKUs, $5M+ annual revenue

---

## 1. Current State — How Fulfillment Works Today

### The Systems
| System | What It Does | Where It Runs | Status |
|--------|-------------|---------------|--------|
| **Zero** | Order management, PO generation, dispatch, marketplace integration | PHP/XAMPP on Windows PC at 192.168.20.57 (PH office) | Legacy — 10+ year old PHP monolith |
| **IREN** | Print file generation — takes order data + design artwork → produces print-ready files | Java app on local Windows PC (PH office) | Black box — built by external developer, no API, no documentation |
| **DRECO** | Design replication — generates product mockups across device templates | Local app (PH office) | Connected to IREN and Zero via shared MySQL DB |
| **AWS Aurora** | Downstream sync of PH master database | AWS RDS (us-east-1) | Slave copy of 192.168.20.160 |
| **Google Datastream** | CDC sync from Aurora → BigQuery | GCP | Running, syncs every ~2 min |
| **BigQuery** | Analytics + order data warehouse | GCP project instant-contact-479316-i4 | 2 key datasets: zero_dataset (orders) + elcell_co_uk_barcode (addresses, tracking, dispatch) |
| **Veeqo** | Inventory sync + order management for some channels | SaaS | Active — 13.5M API calls/month to Walmart |
| **Stamps.com** | USPS label printing for US orders | SaaS + desktop app | Active — Patrick runs daily |
| **Amazon Buy Shipping** | Label purchase for Amazon FBM orders (USPS/FedEx) | Amazon Seller Central | Active — provides seller protection |
| **Evri** | UK/EU shipping labels | CSV upload to Evri portal | Manual — Drew tested CSV format |
| **Royal Mail** | UK domestic shipping | Click & Drop (manual website) | Manual — no API integration |

### The Process Flow (Current)
```
1. ORDERS ARRIVE
   Amazon, eBay, Walmart, Shopify, OnBuy → Zero imports orders
   Zero writes to PH MySQL DB (192.168.20.160)
   DB syncs to AWS Aurora → Datastream → BigQuery

2. PO GENERATION (Zero)
   Zero's PHP rules engine (1,300 lines) determines:
   - WHERE to print (PH, UK, or FL) based on product type, stock, day of week
   - WHAT carrier to use based on destination country
   - WHICH wave (Wave 1: PH morning, Wave 2: UK afternoon, Wave 3: US afternoon)
   Output: Picking list per location

3. PRINT FILE GENERATION (IREN)
   Operator manually types PO number into IREN
   IREN reads order details from MySQL DB
   IREN generates print-ready files from design artwork
   Files saved to local network share
   
4. PICKING & PACKING (Manual)
   Staff prints picking list
   Staff locates blank cases, matches printed product to order
   Staff visually verifies design matches SKU (error-prone)
   
5. LABEL PRINTING (Multiple Systems)
   Amazon orders: Amazon Buy Shipping in Seller Central (USPS/FedEx)
   eBay/Website US: Stamps.com desktop app
   UK domestic: Royal Mail Click & Drop (manual)
   UK/EU: Evri CSV upload (manual)
   
6. DISPATCH & TRACKING (Zero)
   Tracking numbers entered back into Zero (manual or semi-auto)
   Zero updates marketplace order status (Amazon SP-API, eBay API)
   Dispatch date recorded in MySQL → syncs to BQ

7. MONITORING (Manual)
   No automated tracking verification
   No acceptance scan monitoring
   Customer complaints are first signal of shipping problems
```

### The Data Flow
```
PH Master DB (192.168.20.160, MySQL)
    ↓ replication
AWS Aurora RDS
    ↓ Google Datastream (CDC, ~2 min)
BigQuery
    ├── zero_dataset.orders (order status, SKU, price, marketplace)
    └── elcell_co_uk_barcode.order_tracker_xls (addresses, tracking, dispatch)
    ↓ nightly sync (sync_bq_orders.py)
Supabase (analytics + inventory)
```

**Data integrity verified (Mar 27):**
- zero_dataset.orders: 4,020 SRNs in last 7 days
- order_tracker_xls: 4,267 SRNs (extra 247 = returns/cancellations)
- Match rate: 100% — every order has address data
- Address completeness: 100% name, 100% address, 100% zip, 88% phone

---

## 2. Pain Points

### P1 — Critical (causing revenue loss or operational risk)

**2.1 No automated shipment tracking verification**
- Labels printed but packages not scanned by carrier = lost shipments
- Currently discovered only when customer complains (2-5 days late)
- Impact: Late delivery penalties, A-to-Z claims, negative reviews
- No daily exception report exists

**2.2 Manual label generation across 4+ tools**
- Amazon Buy Shipping (Seller Central), Stamps.com (desktop), Royal Mail (website), Evri (CSV)
- Each requires separate login, manual data entry, different workflows
- Staff switch between 4 tools per day — error-prone, slow
- No unified view of what's been shipped vs what hasn't

**2.3 IREN is a black box with single point of failure**
- Java app on ONE PC in Philippines — if that PC dies, print file generation stops
- No documentation, no API, no source code access (built by external developer)
- Operator manually types PO numbers — typos cause wrong print files
- No cloud backup, no redundancy

**2.4 Zero's routing rules are hardcoded PHP**
- 1,300 lines of PHP with embedded business logic
- Changes require developer intervention (edit PHP, restart server)
- No UI for operations team to adjust rules (e.g., printer down → reroute)
- Rules scattered across functions — no single source of truth

### P2 — High (causing inefficiency)

**2.5 No per-office self-service**
- PH, UK, and FL offices can't independently generate their own picking lists and labels
- PH processes everything centrally, then distributes to other offices
- Time zone dependency: UK/FL wait for PH to generate their POs
- Wave timing is rigid — no flexibility for rush orders

**2.6 Visual QC is human-only**
- Packers visually match printed product to SKU on picking list
- Error rate unknown but non-zero — wrong design shipped = return + replacement cost
- No automated verification, no audit trail of what was packed

**2.7 Tracking writeback is fragile**
- Tracking numbers entered manually into Zero
- Non-Amazon channels (eBay, Walmart, website) depend on Zero updating marketplace APIs
- If Zero misses an update, customer sees "no tracking" — support burden

**2.8 No unified dispatch dashboard**
- Operations managers have no single view of: pending orders, dispatched today, carrier distribution, problem shipments
- Reporting is ad-hoc (manual queries, spreadsheets)

### P3 — Medium (process improvement)

**2.9 No carrier rate optimization**
- No automated comparison of carrier options per shipment
- Staff use default carrier without checking if a cheaper/faster option exists
- Amazon Buy Shipping does rate comparison, but only for Amazon orders

**2.10 No packaging optimization**
- Default dimensions used for all products (19×12×2cm, 100g)
- Oversized labels = higher shipping cost; undersized = carrier surcharges
- No product-type-specific packaging profiles

---

## 3. Ideal Path Forward

### Phase 1 — Foundation + Quick Wins (Weeks 1-4)
**Goal:** Unified order queue + Evri/Royal Mail label generation + daily tracking monitor

| Deliverable | Description | Pain Point Solved |
|-------------|-------------|-------------------|
| **Unified Order Queue** | Web portal showing ALL pending orders across all marketplaces, filterable by office/carrier/product type | P2.8 |
| **Picking List Generator** | Group orders by product type, include product images from S3 CDN | P2.5 |
| **Evri CSV Generator** | Auto-generate Evri-format CSV from selected UK/EU orders | P2.2 (partial) |
| **BQ → Supabase Sync** | 15-min sync of pending orders with full address data | Data foundation |
| **Daily Tracking Monitor** | Flag shipments without acceptance scan after 24h | P1.1 |
| **SRN Reconciliation** | Daily data integrity check between BQ tables | Data quality |
| **Configurable Rules Table** | Supabase table of routing rules (country → carrier → service) with UI | P1.4 (partial) |

### Phase 2 — Carrier Integration + Writeback (Weeks 5-8)
**Goal:** Automated label purchase across all carriers + tracking writeback

| Deliverable | Description | Pain Point Solved |
|-------------|-------------|-------------------|
| **Amazon Buy Shipping API** | Automated label purchase for Amazon FBM orders — maintains seller protection | P2.2, P1.1 |
| **Stamps.com API** | Programmatic USPS/UPS/DHL label generation for non-Amazon US orders | P2.2 |
| **Royal Mail API** | Automated UK domestic label generation (replaces Click & Drop) | P2.2 |
| **Evri API via ShipStation** | API-based label generation replacing CSV upload | P2.2 |
| **Marketplace Tracking Push** | Auto-update eBay, Walmart, Shopify with tracking numbers via their APIs | P2.7 |
| **Aurora Writeback** | Push tracking back to Zero's database → keeps internal records current | P2.7 |
| **Multi-Office RBAC** | PH/UK/FL each see only their orders, generate only their labels | P2.5 |
| **Rules Engine UI** | Full CRUD for routing rules with test mode and override toggles | P1.4 |

### Phase 3 — Print Files + Vision QC (Weeks 9-12)
**Goal:** Replace IREN with cloud service + add packing verification

| Deliverable | Description | Pain Point Solved |
|-------------|-------------|-------------------|
| **Cloud Print Composition** | Python service generating print-ready files from SKU + S3 design images | P1.3 |
| **"Send to Print" Workflow** | Portal button triggers print file generation for selected orders | P1.3 |
| **Vision QC Microservice** | Camera → Gemini Vision → match printed product to expected SKU | P2.6 |
| **Packing Audit Trail** | Log every QC check: order, image, match result, confidence, timestamp | P2.6 |
| **Packaging Profiles** | Product-type-specific weight/dimensions for accurate label costs | P2.10 |

### Phase 4 — Optimization + Intelligence (Weeks 13+)
**Goal:** Carrier rate optimization + predictive analytics

| Deliverable | Description | Pain Point Solved |
|-------------|-------------|-------------------|
| **Carrier Rate Shopping** | Compare rates across carriers per shipment, suggest cheapest on-time option | P2.9 |
| **Predictive Dispatch** | Forecast daily order volumes → pre-position inventory → optimize wave timing | P2.5 |
| **Cost Analytics** | Per-order shipping cost tracking, carrier cost comparison, margin impact | P2.9 |

---

## 4. Key Architectural Decisions

### 4.1 Why NOT just extend Zero?
- Zero is PHP monolith on a local Windows PC behind a firewall
- No API surface — everything is MySQL read/write
- Modifying Zero risks breaking production order processing
- Cloud portal can run alongside Zero, reading the same data via BQ

### 4.2 Why FastAPI + Next.js (not just Next.js)?
- Label generation, carrier API calls, print file rendering = backend-heavy workflows
- Long-running jobs, retries, carrier webhooks, binary document handling
- Python ecosystem needed for future AI vision (Gemini API) + image processing
- Next.js excels at UI/dashboard — let it do what it's good at

### 4.3 Why Supabase (not direct BQ)?
- BQ is analytics-optimized, not transactional — expensive for real-time page loads
- Supabase gives us Postgres (ACID), auth, real-time subscriptions, edge functions
- Sync from BQ every 15 min = fresh enough for fulfillment ops
- Supabase already in our stack (orders, inventory tables exist)

### 4.4 Why hybrid carrier strategy?
- No single aggregator covers all our carriers + Amazon Buy Shipping
- Amazon Buy Shipping is MANDATORY for seller protection — can't route through EasyPost
- Evri requires corporate account via ShipStation
- Royal Mail has direct API — no need for aggregator
- Stamps.com already covers USPS/UPS/DHL

### 4.5 Why shadow mode before cutover?
- Zero handles 500+ orders/day across $5M+ revenue
- One bad routing rule = orders shipped to wrong location = customer impact
- Run new system in parallel for 1 week, compare output to Zero's output
- Only cut over when outputs match consistently

---

## 5. Security Requirements

| Requirement | How |
|-------------|-----|
| API keys (carrier, marketplace) | Google Secret Manager — never in code or env vars |
| Multi-office access | Supabase Auth + RBAC — PH/UK/FL roles |
| Audit trail | Every label, void, dispatch, rule change logged with user + timestamp |
| Build environment | Claude Code project — sandboxed, no public git |
| PII handling | Buyer addresses in Supabase — encrypted at rest, access-logged |
| Zero risk | Read-only from BQ until shadow mode validated. Writes only to Supabase until writeback approved. |

---

## 6. What We Need From Chad (IREN)

### Already Received
- Chad's initial assessment of Zero → IREN → DRECO connections (sent Mar 20)
- Claude Code analysis of IREN codebase (sent Mar 23)
- Three-phase automation plan: DB polling → webhooks → Claude API agent layer

### Still Needed

**6.1 IREN Input/Output Specification**
- What EXACTLY does IREN receive as input? (PO number? Order lines? SKU list?)
- What format? (MySQL query? CSV? Manual entry?)
- What EXACTLY does it output? (File format? PNG? TIFF? PDF? Resolution?)
- Where are output files saved? (Network path? Local folder?)
- File naming convention? (Does filename contain SKU, order number, design code?)

**6.2 IREN's Design Asset Sources**
- Where does IREN pull design artwork from? (Local folder? Network share? S3?)
- What format are source designs? (AI? PSD? PNG? SVG?)
- How does IREN map a design code (e.g., NARUICO) to the correct artwork file?
- Are there design-specific templates per product type? (Different layout for HTPCR vs HB401 vs H89?)

**6.3 Print Composition Logic**
- How does IREN position the design on the product template?
- Does it handle different device sizes automatically? (IPH17PMAX vs IPH13 = different dimensions)
- What about bleed, trim, and safe zones?
- Color profile handling? (CMYK? RGB? ICC profile?)

**6.4 Product Type Templates**
- How many distinct print templates exist? (One per product type? Per device?)
- Where are templates stored?
- Template format? (Java-specific or standard image format?)

**6.5 IREN Database Dependencies**
- Which MySQL tables does IREN read from?
- Which tables does it write to? (Status updates, completion flags?)
- Does IREN update order status in Zero after generating print files?

**6.6 DRECO Connection**
- How does DRECO receive design files from IREN (or vice versa)?
- Does DRECO generate the device-specific mockups that IREN uses as templates?
- What triggers DRECO to run? (DB status change? Manual? File watcher?)

**6.7 Edge Cases & Failure Modes**
- What happens when IREN can't find a design file?
- What happens when a new device is added that IREN doesn't have a template for?
- How are multi-item orders handled? (Multiple print files per order?)
- How are re-prints handled? (Customer return → reprint same design?)

**6.8 Access for Cloud Replication**
- Can Chad provide sample input/output pairs? (10 real POs with their print file outputs)
- Can we get read access to the IREN source code repo (if one exists)?
- Can Chad run IREN in debug mode to capture the processing pipeline?

---

## 7. Deliverable Summary

| # | Deliverable | Phase | Impact | Owner |
|---|-------------|-------|--------|-------|
| 1 | Unified Order Queue (web portal) | 1 | 🔴 HIGH | Jay Mark |
| 2 | Picking List Generator | 1 | 🟠 HIGH | Jay Mark |
| 3 | Evri CSV Auto-Generator | 1 | 🟠 HIGH | Jay Mark |
| 4 | Daily Tracking Monitor | 1 | 🔴 HIGH | Ava (cron) |
| 5 | Configurable Routing Rules | 1 | 🔴 HIGH | Jay Mark + Ava |
| 6 | Amazon Buy Shipping Integration | 2 | 🔴 HIGH | Jay Mark |
| 7 | Stamps.com API Integration | 2 | 🟠 HIGH | Jay Mark |
| 8 | Royal Mail API Integration | 2 | 🟠 HIGH | Jay Mark |
| 9 | Marketplace Tracking Push | 2 | 🔴 HIGH | Jay Mark |
| 10 | Multi-Office RBAC | 2 | 🟡 MED | Harry |
| 11 | Cloud Print File Service (IREN replacement) | 3 | 🔴 HIGH | Jay Mark + Chad |
| 12 | Vision QC Microservice | 3 | 🟡 MED | Ava |
| 13 | Carrier Rate Shopping | 4 | 🟡 MED | Future |

---

## 8. Research Questions for LLM Council

1. What is the best architecture for a multi-office cloud fulfillment portal handling 500+ orders/day with 5+ carrier integrations?
2. Should Amazon Buy Shipping be called directly via SP-API, or through an aggregator like EasyPost/ShipStation?
3. What's the safest approach to write tracking numbers back to a legacy MySQL/Aurora database without breaking the existing system?
4. For replacing a local Java print file generator (IREN) with a cloud service — what's the best approach for high-fidelity design-to-print composition?
5. How should carrier API credentials be managed across 3 offices with different carrier accounts?
6. What's the optimal sync frequency between BigQuery (source) and Supabase (operational DB) for fulfillment operations?
7. Is FastAPI + Next.js the right split, or should the backend be Node.js to match the frontend runtime?
8. How do ShipStation-style fulfillment tools handle multi-warehouse routing with timezone-based wave scheduling?

---

*Use this document to prompt Perplexity, Claude, GPT-5.4, or any LLM Council member.*
*Cross-ref: BUILD_SOP.md (detailed implementation), Harry's SPEC.md (GDrive), GPT-5.4 architecture research*
