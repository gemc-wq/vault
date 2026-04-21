# PULSE Dashboard (Product Uplift & Listing Signal Engine)
> **Owner:** Ava | **Status:** LIVE | **Updated:** 2026-03-18

## URLs
- **V2 (current):** https://pulse-dashboard-v2.vercel.app
- **V1 (legacy):** https://pulse-dashboard-inky.vercel.app
- **Repo:** github.com/gemc-wq/pulse-dashboard-v2

## What It Does
Velocity-driven product intelligence dashboard for Ecell Global.
- **Leaderboard:** Top designs, devices, product types by revenue (with regional filters US/UK/EU)
- **Champions:** Individual child design rankings with velocity indicators
- **Gap Analysis:** Cross-region gaps — designs selling in one region but absent from another's top 200
- **Elbow Detection:** Automatic optimal SKU count calculation (80% revenue coverage point)

## Data Sources
- **BQ orders** via Supabase RPC functions (get_leaderboard, get_champion_designs, get_device_leaderboard)
- **Region:** Uses `buyer_country` not `po_location`
- **SKU parsing:** `SPLIT(Custom_Label, '-')` with F-prefix FBA merge rule

## Key Decisions
- **Champion selection = COMBINED back case revenue** (HTPCR + HC + HB401) — never HTPCR alone
- Combined elbow: 590 designs = 80% of $440K US back case revenue
- Gap finder compares top-200 sellers per region (NOT marketplace listings)
- Label "Missing In" should be updated to "Outside Top 200" — misleading (2026-03-14)
- Product group filtering required — don't mix desk mats with phone cases in rankings
- Each product group has its own elbow (back cases, desk mats, skins, wallets, gaming)

## Stack
- Next.js 14, TypeScript, Tailwind, Recharts
- Supabase (RPC functions) + BQ (via GCP service account)
- Vercel deployment (ecells-projects-3c3b03d7)

## Related
- Conversion Dashboard: `projects/conversion-dashboard/` — Amazon sessions/conversion data
- PRUNE App: `projects/prune-app/` — dead weight catalog analysis
