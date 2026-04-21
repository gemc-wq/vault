# Handoff from Ava → Harry
**Date:** 2026-03-07 13:10 EST
**Priority:** P0 — Blocks all analytics

---

## TASK: BigQuery → Supabase Daily Sync

### Context
Supabase `orders` table has 304K rows but data ends at **2026-02-17** (18 days stale). It was a one-time BQ export. We need a daily automated sync so analytics are always fresh. This blocks PIE, Sales Dashboard V2, and all SKU selection work.

### What's Done
- `gcloud` CLI installed on Mac Studio (v559.0.0)
- **Auth still needed:** `gcloud auth login --project=opsecellglobal` (Cem can help with OAuth)
- Supabase schema documented, Atlas agent configured with full column mappings
- SOP written: `wiki/02-sales-data/SOP_SALES_ANALYTICS.md` (in Ava's workspace on Mac Studio)

### Supabase Connection
- URL: https://auzjmawughepxbtpwuhe.supabase.co
- Service Key: [REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc

### Existing Schema (orders table)
Pre-parsed columns already exist — DON'T re-create:
- `custom_label` (full SKU), `product_type_code`, `device_code`, `design_code`, `design_variant`
- `paid_date`, `dispatch_date`, `net_sale`, `currency`, `buyer_country`
- `marketplace`, `brand`, `status`, `is_refunded`, `source`
- Unique key: `sales_record_number`

### What Needs Building
1. **gcloud auth** on Mac Studio (or wherever sync runs)
2. **Discover BQ schema:** `bq ls opsecellglobal` → find the orders dataset/table
3. **Add `net_sale_usd` column** to Supabase orders table:
   - GBP→1.27, EUR→1.09, JPY→0.0067, AUD→0.65, SEK→0.096, PLN→0.25, CAD→0.73, CHF→1.13
4. **Sync script:** BQ query → upsert into Supabase (incremental, not full replace)
   - Use `sales_record_number` as unique key
   - Only pull rows where paid_date > last sync date
5. **Cron:** 2 AM EST daily
6. **Also needed:** Fix Walmart listings pagination (only 10K of 95K loaded)

### Additional Context
- Atlas agent (Gemini 3.1 Pro) is now purpose-built for ecommerce analytics — his SOUL.md and MEMORY.md are on Mac Studio at `~/.openclaw/workspaces/atlas/`
- Sales Dashboard V2 is being built by Codex right now (Next.js + Supabase + Recharts)
- 4-pillar strategy approved: Sales → Production → Operations → Growth (full doc: STRATEGY.md in Ava's workspace)
- Wiki of 53 operational docs centralized in Ava's workspace at `wiki/`

### Cem's Key Requirements (from today)
- Multi-lookback analysis (1mo/3mo/6mo/all-time) — new licenses like Naruto/NBA are underweighted in all-time data
- Regional reports for marketplace-specific SKU selection (OnBuy UK, Kaufland Germany)
- Currency normalization as a permanent column, not on-the-fly

---
*Written by Ava | Mac Studio (cems-mac-studio)*
