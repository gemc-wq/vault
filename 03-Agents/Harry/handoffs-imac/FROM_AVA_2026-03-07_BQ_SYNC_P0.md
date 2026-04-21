# URGENT Handoff from Ava → Harry
**Date:** 2026-03-07 13:11 EST
**Priority:** P0 — Blocks ALL analytics, PIE, dashboard, SKU selection

---

## TASK: BigQuery → Supabase Daily Sync

### The Problem
Supabase `orders` table has 304K rows but data ends at **2026-02-17** (18 days stale). One-time export. Need daily automated sync.

### What's Ready on Mac Studio (cems-mac-studio / 100.72.19.27)
- gcloud CLI installed (v559.0.0) — needs `gcloud auth login --project=opsecellglobal`
- Cem available to help with OAuth right now

### Supabase Connection
- URL: https://auzjmawughepxbtpwuhe.supabase.co
- Service Key: [REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc
- GCP Project: opsecellglobal

### Orders Table Schema (already exists)
| Column | Type | Example |
|--------|------|---------|
| sales_record_number | text (UNIQUE KEY) | 111-7069086-6206626 |
| custom_label | text | HC-IPH15PMAX-HPOTDH9-HOG |
| product_type_code | text | HC |
| device_code | text | IPH15PMAX |
| design_code | text | HPOTDH9 |
| design_variant | text | HOG |
| paid_date | date | 2025-07-30 |
| dispatch_date | date | 2025-07-30 |
| net_sale | numeric | 10.65 |
| currency | text | USD |
| buyer_country | text | United States Of America |
| marketplace | text | Amazon |
| brand | text | Time Warner HARRY POTTER |
| status | text | Delivered |
| is_refunded | boolean | false |
| source | text | bigquery |

### Deliverables
1. **gcloud auth** on Mac Studio OR iMac (wherever sync will run)
2. **Find BQ dataset:** `bq ls opsecellglobal` → identify orders table
3. **Add net_sale_usd column:** ALTER TABLE orders ADD COLUMN net_sale_usd NUMERIC(12,4);
   - Rates: GBP=1.27, EUR=1.09, JPY=0.0067, AUD=0.65, SEK=0.096, PLN=0.25, CAD=0.73, CHF=1.13
4. **Incremental sync script:** BQ → Supabase upsert on sales_record_number
5. **Daily cron:** 2 AM EST
6. **Fix Walmart pagination:** Only 10K of 95K listings loaded

### Cem's Requirements
- Multi-lookback analysis needs fresh data (1mo/3mo/6mo)
- New licenses (Naruto, NBA) underweighted without recent data
- Regional reports needed for OnBuy (UK), Kaufland (Germany)
- Sales Dashboard V2 being built now (Codex) — needs live data

### Reference Docs (on Mac Studio at /Users/openclaw/.openclaw/workspace/)
- wiki/02-sales-data/SOP_SALES_ANALYTICS.md
- wiki/02-sales-data/SCHEMA_DESIGN.md
- STRATEGY.md (4-pillar framework)
- Atlas agent workspace: ~/.openclaw/workspaces/atlas/ (SOUL.md + MEMORY.md)

---
*From: Ava (Mac Studio) | To: Harry (iMac)*
*SSH: clawdbot@100.91.149.92 confirmed working*
