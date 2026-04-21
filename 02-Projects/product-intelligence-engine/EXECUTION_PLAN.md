# PIE Execution Plan — Sprint to v0.1
**Created:** 2026-03-07 17:38 EST  
**Target:** First scored output by March 14, 2026

---

## Phase 0: Data Foundation (Mar 7-8) — IN PROGRESS

| # | Task | Owner | ETA | Status |
|---|------|-------|-----|--------|
| 0.1 | BQ → Supabase daily sync + FX + net_sale_usd | Harry | ✅ Done | ✅ |
| 0.2 | BigCommerce catalog → Supabase `bc_products` | Pixel | Mar 7 | 🔵 Running |
| 0.3 | Amazon Active Listings → BQ (ASIN→SKU bridge) | Ava (BQ direct) | Mar 10 | ✅ Done — 3,441,323 rows in `zero_dataset.amazon_active_listings` |
| 0.4 | Amazon US Sessions (80K) analyzed | Atlas | ✅ Done | ✅ |
| 0.5 | gcloud auth on Mac Studio | Cem + Ava | ✅ Done | ✅ |

## Phase 1: Core Analysis (Mar 8-10)

| # | Task | Owner | Depends On | Status |
|---|------|-------|-----------|--------|
| 1.1 | Design-level revenue rankings (full BQ, 2.8M orders, multi-lookback) | Ava (BQ direct) | 0.1 | ✅ Done Mar 9 — `results/pie-phase1.1-design-revenue-rankings.md` |
| 1.2 | Product type gap analysis (design coverage within addressable device sets) | Ava (BQ direct) | 0.3 | ✅ Done Mar 10 — `results/pie-phase1.2-gap-analysis.md` |
| 1.3 | Conversion benchmarking by design/device/product_type (Layer 7) | Atlas | 0.3, 0.4 | 🔵 Ready — ASIN→SKU bridge in BQ |
| 1.4 | Collection completeness audit (each design × core product types) | Atlas + Pixel | 0.2 | ⏳ After BC load |
| 1.5 | Device family coverage check (top 50 devices, full families) | Atlas | 0.2 | ⏳ After BC load |

## Phase 2: Dashboard (Mar 8-10, parallel)

| # | Task | Owner | Depends On | Status |
|---|------|-------|-----------|--------|
| 2.1 | Add PIE tabs to Sales Dashboard V2 (Design Rankings, Concentration, Regional, Opportunities) | Codex | Repo cloned | 🔵 Re-dispatch tonight |
| 2.2 | Deploy updated dashboard to Cloud Run | Harry | 2.1 | ⏳ |
| 2.3 | Add conversion benchmark views (Layer 7 quadrant) | Codex | 1.3 | ⏳ |

## Phase 3: Scoring Engine (Mar 10-12)

| # | Task | Owner | Depends On | Status |
|---|------|-------|-----------|--------|
| 3.1 | Build composite scoring formula (revenue × conversion × completeness × coverage) | Ava + Atlas | 1.1-1.5 | ⏳ |
| 3.2 | Apply brand tiering (A/B/C) | Atlas | 3.1 | ⏳ |
| 3.3 | Apply channel rules (Target+ sports exclusion, FBA candidates) | Atlas | 3.2 | ⏳ |
| 3.4 | Regional split (US vs UK device mixes) | Atlas | 3.2 | ⏳ |
| 3.5 | Generate scored SKU list v0.1 (~200K SKUs) | Pixel | 3.1-3.4 | ⏳ |

## Phase 4: Review & Output (Mar 12-14)

| # | Task | Owner | Depends On | Status |
|---|------|-------|-----------|--------|
| 4.1 | Cem reviews v0.1 scored output | Cem | 3.5 | ⏳ |
| 4.2 | Calibrate scoring weights based on Cem feedback | Ava | 4.1 | ⏳ |
| 4.3 | Generate Shopify import CSV (GoHeadCase) | Pixel | 4.2 | ⏳ |
| 4.4 | Generate Target+ feed (excl US sports) | Pixel | 4.2 | ⏳ |
| 4.5 | Generate Walmart priority list (top 1000 for review velocity) | Pixel | 4.2 | ⏳ |
| 4.6 | Generate Amazon FBA candidate list | Pixel | 4.2 | ⏳ |

## Phase 5: Additional Data (Mar 8+, as Cem provides)

| # | Task | Owner | Status |
|---|------|-------|--------|
| 5.1 | UK Amazon session report upload | Cem | ⏳ Cem pulling |
| 5.2 | DE Amazon session report upload | Cem | ⏳ Cem pulling |
| 5.3 | Amazon Ads keyword reports | Cem | ⏳ Phase 2 layer |
| 5.4 | Target+ item export from Partner Portal | Cem | ⏳ |
| 5.5 | SP-API weekly cron (US/UK/DE active listings) | Harry | ⏳ After manual pipeline proven |

## Critical Path

```
Active Listings loaded (0.3)
        ↓
Gap Analysis + Conversion Benchmarks (1.2, 1.3)
        ↓
Scoring Engine (3.1-3.4)
        ↓
Scored SKU List v0.1 (3.5)
        ↓
Cem Review (4.1) → Calibrate → Ship feeds (4.3-4.6)
```

**Blocker:** Nothing is blocked. All data either exists or has a named owner pulling it.  
**Risk:** Amazon Active Listings file is 6.8GB — download/processing time. Harry should prioritize this.

---

*"PIE defines what we sell. Everything else is distribution."*
