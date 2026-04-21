# Skill: Intelligence & Analytics
**Weight: 5% | Heartbeat: 1x per 2 cycles | Agent: Hermes (Gemma 4 / Kimi K2.5)**

---

## Why 5%
Analytics informs decisions but doesn't drive revenue directly. It's infrastructure — embedded in every other skill rather than consuming standalone attention. Check it least frequently but ensure the data pipelines are running.

## Scope
- PULSE Dashboard (velocity, trending designs)
- Conversion Dashboard (CVR by product, device, marketplace)
- BigQuery reporting and data pipelines
- Weekly Listing Intelligence (automated audit)
- Product Intelligence Engine (PIE — algorithmic SKU selection)
- BQ → Supabase sync monitoring

## Active Projects
| Project | Status | Priority |
|---------|--------|----------|
| PULSE Dashboard v2 | 🟢 Live on Vercel | Maintenance |
| Conversion Dashboard | 🟢 Built | Maintenance |
| Weekly Listing Intelligence | 🟢 Running | Maintenance |
| PIE (Product Intelligence) | 🟡 Concept stage | P2 |
| BQ Orders Sync | 🟢 Nightly cron (Harry's iMac) | Maintenance |
| ASIN→SKU Bridge | 🟢 3.43M mappings | Maintenance |
| Amazon Prime shipping analysis | 🔴 Needs data pull | P1 (feeds Sales skill) |

## Key Metrics
- BQ sync: running nightly? Last successful run date.
- PULSE: top 10 velocity designs this week
- Conversion: US 30d CVR (baseline 2.89%)
- Listing delta: new vs removed vs changed since last week
- Data freshness: how old is the latest order data in Supabase?

## Data Infrastructure
- **BigQuery:** headcase dataset (master: tblDesigns, tblLineups, tblDevices)
- **Supabase:** Unified Product DB (lineups 10,279 | designs 110,634 | products 90,661 | marketplace_listings 467,392)
- **Local SQLite:** 8.5M rows (US 3.44M + UK 5.1M)
- **BQ→Supabase sync:** Harry's iMac cron, upsert with on_conflict=sales_record_number

## Context
- HB401 converts 4x higher than HTPCR (12.46% vs 2.96%)
- Best sellers ≠ best converters (zero overlap in top 10)
- Top 50 lineups = 44.6% revenue
- 590 champion designs cover 80% of back case revenue
- Dynamic pricing candidates: 30 Stars (price up), 13 Q-Marks (price down), 7 Cash Cows (PPC boost)
