# Inventory Ordering App — Master PRD
**Version:** 2.0 | **Date:** 2026-04-13 (Council Fixes Applied)
**Compiled by:** Athena (Chief of Staff)
**Sources:** Harry's PROJECT.md v2.6 + Ava's Strategic Review + Codex's Adversarial Review + Athena's Data Integrity Audit + Cem's Live Directives + LLM Council Reviews (×2)
**Builder:** Claude Code CLI (GSD + Agent Teams) | **Build Approach:** Shadow Mode (confirmed)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Context](#2-business-context)
3. [Data Integrity Findings & Fixes](#3-data-integrity-findings--fixes)
4. [Architecture](#4-architecture)
5. [Two Procurement Processes](#5-two-procurement-processes)
6. [Supply Zone Model](#6-supply-zone-model)
7. [Velocity & Best Sellers Logic](#7-velocity--best-sellers-logic)
8. [Allocation & Shipping Plan](#8-allocation--shipping-plan)
9. [Data Model](#9-data-model)
10. [User Roles & Permissions](#10-user-roles--permissions)
11. [Workflows](#11-workflows)
12. [UI/UX Requirements](#12-uiux-requirements)
13. [Notification System](#13-notification-system)
14. [Implementation Phases](#14-implementation-phases)
15. [Open Questions](#15-open-questions)
16. [Appendix: Agent Reviews](#16-appendix-agent-reviews)
17. [Concurrent Run Protection](#17-concurrent-run-protection-council-fix-8)
18. [Environment Configuration](#18-environment-configuration-cems-council--build-readiness)
19. [Shadow Mode Metrics](#19-shadow-mode-metrics-council--cutover-criteria)
20. [Appendix: Council Fixes Applied](#20-appendix-council-fixes-applied-v20)

---

## 1. Executive Summary

### What
End-to-end procurement and inventory management system replacing manual Excel/email workflows. Covers stock monitoring, reorder automation, China supplier ordering, internal stock transfers, shipment tracking, and finance integration.

### Why
- **Stock-outs = lost sales.** 95 items currently stocked out with active demand (all PH warehouse). Top item losing ~$230/day.
- **Manual process = Cem as bottleneck.** China procurement currently runs through Cem via email. System removes him from the loop.
- **No early warning.** Current alerts jump GREEN → RED. No AMBER threshold. No trending detection.
- **Overordering slow sellers.** Velocity calculation uses 7-day window only — inflates reorder quantities during spikes.

### Key Innovation (from this review)
Two distinct procurement processes identified — no prior spec captured both:

| Process | What | Speed | Frequency | When |
|---------|------|-------|-----------|------|
| **Process 1: Internal Stock Transfers** | PH → FL, PH → UK | Days | **Weekly** | PH has surplus, other site is short |
| **Process 2: Supplier Ordering** | CN → FL / UK / PH | 14-21 days lead time | **Bi-weekly** | Replenishment from China |

### ⚠️ Business Continuity Classification

**This is a business continuity task** (Cem, Apr 13). Must be done correctly with correct data. Stock-outs = lost sales = revenue impact. No shortcuts on data integrity. Data integrity verification runs in parallel with build.

### Agentic Architecture — Three Layers (Cem: "no mistakes, easy way to fix issues")

```
LAYER 1: DATA (Staging Tables + Crons)
  ┌─────────────────────────────────┐
  │ best_sellers_daily              │
  │ reorder_queue (view)            │  Pure SQL. Deterministic.
  │ zone_stock_summary (view)       │  If wrong → fix SQL, re-run.
  │ Cron: daily 06:30 UTC           │
  └──────────────┬──────────────────┘
                 ↓
LAYER 2: INTELLIGENCE (Procurement Agent)
  ┌─────────────────────────────────┐
  │ Reads staging tables            │
  │ Applies PRD rules               │  Claude API. Advisory only.
  │ Validates recommendations       │  If wrong → override in portal.
  │ Flags anomalies                 │  Agent learns from corrections.
  │ Runs AFTER cron, BEFORE portal  │  Cost: ~$0.02/run
  └──────────────┬──────────────────┘
                 ↓
LAYER 3: PORTAL (Human Review + Action)
  ┌─────────────────────────────────┐
  │ Chris/Jae see validated recs    │
  │ Confirm, adjust, or reject      │  Human is final gatekeeper.
  │ Add tracking numbers            │  No automated action without
  │ Approve transfers/POs           │  human confirmation.
  └─────────────────────────────────┘
```

**Why three layers:**
- Layer 1 breaks? Fix the SQL. Data is deterministic and auditable.
- Layer 2 wrong? Override in portal. Agent learns from corrections.
- Layer 3 catches everything. "AI recommends, human decides."
- Each layer is independently testable in shadow mode.

**Procurement agent validates:**
- Zone logic correct? (PH allocation, US/UK split)
- Transfer feasibility? (PH surplus exists?)
- Rounding applied correctly?
- Exclusion rules followed? (DISC, z-prefix, stale)
- Anomaly detection: "Reorder qty jumped 300% vs last week — verify"
- Cross-check: recommendation consistent with PRD rules?

**Tech:** Claude API with system prompt = condensed PRD rules. Runs daily after cron. Output: validated recommendation list + anomaly flags.

### Key Users

| Person | Role | Current Process | New Process |
|--------|------|----------------|-------------|
| **Chris Yunnun** | Warehouse Manager (PH) | Triggers orders in legacy Zero system | Reviews suggested transfers in portal, confirms with tracking # |
| **Jae Vitug** | PH Operations | Sends packing list emails manually | Uses portal to confirm transfers, attach packing lists |
| **Ben** | China Office | Receives PO via email | Downloads POs from China portal by supplier |
| **Cem** | CEO | Bottleneck — in the loop on all China orders | Removed from loop — system auto-generates, managers approve |

### Scale
- 41,479 items in `blank_inventory` across 4 warehouses (UK, Florida, PH, Transit)
- ~9,051 active items (78% are DISC/discontinued — filtered from all logic)
- 336,118 orders in Supabase (partial sync — BigQuery is canonical)
- 3 suppliers (ECELLSZ, XINTAI, others)
- 4 currencies (GBP, USD, CNY, EUR)

---

## 2. Business Context

### North Star
"#1 licensed tech accessories company — any fan's favourite brand on any device, everywhere they shop, faster than anyone."

### 3 Metrics This App Serves
| Metric | How |
|--------|-----|
| **Coverage** | Ensure stock availability so every listing stays active |
| **Speed** | Reduce procurement cycle time via automation |
| **Intelligence** | Velocity-based reordering replaces gut feel |

### Revenue Impact
- $5.5-6M annual revenue
- Stock-out on a top-50 item = ~$100-230/day lost revenue
- 95 current stock-outs × average ~$50/day = **~$4,750/day revenue at risk**
- HB401 converts 4x vs HTPCR — stock-outs on HB401 are disproportionately costly

### Sites & Roles

| Site | Code | Role | Staff |
|------|------|------|-------|
| **UK** | UK | Fulfillment hub for UK + ROW | Warehouse team |
| **Florida** | Florida/FL | US fulfillment hub | Warehouse team |
| **Philippines** | PH | Production + overflow + FBA + Saturday | 38 PH staff |
| **China** | CN | Sourcing, procurement, supplier management | Ben + team |
| **Transit** | TRANSIT | In-transit inventory tracking | System only |

---

## 3. Data Integrity Findings & Fixes

**Audit date:** 2026-04-13 | **Auditor:** Athena (live Supabase queries)

### CRITICAL — Must Fix in Build

| # | Finding | Impact | Fix |
|---|---------|--------|-----|
| **C1** | `avg_daily_sales` = `sales_last_7d / 7` only (20/20 confirmed) | Over-orders up to 126% during weekly spikes | Tiered velocity: best sellers use MAX(7d, 30d); standard items use 30d only |
| **C2** | Supabase `orders` table is ~30% of actual orders (83 vs 277 for top item) | Any velocity calc from orders table under-counts by 70% | **Use `blank_inventory` columns for velocity. NEVER calculate from `orders` table.** |
| **C3** | "Florida" (10,337) vs "FL" (99) warehouse code duplication | Distribution logic silently drops items | Normalise: FL = packaging/materials only. Florida = blank inventory. Map in app layer. |

### HIGH — Address in Build

| # | Finding | Detail |
|---|---------|--------|
| H1 | 98% of items have zero reorder level | Only 749/41,479 have `reorder_level > 0`. Calculate dynamically. |
| H2 | 78% of inventory is DISC | 32,428 items. Filter `product_group != 'DISC'` everywhere. |
| H3 | 95 active stock-outs (all PH) | Top: HTPCR-S931X at 23 units/day, zero stock. |
| H4 | 1,054 dead stock items | >100 units, zero 30d sales. Write-off candidates. |
| H5 | Zero AMBER alerts | GREEN (41,204) → RED (217). No early warning. Add AMBER threshold. |

### Confirmed Working

| Check | Status |
|-------|--------|
| `blank_inventory` snapshot date | ✅ Today (2026-04-13) |
| Orders freshness | ✅ paid_date to Apr 12, synced today 06:00 UTC |
| Reorder formula consistency (where set) | ✅ `avg_daily × 56` uniformly (now corrected to 30d normal / 45d best sellers) |
| No negative stock values | ✅ |
| Per-warehouse tracking | ✅ Each item tracked across UK/PH/Florida/Transit |

### Data Pipeline (Canonical)

```
AWS MySQL (source of truth — all orders)
    ↓ Datastream (real-time replication)
BigQuery zero_dataset
    ↓ Sync Job (every 2 hours)
Supabase blank_inventory    ← USE THIS for velocity & stock
    └── sales_last_7d, sales_last_30d, avg_daily_sales (BigQuery-sourced)

Supabase orders table       ← INCOMPLETE (~30% of actual orders)
    └── DO NOT use for velocity calculations
```

### ⚠️ Zero System Fragility — Business Continuity Risk (Cem, Apr 13)

**Context:** Zero is a 2-decade-old PHP system running on Windows 2007 hardware. The PHP code feeds BigQuery via AWS MySQL Datastream. If Zero fails, the entire data pipeline above breaks — no fresh inventory data, no velocity calculations, no reorder recommendations.

**Current dependencies on Zero:**
1. Order ingestion from Amazon (via API middleware — exists)
2. Order ingestion from eBay (API middleware — **NOT YET BUILT**)
3. Inventory/stock data → AWS MySQL → BigQuery → Supabase
4. Sales velocity calculations (derived from order data)

**Architectural requirement:** This app MUST be built so that if Zero dies:
- The app can detect the failure (order freshness monitoring — see below)
- A bypass route exists: marketplace APIs → Supabase directly (Amazon middleware exists, eBay needs adding)
- The app degrades gracefully with stale data rather than producing silently wrong recommendations

**Ties to:** Business Blueprint 3.0 (offline discussion with Cem). Strategic question: retain AWS MySQL + find new data path, or replace entirely with direct-to-Supabase? Decision pending.

### Order Freshness Monitoring (Cem, Apr 13 — "very important")

**Requirement:** AI-managed monitoring layer that detects when orders stop flowing from ANY channel.

| Channel | Expected Cadence | Alert If |
|---------|-----------------|----------|
| Amazon US | Orders every few minutes | No new orders > 2 hours during business hours |
| Amazon UK | Orders every few minutes | No new orders > 2 hours during business hours |
| eBay | Orders throughout day | No new orders > 4 hours during business hours |
| Walmart | Orders throughout day | No new orders > 6 hours |
| GoHeadCase | Sporadic | No new orders > 24 hours (lower volume) |

**Implementation:**
```sql
-- Add to system_health table
INSERT INTO system_health (component, last_run_at, last_status, snapshot_date)
VALUES ('order_flow_amazon_us', NOW(), 'HEALTHY', CURRENT_DATE);

-- Cron every 30 min: check last order timestamp per channel
-- If gap exceeds threshold → Slack #ops-critical alert
-- "Amazon US orders stopped flowing at 14:32 UTC — last order was 2h17m ago"
```

**Why this matters:** If a marketplace API changes (e.g., Walmart auth token expires), orders silently stop importing. Without monitoring, stock calculations use stale data → wrong reorder decisions → stock-outs. This is the same class of silent failure as the BigQuery sync issue (Council Fix #6).

### FBA Restock — Out of Scope (Cem, Apr 13)

**Decision:** FBA restocking is handled by a **separate existing app** (already on GitHub). This inventory ordering app does NOT manage FBA stock levels.

**Interface point:** Top 30 best sellers should always have plentiful stock. The 6-day FBA restock cycle draws from PH warehouse stock. This app ensures PH has enough stock for both FBA pulls and direct fulfillment — which is why PH safety stock was raised to 21 days (Council Fix CX-5).

**FBA impact on this app:** PH velocity includes FBA-bound orders. The velocity calculations already capture this demand. No separate FBA logic needed here.

---

## 4. Architecture

### Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16 + TypeScript + Tailwind |
| Backend | Next.js API Routes |
| Database | Supabase (PostgreSQL) — project `auzjmawughepxbtpwuhe` |
| Auth | Supabase Auth |
| Storage | Supabase Storage (invoices, packing lists, CSV/PDF exports) |
| Notifications | Slack Webhooks + Email (SendGrid) |
| OCR | Google Vision API (invoices) |
| Finance | Xero API via Finance Agent |
| LLM | Claude API (stock adjustment validation) |
| Deployment | Cloud Run via ecell.app |

### Design System (ecell.app)

| Property | Value |
|----------|-------|
| Background | `bg-[#FAFBFC]` light theme |
| Brand blue | `#0047AB` |
| Fonts | Geist Sans / Geist Mono |
| Cards | `rounded-2xl border border-zinc-200 shadow-sm` |
| Framework | Next.js 16 + Tailwind CSS |

### App Architecture

```
ecell.app (Portal/Dashboard)
      │
      ├─── /inventory     → Inventory Ordering App (this project)
      ├─── /fulfillment   → Fulfillment Portal
      ├─── /listings      → Listings Tracker
      └─── /licenses      → License Manager
```

### External Integrations

| Service | Purpose |
|---------|---------|
| BigQuery | `zero_dataset.inventory` — canonical stock data |
| Slack | Notifications to UK/FL/PH teams |
| Xero | Supplier invoice posting (UK + US entities) |
| Carrier APIs | DHL, FedEx, UPS tracking |

---

## 5. Two Procurement Processes

*Confirmed by Cem, Apr 13 — "we have 2 processes, it's good you called this out."*

### Process 1: Internal Stock Transfers

**Purpose:** Fast response to zone shortages using existing PH surplus.

| Route | Allowed | Lead Time | Reason |
|-------|---------|-----------|--------|
| PH → FL | ✅ | Days | Cost-effective |
| PH → UK | ✅ | Days | Cost-effective |
| UK ↔ FL | ❌ | N/A | High freight — not economical |
| CN → Any | ⚠️ | N/A | CN is staging only. Stock in CN = error flag. |

**Frequency:** Weekly — Friday/Saturday from PH (Cem confirmed Apr 13)

**Trigger:** Scheduled (every Friday) OR on-demand (stock-out alert on key product triggers immediate run).

**Current process:** Chris Yunnun (warehouse manager) triggers in legacy Zero system. Jae Vitug & Chris send packing list emails manually. This becomes agentic.

**New process:** Portal generates suggested transfer list → Chris/Jae review → Confirm with tracking number.

**Approval:** Chris Yunnun (warehouse manager, PH).

**Cost:** Zero additional freight — PH already ships finished goods to FL and UK 2-3 times per week. Raw materials (blanks) piggyback on these existing shipments.

**Output:** Suggested Transfer List in portal → Chris/Jae review → Confirm with tracking number.

**Shipping logistics:** Zero additional cost. PH ships finished goods to FL and UK 2-3 times per week. Blanks get added to these existing shipments (Friday/Saturday dispatch).

**Portal workflow:**
1. System generates suggested transfer list (items, quantities, destination)
2. Chris/Jae open portal → review suggestions
3. Confirm transfers → enter tracking number
4. PH stock deducts → shows as "in transit" to destination
5. Destination confirms receipt → stock added

**Transfer Request Fields:**

| Field | Description |
|-------|-------------|
| `item_code` | SKU to transfer |
| `from_warehouse` | Always "PH" |
| `to_warehouse` | "UK" or "FL" |
| `qty` | Transfer quantity |
| `priority` | HIGH if destination stock < 7 days |
| `status` | SUGGESTED → CONFIRMED → SHIPPED → RECEIVED |
| `tracking_number` | Added by Chris/Jae on confirmation |
| `confirmed_by` | Chris Yunnun or Jae Vitug |

**Logic:**
```typescript
function checkInternalTransfer(item: ZoneItem): TransferOrder[] | null {
  // Council Fix #9 / Codex CX-5: PH safety stock = MAX(21d, lead_time_days)
  // PH is both transfer source AND fulfillment site — 14d was too low
  const ph_safety = item.velocity_ph * 21;  // 21 days (≥ lead time)
  const ph_surplus = Math.max(0, item.stock_ph - ph_safety);
  
  if (ph_surplus === 0) return null;
  
  // Council Fix #16: Check for unconfirmed SUGGESTED transfers before generating new ones
  if (item.has_pending_suggested_transfer) return null;  // Don't duplicate
  
  const transfers: TransferOrder[] = [];
  
  // Zone US short? (Council Fix #4: deduct in-transit)
  const us_need = Math.max(0, (item.zone_us_target * 0.5) - item.stock_fl - item.in_transit_to_fl);
  if (us_need > 0) {
    const qty = Math.min(ph_surplus, us_need);
    transfers.push({ from: 'PH', to: 'FL', qty: Math.ceil(qty / 10) * 10, item: item.item_code });
  }
  
  // Zone UK short?
  const remaining = ph_surplus - (transfers[0]?.qty || 0);
  const uk_need = Math.max(0, (item.zone_uk_target * 0.5) - item.stock_uk - item.in_transit_to_uk);
  if (uk_need > 0 && remaining > 0) {
    const qty = Math.min(remaining, uk_need);
    transfers.push({ from: 'PH', to: 'UK', qty: Math.ceil(qty / 10) * 10, item: item.item_code });
  }
  
  return transfers.length > 0 ? transfers : null;
}

// Cem Council: PH scarcity priority — when multiple items compete for PH surplus
function prioritiseTransfers(transfers: TransferOrder[], items: ZoneItem[]): TransferOrder[] {
  // Priority = ascending days_of_cover at destination. Lowest cover = highest priority.
  return transfers.sort((a, b) => {
    const aDoc = items.find(i => i.item_code === a.item)?.destination_days_of_cover ?? 999;
    const bDoc = items.find(i => i.item_code === b.item)?.destination_days_of_cover ?? 999;
    return aDoc - bDoc;
  });
}
```

### Process 2: Supplier Ordering

**Purpose:** Replenishment from China when internal transfers can't cover the shortfall (or PH is also short).

**Frequency:** Bi-weekly (Cem confirmed Apr 13) — scheduled OR on-demand when stock-out alert triggers.

**Trigger:** Zone stock below threshold AND internal transfer cannot fully cover.

**Approval:** Finance/Manager (PO amount threshold).

**Output:** Purchase Order + Shipping Plan (CSV/PDF for Ben in China).

**Flow:**
```
Reorder Queue (auto-generated)
    ↓
PO Created (DRAFT)
    ↓
Manager Approves → Status: APPROVED
    ↓
China Portal downloads PO by supplier
    ↓
China creates Packing List + uploads Invoice
    ↓
China creates Shipment (tracking, carrier, ETA)
    ↓
Slack/email notification to destination warehouse
    ↓
LLM monitors delivery tracking
    ↓
Delivery confirmed → auto-add stock to destination
    ↓
Finance Agent posts invoice to Xero
```

### Operating Cadence

```
DAILY — DAG Pipeline (Council P1-4: dependency chain, not independent crons):
  06:00 UTC → BigQuery sync → writes to system_health on completion
  06:30 UTC → GATE: check system_health.snapshot_date = TODAY (Fix #6)
           → IF stale: ABORT + Slack #ops-critical alert + UI stale banner
           → IF fresh: Run best_sellers_daily staging table refresh
  07:00 UTC → Reorder calculation (reads best_sellers_daily)
           → Stock-out alerts generated for CRITICAL/BLACK items
           → PH stock-out check: if PH free_stocks=0 + sales_7d>0 → HIGH-priority supplier order (Fix #9)
           → If stock-out on key product → trigger on-demand transfer/order report
  Each step writes start/end to operational_events (Fix #20)

WEEKLY (Friday):
  → Run zone stock assessment
  → Generate suggested Internal Transfer list for Chris/Jae
  → Chris/Jae review in portal → Confirm → Add tracking #
  → PH ships blanks with existing Fri/Sat finished goods shipment to FL/UK
  → On-demand: stock-out alert can trigger this any day of the week

BI-WEEKLY (alternating Fridays):
  → Run full reorder calculation
  → Generate PO drafts with shipping plans (CSV/PDF for Ben)
  → Route to manager approval queue
  → Approved POs visible in China portal
  → On-demand: stock-out alert can trigger this any day
```

### Decision Sequence

```
Zone stock check (weekly)
      ↓
  Below threshold?
      ↓ YES
  Can PH internal transfer cover it?
      ├── YES → Process 1: Internal Stock Transfer (weekly, days to fulfil)
      ├── PARTIAL → Process 1 now + queue remainder for bi-weekly supplier order
      └── NO (PH also short) → Queue for Process 2: Supplier Ordering (bi-weekly, 14-21 day lead)
```

**Why this cadence works:** Internal transfers (weekly) are the fast response — move existing stock where it's needed. Supplier orders (bi-weekly) are the strategic replenishment — batch orders for better pricing and shipping efficiency from China. The weekly check ensures no stock-out goes unaddressed for more than 7 days.

---

## 6. Supply Zone Model

*UK↔US transfer is blocked (high freight). Stock is only useful within connected warehouses.*

### Zones

| Zone | Warehouses | What It Means |
|------|-----------|---------------|
| **Zone US** | Florida + PH (US share) | PH handles US overflow, FBA, Saturday |
| **Zone UK** | UK + PH (UK share) | PH handles UK overflow |

**PH is shared** between both zones — allocated proportionally.

### PH Allocation Formula

```
-- Guard: if both FL and UK velocity are zero, default 60/40 split (Council Fix #1)
IF FL_velocity = 0 AND UK_velocity = 0:
  PH_US_share% = 0.60
  PH_UK_share% = 0.40
ELSE:
  PH_US_share% = FL_velocity / NULLIF(FL_velocity + UK_velocity, 0)
  PH_UK_share% = UK_velocity / NULLIF(FL_velocity + UK_velocity, 0)

-- COALESCE all stock reads to 0 (Council Fix #2 — NULL + number = NULL in SQL)
Zone_US_stock = COALESCE(FL_stock, 0) + (COALESCE(PH_stock, 0) × PH_US_share%)
Zone_UK_stock = COALESCE(UK_stock, 0) + (COALESCE(PH_stock, 0) × PH_UK_share%)

-- Deduct in-transit stock from zone need (Council Fix #4)
Zone_US_need = MAX(0, Zone_US_target - Zone_US_stock - in_transit_to_US)
Zone_UK_need = MAX(0, Zone_UK_target - Zone_UK_stock - in_transit_to_UK)

-- For supplier ordering: use effective PH stock (Council Fix #3)
effective_ph_stock = free_stocks - pending_transfers_out
```

**⚠️ SQL Bug Fix (Cem's Council):** PostgreSQL `||` is string concatenation, NOT "or". Use `NULLIF(x, 0)` for division-by-zero protection, not `(x || 1)`.

*Decision (Cem, Apr 13): Proportional allocation is Phase 1 — same math drives the China shipping plan. Not deferrable.*

### Warehouse Map (Live Data)

| Warehouse | Items | Active (non-DISC) | Role |
|-----------|-------|-------------------|------|
| UK | 10,369 | 361 | UK + ROW fulfillment |
| PH | 10,337 | 325 | US overflow + FBA + Saturday + UK overflow |
| Florida | 10,337 | 251 | US primary fulfillment |
| Transit | 10,337 | — | In-flight stock (not orderable) |
| FL | 99 | 63 | Packaging/materials only |

**Transit stock:** Counts as "on order" in zone calculations — not available stock.

---

## 7. Velocity & Best Sellers Logic

### Tiered Velocity (Cem's directive, Apr 13)

| Tier | Items | Velocity Formula | Reorder Level | Rationale |
|------|-------|-----------------|---------------|-----------|
| **Best Sellers** | Top 50 global + top 50 per zone (~80-120 unique) | `MAX(7d/7, 30d/30)` | velocity × **45 days** | Never stock out — higher velocity + more cover |
| **Active** | All items with 30d sales > 0 | `30d/30` only | velocity × **30 days** | Stable ordering, no over-stock |
| **Stale** | No sales in 30 days AND free_stocks > 0 AND in_transit = 0 | No reorder | N/A | Exclude from reorder queue. **Zero-stock items are NOT stale** — they may be demand-suppressed stock-outs (Council Fix #5). |
| **Retire Candidate** | Sales < 5/week AND stock created 2024 or earlier | No reorder | N/A | Flag for review (subjective — human decides) |
| **DISC** | Discontinued group | No reorder | N/A | Excluded from everything |

**Lead time context:** China → destination = 14-21 days. So:
- Normal items: 30d cover = 9-16 day safety buffer after lead time
- Best sellers: 45d cover = 24-31 day safety buffer (extra protection against spikes)

### Best Sellers Daily Staging Table

**Cron:** Daily at 06:30 UTC (after `blank_inventory` sync)

**Table: `best_sellers_daily`**

```sql
CREATE TABLE best_sellers_daily (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_code       TEXT NOT NULL,
    warehouse       TEXT NOT NULL,
    rank            INT NOT NULL,
    velocity_7d     NUMERIC(10,2),
    velocity_30d    NUMERIC(10,2),
    velocity_used   NUMERIC(10,2),          -- MAX(7d, 30d) for best sellers
    sales_last_7d   INT,
    sales_last_30d  INT,
    free_stocks     INT,
    days_of_cover   NUMERIC(10,1),
    stock_risk      TEXT,                   -- CRITICAL / LOW / OK
    reorder_qty     INT,
    snapshot_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(item_code, warehouse, snapshot_date)
);
```

**Best Seller Lists (Union):**
1. **Top 50 Global** — by total velocity across all warehouses
2. **Top 50 Zone US** — by FL + PH velocity
3. **Top 50 Zone UK** — by UK velocity

Union of all three = ~80-120 unique items. All get `MAX(7d, 30d)` treatment.

**Consumers:**

| System | Usage |
|--------|-------|
| Procurement App | Lookup: best seller? → 7d velocity. Otherwise → 30d. |
| PULSE Dashboard | Top sellers widget |
| Stock-out Alerts | `WHERE stock_risk = 'CRITICAL'` |
| Reorder Queue | Pre-calculated `reorder_qty` |

### Velocity TypeScript

```typescript
function getVelocity(item: InventoryItem, bestSellers: Set<string>): number {
  // Council Fix #2: COALESCE nulls to 0
  const v7d = Math.max(0, (item.sales_last_7d ?? 0) / 7);
  const v30d = Math.max(0, (item.sales_last_30d ?? 0) / 30);
  
  if (bestSellers.has(item.item_code)) {
    return Math.max(v7d, v30d);  // Best sellers: always use higher
  }
  return v30d;  // Standard: 30d only
}

// Cem Council Fix: Downtrend flag — alert before reordering into declining trend
function checkDowntrend(item: InventoryItem): { isDowntrend: boolean; ratio: number } {
  const v7d = (item.sales_last_7d ?? 0) / 7;
  const v30d = (item.sales_last_30d ?? 0) / 30;
  if (v30d === 0) return { isDowntrend: false, ratio: 0 };
  const ratio = v7d / v30d;
  return { isDowntrend: ratio < 0.6, ratio };  // 7d < 60% of 30d = declining
}

function getReorderQty(
  velocity: number, 
  currentStock: number, 
  inTransit: number,           // Council Fix #4: deduct in-transit
  isBestSeller: boolean,
  priorityMultiplier: number = 1.0  // Cem Council: HB401 = 1.5x
): number {
  const baseCoverDays = isBestSeller ? 45 : 30;
  const coverDays = Math.round(baseCoverDays * priorityMultiplier);
  const target = velocity * coverDays;
  const need = target - currentStock - inTransit;  // Council Fix #4
  if (need < 1.0) return 0;  // Council Fix #24: minimum threshold
  const base = need >= 1000 ? 100 : 10;
  return Math.ceil(need / base) * base;
}
```

**Priority Multiplier (Cem's Council):** HB401 converts 4x vs HTPCR — stock-outs cost 4x more. Apply `priority_multiplier = 1.5` for HB401 (67-day cover for best sellers). Stored in `product_group_config` table, admin-editable.

---

## 8. Allocation & Shipping Plan

The same proportional math determines zone stock AND tells China where to ship.

### Full Calculation Flow

```typescript
function calculateAllocation(item: {
  item_code: string;
  velocity_fl: number;
  velocity_uk: number;
  velocity_ph: number;
  stock_fl: number;
  stock_uk: number;
  stock_ph: number;
  in_transit_us: number;       // Council Fix #4: in-transit to US zone
  in_transit_uk: number;       // Council Fix #4: in-transit to UK zone
  pending_transfers_out: number; // Council Fix #3: PH transfers already committed
  is_best_seller: boolean;
  priority_multiplier: number; // Cem Council: HB401=1.5, default=1.0
}, config: ProductGroupConfig): ZoneAllocation {
  const baseCoverDays = item.is_best_seller ? 45 : 30;
  const coverDays = Math.round(baseCoverDays * item.priority_multiplier);

  const v_fl = Math.max(0, item.velocity_fl ?? 0);  // Council Fix #2/#14: null/negative guard
  const v_uk = Math.max(0, item.velocity_uk ?? 0);
  const v_ph = Math.max(0, item.velocity_ph ?? 0);
  const v_total = v_fl + v_uk + v_ph;
  
  if (v_total === 0) return zeroAllocation(item.item_code);

  // Council Fix #1: div-by-zero guard — default 60/40 when both FL+UK are zero
  let ph_us_ratio: number, ph_uk_ratio: number;
  if (v_fl + v_uk === 0) {
    ph_us_ratio = 0.60;
    ph_uk_ratio = 0.40;
  } else {
    ph_us_ratio = v_fl / (v_fl + v_uk);
    ph_uk_ratio = v_uk / (v_fl + v_uk);
  }

  // Council Fix #3: use effective PH stock (minus pending transfers out)
  const effective_ph_stock = Math.max(0, (item.stock_ph ?? 0) - item.pending_transfers_out);

  // Zone stock (Council Fix #2: COALESCE nulls)
  const zone_us_stock = (item.stock_fl ?? 0) + (effective_ph_stock * ph_us_ratio);
  const zone_uk_stock = (item.stock_uk ?? 0) + (effective_ph_stock * ph_uk_ratio);

  // Zone target
  const zone_us_velocity = v_fl + (v_ph * ph_us_ratio);
  const zone_uk_velocity = v_uk + (v_ph * ph_uk_ratio);
  const zone_us_target = zone_us_velocity * coverDays;
  const zone_uk_target = zone_uk_velocity * coverDays;

  // Zone need (Council Fix #4: deduct in-transit)
  const zone_us_need = Math.max(0, zone_us_target - zone_us_stock - (item.in_transit_us ?? 0));
  const zone_uk_need = Math.max(0, zone_uk_target - zone_uk_stock - (item.in_transit_uk ?? 0));
  const total_need = zone_us_need + zone_uk_need;

  if (total_need < 1.0) return zeroAllocation(item.item_code);  // Council Fix #24: min threshold

  // Round
  const base = total_need >= 1000 ? 100 : 10;
  const total_rounded = Math.ceil(total_need / base) * base;

  // Distribute by zone need
  const us_share = Math.round(total_rounded * (zone_us_need / total_need));
  const uk_share = total_rounded - us_share;

  // Within US zone: FL + PH split (Council Fix #12: from config table, not hardcoded)
  const fl_ratio = config.fl_ratio;  // default 0.60, admin-editable
  const ship_to_fl = Math.max(0, Math.round(us_share * fl_ratio / 10) * 10);  // Fix #7: no negatives
  const us_to_ph = Math.max(0, us_share - ship_to_fl);

  // Within UK zone: UK + PH split (from config table)
  const uk_ratio = config.uk_ratio;  // default 0.75, admin-editable
  const ship_to_uk = Math.max(0, Math.round(uk_share * uk_ratio / 10) * 10);
  const uk_to_ph = Math.max(0, uk_share - ship_to_uk);

  // PH receives from both zones
  const ship_to_ph = us_to_ph + uk_to_ph;

  // Council Fix #7: assert allocations sum correctly
  console.assert(ship_to_fl + ship_to_uk + ship_to_ph === total_rounded,
    `Allocation mismatch: ${ship_to_fl}+${ship_to_uk}+${ship_to_ph} != ${total_rounded}`);

  return { item_code: item.item_code, total_reorder_qty: total_rounded, ship_to_fl, ship_to_uk, ship_to_ph };
}
```

### Default Distribution Ratios (Configurable per Product Group)

| Product Group | US Zone: FL/PH | UK Zone: UK/PH |
|---------------|---------------|----------------|
| HTPCR, HC, HB401, H89, HDMWH | 60% / 40% | 75% / 25% |
| HLBWH | 20% / 80% | 75% / 25% |
| Default | 60% / 40% | 75% / 25% |

### Shipping Plan Output (CSV for Ben)

```csv
Item_Code,Description,Total_Qty,FL_Qty,UK_Qty,PH_Qty,Supplier,Currency
HTPCR-IPH15,TPU iPhone 15,1920,690,500,730,XINTAI,USD
HLBWH-IPH15,Leather Wallet iPhone 15,500,40,100,360,ECELLSZ,USD
```

PDF version also generated. Both attach to PO for China download.

---

## 9. Data Model

### 9.1 Core Tables

#### `inventory_snapshots` (enhanced from `blank_inventory`)

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `item_code` | text | SKU |
| `description` | text | Product description |
| `warehouse` | text | UK, Florida, PH, CN, TRANSIT |
| `product_group` | text | Category |
| `supplier` | text | Primary supplier |
| `free_stocks` | int | Available stock |
| `on_order` | int | Quantity on order |
| `in_transit` | int | Quantity in transit |
| `sales_last_7d` | int | 7-day sales (from BigQuery) |
| `sales_last_30d` | int | 30-day sales (from BigQuery) |
| `daily_velocity_7d` | decimal | sales_last_7d / 7 |
| `daily_velocity_30d` | decimal | sales_last_30d / 30 |
| `velocity_used` | decimal | Tiered: MAX(7d,30d) for best sellers, 30d for others |
| `days_of_cover` | decimal | free_stocks / velocity_used |
| `alert_level` | text | BLACK, RED, AMBER, GREEN |
| `is_best_seller` | boolean | From best_sellers_daily lookup |
| `is_excluded` | boolean | Z-prefix or stale stock |
| `exclusion_reason` | text | z_prefix, stale_stock, dead_stock, disc |
| `snapshot_date` | date | Data freshness |

#### `best_sellers_daily`
*(See Section 7 for full schema)*

#### `purchase_orders`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `po_number` | text | PO-YYYYMMDD-XXX |
| `supplier` | text | Supplier name |
| `warehouse` | text | Destination (FL, UK, PH, or MULTI) |
| `status` | text | DRAFT → PENDING_APPROVAL → APPROVED → SENT → PARTIAL → RECEIVED → CANCELLED |
| `currency` | text | GBP, USD, CNY |
| `total_amount` | decimal | PO total |
| `distribution_json` | jsonb | {FL: qty, UK: qty, PH: qty} |
| `shipping_plan_generated` | boolean | Order sheet created |
| `order_sheet_url` | text | CSV/PDF URL |
| `rounding_base` | int | 10 or 100 |
| `created_by` | uuid | User |
| `approved_by` | uuid | Approver |
| `created_at` | timestamptz | Creation time |
| `approved_at` | timestamptz | Approval time |
| `sent_to_supplier_at` | timestamptz | When China saw it |
| `expected_delivery` | date | Estimated delivery |

#### `po_lines`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `po_id` | uuid | FK → purchase_orders |
| `item_code` | text | SKU |
| `description` | text | Item description |
| `quantity` | int | Total ordered (rounded) |
| `quantity_fl` | int | Florida allocation |
| `quantity_uk` | int | UK allocation |
| `quantity_ph` | int | PH allocation |
| `unit_price` | decimal | Price per unit |
| `line_total` | decimal | qty × price |
| `received_qty` | int | Qty received |
| `product_type` | text | HTPCR, HC, HB401, etc. |

#### `internal_transfers`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `transfer_number` | text | IT-YYYYMMDD-XXX |
| `item_code` | text | SKU |
| `from_warehouse` | text | Always "PH" |
| `to_warehouse` | text | "UK" or "FL" |
| `qty` | int | Transfer quantity |
| `reason` | text | Stock-out prevention |
| `priority` | text | HIGH / MEDIUM / LOW |
| `status` | text | PENDING → APPROVED → PICKED → SHIPPED → RECEIVED |
| `requested_by` | uuid | System or user |
| `approved_by` | uuid | Warehouse manager |
| `created_at` | timestamptz | Request time |
| `shipped_at` | timestamptz | When picked and shipped |
| `received_at` | timestamptz | Delivery confirmation |
| `received_qty` | int | Actual qty received (Council Fix #17: may differ from shipped) |
| `damage_notes` | text | Damage/discrepancy notes on receipt |

#### `shipments`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `shipment_number` | text | SH-YYYYMMDD-XXX |
| `po_ids` | uuid[] | Array of POs in shipment |
| `origin` | text | CN |
| `destination` | text | UK, FL, PH |
| `carrier` | text | DHL, FedEx, UPS |
| `tracking_number` | text | Carrier tracking # |
| `status` | text | PREPARING → IN_TRANSIT → DELIVERED → EXCEPTION |
| `ship_date` | date | When shipped |
| `eta` | date | Estimated arrival |
| `delivered_at` | timestamptz | Actual delivery |
| `packing_list_url` | text | Document URL |
| `invoice_url` | text | Supplier invoice URL |
| `created_by` | uuid | China user |

#### `shipment_lines`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `shipment_id` | uuid | FK → shipments |
| `po_line_id` | uuid | FK → po_lines |
| `item_code` | text | SKU |
| `shipped_qty` | int | Qty shipped |
| `received_qty` | int | Qty confirmed received |

#### `supplier_invoices`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `shipment_id` | uuid | FK → shipments |
| `supplier` | text | Supplier name |
| `invoice_number` | text | Supplier's invoice # |
| `invoice_date` | date | Invoice date |
| `invoice_amount` | decimal | Total |
| `currency` | text | GBP, USD, CNY |
| `invoice_url` | text | PDF/image URL |
| `ocr_status` | text | PENDING → PROCESSING → COMPLETED → FAILED |
| `extracted_data` | jsonb | OCR-extracted fields |
| `xero_invoice_id` | text | Xero reference |
| `xero_status` | text | NOT_POSTED → POSTED → ERROR |

#### `stock_adjustments`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `item_code` | text | SKU |
| `warehouse` | text | UK, FL, PH |
| `adjustment_type` | text | DAMAGE, WASTE, COUNT_CORRECTION, RECEIPT_CORRECTION |
| `qty_change` | int | Positive (add) or negative (remove) |
| `reason` | text | User explanation |
| `llm_confidence` | int | 0-100 score |
| `llm_flags` | jsonb | Validation flags |
| `llm_explanation` | text | LLM reasoning |
| `status` | text | PENDING → AUTO_APPROVED / MANAGER_APPROVED / REJECTED / DOCS_REQUESTED |
| `requested_by` | uuid | User |
| `approved_by` | uuid | Approver |
| `xero_journal_id` | text | Xero reference |

#### `users`

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `email` | text | Login |
| `name` | text | Display name |
| `role` | text | ADMIN, MANAGER, CHINA_OPS, WAREHOUSE |
| `site` | text | UK, FL, PH, CN |
| `warehouse_codes` | text[] | Multi-warehouse access (Cem Council: not single column) |
| `language` | text | en, zh, tl, es |
| `slack_user_id` | text | For notifications |

### 9.3 Master Tables (Cem's Council — Missing from v1.0)

#### `suppliers` (NEW — Council P1-1)

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | PK |
| `name` | text | ECELLSZ, XINTAI, etc. |
| `contact_email` | text | Primary contact |
| `currency` | text | Default currency (CNY, USD) |
| `lead_time_days` | int | Default 21. Admin-editable. (Council: not hardcoded prose) |
| `payment_terms` | text | Net 30, etc. |
| `is_active` | boolean | Soft delete |

#### `warehouses` (NEW — Council P1-2, fixes FL/Florida C3)

| Column | Type | Description |
|--------|------|-------------|
| `code` | text | PK — UK, Florida, PH, CN, TRANSIT |
| `name` | text | Display name |
| `inventory_type` | text | BLANKS, PACKAGING, FINISHED_GOODS |
| `zone` | text | US, UK, SHARED (PH), STAGING (CN) |
| `is_active` | boolean | |

**Constraint:** All `warehouse` FK columns reference `warehouses.code`. Prevents new code variations.

#### `product_group_config` (NEW — Council Fix #12)

| Column | Type | Description |
|--------|------|-------------|
| `product_group` | text | PK — HTPCR, HC, HB401, HLBWH, etc. |
| `fl_ratio` | decimal | US zone FL share (default 0.60) |
| `uk_ratio` | decimal | UK zone UK share (default 0.75) |
| `priority_multiplier` | decimal | Reorder cover multiplier (HB401=1.5, default=1.0) |
| `min_order_qty` | int | Minimum order quantity (MOQ floor) |

**Validation:** Ratios must be validated against 1 quarter of historical shipment data before go-live.

#### `audit_log` (NEW — Council P1-3)

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | PK auto-increment |
| `table_name` | text | Which table changed |
| `record_id` | uuid | Which record |
| `action` | text | INSERT, UPDATE, DELETE |
| `old_data` | jsonb | Previous values |
| `new_data` | jsonb | New values |
| `changed_by` | uuid | User FK |
| `changed_at` | timestamptz | Timestamp |

#### `system_health` (NEW — Council Fix #6 / Blocker #3)

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | PK |
| `component` | text | bigquery_sync, best_sellers_cron, reorder_cron |
| `last_run_at` | timestamptz | When last completed |
| `last_status` | text | SUCCESS, FAILED, RUNNING |
| `snapshot_date` | date | Data date used in last run |
| `error_message` | text | If failed |

**Data Freshness Gate (Council Fix #6):** Before any cron runs:
```sql
SELECT snapshot_date FROM system_health WHERE component = 'bigquery_sync';
-- If snapshot_date < CURRENT_DATE OR last_run_at < NOW() - INTERVAL '6 hours':
--   ABORT run + Slack CRITICAL alert to #ops-critical
--   UI shows "Data as of: X hours ago" stale banner
```

#### `operational_events` (NEW — Council Fix #20)

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigint | PK |
| `event_type` | text | CRON_START, CRON_END, SYNC_START, SYNC_END |
| `component` | text | Which cron/service |
| `started_at` | timestamptz | |
| `completed_at` | timestamptz | NULL if still running |
| `records_processed` | int | Row count |
| `error` | text | If failed |

**Heartbeat:** Health check every 15min alerts on missing completion records.

### 9.4 PO Approval Thresholds (Cem's Council — Blocker #2)

| Amount | Approver | Implementation |
|--------|----------|----------------|
| < $1,000 | Auto-approve | `approval_tier = 'AUTO'` |
| $1,000 – $10,000 | Manager | `approval_tier = 'MANAGER'` |
| $10,000 – $50,000 | Finance Director | `approval_tier = 'FINANCE'` |
| > $50,000 | CEO / CFO | `approval_tier = 'EXECUTIVE'` |

Add `approval_tier` column to `purchase_orders`. Enforced in API — cannot bypass via direct DB write (RLS).

### 9.5 Invoice Fraud Prevention (Cem's Council — Blocker #1)

**Three-way match before Xero posting:**
1. PO quantity matches packing list quantity (±5% tolerance)
2. Packing list quantity matches invoice quantity
3. Supplier on invoice matches supplier on PO (whitelist validation)

**OCR confidence gate (Council Fix #21):** Min 85% confidence before auto-post. Below 85% → `MANAGER_REVIEW` queue with low-confidence fields highlighted in red.

**Flow:** Invoice upload → OCR → Three-way match → Manager approval → Xero post. No auto-post without human step.

### 9.6 Alert Thresholds (AMBER Definition — Council P1-5)

| Level | Formula | Meaning |
|-------|---------|---------|
| **BLACK** | `free_stocks = 0 AND sales_30d > 0` | Stocked out with demand |
| **RED** | `days_of_cover < lead_time_days` (default 21) | Will stock out before replenishment arrives |
| **AMBER** | `days_of_cover < lead_time_days + reorder_cycle_days` (default 35) | Will stock out before NEXT replenishment |
| **GREEN** | `days_of_cover >= 35` | Healthy |

### 9.7 Stock State Machine (Cem's Council P1-10)

```
ON_HAND → (transfer created) → IN_TRANSIT_INTERNAL → (destination confirms) → ON_HAND
ON_ORDER → (supplier ships) → IN_TRANSIT_SUPPLIER → (warehouse confirms) → ON_HAND
ON_HAND → (damaged/lost) → WRITTEN_OFF
```

Each state tracked separately in zone calculations. `IN_TRANSIT_SUPPLIER` and `IN_TRANSIT_INTERNAL` are distinct — prevents double-counting (Council Fix #5 from Cem's report).

### 9.8 Shadow Mode Environment Isolation (Cem's Council P0-4)

```env
SHADOW_MODE=true   # When set:
# - Block ALL Xero writes
# - Redirect Slack to #shadow-test channel
# - Disable PO status updates to production
# - UI shows orange "SHADOW MODE" banner
# - All data writes go to shadow_ prefixed tables
```

### 9.9 RLS Security (Cem's Council P1-8)

All views MUST use `security_invoker = true` (Supabase views bypass RLS by default).

```sql
-- Example RLS policy for warehouse staff
CREATE POLICY "warehouse_own_site" ON inventory_snapshots
  FOR SELECT USING (
    warehouse = ANY(
      SELECT unnest(warehouse_codes) FROM users WHERE id = auth.uid()
    )
  );
```

### 9.2 Views

| View | Purpose | Access |
|------|---------|--------|
| `v_reorder_queue` | Items needing reorder (days_of_stock < 21, not excluded) | Managers/Admins |
| `v_warehouse_top_selling` | Top 50 by site with traffic lights | Warehouse staff (own site) |
| `v_china_dashboard` | Approved POs not yet shipped, priority items | China ops |
| `v_shipment_tracking` | In-transit shipments with ETA | All roles |
| `v_zone_stock_summary` | Zone US / Zone UK stock levels with PH allocation | Managers/Admins |

---

## 10. User Roles & Permissions

| Role | Create PO | Approve PO | Internal Transfer | China Portal | Stock Adjust | View All Sites |
|------|-----------|-----------|-------------------|--------------|-------------|---------------|
| **ADMIN** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **MANAGER** | ✅ | ✅ | ✅ (approve) | View only | ✅ (approve) | ✅ |
| **CHINA_OPS** | ❌ | ❌ | ❌ | ✅ (full) | ❌ | ❌ |
| **WAREHOUSE** | ❌ | ❌ | ❌ | ❌ | ✅ (request) | ❌ (own site) |

---

## 11. Workflows

### 11.1 Stock Adjustment with LLM Validation

```
Warehouse submits adjustment
    ↓
LLM Validation (Claude API):
  • Recent receipts in 5-day window?
  • Open shipments?
  • Pattern analysis (recurring adjustments?)
  • Cross-reference PO receipts, sales, production
  • Confidence score (0-100)
    ↓
  ≤10 units + ≥90% confidence → Auto-approve
  ≤10 units + 70-90% → Manager review
  11-100 units + ≥95% → Auto-approve  
  11-100 units + <95% → Manager review
  >100 units → CFO review + documentation required
    ↓
  ⚠️ CUMULATIVE CAPS (Cem's Council — prevent auto-approval abuse):
  Daily cap: 50 units auto-approved per warehouse
  Weekly cap: 200 units auto-approved per warehouse
  Any breach → freeze auto-approvals for that warehouse, alert finance
    ↓
Approved → Update stock + Post to Xero (write-off)
    ↓
Audit log entry
```

### 11.2 China Procurement (Process 2)

```
Reorder Queue (auto) → PO Created (DRAFT)
    ↓
Manager Approves → APPROVED
    ↓
China downloads by supplier
    ↓
China creates Packing List + uploads Invoice
    ↓
China creates Shipment (tracking, carrier, ETA)
    ↓
Notification to destination warehouse
    ↓
LLM monitors delivery → Carrier confirms delivery?
    ↓
Status set to DELIVERED_PENDING (Council Fix #10 — NOT auto-add)
    ↓
Warehouse confirms physical receipt in portal (24hr window)
    ↓
Stock committed to destination + Post invoice to Xero
```

### 11.3 China Stock Handling (Simplified — Cem, Apr 13)

No transit tracking needed. CN logs receipt and ships — stock appears at destination on confirmation.

```
PO Approved → CN sees it in China Portal
    ↓
CN receives goods from supplier → Logs receipt
    → on_order decreases
    ↓
CN creates packing list → Ships to destination
    ↓
Destination confirms receipt
    → free_stocks increases at destination
```

**No in-transit state.** Stock goes from "on order" to "at destination" when CN ships and destination confirms. CN just needs: log arrivals, create packing lists, mark as shipped.

---

## 12. UI/UX Requirements

### Language Support

| Language | UI | Content |
|----------|-----|---------|
| English | ✅ Full | ✅ Full |
| Mandarin | ✅ Full (China portal) | POs, Packing Lists, Invoices |

### China Portal Screens (Mandarin)

1. **Dashboard** — Pending POs, shipments in progress, exceptions
2. **PO List** — Download by supplier, filter by status
3. **Packing List Generator** — Select PO lines → generate PDF
4. **Shipment Creator** — Upload docs, add tracking, set ETA
5. **Items On Order** — Priority view with exception highlighting
6. **Invoice Upload** — Drag-drop, OCR preview, submit to finance

**China staff CANNOT:** create POs, approve POs, adjust stock, access warehouse pages.

### Manager/Admin Screens

1. **Dashboard** — Stock alerts, incoming shipments, approval queue
2. **Inventory** — Site-specific stock with traffic lights + zone summary
3. **Reorder Queue** — Auto-generated PO recommendations
4. **Internal Transfers** — PH → FL/UK transfer requests + approvals
5. **Shipment Tracker** — Inbound from China
6. **PO Approval** — Approve/reject pending POs

### Warehouse Staff Screens (Read-Only + Adjustments)

1. **Top Selling Items** — Own site, stock on hand, traffic lights
2. **Stock Adjustment** — Request damage/waste/count corrections
3. **My Requests** — Track adjustment status

**Warehouse staff CANNOT:** create POs, view reorder queue, access China portal, see other sites.

---

## 13. Notification System

### Slack

| Event | Channel | Message |
|-------|---------|---------|
| PO Approved | #procurement | PO-XXX approved → Supplier → Destination |
| Shipment Created | #logistics-{site} | SH-XXX created, ETA, packing list |
| Shipment Delivered | Site channels | SH-XXX delivered, stock auto-added |
| Delivery Exception | #procurement-alerts | SH-XXX delay/exception |
| Low Stock (RED/BLACK) | Site channels | Item XXX at critical level |
| Internal Transfer | #logistics-{site} | Transfer IT-XXX: PH → FL, X units |
| Stock Adjustment | #finance | Adjustment requested: X units, confidence Y% |

### Email

- Daily digest of pending approvals (managers)
- Weekly reorder summary
- Exception reports

---

## 14. Implementation Phases

### Recommended Build Approach

### Build Approach: Shadow Mode (Cem, Apr 13)

**Decision:** Build and launch for testing. Run in parallel with current Zero process.

```
SHADOW MODE (Testing Phase):
  
  Current process (Zero + Chris/Jae)     New system (Procurement App)
           ↓                                        ↓
   Produces transfer/order list              Produces transfer/order list
           ↓                                        ↓
           └──────────── COMPARE ───────────────────┘
                           ↓
                   GAP Analysis
                   • What did the system recommend that Zero didn't?
                   • What did Zero produce that the system missed?
                   • Key differences in quantities, items, destinations
                           ↓
                   Fix gaps → Re-run → Compare again
                           ↓
                   Confidence threshold met → Cutover
```

**Benefits:**
- Zero risk — current process continues uninterrupted
- Real-world validation with actual data
- Exposes edge cases no spec can predict
- Chris/Jae build confidence in new system before cutover
- Cem can verify data accuracy side-by-side

**Requirement:** System must produce output in comparable format to Zero's output for side-by-side GAP analysis.

### Build Phases (progressive, launch when ready)

**Codex's 3-week structure as guide (not hard deadline):**
- **Week 1:** Core procurement backbone — inventory ingestion, reorder logic, PO creation, manager approval
- **Week 2:** China execution — Mandarin UI, packing lists, invoice upload, exception queue
- **Week 3:** Accounting closure — Xero integration, LLM validation, audit trails, end-to-end UAT

### Full Phase Plan

**Phase 1: Core + China + Finance (3 weeks)**
- [x] Supabase schema (Harry — exists, needs enhancement)
- [ ] Best sellers daily staging table + cron
- [ ] Tiered velocity logic (7d/30d)
- [ ] Supply zone calculations
- [ ] Internal stock transfers (Process 1)
- [ ] Reorder queue with exclusions
- [ ] PO creation with allocation + shipping plan
- [ ] Manager approval workflow
- [ ] CSV/PDF export for Ben
- [ ] China portal (Mandarin UI)
- [ ] Packing list + invoice upload
- [ ] Shipment creation + tracking
- [ ] LLM stock adjustment validation
- [ ] Xero invoice posting
- [ ] Notification system (Slack)

**Phase 2: Advanced (2 weeks)**
- [ ] Predictive reordering (PULSE integration)
- [ ] Supplier performance scorecards
- [ ] Carrier API integration (live tracking)
- [ ] Delivery monitoring (LLM)
- [ ] Exception reports + priority algorithms

**Phase 3: Optimisation (Ongoing)**
- [ ] Inventory turns optimisation
- [ ] Cost per unit analysis
- [ ] Seasonal demand patterns
- [ ] Auto stock receipt on delivery

---

## 15. Open Questions

| # | Question | Status | Answer |
|---|----------|--------|--------|
| 1 | Build approach? | ✅ Answered | Shadow mode — build, launch for testing, run parallel with Zero, compare outputs, GAP analysis, fix, cutover. |
| 2 | How do internal transfers work today? | ✅ Answered | Chris Yunnun triggers in legacy Zero system. Jae & Chris send packing list emails. |
| 3 | Who approves internal transfers? | ✅ Answered | Chris Yunnun (warehouse manager, PH) |
| 4 | Who arranges freight for PH→FL / PH→UK transfers? | ✅ Answered | No separate freight — blanks piggyback on existing PH→FL/UK finished goods shipments (2-3x/week) |
| 5 | Is there a cost threshold where transfer doesn't make sense? | ✅ Answered | No cost blockers — zero additional freight cost |
| 6 | When transfer is created, does PH stock immediately show as "in transit"? | ✅ Answered | Yes — PH stock deducts, shows as in transit |
| 7 | Reorder level days of cover? | ✅ Answered | Normal: 30 days. Best sellers: 45 days. Lead time: 14-21 days. |
| 8 | Stale stock threshold? | ✅ Answered | 30d no sales = stale (exclude from reorder). Sales <5/week + created 2024 or earlier = retire candidate (flag, human decides). |
| 9 | China warehouse tracking? | ✅ Answered | No transit state. CN logs receipt, creates packing list, ships. Destination confirms → stock added. |
| 10 | Which carrier APIs? | ⏳ Phase 2 | Not needed for shadow mode testing. |
| 11 | Agentic architecture? | ✅ Answered | 3 layers: Data (SQL/cron) → Intelligence (Claude API, advisory) → Portal (human gatekeeper). No autonomous action. |

---

## 16. Appendix: Agent Reviews

### Review Summary

| Agent | Grade | Key Contribution | Document |
|-------|-------|-----------------|----------|
| **Codex** | A | Adversarial review. Argued for fuller Phase 1. 3-week weekly milestone plan. | `CODEX_ADVERSARIAL_REVIEW.md` |
| **Ava** | A- | Strategic SWOT. Identified 5 critical gaps. MVP PRD with success metrics. | `AVA_STRATEGIC_REVIEW.md` |
| **Athena** | — | Data integrity audit. Found 3 critical issues. Designed supply zone model. Identified two-process architecture. | `DATA_INTEGRITY_REPORT.md` + this doc |
| **Harry** | B+ | Original spec v2.6. Comprehensive but over-scoped. | `PROJECT (2).md` |
| **Hermes** | C+ | 3 advisory versions. Some useful gap analysis but missed critical data issues. | `ADVISORY_*.md` (V1, V2, V3) |

### Key Improvements Over Original Spec

| Area | Harry's v2.6 | This Master PRD |
|------|-------------|----------------|
| Velocity | 7d only (inflates by 126%) | Tiered: best sellers MAX(7d,30d), others 30d |
| Data source | Assumed orders table usable | Documented: orders table is 30% incomplete, use blank_inventory |
| Warehouse codes | FL and Florida used interchangeably | Mapped: FL=packaging, Florida=blanks. Normalisation rules. |
| Processes | Single procurement flow | Two processes: Internal Transfers + Supplier Ordering |
| Stock assessment | Global stock totals | Supply zones (US/UK) with proportional PH allocation |
| Shipping plan | Fixed percentage split | Zone-need-based allocation with configurable ratios per product |
| Reorder levels | Static (98% zero) | Dynamic calculation from velocity × lead time |
| Alert system | GREEN/RED only | GREEN/AMBER/RED/BLACK with thresholds |

---

---

## 17. Concurrent Run Protection (Council Fix #8)

```sql
-- Prevent duplicate suggestions from overlapping cron + on-demand runs
CREATE TABLE cron_run_lock (
  component TEXT PRIMARY KEY,
  locked_at TIMESTAMPTZ,
  locked_by TEXT  -- 'scheduled' or 'on_demand'
);

-- Before each run:
-- SELECT FOR UPDATE SKIP LOCKED from cron_run_lock WHERE component = 'reorder_calc'
-- If locked: queue and coalesce triggers. Don't generate duplicate transfer lists.
```

---

## 18. Environment Configuration (Cem's Council — Build Readiness)

### `.env.example`

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Claude API (Layer 2 Intelligence)
ANTHROPIC_API_KEY=

# Xero (Finance Integration)
XERO_CLIENT_ID=
XERO_CLIENT_SECRET=

# Google Cloud (BigQuery + OCR)
GCP_PROJECT_ID=instant-contact-479316-i4
GCP_SERVICE_ACCOUNT_BASE64=

# Slack Webhooks
SLACK_WEBHOOK_PROCUREMENT=
SLACK_WEBHOOK_LOGISTICS_UK=
SLACK_WEBHOOK_LOGISTICS_FL=
SLACK_WEBHOOK_LOGISTICS_PH=
SLACK_WEBHOOK_OPS_CRITICAL=

# Email
SENDGRID_API_KEY=

# Shadow Mode
SHADOW_MODE=false

# Feature Flags
LAYER2_ENABLED=false          # Defer Layer 2 to post-cutover (Council recommendation)
AUTO_XERO_POST_ENABLED=false  # Require manual Xero posting until shadow mode passes
```

---

## 19. Shadow Mode Metrics (Council — Cutover Criteria)

For cutover from Zero to new system, run parallel for minimum 2 full cycles (4 weeks):

| Metric | Threshold | Measurement |
|--------|-----------|-------------|
| Items flagged for reorder | ≥90% overlap with Zero's output | `item_code` intersection |
| Recommended quantities | Within ±15% of Zero's quantities | Per-item variance |
| Transfer destinations | 100% match (FL/UK/PH routing) | Exact match required |
| Stock-out prevention | New system flags all items Zero flagged + extras | Superset check |
| False positives | <5% recommendations Zero would not have made | Manual review |

**Requirement:** Document Zero's exact CSV export format before build starts (Council P2-6). Shadow mode comparison script joins on `item_code` and flags variances >5%.

**End-to-end dry runs required** (Codex CX-8): Not just list comparison — test full workflow: approvals, tracking, receipt confirmation.

---

## 20. Appendix: Council Fixes Applied (v2.0)

### Athena's Council (Code Architect + Adversary + Codex GPT-5.4)

| # | Fix | Status |
|---|-----|--------|
| 1 | PH allocation div-by-zero → default 60/40 | ✅ Applied |
| 2 | NULL stock COALESCE to 0 | ✅ Applied |
| 3 | Effective PH stock = free_stocks - pending_transfers_out | ✅ Applied |
| 4 | In-transit deducted from zone need | ✅ Applied |
| 5 | Stale rule: zero stock items NOT stale | ✅ Applied |
| 6 | Data freshness gate before cron | ✅ Applied |
| 7 | Math.max(0) on all intermediates + assertion | ✅ Applied |
| 8 | Concurrent run lock (SELECT FOR UPDATE SKIP LOCKED) | ✅ Applied |
| 9 | PH replenishment — daily cron if PH stocked out | ✅ Applied |
| 10 | Delivery → DELIVERED_PENDING, warehouse confirms | ✅ Applied |
| 11 | Best seller sets zone-aware | ✅ Already in spec (Top 50 per zone) |
| 12 | Ratios in product_group_config table, admin-editable | ✅ Applied |
| CX-1 | Normal reorder threshold thin → 30d cover provides 9-16d buffer | ✅ Documented |
| CX-5 | PH safety stock 14d → 21d (≥ lead time) | ✅ Applied |
| CX-10 | Best seller spec contradiction fixed | ✅ Applied (MAX(7d,30d) is canonical) |

### Cem's Council (Claude Opus + GPT-5.4 + Gemini Pro)

| # | Fix | Status |
|---|-----|--------|
| P0-1 | PO approval financial thresholds | ✅ Applied (Section 9.4) |
| P0-2 | Invoice 4-eyes gate + three-way match | ✅ Applied (Section 9.5) |
| P0-3 | BigQuery sync monitoring + stale banner | ✅ Applied (system_health table + freshness gate) |
| P0-4 | Shadow mode environment isolation | ✅ Applied (Section 9.8) |
| P0-5 | PH zone formula NULLIF fix | ✅ Applied (Section 6) |
| P1-1 | Suppliers master table | ✅ Applied (Section 9.3) |
| P1-2 | Warehouses lookup table | ✅ Applied (Section 9.3) |
| P1-3 | Audit log table | ✅ Applied (Section 9.3) |
| P1-4 | Cron DAG dependency chain | ✅ Applied (Operating Cadence) |
| P1-5 | AMBER alert threshold formula (<35d cover) | ✅ Applied (Section 9.6) |
| P1-6 | Cumulative auto-approval caps | ✅ Applied (Section 11.1) |
| P1-7 | Partial indexes for DISC filter | ✅ Noted for migration SQL |
| P1-8 | RLS policy definitions | ✅ Applied (Section 9.9) |
| P1-9 | .env.example | ✅ Applied (Section 18) |
| P1-10 | Stock state machine | ✅ Applied (Section 9.7) |
| P2-1 | Downtrend velocity flag | ✅ Applied (checkDowntrend function) |
| P2-2 | PH scarcity priority queue | ✅ Applied (prioritiseTransfers function) |
| P2-4 | HB401 priority_multiplier | ✅ Applied (product_group_config) |
| P2-10 | DELIVERED_PENDING state | ✅ Applied (Section 11.2) |

**Deferred to Phase 2 (per Council recommendation):**
- P2-3: Separate FBA safety stock tier (30d) — needs Cem decision
- P2-5: lead_time_days on suppliers table — ✅ added but default used for now
- P2-7: Xero multi-entity routing (UK vs US) — needs architect
- P2-8: Currency column on financial tables — added to supplier_invoices (already has it)
- P2-9: China portal file injection mitigations — Phase 2 hardening
- P3-1: Increase best-seller cover to 56d — needs Cem decision
- P3-2: Auth method — default Supabase Email/Password for Phase 1
- P3-3: Cron infrastructure — pg_cron for Phase 1 (Supabase native)
- P3-4: BigQuery sync strategy — incremental upsert on snapshot_date

**Layer 2 (Claude API Intelligence):** Deferred to post-cutover per both councils' recommendation. Layer 1 (SQL/cron) + Layer 3 (portal) are sufficient for shadow mode. `LAYER2_ENABLED=false` by default.

---

*Compiled by Athena | 2026-04-13 | v2.0 with Council Fixes*
*Sources: Harry PROJECT.md v2.6, Ava Strategic Review, Codex Adversarial Review, Athena Data Integrity Audit, Cem live directives (Telegram, Apr 13), LLM Council Review (Athena's), LLM Council Review (Cem's)*
*Total fixes applied: 35 (from 2 independent council reviews)*
