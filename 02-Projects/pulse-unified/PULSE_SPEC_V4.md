# PULSE v4 — Product Uplift & Listing Signal Engine
**Spec: Dashboard + Gap Analysis + Listing Deployment**

**Owner:** Ava (CPSO) | **Date:** 2026-03-10 | **Status:** Approved for build
**Council Input:** LLM Council report (Opus 4.6, GPT 5.4, Gemini 3.1 Pro) — 2026-03-09
**Approved by:** Cem (CEO) — verbal, 2026-03-10

---

## Architecture

```
BigQuery (headcase + orders + marketplace data)
       ↓ ETL (daily delta sync)
Supabase (Unified Product DB)
       ↓ REST API
PULSE Dashboard (Next.js + Tailwind, Vercel)
       ↓ Actions
Shopify (bulk product creation) → Connectors → Walmart / Target+ / OnBuy / Kaufland
```

## Data Foundation (BUILT ✅)

| Table | Rows | Source |
|---|---|---|
| lineups | 10,279 | BQ headcase.tblLineups |
| designs | 110,634 | BQ headcase.tblDesigns |
| product_types | 146 | Orders + BQ parsing |
| devices | 1,322 | Orders + BQ parsing |
| products | 90,661 | Distinct combos from orders |
| marketplace_listings | 467,392 | BQ Amazon (436K) + Walmart (31K) |

**Key mapping:** `design_code` in orders = `LineupLabel` in headcase (99% match rate). Products table references lineups, not individual designs.

---

## View 1: Leaderboard — Coverage Traffic Lights

### Layout
- **Style:** Match Sales Dashboard V2 (dark theme, same fonts, hover interactions)
- **Rows:** Hybrid leaderboard — Top 50 lineups + Top 300 individual designs (covers ~156 lineups)
- **Columns:** Marketplace channels (Amazon US, Walmart, Shopify/DTC, Target+, eBay)
- **Cells:** Traffic light indicators (🟢 🟡 🔴)

### Traffic Light Algorithm
| Color | Meaning | Threshold |
|---|---|---|
| 🟢 Green | Full coverage | Listed on ≥80% of top 10 devices × ≥3 major product types |
| 🟡 Amber | Partial coverage | Listed on 30-80% of eligible combos |
| 🔴 Red | Missing/minimal | <30% coverage OR zero listings |

Thresholds configurable via dashboard controls.

### Leaderboard Algorithm
```
INCLUDE lineup IF:
  - Trailing 6-month revenue in top 50 (Pareto cut)
  OR
  - Any child design (lineup + variant) is in top 300 by revenue
    AND trailing 2-month revenue > $500

SORT BY: trailing 6-month revenue DESC

BADGE "⭐ Champion" on lineups included ONLY because of a top-300 design
BADGE "🚀 Surging" on lineups with velocity ratio > 2x (2mo/6mo normalized)
```

### Leaderboard Controls
- **Slider:** Adjust lineup count (25 / 50 / 100 / 200)
- **Slider:** Adjust design count (100 / 300 / 500)
- **Dropdown:** Time period (3mo / 6mo / 12mo)
- **Filter:** By license category (Anime, Sports, Entertainment, Fantasy, Music)
- **Region filter:** US / UK / EU / All — filters both sales data AND target marketplaces
  - US view: Amazon US + Walmart + Target+ sales data
  - UK view: Amazon UK + eBay UK + OnBuy sales data
  - EU view: Amazon DE/FR/IT/ES + Kaufland sales data
- **Product group toggle:** Phone Cases Only / Desk Mats & Skins / All Products
  - Phone cases = back cases (HTPCR, HC, HB6CR) + leather wallets (HLBWH) — designs replicate across these
  - Desk mats (HDMWH) + skins (H8939) = different design treatment (landscape/large format, may need redesign)
  - Default: Phone Cases Only (highest volume, most directly actionable)

### Drill-Down (Click-Through)
Click a lineup row → expands to show:
- All child designs within that lineup, sorted by revenue
- Traffic lights per design per marketplace
- Champion designs (top 300) get ⭐ badge
- Design image on hover (from `headcase.tblDesigns.ImageURL`, fallback: Amazon listing image)
- Default product shown: iPhone 16 Pro Max variant (highest-volume device)

### Design Image Integration
- Source: `designs.image_url` column (from headcase tblDesigns)
- Fallback: Amazon listing image via `marketplace_listings.title` → scrape, or placeholder
- Display: 80×80px thumbnail on hover, rounded corners
- Default device for mockup: iPhone 16 Pro Max (most popular)

---

## View 2: Opportunity Finder — Conversion Signals

### Purpose
Identify high-converting designs that are under-distributed — products that DON'T sell because they DON'T EXIST yet, not because they're weak.

### Data Source
Amazon Business Report (child ASIN): sessions, page views, conversion rate, units ordered.
File: `data/amazon/BusinessReportbychildAmazonUS_Jan1_Feb24 1.xlsx` (80K rows)

### Algorithm
```
OPPORTUNITY SCORE = 
  conversion_rate_percentile × 0.30    -- Council: conversion is strongest signal
  + velocity_ratio × 0.25              -- Surging designs
  + revenue_rank_percentile × 0.20     -- Proven revenue
  + coverage_gap_score × 0.25          -- How many channels missing

WHERE coverage_gap_score = (total_channels - channels_listed) / total_channels
```

### Five Action Types (Council Recommendation)
| Action | Definition | Routes To |
|---|---|---|
| **LIST IT** | Exists internally, not live on target marketplace | Marketplace ops / Listings team |
| **COMPLETE IT** | Same design/form factor missing device-family variants | Marketplace ops |
| **BUILD IT** | New design × form factor justified by demand signals | Design / merch team |
| **FIX IT** | Listed but conversion is weak → listing quality issue | Content / CRO team |
| **BOOST IT** | Conversion strong but traffic weak → needs PPC | Advertising team |

### Display
- Table sorted by opportunity score DESC
- Columns: Lineup, Design, Product Type, Device, Action Type, Opportunity Score, Est. Revenue
- Color-coded by action type
- Filterable by action type, marketplace, license category

---

## View 3: Deployment Pipeline — Listing Pusher

### Purpose
Turn gap analysis into actual listings. The complete flow from "identified gap" → "live on marketplace."

### Pipeline Stages
```
IDENTIFIED → QUEUED → CREATING_IN_SHOPIFY → SYNCING_TO_CHANNEL → LIVE
```

### Batch Operations
- **Select:** Check individual items or "Select All" filtered results
- **Publish:** Batch create in Shopify via Bulk Product API
- **Product data generated from:**
  - Title: Rules engine (per-channel title templates)
  - Description: Template + design/brand context
  - Price: Amazon price ± channel-specific adjustment
  - Images: headcase ImageURL
  - UPC/GTIN: EAN registry lookup
  - SKU: Generated from product_type + device + lineup + variant codes

### Status Tracking
- Real-time pipeline status per item
- Aggregate stats: "142 queued, 38 creating, 12 syncing, 890 live"
- Filterable by marketplace, status, date range

### Shopify Integration
- Shopify is the HUB — all products created here first
- Connectors push to: Walmart (CedCommerce/Codisto), Target+, OnBuy, Kaufland
- One source of truth for product data across all channels

---

## View 4: License Deep Dive (Bonus View)

### Purpose
Per-license coverage analysis for license review meetings and strategic planning.

### Layout
- **Dropdown:** Select a license (NBA, Harry Potter, Dragon Ball Z, etc.)
- **Matrix:** All designs in that license × all product types × all top devices
- **Traffic lights** at each cell
- **Summary stats:** Total SKUs possible, Total listed, Coverage %, Revenue, Top marketplace

### Use Case
"Show me everything about our NBA coverage. Where are the gaps? What's our revenue? What should we list next?"

---

## Technical Stack

| Component | Technology |
|---|---|
| Frontend | Next.js 16 + React 19 + Tailwind v4 |
| Charts/UI | Recharts or Tremor (match SalesDB V2) |
| Backend API | Supabase REST API (PostgREST) |
| Database | Supabase PostgreSQL |
| Data warehouse | BigQuery (source of truth for heavy queries) |
| Hosting | Vercel (team: ecells-projects-3c3b03d7) |
| Auth | None (internal tool, Vercel preview protection) |

## Styling Requirements
- **Light theme** — white background, cobalt (#0047AB) accents, black text
- **Match Ecell Global branding** — light, professional, consistent with ecellglobal.com
- Fonts consistent with Sales Dashboard V2 (same family, same sizing)
- Smooth transitions on drill-down / expand
- Design images on hover (80×80 thumbnails)
- Traffic light cells with tooltip showing exact coverage stats
- Responsive but desktop-first (this is an ops tool)

---

## Data Refresh Strategy

### Daily Delta Sync (not full overwrite)
```
1. Download Amazon Active Listings report (or SP-API when available)
2. Load into staging table
3. DIFF against current marketplace_listings:
   - NEW SKUs → INSERT
   - Changed price/status → UPDATE
   - Missing from report → mark INACTIVE
4. Log sync stats (inserted, updated, deactivated)
```

### Weekly
- Re-run leaderboard scoring (revenue rankings, velocity ratios)
- Refresh products table with any new combos from orders

### Monthly
- Full dimension table refresh (lineups, designs from headcase)
- Calibrate traffic light thresholds based on actual coverage data

---

## Council Recommendations — Status

| Council Rec | Status in This Spec |
|---|---|
| Profit optimization over revenue | ⏳ Phase 2 — need COGS data per product type |
| SFP over FBA | ✅ Noted, separate workstream (not PULSE scope) |
| Walmart conversion calibration | ✅ Built into closed-loop tracking |
| Closed-loop tracking Phase 1 | ✅ Action log + outcome tracker in View 3 |
| 5-action classification | ✅ LIST IT / COMPLETE IT / BUILD IT / FIX IT / BOOST IT |
| Device lifecycle normalization | ⏳ Phase 2 — need iPhone release date mapping |
| Design-license constraint table | ⏳ Phase 2 — need license rights data from Cem |
| SP-API migration | ⏳ Separate infra project |
| Cannibalization discount | ⏳ Phase 2 — measure first |
| PRICE IT action type | ⏳ Phase 2 |
| RETIRE IT action type | ⏳ Phase 2 |

---

## Build Plan

| Phase | What | Owner | Target |
|---|---|---|---|
| **Phase 1 (this week)** | Leaderboard + Traffic Lights + Drill-down | Codex (Forge) | Mar 14 |
| **Phase 1** | Opportunity Finder (5 action types) | Codex (Forge) | Mar 14 |
| **Phase 1** | Deployment Pipeline UI (status tracking) | Codex (Forge) | Mar 14 |
| **Phase 1** | Regional filters (US/UK/EU) + Product group toggle | Codex (Forge) | Mar 14 |
| **Phase 2 (next week)** | Shopify bulk API integration | Codex (Spark) | Mar 21 |
| **Phase 2** | Daily delta sync cron | Ava/Pixel | Mar 21 |
| **Phase 2** | Conversion data integration (Amazon Business Report) | Atlas | Mar 21 |
| **Phase 2** | Closed-loop outcome tracking | Atlas | Mar 21 |
| **Phase 2** | COGS per product group (Harry builds finance layer) | Harry | Mar 21 |
| **Phase 3 (week 3)** | License Deep Dive view | Codex | Mar 28 |
| **Phase 3** | Profit-weighted scoring (uses Harry's COGS data) | Atlas | Mar 28 |
| **Phase 3** | Device lifecycle normalization | Atlas | Mar 28 |

---

## Success Metrics
- **Coverage increase:** From current baseline → +20% coverage on Walmart within 30 days
- **Listing velocity:** 500+ new listings pushed to Shopify/Walmart per week via PULSE
- **Revenue impact:** $50K+ incremental monthly revenue from PULSE-identified gaps within 60 days
- **Alert accuracy:** >70% of LIST IT alerts result in revenue within 30 days of listing

---

*Spec: PULSE_SPEC_V4.md*
*Location: projects/pulse-unified/ + GDrive Brain/Projects/PULSE/*
*Previous versions: PULSE_SCOPE_V3.md (renamed from PIE)*
