# Product Intelligence Engine — Scope v2
**Project Code:** PIE  
**Priority:** P0 — Everything downstream depends on this  
**Owner:** Ava (Strategic Lead) + Harry (Data Infrastructure)  
**Sponsor:** Cem (CEO)  
**Created:** 2026-03-07 | **Updated:** 2026-03-07 (v2 — reflects today's unlocks)

---

## 1. What PIE Is

An algorithmic system that answers: **"Which of our 1.89M SKUs should we sell, where, and why?"**

It takes our full product catalog (BigCommerce) + 6 years of sales history (BigQuery) + marketplace session data (Amazon) and produces a scored, ranked list of ~200K SKUs optimized for revenue coverage, collection completeness, and channel-specific rules.

PIE is not a dashboard. It's the **decision engine** that feeds everything: GoHeadCase, Target+, Walmart, DTC microsites, Amazon FBA conversion targets.

## 2. Why It's P0

Every downstream project is blocked without PIE's output:
- **GoHeadCase** → Can't stock the Shopify store without knowing which SKUs to list
- **Target+** → Feedonomics ending ~Mar 19, need curated SKU feed
- **Walmart** → 95K listings, 99.9% zero reviews — need to focus effort on winners
- **Amazon FBA** → 3.44M SKUs all FBM — which ones justify FBA investment?
- **Microsites** → Sports/Anime/Entertainment categories need PIE to define product scope
- **Listing Team (PH)** → 8 staff doing manual replication — PIE tells them WHAT to replicate first

## 3. Core Logic

### 3.1 Design-First Approach
> "We sell collections, not individual SKUs"

A **design** is the parent asset. SKUs are just: `design × device × product type`.

**Rank designs by revenue first**, then replicate across devices and product types. This is how the business actually works — a Naruto design gets printed on 50+ phone models and 4+ case types.

### 3.2 Scoring Layers

**Layer 1: Revenue Ranking (BQ — 2.8M orders)**
- Group all orders by `design_code`
- Rank by total revenue (USD-normalized via `net_sale_usd`)
- Multi-lookback: 1mo / 3mo / 6mo / 1yr / all-time
- **Finding:** Elbow at 216 designs. Top 200 = 63.59% of revenue. Marginal contribution drops below 0.1% per design after that.

**Layer 2: Behavioral Scoring (Amazon Sessions — 80K rows)**
- Sessions × Conversion Rate × Buy Box % = **Opportunity Score**
- High sessions + low conversion = optimization target (fix listing, not abandon SKU)
- High conversion + low sessions = hidden gem (increase PPC/visibility)
- **Finding:** Desk mats convert at 3-6%, legacy iPhones (12/13/14) at 7-9% with anime. FHC product line losing Buy Box at 63.6%.

**Layer 3: Collection Completeness (BC Catalog — 408K active variants)**
- Each selected design should exist across core product types:
  - HTPCR (snap case) — #1 revenue, £8.04M
  - HLBWH (wallet) — #2, £7.28M  
  - HC (hard case) — #3, £2.23M
  - HB401 (soft gel) — significant volume
- Score designs by how complete their product type matrix is
- Flag gaps: "Design X has HTPCR but no HLBWH — create wallet variant"

**Layer 4: Device Family Coverage**
- If iPhone 16 selected → must include 16 / Plus / Pro / Pro Max
- Family-based selection, not individual device cherry-picking
- **704 unique devices** globally, but Top 50 = 86.5% of revenue

**Layer 5: Regional Optimization**
- US and UK have fundamentally different device profiles:
  - **US:** iPhone-heavy, desk mats matter (#11 at $62K), Samsung S938U
  - **UK:** Samsung A16 5G in top 10 (#8 at £98K), older iPhones persist, console skins strong
- PIE produces region-specific device lists, not one global list

**Layer 6: Channel Rules (Hard Constraints)**
- **Target+:** ❌ NO US Sports (NFL/NBA/NHL/NCAA/MLS). UK football OK.
- **Amazon FBA:** Prioritize high-session, high-conversion SKUs for FBA migration
- **Walmart:** Focus on SKUs with review-building potential
- **DTC Microsites:** Category-themed subsets (anime, sports, entertainment, fantasy)

**Layer 7: Conversion Benchmarking (Phase 1) — KEY INSIGHT**
> "HB401 converts at 2.5x the snap case rate but has only $16K revenue" — Cem, Mar 7

This layer identifies **under-distributed high-converters** and **over-distributed low-converters**.

For each product type, device, and design, calculate:
- **Average conversion rate** (weighted by sessions)
- **Listing coverage %** — share of addressable SKUs actually listed
- **Conversion-to-coverage ratio** — if conversion share >> listing share, product is under-distributed

**Critical nuance (Cem):** Don't compare raw listing counts across product types. HB401 supports ~20 devices, HTPCR supports 300+. Desk mats come in 3 sizes. The question is: **within each product type's addressable matrix, do we have the top designs covered?**

Gap analysis must answer:
- For HB401: are the top 300 designs live across its supported devices?
- For HDMWH: are the top 300 designs live across all 3 sizes?
- For HTPCR: which top designs are MISSING from which top devices?

**Quadrant classification:**
| | High Conversion | Low Conversion |
|---|---|---|
| **High Sessions** | 🏆 Hero — protect & invest | ⚠️ Fix listing (images/price/reviews) |
| **Low Sessions** | 💎 Hidden gem — boost PPC | 💀 Consider removal |

**Validated findings:**
- HB401: 8.34% conversion (2.54x HTPCR's 3.28%) with only 0.68% listing share
- HDMWH: ~10% revenue share from 0.47% listing share — severely under-listed
- HLBWH: 29% listing share but only 12.9% revenue share, 2.05% conversion — over-distributed

**Data source:** Amazon Business Reports (manual XLSX upload until SP-API weekly cron is live)
- US data: ✅ 80K rows (Jan-Feb 2026)
- UK data: 🔴 Needed
- DE data: 🔴 Needed

**Layer 8: Search Term & Trend Analysis (Phase 2 — bolt-on)**
- External validation layer using Amazon keyword reports (from Ads), Google Trends
- Cross-reference PIE candidates against search volume
- Use case: new license evaluation — "should we invest in Jujutsu Kaisen?"
- High search volume + low listing coverage = immediate opportunity
- Data source: Amazon Ads keyword reports (Cem can pull), Google Trends API
- **Not blocking Phase 1** — adds confidence scoring on top of revenue + conversion layers

### 3.3 Brand Tiering
| Tier | Definition | Design Selection | Est. SKUs |
|------|-----------|-----------------|-----------|
| A | Top 20 brands by revenue | ALL designs | ~120K |
| B | Next 30 brands | Top 10 designs each | ~54K |
| C | Long tail | Top 5 designs each | ~27K |
| **Total** | | | **~201K** |

## 4. Data Sources — Current Status

### ✅ Available & Connected
| Source | Records | Location | Status |
|--------|---------|----------|--------|
| **BigQuery Orders** | **2,802,015** | `instant-contact-479316-i4.zero_dataset.orders` | ✅ LIVE through today |
| **BQ Product Master** | Multiple tables | `instant-contact-479316-i4.headcase.*` | ✅ tblDesigns, tblLineups, tblDesignTags |
| **Supabase Orders** | 304K + syncing | `auzjmawughepxbtpwuhe.supabase.co` | ✅ Daily sync live (Harry, 2 AM ET) |
| **FX Rates** | 240 rows | Supabase `fx_rates_daily` | ✅ Daily refresh (1:30 AM ET) |
| **Amazon US Sessions** | 80,000 | XLSX (Jan-Feb 2026) | ✅ Analyzed by Atlas |
| **BigCommerce Catalog** | 408K variants | TSV → Supabase `bc_products` | ✅ Pixel loading now |
| **Inventory** | 9,800 | Supabase `inventory` | ✅ Active |

| **Amazon US Active Listings** | 3.44M SKUs | GDrive → Supabase/BQ (Harry loading) | ✅ File available, loading |

### ⚠️ Needed
| Source | Purpose | Status |
|--------|---------|--------|
| Walmart Listings (full) | 95K listings, only 10K loaded | ⚠️ Pagination fix (Harry) |
| Target+ Items | Channel-specific selection | ⚠️ Need Cem export from Partner Portal |
| Amazon UK Active Listings | UK marketplace live inventory | 🔴 Need report pull |
| Amazon DE Active Listings | Germany marketplace live inventory | 🔴 Need report pull |
| Amazon UK/EU Sessions | Regional behavioral data | 🔴 Not yet uploaded |
| Amazon SP-API Connection | Automated weekly listing pulls (US/UK/DE) | 🔴 API keys available, not connected |
| Amazon Ads Keyword Reports | Search term analysis (Phase 2) | 🔴 Cem to pull from Ads console |
| GA4 Site Data | On-site behavior (GoHeadCase future) | 🔴 Not connected |

## 5. Architecture

### Agent Roles
| Agent | Model | Role in PIE |
|-------|-------|------------|
| **Atlas** | Gemini 3.1 Pro | Revenue analysis, design rankings, opportunity scoring |
| **Pixel** | Gemini 2.5 Flash | Data processing, ETL, catalog parsing, Supabase loads |
| **Prism** | GPT-5.4 | Behavioral/probabilistic analysis, ensemble second opinion |
| **Ava** | Claude Opus 4.6 | Strategic synthesis, reconciliation, quality gate |
| **Harry** | Claude Opus 4.6 | Data infrastructure, BQ queries, Supabase schema, syncs |
| **Codex** | GPT-5.3 | Dashboard builds (PIE tabs in Sales Dashboard V2) |

### Pipeline
```
BigQuery (2.8M orders)  ──┐
                          ├──→ PIE Scoring Engine ──→ Scored SKU List (~200K)
BigCommerce (408K+)     ──┤         │                        │
                          │         │                        ├──→ Supabase (product master)
Amazon Sessions (80K)   ──┘         │                        ├──→ Shopify Import (GoHeadCase)
                                    │                        ├──→ Target+ Feed
                                    │                        ├──→ Walmart Priority List
                                    │                        └──→ DTC Microsites
                                    │
                              Sales Dashboard V2
                              (Design Rankings, Concentration,
                               Regional, Opportunities tabs)
```

## 6. Key Findings So Far

### From Atlas — Amazon US Session Analysis (Mar 7)
1. **Desk mats are tier-1 hardware** — HDMWH dominates top 50 by revenue. Naruto + Harry Potter desk mats = top sellers.
2. **Traffic black holes exist** — Console skins (Switch, Steam Deck) pulling 1,000-2,400 sessions with <1% conversion. Listing quality audit needed.
3. **Legacy devices are goldmines** — iPhone 12/13/14 converting at 7-9% with anime licenses. Don't sunset.
4. **Buy Box bleed on FHC line** — 63.6% Buy Box. Potential hijackers or pricing issues. Immediate audit.
5. **Top 100 Opportunity Score SKUs identified** — ready for prioritized action.

### From Atlas — Design Revenue Rankings (Mar 7)
1. **Top design:** HPOTDH37 (Harry Potter) — $122.5K
2. **Top 5:** Harry Potter, Peanuts (x2), Harry Potter #2, Barcelona
3. **Elbow point:** 216 designs — marginal contribution < 0.1% beyond that
4. **Top 200 designs = 63.59% of total revenue**
5. **Revenue concentration is steep** — classic long tail, Pareto heavy

### From BigCommerce Catalog (Mar 7)
- 408K active product variants extracted (from 50GB source)
- Parsed into: product_type_code, device_code, design_code, design_variant
- Loading to Supabase `bc_products` table with indexes
- Enables: catalog completeness checking, gap analysis, Shopify export generation

## 7. Output Spec

### PIE Scored SKU List (the deliverable)
For each selected SKU:
- `sku` — our SKU code
- `design_code` — parent design
- `brand` — license/brand
- `product_type_code` — case type
- `device_code` — device model
- `revenue_score` — normalized revenue rank (0-100)
- `opportunity_score` — sessions × conversion × buy box (0-100)
- `completeness_score` — how complete is this design's product type matrix (0-100)
- `composite_score` — weighted combination
- `tier` — A / B / C
- `channels` — which channels this SKU should be listed on (Target+, Walmart, Amazon FBA, DTC)
- `flags` — 🆕 New Entrant, 🔥 Surging, 💀 Dead on Arrival, 🏆 Hero SKU, ⚠️ Buy Box Risk

### Channel-Specific Outputs
- **GoHeadCase Shopify CSV** — filtered by composite score, formatted for Shopify import
- **Target+ Feed** — excludes US sports, includes GTIN/barcode
- **Walmart Priority List** — top 1000 for review velocity campaign
- **Amazon FBA Candidates** — high-session, high-conversion FBM SKUs to convert

## 8. Success Metrics

| Metric | Target |
|--------|--------|
| Revenue coverage | Selected 200K SKUs ≥ 95% of historical revenue |
| Collection completeness | ≥ 90% of designs across all 4 core product types |
| Device family coverage | 100% family completeness for top 50 devices |
| Regional optimization | US and UK device mixes differ by ≥ 15% |
| Time to first scored output | 1 week from today (Mar 14) |

## 9. Immediate Next Steps

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1 | Full design-level revenue query against BQ (2.8M orders, all time) | Atlas | 🔵 Ready to dispatch |
| 2 | Cross-reference BC catalog × BQ orders (which products sell vs exist) | Pixel + Atlas | 🔵 After BC load completes |
| 3 | Build composite scoring engine (combine all 6 layers) | Ava + Atlas | 🔵 After steps 1-2 |
| 4 | Add PIE tabs to Sales Dashboard V2 | Codex | 🟡 Re-dispatch needed |
| 5 | Deploy updated dashboard to Cloud Run | Harry | ⏳ After step 4 |
| 6 | Generate first scored SKU list (v0.1) | Atlas | 🔵 After step 3 |
| 7 | Cem review of v0.1 output + calibration | Cem | ⏳ After step 6 |
| 8 | Generate Shopify import CSV for GoHeadCase | Pixel | ⏳ After step 7 |

## 10. What Changed from v1 → v2

| Item | v1 (Mar 7 AM) | v2 (Mar 7 PM) |
|------|---------------|---------------|
| BQ access | 🔴 No auth | ✅ 2.8M orders, live |
| Order data | 304K (Supabase, stale) | 2.8M (BQ live) + Supabase syncing daily |
| FX normalization | 🔴 No net_sale_usd | ✅ Harry added column + fx_rates_daily |
| Amazon sessions | 🔴 Not available | ✅ 80K rows analyzed, opportunity scores done |
| BC catalog | 🔴 Not connected | ✅ 408K variants parsed, loading to Supabase |
| Agent team | Atlas + Prism | Atlas + Prism + **Pixel** (new, data processing) |
| Dashboard | Separate app planned | **Tabs in existing** Sales Dashboard V2 |
| BQ project | Unknown | `instant-contact-479316-i4` (15 datasets, incl headcase product master) |
| Design rankings | Not run | ✅ Top 200 = 63.59%, elbow at 216 |
| BQ→Supabase sync | Manual one-time | ✅ Automated daily cron (Harry) |

---

*v2 by Ava (CPSO) | 2026-03-07 16:15 EST*  
*"PIE defines what we sell. Everything else is distribution."*
