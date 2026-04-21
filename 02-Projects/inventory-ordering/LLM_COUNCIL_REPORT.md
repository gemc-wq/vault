# LLM Council Report — Master PRD Edge Case Review
**Date:** 2026-04-13 | **PRD Version:** 1.0
**Council:** Code Architect (Claude Opus) + Adversary (Claude Sonnet) + Codex (GPT-5.4, pending)

---

## COUNCIL VERDICT: CAUTION → PROCEED with 12 fixes

The PRD is well-constructed and the data integrity work is rigorous. But **5 issues will silently corrupt data** without throwing visible errors. These must be fixed in the spec before build.

---

## TOP 12 FIXES REQUIRED (Merged from all reviewers)

### CRITICAL — Silent data corruption (fix before build)

| # | Issue | What Happens | Fix |
|---|-------|-------------|-----|
| **1** | PH allocation divides by zero when FL+UK velocity both zero | PH stock becomes invisible to both zones. System orders stock that already exists in PH. | Replace guard: if both zero, default to 60/40 split. Not `0/0`. |
| **2** | NULL stock for items missing from a warehouse | `NULL + number = NULL` in SQL, `NaN` in TypeScript. Allocation produces garbage. | COALESCE all stock reads to 0. Ensure every active item has a row per warehouse. |
| **3** | Transfer deducts PH stock but supplier order reads stale snapshot | PO calc sees pre-transfer PH stock → orders more for PH that's already en route to FL. Double-ordering. | Supplier ordering must use `effective_ph_stock = free_stocks - pending_transfers_out`. |
| **4** | In-transit stock not deducted from zone need | 200 units in transit to UK, zone needs 150 → system orders 150 more. Double-ordering. | `zone_need = MAX(0, target - stock - in_transit_to_zone)` |
| **5** | Stale exclusion hides genuine stock-outs | Item stocked out → zero sales for 30d (demand suppression) → classified "stale" → excluded from reorder. Never gets restocked. | Stale rule: `sales_30d = 0 AND free_stocks > 0 AND in_transit = 0`. Zero stock items are NOT stale. |

### HIGH — Will cause operational problems

| # | Issue | What Happens | Fix |
|---|-------|-------------|-----|
| **6** | No data freshness check on cron | BigQuery sync fails → cron generates recommendations on yesterday's data → nobody knows. | Check `snapshot_date` before running. If >6h old, abort + Slack CRITICAL alert. |
| **7** | Rounding can produce negative PH allocation | Small zone share × ratio → rounds to 0 → subtraction goes negative → "ship -10 to PH." | Add `Math.max(0, ...)` on all intermediates. Assert `FL + UK + PH === total`. |
| **8** | Concurrent on-demand + scheduled runs generate duplicate suggestions | Stock-out alert at 10:00 Friday + scheduled cron at 10:00 → two runs → overlapping transfer lists. | Run lock table with `SELECT FOR UPDATE SKIP LOCKED`. Queue and coalesce triggers. |
| **9** | PH is stocked out — no one transfers TO PH | PH has 95 stock-outs now. It's both transfer source AND fulfillment site. No workflow for PH replenishment. | Daily cron: if PH `free_stocks = 0` + `sales_7d > 0`, generate HIGH-priority supplier order for PH. Not just bi-weekly. |
| **10** | LLM auto-delivery violates human gatekeeper principle | Section 11.2: LLM confirms delivery → auto-add stock + auto-post to Xero. No human step. Hallucinated "delivered" corrupts stock AND ledger. | LLM sets status to `DELIVERED_PENDING`. Warehouse confirms in portal. Then stock writes + Xero posts. |
| **11** | Best seller set is flat — not zone-aware | UK best seller gets MAX(7d,30d) applied to its FL velocity too, inflating US allocation for a UK-popular item. | Zone-aware sets: `{ global, zoneUS, zoneUK }`. Apply per-zone. |
| **12** | 60/40 and 75/25 default ratios have no data backing | Hardcoded splits may not reflect actual fulfillment patterns. If wrong, every allocation is systematically biased. | Store in `product_group_config` table. Validate against 1 quarter of historical shipment data. Make admin-editable. |

---

## ADDITIONAL FINDINGS (fix during shadow mode, before cutover)

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 13 | NULL velocity columns (not zero) propagate NaN through calculations | HIGH | NOT NULL DEFAULT 0 constraints on all velocity columns |
| 14 | Negative velocity from bulk returns reads as healthy (negative days_of_cover) | MEDIUM | `Math.max(0, velocity)` guard. Log negatives as anomalies. |
| 15 | Best seller rank ties at position 50 are non-deterministic | MEDIUM | Add tiebreaker: `ORDER BY velocity DESC, item_code ASC` |
| 16 | Friday holiday → duplicate transfer suggestions next week | MEDIUM | Check for unconfirmed SUGGESTED transfers before generating new ones. Roll forward. |
| 17 | Damaged goods in transit — no partial receipt on transfers | MEDIUM | Add `received_qty` and `damage_notes` to `internal_transfers` table. |
| 18 | New products with zero history are invisible to reorder system | MEDIUM | "New Items" review queue: `created < 45d AND sales_30d = 0 AND stock > 0`. |
| 19 | Layer 2 (Claude API) down → unclear if recommendations still flow | MEDIUM | Layer 2 is non-blocking. Add `layer2_status` column. Portal shows recs with "AI validation unavailable" banner. |
| 20 | Cron fails silently — no heartbeat monitoring | MEDIUM | Write start/end records to `operational_events`. Health check every 15min alerts on missing completion. |
| 21 | OCR confidence not gated before Xero posting | MEDIUM | Min 85% OCR confidence before auto-post. Below → MANAGER_REVIEW. |
| 22 | Supabase down on Friday → transfers block entirely | LOW | Email PDF backup of suggested transfer list at 07:00 Fridays. Confirm via reply. |
| 23 | Chris + Jae both unavailable → no one confirms transfers | LOW | Any MANAGER-role can approve. Escalate to ADMIN if HIGH-priority unconfirmed >4h. |
| 24 | Phantom micro-orders from rounding near-zero need | LOW | Minimum threshold: `if (total_need < 1.0) return zero`. Add MOQ floor per product group. |

---

## ADVERSARY VERDICT

**CAUTION → PROCEED** if these 5 conditions are met:

1. ✅ Sync freshness check (fix #6 above)
2. ✅ Evidence basis for default ratios (fix #12 above)
3. ✅ OCR confidence threshold for Xero (fix #21 above)
4. ✅ Decouple Xero from shadow mode cutover gate
5. ✅ Investigate why 95 stock-outs are exclusively in PH

---

## SHADOW MODE METRICS (Adversary recommendation)

For cutover from Zero to new system, compare:

| Metric | Threshold |
|--------|-----------|
| Items flagged for reorder | ≥90% overlap with Zero's output |
| Recommended quantities | Within ±15% of Zero's quantities |
| Transfer destinations | 100% match (FL/UK/PH routing) |
| Stock-out prevention | New system flags all items Zero flagged + extras |
| False positives | <5% recommendations that Zero would not have made |

Run parallel for minimum 2 full cycles (4 weeks) before cutover.

---

## ARCHITECTURAL RECOMMENDATION

**Defer Layer 2 (Claude API intelligence) to post-cutover.**

Both Adversary and Code Architect agree: Layer 1 (SQL/cron) + Layer 3 (portal) are sufficient for shadow mode and initial cutover. Layer 2 adds complexity without immediate value if the SQL logic is correct. Add the intelligence layer once the deterministic layer is proven in production.

This reduces Phase 1 to: **correct data → correct math → human review**. Three moving parts, not four.

---

---

## CODEX (GPT-5.4) — Top 10 Concerns

| # | Concern | Severity | Overlap |
|---|---------|----------|---------|
| CX-1 | Normal items: 30d cover with 14-21d lead time + bi-weekly cadence = almost no buffer. Reorder view triggers at <21d but lead time alone is 21d. | HIGH | New — not caught by others |
| CX-2 | PH demand disappears in allocation math — PH velocity split by FL:UK ratio ignores PH-only channels (FBA) | HIGH | Reinforces fix #1 (div-by-zero) |
| CX-3 | Seasonal spikes trap stock in wrong zone — NFL/Premier League surges misallocated, can't transfer back | HIGH | New — seasonal override needed |
| CX-4 | Internal transfer uses `zone_target × 0.5` — only half-refills destination, pushes rest to slower China PO | MEDIUM | New — the 0.5 cap needs clarification |
| CX-5 | PH keeps only 14 days before donating — less than China lead time. PH becomes next stock-out after transfers. | HIGH | Reinforces fix #9 (PH replenishment) |
| CX-6 | Piggyback freight treated as infinite capacity — no overflow rule defined | MEDIUM | New |
| CX-7 | Shadow mode has no quantitative cutover standard — "confidence threshold" is subjective | HIGH | Addressed in shadow metrics above |
| CX-8 | Shadow mode tests list parity, not end-to-end workflow (approvals, tracking, receipt) | MEDIUM | New — need dry runs |
| CX-9 | Claude API Layer 2 is premature for Phase 1 — adds debugging complexity before base is proven | MEDIUM | Matches architectural recommendation |
| CX-10 | Best-seller rule inconsistency — tier table says MAX(7d,30d) but Consumers table says "7d velocity" | HIGH | New — spec contradiction to fix |

### NEW FIXES FROM CODEX (not in original 12)

| # | Fix | Priority |
|---|-----|----------|
| **13** | Normal item reorder threshold too late — <21d trigger but lead time is 21d. Change to <30d or add cadence buffer. | HIGH — fix before build |
| **14** | Add seasonal override process — manual zone-weight review before NFL/PL/holiday peaks | MEDIUM — before first season |
| **15** | Clarify the 0.5 cap on internal transfers — is it deliberate? If not, remove it. | MEDIUM — fix before build |
| **16** | PH safety stock should be ≥ lead time (21d), not flat 14d | HIGH — fix before build |
| **17** | Define piggyback capacity overflow rule | LOW — before cutover |
| **18** | Shadow mode: require end-to-end dry runs, not just list comparison | MEDIUM — before cutover |
| **19** | Fix spec contradiction: best sellers use MAX(7d,30d), not "7d velocity" | HIGH — fix before build |

---

## FINAL COUNCIL SUMMARY

**3 reviewers. 24 unique findings. 19 required fixes.**

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Silent data corruption | 5 | — | — | — |
| Operational problems | — | 7 | — | — |
| Shadow mode gaps | — | 2 | 3 | — |
| Spec contradictions | — | 2 | — | — |

**12 fixes required before build starts.** 7 more before cutover. None require rethinking the architecture.

The PRD is sound. The edge cases are fixable. Build can proceed once the critical 5 are addressed in the spec.

---

*Council report compiled by Athena | 2026-04-13*
*All three reviewers complete: Code Architect (Claude Opus), Adversary (Claude Sonnet), Codex (GPT-5.4)*
