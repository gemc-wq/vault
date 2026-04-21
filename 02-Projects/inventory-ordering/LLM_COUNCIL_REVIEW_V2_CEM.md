# MASTER PRD — LLM COUNCIL REVIEW
**Inventory Ordering App v1.0 | Ecell Global**
**Date:** 13 April 2026
**Council:** Claude Opus (Architecture & Risk) · GPT-5.4 (Business Logic) · Gemini Pro (Build Readiness)
**PRD Compiled by:** Athena (Chief of Staff) | **Builder:** Claude Code CLI

---

## 1. Executive Scorecard

| Dimension | Reviewer | Score | Grade |
|-----------|----------|-------|-------|
| Architecture & Data Model | Claude Opus | Fair | C+ |
| Business Logic Completeness | GPT-5.4 | Fair | C+ |
| Risk & Security | Claude Opus | High Risk | D |
| Build Readiness | Gemini Pro | 7.5 / 10 | B |
| **Overall PRD Quality** | **Council** | **Good Foundation — Not Yet Build-Ready** | **B−** |

---

## 2. Traffic Light Summary

### ✅ GREEN — Strong, proceed as-is
- PRD structure and document organisation
- Workflow diagrams (all 3 workflows clearly mapped)
- Supply Zone model with proportional PH allocation formula
- Data source clarity (orders table = 30% complete — documented, do not use)
- Phase plan and shadow mode strategy
- 3-layer agentic architecture ("AI recommends, human decides")

### ⚠️ AMBER — Address before build starts
- Business logic (velocity edge cases, AMBER threshold undefined)
- Build readiness (missing env specs, RLS policies, cron infrastructure decision)
- PH 14-day safety stock (likely too low for FBA role)
- Shadow mode output format (Zero's CSV schema not documented)

### 🔴 RED — Blockers — must fix before any production deployment
- Security controls (no invoice fraud gate, no PO approval threshold)
- Auto-approval abuse (no cumulative caps on stock write-offs)
- Architecture (missing master tables, cron dependency chain, FL/Florida live bug)
- BigQuery sync has no monitoring — silent failure is undetected

---

## 3. Architecture & Data Model Review
**Reviewer:** Claude Opus | **Grade: C+ (Fair)**

### Critical Issues — Production Breakers

**1. Missing Master Tables**
No `suppliers` table, no `products` master, no `warehouses` lookup, no `audit_log`. Multiple missing foreign keys:
- `po_lines` → `inventory_snapshots`
- `shipment_lines` → `po_lines`
- `supplier_invoices` → `purchase_orders`

Also missing: `sync_batch_id` / `synced_at` columns for pipeline tracing; `approved_by` / `approved_at` on relevant tables.

**2. Cron Dependency Chain — No Orchestration**
The pipeline `inventory-sync (06:00 UTC) → best_sellers_daily (06:30 UTC) → reorder-calculation (daily)` has zero dependency management. A delayed BQ sync at 06:00 causes the 06:30 best-sellers cron to run on stale data, poisoning the entire day's procurement recommendations.

> Fix: Use a DAG orchestrator — Cloud Workflows or `pg_cron` with explicit dependency checks before each step proceeds.

**3. PH Zone Formula — Live SQL Bug**
```sql
-- WRONG: || is string concatenation in PostgreSQL
PH_US% = FL_velocity / (FL_velocity + UK_velocity || 1)

-- CORRECT:
PH_US% = FL_velocity / NULLIF(FL_velocity + UK_velocity, 0)
```
When both velocities are 0 (new SKUs, seasonal lulls), the current formula throws a division-by-zero error. This affects every new item launch.

**4. FL/Florida Warehouse Code Duplication (Critical Finding C3 — Still Live)**
Using warehouse name strings to encode inventory type (blanks vs packaging) is a category error. `Florida` (10,337 items) and `FL` (99 items) are used interchangeably in some logic but mean different things.

> Fix: Add a `warehouses` lookup table with an `inventory_type` column and FK constraints. Normalise all references.

**5. In-Transit Double Counting**
CN→PH shipments allocated to Zone US via `PH_US%` can be double-counted alongside PH→FL internal transfers. Both contribute to `in_transit` stock in zone calculations with no state distinction.

> Fix: Implement an explicit stock state machine: `ON_HAND | IN_TRANSIT_SUPPLIER | IN_TRANSIT_INTERNAL`. Each state tracked separately in zone calculations.

**6. Missing Indexes — Performance Risk**
78% DISC items = every view scans ~165,916 rows (41,479 items × 4 warehouses) to find the 22% active items. No partial indexes defined.

```sql
-- Required partial index (example):
CREATE INDEX CONCURRENTLY idx_inventory_active
ON inventory_snapshots(item_code, warehouse)
WHERE product_group != 'DISC';
```
Estimated improvement: 2–5 second queries → <50ms.

**7. RLS Views Bypass Security**
Supabase views bypass Row Level Security by default. Every view (`v_reorder_queue`, `v_warehouse_top_selling`, etc.) needs `security_invoker = true`. The `users` table likely needs a junction table for multi-warehouse access rather than a single `warehouse_code` column.

**8. No Currency Column on Financial Tables**
Multi-currency operation (GBP, USD, CNY, EUR) with no currency tracking on Xero-bound records. Xero reconciliation will silently mix currencies across UK and US entities.

### What's Working
The 3-layer agentic architecture is sound. The proportional PH allocation math is elegant. The `best_sellers_daily` staging table pattern is the correct approach for pre-computed velocity.

---

## 4. Business Logic Review
**Reviewer:** GPT-5.4 | **Grade: C+ (Fair)**

### Critical Gaps

**1. No Downtrend Control in Velocity Formula**
The tiered velocity (`MAX(7d, 30d)` for best sellers) prevents over-ordering during upward spikes — but causes the opposite problem on downtrends. If a SKU's 30d velocity is high but it stopped selling last week, the system reorders to 45-day cover using inflated 30d numbers.

> Fix: Add downtrend flag. If `velocity_7d < velocity_30d * 0.6`, surface a human review alert before auto-generating PO. Do not auto-order into a declining trend.

**2. PH Scarcity Allocation Not Defined**
If multiple items simultaneously trigger PH→FL and PH→UK transfers and PH can't cover all of them, there is no priority queue. The system will silently under-allocate or fail.

> Fix: Priority = ascending `days_of_cover` at destination. Lowest cover = highest priority for PH surplus allocation.

**3. PH 14-Day Safety Reserve May Be Too Low**
PH is the FBA replenishment site. FBA typically requires 30–45 days of stock at Amazon's fulfilment centres. A 14-day PH safety stock buffer before triggering transfers means FBA risk every other week.

> Fix: Consider a separate FBA safety stock tier (30 days) distinct from general PH operational safety stock (14 days).

**4. 45-Day Cover Is Thin for Best Sellers**
Best sellers: 45 days cover. Bi-weekly ordering + 21-day lead time = 35-day worst case from next order cycle. This leaves only 10 days of buffer — any supplier delay or demand spike = stock-out on your most critical SKUs.

> Fix: Increase best-seller cover to 56 days (8 weeks). Or define an emergency single-item fast-track ordering process bypassing bi-weekly cadence.

**5. HB401 Converts 4× — Not Prioritised in Formula**
HB401 has disproportionate revenue impact (4× conversion vs HTPCR) but uses the same allocation formula. A stock-out on HB401 costs 4× more than a stock-out on HTPCR.

> Fix: Add `priority_multiplier` column to `products` master table. HB401 = 1.5× → 67-day cover (best seller tier × 1.5).

**6. AMBER Alert Threshold Not Defined**
The PRD introduces AMBER as a new alert level but never specifies the trigger formula.

> Suggested formula:
> `AMBER = days_of_cover < (lead_time_days + reorder_cycle_days)`
> Where: lead_time = 21 days, reorder_cycle = 14 days → AMBER triggers at <35 days of cover.

**7. No Supplier Lead Time Field in Data Model**
The 14–21 day range is hardcoded prose in the PRD. No `supplier_lead_time_days` column exists. This breaks when suppliers differ or during disruptions.

> Fix: Add `lead_time_days` to the `suppliers` master table (which is also missing — see Architecture section).

**8. Shadow Mode Output Format Undocumented**
For GAP analysis to work, both systems must produce comparable output. Zero's current CSV schema is not documented anywhere in the PRD.

> Fix: Before any build starts, document Zero's exact export format. The shadow mode comparison script joins on `item_code` and flags variances >5%.

### What's Working
The two-process procurement architecture (internal transfers + supplier orders) is the single biggest improvement over v2.6. The decision sequence logic (check PH first, partial coverage handling) is operationally sound.

---

## 5. Risk & Security Review
**Reviewer:** Claude Opus | **Risk Profile: HIGH — 3 Go-Live Blockers**

### 🔴 Go-Live Blockers

**BLOCKER 1: Invoice Fraud — No 4-Eyes Gate**
China ops can upload arbitrary PDFs → OCR → Claude API extraction → Xero posting with no human approval step. No three-way PO matching (PO qty vs packing list vs invoice amount). No supplier master validation. A fraudulent or inflated invoice posts to your accounting system automatically.

> Fix: Mandatory manager approval step before any Xero posting. Three-way match check (PO → packing list → invoice) as a pre-approval gate. Supplier whitelist validation.

**BLOCKER 2: PO Approval Threshold Undefined**
Explicitly acknowledged as unresolved in the PRD (Open Question #5). A manager could single-click approve a $500K PO.

> Suggested thresholds:
> | Amount | Approver |
> |--------|---------|
> | < $1,000 | Auto-approve |
> | $1,000 – $10,000 | Manager |
> | $10,000 – $50,000 | Finance Director |
> | > $50,000 | CEO / CFO |
>
> Implement as `approval_tier` column on `purchase_orders`.

**BLOCKER 3: BigQuery Sync Has No Monitoring**
Silent sync failure = stale data = wrong procurement decisions = the exact stock-outs this system exists to prevent. No `last_sync_at` tracking, no staleness detection, no alert on failure.

> Fix: Sync job writes `last_sync_at` to a `system_health` table. UI displays "Data as of: X hours ago" banner when >2 hours stale. Alert to `#ops-critical` Slack if sync >3 hours stale.

### 🟠 High Risks — Address Before Go-Live

**Claude Auto-Approval Abuse — No Cumulative Caps**
Per-adjustment caps exist (≤10 units at ≥90% confidence → auto-approve) but no daily/weekly cumulative threshold. 50 × 9-unit adjustments per warehouse per month = 450 units written off with zero human review.

> Fix: Daily cap of 50 units auto-approved per warehouse. Weekly cap of 200 units. Any breach → freeze auto-approvals for that warehouse, alert finance team.

**Auto Stock Receipt on Carrier Confirmation**
Section 11.3: "Delivery confirmed → auto-add stock to destination." If carrier API marks as "Delivered" but goods are lost, stolen, or only partially received, stock is inflated in the system.

> Fix: Carrier confirmation triggers `PENDING_RECEIPT` state (not immediate stock addition). Warehouse must confirm physical receipt in portal within 24 hours before stock is committed.

**China Portal File Injection**
PDF uploads processed by OCR → output fed directly to Claude API. A malicious PDF with embedded prompt injection text in invoice fields could manipulate Claude's data extraction output.

> Fix: Sanitise OCR output before passing to LLM. Validate extracted fields against expected invoice schema (numeric amounts, known supplier names, date formats). File type whitelist + 10MB size limit.

**Shadow Mode — No Environment Isolation**
No documented separation preventing shadow mode from writing to production Xero, production Slack channels, or changing live PO statuses.

> Fix: `SHADOW_MODE=true` env var. When set: block all Xero writes, redirect Slack to `#shadow-test` channel, disable PO status updates. Make shadow mode visually obvious in UI (banner or different colour scheme).

### Medium Risks
- Xero multi-entity routing logic (UK vs US entity) is unspecified — wrong routing = tax/compliance issues
- Slack webhooks contain PO numbers, stock levels, shipment data in potentially unsecured channels — ensure all logistics channels are private

---

## 6. Build Readiness Review
**Reviewer:** Gemini Pro | **Score: 7.5 / 10**

The PRD is strategically strong but lacks "last mile" engineering contracts needed to hand to Claude Code and start building today.

### Missing Technical Specs

| Missing Item | Impact |
|-------------|--------|
| RLS policy SQL definitions | Claude Code cannot generate secure DB without this |
| `.env.example` schema | No developer can configure the app |
| Auth method (Email/Password vs Magic Link vs Google OAuth) | Blocks auth implementation |
| Cron infrastructure choice (Vercel Cron vs Cloud Scheduler vs pg_cron) | Blocks all cron jobs |
| BigQuery sync strategy (full overwrite vs incremental upsert) | Affects 165K row table performance |
| AMBER threshold formula | Blocks entire alert system |
| Zero output format for shadow mode | Blocks GAP analysis implementation |

### Minimum `.env.example` Required
```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
ANTHROPIC_API_KEY=
XERO_CLIENT_ID=
XERO_CLIENT_SECRET=
GCP_PROJECT_ID=instant-contact-479316-i4
GCP_SERVICE_ACCOUNT_BASE64=
SLACK_WEBHOOK_PROCUREMENT=
SLACK_WEBHOOK_LOGISTICS_UK=
SLACK_WEBHOOK_LOGISTICS_FL=
SLACK_WEBHOOK_LOGISTICS_PH=
SLACK_WEBHOOK_OPS_CRITICAL=
SENDGRID_API_KEY=
SHADOW_MODE=false
```

### Missing Integration Specs

| Integration | What's Missing |
|-------------|---------------|
| Xero API | Target endpoints, OAuth refresh token flow, SKU → Xero ItemCode mapping |
| Google Vision OCR | Supported MIME types, fallback if unreadable, confidence threshold |
| BigQuery | Exact SQL query text, authentication method (Workload Identity vs Service Account JSON) |
| Slack | Incoming Webhooks vs Slack App with Block Kit (affects all payload structures) |
| Carrier APIs | Specific carriers confirmed, tracking webhook vs polling |

### Error Handling Matrix (Happy Path Only — PRD Gaps)

| Failure | Current PRD | Required Behaviour |
|---------|------------|-------------------|
| BigQuery sync fails | Not covered | Alert `#ops-critical`, preserve yesterday's data, show stale banner |
| Xero post fails | Not covered | Set `xero_sync_failed` status, "Retry Sync" button, log error to `sync_logs` |
| Corrupt invoice upload | Not covered | Synchronous error to China ops, block submission |
| Claude <70% confidence on large adjustment | Not covered | Route to Manual Review queue, highlight low-confidence fields in red |
| Supplier delay (ETA exceeded) | Not covered | Auto-alert procurement Slack, flag PO row in red |

### Recommended Day 1 Build Sequence

If Claude Code starts tomorrow, this is the exact file order that unblocks everything downstream:

1. `supabase/migrations/00001_init.sql` — Schema, enums, RLS policies
2. `types/database.types.ts` — TypeScript interfaces from schema (type safety across full stack)
3. `lib/inventory/allocation.ts` — Pure-function math engine for zone allocation and velocity (unit-testable with no UI dependency)
4. `lib/supabase/server.ts` + `client.ts` — DB and auth connection utilities
5. `app/api/cron/sync-bigquery/route.ts` — Data ingestion pipeline (gets real data flowing)

---

## 7. Consolidated Action Plan

### 🔴 P0 — Go-Live Blockers (fix before any production deployment)

| # | Item | Owner | Effort |
|---|------|-------|--------|
| P0-1 | Define PO approval financial thresholds | Cem (CEO) | 30 min decision |
| P0-2 | Add 4-eyes gate: invoice upload → manager approval → Xero | Architect | 2 days |
| P0-3 | BigQuery sync monitoring + stale data banner in UI | Dev | 1 day |
| P0-4 | Shadow mode environment isolation (`SHADOW_MODE` flag) | Dev | 0.5 days |
| P0-5 | Fix PH zone formula (`||` → `NULLIF`) | Dev | 1 hour |

### 🟠 P1 — High Priority (address before build starts)

| # | Item | Owner | Effort |
|---|------|-------|--------|
| P1-1 | Add `suppliers` master table to schema | Architect | 1 day |
| P1-2 | Add `warehouses` lookup table (resolve FL/Florida) | Architect | 1 day |
| P1-3 | Add `audit_log` table | Dev | 0.5 days |
| P1-4 | Cron DAG orchestration (dependency management between jobs) | Dev | 2 days |
| P1-5 | Define AMBER alert threshold formula (suggest: <35 days cover) | Cem + Dev | 30 min |
| P1-6 | Add cumulative auto-approval caps (daily 50u / weekly 200u per warehouse) | Dev | 1 day |
| P1-7 | Add partial indexes for DISC filter | Dev | 2 hours |
| P1-8 | Write RLS policy SQL definitions for all roles | Dev | 1 day |
| P1-9 | Create `.env.example` with all required variables | Dev | 1 hour |
| P1-10 | Implement stock state machine (`ON_HAND` / `IN_TRANSIT_SUPPLIER` / `IN_TRANSIT_INTERNAL`) | Architect | 1 day |

### 🟡 P2 — Medium Priority (address in Phase 1 build)

| # | Item | Owner | Effort |
|---|------|-------|--------|
| P2-1 | Add downtrend velocity flag (alert before reorder on declining SKUs) | Dev | 1 day |
| P2-2 | PH scarcity priority queue for transfer conflicts | Dev | 1 day |
| P2-3 | Separate FBA safety stock tier (30d) from general PH safety (14d) | Cem decision + Dev | 0.5 days |
| P2-4 | HB401 `priority_multiplier` column in products table | Dev | 0.5 days |
| P2-5 | Add `lead_time_days` to suppliers table | Dev | 0.5 days |
| P2-6 | Document Zero's export format for shadow mode GAP analysis | Chris/Cem | 1 hour |
| P2-7 | Xero multi-entity routing logic (UK vs US entity determination) | Architect | 1 day |
| P2-8 | Currency column on all Xero-bound financial tables | Dev | 0.5 days |
| P2-9 | China portal file injection mitigations (OCR sanitisation, whitelist) | Dev | 1 day |
| P2-10 | Auto stock receipt → `PENDING_RECEIPT` state (24hr physical confirmation window) | Dev | 1 day |

### 🟢 P3 — Low Priority (can defer to Phase 2)

| # | Item | Owner | Effort |
|---|------|-------|--------|
| P3-1 | Increase best-seller cover days from 45 to 56 | Cem decision | 30 min |
| P3-2 | Authentication method decision (Email/Password vs Magic Link vs Google OAuth) | Cem/Dev | 30 min |
| P3-3 | Cron infrastructure decision (Vercel vs Cloud Scheduler vs pg_cron) | Dev | 30 min |
| P3-4 | BigQuery sync strategy decision (full overwrite vs incremental upsert) | Dev | 30 min |
| P3-5 | Slack channel privacy audit (ensure all logistics channels are private) | Cem | 1 hour |

---

## 8. What's Working Well

The PRD is genuinely strong in these areas — preserve them:

| Strength | Why It Matters |
|----------|---------------|
| **Two-Process Architecture** | Correctly separates internal transfers (weekly, days) from supplier orders (bi-weekly, 14-21 days). No prior spec captured both. Single biggest improvement over v2.6. |
| **Zone Model with Proportional PH Allocation** | Mathematically sound. Handles PH serving both US and UK zones correctly. Same formula drives both stock assessment and shipping plan. |
| **Tiered Velocity** | MAX(7d,30d) for best sellers solves the spike-inflation problem that was causing 126% over-ordering. Correct fix. |
| **Data Source Clarity** | Documents that `orders` table is 30% complete. Prohibits its use for velocity. Prevents the most dangerous silent error. |
| **3-Layer Agentic Architecture** | "AI recommends, human decides" is the right posture for a business continuity system. Each layer independently testable and fixable. |
| **Shadow Mode Strategy** | Running parallel with Zero before cutover is exactly right for a $4,750/day revenue-at-risk system. |
| **Workflow Diagrams** | All 3 workflows clearly mapped. China portal, internal transfers, and supplier ordering are unambiguous. |
| **Agent Review Appendix** | Meta-review of prior agents (Codex A, Ava A-, Harry B+, Hermes C+) shows iterative improvement and intellectual honesty. |

---

## 9. Council Verdict

The MASTER_PRD v1.0 is the best spec this project has seen. It correctly identifies the two-process procurement architecture, fixes the velocity inflation bug, documents the data source hierarchy, and maps all workflows. Athena's data integrity audit saved the build from being constructed on broken foundations.

However, **it is not build-ready today** due to 5 go-live blockers and 10 high-priority gaps that would require rework mid-build if not addressed first.

**Recommended path:**
1. Spend 2–3 hours resolving the P0 decisions (PO thresholds, AMBER formula, auth method, cron infrastructure) — these are Cem decisions, not dev work.
2. Dev spends 1 day on P0 technical fixes (NULLIF bug, shadow mode flag, sync monitoring).
3. Architect spends 2 days adding missing tables and RLS policies to the schema.
4. Hand updated PRD + schema to Claude Code → build begins.

**Estimated delay to fix blockers before build: 3 working days.**
**Cost of NOT fixing them: mid-build rework estimated at 1–2 additional weeks.**

---

*Generated by LLM Council | 13 April 2026*
*Council: Claude Opus (Architecture & Risk) | GPT-5.4 (Business Logic) | Gemini Pro (Build Readiness)*
*PRD Version: 1.0 | Compiled by: Athena (Chief of Staff)*
*Classification: Internal — Ecell Global*
