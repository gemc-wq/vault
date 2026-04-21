# Fulfillment Portal — MVP Spec
**Version:** 1.0  
**Date:** 2026-03-27  
**Owner:** Harry (COO, Ecell Global)  
**Status:** Ready to build

---

## 1. Overview

A web portal for the Ecell Global UK fulfilment team to manage outbound order dispatch across all EU/UK/US marketplaces. Built on top of the existing BigQuery data layer (fed by AWS Aurora → Google Datastream), with Supabase as the operational database for fulfillment state.

**Core goals:**
- Single queue of all pending orders that need shipping
- Configurable routing rules (country → carrier → service)
- Label/CSV generation per carrier
- Tracking number entry and write-back to source systems
- Dashboard showing dispatch status at a glance

---

## 2. Architecture

```
AWS Aurora (ZERO) — PHP monolith, NO API surface
    ↓ Google Datastream (live CDC sync, already running)
BigQuery
    ├── zero_dataset.orders                      ← clean order status + financials
    └── elcell_co_uk_barcode.order_tracker_xls   ← full address data
    ↓ nightly sync job
Supabase (PostgreSQL) — fulfillment ops DB
    ├── fulfillment_orders     ← enriched order queue
    ├── fulfillment_rules      ← carrier routing rules
    ├── shipments              ← tracking numbers + dispatch log
    └── sync_log               ← audit trail
    ↓ read/write
Next.js Portal (Vercel) — multi-office, RBAC
    ↓
FastAPI Backend (Jay Mark) — carrier integrations
    ├── Evri CSV (MVP) → ShipStation API (Phase 2)
    ├── Royal Mail SOAP API
    ├── Stamps.com (US — USPS/UPS/DHL)
    └── Amazon Buy Shipping (ALL Amazon orders — mandatory for seller protection)
    ↓ tracking numbers
Aurora: dedicated `order_tracking` table (new, write-only from portal)
    ↓ ZERO JOINs this table read-only — NO writes to ZERO's existing tables
    ↓
Amazon SP-API / Walmart API (handled by ZERO as before)
```

### Write-back Strategy (confirmed by LLM Council)
- Portal writes tracking to a **new `order_tracking` table in Aurora** only
- ZERO reads this table via JOIN — no modification to ZERO's existing schema
- This is the safe boundary: portal never touches ZERO's core tables

---

## 3. Data Sources

### BigQuery — Read Only

**Orders query (pending, undispatched):**
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

**BigQuery credentials:** Service account JSON — available in GCP project `instant-contact-479316-i4`.

### Supabase — Read/Write

- **Project:** `auzjmawughepxbtpwuhe.supabase.co`
- **Env vars:** `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`

---

## 4. Supabase Schema

```sql
-- Carrier routing rules
CREATE TABLE fulfillment_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country_code CHAR(2) NOT NULL,       -- ISO 2-letter, e.g. 'DE'
  country_name TEXT,
  carrier TEXT NOT NULL,               -- 'evri', 'royal_mail', 'ups', 'dpd'
  service_code TEXT NOT NULL,          -- carrier-specific service identifier
  weight_min_g INT DEFAULT 0,
  weight_max_g INT DEFAULT 9999,
  is_active BOOLEAN DEFAULT true,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed: EU → Evri
INSERT INTO fulfillment_rules (country_code, country_name, carrier, service_code) VALUES
  ('DE', 'Germany', 'evri', 'INTERNATIONAL'),
  ('FR', 'France', 'evri', 'INTERNATIONAL'),
  ('IT', 'Italy', 'evri', 'INTERNATIONAL'),
  ('ES', 'Spain', 'evri', 'INTERNATIONAL'),
  ('AT', 'Austria', 'evri', 'INTERNATIONAL'),
  ('NL', 'Netherlands', 'evri', 'INTERNATIONAL'),
  ('BE', 'Belgium', 'evri', 'INTERNATIONAL'),
  ('SE', 'Sweden', 'evri', 'INTERNATIONAL'),
  ('PL', 'Poland', 'evri', 'INTERNATIONAL'),
  ('IE', 'Ireland', 'evri', 'INTERNATIONAL'),
  ('FI', 'Finland', 'evri', 'INTERNATIONAL'),
  ('PT', 'Portugal', 'evri', 'INTERNATIONAL'),
  ('DK', 'Denmark', 'evri', 'INTERNATIONAL'),
  ('GR', 'Greece', 'evri', 'INTERNATIONAL'),
  ('CH', 'Switzerland', 'evri', 'INTERNATIONAL'),
  ('NO', 'Norway', 'evri', 'INTERNATIONAL');

-- Operational order queue (synced from BQ)
CREATE TABLE fulfillment_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sales_record_number TEXT UNIQUE NOT NULL,
  paid_date DATE,
  custom_label TEXT,                   -- SKU
  quantity INT DEFAULT 1,
  buyer_country TEXT,
  buyer_country_code CHAR(2),
  currency TEXT DEFAULT 'EUR',
  net_sale NUMERIC(10,2),
  marketplace TEXT,
  buyer_fullname TEXT,
  buyer_address_1 TEXT,
  buyer_address_2 TEXT,
  buyer_city TEXT,
  buyer_state TEXT,
  buyer_zip TEXT,
  buyer_phone TEXT,
  email_address TEXT,
  postage_service TEXT,
  -- fulfillment state
  fulfillment_status TEXT DEFAULT 'pending',  -- pending | processing | dispatched | cancelled
  assigned_carrier TEXT,
  assigned_service TEXT,
  -- timestamps
  synced_at TIMESTAMPTZ DEFAULT NOW(),
  dispatched_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Shipments / tracking
CREATE TABLE shipments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fulfillment_order_id UUID REFERENCES fulfillment_orders(id),
  sales_record_number TEXT NOT NULL,
  carrier TEXT NOT NULL,
  service_code TEXT,
  tracking_number TEXT,
  label_generated_at TIMESTAMPTZ,
  dispatched_at TIMESTAMPTZ,
  writeback_status TEXT DEFAULT 'pending',  -- pending | sent | failed
  writeback_attempted_at TIMESTAMPTZ,
  writeback_response TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  notes TEXT
);

-- Write-back audit log
CREATE TABLE sync_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sales_record_number TEXT,
  action TEXT,                         -- 'dispatch_confirmed', 'tracking_updated', 'bq_sync'
  status TEXT,                         -- 'ok' | 'error'
  detail TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Packaging profiles (for when guide is provided)
CREATE TABLE packaging_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sku_prefix TEXT,                     -- e.g. 'HTPCR', 'HLBWH', 'HC'
  weight_g INT DEFAULT 100,
  length_cm INT DEFAULT 19,
  width_cm INT DEFAULT 12,
  height_cm INT DEFAULT 2,
  is_default BOOLEAN DEFAULT false,
  notes TEXT
);
INSERT INTO packaging_profiles (sku_prefix, weight_g, length_cm, width_cm, height_cm, is_default)
VALUES ('DEFAULT', 100, 19, 12, 2, true);
```

---

## 5. App Pages

### 5.1 `/` — Dashboard
- **Stat cards:** Total pending | Dispatched today | Awaiting tracking | Rules configured
- **Orders by country** bar chart (recharts)
- **Recent activity** feed (last 10 dispatches)

### 5.2 `/orders` — Order Queue
- Table: SRN | SKU | Buyer | Country | City | Value | Paid Date | Carrier | Status
- Filters: Country, Carrier, Marketplace, Date range, Status
- Bulk select → **Generate CSV** (Evri format) or **Mark dispatched**
- Row click → order detail drawer
- Color coding: today's orders highlighted, overdue (>2 days) flagged red

### 5.3 `/orders/[id]` — Order Detail
- Full address block
- SKU + packaging profile lookup
- Carrier assignment (auto from rules, overridable)
- Tracking number entry field
- Dispatch confirm button
- Shipment history

### 5.4 `/dispatch` — Dispatch Wizard
- Step 1: Select orders (filtered by carrier/country, or manual selection)
- Step 2: Review — show order list, confirm packaging weights
- Step 3: Generate — download Evri CSV / Royal Mail manifest
- Step 4: Enter tracking numbers (bulk paste supported)
- Step 5: Confirm dispatch → writes to Supabase → triggers write-back

### 5.5 `/rules` — Carrier Rules Engine
- Table of all routing rules: Country → Carrier → Service → Weight range → Active
- Inline edit: toggle active, change carrier/service
- Add new rule form
- **Test rule:** enter a country, see which rule fires

### 5.6 `/settings` — Configuration
- Shipper details (company, EORI, reg number, terms)
- Sync schedule (how often to pull from BQ)
- Packaging profiles management
- Write-back toggle (enable/disable ZERO sync)

---

## 6. API Routes (Next.js)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/orders` | List orders (with filters) |
| GET | `/api/orders/[id]` | Single order detail |
| POST | `/api/orders/sync` | Trigger BQ → Supabase sync |
| POST | `/api/dispatch` | Confirm dispatch, save tracking |
| GET | `/api/dispatch/csv` | Generate Evri CSV for selected orders |
| GET | `/api/rules` | List carrier rules |
| POST | `/api/rules` | Create rule |
| PUT | `/api/rules/[id]` | Update rule |
| DELETE | `/api/rules/[id]` | Delete rule |
| POST | `/api/writeback` | Push tracking to ZERO |

---

## 7. Evri CSV Format

Exact column order (required by Evri):

```
ShipperReferenceID, CustomerReference1, CustomerReference2, ServiceCode,
ConsigneeContact, ConsigneeAddress1, ConsigneeAddress2, ConsigneeAddress3,
ConsigneeCity, ConsigneeState, ConsigneeZip, ConsigneeCountry,
ConsigneePhone, ConsigneeEmail,
Weight, WeightUOM, Length, Width, Height, DimensionUOM,
Value, Currency, Description,
ShipperCompany, ShipperEORI, ShipperRegNumber, Terms,
ItemDescription, ItemPrice, ItemQuantity, ItemCountryOfOrigin, ItemHSCode, ItemSKU
```

**Field mapping:**
- `ShipperReferenceID` = `Sales_Record_Number`
- `CustomerReference1` = `Custom_Label` (SKU)
- `CustomerReference2` = last segment of SKU (e.g. `NIG` from `H8939-SRSXCS-HATSGRA-NIG`)
- `ServiceCode` = `INTERNATIONAL`
- `ConsigneeContact` = `Buyer_Fullname + "/1"`
- `ConsigneeCountry` = ISO 2-letter country code
- `Value` / `ItemPrice` = `Net_Sale × Quantity`
- `ShipperCompany` = `Ecell Global Ltd`
- `ShipperEORI` = `GB864395193000`
- `ShipperRegNumber` = `IM2760000742`
- `Terms` = `DDP`
- `Description` / `ItemDescription` = `Phone case`
- `ItemCountryOfOrigin` = `GB`
- `ItemHSCode` = `3926909900`
- Default weight: `100g`, dimensions: `19×12×2cm` (until packaging guide provided)

---

## 8. Environment Variables

```env
# BigQuery
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
BQ_PROJECT=instant-contact-479316-i4

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://auzjmawughepxbtpwuhe.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
SUPABASE_SERVICE_ROLE_KEY=<service_role_key>

# Shipper defaults
SHIPPER_COMPANY="Ecell Global Ltd"
SHIPPER_EORI=GB864395193000
SHIPPER_REG=IM2760000742

# Write-back (Aurora — TBD)
AURORA_HOST=cluster.cluster-cvaofazjtifp.us-east-1.rds.amazonaws.com
AURORA_USER=<user>
AURORA_PASSWORD=<password>
AURORA_DB=<db_name>
```

---

## 9. Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Framework | Next.js 14 (App Router) | Same as other Ecell apps |
| Styling | Tailwind CSS + shadcn/ui | Fast, consistent UI |
| Database | Supabase (Postgres) | Already in stack |
| Data source | BigQuery (via `@google-cloud/bigquery`) | Live order data |
| Charts | Recharts | Lightweight |
| Tables | TanStack Table | Filtering, sorting, bulk select |
| Deploy | Vercel (ecells-projects-3c3b03d7) | Standard Ecell deploy target |
| Auth | Supabase Auth (email/password) | Simple, already available |

---

## 10. MVP Scope (Week 1)

### Offices & Dispatch Waves
| Office | Wave | Window |
|--------|------|--------|
| Philippines (PH) | Wave 1 | Morning |
| United Kingdom (UK) | Wave 2 | Afternoon |
| Florida, US (FL) | Wave 3 | Afternoon |

Multi-office RBAC required from day 1 — users scoped to their office/wave.

### Carriers in Scope
| Carrier | Region | MVP | Phase 2 |
|---------|--------|-----|---------|
| Evri | EU / International | CSV upload | ShipStation API |
| Royal Mail | UK domestic | API (SOAP — exists in ZERO PHP) | — |
| Stamps.com | US (USPS/UPS/DHL) | API | — |
| Amazon Buy Shipping | ALL Amazon orders | API (mandatory — seller protection) | — |
| DPD | UK (potential) | — | Future |

> FedEx handled through Amazon Buy Shipping — no separate integration needed.

---

## 10. MVP Scope (Week 1)

**In scope:**
- [ ] Supabase schema (run SQL above)
- [ ] BQ → Supabase sync script (nightly + manual trigger)
- [ ] `/orders` page — filterable queue with office/wave filter
- [ ] `/dispatch` — generate Evri CSV for selected EU orders
- [ ] `/rules` — view and edit carrier routing rules
- [ ] Manual tracking number entry → Supabase write
- [ ] Basic auth (Supabase Auth, email/password, office assignment)
- [ ] Aurora `order_tracking` table creation (write-back target)

**Out of scope (Phase 2 — Jay Mark FastAPI layer):**
- [ ] Royal Mail SOAP API integration
- [ ] Stamps.com API integration
- [ ] Amazon Buy Shipping API
- [ ] ShipStation API (replaces Evri CSV)
- [ ] Automatic tracking write-back to Aurora `order_tracking`
- [ ] Packaging profile management UI
- [ ] Full RBAC (role permissions beyond office scoping)

---

## 11. Known Data Quirks

- **Character encoding:** Some EU addresses have garbled special chars (e.g. `ß` → `StraÃ?e`) — this is a ZERO/MySQL latin-1 issue, not fixable at app level. Acceptable for now.
- **Ghost records:** Historical orders in `order_tracker_xls` with `f_status = Pending` going back to 2020 — always filter on `zero_dataset.orders` + `Paid_Date >= 30 days` to avoid including these.
- **Ireland orders:** Some arrive with yesterday's `Paid_Date` due to timezone — 7-day window covers this.
- **`Buyer_Country_Code`:** Often NULL in BQ — app should derive from country name using ISO lookup table.
- **`Net_Sale`:** Use this for value. `GBP_Price` is always empty. Currency is in the `Currency` field.
