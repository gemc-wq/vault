# PRUNE — Product Retirement & Unused iNventory Engine

> **Status:** Project Brief (v1)  
> **Created:** 2026-03-11  
> **Owner:** Ava  
> **Priority:** P0 (cost reduction — runs parallel to PULSE)  
> **Cem Directive:** Separate from PULSE. PULSE = uplift/growth. PRUNE = trim dead weight.

---

## Mission

Identify, quantify, and retire dead/underperforming Amazon listings to reduce volume fees, simplify catalog management, and focus production resources on revenue-generating SKUs.

## Problem Statement

- **3.4M active Amazon US listings** — 92.9% had zero sales in 6 months
- **845 designs** with ZERO sales in 12 months (255K listings) — all 4+ years old
- **~$66K/year** estimated volume fees on dead inventory generating <$22K revenue
- **20 entire brands/licenses** with zero sales across ALL lineups
- **574 dead product_type × device combos** (stockable units with no sales)
- Catalog bloat makes analytics, listing management, and team focus harder

## Data Sources

| Source | Location | Size | Purpose |
|--------|----------|------|---------|
| Active Listings (US) | BQ: `zero_dataset.amazon_active_listings` | 3.4M rows | Current catalog |
| Active Listings (UK) | GDrive → pending BQ load | ~9GB | UK catalog |
| Active Listings (DE) | GDrive → pending BQ load | TBD | DE catalog |
| Orders (all) | BQ: `zero_dataset.orders` | 2.8M rows | Sales history |
| Orders (Supabase) | `orders` table | 305K rows | Dashboard queries |
| Headcase Master | BQ: `headcase.tblLineups`, `tblDesigns` | 10K lineups, 110K designs | Brand/license mapping |
| Conversion Data | Supabase: `amazon_conversion_data` | 457K rows | Sessions, page views, Buy Box % |

## Analysis Framework (Hierarchy)

Cem's directive: analyze top-down, not bottom-up.

### Level 1: Marketplace
- Separate analysis per marketplace (US, UK, DE/EU)
- Each marketplace has its own Active Listings file and fee structure

### Level 2: Brand / License
- Identify **entire brands** with zero/negligible sales → candidate for full license retirement
- 20 brands with 100% dead lineups already identified (16K listings)
- Partial dead brands: HCD Custom (51% dead), Monika Strigel (38% dead)

### Level 3: Lineup (Design Collection)
- 507 dead lineups → 98K listings
- Top: WWE New Day (2,155 listings, $0), Nature Magick Floral Black Monogram (1,379), Haroulita Abstract Glitch (1,280)
- Cross-reference with lineup creation date to exclude launches < 90 days

### Level 4: Product Type × Device (Stockable Unit)
- 574 dead combos → 10,694 listings
- CH8939/CH8940 console accessories (~3K listings, all 2021)
- Dead devices: RAZR2022 (13,604 listings), old buds/watch models

### Level 5: Individual Design
- 845 designs with ZERO sales 12mo (255K listings)
- 763 designs with <$50 12mo revenue (389K listings)
- Worst: WYANOWL (3,575 listings, $46/6mo), ANICLUPET (3,495 listings, $48/6mo)

## Key Metrics

| Metric | 6-Month | 12-Month |
|--------|---------|----------|
| Dead designs ($0) | 1,277 (492K listings) | 845 (255K listings) |
| Micro designs (<$10) | 96 (34K listings) | 101 (27K listings) |
| Low designs ($10-50) | 826 (610K listings) | 763 (389K listings) |
| Active designs ($200+) | 1,088 (1.4M listings) | 1,526 (1.96M listings) |
| Dead device listings | 16,102 | 16,102 |
| Dead brand listings | ~16,000 | ~16,000 |
| Dead lineup listings | ~98,000 | ~98,000 |

## Retirement Tiers (Risk-Ordered)

### Tier 1: Immediate (Zero Risk) — ~16K listings
- 20 brands with 100% dead lineups
- All listings 4+ years old, zero sales in 12 months
- Action: Close all listings, no review needed

### Tier 2: Quick Win (Low Risk) — ~98K listings  
- 507 dead lineups (zero sales 12mo, listed 90+ days)
- Includes dead lineups from otherwise-active brands (WWE New Day, etc.)
- Action: Close listings, flag lineup for design team review

### Tier 3: Deep Clean (Medium Risk) — ~11K listings
- 574 dead PT × device combos
- Requires checking if device is truly obsolete vs. seasonal
- Action: Verify device is discontinued, then close

### Tier 4: Low Performers (Needs Review) — ~389K listings
- 763 designs with <$50 revenue in 12 months
- Some may be worth keeping (seasonal, new devices launching)
- Action: Review, score, then close if below threshold

## Fee Impact Estimate

| Category | Listings | Est. Annual Volume Fee | Revenue Generated | Net Impact |
|----------|----------|----------------------|-------------------|------------|
| Tier 1 (dead brands) | 16K | ~$10K | $0 | **-$10K saved** |
| Tier 2 (dead lineups) | 98K | ~$59K | $0 | **-$59K saved** |
| Tier 3 (dead combos) | 11K | ~$7K | $0 | **-$7K saved** |
| Tier 4 (low performers) | 389K | ~$233K | $21K | **-$212K saved** |
| **TOTAL** | **514K** | **~$309K** | **$21K** | **~$288K saved** |

*Fee estimate: conservative $0.005/listing/month based on Amazon's high-volume listing fee structure*

## Dashboard Spec (PRUNE App)

### Views
1. **Overview** — summary cards: total dead listings, fee impact, retirement tiers
2. **Brand View** — table of brands with % dead, total listings, recommendation (RETIRE / REVIEW / KEEP)
3. **Lineup View** — drill-down from brand to individual lineups, sorted by dead listing count
4. **Device View** — obsolete devices with listing counts, last sale date
5. **Export** — CSV generator for listings team: SKU, ASIN, action (CLOSE / REVIEW)

### Filters
- Marketplace (US / UK / DE / All)
- Lookback period (6mo / 12mo)
- Tier (1 / 2 / 3 / 4 / All)
- Brand / License

### Design
- Light theme (match PULSE: white bg, cobalt accents, black text)
- Desktop-first, responsive
- Same font stack as Sales Dashboard V2

## Build Plan

| Phase | Task | Agent | Target |
|-------|------|-------|--------|
| 1 | Create Supabase views for dead inventory | Ava | Mar 11 |
| 2 | Scaffold PRUNE app (Next.js) | Forge/Codex | Mar 12 |
| 3 | Wire views to Supabase | Forge/Codex | Mar 13 |
| 4 | CSV export functionality | Forge/Codex | Mar 13 |
| 5 | Deploy to Vercel | Ava | Mar 14 |
| 6 | UK/DE data integration | Ava | When files available |

## Dependencies
- [ ] UK/DE Active Listings files (Cem downloading, ~9GB each)
- [ ] Codex CLI OAuth refresh (for builds)
- [ ] Amazon fee schedule confirmation (for accurate fee estimates)
- [ ] Cem review of Tier 4 threshold (currently $50/12mo — adjust?)

## Queries (Validated, Ready to Use)

### Dead designs (12mo)
```sql
-- Server: BigQuery (instant-contact-479316-i4)
WITH sold AS (
  SELECT DISTINCT SPLIT(Custom_Label, '-')[SAFE_OFFSET(2)] as dc
  FROM zero_dataset.orders
  WHERE Paid_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
    AND Marketplace LIKE '%mazon%'
)
SELECT dc, listings, latest
FROM listed LEFT JOIN sold ON listed.dc = sold.dc
WHERE sold.dc IS NULL AND latest < DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
```

### Dead brands (all lineups dead)
```sql
-- Brands where EVERY lineup has zero sales in 12 months
-- 20 brands identified, ~16K listings
-- See memory/2026-03-11.md for full list
```

### Dead PT × Device combos
```sql
-- 574 combos, 10,694 listings
-- JOIN sold_combos (pt, device from orders) with listed_combos (from active listings)
-- Filter: zero sales, listed 90+ days
```

---

*Created by Ava, 2026-03-11 00:40 AM*  
*Data validated against BigQuery (2.8M orders) and Supabase (305K orders)*
