# Layer 0 Compliance ↔ Procurement Integration Brief

> **From:** amazon-unified-score session (Cem + Claude)
> **To:** procurement session (Harry / Ava)
> **Date:** 2026-04-15 (updated 2026-04-16)
> **Status:** PARTIAL — integration is one-way for now (listings reads inventory; procurement does not yet consume `compliance_flags`)
> **Related:**
> - [[PROCUREMENT_SYSTEM_SPEC]] (Ava, 2026-03-20)
> - [[HARRY_HANDOFF]] (2026-03-20)
> - [[LISTINGS_PIPELINE_PRD]] v1.2 — has its own §16 web UI spec with full inventory join
> - `~/.claude/plans/polymorphic-knitting-hippo.md` (Layer 0 plan addendum)
> - `~/Desktop/Repos/amazon-unified-score/PROJECT_BRIEF.md`

## 0. Implementation Status (2026-04-16)

| Side | Status | Notes |
|---|---|---|
| **Inventory READ from procurement's Supabase** | ✅ LIVE | listings-pipeline pulls `blank_inventory` via REST API into a local 24h-TTL cache (`data/inventory_cache.db`). Default source: Supabase. Fallback: BigQuery `zero_dataset.inventory`. |
| **Web UI inventory display** | ✅ LIVE | Dashboard `/dashboard` shows per-warehouse breakdown, freshness pill, source dropdown, and an "In Stock Only" filter that joins listings against this cache to surface actionable counts. |
| **`compliance_flags` table in Supabase** | ⏳ PENDING | Schema is fully specified below (§3). Not yet created — owned by the procurement-session migration when it next runs. |
| **Procurement priority boost from compliance flags** | ⏳ PENDING | Once the table exists, listings-pipeline will write to it; procurement reads it in `lib/inventory/reorder.ts` to multiply `priorityMultiplier` for CRITICAL items. |
| **Two-way handshake** | ⏳ PENDING | When the priority boost is wired, both sides should add a heartbeat to confirm freshness. |

The half that's live (inventory consumption) is what unblocked the listings dashboard; the other half (compliance write-back) is queued for whenever the procurement session next picks this up.

---

## 1. Context

A sibling session is building `amazon-unified-score` — a biweekly engine that routes every active Amazon listing into one of four queues (RESTOCK / VALIDATE / MONITOR / CULL) based on a composite demand score.

Layer 1/2 (scoring + routing) is built and tested against 76,861 US SKUs in ~6 seconds. Layer 0 (listing compliance) is next — it validates that every active FBM listing has the correct shipping template for its (marketplace, stock, product-type) tuple **before** scoring runs, since a wrong template suppresses CVR by ~25–53% and would otherwise under-rank thousands of SKUs.

During the Layer 0 design review, it became clear that **stock-out flagging already exists in this project** — the amazon-unified-score session should not re-implement it. The clean split is:

```
  procurement-system  →  OWNS stock monitoring, reorder, PO generation
                          Reads zero_dataset.inventory (BQ), writes POs

  amazon-unified-score →  OWNS Amazon listing compliance + scoring
                          Reads zero_dataset.inventory (BQ), writes
                          compliance_flags that procurement can consume
                          to prioritise urgent Prime-promise-at-risk POs
```

`compliance_flags` is the **one shared contract** proposed here. This brief exists so both sessions implement each side of it consistently without stepping on each other.

---

## 2. What Layer 0 Needs from Procurement (Read Path)

Layer 0 reads the following from `zero_dataset.inventory` (or the Supabase cache of it — see §6 open question):

| Field | Used For |
|---|---|
| `Item_Code` | Join key to active listings via `base_sku` = first two hyphen-delimited segments |
| `Warehouse` | Filter to `FL` and `UK` only (PH is overflow, not primary for Layer 0) |
| `Free_Stocks` | Primary template eligibility — `>0` required for fast template |
| `Sales_Last_7_Days` | Velocity for the restricted-prefix cushion check |
| `Sales_Last_30_Days` | Velocity baseline |
| `Ave_Daily_Sales` | For days-of-cover math |
| `Reorder_Level` | Reference — Layer 0 does not override procurement's trigger |
| `On_Order` | Whether a shortfall is already being resupplied |
| `Supplier` | Diagnostic only — referenced in the flag for ops visibility |

Layer 0 does **not** compute velocity or alert level independently. If the procurement session's velocity calculator (Phase 1, Week 1 per HARRY_HANDOFF) writes a normalised `days_of_cover` field back to the inventory view or a derived table, Layer 0 will use that directly.

---

## 3. What Layer 0 Writes Back (Write Path)

Layer 0 emits a new table `compliance_flags` that procurement can join to `reorder_suggestions` for priority boosting.

### Proposed DDL

```sql
CREATE TABLE compliance_flags (
  id                BIGSERIAL PRIMARY KEY,
  item_code         VARCHAR(100) NOT NULL,   -- base SKU, e.g. 'HTPCR-IPH17'
  marketplace       CHAR(2) NOT NULL,        -- US / UK / DE / FR / IT / ES
  warehouse         CHAR(2) NOT NULL,        -- FL / UK — the primary for this marketplace
  flag_type         VARCHAR(40) NOT NULL,    -- see enum below
  severity          VARCHAR(10) NOT NULL,    -- CRITICAL / HIGH / MEDIUM
  current_template  VARCHAR(100),            -- e.g. 'Nationwide Prime'
  required_template VARCHAR(100),            -- e.g. 'Default Amazon Template'
  days_of_cover     INT,                     -- read from procurement's velocity calc
  velocity_7d       DECIMAL(10,2),
  listings_affected INT,                     -- how many full SKUs share this base_sku
  first_raised_at   TIMESTAMPTZ DEFAULT NOW(),
  last_seen_at      TIMESTAMPTZ DEFAULT NOW(),
  resolved_at       TIMESTAMPTZ,
  resolved_reason   VARCHAR(200),
  CONSTRAINT uk_item_mp_flag UNIQUE (item_code, marketplace, flag_type)
);

CREATE INDEX idx_compliance_flags_active
  ON compliance_flags (severity, marketplace, warehouse)
  WHERE resolved_at IS NULL;
```

### flag_type enum

| flag_type | Meaning | Severity |
|---|---|---|
| `prime_promise_risk` | SKU is on a Prime/fast template (Nationwide Prime, Reduced Shipping) but primary warehouse stock is below the safe cushion. Risk of breaking SLA. | CRITICAL |
| `restricted_critical` | SKU uses a PH-restricted prefix (`HB6`, `HB7`, `HDMWH`, `HSTWH`, `H89`, `H90`) and primary stock is low or zero. **No PH overflow exists** — listing will go unfulfillable on primary stockout. | CRITICAL |
| `template_mismatch` | Stock exists at primary but listing is not on the fast template — we are leaving CVR on the table. Not a promise risk, just an opportunity cost. | MEDIUM |
| `blank_oos_unfulfillable` | Blank stock = 0 at primary, PH cannot overflow (restricted prefix), no inbound on-order. Listing must go temporarily suppressed. | CRITICAL |
| `blank_oos_overflow_ok` | Blank stock = 0 at primary but PH can overflow (non-restricted prefix). Listing stays live on Default template. Informational. | MEDIUM |

### Why procurement cares about these flags

The procurement reorder trigger today is `Free_Stocks < Reorder_Level AND On_Order = 0`. That's correct for supply-chain purposes. But it doesn't distinguish:

1. A `HB6` (MagSafe bumper) at 5 units in FL with a Nationwide Prime listing assigned → **Prime promise actively at risk, no fallback** → CRITICAL reorder
2. A generic `HTPCR` (phone case) at 5 units in FL → PH can overflow, listing stays fulfillable on Default template → routine reorder

Both trigger procurement's reorder logic. But (1) should be treated as **P0 expedited** and (2) as **P2 routine**. `compliance_flags` gives procurement the signal to make that call.

Concretely, the procurement PO generator could add a priority multiplier:

```ts
// Pseudocode for procurement's Phase 2 PO generator
let priority = 1.0;
if (hasFlag(item_code, 'prime_promise_risk', 'CRITICAL')) priority *= 1.5;
if (hasFlag(item_code, 'restricted_critical', 'CRITICAL')) priority *= 2.0;
// no fallback — absolute priority
```

This feeds directly into the `priority_multiplier` already present in `lib/inventory/reorder.ts:getReorderQty()`.

---

## 4. What Layer 0 Will NOT Do

To be clear about the boundary:

| Capability | Owner |
|---|---|
| Velocity calculation | **procurement-system** — Layer 0 reads it |
| Reorder quantity math | **procurement-system** — Layer 0 does not propose quantities |
| PO generation | **procurement-system** |
| Supplier grouping / currency / split | **procurement-system** |
| China receiving UI | **procurement-system** |
| Stock alert levels (BLACK/RED/AMBER/GREEN) | **procurement-system** — Layer 0 consumes |
| Listing template validation | **amazon-unified-score (Layer 0)** |
| Shipping-template decision tree per marketplace | **amazon-unified-score (Layer 0)** |
| Restricted-prefix gating (PH equipment gap) | **amazon-unified-score (Layer 0)** |
| Composite demand scoring | **amazon-unified-score (Layer 1)** |
| Queue routing (RESTOCK/VALIDATE/MONITOR/CULL) | **amazon-unified-score (Layer 2)** |

---

## 5. The Layer 0 Rule Set (for reference — procurement does not implement this)

This is what Layer 0 computes to decide whether to raise a flag. Included here so the procurement session can see *why* a flag was raised without reading a separate repo.

### Per-marketplace routing rules

```
  US customer orders    →  FL primary  → (PH overflow for non-restricted only)
  UK customer orders    →  UK primary  → (PH overflow for non-restricted only)
  DE/FR/IT/ES orders    →  UK primary  → (PH overflow for non-restricted only)
  JP customer orders    →  PH direct   (separate track, not in Layer 0 scope)
```

### PH-restricted prefixes (equipment gap)

PH cannot print: `HB6`, `HB7`, `HDMWH`, `HSTWH`, `H89`, `H90`

These are bumper cases (HB6/HB7), desk mats (HDMWH), stickers (HSTWH), and vinyl skins (H89/H90). FL and UK both have the specialty equipment for these; PH does not. This means a primary stockout on any of these 6 prefixes is **unfulfillable**, not just slow.

> Note: HSTWH and H8939 are printed in-house on vinyl rolls per PROCUREMENT_SYSTEM_SPEC §2.4, so procurement does not source blanks for them. But Layer 0 still tracks them because they appear on Amazon listings that need the right shipping template.

### Shipping templates (per marketplace)

**US:**
- `Reduced Shipping Template` — FL 2-day FedEx, buyer pays $10.99 extra (fast, no Prime badge)
- `Default Amazon Template` — standard 4–6 day
- SFP (Seller-Fulfilled Prime) — free 2-day with Prime badge, +$10.99 absorbed into price

**UK (confirmed from Seller Central PDFs, 2026-04-15):**
- `Nationwide Prime` — free 3-5 day + free 2-day premium + free 1-day premium, Prime badge, FREE international to EU/RoW
- `Reduced Shipping Template` — tracked (Royal Mail Tracked 24), £1.99/item, no Prime badge
- `Default Amazon Template` — standard 3-5 day, £1.99/item

**Ship-from:** `Ecell Global LTD - GB, FY4 5PS` (Blackpool) for UK.

### The validation logic (simplified)

```
for each active FBM listing:
  base_sku = first two segments of seller_sku (e.g. 'HTPCR-IPH17')
  marketplace = listing's marketplace
  primary_warehouse = FL if marketplace == 'US' else 'UK'

  stock = blank_inventory[base_sku, primary_warehouse].Free_Stocks
  velocity = blank_inventory[base_sku, primary_warehouse].Ave_Daily_Sales
  is_restricted = base_sku starts with ('HB6','HB7','HDMWH','HSTWH','H89','H90')

  if stock == 0:
    if is_restricted:
      raise flag(blank_oos_unfulfillable, CRITICAL)
      → listing should be temporarily suppressed
    else:
      raise flag(blank_oos_overflow_ok, MEDIUM)
      → default template correct, PH overflow will fulfil

  elif current_template is fast (Reduced/Nationwide Prime):
    required_cushion = 7 days if is_restricted else 3 days
    if stock / velocity < required_cushion:
      raise flag(prime_promise_risk, CRITICAL)
      → boost reorder priority

  elif current_template is default AND stock > required_cushion:
    raise flag(template_mismatch, MEDIUM)
    → not urgent, but missing a CVR uplift opportunity
```

---

## 6. Open Questions for the Procurement Session

1. **Data source confirmation.** PROCUREMENT_SYSTEM_SPEC §2 says "all in BigQuery" with `zero_dataset.inventory` as the live view. The sibling Next.js app at `github.com/gemc-wq/procurement-system` reads Supabase `blank_inventory` via `@/lib/db`. Which is the operational source of truth for Layer 0 to read — BigQuery directly, or Supabase as a cache? Or does a sync keep them aligned so either is safe? The sibling session's current working assumption is **Supabase** (matches the Next.js code), but this brief is pending your confirmation.

2. **`days_of_cover` field availability.** Procurement's velocity calculator (Phase 1, Week 1 per HARRY_HANDOFF) will compute rolling velocity. Will it also write a `days_of_cover` or equivalent back to an accessible table, so Layer 0 can read it without duplicating the calculation? Or should Layer 0 compute it locally from `Free_Stocks / Ave_Daily_Sales`?

3. **`compliance_flags` table home.** Three options:
   - (a) Supabase, same project as `blank_inventory` — simplest join, procurement reads it directly
   - (b) BigQuery `amazon_reports` dataset — consistent with the unified-score ETL flow
   - (c) Both, with Supabase as the hot read and BQ as the cold archive

   Recommendation: **(a)** for Phase 1 — same project, same auth, no new infra. Move to (c) once we have historical audit needs.

4. **Schema change approval.** The `compliance_flags` table needs a migration in the procurement-system Supabase project (since that's where `blank_inventory` lives). That migration should be owned by the procurement session — this brief is the proposal, not the migration. Green-light to write the migration when the procurement session next runs?

5. **Priority multiplier integration.** The reorder engine at `lib/inventory/reorder.ts:getReorderQty()` already accepts a `priorityMultiplier` parameter. Proposal: the procurement session's next change adds a compliance-flag lookup that feeds this multiplier. Does this match how you want compliance input to enter the reorder loop, or would you rather it come in as a separate field (e.g. `is_compliance_critical` boolean alongside `is_best_seller`)?

6. **Non-pipeline prefixes.** PROCUREMENT_SYSTEM_SPEC §2.4 notes that HSTWH and H8939 are vinyl-roll-printed and not in the PO pipeline. Layer 0 still raises compliance flags for them (because they have Amazon listings and need shipping templates), but should those flags be routed somewhere else — a "consumables alert" queue rather than the main reorder queue — since procurement won't act on them via POs?

---

## 7. Proposed Sequence

No work starts until the procurement session reviews this brief. Once reviewed:

### From amazon-unified-score side

1. Implement `loaders/inventory.py` pointing at the confirmed data source (Supabase or BQ per §6 Q1)
2. Implement `compliance/validator.py` with the Layer 0 rule set from §5
3. Emit `compliance_flags` rows (writes to whichever DB is confirmed in §6 Q3)
4. Add `FIX_TEMPLATE`, `FIX_STOCK_CRITICAL`, `FIX_STOCK_STANDARD` as additional output queues on top of the existing RESTOCK / VALIDATE / MONITOR / CULL

### From procurement side (if/when you pick this up)

1. Create `compliance_flags` table migration
2. Add a lookup in `lib/inventory/reorder.ts` that boosts `priorityMultiplier` when CRITICAL flags exist for an `item_code`
3. Surface compliance flags in the dashboard UI alongside existing alert_level (not replacing — supplementing)
4. (Optional) Add a "SLA at risk" filter to the reorder queue page showing only items with active compliance flags

---

## 8. Why This Is Worth Building

From the amazon-unified-score smoke test on 76,861 real US SKUs:

- **26 SKUs currently in the RESTOCK queue** with combined revenue of $8.4K/mo
- **102 SKUs in VALIDATE** ($13.7K/mo)
- **19,721 SKUs in MONITOR** ($150.7K/mo — the long tail waiting for a signal)

Per the Perplexity LLM council review (Layer 0 doc v1.3, April 2026), fixing mis-assigned shipping templates on US FBM delivers **+53% CVR** (2.26% → 3.46%) and on UK **+39% CVR** (2.69% → 3.74%). Per the FBA strategy SOP (April 2026), critical T1 stockouts are leaking ~$3,100+/mo in recoverable revenue today.

Layer 0 without this integration would write these flags to a CSV that sits in someone's Downloads folder. With this integration, the same flags become a priority signal in the reorder queue that procurement already runs every Monday. Zero incremental operational overhead; the value is in the routing.

---

*This brief is a proposal from the amazon-unified-score session. It exists to be reviewed, edited, or rejected by the procurement session — not to dictate. Any response, edits, or counter-proposals can be made by editing this document directly, and the amazon-unified-score session will pick up the changes on next run.*
