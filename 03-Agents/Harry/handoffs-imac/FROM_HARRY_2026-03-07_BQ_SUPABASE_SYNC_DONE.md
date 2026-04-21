# Harry → Ava: BQ → Supabase Sync + FX + net_sale_usd ✅
**Date:** 2026-03-07
**Priority:** P0 complete (foundation for analytics + PIE)

## What’s Done
1) **Supabase P2 schema**
- Added `orders.net_sale_usd NUMERIC(12,4)` ✅
- Created `public.fx_rates_daily` table ✅
  - Columns: rate_date, currency, rate_to_usd, source, inserted_at
  - PK: (rate_date, currency)

2) **FX backfill loaded**
- FX script executed successfully on iMac
- Backfilled **240 rows** covering **2026-02-25..2026-03-07** (USD + other currencies)
- Source: **frankfurter.app** (daily reference/average; Cem confirmed accuracy not critical)

3) **BQ → Supabase incremental orders sync working**
- Implemented Node script (uses `bq` CLI) to pull last **21 days** from:
  - `instant-contact-479316-i4.zero_dataset.orders` (VIEW)
- Computes `net_sale_usd` using Paid_Date + fx_rates_daily.rate_to_usd
- Ran once successfully: **Upserted 100 orders** (lookbackDays=21)

## Schedules (Cron)
- **FX daily refresh:** 01:30 AM ET
- **Orders sync:** 02:00 AM ET

## Files / Location (on iMac)
- SQL:
  - `~/.openclaw/workspace/sql/2026-03-07_fx_rates_daily.sql`
  - `~/.openclaw/workspace/sql/2026-03-07_orders_net_sale_usd.sql`
- Scripts:
  - `~/.openclaw/workspace/scripts/fx_rates_sync.mjs`
  - `~/.openclaw/workspace/scripts/bq_to_supabase_orders_sync.mjs`
  - `~/.openclaw/workspace/scripts/README_SYNC.md`

## Notes / Next Improvements (optional)
- Current sync uses **lookback window** (21d). Good enough for daily ops; can expand/backfill in batches later.
- FX provider is daily reference, not spot (OK per Cem).
- If Supabase API schema cache ever lags after DDL, restarting PostgREST / waiting a minute fixes.

— Harry ⚡
