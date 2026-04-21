# Handoff: Procurement System Build

**From:** Ava | **To:** Harry | **Date:** 2026-03-20 | **Priority:** P1

## What
Build the Procurement System per `PROCUREMENT_SYSTEM_SPEC.md` (in this folder).

## Phase 1 — Start Here (Week 1)
1. **Create `supplier_currency_map` table in Supabase** — pre-populate with confirmed currencies:
   - RMB: ECELLSZ, XINTAI, YIZE, SHENG, JIZHAN, QICAI
   - USD: SAIBORO, BAOLLY, TOKO, SANXING
   - GBP: KOCH MEDIA, MAINLINE
2. **Build velocity calculator** — 7-day rolling sales by region (Buyer_Country) by item_code from BQ orders view
3. **Build reorder trigger** — items where `Free_Stocks < Reorder_Level` AND `On_Order = 0`
4. **Cost lookup function** — pull most recent `f_buying_price` from `t_purchase_order_return_line` per item. Pair with `supplier_currency_map` for currency. Do NOT use `t_mfg_supplier_price` — it's stale.

## Phase 2 — PO Generator (Week 2)
- Split algorithm: velocity ratios per destination (US/UK/PH) with PH capacity cap
- Generate separate POs per supplier × destination
- Include last PO price + currency on each line
- Output: JSON + printable PDF

## Phase 3 — China Receiving UI (Week 3)
- Simple Next.js page on Supabase
- Outstanding POs list → receive goods → ship to destination
- Replaces Zero's PO receiving screen

## Key Data
- BQ inventory view: `zero_dataset.inventory` (real-time, confirmed working today)
- PO tables: `elcell_co_uk_barcode.t_purchase_order_return` + `_return_line`
- Orders: `zero_dataset.orders` (has Buyer_Country for split calc)
- Full spec has all table schemas, supplier details, confirmed pricing

## Don't
- Don't use `t_mfg_supplier_price` for costs (stale — shows HTPCR at ¥1.80, actual is ¥3.50-5)
- Don't use `PO_Location` for splits — use `Buyer_Country`
- Don't build full COGS dashboard yet (Phase 4, Ava owns)
