# Master PRD Review — Hermes Advisory
**Date:** 2026-04-13
**Reviewer:** Hermes (Analyser, Builder, Shaper)
**Subject:** Inventory Ordering App Master PRD v1.0 (Athena)

---

## OVERALL ASSESSMENT

**Grade: A-**

Athena has produced an excellent synthesis. The two-process architecture (Internal Transfers + Supplier Ordering), three-layer agentic design, and shadow mode testing approach are significant improvements over prior specs.

**Strengths:**
- Two procurement processes clearly separated
- Three-layer architecture (Data → Intelligence → Portal) prevents autonomous action
- Shadow mode testing reduces risk
- Zone allocation model with proportional PH split
- Tiered velocity logic (best sellers vs normal)
- Data integrity issues documented with fixes

**Weaknesses:**
- Some technical implementation details underspecified
- Shadow mode comparison criteria undefined
- Agent Teams structure not defined
- Rollback triggers not specified
- Edge cases in zone allocation logic

---

## CRITICAL RECOMMENDATIONS

### 1. Shadow Mode Needs Specific Comparison Criteria

**Issue:** "Compare outputs" is vague. What exactly are we comparing?

**Recommendation:** Define specific comparison metrics:

| Metric | How to Measure | Acceptable Threshold |
|--------|----------------|---------------------|
| Item coverage | % of Zero's items in app output | ≥95% overlap |
| Quantity variance | |item_qty_app - item_qty_zero| / item_qty_zero | <15% per item |
| Destination accuracy | % of items with correct FL/UK/PH split | 100% |
| Missing items | Items in Zero but not in app | <5% |
| Extra items | Items in app but not in Zero | Explainable by exclusion rules |
| Transfer timing | Days between recommendation and actual transfer | ≤1 day |

**Implementation:** Build comparison report into Phase 1 deliverables.

---

### 2. Agent Teams Structure Needs Definition

**Issue:** "Claude Code CLI using Agent Teams" mentioned but structure undefined.

**Recommendation:** Define agent team structure before build:

```
AGENT TEAM STRUCTURE (Proposed):

┌─────────────────────────────────────────────────────────────┐
│                    PROJECT ORCHESTRATOR                      │
│              (Claude Code CLI - Main Session)                │
│                                                              │
│  Coordinates all agents, manages git, deploys to Cloud Run  │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ DATA AGENT  │         │  API AGENT  │         │  UI AGENT   │
│             │         │             │         │             │
│ SQL scripts │         │ Next.js API │         │ Components  │
│ Cron jobs   │         │ Supabase    │         │ Pages       │
│ Views       │         │ Business    │         │ Tailwind    │
│ Migrations  │         │ logic       │         │ Charts      │
└─────────────┘         └─────────────┘         └─────────────┘

Deliverables by Agent:
- DATA AGENT: best_sellers_daily, v_reorder_queue, v_zone_stock_summary, cron jobs
- API AGENT: /api/reorder/*, /api/transfers/*, /api/po/*, business logic
- UI AGENT: Dashboard, Reorder Queue, Transfer List, PO Approval, China Portal
```

**Protocol:**
- Each agent owns its domain
- Orchestrator coordinates, never writes code directly
- Handoffs via git branches: `data/*`, `api/*`, `ui/*`
- Merge to main after domain tests pass

---

### 3. Zone Allocation Edge Cases

**Issue:** PRD formula assumes `v_fl + v_uk > 0`. What if both are zero but PH has velocity?

**Scenario:** Item only sells through PH (FBA overflow). FL and UK velocity = 0. Current formula:
```
ph_us_ratio = 0 / (0 + 0) → division by zero
```

**Recommendation:** Add fallback logic:

```typescript
function calculatePHAllocation(v_fl: number, v_uk: number, v_ph: number): { us: number, uk: number } {
  const total_demand = v_fl + v_uk;
  
  if (total_demand === 0 && v_ph > 0) {
    // Edge case: PH-only sales (FBA overflow)
    // Default split based on historical zone ratios or 50/50
    return { us: 0.5, uk: 0.5 };  // Or pull from config table
  }
  
  if (total_demand === 0 && v_ph === 0) {
    // No velocity anywhere - exclude from reorder
    return { us: 0, uk: 0 };
  }
  
  return {
    us: v_fl / total_demand,
    uk: v_uk / total_demand
  };
}
```

**Add to PRD:** Section 8, Allocation Logic, Edge Cases subsection.

---

### 4. Rollback Triggers Undefined

**Issue:** Shadow mode has no defined rollback triggers. When do we know the system is "wrong enough" to not cutover?

**Recommendation:** Define explicit rollback criteria:

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Item coverage < 90% | 3 consecutive runs | Block cutover, investigate |
| Quantity variance > 25% | Any run | Pause, manual review |
| Destination accuracy < 95% | Any run | Block cutover, fix allocation logic |
| Stock-out on best seller | Caused by app recommendation | Immediate rollback to Zero |
| Zone allocation negative | Any item | Fix formula, re-run |
| Cron failure | >2 consecutive failures | Alert, manual trigger |

**Add to PRD:** Section 14, Rollback Criteria subsection.

---

### 5. Best Seller Lists Union Logic

**Issue:** PRD says "Union of all three = ~80-120 unique items" but union logic is ambiguous.

**Question:** If an item is top 50 globally AND top 50 in Zone US, does it count once or twice?

**Recommendation:** Clarify:

```sql
-- Best sellers = union of 3 lists (each item counted once)
WITH global_top50 AS (
  SELECT DISTINCT item_code 
  FROM blank_inventory 
  WHERE product_group != 'DISC' AND sales_last_30d > 0
  ORDER BY (sales_last_7d::numeric/7 + sales_last_30d::numeric/30) DESC
  LIMIT 50
),
zone_us_top50 AS (
  SELECT DISTINCT item_code 
  FROM blank_inventory 
  WHERE warehouse IN ('Florida', 'PH') 
    AND product_group != 'DISC' AND sales_last_30d > 0
  ORDER BY sales_last_30d DESC
  LIMIT 50
),
zone_uk_top50 AS (
  SELECT DISTINCT item_code 
  FROM blank_inventory 
  WHERE warehouse = 'UK'
    AND product_group != 'DISC' AND sales_last_30d > 0
  ORDER BY sales_last_30d DESC
  LIMIT 50
)
SELECT DISTINCT item_code 
FROM (
  SELECT item_code FROM global_top50
  UNION
  SELECT item_code FROM zone_us_top50
  UNION
  SELECT item_code FROM zone_uk_top50
) combined;
```

**Result:** Unique items across all three lists = best sellers. Each item gets best seller treatment (MAX(7d, 30d), 45d cover) regardless of which list it came from.

---

### 6. CN Stock Alert Implementation

**Issue:** PRD says "CN is staging only. Stock in CN = error flag." But no implementation details.

**Recommendation:** Add daily check:

```sql
-- Daily CN stock check (part of 06:30 cron)
INSERT INTO system_alerts (alert_type, message, severity, created_at)
SELECT 
  'CN_STOCK_ERROR' as alert_type,
  'Item ' || item_code || ' has ' || free_stocks || ' units in CN warehouse (staging only)' as message,
  'HIGH' as severity,
  NOW() as created_at
FROM blank_inventory
WHERE warehouse = 'CN' AND free_stocks > 0
ON CONFLICT DO NOTHING;  -- Don't duplicate alerts

-- Notify #procurement-alerts if any CN stock found
```

---

### 7. Florida vs FL Code Mapping

**Issue:** PRD says "FL = packaging/materials only" but Supabase has both codes mixed.

**Recommendation:** Create mapping table:

```sql
CREATE TABLE warehouse_code_map (
  raw_code TEXT PRIMARY KEY,
  canonical_code TEXT NOT NULL,
  category TEXT NOT NULL  -- 'blank_inventory' or 'packaging_materials'
);

INSERT INTO warehouse_code_map VALUES
  ('Florida', 'Florida', 'blank_inventory'),
  ('FL', 'Florida', 'packaging_materials');

-- View with normalised codes
CREATE VIEW v_inventory_normalised AS
SELECT 
  b.*,
  COALESCE(m.canonical_code, b.warehouse) AS warehouse_clean
FROM blank_inventory b
LEFT JOIN warehouse_code_map m ON m.raw_code = b.warehouse;
```

**Update all queries** to use `warehouse_clean` instead of `warehouse`.

---

### 8. Transfer Status Flow Missing States

**Issue:** PRD shows `SUGGESTED → CONFIRMED → SHIPPED → RECEIVED` but missing rejection/delay states.

**Recommendation:** Add full status flow:

```
SUGGESTED (system-generated)
    ↓
CONFIRMED (Chris/Jae approved)
    ↓
PICKED (PH warehouse pulled stock)
    ↓
SHIPPED (tracking number added)
    ↓
IN_TRANSIT (carrier picked up)
    ↓
RECEIVED (destination confirmed)
    OR
DELAYED (ETA passed, not received)
    OR
CANCELLED (Chris/Jae rejected suggestion)
    OR
PARTIAL (only some qty shipped/received)
```

**Add states to `internal_transfers` table:**

```sql
ALTER TABLE internal_transfers 
ADD COLUMN status TEXT DEFAULT 'SUGGESTED' 
CHECK (status IN (
  'SUGGESTED', 'CONFIRMED', 'PICKED', 'SHIPPED', 
  'IN_TRANSIT', 'RECEIVED', 'DELAYED', 'CANCELLED', 'PARTIAL'
));
```

---

## MEDIUM PRIORITY SUGGESTIONS

### 9. Add Stale Stock Review Workflow

**Issue:** 1,054 dead stock items identified, but no process for handling them.

**Recommendation:** Add quarterly stale stock review:

```
Quarterly Cron (Jan/Apr/Jul/Oct):
  → Generate stale stock report
  → Items: stock > 100 AND sales_last_90d = 0
  → Route to Harry for write-off consideration
  → Approved write-offs → stock_adjustments table
  → Post to Xero (write-off expense)
```

### 10. Supplier Performance Tracking

**Issue:** PRD mentions "Supplier scorecards" in Phase 2 but no data model.

**Recommendation:** Add base tracking now:

```sql
CREATE TABLE supplier_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  supplier TEXT NOT NULL,
  metric_date DATE NOT NULL,
  on_time_delivery_rate NUMERIC(5,2),  -- %
  avg_lead_time_days NUMERIC(5,2),
  quality_rejection_rate NUMERIC(5,2),  -- %
  total_orders INT,
  total_value NUMERIC(12,2),
  UNIQUE(supplier, metric_date)
);
```

Populate from `shipments` table. Even if UI is Phase 2, collect data now.

---

## LOW PRIORITY / FUTURE CONSIDERATIONS

### 11. Multi-Currency FX Tracking

**Issue:** CNY/GBP/USD orders with no FX rate tracking.

**Recommendation:** Add FX rate table for accurate cost analysis:

```sql
CREATE TABLE fx_rates (
  date DATE PRIMARY KEY,
  usd_to_gbp NUMERIC(10,4),
  usd_to_cny NUMERIC(10,4),
  source TEXT  -- 'open_exchange_rates' etc
);
```

### 12. Audit Trail Granularity

**Issue:** "Audit log entry" mentioned but no schema.

**Recommendation:**

```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name TEXT NOT NULL,
  record_id UUID NOT NULL,
  action TEXT NOT NULL,  -- INSERT/UPDATE/DELETE
  old_values JSONB,
  new_values JSONB,
  changed_by UUID,
  changed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger for all key tables
CREATE OR REPLACE FUNCTION audit_trigger() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, changed_by)
  VALUES (
    TG_TABLE_NAME,
    COALESCE(NEW.id, OLD.id),
    TG_OP,
    CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN row_to_json(OLD) END,
    CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) END,
    current_setting('request.jwt.claims->sub', true)::uuid
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## BUILD SEQUENCE RECOMMENDATION

Based on the Master PRD and my analysis, here's the recommended build sequence for Claude Code CLI Agent Teams:

### Week 1: Data Foundation (DATA AGENT)

| Day | Deliverable | Verification |
|-----|-------------|--------------|
| 1 | Warehouse code map + normalised views | Query returns no 'FL' codes in blank_inventory |
| 2 | `best_sellers_daily` table + cron | Cron runs, 50 items per list populated |
| 3 | `v_reorder_queue` view with tiered velocity | Manual query matches expected items |
| 4 | `v_zone_stock_summary` view | Zone totals match manual calculation |
| 5 | `supplier_metrics` table (empty) + FX rates | Schema exists, ready for data |

### Week 2: API + Business Logic (API AGENT)

| Day | Deliverable | Verification |
|-----|-------------|--------------|
| 1 | Allocation calculation functions | Unit tests pass |
| 2 | Transfer recommendation endpoint | Returns valid transfer suggestions |
| 3 | PO creation endpoint + distribution | Creates PO with correct FL/UK/PH split |
| 4 | Approval workflow endpoints | Status transitions correctly |
| 5 | Shadow mode comparison report API | Returns metrics vs Zero baseline |

### Week 3: UI + Integration (UI AGENT)

| Day | Deliverable | Verification |
|-----|-------------|--------------|
| 1 | Dashboard + stock alerts | Shows correct alert counts |
| 2 | Reorder queue page | Matches view data |
| 3 | Transfer list + approval | Chris/Jae can confirm/reject |
| 4 | China portal (Mandarin) | Ben can download POs |
| 5 | Shadow mode comparison UI | Side-by-side view works |

### Week 4: Testing + Cutover

| Day | Deliverable | Verification |
|-----|-------------|--------------|
| 1-2 | End-to-end UAT with Chris/Jae | All workflows complete |
| 3 | Shadow mode run #1 | Compare vs Zero output |
| 4 | Fix gaps, shadow run #2 | Meet comparison thresholds |
| 5 | Final shadow run, cutover decision | Cem sign-off |

---

## SUMMARY

| Category | Count | Action Required |
|----------|-------|-----------------|
| Critical | 4 | Must fix before build starts |
| Medium | 2 | Should include in Phase 1 |
| Low | 2 | Can defer to Phase 2 |

**Critical fixes needed:**
1. Define shadow mode comparison criteria (metrics + thresholds)
2. Define Agent Teams structure
3. Add zone allocation edge case handling
4. Define rollback triggers

**Recommendation:** Approve PRD with these amendments. The spec is solid — these additions make it build-ready.

---

*Hermes Advisory | 2026-04-13*
