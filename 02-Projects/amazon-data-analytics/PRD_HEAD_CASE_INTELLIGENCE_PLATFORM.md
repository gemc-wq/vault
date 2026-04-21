# PRD: Head Case Intelligence Platform

**Version:** 1.0 DRAFT  
**Created:** 2026-04-15  
**Owner:** Cem Celikkol  
**Status:** DRAFT — awaiting Cem review

---

## 1. What This Is

One system. One SKU view. One action queue.

Every SKU across every marketplace has one row with every dimension populated: stock, pricing, template, fulfillment, demand, creative coverage, and a composite score. The system continuously analyses, recommends actions, and — with human approval — executes them.

It replaces: the shipping template fixer, the listing edit app, the pricing optimizer, the FBA conversion tool, the procurement/inventory app, and the weekly manual analysis cycle. Not five apps. One platform.

---

## 2. Design Principles

| # | Principle | Implication |
|---|-----------|-------------|
| 1 | **One system, not a bunch of apps** | Every new capability is a module in this platform, not a new repo. |
| 2 | **Fix all processes when you touch one** | Changing a shipping template triggers: is the price right? Is inventory sufficient? Is FBA better? Should we restock? |
| 3 | **Marketplace isolation is sacred** | US, UK, DE never share a table row. Every query, every join, every output is marketplace-scoped. |
| 4 | **Zero is legacy — read from it, don't extend it** | Strangler fig pattern. Build independently, sync data via BQ, replace Zero functions over time. |
| 5 | **AI recommends, human decides** | The system proposes. Cem approves. No autonomous execution on live listings or pricing. |
| 6 | **Self-learning loop** | Every action's outcome feeds back into the scoring weights. The system gets smarter every week. |

---

## 3. Architecture

```
MARKETPLACES                           ZERO (Legacy)
Amazon US/UK/DE/FR/IT/ES               PHP/Apache, AWS
Walmart, GoHeadCase                    Orders, labels, POs,
     │                                 print files, tracking
     │ SP-API reports                        │
     │ (via middleware)                      │ BQ replication
     ▼                                      ▼
┌──────────────────────────────────────────────┐
│            DATA LAYER                         │
│                                               │
│  BigQuery (warehouse)                         │
│  ├── amazon_reports.*        ← SP-API data    │
│  ├── zero_dataset.orders     ← Zero sync      │
│  ├── headcase.*              ← product master  │
│  └── hcip.unified_sku_view   ← THE VIEW       │
│                                               │
│  Supabase (operational DB)                    │
│  ├── blank_inventory         ← stock levels   │
│  ├── orders                  ← order history  │
│  ├── sku_scores              ← scoring output │
│  ├── action_queue            ← what to do     │
│  └── action_log              ← what was done  │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│          INTELLIGENCE LAYER                   │
│                                               │
│  Scoring Engine                               │
│  ├── Template score   (correct template?)     │
│  ├── Price score      (room to optimise?)     │
│  ├── Inventory score  (stock vs demand?)      │
│  ├── Fulfillment score (FBA/SFP candidate?)   │
│  ├── Demand score     (trending? sessions?)   │
│  ├── Creative score   (design coverage gap?)  │
│  └── Composite score  (weighted total)        │
│                                               │
│  Action Generator                             │
│  → For each SKU: what's the highest-impact    │
│    action? Fix template? Raise price?         │
│    Restock? Convert to FBA? Cull? Brief       │
│    creative team?                             │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│          ACTION LAYER                         │
│                                               │
│  Action Queue (one queue, priority-sorted)    │
│  ├── FIX_TEMPLATE    → SP-API feed/patch      │
│  ├── ADJUST_PRICE    → SP-API listings patch  │
│  ├── CONVERT_FBA     → FBA inbound shipment   │
│  ├── RESTOCK         → PO to supplier         │
│  ├── CULL            → Close/suppress listing  │
│  ├── BRIEF_CREATIVE  → Design brief to PH     │
│  └── LAUNCH_SFP      → SFP enrollment         │
│                                               │
│  Workflow: Score → Propose → Preview →        │
│            Approve (Cem) → Execute → Verify   │
│                                               │
│  Every action logged to action_log            │
│  Every outcome measured after 14 days         │
│  Results feed back into scoring weights       │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│          LEARNING LAYER                       │
│                                               │
│  14-day attribution window                    │
│  Compare: pre-action metrics vs post-action   │
│  ├── CVR changed?                             │
│  ├── Revenue changed?                         │
│  ├── Sessions changed?                        │
│  └── Buy Box %?                               │
│                                               │
│  Update scoring weights based on outcomes     │
│  Surface patterns to creative team            │
│  "HB401 Naruto on iPhone 17 = best seller"   │
│  "Peanuts on Samsung underperforms by 40%"    │
│  → Generate creative briefs automatically     │
└──────────────────────────────────────────────┘
```

---

## 4. The Unified SKU View

One row per SKU per marketplace. This is the foundation.

### 4.1 Schema

```sql
CREATE TABLE hcip.unified_sku (
    -- Identity
    sku                     STRING NOT NULL,     -- Full SKU: HTPCR-IPH17PMAX-NARUICO-AKA
    marketplace             STRING NOT NULL,     -- US, UK, DE, FR, IT, ES
    asin                    STRING,

    -- Parsed SKU components
    product_type            STRING,              -- HTPCR, HB401, HLBWH, etc.
    device_code             STRING,              -- IPH17PMAX, S25ULTRA, etc.
    design_code             STRING,              -- NARUICO, PNUTCHA, etc.
    variant                 STRING,              -- AKA, CLR, etc.
    base_sku                STRING,              -- product_type + device (inventory match key)
    is_fba                  BOOLEAN,             -- F-prefix detection

    -- Listing data (from Active Listings report)
    item_name               STRING,
    price                   FLOAT64,
    quantity                INT64,
    fulfillment_channel     STRING,              -- AMAZON_NA / DEFAULT / AMAZON_EU
    shipping_template       STRING,              -- Current template name
    listing_status          STRING,              -- Active / Inactive

    -- Performance data (from Business Report — 90 day)
    sessions_90d            INT64,
    units_90d               INT64,
    conversion_rate         FLOAT64,             -- Unit Session Percentage
    revenue_90d             FLOAT64,             -- Ordered Product Sales
    buy_box_pct             FLOAT64,             -- Featured Offer %

    -- Inventory (from Supabase blank_inventory)
    stock_fl                INT64,               -- Florida warehouse
    stock_uk                INT64,               -- UK warehouse
    stock_ph                INT64,               -- Philippines warehouse
    stock_total             INT64,               -- Sum of all locations
    has_required_stock      BOOLEAN,             -- Stock in correct warehouse for marketplace

    -- Fulfillment analysis
    has_fba_twin            BOOLEAN,             -- Does an FBA version exist?
    fba_twin_sku            STRING,              -- The FBA SKU if it exists
    fba_twin_sessions       INT64,               -- FBA twin's sessions (for comparison)
    fba_twin_cvr            FLOAT64,             -- FBA twin's conversion rate

    -- Orders analysis (from orders data — for SFP)
    secondday_orders_90d    INT64,               -- Orders with ship-service-level=SecondDay
    shipping_revenue_90d    FLOAT64,             -- What customers paid for shipping

    -- Creative coverage
    design_count_this_device INT64,              -- How many designs exist for this device?
    design_revenue_rank     INT64,               -- This design's revenue rank (1=top)
    device_has_coverage_gap BOOLEAN,             -- Fewer designs than top devices?

    -- Scores (0-100 each)
    score_template          FLOAT64,             -- 0=correct, 100=wrong+high impact
    score_price             FLOAT64,             -- 0=optimal, 100=strong optimisation opportunity
    score_inventory         FLOAT64,             -- 0=well stocked, 100=urgent restock
    score_fulfillment       FLOAT64,             -- 0=optimal channel, 100=should convert FBA/SFP
    score_demand            FLOAT64,             -- 0=declining, 100=surging
    score_creative          FLOAT64,             -- 0=well covered, 100=major gap
    score_composite         FLOAT64,             -- Weighted total

    -- Recommended action
    recommended_action      STRING,              -- FIX_TEMPLATE, ADJUST_PRICE, RESTOCK, etc.
    action_priority         INT64,               -- 1=highest
    action_detail           STRING,              -- e.g. "Change to Reduced Shipping Template"
    estimated_revenue_impact FLOAT64,            -- $ impact if action taken

    -- Metadata
    scored_at               TIMESTAMP,
    data_freshness          TIMESTAMP,           -- Oldest data source used

    PRIMARY KEY (sku, marketplace)
);
```

### 4.2 Data Sources Mapped to Columns

| Column Group | Source | Refresh |
|-------------|--------|---------|
| Identity + Parsed SKU | Active Listings report | Weekly (Monday cron) |
| Listing data | Active Listings report | Weekly |
| Performance | Business Report (manual download) | Weekly |
| Inventory | Supabase `blank_inventory` | Real-time |
| Fulfillment analysis | Computed: cross-reference FBA/FBM twins in listings | Weekly |
| Orders / SFP | Orders report (manual download) | Monthly |
| Creative coverage | Computed: count designs per device from listings | Weekly |
| Scores | Computed by scoring engine | After each data refresh |

### 4.3 Marketplace Isolation

```sql
-- EVERY query includes marketplace filter. No exceptions.
-- Views are per-marketplace for safety:

CREATE VIEW hcip.sku_us AS
SELECT * FROM hcip.unified_sku WHERE marketplace = 'US';

CREATE VIEW hcip.sku_uk AS
SELECT * FROM hcip.unified_sku WHERE marketplace = 'UK';

CREATE VIEW hcip.sku_de AS
SELECT * FROM hcip.unified_sku WHERE marketplace = 'DE';
```

---

## 5. Scoring Engine

### 5.1 Template Score (0-100)

```
IF shipping_template = correct_template_for_marketplace:
    score = 0
ELSE IF has_required_stock AND sessions_90d > 0:
    score = 80 + (revenue_90d_percentile * 20)  -- Wrong template + active + stocked = urgent
ELSE IF NOT has_required_stock:
    score = 20  -- Wrong template but no stock to fulfill anyway
ELSE:
    score = 40  -- Wrong template, no sessions (low priority)
```

Correct templates:
- US: `Reduced Shipping Template`
- UK: `Nationwide Prime`
- DE: `Reduced Shipping Template`

### 5.2 Price Score (0-100)

```
-- High CVR + not at price ceiling = opportunity to increase
-- Low CVR + high price = reduce or fix listing

IF conversion_rate > marketplace_median_cvr * 1.5:
    -- Converting well above average — room to raise price
    headroom = (price_ceiling[product_type] - price) / price_ceiling[product_type]
    score = headroom * 100
ELSE IF conversion_rate < marketplace_median_cvr * 0.5 AND price > price_floor[product_type]:
    -- Converting poorly and price is high — consider reduction
    score = 70
ELSE:
    score = 20  -- Price is probably fine
```

Price ranges (US):

| Product Type | Floor | Ceiling | Current Typical |
|-------------|-------|---------|----------------|
| HB401 | $17.95 | $24.95 | $19.95 |
| HTPCR | $7.95 | $16.95 | $9.95-$14.95 |
| HLBWH | $19.95 | $34.95 | $24.95-$29.95 |
| HC | $7.95 | $12.95 | $9.95 |
| HDMWH | $24.95 | $39.95 | $29.95 |
| HSTWH | $3.95 | $12.95 | $4.95-$9.95 |

**NOTE:** These ranges need Cem's confirmation. Floors and ceilings are estimates based on observed data.

### 5.3 Inventory Score (0-100)

```
IF stock_total = 0 AND sessions_90d > 100:
    score = 100  -- Out of stock with demand = critical
ELSE IF stock_total < (units_90d / 3):  -- Less than 1 month supply
    score = 80
ELSE IF stock_total < units_90d:  -- Less than 3 months supply
    score = 50
ELSE:
    score = 10  -- Well stocked
```

### 5.4 Fulfillment Score (0-100)

```
IF is_fba:
    score = 0  -- Already FBA, nothing to optimise
ELSE IF has_fba_twin AND fba_twin_cvr > conversion_rate * 1.3:
    score = 90  -- FBA twin converts 30%+ better — should be FBA
ELSE IF secondday_orders_90d > 10:
    score = 70  -- Customers paying for speed — SFP candidate
ELSE IF shipping_template != correct_template:
    score = 50  -- At minimum fix the template
ELSE:
    score = 10
```

### 5.5 Demand Score (0-100)

```
-- Compare recent 30d sessions vs 90d average
recent_daily = sessions_30d / 30
average_daily = sessions_90d / 90

IF recent_daily > average_daily * 1.5:
    score = 90  -- Surging demand
ELSE IF recent_daily > average_daily * 1.1:
    score = 70  -- Growing
ELSE IF recent_daily > average_daily * 0.9:
    score = 50  -- Stable
ELSE IF recent_daily > average_daily * 0.5:
    score = 30  -- Declining
ELSE:
    score = 10  -- Dying
```

### 5.6 Creative Score (0-100)

```
-- How many designs does this device have vs the top device?
top_device_designs = MAX(design_count_this_device) across all devices for this product_type
coverage_ratio = design_count_this_device / top_device_designs

IF coverage_ratio < 0.3 AND demand_score > 70:
    score = 100  -- Hot device with few designs = huge gap
ELSE IF coverage_ratio < 0.5:
    score = 60
ELSE IF coverage_ratio < 0.8:
    score = 30
ELSE:
    score = 5  -- Well covered
```

### 5.7 Composite Score

```
composite = (
    score_template    * 0.25 +   -- 25% — direct CVR impact
    score_price       * 0.20 +   -- 20% — margin impact
    score_inventory   * 0.20 +   -- 20% — availability
    score_fulfillment * 0.15 +   -- 15% — delivery experience
    score_demand      * 0.10 +   -- 10% — growth signal
    score_creative    * 0.10     -- 10% — coverage gap
)
```

Weights are initial estimates. The learning layer adjusts them based on which actions produce the best outcomes.

---

## 6. Action Queue

### 6.1 Schema

```sql
CREATE TABLE action_queue (
    id                  UUID PRIMARY KEY,
    sku                 TEXT NOT NULL,
    marketplace         TEXT NOT NULL,
    action_type         TEXT NOT NULL,    -- FIX_TEMPLATE, ADJUST_PRICE, RESTOCK, etc.
    action_detail       JSONB,           -- Specific parameters
    priority            INT,             -- 1=highest
    composite_score     FLOAT,
    estimated_impact    FLOAT,           -- Revenue $ impact
    status              TEXT DEFAULT 'proposed',  -- proposed → approved → executing → done → verified
    proposed_at         TIMESTAMP DEFAULT now(),
    approved_at         TIMESTAMP,
    approved_by         TEXT,            -- Always 'cem' for now
    executed_at         TIMESTAMP,
    verified_at         TIMESTAMP,
    outcome             JSONB,           -- Pre/post metrics after 14 days
    created_at          TIMESTAMP DEFAULT now()
);
```

### 6.2 Action Types

| Action | Trigger | Execution Method | Approval |
|--------|---------|-----------------|----------|
| `FIX_TEMPLATE` | score_template > 60 | SP-API flat file feed | Batch approval (100+ at a time) |
| `ADJUST_PRICE` | score_price > 60 | SP-API listings patch | Per-SKU or batch with preview |
| `CONVERT_FBA` | score_fulfillment > 80 | Manual (create FBA shipment) | Per-SKU |
| `LAUNCH_SFP` | secondday_orders > 10 | SP-API SFP enrollment | Batch |
| `RESTOCK` | score_inventory > 70 | PO generation (→ Zero or new system) | Batch |
| `CULL` | sessions_90d = 0 AND stock = 0 AND age > 180d | SP-API listing delete/close | Batch with review |
| `BRIEF_CREATIVE` | score_creative > 80 AND score_demand > 60 | Brief to PH creative team | Weekly digest |

### 6.3 Workflow

```
SCORING ENGINE runs weekly (after data refresh)
  → Populates action_queue with proposed actions
  → Sorted by estimated_impact DESC

CEM reviews in UI:
  → Filter by action_type, marketplace, priority
  → Preview: "These 847 SKUs need template fix. Est. impact: $180K/year"
  → Approve batch or individual items
  → Hit "Execute"

SYSTEM executes approved actions:
  → FIX_TEMPLATE: generates flat file feed, submits to SP-API
  → ADJUST_PRICE: patches via SP-API Listings Items
  → BRIEF_CREATIVE: compiles brief, sends to PH team
  → Logs everything to action_log

14 DAYS LATER:
  → System pulls fresh performance data
  → Compares pre vs post for every executed action
  → Calculates: did CVR improve? Did revenue change?
  → Updates scoring weights if pattern detected
```

---

## 7. One UI

Not five dashboards. One interface with tabs/views.

```
┌──────────────────────────────────────────────────────────┐
│  HEAD CASE INTELLIGENCE PLATFORM         [US ▼] [UK] [DE]│
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [Dashboard] [Action Queue] [SKU Explorer] [Learning]    │
│                                                          │
├── DASHBOARD ─────────────────────────────────────────────┤
│                                                          │
│  Actions Pending: 1,247    Approved Today: 0             │
│  Est. Revenue Impact: $340K/year                         │
│                                                          │
│  By Type:                                                │
│  ├── Fix Template:    847  ($180K impact)                │
│  ├── Adjust Price:    203  ($95K impact)                 │
│  ├── Restock:          89  ($42K impact)                 │
│  ├── Convert FBA:      62  ($18K impact)                 │
│  ├── Brief Creative:   31  (coverage gap)                │
│  └── Cull:             15  (dead SKUs)                   │
│                                                          │
│  Learning: Last batch +22% CVR avg (14d attribution)     │
│                                                          │
├── ACTION QUEUE ──────────────────────────────────────────┤
│                                                          │
│  Filter: [All Types ▼] [Priority ▼] [Score > 60 ▼]      │
│                                                          │
│  [☐ Select All]  [Approve Selected]  [Preview]           │
│                                                          │
│  ☐ │ P1 │ FIX_TEMPLATE │ HSTWH-L-WWE2JCEN │ Score: 94  │
│  ☐ │ P2 │ ADJUST_PRICE │ HB401-IPH17P-NAR │ Score: 88  │
│  ☐ │ P3 │ FIX_TEMPLATE │ HLBWH-IPH17-HPOT │ Score: 85  │
│  ☐ │ P4 │ RESTOCK      │ HTPCR-IPH17P-DRG │ Score: 82  │
│    │ ...                                                 │
│                                                          │
├── SKU EXPLORER ──────────────────────────────────────────┤
│                                                          │
│  Search: [____________]  or filter by:                   │
│  Product Type [▼]  Device [▼]  Design [▼]  Template [▼] │
│                                                          │
│  SKU: HTPCR-IPH17PMAX-NARUICO-AKA                       │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Price: $14.95  │ CVR: 3.8%  │ Sessions: 1,250  │     │
│  │ Stock: FL=45   │ Template: Default (WRONG)      │     │
│  │ FBA twin: Yes  │ FBA CVR: 5.2% (+37%)          │     │
│  │ Scores: Template=94 Price=45 Inventory=30       │     │
│  │ Action: FIX_TEMPLATE (Priority 1)               │     │
│  └─────────────────────────────────────────────────┘     │
│                                                          │
├── LEARNING ──────────────────────────────────────────────┤
│                                                          │
│  Last 30 days: 342 actions executed                      │
│  ├── Template fixes:  +25% CVR average                   │
│  ├── Price increases: +8% revenue, -2% units             │
│  ├── FBA conversions: +37% CVR average                   │
│  └── Creative briefs: 12 new designs launched            │
│                                                          │
│  Weight adjustments:                                     │
│  Template weight: 0.25 → 0.28 (high impact confirmed)   │
│  Creative weight: 0.10 → 0.08 (slower ROI than expected) │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 8. Data Pipeline (Ingestion)

One pipeline. Handles all file types. Tags marketplace. Detects changes.

```python
# Pseudocode — single entry point for all data

def ingest(source, marketplace):
    """
    source: file path, SP-API report type, or 'supabase'
    marketplace: US, UK, DE (required, never inferred)
    """
    # 1. Load (handles TSV, CSV, encoding, chunking)
    raw = load_file(source, marketplace)

    # 2. Tag marketplace immediately
    raw['marketplace'] = marketplace

    # 3. Parse SKUs
    raw = parse_skus(raw)  # Adds product_type, device, design, variant, is_fba, base_sku

    # 4. Hash for delta detection
    raw['row_hash'] = raw.apply(compute_hash, axis=1)

    # 5. Detect changes vs previous snapshot
    changes = detect_delta(raw, marketplace)  # new, changed, removed SKUs

    # 6. Load to BigQuery (marketplace-scoped table)
    load_to_bq(raw, f'hcip.listings_{marketplace.lower()}')

    # 7. Update unified_sku view
    refresh_unified_sku(marketplace)

    # 8. Re-score changed SKUs
    rescore(changes, marketplace)

    return changes
```

---

## 9. Where It Lives

| Component | Location | Why |
|-----------|----------|-----|
| Data warehouse | BigQuery (`instant-contact-479316-i4`) | Already has 4.08M rows, scales infinitely, $0 at rest |
| Operational DB | Supabase | Already has inventory, orders, experiment tables. Real-time API. |
| Scoring engine | Python on Mac Studio (cron) or Cloud Function | Runs weekly after data refresh |
| Action execution | SP-API via middleware (Cloud Run) | Already deployed, handles auth |
| UI | Web app (single page) | TBD: extend existing sales dashboard or new |
| Agent orchestration | ZEUS (Mac Studio) | Athena coordinates, delegates analysis |

---

## 10. Build Phases

| Phase | What | Delivers | Effort |
|-------|------|----------|--------|
| **1** | Unified SKU table + ingestion pipeline | One view of every SKU with parsed components, stock levels, and performance data. Foundation for everything else. | 1-2 weeks |
| **2** | Scoring engine + template score | Score every SKU. Execute shipping template fixes (9,778 US SKUs ready). First measurable win (~$200K/year). | 1 week |
| **3** | Action queue + approval UI | One queue, one UI. Cem can review and approve batches. Replaces manual CSV review. | 1-2 weeks |
| **4** | Price + inventory + fulfillment scores | Full scoring across all dimensions. Actions for pricing, restocking, FBA conversion. | 2 weeks |
| **5** | Learning layer | 14-day attribution. Automatic weight adjustment. System gets smarter. | 1 week |
| **6** | Creative intelligence | Gap detection → automatic briefs. "Design Naruto for iPhone 17 HB401." Closes the loop back to PH creative team. | 2 weeks |

---

## 11. What Dies

| Kill | Why |
|------|-----|
| Hermes's standalone Flask listing edit app plan | Replaced by Action Queue + UI |
| Separate pricing optimizer app | Replaced by Price Score + Action Queue |
| Separate FBA conversion tool | Replaced by Fulfillment Score + Action Queue |
| Separate procurement/inventory app | Replaced by Inventory Score + Restock action |
| Multiple analysis Python scripts | Replaced by Scoring Engine |
| Weekly manual CSV analysis | Replaced by automated scoring + dashboard |

---

## 12. Blockers

| Blocker | Impact | Owner | Status |
|---------|--------|-------|--------|
| SP-API write scope | Can't execute template/price changes via API | Patrick (PH) | Waiting |
| Middleware repo on Mac Studio | Can't modify middleware from here | Cem (scp) | Waiting |
| `custom=true` cron verification | No shipping template data in BQ until Apr 20 | Automated | Monday |
| Price floors/ceilings confirmation | Scoring engine needs real bounds per product type | Cem | Not started |
| Licence tier rankings | Pricing engine needs tier definitions | Cem | Not started |
| Zero data flow documentation | ~~Need to understand BQ replication from Zero~~ | ~~Cem~~ | **RESOLVED** — see Section 15 |

---

## 13. DelegAIt Product Opportunity

This entire platform — unified SKU view, scoring engine, action queue, learning loop — is marketplace-agnostic and seller-agnostic. Any Amazon seller doing $1M+ with 10K+ SKUs faces the same problems:

- Wrong shipping templates losing conversion
- Suboptimal pricing leaving money on the table
- Manual analysis that doesn't scale
- No feedback loop from execution to creative

**DelegAIt product:** "Amazon Intelligence Platform" — $999-$2,500/mo depending on SKU count. Customer #1 = Ecell Global. Build for us, productize for everyone.

---

## 14. Success Metrics

| Metric | Baseline (Apr 2026) | Target (Jul 2026) |
|--------|--------------------|--------------------|
| SKUs on correct template | ~75% (est.) | 99% |
| Time to identify + fix template issue | Weeks (manual) | < 24 hours (automated) |
| Pricing experiments running | 0 | 10+ concurrent |
| Revenue from template fixes | $0 | $200K/year run rate |
| Actions proposed per week | 0 (manual) | 500+ (automated scoring) |
| Creative briefs from data | 0 | 5/week |
| Time from insight to action | Days-weeks | Same day |

---

## 15. Zero Infrastructure Map

**Source:** `barcode.php` analysis + Marketplace DB Routing Report (March 2026)

### 15.1 Server Topology

| Server | IP / Endpoint | Role | Database(s) |
|--------|---------------|------|-------------|
| **Aurora RDS (Production)** | `cluster.cluster-cvaofazjtifp.us-east-1.rds.amazonaws.com` | Primary write target for ALL crons and marketplace scripts | `elcell_co_uk_barcode` (main), `elcell_co_uk`, `elcell_co_uk_time` |
| **Clone Server** | `192.168.20.160` | Product/design data reads (read-only for most scripts) | `headcase`, `cfxb2b_db`, `variation-exporter` |
| **US Server** | `192.168.20.66` | US-specific routing (bar_us mode) | `elcell_co_uk_barcode` |
| **AU Server** | `192.168.20.173` | AU-specific routing (bar_au mode) | `elcell_co_uk_barcode` |
| **Sage MSSQL** | `192.168.20.74` / `52.200.143.9` | Accounting integration | Sage databases |
| **Local PHP/Apache** | `192.168.20.57` | Zero application code | N/A |
| **Cloud PHP/Apache** | `34.196.137.61` | Zero cloud mirror | N/A |

### 15.2 Database Routing Logic (barcode.php)

```
CLI / Cron → defaults to sage_2013 profile → Aurora RDS
Web request → routes by SERVER_NAME or cookie:
  bar_uk  → Aurora RDS
  bar_us  → 192.168.20.66
  bar_au  → 192.168.20.173
```

- `PointDBLock.lock` file provides manual failover mechanism
- Uses deprecated `mysql_connect()` (not mysqli) — confirms legacy status
- Credentials: hardcoded in PHP (user=`elcell`) — typical of 15-year-old systems

### 15.3 BQ Replication (Already Exists)

| BQ Dataset | Source | Contains | Status |
|------------|--------|----------|--------|
| `elcell_co_uk_barcode` | Aurora RDS (main DB) | Orders, production, inventory, labels, tracking | **LIVE** — needs column verification |
| `headcase` | Clone server (192.168.20.160) | Product master, design data, device mappings | **LIVE** — needs column verification |

**Key finding:** The BQ sync from Aurora RDS already exists. The Intelligence Platform's data layer does NOT need to build a new Zero→BQ pipeline. It needs to:
1. Verify these datasets have the columns the unified SKU view requires
2. Confirm refresh frequency (target: daily or better)
3. Build the join logic from Zero data + SP-API data → unified SKU table

### 15.4 What the Platform Reads from Zero

| Data Need | Zero Table (likely) | BQ Dataset | Used By |
|-----------|-------------------|------------|---------|
| Order history | `orders` / `order_items` | `elcell_co_uk_barcode` | SFP analysis, demand scoring |
| Production status | `production_*` | `elcell_co_uk_barcode` | Fulfillment scoring |
| Product master | `products` / `designs` | `headcase` | SKU parsing, creative coverage |
| Inventory levels | Via Supabase `blank_inventory` | N/A (Supabase direct) | Inventory scoring |

### 15.5 What the Platform Does NOT Do with Zero

- ❌ Write to Zero databases
- ❌ Extend Zero PHP code
- ❌ Add new tables to Aurora RDS
- ❌ Modify barcode.php routing

Zero is read-only for this platform. Strangler fig: new capabilities built in BQ + Supabase + SP-API. Zero eventually loses functions, never gains them.

---

## 16. Remaining Open Items

| Item | Owner | Priority | Notes |
|------|-------|----------|-------|
| Price floors/ceilings per product type | Cem | P1 | Scoring engine needs real bounds |
| Licence tier rankings (T1/T2/T3) | Cem | P1 | Pricing engine tier multipliers |
| BQ dataset column verification | Athena/Hermes | P1 | Confirm `elcell_co_uk_barcode` and `headcase` have needed columns |
| BQ sync refresh frequency | Athena/Hermes | P2 | Confirm daily or better |
| SP-API write scope | Patrick (PH) | P0 | Blocks all execution actions |
| Middleware repo transfer | Cem | P2 | scp from MacBook to Mac Studio |
| `custom=true` cron verification | Automated | P2 | First run Apr 20 — check shipping template in BQ |

---

**Document Version:** 1.1 DRAFT  
**Next Step:** Cem review → confirm price ranges, licence tiers → verify BQ columns → Phase 1 build
