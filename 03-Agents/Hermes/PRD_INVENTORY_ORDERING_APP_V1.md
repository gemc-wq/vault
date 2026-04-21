# Inventory Ordering App — Product Requirements Document (PRD)
**Version:** 1.0 | **Date:** 2026-04-13
**Author:** Hermes (synthesizing Athena, Codex, Ava, and PROJECT v2.6)
**Status:** DRAFT — Pending Cem Approval

---

## 0. EXECUTIVE DECISION REQUIRED

**Three documents agree on one thing: the current Supabase setup is NOT production-ready.**

| Issue | Source | Severity | Blocks Build? |
|-------|--------|----------|---------------|
| Velocity uses 7d only (over-orders 126%) | Athena | CRITICAL | YES |
| 70% of orders missing from Supabase | Athena | CRITICAL | YES |
| FL vs Florida warehouse duplication | Athena | CRITICAL | YES |
| 78% DISC items polluting all queries | Athena | HIGH | YES |
| Harry's POC "not up to the job" | Cem | CRITICAL | YES |
| No AMBER alerts (GREEN→RED only) | Athena | MEDIUM | NO |

**RECOMMENDATION:** Before any app development, complete **Data Foundation Sprint (1 week)** to fix these issues. Then proceed to **App Build Sprint (3 weeks)**.

---

## 1. PRODUCT VISION

Replace manual Excel-based procurement with an automated, trustworthy system that:
1. **Never over-orders** (blended velocity, not just 7-day spikes)
2. **Never misses real demand** (uses BigQuery-sourced data, not incomplete Supabase orders)
3. **Distributes stock intelligently** (FL/UK/PH split based on actual fulfillment patterns)
4. **Closes the finance loop** (PO → shipment → receipt → Xero)

---

## 2. SYNTHESIS: RESOLVING THE CONFLICTS

### 2.1 Ava vs Codex: MVP Approach

| Position | Ava | Codex | Hermes Resolution |
|----------|-----|-------|-------------------|
| Timeline | 2-week MVP | 3-week full Phase 1 | **3 weeks** (Codex is right on risk) |
| LLM validation | Phase 3 | Phase 1 (high blast radius) | **Phase 2** (but ship simple approval first) |
| China portal | Phase 2 | Phase 1 (operational core) | **Phase 1** (China IS the bottleneck) |
| Xero integration | Phase 3 | Phase 1 (finance trust) | **Phase 2** (but design schema now) |
| Slack approval | Primary | Risky (no audit trail) | **App-first, Slack notify** |

**Resolution:** Codex's critique is correct. Ava's MVP creates "front-end automation with back-end manual improvisation." The China office processes every PO. Without China tooling, the bottleneck moves from Excel to Slack notifications.

### 2.2 Data Issues: What Athena Found

Athena's data integrity report is **blocking**. Key findings:

| Finding | Impact | Fix Required |
|---------|--------|--------------|
| `avg_daily_sales = sales_last_7d / 7` | Over-orders 126% on spikes | Implement blended velocity |
| Supabase `orders` = 30% of actual | Under-orders 70% | Use `blank_inventory` velocity, NOT orders |
| `FL` vs `Florida` codes | Distribution logic fails | Normalise warehouse codes |
| 32,428 DISC items | Noise in all queries | Add `product_group != 'DISC'` filter |
| 95 active stock-outs in PH | Revenue at risk | Flag for immediate reorder |

---

## 3. DATA FOUNDATION SPRINT (Week 1)

**Goal:** Fix critical data issues so the app has a trustworthy foundation.

### 3.1 Warehouse Code Normalisation

**Problem:** Two codes for Florida:
- `Florida`: 10,337 items (99%)
- `FL`: 99 items (1%)

**Fix:**
```sql
-- Normalise to 'Florida' as canonical
UPDATE blank_inventory SET warehouse = 'Florida' WHERE warehouse = 'FL';

-- Add constraint to prevent future variations
ALTER TABLE blank_inventory ADD CONSTRAINT valid_warehouse 
  CHECK (warehouse IN ('UK', 'PH', 'Florida', 'Transit'));
```

### 3.2 Velocity Calculation Fix

**Problem:** `avg_daily_sales = sales_last_7d / 7` causes 126% over-ordering on spikes.

**Solution:** Implement tiered velocity from Best Sellers Staging Spec:

```sql
-- Add columns to blank_inventory
ALTER TABLE blank_inventory ADD COLUMN velocity_7d NUMERIC(10,2);
ALTER TABLE blank_inventory ADD COLUMN velocity_30d NUMERIC(10,2);
ALTER TABLE blank_inventory ADD COLUMN velocity_blended NUMERIC(10,2);
ALTER TABLE blank_inventory ADD COLUMN is_best_seller BOOLEAN DEFAULT FALSE;

-- Calculate velocities
UPDATE blank_inventory SET
  velocity_7d = ROUND(COALESCE(sales_last_7d::numeric / 7, 0), 2),
  velocity_30d = ROUND(COALESCE(sales_last_30d::numeric / 30, 0), 2),
  velocity_blended = ROUND(
    GREATEST(
      COALESCE(sales_last_7d::numeric / 7, 0),
      COALESCE(sales_last_30d::numeric / 30, 0)
    ), 2
  );

-- Mark best sellers (top 50 per warehouse by velocity)
WITH ranked AS (
  SELECT id,
    ROW_NUMBER() OVER (
      PARTITION BY warehouse 
      ORDER BY velocity_blended DESC
    ) AS rank
  FROM blank_inventory
  WHERE product_group != 'DISC'
    AND sales_last_30d > 0
)
UPDATE blank_inventory b
SET is_best_seller = TRUE
FROM ranked r
WHERE b.id = r.id AND r.rank <= 50;
```

### 3.3 Create Best Sellers Daily Table

From Best Sellers Staging Spec:

```sql
CREATE TABLE best_sellers_daily (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_code       TEXT NOT NULL,
    warehouse       TEXT NOT NULL,
    rank            INT NOT NULL,
    velocity_7d     NUMERIC(10,2),
    velocity_30d    NUMERIC(10,2),
    velocity_used   NUMERIC(10,2),
    sales_last_7d   INT,
    sales_last_30d  INT,
    free_stocks     INT,
    days_of_cover   NUMERIC(10,1),
    stock_risk      TEXT,  -- CRITICAL / LOW / OK
    reorder_qty     INT,
    snapshot_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(item_code, warehouse, snapshot_date)
);

CREATE INDEX idx_bs_daily_date ON best_sellers_daily(snapshot_date);
CREATE INDEX idx_bs_daily_item ON best_sellers_daily(item_code);
```

### 3.4 Fix Alert System

**Problem:** No AMBER alerts. Items go GREEN → RED with no warning.

**Fix:**
```sql
-- Recalculate alert levels with AMBER
UPDATE blank_inventory SET
  alert_level = CASE
    WHEN free_stocks = 0 THEN 'BLACK'
    WHEN days_of_stock < 7 THEN 'RED'
    WHEN days_of_stock < 14 THEN 'AMBER'
    WHEN days_of_stock < 21 THEN 'YELLOW'
    ELSE 'GREEN'
  END;
```

### 3.5 Document Data Source Rules

**CRITICAL RULE:** The procurement app MUST use `blank_inventory` velocity columns for reorder calculations. NEVER calculate velocity from the Supabase `orders` table (it's 70% incomplete).

```
DATA FLOW:
AWS MySQL (canonical orders)
    ↓ Datastream (real-time)
BigQuery zero_dataset.inventory
    ↓ Sync Job (2hr)
Supabase blank_inventory ← USE THIS for velocity
    (sales_last_7d, sales_last_30d, velocity_blended)

Supabase orders table ← INCOMPLETE (~30% of actual)
    DO NOT USE for velocity calculations
```

---

## 4. APP BUILD SPRINT (Weeks 2-4)

### 4.1 Phase 1A: Core Procurement (Week 2)

**Goal:** Auto-generate reorder POs with multi-site distribution.

#### Feature 1.1: Reorder Queue

**View: `v_reorder_queue`**
```sql
CREATE VIEW v_reorder_queue AS
SELECT 
  item_code,
  warehouse,
  description,
  product_group,
  supplier,
  free_stocks,
  velocity_blended AS daily_velocity,
  ROUND(free_stocks / NULLIF(velocity_blended, 0), 1) AS days_of_stock,
  alert_level,
  is_best_seller,
  -- Calculate reorder qty: 56 days cover - current stock
  GREATEST(0,
    CASE 
      WHEN velocity_blended * 56 - free_stocks >= 1000
      THEN CEIL((velocity_blended * 56 - free_stocks) / 100) * 100
      ELSE CEIL((velocity_blended * 56 - free_stocks) / 10) * 10
    END
  )::INT AS suggested_reorder_qty
FROM blank_inventory
WHERE product_group != 'DISC'
  AND sales_last_30d > 0
  AND velocity_blended > 0
  AND (
    free_stocks = 0  -- BLACK: stock-out
    OR free_stocks / velocity_blended < 21  -- < 3 weeks cover
  )
ORDER BY 
  CASE alert_level
    WHEN 'BLACK' THEN 1
    WHEN 'RED' THEN 2
    WHEN 'AMBER' THEN 3
    ELSE 4
  END,
  velocity_blended DESC;
```

#### Feature 1.2: Multi-Site Distribution Logic

**Function: `calculate_distribution()`**
```typescript
interface Distribution {
  FL: number;
  UK: number;
  PH: number;
}

function calculateDistribution(
  itemCode: string, 
  totalNeed: number,
  productType: string
): Distribution {
  
  // Internal transfer check: can PH transfer to FL/UK?
  // (This is Phase 1B feature - just stub for now)
  
  const distribution = { FL: 0, UK: 0, PH: 0 };
  
  // Product type routing rules
  if (['HTPCR', 'HC', 'HB401', 'H89', 'HDMWH'].includes(productType)) {
    // US product types - primarily FL, some PH
    distribution.FL = Math.floor(totalNeed * 0.6);
    distribution.PH = Math.floor(totalNeed * 0.4);
  } else if (productType === 'HLBWH') {
    // Wallet cases - primarily PH
    distribution.PH = Math.floor(totalNeed * 0.8);
    distribution.FL = Math.floor(totalNeed * 0.2);
  } else {
    // Default split (for UK/ROW items)
    distribution.UK = totalNeed;  // All to UK
  }
  
  // Apply rounding
  const base = totalNeed >= 1000 ? 100 : 10;
  distribution.FL = roundToBase(distribution.FL, base);
  distribution.UK = roundToBase(distribution.UK, base);
  distribution.PH = roundToBase(distribution.PH, base);
  
  // Reconcile total
  const total = distribution.FL + distribution.UK + distribution.PH;
  if (total !== totalNeed) {
    const diff = totalNeed - total;
    const largest = getLargestSite(distribution);
    distribution[largest] += roundToBase(diff, base);
  }
  
  return distribution;
}

function roundToBase(value: number, base: number): number {
  return Math.round(value / base) * base;
}
```

#### Feature 1.3: PO Creation with Shipping Plan

**Tables: `purchase_orders`, `po_lines`**

```sql
CREATE TABLE purchase_orders (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  po_number       TEXT UNIQUE NOT NULL,  -- PO-YYYYMMDD-XXX
  supplier        TEXT NOT NULL,
  status          TEXT DEFAULT 'DRAFT',  -- DRAFT/PENDING/APPROVED/SENT/PARTIAL/RECEIVED/CANCELLED
  currency        TEXT DEFAULT 'USD',
  total_amount    NUMERIC(12,2),
  distribution_json JSONB,  -- {FL: qty, UK: qty, PH: qty}
  shipping_plan_url TEXT,
  rounding_base   INT DEFAULT 10,
  created_by      UUID,
  approved_by     UUID,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  approved_at     TIMESTAMPTZ,
  sent_at         TIMESTAMPTZ,
  expected_delivery DATE,
  notes           TEXT
);

CREATE TABLE po_lines (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  po_id           UUID REFERENCES purchase_orders(id) ON DELETE CASCADE,
  item_code       TEXT NOT NULL,
  description     TEXT,
  quantity        INT NOT NULL,
  quantity_fl     INT DEFAULT 0,
  quantity_uk     INT DEFAULT 0,
  quantity_ph     INT DEFAULT 0,
  unit_price      NUMERIC(10,2),
  line_total      NUMERIC(12,2),
  received_qty    INT DEFAULT 0,
  product_type    TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_po_lines_po ON po_lines(po_id);
CREATE INDEX idx_po_lines_item ON po_lines(item_code);
```

#### Feature 1.4: Shipping Plan Export (CSV/PDF)

**Format for Ben:**
```csv
Item_Code,Description,Total_Qty,FL_Qty,UK_Qty,PH_Qty,Supplier,Currency,Unit_Price,Line_Total
HTPCR-IPH15P,TPU iPhone 15 Pro,1000,600,0,400,XINTAI,USD,0.48,480.00
HLBWH-IPH15P,Leather Wallet iPhone 15 Pro,500,0,0,500,ECELLSZ,USD,0.92,460.00
```

**PDF Generation:** Use PDFKit or similar. Include:
- PO header (number, date, supplier, total)
- Line items table
- Distribution summary
- Signature/approval box

---

### 4.2 Phase 1B: Approval Workflow (Week 3)

**Goal:** Managers approve/reject POs with audit trail.

#### Feature 1.5: In-App Approval Queue

**NOT Slack-first (per Codex critique).** Slack notifies, app approves.

**View: `v_pending_approvals`**
```sql
CREATE VIEW v_pending_approvals AS
SELECT 
  po.id,
  po.po_number,
  po.supplier,
  po.total_amount,
  po.currency,
  po.created_at,
  COUNT(pl.id) AS line_count,
  SUM(pl.quantity) AS total_units,
  u.name AS created_by_name
FROM purchase_orders po
LEFT JOIN po_lines pl ON pl.po_id = po.id
LEFT JOIN users u ON u.id = po.created_by
WHERE po.status = 'PENDING'
GROUP BY po.id, po.po_number, po.supplier, po.total_amount, 
         po.currency, po.created_at, u.name
ORDER BY po.created_at DESC;
```

#### Feature 1.6: Approval API

```typescript
// POST /api/purchase-orders/:id/approve
async function approvePO(poId: string, userId: string): Promise<PO> {
  // 1. Update PO status
  const po = await db.update('purchase_orders', {
    id: poId,
    status: 'APPROVED',
    approved_by: userId,
    approved_at: new Date()
  });
  
  // 2. Generate shipping plan CSV/PDF
  const shippingPlanUrl = await generateShippingPlan(po);
  await db.update('purchase_orders', { id: poId, shipping_plan_url: shippingPlanUrl });
  
  // 3. Notify China team (Slack + email)
  await notifyChinaTeam(po, shippingPlanUrl);
  
  // 4. Update inventory: on_order += quantity
  for (const line of po.lines) {
    await db.query(`
      UPDATE blank_inventory 
      SET on_order = on_order + $1 
      WHERE item_code = $2
    `, [line.quantity, line.item_code]);
  }
  
  return po;
}

// POST /api/purchase-orders/:id/reject
async function rejectPO(poId: string, userId: string, reason: string): Promise<PO> {
  return db.update('purchase_orders', {
    id: poId,
    status: 'REJECTED',
    notes: reason,
    approved_by: userId,
    approved_at: new Date()
  });
}
```

#### Feature 1.7: Slack Notification (Not Approval)

**Per Codex critique:** Slack for notifications, not for approval actions. Approval happens in-app for audit trail.

```typescript
async function notifyManagerOfPendingPO(po: PO): Promise<void> {
  await slack.postMessage({
    channel: '#procurement',
    text: `PO ${po.po_number} pending approval`,
    blocks: [
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*PO ${po.po_number}* pending approval\n` +
                `Supplier: ${po.supplier}\n` +
                `Items: ${po.line_count} SKUs\n` +
                `Total: ${po.currency} ${po.total_amount}`
        }
      },
      {
        type: 'actions',
        elements: [
          {
            type: 'button',
            text: { type: 'plain_text', text: 'Review in App' },
            url: `https://ecell.app/procurement/po/${po.id}`
          }
        ]
      }
    ]
  });
}
```

---

### 4.3 Phase 1C: China Portal (Week 4)

**Goal:** China team can download POs, create shipments, upload docs.

**Per Codex:** China IS the operational core. Deferring this creates bottleneck.

#### Feature 1.8: China Dashboard (Mandarin)

**Screens:**
1. **PO List** — Download by supplier, filter by status
2. **Packing List Generator** — Select PO lines → generate PDF
3. **Shipment Creator** — Add tracking, carrier, ETA
4. **Document Upload** — Packing list + supplier invoice

#### Feature 1.9: Shipment Tracking

**Tables: `shipments`, `shipment_lines`**

```sql
CREATE TABLE shipments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  shipment_number TEXT UNIQUE NOT NULL,  -- SH-YYYYMMDD-XXX
  po_ids          UUID[],  -- Multiple POs per shipment
  origin          TEXT DEFAULT 'CN',
  destination     TEXT NOT NULL,  -- Florida, UK, PH
  carrier         TEXT,  -- DHL, FedEx, UPS
  tracking_number TEXT,
  status          TEXT DEFAULT 'PREPARING',  -- PREPARING/IN_TRANSIT/DELIVERED/EXCEPTION
  ship_date       DATE,
  eta             DATE,
  delivered_at    TIMESTAMPTZ,
  packing_list_url TEXT,
  invoice_url     TEXT,
  created_by      UUID,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE shipment_lines (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  shipment_id     UUID REFERENCES shipments(id) ON DELETE CASCADE,
  po_line_id      UUID REFERENCES po_lines(id),
  item_code       TEXT NOT NULL,
  shipped_qty     INT NOT NULL,
  received_qty    INT DEFAULT 0
);
```

#### Feature 1.10: Auto Stock Receipt

When shipment marked DELIVERED:
```sql
-- Trigger: auto-add stock to destination warehouse
CREATE OR REPLACE FUNCTION on_shipment_delivered()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'DELIVERED' AND OLD.status != 'DELIVERED' THEN
    -- Add stock to destination warehouse
    UPDATE blank_inventory b
    SET 
      free_stocks = free_stocks + s.shipped_qty,
      on_order = GREATEST(0, on_order - s.shipped_qty)
    FROM shipment_lines s
    WHERE s.shipment_id = NEW.id
      AND b.item_code = s.item_code
      AND b.warehouse = NEW.destination;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_shipment_delivered
AFTER UPDATE ON shipments
FOR EACH ROW EXECUTE FUNCTION on_shipment_delivered();
```

---

### 4.4 Phase 2: Intelligence & Finance (Weeks 5-6)

#### Feature 2.1: Internal Transfer Rules

**PH → UK/FL transfers** (not UK ↔ FL due to freight cost):
```sql
CREATE TABLE internal_transfers (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  item_code       TEXT NOT NULL,
  from_warehouse  TEXT NOT NULL,  -- Always 'PH'
  to_warehouse    TEXT NOT NULL,  -- 'UK' or 'Florida'
  qty             INT NOT NULL,
  status          TEXT DEFAULT 'PENDING',  -- PENDING/PICKED/SHIPPED/RECEIVED
  priority        TEXT,  -- HIGH if destination stock < 7 days
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  shipped_at      TIMESTAMPTZ,
  received_at     TIMESTAMPTZ
);
```

**Logic:**
```typescript
function checkInternalTransferOpportunity(
  itemCode: string
): InternalTransfer | null {
  const phStock = getStock('PH', itemCode);
  const flStock = getStock('Florida', itemCode);
  const ukStock = getStock('UK', itemCode);
  
  const flVelocity = getVelocity('Florida', itemCode);
  const ukVelocity = getVelocity('UK', itemCode);
  
  const flNeed = flStock < flVelocity * 21 ? flVelocity * 56 - flStock : 0;
  const ukNeed = ukStock < ukVelocity * 21 ? ukVelocity * 56 - ukStock : 0;
  
  if (phStock > 100 && (flNeed > 0 || ukNeed > 0)) {
    return {
      itemCode,
      fromWarehouse: 'PH',
      toWarehouse: flNeed > ukNeed ? 'Florida' : 'UK',
      qty: Math.min(phStock - 100, Math.max(flNeed, ukNeed)),
      priority: (flStock < flVelocity * 7 || ukStock < ukVelocity * 7) ? 'HIGH' : 'NORMAL'
    };
  }
  
  return null;
}
```

#### Feature 2.2: Stock Adjustment with LLM Validation

**Per Codex:** "Low-frequency but high-blast-radius."

**Table: `stock_adjustments`**
```sql
CREATE TABLE stock_adjustments (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  item_code         TEXT NOT NULL,
  warehouse         TEXT NOT NULL,
  adjustment_type   TEXT NOT NULL,  -- DAMAGE/WASTE/COUNT_CORRECTION
  qty_change        INT NOT NULL,  -- Negative for removal
  reason            TEXT,
  llm_confidence    INT,  -- 0-100
  llm_flags         JSONB,  -- {recent_receipt: bool, open_shipment: bool}
  llm_explanation   TEXT,
  status            TEXT DEFAULT 'PENDING',  -- PENDING/AUTO_APPROVED/MANAGER_APPROVED/REJECTED
  requested_by      UUID,
  approved_by       UUID,
  xero_journal_id   TEXT,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  approved_at       TIMESTAMPTZ
);
```

**LLM Validation Logic:**
```typescript
async function validateAdjustment(request: AdjustmentRequest): Promise<ValidationResult> {
  const context = await gatherContext(request.itemCode, request.warehouse);
  
  const prompt = `You are validating a stock adjustment request.

REQUEST:
- Item: ${request.itemCode}
- Warehouse: ${request.warehouse}
- Type: ${request.adjustmentType}
- Qty: ${request.qtyChange}
- Reason: ${request.reason}

CONTEXT (last 30 days):
- Stock received: ${context.receipts}
- Stock shipped: ${context.shipments}
- Previous adjustments: ${context.adjustments}
- Current system stock: ${context.currentStock}

VALIDATE:
1. Is this legitimate? (Y/N/UNCERTAIN)
2. Confidence (0-100)
3. Flags: ${JSON.stringify(context.flags)}
4. Action: auto_approve / manager_review / request_docs
5. Explanation (2-3 sentences)

Note: "recent_receipt" = stock received in last 5 days (accounts for weekend)`;

  const response = await llm.complete(prompt);
  return parseValidation(response);
}
```

#### Feature 2.3: Supplier Invoice → Xero

**Per Codex:** "Finance closure is not optional at go-live."

**Table: `supplier_invoices`**
```sql
CREATE TABLE supplier_invoices (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  shipment_id     UUID REFERENCES shipments(id),
  supplier        TEXT NOT NULL,
  invoice_number  TEXT,
  invoice_date    DATE,
  amount          NUMERIC(12,2),
  currency        TEXT DEFAULT 'USD',
  invoice_url     TEXT,
  ocr_status      TEXT DEFAULT 'PENDING',
  ocr_data        JSONB,
  xero_invoice_id TEXT,
  xero_status     TEXT DEFAULT 'NOT_POSTED',
  uploaded_by     UUID,
  uploaded_at     TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 5. SUPABASE SCHEMA: COMPLETE SETUP

Harry's POC is incomplete. Here's the full schema:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Core tables (from above)
CREATE TABLE blank_inventory (...);
CREATE TABLE best_sellers_daily (...);
CREATE TABLE purchase_orders (...);
CREATE TABLE po_lines (...);
CREATE TABLE shipments (...);
CREATE TABLE shipment_lines (...);
CREATE TABLE internal_transfers (...);
CREATE TABLE stock_adjustments (...);
CREATE TABLE supplier_invoices (...);

-- Users table
CREATE TABLE users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT UNIQUE NOT NULL,
  name          TEXT,
  role          TEXT NOT NULL,  -- ADMIN/MANAGER/CHINA_OPS/WAREHOUSE
  site          TEXT,  -- UK/Florida/PH/CN
  language      TEXT DEFAULT 'en',  -- en/zh/tl/es
  slack_user_id TEXT,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Views
CREATE VIEW v_reorder_queue AS ...;
CREATE VIEW v_pending_approvals AS ...;
CREATE VIEW v_best_sellers AS
  SELECT * FROM best_sellers_daily WHERE snapshot_date = CURRENT_DATE;

-- Functions
CREATE OR REPLACE FUNCTION calculate_velocity(...) ...;
CREATE OR REPLACE FUNCTION on_shipment_delivered() ...;

-- Cron jobs (pg_cron)
SELECT cron.schedule(
  'update-best-sellers',
  '30 6 * * *',  -- 06:30 UTC daily
  $$DELETE FROM best_sellers_daily WHERE snapshot_date = CURRENT_DATE; INSERT INTO ...$$
);
```

---

## 6. CRON SCHEDULE

| Job | Schedule | Purpose |
|-----|----------|---------|
| `inventory-sync` | 02:00 UTC | BigQuery → Supabase blank_inventory |
| `best-sellers-update` | 06:30 UTC | Recalculate top 50 per warehouse |
| `reorder-calc` | 07:00 UTC | Generate PO drafts from queue |
| `stock-alerts` | 08:00 UTC | Email BLACK/RED items to managers |
| `shipment-tracking` | Every 4h | Update shipment statuses from carrier APIs |

---

## 7. TESTING PLAN

### 7.1 Data Validation Tests

| Test | Expected | Owner |
|------|----------|-------|
| Warehouse normalisation | 0 items with 'FL' code | Week 1 |
| Velocity calculation | blended = MAX(7d, 30d) | Week 1 |
| Best seller tagging | 50 items per warehouse | Week 1 |
| Alert levels | AMBER exists between GREEN and RED | Week 1 |

### 7.2 Functional Tests

| Test | Expected | Owner |
|------|----------|-------|
| Reorder queue | Only non-DISC, active items | Week 2 |
| Distribution logic | FL gets 60% US, UK gets 100% UK | Week 2 |
| PO creation | Shipping plan generated | Week 2 |
| Approval workflow | Status transitions correctly | Week 3 |
| China portal | Mandate UI loads POs | Week 4 |
| Shipment delivery | Stock auto-added | Week 4 |

### 7.3 Integration Tests

| Test | Expected | Owner |
|------|----------|-------|
| BigQuery → Supabase sync | Zero data loss, <10s latency | Week 1 |
| PO → on_order update | Inventory reflects PO | Week 2 |
| Shipment → stock receipt | free_stocks increases | Week 4 |

---

## 8. SUCCESS METRICS

| Metric | Target | Measurement |
|--------|--------|-------------|
| Manual reorder time | 10 hrs/week → 2 hrs/week | Staff time tracking |
| Over-ordering rate | <5% (vs 126% current) | Compare to manual baseline |
| Stock-out rate | <1% of active items | Daily stock-out count |
| PO accuracy | 95%+ correct distribution | Manager rejection rate |
| China processing time | <4 hours from PO to shipment | Timestamp delta |
| Approval SLA | <2 hours average | Approval timestamp analysis |

---

## 9. RISKS & MITIGATIONS

| Risk | Severity | Mitigation |
|------|----------|-----------|
| BigQuery freshness fails | HIGH | Daily freshness check + fallback to previous snapshot |
| Distribution logic produces wrong split | HIGH | Unit tests + manual QA before each PO batch |
| China team doesn't adopt portal | MEDIUM | Bilingual onboarding + training session |
| Managers ignore Slack notifications | MEDIUM | Daily email digest + escalation after 4 hours |
| LLM validation hallucinates | MEDIUM | Never auto-approve adjustments >10 units |

---

## 10. OPEN QUESTIONS FOR CEM

1. **Top 50 best sellers:** Per warehouse (150 total) or global (50 total)?
2. **Rounding threshold:** Confirm 1000 units as switch point (base 10 → base 100)?
3. **Stale stock threshold:** Is 30 days correct for exclusion?
4. **Approval escalation:** Auto-approve after X hours if no action? (Codex says NO)
5. **Builder assignment:** Hermes, Claude Code CLI, or Codex?

---

## 11. TIMELINE SUMMARY

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Data Foundation | Fixed warehouse codes, velocity calc, best sellers, alerts |
| 2 | Core Procurement | Reorder queue, distribution logic, PO creation |
| 3 | Approval Workflow | In-app approval, Slack notifications |
| 4 | China Portal | Mandarin UI, shipments, stock receipt |
| 5-6 | Intelligence | Transfers, LLM validation, Xero integration |

**Go-live target:** End of Week 4 (May 11, 2026)

---

*PRD v1.0 | Hermes | 2026-04-13*
*Synthesizing: Athena (Data Integrity), Codex (Adversarial Review), Ava (Strategic Analysis), PROJECT v2.6*
