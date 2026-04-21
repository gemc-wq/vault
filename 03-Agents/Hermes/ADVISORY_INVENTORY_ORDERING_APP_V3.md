# Advisory Report: Inventory Ordering App v2.6 — Scope Review
**Prepared by:** Hermes (Operations Librarian)
**Date:** 2026-04-13
**Reference:** PROJECT.md v2.6

---

## Executive Summary

Version 2.6 significantly expands scope with **warehouse staff portal**, **LLM-validated stock adjustments**, and **internal transfer rules**. The spec is now comprehensive but introduces **build complexity trade-offs**.

**Recommendation:** Split into **Core (Phase 1)** and **Intelligence (Phase 2)** to avoid blocking procurement automation on LLM features.

---

## What's New in v2.6

| Feature | Complexity | Phase Recommendation |
|---------|------------|---------------------|
| **Warehouse Staff Portal** | LOW | Phase 1 — Simple read-only views |
| **Stock Adjustment + LLM Validation** | HIGH | Phase 2 — Requires LLM integration |
| **Internal Transfer Rules (PH→UK/FL)** | MEDIUM | Phase 1 — Logic is well-defined |
| **Item Exclusion (z-prefix, stale stock)** | LOW | Phase 1 — SQL filters |
| **Multi-site distribution logic** | MEDIUM | Phase 1 — Core feature |
| **Rounding logic (base 10/100)** | LOW | Phase 1 — Simple function |
| **Shipping plan CSV/PDF export** | LOW | Phase 1 — Standard output |

---

## Scope Risk Assessment

### HIGH Complexity — Consider Deferring

**LLM Stock Adjustment Validation**

The LLM validation logic is sophisticated:
- Checks recent receipts (5-day window for weekends)
- Cross-references shipments, production records
- Confidence scoring (0-100)
- Multi-tier approval thresholds
- Auto-approve vs manager review vs CFO review

**Risk:** This adds significant build time and requires:
1. LLM API integration (OpenAI/Anthropic)
2. Context gathering from multiple tables
3. Confidence scoring logic
4. Approval workflow state machine

**Recommendation:** Start with **simple manager approval** in Phase 1. Add LLM validation in Phase 2.

---

### MEDIUM Complexity — Include in Phase 1

**Internal Transfer Rules**

Well-specified:
- PH → UK: ✅
- PH → FL: ✅
- UK ↔ FL: ❌ (high freight)
- CN: Staging only (flag as error if stock exists)

**Implementation:** Straightforward conditional logic. Include in Phase 1.

**Multi-Site Distribution**

Pseudocode provided. Clear product type mapping:
- HTPCR, HC, HB401, H89, HDMWH → FL 60%, PH 40%
- HLBWH → PH 80%, FL 20%
- Default → FL 37.5%, UK 37.5%, PH 25%

**Implementation:** TypeScript function as specified. Include in Phase 1.

---

### LOW Complexity — Include in Phase 1

**Item Exclusion Rules**
```sql
WHERE LOWER(item_code) NOT LIKE 'z-%'
AND (sales_last_30d > 0 OR sales_last_7d > 0)
```

**Rounding Logic**
```typescript
const roundingBase = totalNeed >= 1000 ? 100 : 10;
return Math.round(value / base) * base;
```

**Warehouse Staff Portal**
- Read-only top 50 items by velocity
- Traffic light status
- Simple stock adjustment request form (no LLM initially)

---

## Remaining Gaps

### 1. Builder Assignment — CRITICAL
**Status:** TBA (could be Hermes, Claude Code CLI, or Codex)

**Question:** What's the decision criteria for builder selection?
- Hermes: Best for iterative, human-in-loop development
- Claude Code CLI: Best for autonomous, spec-complete builds
- Codex: Best for rapid prototyping

### 2. LLM Provider for Stock Validation — UNDEFINED
- OpenAI GPT-4?
- Anthropic Claude?
- Local model (cost savings)?

**Recommendation:** Start with Claude via API (best reasoning for validation tasks).

### 3. Stale Stock Threshold — CLARIFICATION NEEDED
Spec says:
- "No sales in 30 days" → exclude from reorder
- "No sales in 90+ days" → flag for review

**Question:** Is 30 days the right threshold? Some items may be seasonal.

### 4. Rounding Threshold — STILL UNDEFINED
Spec shows:
```typescript
const roundingBase = totalNeed >= 1000 ? 100 : 10;
```

**Question:** Is 1000 units the threshold? Or should it be configurable per product type?

---

## Build Strategy Recommendation

### Phase 1A: Core Procurement (2 weeks)
- Inventory sync from BigQuery
- Reorder queue with exclusions
- Multi-site distribution logic
- PO creation with shipping plan
- CSV/PDF export for Ben
- Manager approval workflow

### Phase 1B: Warehouse Portal (1 week)
- Top selling items view
- Stock on hand with traffic lights
- Simple stock adjustment requests (manager approval, no LLM)

### Phase 2A: Intelligence Layer (2 weeks)
- LLM stock adjustment validation
- Confidence scoring
- Auto-approve thresholds
- CFO review queue

### Phase 2B: China Portal (2 weeks)
- Mandarin UI
- PO download by supplier
- Shipment creation
- Document upload

---

## Questions for Cem

1. **Builder selection:** What factors determine whether Hermes, Claude Code CLI, or Codex builds this?

2. **LLM provider:** Which API for stock validation — OpenAI, Anthropic, or other?

3. **Phase priority:** Should we defer LLM validation to Phase 2 and ship core procurement faster?

4. **Stale stock threshold:** Is 30 days correct, or should it vary by product type?

5. **Rounding threshold:** Confirm 1000 units as base 10→100 switch point?

---

## Summary

Version 2.6 is a well-designed, comprehensive spec. The main risk is **scope creep delaying core procurement automation**.

**Recommendation:**
- Phase 1: Core procurement + warehouse portal (no LLM)
- Phase 2: LLM validation + China portal

This gets reordering automation live in 2-3 weeks while intelligence features are built in parallel.

---

*Prepared by Hermes | 2026-04-13*
