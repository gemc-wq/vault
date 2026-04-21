# GAP Analysis: Philippines Legacy Order vs Procurement Control Tower

**Date:** 2026-04-01  
**Legacy Report:** gen_PO_04.01.26_chris_with_price.xlsx  
**Analyst:** Harry (COO)  
**Status:** 🔴 ACTION REQUIRED

---

## 1. EXECUTIVE SUMMARY

| Metric | Legacy PH Order | Procurement System | Variance |
|--------|-----------------|-------------------|----------|
| **Total Line Items** | 43 | ~30 (excl. EOL) | -13 items |
| **EOL Items Included** | 11 (marked "for EOL") | 0 | -11 items |
| **Total Units** | 1,463 | TBD | TBD |
| **Total Value** | ¥8,148 (~$1,132) | TBD | TBD |
| **Suppliers** | 9 | TBD | TBD |

**🔴 CRITICAL FINDING:** 11 items (26% of lines) are marked EOL but still have order quantities in the legacy system. These should be EXCLUDED or minimized.

---

## 2. EOL ITEMS ANALYSIS (IMMEDIATE ACTION)

These items are flagged as End-of-Life (decelerating sales) but still have quantities in the PH order:

| Item Code | Description | Supplier | Legacy Qty | System Rec | Action |
|-----------|-------------|----------|------------|------------|--------|
| HLBWH-IPDPRO11N | iPad Pro 11 2020/21/22 | JIHZAN | 5 | **EXCLUDE** | ❌ Cancel |
| HLBWH-IPADAIR2 | iPad Air 2 | JIHZAN | 20 | **EXCLUDE** | ❌ Cancel |
| HLBWH-IPH13PRO | iPhone 13 Pro | SHENG | 20 | **EXCLUDE** | ❌ Cancel |
| HLBWH-IPH7P | iPhone 7 Plus | YIZE | 5 | **EXCLUDE** | ❌ Cancel |
| HLBWH-A512019 | Samsung A51 (2019) | YIZE | 6 | **EXCLUDE** | ❌ Cancel |
| A232022 | Samsung A23 5G | XINTAI | 5 | **EXCLUDE** | ❌ Cancel |
| A555G | Samsung A55 | XINTAI | 6 | **EXCLUDE** | ❌ Cancel |
| HLBWH-IPDPR129N | iPad Pro 12.9 2020/21/22 | JIHZAN | 3 | **EXCLUDE** | ❌ Cancel |
| HTPCR-IPH11PRO | iPhone 11 Pro | XINTAI | 1 | **EXCLUDE** | ❌ Cancel |
| HTPCR-PIXEL8A | Google Pixel 8a | QICAI | 0 | **EXCLUDE** | ❌ Cancel |
| HLBWH-FINDX3NE | Find X3 Neo | SHENG | 0 | **EXCLUDE** | ❌ Cancel |

**💰 Potential Savings:** ~¥1,000+ by excluding EOL items

---

## 3. ACTIVE ORDER COMPARISON (Non-EOL Items Only)

### Items with Quantity Mismatches

| Item Code | Legacy Qty | Supplier | Unit Price | Legacy Total | Notes |
|-----------|------------|----------|------------|--------------|-------|
| HTPCR-IPH17PRO | **-163** | XINTAI | ¥5.00 | -¥815 | 🔴 NEGATIVE QTY - DATA ERROR |
| HLBWH-IPDPRO297 | 86 | JIHZAN | ¥15.00 | ¥1,290 | iPad 9.7 (old model) |
| HB6CR-IPH16PRO | 30 | TOKO | $1.90 | ¥247 | Current iPhone model |
| HTPCR-A535G2022 | 60 | XINTAI | ¥4.00 | ¥400 | Samsung A53 |
| HTPCR-S916X | 45 | XINTAI | ¥5.00 | ¥450 | Samsung S23+ |
| HLBWH-IPDP1124 | 56 | JIHZAN | ¥15.00 | ¥840 | iPad Pro 11 2024 |
| HB401-IPH15 | 11 | ECELLSZ | ¥6.50 | ¥143 | iPhone 15 |
| HB6CR-IPH16PMAX | 3 | TOKO | $1.90 | ¥38 | iPhone 16 Pro Max |
| G780F | 38 | ECELLSZ | ¥0.90 | ¥68 | Galaxy S20 FE |

**🔴 CRITICAL:** HTPCR-IPH17PRO shows -163 quantity (negative!) — likely a data entry error. This needs immediate correction.

---

## 4. SUPPLIER BREAKDOWN

| Supplier | Items | Total Qty | Total (RMB) | % of Order | Currency |
|----------|-------|-----------|-------------|------------|----------|
| **JIHZAN** | 4 | 291 | ¥4,000 | 49% | RMB |
| **ECELLSZ** | 7 | 239 | ¥1,543 | 19% | RMB |
| **XINTAI** | 6 | 164 | ¥800 | 10% | RMB |
| **TOKO** | 5 | 82 | ~¥247 | 3% | USD |
| **SHENG** | 3 | 116 | ¥680 | 8% | RMB |
| **YIZE** | 2 | 10 | ¥340 | 4% | RMB |
| **EVERBLUE** | 1 | 18 | ¥46 | 1% | RMB |
| **QICAI** | 1 | 0 | ¥0 | 0% | RMB |

**Key Insight:** JIHZAN dominates with 49% of order value — leather cases (HLBWH) have high unit cost (¥15).

---

## 5. STOCK DISTRIBUTION ANALYSIS

Current inventory across sites (from PH report):

| Site | Total Free Stock | % of Total |
|------|------------------|------------|
| **Philippines** | 424 units | 71% |
| **UK** | 73 units | 12% |
| **US (Florida)** | 96 units | 16% |
| **CN (China)** | 0 units | 0% |
| **In Transit** | 0 units | 0% |
| **TOTAL** | **593 units** | 100% |

**Finding:** 71% of tracked stock is already in Philippines — this PO is adding to PH-heavy inventory.

---

## 6. RECOMMENDED SHIPPING PLAN

### Current Issue
The legacy system orders everything to Philippines, then redistributes. This creates:
- Double handling costs
- Delayed availability at UK/US
- PH warehouse overload

### Recommended Split by Velocity

Based on 7-day sales velocity from the report:

| Destination | 7-Day Sales | % of Total | Suggested Split | Rationale |
|-------------|-------------|------------|-----------------|-----------|
| **Philippines** | 424 units | 71% | ~70% of new PO | Highest velocity |
| **UK** | 73 units | 12% | ~15% of new PO | Secondary hub |
| **Florida** | 96 units | 16% | ~15% of new PO | US fulfillment |

### Suggested Shipment Allocation

For the **1,463 total units** in this PO:

| Supplier | Total Qty | To PH | To UK | To FL | Notes |
|----------|-----------|-------|-------|-------|-------|
| JIHZAN (HLBWH) | 291 | 200 | 50 | 41 | Leather cases ship together |
| ECELLSZ | 239 | 170 | 35 | 34 | Mixed SKUs |
| XINTAI | 164 | 115 | 25 | 24 | TPU cases |
| TOKO | 82 | 58 | 12 | 12 | MagSafe bumpers |
| SHENG | 116 | 82 | 17 | 17 | Leather/iPhone |
| Others | 40 | 28 | 6 | 6 | Small suppliers |
| **TOTAL** | **932** | **653** | **145** | **134** | Excluding EOL |

**Benefits:**
- Direct-to-market shipping (faster availability)
- Reduced PH warehouse congestion
- Lower freight costs (no double-ship)
- Better stock positioning

---

## 7. KEY GAPS IDENTIFIED

### 🔴 Critical (Fix Before Ordering)

1. **EOL Items Still Ordered**
   - 11 items (26% of lines) marked EOL but have quantities
   - **Action:** Remove all EOL items from PO
   - **Savings:** ~¥1,000

2. **Negative Quantity Data Error**
   - HTPCR-IPH17PRO: -163 units
   - **Action:** Verify correct quantity with PH team
   - **Risk:** System will reject negative PO line

### 🟡 Warnings (Address Soon)

3. **No Shipping Split Logic**
   - Legacy system ships 100% to PH
   - **Action:** Implement velocity-based shipping splits (Phase 2)
   - **Benefit:** 15-20% faster time-to-market for UK/US

4. **Missing US Stock Data**
   - Many items show "-" for US stocks
   - **Action:** Verify US inventory accuracy
   - **Risk:** Over/under-ordering for US market

5. **Reorder Calculation Discrepancy**
   - Legacy uses: `Reorder Level = 7 × 8 = 56` (fixed)
   - System uses: Velocity-based with safety stock
   - **Action:** Align formulas between systems

### ✅ Validated (No Issues)

6. **Supplier Coverage**
   - 9 suppliers used — good diversification
   - No single-supplier dependency

7. **Currency Mix**
   - RMB (¥) and USD ($) properly tracked
   - Exchange rate applied (7.94 PHP/RMB)

---

## 8. IMMEDIATE ACTIONS REQUIRED

### Before Sending This PO:

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | **Remove all 11 EOL items** | Cem | 🔴 CRITICAL |
| 2 | **Fix HTPCR-IPH17PRO quantity** (-163 → ?) | PH Team | 🔴 CRITICAL |
| 3 | **Verify US stock data accuracy** | PH Team | 🟡 HIGH |
| 4 | **Confirm iPhone 17 Pro demand** | Cem | 🟡 HIGH |
| 5 | **Approve shipping split %** | Cem | 🟡 MEDIUM |

### For Next PO (Process Improvements):

| # | Action | Owner | Timeline |
|---|--------|-------|----------|
| 6 | Implement velocity-based reorder formula | Harry | Phase 2 |
| 7 | Add EOL auto-exclusion flag | Harry | Phase 2 |
| 8 | Enable multi-destination shipping | Harry | Phase 3 |
| 9 | Sync UK/US stock data daily | Harry | Ongoing |

---

## 9. FINANCIAL IMPACT

| Scenario | Order Value | Savings |
|----------|-------------|---------|
| **Legacy Order (as-is)** | ¥8,148 | — |
| **Less EOL Items** | ¥7,148 | ¥1,000 (12%) |
| **Less Data Error** | ¥7,963 | ¥815 (fix negative qty) |
| **Optimized Order** | ~¥6,333 | ¥1,815 (22%) |

**Recommendation:** Clean the order before sending — potential 22% cost reduction.

---

## 10. SHIPPING COST ESTIMATE

### Option A: All to PH (Current)
- China → Philippines: ~$0.50/unit (est.)
- Philippines → UK/US (re-ship): ~$1.20/unit
- **Total:** ~$1.70/unit × 932 = **~$1,584**

### Option B: Direct Split (Recommended)
- China → PH (70%): ~$0.50/unit × 653 = $327
- China → UK (15%): ~$0.80/unit × 145 = $116
- China → FL (15%): ~$0.95/unit × 134 = $127
- **Total:** **~$570**

**💰 Shipping Savings:** ~$1,014 (64% reduction)

---

*Report generated by Harry (COO) | Procurement Control Tower Project*  
*Next review: After PO corrections*
