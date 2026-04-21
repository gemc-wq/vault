# Data Integrity Report — Inventory Ordering App
**Prepared by:** Athena | **Date:** 2026-04-13
**Purpose:** Pre-build data validation per Cem's directive: "Is the data correct?"

---

## VERDICT: BUILD CANNOT START WITHOUT FIXING 3 CRITICAL ISSUES

---

## CRITICAL ISSUE #1: Velocity Uses 7-Day Window Only

**Finding:** `avg_daily_sales` = `sales_last_7d / 7` — confirmed 20/20 top items.

| Item | 30d Sales | 7d Sales | avg_daily (actual) | 30d/30 | 7d/7 |
|------|-----------|----------|-------------------|--------|------|
| HTPCR-IPH15 | 608 | 240 | 34.3 | 20.3 | **34.3 ✅** |
| HTPCR-IPHSE4 | 571 | 301 | 43.0 | 19.0 | **43.0 ✅** |
| HTPCR-IPH14 | 494 | 225 | 32.1 | 16.5 | **32.1 ✅** |

**Risk:** Reorder level = avg_daily × 56 (8-week lead time). A 1-week sales spike triggers 8 weeks of inflated ordering. A 1-week dip triggers stock-outs.

**Example:** HTPCR-IPHSE4 has reorder_level = 2,408 units based on a 43/day 7d spike. At 30d average (19/day), the correct reorder would be 1,064. We'd over-order by **126%**.

**Fix required:** Use weighted average: `(sales_last_7d/7 × 0.4) + (sales_last_30d/30 × 0.6)` or similar blended formula. The PROJECT.md v2.6 spec already suggests this — the current BigQuery view does NOT implement it.

---

## CRITICAL ISSUE #2: Supabase Orders Table is Incomplete

**Finding:** Cross-reference failed. HTPCR-IPH15 in last 7 days:
- `blank_inventory` says: **277 sales** (across all warehouses)
- `orders` table has: **83 rows**
- Discrepancy: **70% of orders are missing**

**Root cause:** `blank_inventory` sales data comes from BigQuery (via Datastream from AWS MySQL). The Supabase `orders` table is a partial sync — only 336K rows vs the full order dataset.

**Risk:** If the procurement app calculates velocity from Supabase `orders` instead of using BigQuery-sourced `blank_inventory`, it will under-count sales by ~70% and trigger chronic stock-outs.

**Fix required:** The app MUST use `blank_inventory.sales_last_*` columns (BigQuery-sourced) for velocity. Never calculate velocity from the Supabase `orders` table directly.

---

## CRITICAL ISSUE #3: Warehouse Code Duplication

**Finding:** Two codes for Florida warehouse:

| Code | Items | Likely Origin |
|------|-------|---------------|
| `Florida` | 10,337 | BigQuery/AWS source system |
| `FL` | 99 | Manual/Supabase entry |

**Risk:** Distribution logic splitting by warehouse will miss 99 FL items or double-count Florida. Any `WHERE warehouse = 'FL'` query ignores 99% of Florida inventory.

**Full warehouse map:**

| Warehouse | Items | % |
|-----------|-------|---|
| UK | 10,369 | 25.0% |
| PH | 10,337 | 24.9% |
| Florida | 10,337 | 24.9% |
| Transit | 10,337 | 24.9% |
| FL | 99 | 0.2% |
| **Total** | **41,479** | **100%** |

**Fix required:** Normalise warehouse codes. Merge `FL` → `Florida` (or vice versa). Add constraint to prevent new variations.

---

## HIGH ISSUES

### Issue #4: 98% of Items Have Zero Reorder Level

Only **749 / 41,479** items (1.8%) have `reorder_level > 0`. The remaining 40,730 items have no automated reorder trigger.

For items WITH reorder levels, the formula is consistent: `reorder_level = avg_daily_sales × 56` (8-week cover).

**Implication:** The reorder system currently protects less than 2% of inventory. The app must calculate reorder levels dynamically rather than relying on the pre-set column.

### Issue #5: 78% of Inventory is Discontinued

| Product Group | Items | % |
|---------------|-------|---|
| DISC | 32,428 | 78.2% |
| Active groups | 9,051 | 21.8% |

Every query, dashboard, and reorder algorithm must filter `product_group != 'DISC'` or results will be massively skewed.

### Issue #6: 95 Active Stock-Outs (All in PH)

| Item | 7d Sales | Avg Daily | Stock | Revenue at Risk* |
|------|----------|-----------|-------|-----------------|
| HTPCR-S931X | 162 | 23.1/day | 0 | ~$230/day |
| HDMWH-250X300X3 | 100 | 14.3/day | 0 | ~$143/day |
| HB401-A172025 | 75 | 10.7/day | 0 | ~$107/day |
| HLBWH-IPH17 | 45 | 6.4/day | 0 | ~$64/day |

*Estimated at ~$10 average order value

All stock-outs are in **PH warehouse**. This validates Cem's concern: "we stock out we lose sales."

### Issue #7: 1,054 Dead Stock Items

Items with >100 units in stock but zero sales in 30 days. Potential write-off candidates for the LLM validation feature.

### Issue #8: Alert System Has No Early Warning

| Level | Count | % |
|-------|-------|---|
| GREEN | 41,204 | 99.3% |
| AMBER | 0 | 0% |
| RED | 217 | 0.5% |

Zero AMBER alerts means no gradual warning — items go from GREEN to RED with no intermediate state. The alert logic needs a proper AMBER threshold.

---

## WHAT'S CORRECT (Good News)

| Check | Result |
|-------|--------|
| `blank_inventory` snapshot date | ✅ Today (2026-04-13) |
| Orders table freshness | ✅ paid_date up to Apr 12, synced today 06:00 UTC |
| Orders date range | ✅ Jan 1, 2025 → Apr 12, 2026 (467 days) |
| Reorder formula consistency | ✅ All items use `avg_daily × 56` |
| No negative stock values | ✅ Zero items with negative `free_stocks` |
| Per-warehouse tracking | ✅ Each item tracked across UK/PH/Florida/Transit |
| Multi-site sales allocation | ✅ Sales correctly attributed per warehouse |

---

## RECOMMENDATIONS BEFORE BUILD

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | Implement blended velocity formula (7d + 30d weighted) | Builder | P0 — blocks accurate reordering |
| 2 | Document: "Use blank_inventory for velocity, NOT orders table" | Athena | P0 — prevents fatal architecture mistake |
| 3 | Normalise warehouse codes (FL → Florida or vice versa) | Builder/Harry | P0 — blocks distribution logic |
| 4 | Filter DISC items from all reorder queries | Builder | P1 — prevents noise |
| 5 | Calculate reorder levels dynamically (not rely on pre-set column) | Builder | P1 — only 2% have levels |
| 6 | Add AMBER alert threshold | Builder | P2 — early warning system |
| 7 | Flag 95 active stock-outs for immediate China reorder | Operations | P1 — revenue recovery |
| 8 | Review 1,054 dead stock items for write-off | Harry/Finance | P2 — capital recovery |

---

## DATA SOURCES CONFIRMED

```
AWS MySQL (canonical orders)
    ↓ Datastream (real-time)
BigQuery zero_dataset
    ↓ Sync Job (2hr)
Supabase blank_inventory ← USE THIS for velocity
    (sales_last_7d, sales_last_30d, avg_daily_sales sourced from BQ)

Supabase orders table ← INCOMPLETE (~30% of actual orders)
    DO NOT use for velocity calculations
```

---

*Report generated from live Supabase queries on 2026-04-13. All numbers verified against actual data.*
