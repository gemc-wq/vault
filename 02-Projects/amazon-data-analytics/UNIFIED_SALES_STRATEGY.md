# Unified Amazon Sales Strategy — FBM / FBA / Seller-Fulfilled Prime
**Head Case Designs | v1.0 | 2026-04-15**
**Author:** Athena (synthesis) · **Consumers:** Cem, Hermes, Ava · **Review cadence:** Monthly

> **Sources synthesised:**
> - [amazon-fba-strategy-sop.pplx.md](~/Downloads/amazon-fba-strategy-sop.pplx.md) — 7-pillar FBA framework
> - [fbm-twin-dead-stock-strategy.pplx.md](~/Downloads/fbm-twin-dead-stock-strategy.pplx.md) — FBM twin demand signal
> - [PROJECT_SHIPPING_TEMPLATE_OPTIMIZATION.md](~/Downloads/PROJECT_SHIPPING_TEMPLATE_OPTIMIZATION.md) — +25% CVR shipping lever
> - [MIDDLEWARE_PRD_CONSOLIDATED.md](~/Documents/Cem%20Vault/02-Projects/amazon-data-analytics/MIDDLEWARE_PRD_CONSOLIDATED.md) — data pipeline
> - [SOP_SHIPPING_TEMPLATE_OPTIMIZATION.md](~/Documents/Cem%20Vault/02-Projects/amazon-data-analytics/SOP_SHIPPING_TEMPLATE_OPTIMIZATION.md) — procedural detail

---

## 1. Thesis & Opportunity

**Fulfilment channel is a CVR lever, not a cost lever.** Every SKU has three viable routes to a customer — FBA, FBM, or Seller-Fulfilled Prime — and the right one depends on demand signal and unit economics, not blanket policy. POD catalogs like ours live or die by the interaction between two truths:

1. **CVR compounds ranking.** A 2% → 4% CVR bump is not +100% sales; Amazon's A9 rewards it with +200–400% over 60 days because sessions follow rank.
2. **Inventory is the enemy of optionality.** Every unit in FBA is a bet against pivoting. The only units that should live in a fulfilment centre are the ones already earning their placement fee back in conversion uplift.

Those two truths collapse to a simple rule: **FBA is for proven demand; FBM is for demand discovery; SFP is for the bridge.**

### Consolidated opportunity size

| Stream | Source | Annualised |
|---|---|---|
| FBM twin → FBA restocks (33 STRONG + 151 MODERATE) | FBM twin doc | **£600K–960K/yr gross** |
| T1 OOS recovery (114 SKUs) | FBA SOP | ~$37K/yr |
| Shipping template fix (9,778 US FBM SKUs, +25% CVR) | Shipping SOP | ~$200K/yr |
| SFP trial (10 high-CVR candidates) | This doc | Unproven — pilot |
| **Total gross at stake** | — | **~$850K–1.2M/yr** |

Three motions run in parallel across the next 90 days: **(a) restock proven winners, (b) cull dead weight, (c) upgrade fulfilment on high-CVR FBM items.** Nothing on this page is new demand creation — it is all reclaiming revenue the current catalog already earns but loses to channel mismatches.

---

## 2. The Three-Channel Decision Model

Every active ASIN must resolve to exactly one primary fulfilment channel per marketplace. Use this table before any restock decision:

| SKU State | Signal | Channel | Rationale |
|---|---|---|---|
| Proven seller, stable demand | ≥5u/30d, CVR ≥3% | **FBA** | Prime badge compounds ranking; expect 2.0–2.8× FBM multiplier |
| New launch (iPhone 18, new IP) | Untested, zero history | **FBM day 1 → FBA day 14** | Zero inventory risk; convert after first demand signal |
| High-CVR niche, low volume | CVR ≥8%, <5u/30d | **SFP trial** | Prime badge without FBA placement cost; validates before commit |
| Long-tail catalog filler | <1u/30d | **FBM only** | Near-zero carrying cost; auto-culls itself if dead |
| Zero signal 90+ days | 0u, 0 sessions | **Suppress FBA, keep FBM live** | FBM listing remains as demand sensor; no storage cost |
| T1 OOS, FBA ETA >7d | Active demand, stock on hand | **FBM bridge** | Only if ASP ≥$18, CVR >5% |

### Channel unit economics (US)

| Cost Line | FBA | FBM Reduced Template | SFP |
|---|---|---|---|
| Customer pays shipping | $0 (Prime) | $10.99 (pays for FedEx 2-day) | $0 (Prime) |
| Seller fulfilment cost | $6 fee to Amazon | $11–12 FedEx | $11–12 FedEx |
| Storage cost | Monthly + LTSF risk | $0 | $0 |
| Prime badge | ✅ | ❌ | ✅ |
| CVR lift vs Default FBM | +~200% (A9 boost) | +25% (confirmed) | +~100–150% (estimated) |
| **Break-even ASP vs FBA** | baseline | ≥$16 | ≥$22 |

**SFP is not free.** It costs ~$5/unit more than FBA at current FedEx rates and requires ASP ≥$22 for margin neutrality. Pilot it on high-CVR items where the conversion lift earns back the shipping spend, then either graduate to FBA or retreat to FBM.

---

## 3. The Five Inputs (Data Model)

One unified dataset, five streams, all flowing through the middleware → BigQuery pipeline:

| # | Input | Source → Table | Refresh | Status |
|---|---|---|---|---|
| 1 | FBA inventory state (stock, age, OOS) | SP-API FBA Inventory → `fba_inventory_us` | Weekly | ❌ Blocked (SP-API Inventory role missing) |
| 2 | Demand signal (sessions, units, CVR, 15/15 accel) | SP-API Sales & Traffic → BQ | Daily | ❌ Blocked (Analytics role missing) |
| 3 | FBM twin signal (FBM sales while FBA OOS) | Derived: FBM orders ∩ FBA OOS window | Weekly | ⚠️ Manual until #1 + #2 unblock |
| 4 | License tier (Gold/Silver/Bronze) | This doc, refreshed quarterly | Quarterly | ✅ Current |
| 5 | On-hand inventory (FL warehouse) | Supabase `blank_inventory` → REST API | Real-time | ✅ Current |

> **The P0 gate:** Inputs 1 and 2 require SP-API role grants (Analytics, Inventory, Finance). Waiting on Patrick in PH to add them in Seller Central → Developer Apps. Until then, Unified Score (Section 4) runs on amended CSVs, not live data. See [MIDDLEWARE_PRD_CONSOLIDATED.md §6](~/Documents/Cem%20Vault/02-Projects/amazon-data-analytics/MIDDLEWARE_PRD_CONSOLIDATED.md).

---

## 4. The Unified Score

The three source docs each defined their own scoring model (RSQ, CRS, shipping-template uplift). They don't contradict — they measure the same thing from different angles. Consolidating them:

```
Unified Score =
   Revenue Score       × 0.35   # 30d combined FBA+FBM revenue
 + CVR Score           × 0.25   # Post-Prime-uplift CVR estimate
 + Licence Tier Score  × 0.20   # Gold=10 / Silver=7 / Bronze=3
 + Device Stage Score  × 0.10   # iPhone17=10, 16=7, 15/14/13=5, Samsung=6
 + Acceleration Score  × 0.10   # 15d/15d ratio: >3×=10, 1.5–3×=7, 1–1.5×=5, <1×=2

Component scales (0–10):
  Revenue:       ≥$300=10 / $200–299=8 / $150–199=6 / $100–149=4 / <$100=2
  CVR:           ≥8%=10   / 5–7.9%=8  / 3–4.9%=6   / 2–2.9%=4   / 1–1.9%=2
```

### Decision thresholds

| Score | Channel Action | Queue |
|---|---|---|
| **≥ 7.0** | FBA restock full qty (or FBM→FBA conversion) | RESTOCK |
| **5.0–6.9** | SFP trial OR FBM bridge (pick by stock + ASP) | VALIDATE |
| **3.0–4.9** | FBM only; revisit in 60d | MONITOR |
| **< 3.0** | Suppress FBA; keep FBM live as sensor | CULL |

**Revenue floor gates:** STRONG restocks require ≥$150/mo FBM revenue; MODERATE require ≥$80/mo. This filters out low-price SKUs that pass on unit count alone but don't justify FBA storage.

---

## 5. The 30-Day Action Queue

Every P0/P1 action from all three source docs, deduplicated and ranked:

| # | Priority | Action | Source | Impact | Owner |
|---|---|---|---|---|---|
| 1 | **P0** | Restock 114 T1 OOS SKUs (Naruto/Peanuts/HP iPhone 17 Pro + Harry Potter mats) — ship by 2026-04-17 | FBA SOP | $3,100+/mo | Inventory Ops |
| 2 | **P0** | Ship Naruto Akatsuki Pattern + Itachi Graphic XL mats (#1, #2 FBM twin) | FBM twin | ~£40K/mo | Inventory Ops |
| 3 | **P0** | NY Knicks XL Mat Pad (B0GRPR3GX5) — FBM→FBA, NBA Playoffs window closes May | FBM twin | Seasonal spike | Inventory Ops |
| 4 | **P0** | Fix shipping template on 9,778 US FBM SKUs → Reduced Shipping Template | Shipping SOP | ~$200K/yr | Athena (API script) |
| 5 | **P1** | L4 Surge restock: B0FDW74M1K (Batman mat pad, 8× accel) — 72hr ship | FBA SOP | High | Inventory Ops |
| 6 | **P1** | FC Barcelona iPhone 17 Pro Max restock + iPhone 17/16 PM conversions (3 SKUs) | FBM twin | ~£15K/mo | Inventory Ops |
| 7 | **P1** | SFP pilot: 10 high-CVR FBM candidates (Gilmore Girls 44%, Liverpool 26%, Naruto Bumper 12.2%, Dragon Ball Super iPhone 15 9.5%) | FBM twin | Channel validation | Cem + Hermes |
| 8 | **P1** | Begin 180d+ aged inventory removal orders (~150 SKUs) | FBA SOP | $30+/mo LTSF saved | Inventory Ops |
| 9 | **P2** | WWE cull: 563 → 75 SKUs (keep only the 30 with any 90d sales + 45 strategic) | FBA SOP | Storage + focus | Portfolio Mgr |
| 10 | **P2** | Harry Potter cull: 1,107 → 150 SKUs (concentrate on top-20% revenue) | FBA SOP | Storage + focus | Portfolio Mgr |
| 11 | **P2** | Suppress 5,845 zero-signal dead FBA SKUs (keep FBM live as sensor) | FBM twin | Catalog clarity | Athena (bulk script) |
| 12 | **P3** | Red flag investigation: Naruto Bumper iPhone 16e (B0G589R52C) — 12.2% CVR but 0.2× accel | FBM twin | Protect CVR signal | Hermes |
| 13 | **P3** | Listing audit: Naruto Itachi M Mat (1.9% CVR vs 3.7% XL) + Batman Arkham Knight (2.8% vs 4.2% Arkham Origins) | FBM twin | CVR recovery | Content/Marketing |
| 14 | **P3** | Buy Box audit across all 812 active FBA SKUs | FBA SOP | CVR protection | Inventory Ops |

**Concentration risk flag (FBM twin doc):** 3 of the top 10 FBA restocks are Naruto desk mats. Stagger shipments by 4 weeks to avoid simultaneous aged-inventory exposure if Naruto demand softens.

---

## 6. POD Principles (Framing for Every Decision)

These six principles inform — and constrain — the scoring thresholds and SOPs above. They are the "why" behind the numbers.

1. **80/20 in POD is 95/5.** Print-on-demand catalogs follow power laws more extreme than retail. Harry Potter earns $3,624/mo from a small fraction of 1,107 SKUs; WWE earns $1,009 from 563. **Concentration wins.**
2. **CVR compounds ranking.** A CVR bump earns a ranking bump which earns a traffic bump. Treat CVR as the investment, not the output.
3. **Inventory is the enemy of optionality.** Pre-stock only what you've proven. New launches go FBM day 1, FBA day 14.
4. **Licensing cadence > product cadence.** Align SKU launches to IP events — NBA Playoffs, new anime season, film release — not internal product calendars. This is why NY Knicks at #3 P0 is a time-bound decision.
5. **The 3-SKU rule.** Never hold >3 SKUs in the same licence/device/format combo unless the top one does >5u/30d. Prevents cannibalisation of impressions.
6. **Kill fast, grow slow.** Culls monthly, restocks weekly. Asymmetric update cadence biases the catalog toward winners.

---

## 7. SOPs (Three Unified Procedures)

The five SOPs across the source docs collapse to three. Each replaces 2–3 legacy procedures.

### SOP-A — Weekly Fulfilment Review

- **Frequency:** Mondays, 60 minutes
- **Owner:** Inventory Ops (primary) + Hermes (analysis)
- **Inputs:** The five data streams (§3), previous week's action queue status
- **Replaces:** FBA SOP-01, FBM twin weekly, shipping template weekly monitoring
- **Steps:**
  1. Pull fresh Business Report + FBA Inventory Report + FBA Restock Report from middleware `/api/v1/reports/request-and-wait`
  2. Compute Unified Score for every ASIN with any sales in last 30d
  3. Emit four queues: RESTOCK (≥7.0), VALIDATE (5.0–6.9), MONITOR (3.0–4.9), CULL (<3.0)
  4. For each RESTOCK item: confirm on-hand stock in Supabase FL warehouse → create FBA shipment
  5. For each VALIDATE item: decide SFP trial vs FBM bridge based on ASP (≥$22 SFP / ≥$18 FBM) and 90-day performance
  6. Run 15d/15d acceleration: any ratio >3× with ≥5u = L4 Surge → emergency T1 treatment
  7. Update KPI dashboard (§10); log exceptions
- **Output:** Signed weekly shipment plan, SFP trial additions, KPI delta

### SOP-B — Monthly Portfolio Health

- **Frequency:** First Monday of month, 2–3 hours
- **Owner:** Portfolio Manager + Inventory Ops
- **Replaces:** FBA SOP-02 + SOP-05
- **Steps:**
  1. Pull full FBA Inventory Report; segment by health (Excess / Healthy / Low / OOS)
  2. Run liquidation stage gating on all excess (Stages 1–6 per FBA SOP Pillar 6)
  3. Age review: any SKU >180d → removal order unless Unified Score ≥5.0
  4. Recalculate Gold/Silver/Bronze license tiers based on units/SKU trend (quarterly alternatives)
  5. FBM→FBA conversion scan: any FBM ASIN with Unified Score ≥7.0 and no FBA stock → add to shipment plan
  6. Cull approvals: execute prior month's CULL queue (suppress FBA, keep FBM live)
  7. Update A+ Content tracker for Gold-tier licenses; Vine enrollment for <10 review SKUs
  8. Buy Box audit: any SKU <95% → root-cause + fix
- **Output:** Monthly health memo; updated cull / restock / conversion queues

### SOP-C — Real-Time Escalation (DSEWS + New Launch + Emergency Bridge)

- **Frequency:** Ad-hoc, triggered
- **Owner:** Demand Analyst → Inventory Ops
- **Replaces:** FBA DSEWS alerts (Pillar 5), SOP-04 (new launch), FBM bridge protocols
- **Triggers & actions:**

| Trigger | Level | Response | Timeline |
|---|---|---|---|
| ≥10u in first 15d OR CVR >30% with >50 sessions | L4 Surge | Emergency T1; ship 72hr | Same day |
| ≥5u in first 15d OR >5× accel | L3 Breakout | Unified Score + shipment plan | ≤5 business days |
| New smartphone launch (Apple/Samsung flagship) | N/A | FBM day 1, FBA day 14, top 20 SKUs Gold licenses | 60d lead time |
| T1 OOS + FBA ETA >7d + stock on hand + ASP ≥$18 | Bridge | Activate FBM listing until FBA receives stock | Immediate |
| Major licence event (film/season/controversy) | N/A | Pull affected SKUs from cull queue; re-score | Within 24h |
| FBM twin 5× accel in 14d | Bridge → Convert | Same-day FBA conversion evaluation | Same day |

---

## 8. Marketplace Overlays

The core strategy is shared. These are the deltas.

### 8.1 US (Primary)

- **FBM uplift lever:** Reduced Shipping Template (2-day FedEx $10.99) → +25% CVR proven
- **SFP:** Pilot 10 high-CVR candidates starting here
- **Blocker:** 9,778 SKUs currently on wrong template — P0 #4 fixes this
- **Data:** Shipping template column lands in BQ on Monday 2026-04-20 first run (after cron update 2026-04-14); until then, shipping template analysis uses manually amended CSVs — see [SOP_SHIPPING_TEMPLATE_OPTIMIZATION.md §1.1](~/Documents/Cem%20Vault/02-Projects/amazon-data-analytics/SOP_SHIPPING_TEMPLATE_OPTIMIZATION.md)

### 8.2 UK (Secondary)

- **FBM uplift lever:** Nationwide Prime (Seller-Fulfilled Prime, next-day, Prime badge) replaces US shipping template logic
- **Data gap:** No current analysis. Run equivalent of FBM twin analysis against UK listings table once middleware UK sync completes
- **Action:** Phase 2 — after US execution stabilises (target 2026-05-15)

### 8.3 DE / FR / IT / ES (Tertiary)

- Data pipeline exists (listings table for DE, others pending)
- No strategy analysis yet
- **Phase 3** — earliest 2026-Q3
- Single action for now: ensure shipping template column lands in BQ for all 6 marketplaces

---

## 9. Known Gaps & Blockers

Honest inventory of what prevents full execution today:

| Gap | Impact | Unblock |
|---|---|---|
| SP-API Analytics role missing | 12 cron jobs blocked (Sales & Traffic all 6 marketplaces × 14d+30d) | Patrick (PH) adds in Seller Central → Developer Apps |
| SP-API Inventory role missing | 4 FBA report jobs blocked | Same |
| SP-API Finance role missing | 6 Settlement jobs blocked | Same |
| Ads API secrets empty (×6) | Cannot automate Sponsored Products (Pillar 7 of FBA SOP) | Populate from Amazon Ads console |
| Shipping template column first run | Manual CSV workaround until 2026-04-20 | Automatic — already scheduled |
| FBA Management App not built | No operator UI for this strategy — all flows are CLI/notebook for now | Build per [FBA_Management_App_Project_Brief.md](~/Desktop/Repos/Claude%20Code%20FBA/FBA_Management_App_Project_Brief.md) |
| UK/DE strategy analysis | FBM twin + Unified Score models not run against non-US data | Phase 2 post-US stabilisation |

---

## 10. Success Metrics (90-Day Review)

| KPI | Baseline | 90d Target | Source Doc |
|---|---|---|---|
| Active FBA SKU count | 812 | ≤720 | FBA SOP |
| Portfolio-wide units/SKU | ~0.16 | ≥0.22 | FBA SOP |
| Catalog-wide CVR | 0.57% | ≥1.0% | FBA SOP |
| Shipping-template-wrong SKUs (US FBM) | 9,778 | 0 | Shipping SOP |
| FBM twin STRONG restocks actioned | 0 of 33 | 33 of 33 | FBM twin |
| FBM twin MODERATE restocks actioned | 0 of 151 | ≥100 | FBM twin |
| SFP trial candidates live | 0 | ≥10 | This doc |
| Monthly FBA storage cost | $151 | <$120 | FBA SOP |
| WWE active SKU count | 563 | ≤75 | FBA SOP |
| Harry Potter active SKU count | 1,107 | ≤150 | FBA SOP |
| Incremental monthly revenue | $0 | ≥£40K | Composite |
| Mean L3/L4 alert → FBA ship time | unknown | ≤5 business days | FBA SOP |

### Leading indicators (weekly)

- T1 OOS SKU count (target: <10 at any point after Week 2)
- Unified Score RESTOCK queue depth (target: zero items aging >7d)
- Unified Score CULL queue throughput (target: ≥100/week sustained)
- FBM twin signal refresh timeliness (target: ≤24h after weekly pull)

---

## 11. Implementation Sequence (Concrete First 14 Days)

Because the P0 queue has too many items to run in parallel, sequence them:

| Day | Focus | Owner | Gate |
|---|---|---|---|
| 1 (Apr 15) | Emergency T1 OOS restocks (#1, #2, #3) — paper shipments today | Inventory Ops | Stock on hand confirmed in Supabase |
| 2–3 | Ship P0 #1–3 to FBA; activate FBM bridges where FBA ETA >7d | Inventory Ops | Carrier picked |
| 4–5 | L4 Surge restock (#5 Batman mat) | Inventory Ops | 72hr window |
| 6–7 | Shipping template API script — test on 50 SKUs | Athena | Manual test confirms template name |
| 8–10 | Shipping template rollout — wave 1 (1,000 SKUs, highest revenue) | Athena | Script stable |
| 11–14 | SFP pilot setup: 10 candidates enrolled, before/after tracking live | Cem + Hermes | Amazon SFP trial approval |

Days 15–30: complete shipping template rollout, begin P2 cull (WWE + HP), run first SOP-A at scale on 2026-04-20 after Sales & Traffic pipeline unblocks.

---

## 12. What This Strategy Explicitly Rejects

- **"Restock everything that's OOS."** ~5,845 dead FBA SKUs have zero demand signal. Restocking any of them is a margin drain.
- **"Convert all FBM to FBA."** FBM is the demand sensor. Keeping 5,845+ long-tail FBM listings live costs nothing and catches future demand spikes automatically.
- **"SFP for every FBM item."** SFP costs ~$5/unit more than FBA. Only high-CVR items earn that back. Pilot before scale.
- **"Build more SKUs."** The FBA SOP's finding is unambiguous: the problem is concentration, not catalog size. Harry Potter at 1,107 SKUs generates less per-SKU than Dragon Ball at 45. New SKU development is gated at Gold-tier licenses on iPhone 17 only.
- **"Blanket discount excess inventory."** The 6-stage liquidation protocol (FBA SOP Pillar 6) gates discounting by license tier and CVR — Gold-tier SKUs with CVR >10% never hit Outlet.

---

## 13. Next Document Update

- **2026-05-15:** Post-first-30-days retrospective. Update Unified Score weights based on actuals. Calibrate FBA uplift multiplier (currently assumed 2.0× FBM floor, conservative).
- **2026-07-15:** 90-day full review against Section 10 KPIs. Re-tier licenses.
- **2026-10-15:** Phase 2 scope — UK analysis complete. iPhone 18 launch protocol execution review.

---

*End of strategy. For detail on any component, follow the source doc citations at the top of this file.*
