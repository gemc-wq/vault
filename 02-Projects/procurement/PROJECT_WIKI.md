# Inventory Ordering App — Project Wiki
**Version:** 2.6  
**Date:** 2026-04-13  
**Owner:** Harry (COO, Ecell Global)  
**Status:** Active build — Internal transfer rules added

---

## 1. Overview

Inventory Ordering App is the **end-to-end procurement and inventory management system** for Ecell Global's blank inventory across all sites. It replaces manual Excel-based workflows with an integrated platform connecting China sourcing, regional warehouses, and finance.

### Primary Sites
| Site | Code | Role |
|------|------|------|
| **UK** | UK | Fulfillment hub for Europe |
| **Florida (FL)** | FL | US fulfillment hub |
| **Philippines (PH)** | PH | Production + regional fulfillment |
| **China** | CN | Sourcing, procurement, supplier management |
| **Transit** | TRANSIT | In-transit inventory tracking |

### Core Purpose
1. **Stock Monitoring** — Track inventory levels across all warehouses
2. **Reorder Management** — Auto-generate purchase orders based on velocity
3. **China Procurement** — End-to-end workflow from PO to stock receipt
4. **Shipment Tracking** — Monitor in-transit inventory with delivery alerts
5. **Finance Integration** — Auto-post supplier invoices to Xero

---

## 2. Key Deliverables (Expanded Scope)

### 2.1 Purchase Order Management
- **PO Generation** — Auto-create POs from reorder queue with supplier/warehouse logic
- **Multi-Site Distribution Logic** — POs split across FL/UK/PH based on product type and capacity rules
- **Shipping Plan Generation** — Auto-calculate destination split with Ben's exportable order sheet
- **Rounding Logic** — Round quantities to base 10 or base 100 per logistics requirements
- **PO Approval Workflow** — UK/FL/PH managers approve POs before China sees them
- **Item Exclusion Rules** — Auto-exclude `z-` prefix items and stale stock from reorder queue
- **PO Versioning** — Track revisions and amendments
- **Multi-currency Support** — GBP (UK), USD (FL/PH/CN), CNY (CN local)

### 2.2 China Office Portal (Mandarin Support)
- **Full Mandarin UI** — Complete Chinese language interface
- **PO Download by Supplier** — China team downloads POs grouped by supplier
- **Packing List Creation** — Generate packing lists from POs
- **Packing List Upload** — Upload Excel/PDF packing lists per shipment
- **Supplier Invoice Upload** — Upload supplier invoices (PDF/image)
- **Shipment Creation** — Create shipments with tracking info, ETA, carrier
- **Exception Reports** — Priority view of urgent/high-priority items on order

### 2.3 Shipment & Logistics
- **Shipment Tracking** — Track all in-transit shipments (CN→UK, CN→FL, CN→PH)
- **ETA Notifications** — Slack/email alerts to UK/FL/PH when shipments created
- **Packing List Distribution** — Auto-send packing lists to destination warehouses
- **Delivery Monitoring** — LLM monitors tracking and alerts on delivery
- **Auto Stock Receipt** — On delivery confirmation, auto-add stock to destination warehouse

### 2.4 Exception Management
- **Items On Order Page** — China office view showing all items on order
- **Priority Levels** — Critical/High/Medium/Low based on stock-out risk
- **Overdue Alerts** — Flag POs/shipment delays exceeding thresholds
- **Discrepancy Reports** — Highlight qty/price mismatches between PO and invoice

### 2.5 Warehouse Staff Portal (Read-Only + Adjustments)
- **Top Selling Items View** — Site-specific page showing top 50 items by sales velocity
- **Stock on Hand Display** — Current free stock levels with traffic light status (RED/AMBER/GREEN/BLACK)
- **Stock Adjustment Requests** — Submit damage/waste/count correction requests only
- **Request Tracking** — View status of own adjustment requests
- **NO PO Creation** — Warehouse staff cannot create purchase orders
- **NO Reorder Queue Access** — Cannot view or modify reorder recommendations
- **Site Isolation** — Can only see own warehouse data

### 2.6 Stock Adjustment & Write-off Workflow
- **Adjustment Request** — Warehouse submits stock adjustment (damage/waste/count correction)
- **LLM Validation** — AI reviews request against recent receipts, shipments, and patterns
- **Approval Queue** — Validated requests route to manager approval
- **Auto-posting** — Approved adjustments update inventory + post to Xero (write-off expense)
- **Audit Trail** — Full log of who/what/when/why for each adjustment

### 2.7 Finance Integration
- **Invoice Upload** — Supplier invoices uploaded in China portal
- **OCR/Extraction** — Auto-extract invoice data (supplier, amount, items)
- **Xero Posting** — Feed to Finance Agent for Xero recording
- **Inventory Accounting** — Record as inventory asset (Xero doesn't track inventory)
- **Multi-entity Support** — Post to correct Xero org (UK vs US)

---

## 3. Workflow: China Procurement to Stock Receipt

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CHINA PROCUREMENT WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────────────┘

[UK/FL/PH]                    [CHINA OFFICE]                    [DESTINATION]
    │                               │                                  │
    ▼                               │                                  │
┌─────────────┐                     │                                  │
│ Reorder     │                     │                                  │
│ Queue       │                     │                                  │
│ (Auto-gen)  │                     │                                  │
└──────┬──────┘                     │                                  │
       │                            │                                  │
       ▼                            │                                  │
┌─────────────┐                     │                                  │
│ PO Created  │────────────────────►│                                  │
│ (Pending    │   PO Notification   │                                  │
│  Approval)  │                     │                                  │
└──────┬──────┘                     │                                  │
       │                            │                                  │
       ▼                            │                                  │
┌─────────────┐                     │                                  │
│ Manager     │                     │                                  │
│ Approves    │                     │                                  │
└──────┬──────┘                     │                                  │
       │                            │                                  │
       ▼                            ▼                                  │
┌─────────────┐              ┌─────────────┐                          │
│ PO Status:  │─────────────►│ China Portal│                          │
│ APPROVED    │              │ - View POs  │                          │
└─────────────┘              │ - Download  │                          │
                             │   by supplier│                         │
                             └──────┬──────┘                          │
                                    │                                 │
                                    ▼                                 │
                             ┌─────────────┐                          │
                             │ Create      │                          │
                             │ Packing List│                          │
                             │ (from PO)   │                          │
                             └──────┬──────┘                          │
                                    │                                 │
                                    ▼                                 │
                             ┌─────────────┐                          │
                             │ Upload      │                          │
                             │ - Packing   │                          │
                             │   List      │                          │
                             │ - Supplier  │                          │
                             │   Invoice   │                          │
                             └──────┬──────┘                          │
                                    │                                 │
                                    ▼                                 │
                             ┌─────────────┐                          │
                             │ Create      │                          │
                             │ Shipment    │                          │
                             │ - Tracking  │                          │
                             │ - Carrier   │                          │
                             │ - ETA       │                          │
                             └──────┬──────┘                          │
                                    │                                 │
           ┌────────────────────────┘                                 │
           │                                                         │
           ▼                                                         ▼
    ┌─────────────┐                                          ┌─────────────┐
    │ Slack/Email │─────────────────────────────────────────►│ UK/FL/PH    │
    │ Notification│   Packing List + ETA Alert               │ Notification│
    │ (Auto-send) │                                          │             │
    └─────────────┘                                          └──────┬──────┘
                                                                    │
                                                                    ▼
                                                             ┌─────────────┐
                                                             │ LLM Monitor │
                                                             │ Tracks      │
                                                             │ Delivery    │
                                                             └──────┬──────┘
                                                                    │
                                                                    ▼
                                                             ┌─────────────┐
                                                             │ Delivered?  │
                                                             └──────┬──────┘
                                                                    │
                                              ┌─────────────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │ Auto Add    │
                                       │ Stock to    │
                                       │ Destination │
                                       │ Warehouse   │
                                       └──────┬──────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │ Finance     │
                                       │ Agent Posts │
                                       │ to Xero     │
                                       └─────────────┘
```

---

## 3.5 Multi-Site Distribution Rules

### Site Capacity & Product Type Allocation

**Based on actual order fulfillment data (`orders.PO_Location`):**

| Site | Primary Product Types | Capacity | Overflow Handling |
|------|----------------------|----------|-------------------|
| **Florida (FL)** | HTPCR, HC, HB401, H89**, HDMWH | ~37.5% US orders | — |
| **Philippines (PH)** | HLBWH (US), Saturday print, FBA | ~25% total orders | UK overflow on Mondays |
| **UK** | All UK + ROW orders | ~37.5% | Monday overflow to PH |

### Fixed Country Rules
- UK handles all UK domestic orders
- UK handles all Rest-of-World (ROW) orders
- FL handles US orders (specific product types)
- PH handles US overflow + FBA + Saturday production

### Shipping Plan Calculation
When POs are created, the system must:

1. **Calculate total reorder need** based on combined velocity across all sites
2. **Apply distribution rules** by product type:
   - HTPCR, HC, HB401, H89**, HDMWH → primarily FL
   - HLBWH → primarily PH
   - All UK/ROW → UK
3. **Account for overflow rules**:
   - PH prints 25% of total orders
   - UK Monday overflow → PH
   - PH Saturday + FBA capacity reserved
4. **Round quantities**:
   - Base 10 rounding for standard items
   - Base 100 rounding for high-volume items
5. **Generate exportable order sheet** for Ben (CSV + PDF)

### Order Sheet Format
```csv
Item_Code,Description,Total_Qty,FL_Qty,UK_Qty,PH_Qty,Supplier,Currency
HTPCR-IPH15P,TPU iPhone 15 Pro,1000,600,200,200,XINTAI,USD
HLBWH-IPH15P,Leather Wallet iPhone 15 Pro,500,0,0,500,ECELLSZ,USD
```

---

## 4. Data Model & Supabase Schema

### 4.1 Core Tables

#### `inventory_snapshots`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `item_code` | text | SKU |
| `description` | text | Product description |
| `warehouse` | text | UK, FL, PH, CN, TRANSIT |
| `product_group` | text | Category |
| `supplier` | text | Primary supplier |
| `free_stocks` | int | Available stock |
| `on_order` | int | Quantity on order |
| `in_transit` | int | Quantity in transit |
| `sales_last_7d` | int | 7-day sales velocity |
| `sales_last_30d` | int | 30-day sales velocity |
| `daily_velocity_7d` | decimal | Calculated 7d velocity |
| `daily_velocity_30d` | decimal | Calculated 30d velocity |
| `weighted_daily_velocity` | decimal | (7d × 0.7) + (30d × 0.3) |
| `days_of_stock` | decimal | free_stocks / velocity |
| `velocity_flag` | boolean | Anomaly detected |
| `alert_level` | text | RED, AMBER, GREEN, BLACK |
| `is_excluded` | boolean | Z-prefix or stale stock exclusion |
| `exclusion_reason` | text | z_prefix, stale_stock, dead_stock |
| `last_sale_date` | date | Date of last sale (for stale detection) |
| `snapshot_date` | date | Data freshness |

#### `purchase_orders`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `po_number` | text | Unique PO number (PO-YYYYMMDD-XXX) |
| `supplier` | text | Supplier name |
| `warehouse` | text | Destination warehouse (FL, UK, PH, or MULTI) |
| `status` | text | DRAFT, PENDING_APPROVAL, APPROVED, SENT, PARTIAL, RECEIVED, CANCELLED |
| `currency` | text | GBP, USD, CNY |
| `total_amount` | decimal | PO total |
| `distribution_json` | jsonb | {FL: qty, UK: qty, PH: qty} split |
| `shipping_plan_generated` | boolean | Order sheet created |
| `order_sheet_url` | text | GDrive/Storage URL to CSV/PDF |
| `rounding_base` | int | 10 or 100 |
| `created_by` | uuid | User who created |
| `approved_by` | uuid | User who approved |
| `created_at` | timestamp | Creation time |
| `approved_at` | timestamp | Approval time |
| `sent_to_supplier_at` | timestamp | When China downloaded/saw |
| `expected_delivery` | date | Estimated delivery |

#### `po_lines`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `po_id` | uuid | FK to purchase_orders |
| `item_code` | text | SKU |
| `description` | text | Item description |
| `quantity` | int | Total ordered qty (rounded) |
| `quantity_fl` | int | Allocation for Florida |
| `quantity_uk` | int | Allocation for UK |
| `quantity_ph` | int | Allocation for PH |
| `unit_price` | decimal | Price per unit |
| `line_total` | decimal | qty × price |
| `received_qty` | int | Qty received so far |
| `product_type` | text | HTPCR, HC, HB401, H89**, HDMWH, HLBWH, etc. |

#### `shipments`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `shipment_number` | text | Unique shipment ID |
| `po_ids` | uuid[] | Array of POs in shipment |
| `origin` | text | CN |
| `destination` | text | UK, FL, PH |
| `carrier` | text | DHL, FedEx, UPS, etc. |
| `tracking_number` | text | Carrier tracking # |
| `status` | text | PREPARING, IN_TRANSIT, DELIVERED, EXCEPTION |
| `ship_date` | date | When shipped |
| `eta` | date | Estimated arrival |
| `delivered_at` | timestamp | Actual delivery time |
| `packing_list_url` | text | GDrive/Storage URL |
| `invoice_url` | text | Supplier invoice URL |
| `created_by` | uuid | China user who created |
| `created_at` | timestamp | Creation time |

#### `shipment_lines`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `shipment_id` | uuid | FK to shipments |
| `po_line_id` | uuid | FK to po_lines |
| `item_code` | text | SKU |
| `shipped_qty` | int | Qty in this shipment |
| `received_qty` | int | Qty confirmed received |

#### `supplier_invoices`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `shipment_id` | uuid | FK to shipments |
| `supplier` | text | Supplier name |
| `invoice_number` | text | Supplier's invoice # |
| `invoice_date` | date | Invoice date |
| `invoice_amount` | decimal | Total amount |
| `currency` | text | GBP, USD, CNY |
| `invoice_url` | text | PDF/image URL |
| `ocr_status` | text | PENDING, PROCESSING, COMPLETED, FAILED |
| `extracted_data` | jsonb | OCR-extracted fields |
| `xero_invoice_id` | text | Xero reference after posting |
| `xero_status` | text | NOT_POSTED, POSTED, ERROR |
| `uploaded_by` | uuid | China user |
| `uploaded_at` | timestamp | Upload time |

#### `users`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `email` | text | Login email |
| `name` | text | Display name |
| `role` | text | ADMIN, MANAGER, CHINA_OPS, WAREHOUSE |
| `site` | text | UK, FL, PH, CN |
| `language` | text | en, zh, tl, es |
| `slack_user_id` | text | For notifications |

### 4.2 Views

#### `v_reorder_queue`
Calculated view showing items needing reorder:
- Items with `days_of_stock < 21`
- **Excluded:** `is_excluded = false` (no z-prefix, not stale)
- Sorted by priority (RED first, then AMBER)
- Shows suggested order qty based on velocity
- **Access:** Managers/Admins only

#### `v_warehouse_top_selling`
Warehouse staff view — top selling items with stock:
- Top 50 items by `sales_last_30d` per warehouse
- Current `free_stocks` level
- Traffic light status (RED/AMBER/GREEN/BLACK)
- **Excluded:** `is_excluded = false`
- **Access:** Warehouse staff (own site only)

#### `v_china_dashboard`
China office view:
- All APPROVED POs not yet shipped
- Items on order grouped by priority
- Overdue items highlighted

#### `v_shipment_tracking`
Real-time shipment status:
- In-transit shipments
- ETA calculations
- Delay alerts

---

## 5. User Roles & Permissions

| Role | Permissions |
|------|-------------|
| **ADMIN** | Full access, all sites |
| **MANAGER** | Approve POs, view all sites, manage users |
| **CHINA_OPS** | View approved POs, create shipments, upload docs, Mandarin UI |
| **WAREHOUSE** | View top-selling inventory, request stock adjustments, local site only |

---

## 6. Notification System

### 6.1 Slack Notifications
| Event | Channel | Message |
|-------|---------|---------|
| PO Approved | #procurement | PO-XXX approved for Supplier → Destination |
| Shipment Created | #logistics-uk / #logistics-fl / #logistics-ph | Shipment SH-XXX created, ETA: YYYY-MM-DD, Packing list attached |
| Shipment Delivered | Site channels | Shipment SH-XXX delivered, stock auto-added |
| Delivery Exception | #procurement-alerts | Shipment SH-XXX delay/exception |
| Low Stock Alert | Site channels | Item XXX at BLACK/RED level |

### 6.2 Email Notifications
- Daily digest of pending approvals (managers)
- Weekly reorder summary
- Exception reports

---

## 7. Technical Infrastructure

### 7.1 Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16 + TypeScript |
| Backend | Next.js API Routes |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| Storage | Supabase Storage (invoices/packing lists) |
| Notifications | Slack Webhooks + Email (SendGrid) |
| OCR | Tesseract / Google Vision API |
| Finance Integration | Xero API via Finance Agent |
| Deployment | Cloud Run |

### 7.2 External Integrations
| Service | Purpose |
|---------|---------|
| **BigQuery** | `zero_dataset.inventory` — canonical stock data |
| **Slack** | Notifications to UK/FL/PH teams |
| **Xero** | Supplier invoice posting (UK + US entities) |
| **Carrier APIs** | Tracking (DHL, FedEx, UPS) |
| **GDrive** | Document backup |

### 7.3 Cron Jobs
| Job | Schedule | Purpose |
|-----|----------|---------|
| `inventory-sync` | Every 2 hours | Sync from BigQuery to Supabase |
| `reorder-calculation` | Daily | Recalculate reorder queue |
| `shipment-tracking` | Every 4 hours | Update shipment statuses |
| `delivery-monitor` | Every hour | Check for delivered shipments |

---

## 8. China Stock Handling Question

### Option A: CN Warehouse → Transit → Destination (Recommended)
```
Supplier → CN Warehouse (receipt recorded) → Transit → UK/FL/PH (delivery recorded)
```
- **Pros:** Full visibility of stock location, accurate in-transit tracking
- **Cons:** More state transitions to manage

### Option B: On-Order Until Arrival (Simpler)
```
Supplier → (no tracking) → UK/FL/PH (delivery recorded)
```
- **Pros:** Simpler, less data to maintain
- **Cons:** No visibility of goods in China or in transit

**Recommendation:** Option A with automated state transitions:
1. China receives goods → `on_order` decreases, `cn_stock` increases
2. Shipment created → `cn_stock` decreases, `in_transit` increases
3. Delivery confirmed → `in_transit` decreases, `free_stocks` increases

---

## 9. UI/UX Requirements

### 9.1 Language Support
| Language | UI | Content |
|----------|-----|---------|
| English (EN) | ✅ Full | ✅ Full |
| Mandarin (ZH) | ✅ Full | POs, Packing Lists, Invoices |
| Tagalog (TL) | Optional | Notifications only |
| Spanish (ES) | Optional | Notifications only |

### 9.2 China Portal Screens (Mandarin)
1. **Dashboard** — Pending POs, shipments in progress, exception alerts
2. **PO List** — Downloadable by supplier, filterable by status
3. **Packing List Generator** — Select PO lines → generate PDF
4. **Shipment Creator** — Upload docs, add tracking, set ETA
5. **Items On Order** — Priority view with exception highlighting
6. **Invoice Upload** — Drag-drop, OCR preview, submit to finance

**China Staff CANNOT:**
- Create purchase orders
- Approve POs
- Adjust stock
- Access warehouse staff pages

### 9.3 Regional Portal Screens

#### Manager/Admin View (Full Access)
1. **Dashboard** — Stock alerts, incoming shipments, approval queue
2. **Inventory** — Site-specific stock levels with traffic lights
3. **Reorder Queue** — Auto-generated PO recommendations
4. **Shipment Tracker** — Inbound shipments from China
5. **PO Approval** — Approve/reject pending POs

#### Warehouse Staff View (Read-Only + Adjustments Only)
1. **Top Selling Items** — Site-specific, stock on hand, traffic light status
2. **Stock Adjustment** — Request damage/waste/count corrections only
3. **My Requests** — Track adjustment request status

**Warehouse Staff CANNOT:**
- Create purchase orders
- View reorder queue
- Approve POs
- Access China portal
- See other warehouses' data

---

## 10. Item Exclusion Rules

### 10.1 Z-Prefix Items (RETIRED/DISCONTINUED)
**Rule:** Always exclude items with `z-` or `Z-` prefix in `Item_Code`.

| Prefix | Meaning | Action |
|--------|---------|--------|
| `z-` | Retired/discontinued SKU | Exclude from all inventory views and reorder queue |
| `Z-` | Retired/discontinued SKU | Exclude from all inventory views and reorder queue |

**Implementation:**
```sql
WHERE LOWER(item_code) NOT LIKE 'z-%'
```

### 10.2 Stale Stock Items
**Definition:** Items with inventory but no sales velocity.

| Criteria | Threshold | Action |
|----------|-----------|--------|
| `sales_last_30d = 0` AND `sales_last_7d = 0` | No sales in 30 days | Flag as stale, exclude from reorder queue |
| `free_stocks > 100` AND `days_of_stock > 90` | Excess dead stock | Report to finance for write-off consideration |
| `last_sale_date < NOW() - INTERVAL '90 days'` | No sales in 90+ days | Exclude from reorder, flag for review |

**Stale Stock Report:**
Weekly automated report showing:
- Items with >90 days of stock at current velocity
- Items with zero sales in last 90 days
- Estimated carrying cost of stale inventory

### 10.3 Excluded Product Groups
| Product Group | Reason | Action |
|---------------|--------|--------|
| (To be defined) | — | Exclude from reorder |

---

## 11. Data Source Reference (CRITICAL)

### Canonical Inventory Data Source
**Always use:** `instant-contact-479316-i4.zero_dataset.inventory` (BigQuery VIEW)

| Property | Value |
|----------|-------|
| **Project** | `instant-contact-479316-i4` |
| **Dataset** | `zero_dataset` |
| **Table/View** | `inventory` (type: VIEW) |
| **Data freshness** | Live — updated daily from Sage |
| **Last verified** | 2026-04-11 |

### Canonical Demand Data Source (by Site)
**Always use:** `instant-contact-479316-i4.zero_dataset.orders.PO_Location`

| Property | Value |
|----------|-------|
| **Table** | `zero_dataset.orders` |
| **Column** | `PO_Location` |
| **Values** | `PH`, `UK`, `Florida`, `DE` |
| **Purpose** | Shows which warehouse *fulfilled* each order — actual demand by site |
| **Use case** | Calculate site-specific velocity, stock cover, reorder priorities |

**Critical distinction:**
- `inventory.Warehouse` = where stock is physically located
- `orders.PO_Location` = which site processed the sale (true demand signal)

### ⚠️ DO NOT USE — Stale/Legacy Tables
| Table | Status | Why |
|-------|--------|-----|
| `elcell_co_uk_barcode.t_sage_stock` | ❌ STALE | Last updated 2014 |
| `production_tracker.t_uk_stocks` | ❌ STALE | Not maintained |
| `production_tracker.t_fl_stocks` | ❌ STALE | Not maintained |

### Exclusion Rules (See Section 10)
1. **Z-prefix items** — Always exclude `z-` or `Z-` prefix in `Item_Code`
2. **Stale stock** — Exclude items with no sales in 30+ days from reorder queue
3. **Dead stock** — Flag items with >90 days of stock for finance review

---

## 11. Stock Adjustment Workflow with LLM Validation

### 11.1 Adjustment Types
| Type | Description | Accounting Treatment |
|------|-------------|---------------------|
| **Damage** | Physical damage in warehouse | Write-off to P&L |
| **Waste** | Production/printing waste | Write-off to P&L |
| **Count Correction** | Physical count vs system mismatch | Inventory adjustment |
| **Receipt Correction** | Wrong qty received | Adjust PO receipt |

### 11.2 LLM Validation Logic
When warehouse submits adjustment, LLM checks:

```
VALIDATION CHECKS:
├── Recent Activity Check
│   ├── Was stock received in last 5 days? (may not be processed yet, accounts for weekends)
│   ├── Is there an open shipment for this item? (in transit confusion)
│   └── Was there a recent stock count? (count error vs actual loss)
├── Pattern Analysis
│   ├── Same item adjusted recently? (recurring issue)
│   ├── Same warehouse high adjustment rate? (process problem)
│   └── Unusual magnitude? (outlier detection)
├── Cross-Reference
│   ├── Check PO receipts for this item (did we receive less?)
│   ├── Check sales/shipment out (did we ship more?)
│   └── Check production records (waste logged?)
└── Confidence Score
    ├── HIGH (90%+) → Auto-approve small amounts, queue large
    ├── MEDIUM (70-90%) → Queue for manager review
    └── LOW (<70%) → Request additional documentation
```

### 11.3 LLM Prompt Template
```
You are validating a stock adjustment request.

REQUEST:
- Item: {item_code} - {description}
- Warehouse: {warehouse}
- Adjustment Type: {damage/waste/count_correction}
- Qty: {qty}
- Reason: {user_provided_reason}
- Requested by: {user} at {timestamp}

CONTEXT (last 30 days):
- Stock received: {receipts_json}
- Stock shipped: {shipments_json}
- Previous adjustments: {adjustments_json}
- Current system stock: {free_stocks}
- Last physical count: {last_count_date}

VALIDATE:
1. Is this likely legitimate? (Y/N/UNCERTAIN)
2. Confidence score (0-100)
3. Flags: [recent_receipt] [open_shipment] [pattern_match] [unusual_magnitude]
4. Suggested action: [auto_approve] [manager_review] [request_docs]
5. Explanation: (2-3 sentences)

Note: "recent_receipt" = stock received in last 5 days (accounts for weekend delays)
```

### 11.4 Approval Thresholds
| Adjustment Qty | Confidence | Action |
|---------------|------------|--------|
| ≤10 units | ≥90% | Auto-approve |
| ≤10 units | 70-90% | Manager review |
| ≤10 units | <70% | Request docs |
| 11-100 units | ≥95% | Auto-approve |
| 11-100 units | <95% | Manager review |
| >100 units | Any | CFO review + docs required |

### 11.5 Workflow Diagram
```
[Warehouse] → [Submit Adjustment] → [LLM Validation]
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
              [Auto-Approve]         [Manager Review]      [Request Docs]
                    │                      │                      │
                    ▼                      ▼                      ▼
              [Update Stock]          [Approve/Reject]    [Warehouse Uploads]
                    │                      │                      │
                    ▼                      ▼                      ▼
              [Post to Xero]          [Update Stock]      [LLM Re-evaluates]
                    │                      │                      │
                    └──────────────────────┴──────────────────────┘
                                           │
                                           ▼
                                    [Audit Log Entry]
```

### 11.6 Database Schema Additions

#### `stock_adjustments`
| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `item_code` | text | SKU |
| `warehouse` | text | UK, FL, PH |
| `adjustment_type` | text | DAMAGE, WASTE, COUNT_CORRECTION, RECEIPT_CORRECTION |
| `qty_change` | int | Positive (add) or negative (remove) |
| `reason` | text | User explanation |
| `llm_confidence` | int | 0-100 score |
| `llm_flags` | jsonb | {recent_receipt: bool, open_shipment: bool, ...} |
| `llm_explanation` | text | LLM reasoning |
| `status` | text | PENDING, AUTO_APPROVED, MANAGER_APPROVED, REJECTED, DOCS_REQUESTED |
| `requested_by` | uuid | User |
| `approved_by` | uuid | Approver (if manual) |
| `xero_journal_id` | text | Xero reference |
| `created_at` | timestamp | Request time |
| `approved_at` | timestamp | Approval time |

---

## 12. Distribution Logic Pseudocode

```typescript
// Calculate multi-site PO distribution
function calculateDistribution(itemCode: string, totalNeed: number): Distribution {
  const productType = getProductType(itemCode); // HTPCR, HLBWH, etc.
  
  // Check for internal transfer opportunity (PH → UK/FL only)
  const phStock = getStock('PH', itemCode);
  const flNeed = getStockOutRisk('FL', itemCode);
  const ukNeed = getStockOutRisk('UK', itemCode);
  
  // Internal transfer rules:
  // - PH can transfer TO UK or FL
  // - NO transfers between UK ↔ FL (high freight cost)
  // - CN is staging only — stock in CN is error/mistake
  if (phStock > 100 && (flNeed > 0 || ukNeed > 0)) {
    createInternalTransferRequest(itemCode, phStock, flNeed, ukNeed);
    // Reduce external PO qty by transfer amount
  }
  
  // Base distribution percentages
  let distribution = {
    FL: 0,
    UK: 0,
    PH: 0
  };
  
  // Apply product type rules
  if (['HTPCR', 'HC', 'HB401', 'H89', 'HDMWH'].includes(productType)) {
    // US product types - primarily FL, some PH
    distribution.FL = Math.floor(totalNeed * 0.6);
    distribution.PH = Math.floor(totalNeed * 0.4);
  } else if (productType === 'HLBWH') {
    // Wallet cases - primarily PH
    distribution.PH = Math.floor(totalNeed * 0.8);
    distribution.FL = Math.floor(totalNeed * 0.2);
  } else {
    // Default split
    distribution.FL = Math.floor(totalNeed * 0.375);
    distribution.UK = Math.floor(totalNeed * 0.375);
    distribution.PH = Math.floor(totalNeed * 0.25);
  }
  
  // Apply rounding (base 10 or 100)
  const roundingBase = totalNeed >= 1000 ? 100 : 10;
  distribution.FL = roundToBase(distribution.FL, roundingBase);
  distribution.UK = roundToBase(distribution.UK, roundingBase);
  distribution.PH = roundToBase(distribution.PH, roundingBase);
  
  // Ensure total matches (adjust largest)
  const roundedTotal = distribution.FL + distribution.UK + distribution.PH;
  if (roundedTotal !== totalNeed) {
    const diff = totalNeed - roundedTotal;
    const largest = getLargestSite(distribution);
    distribution[largest] += roundToBase(diff, roundingBase);
  }
  
  return distribution;
}

function roundToBase(value: number, base: number): number {
  return Math.round(value / base) * base;
}
```

---

## 13. Implementation Phases

### Phase 1: Foundation (Current)
- [x] Supabase schema
- [x] Basic inventory sync
- [ ] Item exclusion rules (z-prefix, stale stock)
- [ ] Stale stock detection and reporting
- [ ] Stock adjustment workflow with LLM validation
- [ ] PO creation workflow with multi-site distribution
- [ ] Shipping plan generation (CSV/PDF export for Ben)
- [ ] Rounding logic (base 10/100)
- [ ] Approval queue

### Phase 2: China Portal
- [ ] Mandarin UI
- [ ] PO download by supplier
- [ ] Packing list generation
- [ ] Shipment creation
- [ ] Document upload

### Phase 3: Logistics & Notifications
- [ ] Slack/email notifications
- [ ] Shipment tracking
- [ ] Delivery monitoring
- [ ] Auto stock receipt

### Phase 4: Finance Integration
- [ ] Invoice OCR
- [ ] Finance Agent integration
- [ ] Xero posting
- [ ] Exception handling

### Phase 5: Advanced Features
- [ ] Exception reports
- [ ] Priority algorithms
- [ ] Predictive reordering
- [ ] Supplier performance

---

## 14. Internal Stock Transfer Rules

### 14.1 Transfer Routes (Allowed)
| From | To | Allowed | Reason |
|------|-----|---------|--------|
| **PH** | UK | ✅ Yes | Cost-effective internal transfer |
| **PH** | FL | ✅ Yes | Cost-effective internal transfer |
| **UK** | FL | ❌ No | High freight cost — not economical |
| **FL** | UK | ❌ No | High freight cost — not economical |
| **CN** | Any | ⚠️ Staging only | CN is consolidation point, not storage |

### 14.2 CN Stock Alert
**If stock exists in CN warehouse:**
- Flag as **ERROR** — CN is staging/consolidation only
- Do NOT create transfer request
- Alert operations team for investigation
- Likely causes: missed packing list, shipment not created, data error

### 14.3 Transfer Trigger Logic
```
IF (FL stock-out risk OR UK stock-out risk) 
   AND PH stock > 100 units:
   
   → Create internal transfer request (PH → needy site)
   → Reduce external PO qty by transfer amount
   → Notify PH warehouse to prepare transfer
```

### 14.4 Transfer Request Fields
| Field | Description |
|-------|-------------|
| `item_code` | SKU to transfer |
| `from_warehouse` | Always "PH" |
| `to_warehouse` | "UK" or "FL" |
| `qty` | Transfer quantity (max available in PH) |
| `reason` | "Stock-out prevention — internal transfer" |
| `priority` | HIGH if destination stock < 7 days |
| `status` | PENDING → PICKED → SHIPPED → RECEIVED |

---

## 15. Open Questions

1. **China warehouse:** Do we need to track stock physically in China, or skip to transit?
2. **Carrier tracking:** Which carriers need API integration? (DHL, FedEx, UPS, others?)
3. **Invoice OCR:** Full automation or human verification step?
4. **Xero entities:** UK and US only, or separate for PH/CN?
5. **Approval thresholds:** Auto-approve POs under certain amount?

---

## 16. Files & Locations

| Resource | Local Path | GDrive |
|----------|------------|--------|
| Project Wiki | `wiki/inventory-ordering-app/PROJECT.md` | `Brain/Projects/inventory-ordering-app/wiki/` |
| App Code | `tmp/procurement-system/` | `Brain/Projects/inventory-ordering-app/code/` |
| Database Schema | `sql/procurement_schema.sql` | TBD |
| Sync Scripts | `scripts/bq_to_supabase_inventory_sync.mjs` | TBD |

---

*Updated: 2026-04-13 | Version 2.6 — Internal stock transfer rules added*
