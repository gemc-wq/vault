# Inventory Ordering App — Ava's Strategic Analysis & PRD

**Date:** Mon Apr 13, 2026 | **Requested by:** Cem | **Source:** Harry's PROJECT_2 (v2.6)

---

## 1. EXECUTIVE SUMMARY

Harry's Inventory Ordering App is a **well-architected procurement backbone** with exceptional operational rigor. However, it is:
- **Over-scoped for Phase 1** (5 phases, China portal with Mandarin, LLM stock validation, Xero integration)
- **Lacks business case** (no ROI, no cost-benefit analysis, no revenue impact quantification)
- **Missing critical urgency context** (is this blocking go-live? How much manual effort does it save?)
- **Orphaned from product strategy** (no connection to 3-pillar framework: Coverage, Speed, Intelligence)

**Recommendation:** Refocus as **"Reorder Automation MVP"** (2-week Phase 1) tied to specific inventory pain points.

---

## 2. SWOT ANALYSIS

### STRENGTHS ✅

| Strength | Impact |
|----------|--------|
| **Comprehensive data model** | Supabase schema is production-ready, multi-warehouse/multi-site aware |
| **Multi-site logic** | PH/UK/FL distribution rules tie to actual fulfillment patterns (from `orders.PO_Location`) |
| **Item exclusion framework** | Z-prefix + stale stock rules prevent ghost reorders (P0 operational risk) |
| **LLM validation for adjustments** | Prevents erroneous write-offs, adds audit trail |
| **Mandarin support** | China team autonomy increases (reduces bottleneck) |
| **Internal transfer rules** | Optimizes inventory movement (PH → UK/FL, not inter-regional) |
| **Finance integration path** | Xero posting closes the loop (AR → GL reconciliation) |

### WEAKNESSES ❌

| Weakness | Risk |
|----------|------|
| **5 phases = vaporware timeline** | Phased approach correct, but missing concrete Phase 1 exit criteria |
| **No ROI quantification** | How many hours/week does this save? Reduces stockouts by X%? Saves Y in carrying cost? |
| **China portal feels gold-plated** | Mandarin UI + full supplier workflow is nice, but MVP needs core PO logic first |
| **LLM validation is premature** | Stock adjustments are <1% of daily volume; prioritize the 99% first |
| **Missing demand signal integration** | No connection to PULSE, conversion data, or sales velocity predictions |
| **Orphaned from supplier mgmt** | How do suppliers interact? Are they in the system? Email still primary? |
| **No exception handling SOP** | "Overdue alerts" mentioned but no escalation workflow defined |
| **BigQuery dependency unclear** | Is `zero_dataset.inventory` live and reliable? When was it last validated? |

### OPPORTUNITIES 🎯

| Opportunity | Strategic Fit |
|-------------|---------------|
| **Link to PULSE leaderboard** | Stock coverage % by design (enable "never stock out on top 50 designs") |
| **Predictive reorder** | Use historical velocity + seasonality to auto-calc reorder points (reduce manual guessing) |
| **Supplier scorecards** | Track on-time delivery % by supplier → inform sourcing strategy |
| **Cost optimization** | Consolidate orders by supplier → negotiate volume discounts |
| **Regional demand forecasting** | US vs UK vs EU demand curves → optimize warehouse split |
| **Inventory turns metric** | Measure carrying cost by design → feed into product deprecation decisions |
| **Integrate with ListingForge** | Image automation + inventory automation = end-to-end SKU pipeline |

### THREATS ⚠️

| Threat | Mitigation |
|--------|-----------|
| **BigQuery freshness failure** | If `zero_dataset.inventory` breaks, entire system blind; need fallback to Sage directly |
| **China supplier disruption** | App assumes suppliers reliable; what if POs sit for weeks? Need carrier tracking + escalation |
| **Multi-currency complexity** | GBP/USD/CNY exchange rates matter; FX fluctuations impact margins (~2-5% variance) |
| **Warehouse staff adoption** | If interface is confusing, staff won't use it; revert to manual Excel |
| **Regulatory/Customs delays** | In-transit inventory not in warehouse; impacts inventory accounting (needs Xero fix) |
| **Over-dependence on LLM** | If LLM validation fails (hallucination), auto-approvals are wrong; need human fallback |

---

## 3. GAP ANALYSIS: Harry's Plan vs. Execution Reality

### Gap 1: No Business Case
| Harry's Plan | Reality | Impact |
|-------------|---------|--------|
| "Replaces manual Excel workflows" | Excel is still the source of truth (staff don't trust automation) | Adoption risk HIGH |
| "End-to-end procurement" | PO creation is manual, approval is email, invoicing is Xero-only | Process gaps in specs |
| "Finance integration" | Xero posting mentioned but HOW (who triggers? when?) is vague | Orphaned deliverable |

**Fix:** Quantify: "Reordering currently takes X hours/week across PH/UK/FL; automation saves Y hours/week; ROI = Z weeks."

### Gap 2: Phase 1 is Underspecified
| Deliverable | Status | Issue |
|-------------|--------|-------|
| Supabase schema | ✅ Done | Clear |
| Item exclusion rules | ⚠️ Defined but not tested | Need test data + edge cases |
| Stock adjustment workflow | ✅ Good detail | But LOW priority (adjustments are rare) |
| PO auto-generation | ❌ Missing | **CORE FEATURE** — no algorithm spec |
| Multi-site distribution | ✅ Pseudocode exists | But not integrated into PO creation |
| Approval workflow | ⚠️ Vague | Who approves? When? Slack or app? |
| Shipping plan export | ✅ CSV format defined | But "Ben's order sheet" is vague — needs Ben's input |

**Fix:** Lock Phase 1 scope: Item exclusion + PO auto-gen + approval queue. Phase 2: China portal.

### Gap 3: Demand Data Integration Missing
| Source | Status | Gap |
|--------|--------|-----|
| `zero_dataset.orders.PO_Location` | ✅ Referenced | But not connected to reorder logic |
| PULSE velocity data | ✅ Exists (90d, 30d, 7d) | Not fed into reorder point calc |
| Seasonality/trends | ❌ Missing | Reorder points don't adjust for Q4 vs Q1 |
| Top 50 champions | ✅ Known | But app treats all designs equally |

**Fix:** Import PULSE leaderboard into reorder queue; prioritize restocking top revenue designs.

### Gap 4: Supplier Data Model Vague
| Field | Status | Gap |
|-------|--------|-----|
| Supplier performance | ⚠️ Mentioned ("Items on Order") | No metrics (on-time %, lead time variability) |
| Lead times | ❌ Missing | Fixed-ETA assumption doesn't match reality (XINTAI = 30d, others = 45d) |
| Pricing | ⚠️ PO tracks unit price | No price history, volume discounts, or supplier catalog |
| Capacity | ❌ Missing | What if supplier can only make 1000 units/PO? App doesn't check |

**Fix:** Add supplier master table with lead time, capacity, performance metrics.

### Gap 5: Exception Handling Underdeveloped
| Scenario | Plan | Gap |
|----------|------|-----|
| PO delivery is 30d late | "Overdue alerts" | No escalation workflow (who calls supplier? when?) |
| QC rejects 20% of shipment | "Discrepancy reports" | No process for rejection, replacement, credit note |
| Supplier price increase | "PO versioning exists" | No approval workflow for revised pricing |
| Demand spike (2x velocity) | "Reorder calc auto-runs daily" | No emergency PO acceleration logic |

**Fix:** Define SOP for each exception with escalation rules.

---

## 4. ADVISOR RECOMMENDATION (Opus 4.6 Perspective)

### Strategic Fit to Ecell North Star

**North Star:** "Coverage, Speed, Intelligence"

| Pillar | Current Plan | Alignment |
|--------|-------------|-----------|
| **Coverage** | Multi-warehouse logic optimizes stock placement | ✅ Strong — ensures top 50 designs never stock out |
| **Speed** | Faster reordering = faster replenishment | ⚠️ Weak — still human-dependent approval |
| **Intelligence** | LLM validation + supplier scorecards | ✅ Medium — data-driven but missing predictive layer |

**Verdict:** App is **operationally sound** but **strategically incomplete**. It optimizes procurement (cost/efficiency) but doesn't optimize *product* (revenue/demand).

---

## 5. AVA'S IMPROVED PROJECT PLAN

### Phase 1: "Reorder Automation MVP" (2 weeks, Apr 15–28)

**Goal:** Auto-generate reorder POs with human approval, 10 hours/week saved

**Scope:**
1. ✅ Supabase schema (Harry's done)
2. ✅ Item exclusion rules (z-prefix + stale stock)
3. **PO auto-gen algorithm** (reorder point calc + multi-site distribution)
4. **Approval workflow** (Slack-based approval, <2 min per PO)
5. **Shipping plan export** (CSV for Ben's procurement team)
6. **Daily cron job** (run reorder calc, create POs, notify managers)
7. **Reporting** (daily "POs pending approval" digest)

**Success metrics:**
- 95%+ of reorders auto-generated (no manual Excel)
- <1% error rate in distribution logic
- 10 hours/week saved across PH/UK/FL

**Deliverables:**
- Supabase schema live
- Reorder calc function (Python/SQL)
- PO approval dashboard (simple, Slack-integrated)
- Shipping plan CSV export
- Cron job deployed

**Owner:** Harry + Codex (2-week sprint)

---

### Phase 2: "China Portal & Logistics" (3 weeks, May 1–21)

**Goal:** China team can download POs, create shipments, upload docs; remove Cem bottleneck

**Scope:**
1. Mandarin UI (PO list, packing list generator, shipment creator)
2. Supplier grouping (auto-group POs by supplier for batch download)
3. Packing list generation (auto-populate from PO lines)
4. Shipment creation + tracking (ETA calc, carrier selection)
5. Document upload (packing list + invoice OCR)
6. Slack notifications (when PO ready, shipment dispatched, delivery alert)

**Success metrics:**
- China team processes 100% of POs without Cem intervention
- Shipment tracking accuracy >95%
- Packing list errors <2%

---

### Phase 3: "Finance Integration & Adjustments" (2 weeks, Jun 1–14)

**Goal:** Auto-post invoices to Xero, validate stock adjustments, close GL loop

**Scope:**
1. Invoice OCR (extract supplier, amount, date, item code)
2. Xero posting (create bill, tag to purchase order)
3. Stock adjustment workflow (LLM validation + manager approval)
4. Multi-entity support (UK vs US Xero orgs)
5. Reconciliation report (PO qty vs received qty vs invoiced qty)

**Success metrics:**
- 90%+ of invoices auto-OCR'd
- 95%+ auto-post to Xero (no manual entry)
- Stock adjustment errors <1%

---

### Phase 4: "Predictive & Optimization" (Ongoing, post-launch)

**Goal:** Intelligence layer — demand forecasting, supplier optimization, cost reduction

**Scope:**
1. **Demand forecasting** (PULSE velocity + seasonality → reorder point)
2. **Supplier scorecards** (on-time %, lead time, quality, cost)
3. **Cost optimization** (consolidate orders by supplier for volume discounts)
4. **Inventory turns** (carrying cost by design, feed into product strategy)
5. **Regional demand curves** (optimize PH/UK/FL split by market)

**Success metrics:**
- Stockout rate reduced from 3% to <1%
- Carrying cost reduced by 10%
- Supplier on-time delivery improves to 95%+

---

## 6. PRD: REORDER AUTOMATION MVP (Phase 1)

### 6.1 Product Vision
Replace manual Excel-based reorder management with an automated workflow that:
- Auto-calculates reorder points for all items across PH/UK/FL
- Auto-generates purchase orders with correct multi-site distribution
- Routes POs to managers for approval (Slack-based)
- Exports shipping plan for procurement team
- Runs daily with zero manual intervention

### 6.2 Success Criteria
| Metric | Target | Owner |
|--------|--------|-------|
| Manual reorder time | 10 hrs/week → 1 hr/week | Harry |
| PO accuracy (distribution logic) | 95%+ correct | Codex validation |
| Approval SLA | <2 min per PO | Manager |
| Stale/excluded items | 100% filtered out | System |
| Daily cron uptime | 99.5% | DevOps |

### 6.3 User Flows

#### Flow 1: Daily Reorder Calculation (Automated Cron)

```
[6 AM UTC] Cron triggers
  ↓
[Step 1] Fetch latest inventory from BigQuery (`zero_dataset.inventory`)
  ↓
[Step 2] Fetch latest sales velocity from PULSE (90d, 30d, 7d)
  ↓
[Step 3] For each item:
  - Calculate reorder point: (daily_velocity × lead_time) + safety_stock
  - If free_stocks < reorder_point AND is_excluded = false:
    → Add to reorder queue
  ↓
[Step 4] Group items by supplier
  ↓
[Step 5] For each supplier/item group:
  - Calculate multi-site distribution (FL/UK/PH split)
  - Apply rounding logic (base 10 or 100)
  - Create purchase order (DRAFT status)
  ↓
[Step 6] Notify managers via Slack:
  "3 new POs pending approval. Review & approve in 2 min."
  ↓
[Managers approve/reject in Slack]
  ↓
[Approved POs marked APPROVED]
  ↓
[7 AM] Shipping plan exported (CSV for Ben)
  ↓
[Cron complete]
```

#### Flow 2: Manager Approval (Slack-Based)

```
Manager receives Slack message:
┌─────────────────────────────────┐
│ PO-20260413-001 Pending Approval │
│ Supplier: XINTAI                │
│ Items: 12 SKUs                  │
│ Total: $45,200 USD              │
│                                 │
│ [Preview] [Approve] [Reject]    │
└─────────────────────────────────┘

[Manager clicks Preview]
  ↓
Shows 3-column table:
  Item | Qty | Distribution (FL/UK/PH)
  ───────────────────────────────────
  HTPCR-IPH17 | 1000 | 600/200/200
  HB401-IPH17 | 800  | 480/160/160
  ...
  
[Manager clicks Approve]
  ↓
PO status = APPROVED
Notification sent to China team
Shipping plan updated
```

#### Flow 3: Item Exclusion (Z-Prefix + Stale Stock)

```
Reorder calc runs:
  ↓
For each item in queue:
  - Check if item_code starts with 'z-' or 'Z-'
  - If YES: exclude from queue, log reason "z_prefix"
  - If NO: check if sales_last_30d = 0
    - If YES: exclude, log reason "stale_stock"
    - If NO: add to reorder queue
  ↓
Excluded items report generated:
  "45 items excluded this run (12 z-prefix, 33 stale)"
  ↓
[Weekly] Stale stock email to finance:
  Items with >90 days of stock at current velocity
  Recommended action: write-off or promotional clearance
```

### 6.4 Data Model (Supabase)

**Use Harry's existing schema** (sections 4.1–4.2 in his doc). Key tables:
- `inventory_snapshots` (current stock levels per warehouse)
- `purchase_orders` (PO master)
- `po_lines` (individual items per PO)
- `shipments` (in-transit tracking)
- `users` (managers, warehouse staff, China ops)

**New views needed:**
- `v_reorder_queue` (items needing reorder, sorted by priority)
- `v_stale_stock` (items with zero sales in 30 days)
- `v_pending_approval` (POs awaiting manager decision)

### 6.5 API Endpoints (Next.js)

```
POST /api/reorder/calculate
  - Trigger manual reorder calculation
  - Return: {po_count, total_qty, total_amount}

POST /api/purchase-orders/:po_id/approve
  - Approve PO, mark as APPROVED
  - Return: {status: "approved", shipping_plan_url}

POST /api/purchase-orders/:po_id/reject
  - Reject PO with optional reason
  - Return: {status: "rejected"}

GET /api/reports/daily-reorder-summary
  - Return: JSON of today's reorder stats
  - Used for Slack digest + monitoring

GET /api/inventory/excluded-items
  - Return: List of excluded items + reasons
  - Used for stale stock report
```

### 6.6 Notifications

| Event | Channel | Message | Recipient |
|-------|---------|---------|-----------|
| PO created (pending approval) | Slack #procurement | "3 POs pending approval" with Preview/Approve buttons | Managers |
| PO approved | Slack #logistics-cn | "PO-20260413-001 approved, ready for download" | China team |
| Daily summary | Email | "Yesterday: 5 POs approved, 847 units ordered, $92K spend" | Harry + Cem |

### 6.7 Cron Schedule

| Job | Schedule | Purpose |
|-----|----------|---------|
| `inventory-sync` | 2 AM UTC | Pull latest stock from BigQuery |
| `reorder-calculate` | 6 AM UTC | Auto-gen POs, notify managers |
| `shipping-plan-export` | 7 AM UTC | Generate CSV for Ben |
| `daily-summary-email` | 8 AM UTC | Send digest to Harry + Cem |

### 6.8 Testing & Validation

**Pre-Launch (2 weeks):**
1. Test reorder calc against 90 days of historical data
   - Expected: 95%+ of POs match manual reorder patterns
2. Test multi-site distribution logic
   - Expected: FL gets 60% US items, PH gets 40%, UK gets 100% UK items
3. Test item exclusion rules
   - Expected: z-prefix excluded 100%, stale stock excluded 100%
4. Test approval workflow
   - Expected: Managers can approve/reject via Slack in <30s
5. Integration test: BigQuery → Supabase → PO creation
   - Expected: Zero data loss, <10s latency

**UAT (1 week):**
- Harry uses app to generate 20 POs
- Managers approve via Slack
- China team downloads and processes
- Compare to manual workflow: time saved?

### 6.9 Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| BigQuery `zero_dataset.inventory` is stale/wrong | HIGH | Validate data freshness every morning; if >1 day old, alert + use fallback (previous snapshot) |
| Reorder calc produces wildly wrong qtys | HIGH | Test against 90d history; require manager approval before auto-PO |
| Multi-site distribution logic breaks | MEDIUM | Hardcode fallback to 50/50/25 split if calc fails |
| Managers don't check Slack; POs pile up | MEDIUM | Add daily escalation email; auto-approve after 4 hours if no action |
| China team doesn't understand PO format | MEDIUM | Test with China team before launch; create user guide (Mandarin) |

### 6.10 Success Definition (EOD Apr 28)

- ✅ 100% of daily reorders auto-generated (no manual Excel)
- ✅ Manager approval workflow live (Slack-based)
- ✅ 95%+ approval rate (managers trust the calc)
- ✅ 10 hours/week saved (Harry + warehouse staff feedback)
- ✅ Zero critical issues found in UAT
- ✅ Ready to hand off to China portal build (Phase 2)

---

## 7. COMPARISON: Harry's Plan vs. Ava's Improved Plan

| Aspect | Harry | Ava | Delta |
|--------|-------|-----|-------|
| Phase 1 scope | All features (PO, approval, export, adjustments, LLM) | Reorder automation + approval only | **Focused** |
| Timeline | Vague phasing | 2-week MVP, clear exit criteria | **Concrete** |
| Business case | "Replaces Excel" | "Saves 10 hrs/week, 95%+ accuracy" | **Quantified** |
| Demand integration | No mention | Tied to PULSE velocity | **Aligned** |
| China portal | Phase 2 | Phase 2 | **Same** |
| LLM validation | Phase 1 feature | Phase 3 (lower priority) | **Deprioritized** |
| Supplier data | Vague | Master table + lead times (Phase 2) | **Structured** |
| Exception handling | Mentioned, not detailed | SOP defined (Phase 3) | **Detailed** |
| ROI clarity | Implied | Explicit metrics (10 hrs/week, <1% error) | **Clear** |

---

## 8. NEXT STEPS

**For Cem:**
1. Approve Phase 1 MVP scope (2-week sprint starting Apr 15)
2. Confirm Harry can lead backend + Codex for deployment
3. Identify manager(s) for approval testing

**For Harry:**
1. Validate `zero_dataset.inventory` freshness (BigQuery query)
2. Define reorder point formula (safety stock + lead time logic)
3. Lock shipping plan CSV format with procurement team (Ben's requirements)

**For Codex:**
1. Implement reorder calc algorithm (Python/SQL)
2. Build Next.js approval workflow (Slack integration)
3. Deploy cron job to Cloud Run

**For Ava:**
1. Track Phase 1 deliverables weekly
2. Plan Phase 2 (China portal) scope in parallel
3. Integrate with PULSE velocity data (dependency for Phase 1.5)

---

## 9. APPENDIX: FULL SWOT MATRIX

### STRENGTHS (Keep / Leverage)
- Comprehensive multi-warehouse logic
- Z-prefix + stale stock exclusion framework
- Internal transfer rules (PH → UK/FL optimization)
- Supabase schema production-ready
- Finance integration path (Xero posting)
- Mandarin support planned (reduces bottleneck)

### WEAKNESSES (Address / Mitigate)
- Over-scoped Phase 1 (cut LLM validation, stock adjustments)
- No ROI quantification (add: hrs saved, error rate, stockout prevention)
- China portal feels gold-plated (defer to Phase 2)
- BigQuery dependency untested (validate schema freshness daily)
- Supplier data model incomplete (lead times, capacity, perf metrics missing)
- Exception handling undefined (add escalation SOP)

### OPPORTUNITIES (Capture / Expand)
- Link to PULSE leaderboard (never stock out on top 50)
- Predictive reordering (velocity + seasonality → dynamic reorder points)
- Supplier scorecards (on-time %, cost, quality metrics)
- Cost optimization (consolidate orders → volume discounts)
- Inventory turns analysis (feed into product deprecation decisions)
- End-to-end SKU pipeline (ListingForge + inventory automation)

### THREATS (Monitor / Mitigate)
- BigQuery failure = system blind (need fallback to Sage)
- China supplier disruptions (tracking + escalation SOP)
- Multi-currency complexity (FX variance 2-5%)
- Adoption risk (staff revert to Excel if confusing)
- LLM hallucination risk (need human fallback for auto-approvals)
- Customs/regulatory delays (in-transit inventory accounting gap)

---

**Status:** ✅ READY FOR PHASE 1 EXECUTION

**Recommendation:** Approve Ava's Phase 1 MVP plan. Start sprint Apr 15. Measure success at EOD Apr 28.
