# Advisory Report: Inventory Ordering App
**Prepared by:** Hermes (Operations Librarian)
**Date:** 2026-04-13
**Reference:** PROJECT.md v2.0 vs Blueprint V3

---

## Executive Summary

The Inventory Ordering App (PROJECT.md v2.0) is a comprehensive procurement system spec that **partially overlaps** with Blueprint V3's Stage 7B but introduces **schema conflicts, data source ambiguity, and ownership gaps** that must be resolved before build proceeds.

**Key Finding:** The PROJECT.md spec was written independently of Blueprint V3's existing table structures and migration plans, creating a risk of duplicate work and data inconsistency.

---

## Gap Analysis

### 1. Data Source Conflict — CRITICAL

| Document | Canonical Source | Status |
|----------|------------------|--------|
| PROJECT.md | BigQuery `zero_dataset.inventory` (VIEW) | Live, daily updates |
| Blueprint V3 | Legacy MySQL + Supabase `blank_inventory` | MySQL stale, Supabase built |

**Gap:** PROJECT.md correctly identifies BigQuery as the canonical source (verified 2026-04-11), but Blueprint V3 Stage 7B still references MySQL migration that hasn't occurred.

**Risk:** If two systems read from different sources, inventory decisions will be wrong.

**Recommendation:** Formalize BigQuery → Supabase sync as the ONLY data pipeline. Archive MySQL references.

---

### 2. Schema Collision — HIGH

**PROJECT.md Tables:**
- `purchase_orders` (columns: po_number, supplier, warehouse, status, currency, total_amount...)
- `po_lines` (columns: po_id, item_code, quantity, unit_price...)
- `shipments` (columns: shipment_number, po_ids[], origin, destination, carrier...)
- `supplier_invoices` (columns: invoice_number, ocr_status, extracted_data, xero_status...)

**Blueprint V3 - Harry's Existing Tables:**
- `purchase_orders`, `po_line_items` (different naming: `po_line_items` vs `po_lines`)
- `packing_lists` (not in PROJECT.md)
- `supplier_invoices`, `goods_receipts` (different structure)
- `stock_out_alerts`, `inventory_snapshots`

**Gap:** Column naming differs. `po_lines` vs `po_line_items`. PROJECT.md adds `po_ids[]` array to shipments (good), but doesn't include `packing_lists` table that Harry built.

**Risk:** If Harry's tables already exist with data, PROJECT.md schema will cause migration pain.

**Recommendation:** Align on Harry's existing table names or explicitly document migration path.

---

### 3. Missing Integration Points — MEDIUM

PROJECT.md operates in isolation. No documented connection to:

| Blueprint V3 Stage | Integration Needed | Status |
|--------------------|-------------------|--------|
| Stage 8: Fulfillment Portal | Shipment delivery → stock receipt trigger | Not specified |
| Stage 10: PULSE | Velocity data → reorder algorithm | Referenced but not wired |
| Listings Management | Stock availability → listing status | Not mentioned |

**Gap:** How does auto-reorder connect to PULSE velocity signals? If a design is surging on PULSE, does the app increase reorder quantities?

**Recommendation:** Add "Intelligence Integration" section to PROJECT.md linking PULSE signals to reorder calculations.

---

### 4. Ownership Confusion — MEDIUM

| Role | PROJECT.md | Blueprint V3 |
|------|------------|--------------|
| Owner | Harry (COO) | Harry (finance), Jay Mark (Supabase) |
| Builder | Not specified | Jay Mark for tables, Harry for automation |
| App hosting | Cloud Run | ecell.app (central hub) |

**Gap:** PROJECT.md says Cloud Run deployment. Blueprint V3 centralizes everything under ecell.app. Which is the target architecture?

**Recommendation:** Clarify if Inventory Ordering App is:
- A standalone Cloud Run service (PROJECT.md suggests this)
- A module inside ecell.app (Blueprint V3 suggests this)

---

### 5. China Office Portal — UNDEFINED

PROJECT.md specifies full Mandarin UI for China office. Blueprint V3 has no mention of China-specific interfaces.

**Gap:** Where does China portal live? 
- Subdomain: china.ecell.app?
- Route: ecell.app/china?
- Separate app entirely?

**Recommendation:** Define China portal architecture before Phase 2 build.

---

### 6. Phase Status Inconsistency — LOW

| Item | PROJECT.md Status | Blueprint V3 Status |
|------|-------------------|---------------------|
| Supabase schema | ✅ Done | ✅ Jay Mark built |
| PO creation workflow | 🟡 Pending | 🔴 Not started |
| Approval queue | 🟡 Pending | 🔴 Not started |
| Real-time dashboard | Not mentioned | 🔴 Not started |

**Gap:** PROJECT.md marks items as "pending" while Blueprint V3 marks same items as "not started." Inconsistent status reporting.

---

## SWOT Analysis

### Strengths
1. **Comprehensive workflow design** — Covers procurement → shipment → delivery → finance
2. **Mandarin support** — Critical for China office efficiency (currently manual email process)
3. **Multi-site architecture** — Properly models UK, FL, PH, CN, TRANSIT as distinct entities
4. **BigQuery integration** — Uses correct canonical source (not stale MySQL)
5. **Velocity-based reordering** — Intelligent stock management vs. manual thresholds
6. **Multi-currency** — GBP, USD, CNY support reflects actual operations

### Weaknesses
1. **Schema conflicts with Harry's existing tables** — Different naming, different columns
2. **No migration plan** — How do we move from current state to this design?
3. **Isolated design** — Doesn't integrate with Blueprint V3's other stages
4. **Ownership ambiguity** — Harry vs Jay Mark vs unspecified builder
5. **Deployment target unclear** — Cloud Run vs ecell.app?
6. **Missing packing_lists table** — Harry built it, PROJECT.md omits it

### Opportunities
1. **50%+ efficiency gain** — China office currently emails POs and packing lists manually
2. **Stock-out prevention** — Auto-reorder based on velocity could eliminate black-level events
3. **PULSE integration** — Feed velocity signals into reorder algorithm for predictive purchasing
4. **Finance automation** — Invoice OCR → Xero posting eliminates manual data entry
5. **Carrier API integration** — Real-time tracking visibility for all stakeholders

### Threats
1. **Parallel system risk** — If built separately from Blueprint V3, creates data silos
2. **Harry table conflict** — Existing finance tables may block PROJECT.md schema
3. **MySQL dependency** — If migration from MySQL isn't completed, data inconsistency
4. **IREN2 dependency** — $50K/day risk if print file monitoring fails (Stage 7B connection)
5. **Scope creep** — Phase 2 (China portal) is large; could delay core functionality

---

## Critical Recommendations

### Immediate (Before Build Starts)

1. **Schema Reconciliation Meeting**
   - Owner: Cem, Harry, Jay Mark
   - Agenda: Align PROJECT.md schema with Harry's existing tables
   - Output: Single canonical schema document

2. **Data Pipeline Decision**
   - Confirm: BigQuery → Supabase as only pipeline
   - Archive: MySQL references in Blueprint V3
   - Document: Sync frequency, error handling

3. **Architecture Decision**
   - Choose: Cloud Run standalone OR ecell.app module
   - Document in both PROJECT.md and Blueprint V3

### Short-Term (Week 1-2)

4. **Integration Mapping**
   - Define: PULSE → reorder algorithm connection
   - Define: Shipment delivery → Fulfillment Portal trigger
   - Define: Stock availability → listing status

5. **China Portal Architecture**
   - Decide: china.ecell.app vs ecell.app/china vs separate
   - Plan: Authentication (do China staff have Supabase accounts?)

### Medium-Term (Week 3-4)

6. **Migration Plan**
   - Document: How to move from current Excel/email workflows
   - Test: Harry's existing data migration to aligned schema
   - Rollout: UK pilot → FL → PH → China

---

## Questions for Cem

1. Should Inventory Ordering App be a standalone Cloud Run service or integrated into ecell.app?
2. Do Harry's existing finance tables take precedence over PROJECT.md schema?
3. Is the China office portal a Phase 2 priority or can it wait until core is stable?
4. Should PULSE velocity signals directly influence reorder quantities, or keep them separate?

---

*Prepared by Hermes | 2026-04-13*
*Save to: ~/Vault/03-Agents/Hermes/ADVISORY_INVENTORY_ORDERING_APP.md*
