# Best Sellers Staging Table — Specification
**Status:** DRAFT v2 | **Date:** 2026-04-13
**Origin:** Cem's directive — use PULSE-style daily cron to tag best sellers
**Updated:** Supply zone logic per Cem's feedback (no UK↔US transfer)

---

## Purpose

Daily cron creates a staging table that:
1. Tags top 50 global + top 50 per supply zone best-selling items
2. Provides the procurement app with a lookup: "is this item a best seller?"
3. Drives tiered velocity logic (best sellers use 7d, others use 30d)
4. Mirrors PULSE dashboard's trending detection
5. Calculates zone-level stock availability (not misleading global totals)

---

## Supply Zone Model

Stock is only useful within connected warehouses. UK↔US transfer is blocked (high freight).

| Zone | Warehouses | Rationale |
|------|-----------|-----------|
| **Zone US** | Florida + PH (US share) | PH handles US overflow, FBA, Saturday |
| **Zone UK** | UK + PH (UK share) | PH handles UK overflow |

**PH is shared** — allocated proportionally based on velocity.

### PH Allocation Formula

```
PH_US_share% = (FL_velocity + PH_velocity_for_US) / (FL_velocity + UK_velocity + PH_total_velocity)
PH_UK_share% = (UK_velocity + PH_velocity_for_UK) / (FL_velocity + UK_velocity + PH_total_velocity)

Zone_US_stock = FL_stock + (PH_stock × PH_US_share%)
Zone_UK_stock = UK_stock + (PH_stock × PH_UK_share%)
```

**Decision (Cem, Apr 13):** Proportional allocation is Phase 1 — same math drives the China shipping plan. Not deferrable.

### Best Seller Lists (Union)

1. **Top 50 Global** — by total velocity across all warehouses. Ensures globally important items aren't missed.
2. **Top 50 Zone US** — by FL + PH velocity. Catches US regional best sellers.
3. **Top 50 Zone UK** — by UK velocity. Catches UK regional best sellers.

Union = ~80-120 unique items after overlap. All get MAX(7d, 30d) velocity treatment.

---

## Table: `best_sellers_daily`

```sql
CREATE TABLE best_sellers_daily (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_code       TEXT NOT NULL,
    warehouse       TEXT NOT NULL,
    rank            INT NOT NULL,           -- 1-50 by velocity
    velocity_7d     NUMERIC(10,2),          -- sales_last_7d / 7
    velocity_30d    NUMERIC(10,2),          -- sales_last_30d / 30
    velocity_used   NUMERIC(10,2),          -- MAX(7d, 30d) for best sellers
    sales_last_7d   INT,
    sales_last_30d  INT,
    free_stocks     INT,
    days_of_cover   NUMERIC(10,1),          -- free_stocks / velocity_used
    stock_risk      TEXT,                   -- CRITICAL / LOW / OK
    reorder_qty     INT,                    -- calculated reorder quantity
    snapshot_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(item_code, warehouse, snapshot_date)
);

CREATE INDEX idx_bs_daily_date ON best_sellers_daily(snapshot_date);
CREATE INDEX idx_bs_daily_item ON best_sellers_daily(item_code);
```

---

## Cron Logic (Daily, 06:30 UTC — after blank_inventory sync)

```sql
-- Step 1: Clear today's data
DELETE FROM best_sellers_daily WHERE snapshot_date = CURRENT_DATE;

-- Step 2: Insert top 50 per warehouse by blended velocity
INSERT INTO best_sellers_daily (
    item_code, warehouse, rank, velocity_7d, velocity_30d, velocity_used,
    sales_last_7d, sales_last_30d, free_stocks, days_of_cover, stock_risk, reorder_qty
)
SELECT 
    item_code,
    warehouse,
    ROW_NUMBER() OVER (PARTITION BY warehouse ORDER BY GREATEST(
        COALESCE(sales_last_7d::numeric / 7, 0),
        COALESCE(sales_last_30d::numeric / 30, 0)
    ) DESC) AS rank,
    ROUND(COALESCE(sales_last_7d::numeric / 7, 0), 2) AS velocity_7d,
    ROUND(COALESCE(sales_last_30d::numeric / 30, 0), 2) AS velocity_30d,
    ROUND(GREATEST(
        COALESCE(sales_last_7d::numeric / 7, 0),
        COALESCE(sales_last_30d::numeric / 30, 0)
    ), 2) AS velocity_used,
    sales_last_7d,
    sales_last_30d,
    free_stocks,
    CASE 
        WHEN GREATEST(COALESCE(sales_last_7d::numeric / 7, 0), COALESCE(sales_last_30d::numeric / 30, 0)) > 0
        THEN ROUND(free_stocks / GREATEST(COALESCE(sales_last_7d::numeric / 7, 0), COALESCE(sales_last_30d::numeric / 30, 0)), 1)
        ELSE 999
    END AS days_of_cover,
    CASE
        WHEN free_stocks = 0 THEN 'CRITICAL'
        WHEN free_stocks / NULLIF(GREATEST(COALESCE(sales_last_7d::numeric / 7, 0), COALESCE(sales_last_30d::numeric / 30, 0)), 0) < 14 THEN 'LOW'
        ELSE 'OK'
    END AS stock_risk,
    -- Reorder qty: (45 days cover for best sellers * velocity) - current stock, rounded to base
    -- Note: best_sellers get 45d cover; normal items get 30d (applied in app layer, staging uses 45d)
    GREATEST(0, 
        CASE 
            WHEN GREATEST(COALESCE(sales_last_7d::numeric / 7, 0), COALESCE(sales_last_30d::numeric / 30, 0)) * 45 - free_stocks >= 1000
            THEN CEIL((GREATEST(COALESCE(sales_last_7d::numeric / 7, 0), COALESCE(sales_last_30d::numeric / 30, 0)) * 45 - free_stocks) / 100) * 100
            ELSE CEIL((GREATEST(COALESCE(sales_last_7d::numeric / 7, 0), COALESCE(sales_last_30d::numeric / 30, 0)) * 45 - free_stocks) / 10) * 10
        END
    )::INT AS reorder_qty
FROM blank_inventory
WHERE product_group != 'DISC'
  AND COALESCE(sales_last_30d, 0) > 0
  AND warehouse IN ('UK', 'PH', 'Florida')  -- Exclude Transit, normalize FL
ORDER BY warehouse, rank;

-- Step 3: Trim to top 50 per warehouse
DELETE FROM best_sellers_daily 
WHERE snapshot_date = CURRENT_DATE AND rank > 50;
```

---

## Consumers

| System | How It Uses This Table |
|--------|----------------------|
| **Procurement App** | Lookup: `WHERE item_code IN (SELECT item_code FROM best_sellers_daily WHERE snapshot_date = CURRENT_DATE)` → use 7d velocity. All others → use 30d. |
| **PULSE Dashboard** | Can reference for "top sellers" widget instead of recalculating |
| **Stock-out Alerts** | `WHERE stock_risk = 'CRITICAL'` → immediate alert |
| **Reorder Queue** | Pre-calculated `reorder_qty` ready for PO generation |

---

## Tiered Velocity Logic (for procurement app)

```typescript
function getVelocity(item: InventoryItem, bestSellers: Set<string>): number {
  const v7d = item.sales_last_7d / 7;
  const v30d = item.sales_last_30d / 30;
  
  if (bestSellers.has(item.item_code)) {
    // Best sellers: use whichever is HIGHER (never stock out)
    return Math.max(v7d, v30d);
  } else {
    // Standard items: use 30d only (stable, no over-ordering)
    return v30d;
  }
}

function getReorderQty(velocity: number, currentStock: number, leadTimeDays: number = 56): number {
  const target = velocity * leadTimeDays;
  const need = target - currentStock;
  if (need <= 0) return 0;
  const base = need >= 1000 ? 100 : 10;
  return Math.ceil(need / base) * base;
}
```

---

---

## Allocation → Shipping Plan (China Distribution)

The same proportional math that determines zone stock also tells China WHERE to ship.

### Full Calculation Flow

```typescript
interface ZoneAllocation {
  item_code: string;
  total_reorder_qty: number;      // Total units to order from China
  ship_to_fl: number;             // Units destined for Florida
  ship_to_uk: number;             // Units destined for UK
  ship_to_ph: number;             // Units destined for PH
}

function calculateAllocation(item: {
  item_code: string;
  velocity_fl: number;            // FL avg_daily_sales
  velocity_uk: number;            // UK avg_daily_sales
  velocity_ph: number;            // PH avg_daily_sales
  stock_fl: number;
  stock_uk: number;
  stock_ph: number;
  is_best_seller: boolean;
}, leadTimeDays: number = 56): ZoneAllocation {

  // Step 1: Determine velocity per site
  const v_fl = item.velocity_fl;
  const v_uk = item.velocity_uk;
  const v_ph = item.velocity_ph;
  const v_total = v_fl + v_uk + v_ph;
  
  if (v_total === 0) return { item_code: item.item_code, total_reorder_qty: 0, ship_to_fl: 0, ship_to_uk: 0, ship_to_ph: 0 };

  // Step 2: PH serves both zones — split PH velocity by destination
  // PH handles: US overflow, FBA, Saturday orders + UK overflow
  // Approximation: PH velocity splits proportional to FL vs UK velocity
  const ph_us_ratio = v_fl / (v_fl + v_uk || 1);
  const ph_uk_ratio = v_uk / (v_fl + v_uk || 1);

  // Step 3: Zone stock (what's actually available per zone)
  const zone_us_stock = item.stock_fl + (item.stock_ph * ph_us_ratio);
  const zone_uk_stock = item.stock_uk + (item.stock_ph * ph_uk_ratio);

  // Step 4: Zone target (lead time × zone velocity)
  const zone_us_velocity = v_fl + (v_ph * ph_us_ratio);
  const zone_uk_velocity = v_uk + (v_ph * ph_uk_ratio);
  
  const zone_us_target = zone_us_velocity * leadTimeDays;
  const zone_uk_target = zone_uk_velocity * leadTimeDays;

  // Step 5: Zone need
  const zone_us_need = Math.max(0, zone_us_target - zone_us_stock);
  const zone_uk_need = Math.max(0, zone_uk_target - zone_uk_stock);
  const total_need = zone_us_need + zone_uk_need;

  if (total_need === 0) return { item_code: item.item_code, total_reorder_qty: 0, ship_to_fl: 0, ship_to_uk: 0, ship_to_ph: 0 };

  // Step 6: Round total to base 10 or 100
  const base = total_need >= 1000 ? 100 : 10;
  const total_rounded = Math.ceil(total_need / base) * base;

  // Step 7: Distribute to destinations using PROJECT.md product mapping
  // Default split (configurable per product type):
  //   HTPCR, HC, HB401, H89, HDMWH → FL 60%, PH 40% (of US zone)
  //   HLBWH → PH 80%, FL 20% (of US zone)
  // UK zone → 100% UK
  const us_share = Math.round(total_rounded * (zone_us_need / total_need));
  const uk_share = total_rounded - us_share;

  // Within US zone: split between FL and PH per product rules
  const fl_ratio = 0.60;  // Default — override per product_group
  const ship_to_fl = Math.round(us_share * fl_ratio / 10) * 10;
  const us_to_ph = us_share - ship_to_fl;

  // Within UK zone: split between UK and PH (PH handles overflow)
  const uk_ratio = 0.75;  // Default — override per product_group
  const ship_to_uk = Math.round(uk_share * uk_ratio / 10) * 10;
  const uk_to_ph = uk_share - ship_to_uk;

  // PH receives from both zones
  const ship_to_ph = us_to_ph + uk_to_ph;

  return {
    item_code: item.item_code,
    total_reorder_qty: total_rounded,
    ship_to_fl,
    ship_to_uk,
    ship_to_ph,
  };
}
```

---

## Two Procurement Processes (Confirmed by Cem, Apr 13)

### Process 1: Internal Stock Transfers

| Route | Allowed | Lead Time |
|-------|---------|-----------|
| PH → FL | ✅ | Days (shipping only) |
| PH → UK | ✅ | Days (shipping only) |
| UK ↔ FL | ❌ | Blocked (high freight) |

**Trigger:** Zone stock below threshold AND PH has surplus above its own needs.

```typescript
function checkInternalTransfer(item: ZoneItem): TransferOrder | null {
  // PH surplus = PH stock - PH's own safety stock (14 days cover)
  const ph_safety = item.velocity_ph * 14;
  const ph_surplus = Math.max(0, item.stock_ph - ph_safety);
  
  if (ph_surplus === 0) return null;  // Nothing to transfer
  
  const transfers: TransferOrder[] = [];
  
  // Zone US short?
  const us_need = Math.max(0, (item.zone_us_target * 0.5) - item.stock_fl);  // 50% target = urgent threshold
  if (us_need > 0) {
    const transfer_qty = Math.min(ph_surplus, us_need);
    transfers.push({ from: 'PH', to: 'FL', qty: Math.ceil(transfer_qty / 10) * 10, item: item.item_code });
  }
  
  // Zone UK short?
  const remaining_surplus = ph_surplus - (transfers[0]?.qty || 0);
  const uk_need = Math.max(0, (item.zone_uk_target * 0.5) - item.stock_uk);
  if (uk_need > 0 && remaining_surplus > 0) {
    const transfer_qty = Math.min(remaining_surplus, uk_need);
    transfers.push({ from: 'PH', to: 'UK', qty: Math.ceil(transfer_qty / 10) * 10, item: item.item_code });
  }
  
  return transfers.length > 0 ? transfers : null;
}
```

**Output:** Internal Transfer Request (separate from PO)
- Approved by warehouse manager (not finance)
- No supplier, no invoice — just stock movement

### Process 2: Supplier Ordering

**Trigger:** Zone stock below threshold AND internal transfer cannot fully cover the shortfall (or PH also needs replenishment).

Uses the full allocation + shipping plan logic above.

**Output:** PO + Shipping Plan CSV/PDF for Ben

### Decision Sequence

```
Zone stock check
      ↓
  Below threshold?
      ↓ YES
  Can PH internal transfer cover it?
      ├── YES → Generate Internal Transfer Request (fast)
      ├── PARTIAL → Generate Internal Transfer + China PO for remainder
      └── NO (PH also short) → Generate China PO for full amount
```

### Shipping Plan Output (for Ben / China Office)

Each PO generates a shipping plan CSV:

| Item Code | Total Qty | → Florida | → UK | → PH | Zone US Days Cover | Zone UK Days Cover |
|-----------|-----------|-----------|------|------|-------------------|-------------------|
| HTPCR-IPH15 | 1,920 | 690 | 500 | 730 | 56 | 56 |

This CSV + PDF attaches to the PO and goes to Ben in supplier-optimised format.

---

## Open Questions for Cem

1. ✅ **ANSWERED:** Top 50 global + top 50 per zone (union). ~80-120 unique items.
2. ✅ **ANSWERED:** Proportional PH allocation — same math drives China shipping plan.
3. **Should Transit warehouse stock count toward "on order" in zone calculations?**
4. **Retention:** Keep 30 days of staging table history for trend analysis?
