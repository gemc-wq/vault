# Handoff: Inventory Dashboard + Procurement Layer
**From:** Ava (Planner) → **To:** Harry (Builder)
**Date:** 2026-03-12
**Priority:** P0 — build this week

---

## Context
Ava built the inventory data foundation today. Your job is to build the procurement/finance layer on top of it and ship a working dashboard.

---

## What Already Exists (DO NOT rebuild)

### Supabase Project
- URL: `https://auzjmawughepxbtpwuhe.supabase.co`
- Service role key: `[REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc`
- Direct psql: `postgresql://postgres:[REDACTED_DB_PASSWORD]@db.auzjmawughepxbtpwuhe.supabase.co:5432/postgres`
- ⚠️ Session pooler does NOT work. Use direct connection only.

### Table: `blank_inventory`
- **5,193 rows** (3 warehouses × unique blank SKUs)
- **Only ~1,210 are active** (have sales in last 30 days)
- **~3,980 are dead stock** (stock on shelf, zero sales)
- Columns: warehouse, item_code, product_group, description, supplier, free_stocks, snapshot_stocks, sales_last_30d, sales_last_7d, avg_daily_sales, reorder_level, on_order, last_po_date, last_po_qty, avg_po_price (COGS), snapshot_date, last_deduction_date
- Unique key: `(warehouse, item_code)`
- Data source: BQ `zero_dataset.inventory` snapshot taken 2026-03-12

### Views
- `v_inventory_alerts_v2` — per-site alerts (BLACK/RED/YELLOW/GREEN)
- `v_inventory_global` — aggregated across all sites with `stock_by_site` JSON column

### Automated Scripts (running nightly)
1. `sync_bq_orders.py` — BQ orders → Supabase `orders` table (1 AM EST)
2. `deduct_inventory.py` — subtracts today's orders from `blank_inventory.free_stocks` (runs after sync)
3. `snapshot_inventory.py` — refreshes BQ inventory snapshot (run manually when needed)

### Key Data Facts
- `item_code` has TWO formats: `HTPCR-IPH16` (with product prefix) or `IPH16` (device-only, for HC/PC items)
- `avg_daily_sales` is GLOBAL demand (not per-site)
- Site capability constraints: H89/HST/HDM → never PH. PH does UV-printable cases only.
- Skins (H89/H90) at 9,999 units = unlimited roll stock, not discrete inventory
- BQ inventory has `Average_PO_Price` = COGS per blank unit

---

## What You Build

### Phase 1: Dashboard + Reorder Suggestions (this week)

**Dashboard UI** (Next.js, your usual stack):
1. **Active Inventory** — the ~1,210 active SKUs with alert levels, days-of-stock, stock-by-site
2. **Fast Movers** — top items by daily sales rate
3. **Critical Alerts** — RED and BLACK items (< 1 week stock or zero)
4. **Aged/Dead Stock** — the 3,980 items with stock but no sales (tag for write-off review)

**Reorder Engine:**
- Use this formula (from your plan, approved):
  - `demandSignalDaily = max(avgDailyUsage7d, avgDailyUsage30d)`
  - `leadTimeDays = 21` (default, override per supplier later)
  - `safetyDays = 14` fast movers, `7` regular
  - `suggestedOrderUnits = max(0, reorderPoint - onHand)`
- Generate suggested reorder lines → approval queue

**New Supabase tables (Phase 1):**
```sql
-- Reorder suggestions (auto-generated)
CREATE TABLE reorder_suggestions (
  id BIGSERIAL PRIMARY KEY,
  item_code TEXT NOT NULL,
  warehouse TEXT NOT NULL,
  suggested_qty INTEGER NOT NULL,
  demand_signal_daily NUMERIC(10,2),
  days_of_stock INTEGER,
  current_stock INTEGER,
  reorder_point INTEGER,
  status TEXT DEFAULT 'pending', -- pending/approved/rejected/ordered
  created_at TIMESTAMPTZ DEFAULT now(),
  approved_at TIMESTAMPTZ,
  approved_by TEXT,
  notes TEXT
);

-- PO batches (internal approval object)  
CREATE TABLE po_batches (
  id BIGSERIAL PRIMARY KEY,
  batch_date DATE NOT NULL DEFAULT CURRENT_DATE,
  status TEXT DEFAULT 'draft', -- draft/approved/sent
  total_lines INTEGER,
  total_units INTEGER,
  created_at TIMESTAMPTZ DEFAULT now(),
  approved_at TIMESTAMPTZ,
  notes TEXT
);

-- Supplier POs (one per supplier per batch)
CREATE TABLE po_supplier_orders (
  id BIGSERIAL PRIMARY KEY,
  batch_id BIGINT REFERENCES po_batches(id),
  supplier TEXT NOT NULL,
  status TEXT DEFAULT 'draft', -- draft/sent/acknowledged/in_production/shipped/in_transit/received
  sent_at TIMESTAMPTZ,
  expected_delivery DATE,
  tracking_info TEXT,
  notes TEXT
);

-- PO line items
CREATE TABLE po_order_lines (
  id BIGSERIAL PRIMARY KEY,
  supplier_order_id BIGINT REFERENCES po_supplier_orders(id),
  suggestion_id BIGINT REFERENCES reorder_suggestions(id),
  item_code TEXT NOT NULL,
  warehouse TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price NUMERIC(10,2), -- from avg_po_price
  total_price NUMERIC(10,2),
  received_qty INTEGER DEFAULT 0
);
```

### Phase 2: Finance Layer (next week)

**After PO workflow is working**, add:
```sql
CREATE TABLE goods_receipts (
  id BIGSERIAL PRIMARY KEY,
  supplier_order_id BIGINT REFERENCES po_supplier_orders(id),
  received_date DATE NOT NULL,
  item_code TEXT NOT NULL,
  received_qty INTEGER NOT NULL,
  notes TEXT
);
-- On receipt: UPDATE blank_inventory SET free_stocks = free_stocks + received_qty

CREATE TABLE supplier_invoices (
  id BIGSERIAL PRIMARY KEY,
  supplier_order_id BIGINT REFERENCES po_supplier_orders(id),
  invoice_number TEXT,
  invoice_date DATE,
  amount NUMERIC(12,2),
  currency TEXT DEFAULT 'USD',
  status TEXT DEFAULT 'pending', -- pending/approved/paid
  matched BOOLEAN DEFAULT false
);

CREATE TABLE supplier_payments (
  id BIGSERIAL PRIMARY KEY,
  invoice_id BIGINT REFERENCES supplier_invoices(id),
  payment_date DATE,
  amount NUMERIC(12,2),
  method TEXT, -- bank_transfer/paypal/etc
  reference TEXT
);
```

---

## Critical Rules

1. **Read from `blank_inventory`** for stock data. Do NOT re-query BQ inventory.
2. **When goods are received**, UPDATE `blank_inventory.free_stocks += received_qty`. This is how stock goes UP. Orders deductions (Ava's script) are how stock goes DOWN.
3. **Aged units = items where sales_last_30d = 0 AND free_stocks > 0**. There are 3,980 of these.
4. **Skin blanks (H89/H90) at 9,999** are effectively unlimited roll stock. Consider excluding from reorder logic or flagging differently.
5. **Site capabilities:** H89, HST, HDM → never PH. PH = UV cases only. UK/FL do everything.
6. **Supplier field** is already in `blank_inventory` — use it for PO splits.
7. Deploy to Vercel, same team (`ecells-projects-3c3b03d7`). Git author: `gemc99@me.com`.

---

## Definition of Done (Phase 1)
- [ ] Dashboard showing active inventory with alert levels
- [ ] Reorder suggestion engine running against live data
- [ ] Approval UI (approve/reject/edit qty)
- [ ] PO batch creation from approved lines
- [ ] Supplier PO split (grouped by supplier)
- [ ] Deployed and accessible

**Ship target: Mar 19**

---

*Questions → ask Cem or write to handoffs folder. Ava will review all output before it goes live.*
