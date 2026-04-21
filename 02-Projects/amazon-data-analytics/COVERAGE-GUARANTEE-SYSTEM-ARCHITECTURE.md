# Coverage Guarantee System: Architecture Brief

**Author:** Athena + Cem | **Date:** 2026-04-11 | **Status:** DRAFT — For LLM Council Review
**North Star:** Every champion design listed on every target device × product type × marketplace. No gaps. No guessing.

---

## The Problem

Coverage is currently a hope, not a guarantee. The Philippines team decides what gets listed, with no systematic oversight. Result:

- **15% of listings** on wrong shipping template ($37.5K/mo revenue loss)
- **4 pricing failures** found today (FBA priced lower than FBM)
- **Unknown device coverage gaps** (iPhone 17 Pro buyers 108% more likely to pay premium — are we listed?)
- **No delta monitoring** — Cem can't see what changed week to week
- **PH accuracy unknown** — EOD reports not validated against actual listings

**Root cause:** Humans decide what to list. The system should decide. Humans should execute.

---

## The Architecture: Three Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    COVERAGE GUARANTEE SYSTEM                     │
│                                                                  │
│  LAYER 1: GENERATE (Blueprint V3)                               │
│  ─────────────────────────────────                              │
│  Trigger: New design image uploaded to S3                        │
│      ↓                                                           │
│  SKU Matrix: design × 6 devices × 5 product types = 30+ SKUs    │
│  Price Rules: FBM=$19.95, FBA=$25.95 (by product type)          │
│  Content: Echo generates titles, bullets, descriptions           │
│  Shipping: Auto-assign Reduced (US) / Prime (UK) at creation    │
│  Upload: SP-API (Amazon), Shopify API, Codisto (Walmart)        │
│                                                                  │
│  LAYER 2: MONITOR (Listings Intelligence)                       │
│  ────────────────────────────────────────                       │
│  Weekly: Active Listings Report delta (what changed?)            │
│  Weekly: Price integrity audit (FBA/FBM pairs correct?)          │
│  Weekly: Shipping template compliance (100% target)              │
│  Weekly: Device × product type coverage (all combinations?)      │
│  Daily: PH EOD accuracy check (did they list what we told them?) │
│  90-day: Business Report cross-reference (sessions + conversion) │
│                                                                  │
│  LAYER 3: CORRECT (Automated Fix Loop)                          │
│  ─────────────────────────────────────                          │
│  Gap found → Correction queued → Blueprint middleware executes   │
│  Price wrong → Price update queued → SP-API fixes it             │
│  Template wrong → Template update queued → SP-API fixes it       │
│  Device missing → SKU generation triggered → Full pipeline runs  │
│  PH missed item → Re-queued automatically → No manual chase      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: GENERATE (Blueprint V3 — Stages 2-6)

### Trigger: New Product Image in S3

```
Designer uploads artwork
    ↓
DRECO/ListingForge replicates across all devices
    ↓
System auto-generates SKU matrix:
    
    For NARUTO-GEAR5 design:
    ├── HTPCR-IPH17PMAX-NARUG5-BLK  ($19.95, Reduced Shipping)
    ├── HTPCR-IPH17PRO-NARUG5-BLK   ($19.95, Reduced Shipping)
    ├── HTPCR-IPH17-NARUG5-BLK      ($19.95, Reduced Shipping)
    ├── HTPCR-IPH16PMAX-NARUG5-BLK  ($19.95, Reduced Shipping)
    ├── HTPCR-IPH16PRO-NARUG5-BLK   ($19.95, Reduced Shipping)
    ├── HTPCR-IPH16-NARUG5-BLK      ($19.95, Reduced Shipping)
    ├── HB401-IPH17PMAX-NARUG5-BLK  ($21.95, Reduced Shipping)
    ├── HB401-IPH17PRO-NARUG5-BLK   ($21.95, Reduced Shipping)
    ├── ... (all 6 devices)
    ├── HB6CR-IPH17PMAX-NARUG5-BLK  ($24.95, Reduced Shipping)
    ├── ... (all devices × all product types)
    ├── FHB401-IPH17PMAX-NARUG5-BLK ($25.95, FBA, Reduced Shipping)
    └── ... (FBA variants for top designs)
    
    = 30-90 SKUs per design, ALL generated automatically
    ↓
Echo generates content for each SKU
    ↓
Queued for upload: Amazon US → UK → DE → Shopify → Walmart
    ↓
PH team executes upload (they don't decide WHAT — system decided)
```

### Rules Engine (decides everything PH currently guesses)

```yaml
coverage_rules:
  target_devices:
    tier_1: [IPH17PMAX, IPH17PRO, IPH17, IPH16PMAX, IPH16PRO, IPH16]
    tier_2: [IPHSE4, S25ULTRA, S25PLUS, S25, PIXEL9PRO]
    tier_3: [remaining devices from jig data]
  
  target_product_types:
    always: [HTPCR, HB401]
    if_champion: [HB6CR, HB7BK, HLBWH]
    desk_mats: [HDMWH]  # 600x300, 900x400
  
  target_marketplaces:
    always: [amazon_us, amazon_uk, shopify]
    if_licensed_region: [amazon_de, walmart, target_plus]

pricing_rules:
  FBM:
    HTPCR: 19.95
    HB401: 21.95
    HB6CR: 24.95
    HB7BK: 24.95
    HLBWH: 29.95
    HDMWH: 24.95  # desk mats
  FBA:
    premium: +6.00  # validated today: median FBA premium is $6.00
  
shipping_rules:
  US: "Reduced Shipping"      # ⚠️ CONFIRM EXACT NAME
  UK: "Nationwide Prime"      # ⚠️ CONFIRM EXACT NAME  
  DE: "[TBD]"                 # ⚠️ CONFIRM EXACT NAME
```

### What Exists Today (Blueprint V3 Status)

| Component | Status | Owner | Blocker |
|-----------|--------|-------|---------|
| ListingForge (image replication) | 🟡 POC built | Jay Mark | Jig validation for modern devices |
| Echo (content generation) | ✅ Framework ready | — | None |
| SKU generation logic | 🟡 Script exists | — | Needs rules engine integration |
| EAN assignment | ✅ Built (44K pool) | — | None |
| Amazon middleware (Cloud Run) | ✅ Live | — | Needs Product Listing scope |
| Shopify API | 🟡 Connected | — | None |
| Codisto (Walmart) | 🟡 Subscribed | — | Setup needed |
| Supabase `license_skus` table | 🔴 Schema update needed | Jay Mark | Jay Mark availability |

---

## Layer 2: MONITOR (Listings Intelligence)

### Four Automated Monitors

#### Monitor 1: Weekly Delta
**What:** Compare this week's Active Listings Report vs last week's
**Catches:** New listings, removed listings, price changes, status changes, template changes
**Output:** Delta report with counts and drill-down
**Data:** Active Listings Report (6.8GB TSV, downloaded weekly)
**Tool:** Python script → SQLite (not LLM — file too large)

#### Monitor 2: Price Integrity
**What:** For every FBA/FBM pair of the same design, verify FBA is priced $5-7 higher
**Catches:** Pricing errors (4 found today), unauthorized price changes, margin leaks
**Output:** Alert on any pair where FBA ≤ FBM, or price outside expected range
**Data:** Active Listings Report (price column) + Sales data (actual transaction prices)
**Frequency:** Weekly
**Validated today:** 99% correct (409/415 pairs), avg premium $5.86, median $6.00

#### Monitor 3: Shipping Template Compliance
**What:** Every listing checked against rules engine (US=Reduced, UK=Prime)
**Catches:** New listings defaulting to Standard, template drift, script failures
**Output:** Compliance % overall + by device, product type, design, region
**Target:** 100% (currently 85%)
**Data:** Active Listings Report (`merchant-shipping-group` column)
**Frequency:** Weekly + daily delta for new listings
**Blocker:** ⚠️ Cem must confirm exact template names

#### Monitor 4: Device × Product Coverage
**What:** For each champion design, verify all target combinations exist
**Catches:** Missing variants, incomplete product type coverage, regional gaps
**Output:** Coverage heatmap (design × device × product type → listed/gap)
**Data:** Active Listings Report + PULSE champion list + SKU parsing rules
**Frequency:** Weekly

#### Monitor 5: PH Accuracy Audit
**What:** Compare PH daily EOD report vs actual Active Listings delta
**Catches:** Over-reporting, missed listings, wrong product types, delays
**Output:** Accuracy % per team member, leaderboard, trend
**Data:** Slack #eod-listings + Active Listings delta
**Frequency:** Daily

---

## Layer 3: CORRECT (Automated Fix Loop)

```
Monitor finds gap
    ↓
Gap classified:
    ├── PRICE_ERROR → Queue SP-API price update
    ├── TEMPLATE_WRONG → Queue SP-API template update  
    ├── DEVICE_MISSING → Trigger Blueprint Layer 1 (generate new SKU)
    ├── PRODUCT_TYPE_MISSING → Trigger Blueprint Layer 1
    ├── REGION_MISSING → Queue listing for new marketplace
    └── LISTING_SUPPRESSED → Alert PH team with reason
    ↓
Correction queue (Supabase table):
    action_id | type | sku | target | priority | status
    ↓
Blueprint middleware reads queue → executes via SP-API
    ↓
Next delta confirms fix applied
```

**Safety:** Manual approval for first 30 days (Cem reviews queue → clicks "execute"). After 30 days of clean execution: auto-execute low-risk (template fixes, known pricing), manual for high-risk (new listings, suppressions).

---

## Data We Validated Today (Apr 11)

| Finding | Data Point | Source |
|---------|-----------|--------|
| FBA gets 5x more traffic than FBM | Median 67 vs 12 sessions/ASIN | Business Report 90-day |
| 13.3% of buyers pay $12.99 for 2-day | 3,541 of 26,699 orders | Sales data 90-day |
| iPhone 17 Pro buyers 108% more likely to pay for speed | SecondDay over-index by device | Sales data 90-day |
| MagSafe buyers 61% more likely to pay for speed | HB7BK over-index | Sales data 90-day |
| FBA pricing 99% correct | 409/415 pairs, avg $5.86 premium | Sales data 90-day |
| 4 pricing failures exist | FBA priced below FBM | Sales data 90-day |
| 85% shipping template compliance | 15% on Standard (wrong) | Active Listings Report |
| Naruto fans most impulse-driven | 122 index for 2-day shipping | Sales data 90-day |

---

## Build Sequence

### Phase 0: Foundation (This Weekend — Athena + Cem)
- [ ] **Cem: Confirm shipping template names** (US/UK/DE) — 10 min in Seller Central
- [ ] **Athena: Build TSV→SQLite loader** for Active Listings Report (6.8GB file)
- [ ] **Athena: Build first weekly delta** (this week vs last week's Active Listings)
- [ ] **Athena: Build price integrity monitor** (extend today's analysis to full cron)
- [ ] **Athena: Fix 4 pricing failures** identified today (queue for Cem approval)

### Phase 1: Monitor Layer (Apr 15-25 — 10 days)
- [ ] Shipping template compliance monitor (once names confirmed)
- [ ] Device × product type coverage heatmap
- [ ] PH accuracy audit (daily EOD comparison)
- [ ] Weekly delta cron (Gemma 4 on Saturday, 600s timeout)
- [ ] Dashboard V1: scorecard + compliance + coverage + delta

### Phase 2: Rules Engine + Generation (Apr 25-May 10 — 15 days)
- [ ] Pricing rules YAML (from today's validated data)
- [ ] Shipping template rules YAML
- [ ] Coverage rules YAML (devices × product types per design tier)
- [ ] Wire rules into Blueprint's SKU generation (Jay Mark)
- [ ] Wire rules into ListingForge image pipeline

### Phase 3: Correction Loop (May 10-25 — 15 days)
- [ ] Correction queue table (Supabase)
- [ ] SP-API execution via Blueprint middleware
- [ ] Manual approval UI (Cem reviews → approves → executes)
- [ ] Auto-requeue on failure
- [ ] Delta confirms fix applied

### Phase 4: Full Automation (May 25+ — ongoing)
- [ ] New image trigger → full pipeline runs automatically
- [ ] Auto-execute low-risk corrections (templates, known prices)
- [ ] Self-learning: which designs need which devices based on sales velocity
- [ ] PULSE integration: champion status → auto-expand coverage

---

## Agent Assignments (SOUL V4 Roster)

| Task | Owner | Model/Tool | Notes |
|------|-------|-----------|-------|
| TSV→SQLite loader | **Athena** (CLI) | Python script | 6.8GB file, runs on Mac Studio |
| Weekly delta cron | **Gemma 4** | Ollama, 600s | Saturday mornings |
| Price integrity monitor | **Athena** (CLI) | Python script | Extend today's analysis |
| Shipping compliance | **Athena** (CLI) | Python script | Once template names confirmed |
| Coverage heatmap | **Hermes** | OpenClaw ACP | Needs PULSE champion data |
| Dashboard UI | **Jay Mark** (human) | Next.js / ecell.app | Or Claude Code CLI build |
| Rules engine YAML | **Athena** (draft) | Green Zone | Cem approves final rules |
| Blueprint integration | **Jay Mark** (human) | Supabase + middleware | ListingForge + Echo |
| SP-API execution | **Blueprint middleware** | Cloud Run | Already live, needs scope |
| PH accuracy audit | **Athena** (CLI) | Python + Slack | Daily cron |

---

## Revenue Impact

| Fix | Monthly Impact | Confidence | Timeline |
|-----|---------------|------------|----------|
| Shipping template 85%→100% | +$37.5K/mo | HIGH (data-validated) | Phase 1 |
| Price integrity (4 failures) | +$1-2K/mo | HIGH (found today) | Phase 0 |
| Device coverage gaps | +$150-200K/mo | MEDIUM (PULSE estimate) | Phase 2-3 |
| Full coverage guarantee | +$300-400K/yr | MEDIUM (composite) | Phase 4 |

---

## DelegAIt Product Candidate

**Product name:** Coverage Guarantee Engine
**What it does:** Ensures every product is listed on every target marketplace × variant, with correct pricing and shipping, monitored automatically.
**ICP:** E-commerce companies with 1K+ SKUs, offshore listing teams, multi-marketplace presence.
**Pricing tier:** $999-$2,500/mo (high value — prevents revenue leakage)
**Unique insight:** The system decides, humans execute, automation monitors. Not a dashboard — a guarantee.

---

**Status:** DRAFT — For LLM Council Review
**Next:** Cem confirms shipping template names → Phase 0 build starts this weekend
