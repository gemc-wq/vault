# Finance Operations Platform — Build Spec
> **For use with Claude CLI (Opus)**
> **Owner:** Cem | **Specs by:** Harry | **Orchestrator:** Athena
> **Date:** 2026-04-07

## What This Is

A unified finance operations platform for Ecell Global covering:
1. **Invoice Processing** — email/GDrive intake → OCR → review → Xero posting (UK + US)
2. **China Procurement** — PO creation → packing lists → goods receipt → invoice matching → inventory control

These are two modules of ONE app, sharing auth, database, and UI shell.

---

## Architecture Decision

**Stack:** Next.js 15 + Supabase + Xero API + Google Drive API
**Hosting:** Vercel (frontend) + Supabase (backend/DB) + N8N (email triggers only)
**Why not pure N8N?** N8N handles simple automations but this needs: review queues, multi-org routing, audit trails, inventory state management, and a proper UI for 4 offices (UK, US, PH, CN).

Harry's existing N8N webhook (`https://n8n.ecellglobal.com/webhook/xero-invoice`) stays as an optional ingest point — the app can receive invoices from it.

---

## Module 1: Invoice Processing (UK + US → Xero)

### The Flow
```
EMAIL / GDRIVE                    REVIEW                      XERO
─────────────── → ──────────── → ──────────── → ────────────
Invoice arrives    OCR extract    Human reviews   Post as DRAFT
(PDF attached)     fields         & corrects      bill in Xero
                                  supplier match   (UK or US org)
                                                  
                                  ↓ FILED
                                  GDrive: /Finance/Invoices/{supplier}/{year}/
```

### 1.1 Intake Sources (Priority Order)
1. **Email forwarding** — Cem's email and finance@ecellglobal.com receive invoices. Forward to a dedicated intake address OR use N8N to watch a Gmail label and POST to the app's API.
2. **GDrive folder** — Drop invoices into `/Finance/Invoices/Inbox/`. App watches via Google Drive API webhook or polling.
3. **Manual upload** — Drag-and-drop in the app UI.

### 1.2 Extraction Pipeline
```
PDF/Image received
    ↓
OCR + Field Extraction (Google Document AI or Claude Vision):
  - Supplier name
  - Invoice number
  - Invoice date
  - Due date
  - Currency (GBP / USD / EUR)
  - Line items (description, qty, unit price, total)
  - Tax amount
  - Total amount
  - PO reference (if present)
    ↓
Auto-match supplier against Xero contacts (fuzzy match)
Auto-detect org (UK or US) from currency + supplier mapping
    ↓
Create draft in review queue
```

### 1.3 Review Queue UI (`/invoices/review`)
- Table of pending invoices with extracted fields
- Editable: supplier, amounts, line items, account codes, tax codes
- Org selector: UK / US (auto-suggested but overridable)
- Actions: **Approve** (posts to Xero as DRAFT bill) | **Reject** (with notes) | **Edit & Approve**
- Show OCR confidence scores — highlight low-confidence fields in amber

### 1.4 Filing System
On approval, auto-file the source PDF:
- **GDrive path:** `/Finance/Invoices/{supplier_name}/{year}/{invoice_number}.pdf`
- **Supabase:** Store file reference, Xero bill ID, posting timestamp

### 1.5 Xero Integration
- **OAuth2** for both UK and US orgs (separate tenant IDs)
- **Post as DRAFT** — never auto-approve (human-in-the-loop for MVP)
- **Duplicate check:** invoice_number + supplier + amount before posting
- **Account code mapping:** per-org lookup table (UK uses different codes than US)
- **Tax code mapping:** per-org (UK VAT vs US sales tax)
- **Store Xero response:** bill ID, status, org, posted_at

### 1.6 Xero Data Sync
Pull from Xero nightly into local Supabase tables:
- `xero_contacts` (suppliers)
- `xero_accounts` (chart of accounts, per org)
- `xero_bills` (posted bills)
- `xero_invoices` (sales invoices)
- `xero_payments`
- `xero_journals`

This enables the query/reporting layer without hitting Xero API live.

---

## Module 2: China Procurement & Inventory Control

### The Flow
```
INVENTORY          PO CREATION       CHINA OFFICE      GOODS IN         INVOICE MATCH
─────────── → ──────────── → ──────────── → ──────────── → ────────────
Stock below    Auto-generate   China confirms   UK/PH/FL        Match supplier
reorder point  split POs by    production &     receives &      invoice against
               destination     ships            books stock     PO + packing list
```

### 2.1 Inventory Dashboard (`/inventory`)
**Data source:** BigQuery `zero_dataset.inventory` (real-time via Datastream)

Per-site pages: `/inventory/uk`, `/inventory/ph`, `/inventory/fl`

Each shows top 50 items with:
- Item code + description
- Free stock | On order
- 7-day sales | 30-day sales
- Weighted daily velocity: `(vel_7d × 0.7) + (vel_30d × 0.3)`
- Days of stock: `free_stock / weighted_velocity`
- Traffic light: 🔴 <14 days | 🟡 <21 days | 🟢 21+ days
- Velocity anomaly flag (>35% deviation between 7d and 30d rates)

**Tracks BLANKS only** (not finished goods). Format: `{PRODUCT_TYPE}-{DEVICE}` e.g. `HTPCR-IPH16`

### 2.2 Reorder Engine
```python
# Trigger: items where Free_Stocks < Reorder_Level AND On_Order = 0
# Exclude: PACKG, PROD-CON, PROD-SUPPLIES product groups

for item in items_below_reorder:
    # Get 7-day velocity by buyer country
    vel_US = sales_7d(item, countries=["US", "CA", "MX"])
    vel_UK = sales_7d(item, countries=["GB", "EU", "AU", "NZ", ...])
    vel_PH = sales_7d(item, countries=["JP"])  # + overflow
    
    total = vel_US + vel_UK + vel_PH
    
    # Split by demand ratio
    qty_US = reorder_qty * (vel_US / total)
    qty_UK = reorder_qty * (vel_UK / total)
    qty_PH = reorder_qty * (vel_PH / total)  # subject to PH cap
    
    # Generate separate PO per supplier × destination
    create_po(supplier=item.supplier, destination="FL", items=[...])
    create_po(supplier=item.supplier, destination="UK", items=[...])
```

### 2.3 PO Management (`/procurement/orders`)
- **Create:** Auto-generated from reorder engine OR manual
- **Approve:** Cem reviews and approves before sending
- **Track:** Status flow: `DRAFT → APPROVED → SENT → ACKNOWLEDGED → IN_PRODUCTION → SHIPPED → RECEIVED`
- **View:** Outstanding POs grouped by supplier and destination
- **Output:** Printable PDF + JSON

### 2.4 China Office Portal (`/procurement/china`)
**Audience:** China team (simplified, mobile-friendly)
- View outstanding POs assigned to their suppliers
- Mark items as: `IN_PRODUCTION` → `SHIPPED` (with tracking number)
- Upload packing list (PDF or structured form)
- No auth for MVP (internal network only)

### 2.5 Packing List Creator (`/procurement/packing-lists`)
- Auto-generate from PO: list items, quantities, weights
- China office can edit and confirm
- Print-friendly layout for shipping
- Links to PO and eventual goods receipt

### 2.6 Goods Receipt (`/procurement/receiving`)
**Audience:** UK, PH, FL warehouse teams
- Select PO → mark items received (full or partial)
- Capture: date received, qty received, condition notes
- Auto-update inventory on receipt
- Discrepancy flag if received ≠ ordered

### 2.7 Invoice Matching (3-Way Match)
```
PO (what we ordered)
    ↓ compare
Packing List (what was shipped)
    ↓ compare  
Supplier Invoice (what they're billing)
    ↓
Match result: ✅ MATCH | ⚠️ PARTIAL | ❌ DISCREPANCY
    ↓
If match → route to Module 1 review queue → Xero
If discrepancy → flag for Cem review
```

### 2.8 Supplier Costs Reference
**Already confirmed by Cem (stored in `supplier_currency_map`):**

| Product | Supplier | Currency | Cost |
|---------|----------|----------|------|
| HTPCR | XINTAI | RMB | ¥3.50 |
| HB401 | ECELLSZ | RMB | ¥6.50 |
| HLBWH Phone | JIZHAN/SHENG | RMB | ¥7.00 |
| HLBWH Kindle | JIZHAN | RMB | ¥14.00 |
| HLBWH iPad | JIZHAN | RMB | ¥15.00 |
| HB6/HB7 MagSafe | TOKO | USD | $1.90 |
| HDMWH 900×400 | TOKO | USD | $1.76 |
| HDMWH 600×300 | TOKO | USD | $0.86 |
| HDMWH 250×300 | ECELLSZ | RMB | ¥2.80 |

Vinyl (H8939/HSTWH): $0.75/ft² — per-unit cost varies by device dimensions.

---

## Database Schema (Supabase)

### Shared / Config
```sql
-- Xero org connections
CREATE TABLE xero_orgs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,          -- 'Ecell Global UK' / 'Ecell Global Inc'
  country TEXT NOT NULL,       -- 'UK' / 'US'
  tenant_id TEXT NOT NULL,     -- Xero tenant ID
  default_currency TEXT NOT NULL, -- 'GBP' / 'USD'
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Supplier master (synced from Xero + enriched)
CREATE TABLE suppliers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  xero_contact_id_uk TEXT,
  xero_contact_id_us TEXT,
  default_currency TEXT NOT NULL DEFAULT 'USD',
  country TEXT,                -- 'CN', 'UK', 'US'
  is_china_supplier BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Account code mappings per org
CREATE TABLE account_code_mappings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES xero_orgs(id),
  category TEXT NOT NULL,      -- 'inventory', 'shipping', 'packaging'
  account_code TEXT NOT NULL,
  account_name TEXT,
  tax_type TEXT                -- 'INPUT' / 'NONE' / etc
);
```

### Module 1: Invoice Processing
```sql
-- Inbound documents (email, gdrive, upload)
CREATE TABLE inbound_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source TEXT NOT NULL,        -- 'email' / 'gdrive' / 'upload'
  source_ref TEXT,             -- email message ID or gdrive file ID
  filename TEXT NOT NULL,
  file_url TEXT,               -- Supabase storage URL
  status TEXT DEFAULT 'pending', -- pending → extracted → in_review → approved → posted → rejected
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Extracted invoice data (from OCR)
CREATE TABLE extracted_invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES inbound_documents(id),
  supplier_name TEXT,
  supplier_id UUID REFERENCES suppliers(id),
  invoice_number TEXT,
  invoice_date DATE,
  due_date DATE,
  currency TEXT,
  subtotal DECIMAL(12,2),
  tax_amount DECIMAL(12,2),
  total_amount DECIMAL(12,2),
  po_reference TEXT,
  org_id UUID REFERENCES xero_orgs(id), -- auto-detected UK or US
  confidence_score DECIMAL(3,2),        -- OCR confidence 0-1
  extracted_at TIMESTAMPTZ DEFAULT now()
);

-- Extracted line items
CREATE TABLE extracted_line_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID REFERENCES extracted_invoices(id),
  description TEXT,
  item_code TEXT,
  quantity DECIMAL(10,2),
  unit_price DECIMAL(12,4),
  tax_amount DECIMAL(12,2),
  line_total DECIMAL(12,2),
  account_code TEXT
);

-- Xero posting log
CREATE TABLE xero_postings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID REFERENCES extracted_invoices(id),
  xero_bill_id TEXT,           -- returned by Xero API
  xero_org_id UUID REFERENCES xero_orgs(id),
  status TEXT DEFAULT 'draft', -- draft → authorised → paid
  posted_at TIMESTAMPTZ DEFAULT now(),
  posted_by TEXT,
  error_message TEXT
);

-- GDrive filing log
CREATE TABLE filed_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID REFERENCES inbound_documents(id),
  gdrive_file_id TEXT,
  gdrive_path TEXT,            -- /Finance/Invoices/{supplier}/{year}/
  filed_at TIMESTAMPTZ DEFAULT now()
);
```

### Module 2: Procurement & Inventory
```sql
-- Purchase orders
CREATE TABLE purchase_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  po_number TEXT UNIQUE NOT NULL,
  supplier_id UUID REFERENCES suppliers(id),
  destination TEXT NOT NULL,   -- 'UK' / 'FL' / 'PH'
  status TEXT DEFAULT 'draft', -- draft → approved → sent → acknowledged → in_production → shipped → received
  currency TEXT NOT NULL,
  total_amount DECIMAL(12,2),
  notes TEXT,
  approved_by TEXT,
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- PO line items
CREATE TABLE po_line_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  po_id UUID REFERENCES purchase_orders(id),
  item_code TEXT NOT NULL,     -- e.g. HTPCR-IPH17
  description TEXT,
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(12,4),
  currency TEXT,
  line_total DECIMAL(12,2)
);

-- Packing lists (created by China office)
CREATE TABLE packing_lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  po_id UUID REFERENCES purchase_orders(id),
  tracking_number TEXT,
  ship_date DATE,
  carrier TEXT,
  total_boxes INTEGER,
  total_weight_kg DECIMAL(8,2),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Packing list line items
CREATE TABLE packing_list_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  packing_list_id UUID REFERENCES packing_lists(id),
  item_code TEXT NOT NULL,
  quantity_shipped INTEGER NOT NULL
);

-- Goods receipts (warehouse teams)
CREATE TABLE goods_receipts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  po_id UUID REFERENCES purchase_orders(id),
  packing_list_id UUID REFERENCES packing_lists(id),
  received_by TEXT,
  received_at TIMESTAMPTZ DEFAULT now(),
  location TEXT NOT NULL,      -- UK / FL / PH
  status TEXT DEFAULT 'pending' -- pending → partial → complete → discrepancy
);

-- Goods receipt line items
CREATE TABLE goods_receipt_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  receipt_id UUID REFERENCES goods_receipts(id),
  item_code TEXT NOT NULL,
  quantity_expected INTEGER,
  quantity_received INTEGER,
  condition_notes TEXT
);

-- 3-way match results
CREATE TABLE invoice_matches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  supplier_invoice_id UUID REFERENCES extracted_invoices(id),
  po_id UUID REFERENCES purchase_orders(id),
  packing_list_id UUID REFERENCES packing_lists(id),
  match_status TEXT,           -- match / partial / discrepancy
  discrepancy_notes TEXT,
  reviewed_by TEXT,
  reviewed_at TIMESTAMPTZ
);

-- Inventory snapshots (from BQ, refreshed nightly)
CREATE TABLE inventory_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  item_code TEXT NOT NULL,
  warehouse TEXT NOT NULL,
  free_stock INTEGER,
  on_order INTEGER,
  sales_7d INTEGER,
  sales_30d INTEGER,
  daily_velocity_7d DECIMAL(8,2),
  daily_velocity_30d DECIMAL(8,2),
  weighted_velocity DECIMAL(8,2),
  days_of_stock DECIMAL(8,1),
  alert_level TEXT,            -- RED / AMBER / GREEN
  velocity_flag BOOLEAN DEFAULT false,
  snapshot_date DATE DEFAULT CURRENT_DATE
);
```

---

## Build Phases

### Phase 1: Foundation (Week 1)
**Goal:** App shell + auth + database + Xero connection

- [ ] Next.js 15 project setup (App Router, Tailwind, shadcn/ui)
- [ ] Supabase project setup + run all CREATE TABLE statements above
- [ ] Xero OAuth2 flow for UK + US orgs
- [ ] Xero data sync: contacts, accounts (nightly cron)
- [ ] App shell: sidebar nav, org switcher (UK/US), auth
- [ ] Supplier table pre-populated from Xero contacts + currency map

### Phase 2: Invoice Processing MVP (Week 2)
**Goal:** Upload invoice → extract → review → post to Xero

- [ ] File upload UI (drag-and-drop PDF/image)
- [ ] OCR extraction (Claude Vision API or Google Document AI)
- [ ] Supplier auto-match (fuzzy against Xero contacts)
- [ ] Org auto-detection (currency + supplier → UK or US)
- [ ] Review queue UI with editable fields
- [ ] Xero bill posting (DRAFT only)
- [ ] Duplicate detection (invoice_number + supplier + amount)
- [ ] GDrive filing on approval: `/Finance/Invoices/{supplier}/{year}/`

### Phase 3: Email Intake (Week 2-3)
**Goal:** Invoices from email land in the review queue automatically

- [ ] Option A: N8N watches Gmail label → POSTs PDF to app API
- [ ] Option B: Google Apps Script on finance email → forwards to app
- [ ] Inbound document table tracks source (email/gdrive/upload)
- [ ] GDrive folder watcher (polling or webhook)

### Phase 4: Inventory Dashboard (Week 3)
**Goal:** Live inventory view with traffic lights

- [ ] BQ → Supabase nightly snapshot (inventory_snapshots table)
- [ ] Site pages: `/inventory/uk`, `/inventory/ph`, `/inventory/fl`
- [ ] Top 50 items per site by 30-day sales
- [ ] Weighted velocity calculation + traffic light display
- [ ] Velocity anomaly flags
- [ ] Global dashboard with cross-site summary

### Phase 5: PO Management (Week 3-4)
**Goal:** Auto-generate split POs from inventory triggers

- [ ] Reorder engine: detect items below threshold
- [ ] Split algorithm: demand-based by buyer country (BQ query)
- [ ] PO generator: separate PO per supplier × destination
- [ ] Cem approval UI before sending
- [ ] PO status tracking (draft → approved → sent → ... → received)
- [ ] Printable PO PDF output

### Phase 6: China Office Portal (Week 4)
**Goal:** China team can manage their POs

- [ ] Simplified mobile-friendly UI at `/procurement/china`
- [ ] View outstanding POs for their suppliers
- [ ] Mark as: in_production → shipped (with tracking)
- [ ] Create/upload packing list
- [ ] No auth for MVP (internal tool)

### Phase 7: Goods Receipt + Invoice Match (Week 4-5)
**Goal:** Close the procurement loop

- [ ] Goods receipt UI for UK/FL/PH warehouse teams
- [ ] Mark items received (full or partial)
- [ ] Discrepancy detection (received ≠ ordered)
- [ ] 3-way match: PO ↔ Packing List ↔ Supplier Invoice
- [ ] Route matched invoices to Module 1 review queue → Xero
- [ ] Flag discrepancies for Cem review

---

## Key Integration Points

| System | Integration | Method |
|--------|------------|--------|
| **Xero UK** | OAuth2, bill posting, data sync | Xero API v2 |
| **Xero US** | OAuth2, bill posting, data sync | Xero API v2 |
| **BigQuery** | Inventory data, sales velocity, PO history | BigQuery API (read) |
| **Google Drive** | Invoice filing, packing list storage | Drive API v3 |
| **Gmail/N8N** | Email invoice intake | N8N webhook or Apps Script |
| **Supabase** | All app data, auth, real-time subscriptions | Supabase JS client |
| **Harry's N8N webhook** | Optional ingest point | POST to webhook keeps working |

---

## Environment Variables Needed

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Xero
XERO_CLIENT_ID=
XERO_CLIENT_SECRET=
XERO_REDIRECT_URI=

# Google (Drive + optional OCR)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_DRIVE_INVOICES_FOLDER_ID=

# OCR (pick one)
ANTHROPIC_API_KEY=           # For Claude Vision extraction
# OR
GOOGLE_DOCUMENT_AI_PROCESSOR_ID=  # For Document AI

# BigQuery
GOOGLE_APPLICATION_CREDENTIALS=  # Service account JSON path
BQ_PROJECT_ID=
```

---

## Success Criteria

The platform is MVP-complete when:
1. ✅ Upload a UK supplier invoice PDF → extracted fields shown → review → approve → DRAFT bill appears in Xero UK
2. ✅ Same for US org
3. ✅ Approved invoices auto-filed in GDrive under correct supplier/year folder
4. ✅ Inventory dashboard shows live traffic-light status for UK/PH/FL
5. ✅ Reorder engine generates split POs based on demand
6. ✅ Cem can approve POs in the app
7. ✅ China office can mark POs as shipped with tracking
8. ✅ Warehouse teams can confirm goods received
9. ✅ 3-way match links PO + packing list + supplier invoice before posting to Xero

---

## Reference Specs (in Vault)
- `03-Agents/Harry/projects/XERO_FINANCE_APP_SCOPE.md` — original Xero scope
- `03-Agents/Harry/projects/INVENTORY_ORDERING_APP.md` — inventory ordering spec
- `03-Agents/Harry/projects/PROCUREMENT_SYSTEM_SPEC.md` — procurement system v1
- `03-Agents/Harry/projects/procurement/COGS_INVENTORY_ROADMAP.md` — COGS + inventory roadmap
- `01-Wiki/05-inventory/SOP_INVENTORY_TRACKING.md` — inventory SOP (draft 0.1)
