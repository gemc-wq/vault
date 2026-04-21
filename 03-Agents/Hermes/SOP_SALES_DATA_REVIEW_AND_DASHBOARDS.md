# SOP: Sales Data Review & Dashboard Standards
**Owner:** Ava (CPO) | **Date:** 2026-04-14 | **Version:** 1.0
**Audience:** Hermes (Sales Analyst), Harry (COO), Future Agents
**Status:** LIVE — follow this for all sales reporting

---

## 1. Why This Exists

We have 1.89M SKUs, $5.5–6M revenue, and 6 marketplaces. Raw data is noise. This SOP defines:
- **What** hierarchy to use when organizing sales data
- **What** KPIs matter at each level
- **How** to present data so decisions can be made without context-switching
- **What** future data sources to incorporate as they come online

This SOP codifies the approach from Sales Dashboard V1/V2 and PULSE, built over 2025–2026.

---

## 2. The Data Hierarchy (Non-Negotiable)

Every sales view must be built around this hierarchy in order:

```
Level 1:  Device (e.g. iPhone 17 Pro Max)
Level 2:  Product Type (e.g. HTPCR — Soft Gel Case)
Level 3:  Product Type × Device Combo  ← THE STOCKABLE UNIT
Level 4:  License / Brand (e.g. Naruto, Harry Potter, NFL)
Level 5:  Design Parent (e.g. NARUICO — the specific artwork within the license)
Level 6:  Design Child (e.g. NARUICO-AKA — specific colorway/variant)
Level 7:  Top SKUs (full SKU: HTPCR-IPH16-NARUICO-AKA)
```

**Correction from previous versions:** The old hierarchy had a redundant "Design" level between Product Type×Device and Design Parent. Removed. The correct chain is: License → Design Parent → Design Child. "License" replaces the generic "Design" grouping at the top of the creative hierarchy — it's the IP owner (Naruto = Viz Media, Harry Potter = WB, etc.) and the correct business unit for royalty reporting and strategic decisions.

### Why Product Type × Device is the Stockable Unit

A design doesn't exist in isolation — it only becomes a sellable product when combined with a product type AND a device. The combo `HTPCR × iPhone 16 Pro Max` is what we produce, stock, and list. All gap analysis, inventory planning, and listing decisions must use this grain.

### SKU Structure (Always Parse This Way)
```
{PRODUCT_TYPE}-{DEVICE}-{DESIGN}-{VARIANT}
Example: HTPCR-IPH16PMAX-NARUICO-AKA
```
- Strip leading `F` from product type for FBA matching (FHTPCR → HTPCR)
- Combine FBA + FBM units for the same design in all analytics
- Exceptions (NOT FBA): FLAG, F1309, FRND, FKFLOR

---

## 3. The Five Product Types We Analyze

| Code | Full Name | Price | Key Insight |
|------|-----------|-------|-------------|
| HTPCR | Soft Gel / Tough Phone Case | $19.95 | Highest volume — our workhorse |
| HB401 | Hybrid Hard Case | $19.95 | ⭐ Converts 4× higher than HTPCR (11.81% vs 2.96%) |
| HLBWH | Leather Book Wallet | $24.95 | Underperformer — watch conversion carefully |
| HB6CR | Clear MagSafe Case | $24.95 | Low volume, outstanding conversion (8.45%) |
| HB7BK | Black MagSafe Case | $24.95 | Low volume, excellent conversion (6.76%) |

**Rule:** When building any report, show all 5 types side by side. Never report HTPCR in isolation — it masks the HB401 opportunity.

---

## 4. Dashboard Levels (What Hermes Must Produce)

### Level 1 — Executive Overview
**Audience:** Cem (CEO)
**Frequency:** Weekly (Monday AM)

Metrics:
- Total revenue this week / vs prior week / vs same week last year
- Units sold
- Unique SKUs sold
- By territory (US / UK / EU / ROW) — revenue + units + % of total
- By marketplace channel (Amazon / eBay / Own Sites / Walmart / Other)
- Top 5 winning designs (vs prior week)
- Top 5 losing designs (vs prior week)

Format: Cards + 2-bar-chart maximum. No tables at this level.

---

### Level 2 — Device Performance
**Purpose:** Where is demand by device? Which phones should we prioritize for new listings?

Columns per device:
- Units (this period)
- Revenue
- Sessions (when available from Amazon Business Reports)
- Conversion Rate (sessions → units)
- YoY trend

**Quadrant classification (based on Sessions + Conversion):**
- ⭐ STAR: High sessions + High conversion → hold price or test increase
- ❓ QUESTION MARK: High sessions + Low conversion → fix listing or test price cut
- 🐄 CASH COW: Low sessions + High conversion → increase PPC
- 🪨 DOG: Low sessions + Low conversion → deprioritize, review listing

**Top 50 devices cover 86.5% of revenue** — always limit to top 50 unless specifically drilling down.

---

### Level 3 — Product Type Performance
**Purpose:** Which case type is growing or declining? Where should we invest in new listings?

Show per product type:
- Units / Revenue / Conversion rate (when available)
- % of total revenue
- WoW and MoM trend
- Indexed momentum score (see PULSE Phase 2 spec)

**Key benchmark to always show:**
> HB401 converts at 11.81% vs HTPCR at 2.96% — 4× higher. HB401 is under-distributed.

---

### Level 4 — Product Type × Device Combo
**This is the stockable unit. This level drives operational decisions.**

Use case: "How many HTPCR-IPH16PMAX combos do we have live? Are we missing any top designs on that combo?"

Table structure:
```
Device | Product Type | Units | Revenue | Conv% | # Designs Listed | Gap vs Top50 Designs
```

Sorted by revenue DESC. Highlight any combo in top 50 devices × top 5 product types that has <80% of top-50 designs listed.

---

### Level 4 — License / Brand Performance
**Purpose:** Which IP licenses are driving revenue? Feeds license renewal decisions and royalty reporting.

Show per license:
- Revenue, Units, # design parents, # active SKUs
- % of total revenue
- WoW / MoM trend
- License expiry status (flag expired or <90 days to renewal)
- MG shortfall alert if applicable (e.g. NBA $200K shortfall, Shelby $27.5K shortfall)

Sorted by revenue DESC. This is the view Cem uses for license review meetings.

---

### Level 5 — Design Parent Performance
**Purpose:** Within a license, which specific artworks are driving sales?

Example: Within NARUTO license → NARUICO (Naruto Iconic) vs NARUCHA (Naruto Characters) vs NARUBOA (Naruto Board Art)

Show per design parent:
- Revenue, Units, # child variants, # active listings
- Coverage: how many of top 50 devices is it listed on?
- Badge: 🏆 Champion (top 500 revenue), 🚀 Surging (velocity ratio >2× MoM)
- Quadrant (same ⭐/❓/🐄/🪨 logic when sessions available)

---

### Level 6 — Design Child Performance
**Purpose:** Specific colorway/variant level — the actual printable asset.

Example: NARUICO-AKA (Akatsuki red colorway)

Show per design child:
- Revenue, Units, Conv% (when available)
- Which product types and devices is it listed on?
- Coverage gap vs top 50 devices
- Image thumbnail (from S3 CDN: `elcellonline.com/atg/{DESIGN}/{VARIANT}/...`)

---

### Level 6 — Top SKUs
**Purpose:** Identify the specific unit-level winners and outliers for operational decisions.

Top 100 SKUs by revenue (weekly):
```
SKU | Units | Revenue | Marketplace | WoW change | Conv% (if available)
```

Rules:
- Show FBA + FBM combined (combine HTPCR + FHTPCR for same design/device)
- Flag new entrants (not in top 100 last week)
- Flag drop-offs (was in top 100, now gone)

---

## 5. Conversion Rate Analysis — The Full Framework

Conversion rate is our single most important e-commerce KPI. A product can have great traffic and still die if the listing doesn't convert. This section defines how we measure, segment, and act on conversion data.

### 5.1 The Conversion Equation
```
Conversion Rate = Units Ordered ÷ Sessions × 100
```
Source: Amazon Business Reports (Child ASIN granularity)

**Baseline benchmarks (US, March 2026):**
- Overall: 2.89% (30-day)
- HTPCR: 2.96%
- HB401: 11.81% ← 4× higher than HTPCR
- HB6CR MagSafe: 8.45%
- Category average: ~1.5%

### 5.2 Segmentation Layers for Conversion Analysis

Never report conversion as a single number. Always segment by:

**Layer 1 — Product Type**
HTCPR vs HB401 vs HLBWH etc. (see Level 2 benchmarks above). HB401 outperforms by 4× — always call this out.

**Layer 2 — Device**
Apply the quadrant model: high sessions + high conversion (⭐) vs high sessions + low conversion (❓). See device quadrant table.

**Layer 3 — Region (UK vs US)**
US and UK convert differently and must NEVER be mixed in conversion analysis:
- Different price points (GBP vs USD)
- Different competitive landscape (eBay is stronger in UK, Amazon Prime penetration differs)
- Different fulfillment expectations
- **Rule:** Always show UK conversion and US conversion as separate columns. Aggregate "global" conversion is meaningless.

**Layer 4 — FBA vs FBM (Shipping Template)**
This is the highest-impact segmentation we currently can't do properly — but it's critical:
- FBA listings carry the Prime badge — empirically converts significantly higher
- FBM listings without Prime template convert at a discount
- Mixing FBA and FBM in conversion averages masks the true signal
- **Rule:** Once shipping template data flows (custom=true fix), ALWAYS split conversion by FBA vs FBM. Flag any high-traffic FBM listing that should be converted to FBA.

Shipping template names map as:
- Templates containing "Prime" or "FBA" = Prime-eligible
- Standard templates = FBM
- Missing/deprecated = unknown (flag for investigation)

### 5.3 Conversion Drivers (What Sales Analytics Can + Cannot Measure)

**CAN measure (Hermes scope):**
| Driver | How to detect |
|--------|---------------|
| FBA vs FBM (Prime badge) | Shipping template from Active Listings report |
| Price point | From listings + orders data |
| Session volume | From Business Reports |
| Buy Box % | From Sales & Traffic report (when permissions fixed) |
| Regional differences | Segment UK vs US separately |
| Device-level conversion | Business Report child ASIN grain |
| Momentum (velocity trend) | Compare 14d vs 90d daily rate |

**CANNOT measure (out of Hermes scope — falls to Content/Creative skill):**
| Driver | Why it's out of scope |
|--------|----------------------|
| Image quality | Requires human visual judgment / A/B testing |
| Listing copy quality | Content skill (Echo agent) |
| Keyword relevance | SEO skill (Bolt agent) |
| A+ Content / Brand Story | Creative skill |
| Customer reviews / ratings | Qualitative, not quantitative analytics |

**Document but don't solve:** Hermes should flag listings with high sessions but low conversion (Question Marks) and note "possible image/copy issue — refer to Content skill for investigation." That's the boundary.

### 5.4 Conversion Action Plan (Standing Playbook)

When Hermes identifies a conversion issue, escalate using this framework:

| Symptom | First check | Likely fix | Owner |
|---------|-------------|-----------|-------|
| High sessions, low conversion, FBM listing | Is there an FBA twin? | Convert to FBA or add Prime template | Ops |
| High sessions, low conversion, FBA listing | Price vs competitors? | Test price reduction $0.50-$1 | Ava/Cem |
| Low sessions, high conversion | PPC budget too low | Increase sponsored ads | Ads team |
| UK converts lower than US for same SKU | Shipping cost? Price parity? | Check UK price + shipping template | Ops |
| Conversion dropped WoW for specific device | Competitor launched? Price change? | Check competitor listings | Loom/Bolt |

---

## 6. KPIs — Current vs Future

### Currently Available (from orders/BQ data)
| KPI | Source | Grain |
|-----|--------|-------|
| Units sold | orders table | SKU / device / design |
| Revenue (GBP/USD) | orders table | SKU / territory |
| Marketplace channel | orders.Marketplace | Channel level |
| Buyer country | orders.Buyer_Country | Territory level |
| Product type | SKU parsing | Product level |
| Device | SKU parsing | Device level |
| Design | SKU parsing | Design level |
| FBA vs FBM | F-prefix on SKU | SKU level |

### Coming Online (when Amazon Reports permissions are fixed)
| KPI | Report Type | What it unlocks |
|-----|-------------|-----------------|
| Sessions | GET_SALES_AND_TRAFFIC_REPORT | Conversion rate calculation |
| Page views | GET_SALES_AND_TRAFFIC_REPORT | Visibility vs browse depth |
| Conversion rate | Derived (units ÷ sessions) | Pricing/listing quality signal |
| Buy Box % | GET_SALES_AND_TRAFFIC_REPORT | Competitive positioning |
| Search keywords | Brand Analytics (future) | Demand intelligence |
| FBA inventory level | GET_AFN_INVENTORY_DATA | Stock-out risk |
| FBA fees | GET_FBA_ESTIMATED_FBA_FEES | True margin calculation |

### High-Priority Future KPI: Shipping Template
| KPI | Source | Why it matters |
|-----|--------|----------------|
| Shipping template name | Active Listings report (custom=true) | Determines Prime eligibility per ASIN |
| FBA/FBM flag | SKU prefix + shipping template | Segmentation for conversion analysis |

**Once shipping template data flows:** Always segment conversion analysis by FBA vs FBM. FBA listings have Prime badge and convert significantly higher — mixing them distorts the signal.

### High-Priority Future KPI: Amazon Search Analytics
When Brand Analytics access is restored:
| KPI | Use case |
|-----|----------|
| Top search terms → our ASINs | Which searches are we winning? |
| Search volume by keyword | Demand sizing (iPhone 17 is #1 in our category) |
| Keyword → conversion rate | Quality of traffic for specific searches |

Priority keywords to track: `iphone 17 case`, `iphone 17 pro max case`, `peanuts phone case`, `naruto phone case`, and all top-10 device × license combos.

---

## 7. PULSE — The Reference Implementation

PULSE (Product Uplift & Listing Signal Engine) is the canonical way we present actionable product data. Hermes should understand this before building any reports.

### PULSE Views
1. **Leaderboard** — Top 50 lineups × marketplace coverage traffic lights (🟢🟡🔴)
2. **Opportunity Finder** — Conversion signals by design, flagged with action type
3. **Deployment Pipeline** — Gap → listing creation workflow
4. **License Deep Dive** — Per-IP coverage matrix

### PULSE Action Types (for Hermes to flag in reports)
| Action | When to flag |
|--------|-------------|
| LIST IT | Exists in catalog, not live on target marketplace |
| COMPLETE IT | Missing device-family variants for an existing design |
| BUILD IT | New design justified by demand signals |
| FIX IT | Listed but conversion is weak → listing quality issue |
| BOOST IT | Conversion strong but traffic low → PPC opportunity |

### PULSE Opportunity Score Formula
```
OPPORTUNITY SCORE =
  conversion_rate_percentile × 0.30
  + velocity_ratio × 0.25
  + revenue_rank_percentile × 0.20
  + coverage_gap_score × 0.25

WHERE coverage_gap_score = (total_channels - channels_listed) / total_channels
```

### PULSE Champions
- 590 designs earn ~80% of revenue ($352K / $440K 80th percentile)
- Always cross-reference against Champion list before flagging gaps
- Champion badge: design in top 500 by trailing 6-month revenue

---

## 8. Momentum Scoring (Phase 2 PULSE)

Every report should optionally include momentum scores. Formula:

```
daily_rate_short = units_last_14d / 14
daily_rate_long  = units_last_90d / 90
momentum_score   = ((daily_rate_short - daily_rate_long) / daily_rate_long) × 100

🔥 > +50% = Surging
📈 +20–50% = Accelerating
➡️ -20 to +20% = Steady
📉 -50 to -20% = Declining
❄️ < -50% = Cooling
```

Apply at: design parent, product type, device, and territory levels.

---

## 9. Sales Dashboard V2 Reference

**Repo:** `github.com/gemc99-boop/sales-dashboard`
**Stack:** Vite + React + Recharts + Tailwind (frontend) + Node/Express (API) + BigQuery
**Data source:** `instant-contact-479316-i4.zero_dataset.orders` (2.8M rows, 2020–present)

### API Endpoints (for Hermes to call if needed)
```
GET /api/overview?from=YYYY-MM-DD&to=YYYY-MM-DD
GET /api/channels?from=...&to=...
GET /api/territories?from=...&to=...
GET /api/products?from=...&to=...&groupBy=type|device|design|brand
GET /api/top-skus?from=...&to=...&limit=50
GET /api/momentum?groupBy=brand&shortDays=14&longDays=90&limit=50
```

### Territory Groups
```
US: "United States Of America", "United States", "USA"
UK: "United Kingdom"
Europe: Germany, Italy, France, Austria, Belgium, Switzerland, Spain, Sweden, Netherlands, Luxembourg, Finland, Ireland + others
Japan: "Japan", "JP"
ROW: everything else
```

### Channel Groups
```
Amazon: all Amazon variants
eBay: e_cell, e_cell-usa, ecell_accessorize
Own Sites: head_case_designs, head_case_designs-us, Big Commerce
Walmart / Rakuten / B2B / Other
```

---

## 10. Hermes Reporting Standards

### Weekly Report Structure (every Monday)

**Section 1 — Executive Summary** (3 bullets max)
- Top insight this week
- Biggest mover (up)
- Biggest mover (down)

**Section 2 — Device Performance Table**
- Top 20 devices by units, sorted desc
- Include WoW delta column
- Flag quadrant (⭐/❓/🐄/🪨) when sessions data available

**Section 3 — Product Type Performance**
- All 5 product types
- Units, Revenue, Conv% (when available), WoW trend

**Section 4 — Top Designs (Parent Level)**
- Top 20 by revenue
- With momentum score where possible

**Section 5 — Top SKUs**
- Top 50 by revenue
- Flag FBA vs FBM
- Flag new entries and exits vs prior week

**Section 6 — Action Items** (max 5)
- Formatted as: `[ACTION TYPE] Design/Device — Reason — Suggested action`
- Example: `[BOOST IT] NARUICO × iPhone 16 Pro Max — 8.3% conversion, low sessions — increase PPC budget`

### Format Rules
- No narrative fluff — tables and bullets only
- Always show WoW delta alongside current period
- Always combine FBA + FBM for the same base SKU
- Use Buyer_Country (not PO_Location) for all geographic analysis
- Currency: show GBP for UK, USD for US — never mix in the same table

---

## 11. Known Data Quality Issues

| Issue | Impact | Status |
|-------|--------|--------|
| Sessions/conversion not yet available | Can't do full quadrant analysis | Blocked — pending SP-API Analytics role |
| Shipping template missing from listings | Can't segment FBA vs FBM properly | Fix in progress (custom=true report option) |
| UK listings table not yet in BQ | No UK Active Listings in middleware | UK sync needed after US validated |
| NFL license expired Mar 31 | NFL SKUs in sell-off — exclude from growth analysis | Ongoing until ~Jun 29 |

---

## 12. The North Star Metrics

Every report should ultimately answer these three questions:

1. **Coverage:** Are our top 500 designs listed on all 5+ marketplaces? (metric: % coverage)
2. **Speed:** Are orders fulfilling in <48h? (metric: avg fulfillment time — from ops data)
3. **Intelligence:** Which SKUs are performing, which are dead weight? (metric: revenue per SKU, velocity)

If a table or chart doesn't help answer one of these three questions, cut it.

---

*Sources: PULSE V4 Spec (2026-03-10), Sales Dashboard V2 Brief (2026-03), PHASE2_MOMENTUM_SPEC.md, PULSE Conversion Baselines (2026-03-21), Cem briefing (2026-04-14)*
*Filed by: Ava | For: Hermes | cc: Athena*
