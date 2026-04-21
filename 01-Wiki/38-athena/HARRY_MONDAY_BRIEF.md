# Harry Monday Brief — Apr 7, 2026
**From:** Ava (Strategy)
**To:** Harry (COO)
**Priority:** P0

---

## MAIN DELIVERY THIS WEEK: Inventory Alert System by Office

**Cem's exact requirement:**
> Inventory alerts by office, with full inventory order-to-receive tracking, in multilingual format.

This is NOT the Xero finance app. That is secondary. This is the **inventory control tower** — the thing that tells each office when stock is low, what's on order, what's in transit, and what needs reordering. In the language of the person reading it.

---

## What you've already built (keep it, build on top):

✅ `blank_inventory` table + `v_inventory_alerts_v2` view in Supabase  
✅ Stock-out Airweave monitor (`scripts/stock_out_airweave_monitor.mjs`)  
✅ Procurement system Next.js app (`tmp/procurement-system/`)  
✅ Finance middleware DB schema (11 tables: POs, packing lists, GRNs, invoices, alerts)  
✅ PH order gap analysis (11 EOL items to cut, negative qty error flagged)  
✅ Traffic light thresholds confirmed by Cem: RED <14d / AMBER <21d / GREEN 21d+

---

## SPEC: Inventory Alert System v1

### Core behaviour
Each office (UK, PH, FL) gets a **daily alert** — in their language — that shows:

1. **RED/AMBER items** = stock running out (< 21 days cover)
2. **On order** = what's already been ordered, expected arrival
3. **In transit** = what's shipped from China but not received yet
4. **What to reorder** = recommended qty based on weighted 7d/30d velocity

### Output format options (choose one per office):
- **Telegram message** (Ava can relay for Cem, direct for others if bot added)
- **Slack post** to #eod or dedicated #stock-alerts channel
- **Email** to office manager

### Languages:
| Office | Manager | Language |
|--------|---------|----------|
| UK | Andrew Faulder, Davy Migo | English |
| PH | Chris Yunnun, Jay Mark | Tagalog / English |
| FL | Chris Rueda | Spanish / English |
| CN (supplier) | Ben (cn.ben@foxmail.com) | Mandarin |

SKU codes are language-agnostic. Translate: product descriptions, status labels (Out of Stock → "Sin stock" / "Walang stock"), instructions.

### Alert structure per office (example — UK, English):
```
📦 UK Inventory Alert — Monday 7 April

🔴 CRITICAL (< 14 days stock)
  HTPCR-IPH16PMAX  |  12 units  |  4.2 days  |  On order: 200 (ETA Apr 12)
  HLBWH-S928U      |  3 units   |  1.1 days  |  NOT ordered ⚠️

🟡 LOW (< 21 days stock)
  HB401-IPH15PRO   |  45 units  |  18 days   |  On order: 0
  HTPCR-IPH17      |  22 units  |  16 days   |  On order: 50 (ETA Apr 10)

✅ Reorder Recommendations:
  HLBWH-S928U      →  Order 100 (7-day velocity: 2.7/day)
  HB401-IPH15PRO   →  Order 60

Next full report: Tomorrow 8 AM
```

### Velocity calculation (per PROJECT.md spec):
- `daily_velocity_7d = sales_last_7d / 7`
- `daily_velocity_30d = sales_last_30d / 30`
- `weighted = (velocity_7d × 0.7) + (velocity_30d × 0.3)`
- `days_of_stock = free_stock / weighted_velocity`
- Velocity anomaly flag when 7d differs from 30d by >35%

---

## BUILD PLAN (Monday → Wednesday target)

### Day 1 (Mon): Data layer
1. Run `sql/finance_middleware_schema.sql` migrations on Supabase (already written)
2. Verify `bq_to_supabase_inventory_sync.mjs` is pulling correct columns (note: use `f_SageStockCode` not `f_DeviceCode` for UK stocks)
3. Confirm `blank_inventory` has current data for all 3 offices
4. Add `on_order_qty`, `in_transit_qty` columns if not present (link to `purchase_orders` / `packing_lists` tables)

### Day 2 (Tue): Alert generation
1. Build `scripts/generate_inventory_alert.mjs`:
   - Queries Supabase for RED/AMBER items per office
   - Pulls on-order and in-transit from `purchase_orders` / `packing_lists`
   - Calculates weighted velocity + days_of_stock
   - Generates alert text in EN / ES / TL (Mandarin for CN if needed)
2. Test alert output for each office — check it reads correctly
3. Wire Telegram notification (Ava's bot token is in `.env`)

### Day 3 (Wed): Cron + UI
1. Add to cron schedule: daily 8 AM per timezone (UK 8 AM BST, PH 8 AM PHT, FL 8 AM EDT)
2. Update procurement-system app dashboard to show live traffic lights per office
3. Add `/inventory/uk`, `/inventory/ph`, `/inventory/fl` pages (spec already in wiki/inventory-ordering-app/PROJECT.md)

---

## SECONDARY: Xero OAuth (do AFTER inventory alerts shipped)

Harry needs help completing Xero auth for UK + US orgs.

**Step-by-step (Cem to do):**
1. Go to https://developer.xero.com/myapps
2. Click your app → copy **Client ID** and **Client Secret** (for both UK and US Xero organisations)
3. Send Cem the client ID + secret via Telegram (Ava will forward to Harry securely)
4. Harry runs `node scripts/exchange-xero-code.js` to complete the OAuth flow
5. Tokens stored locally — never in GDrive or MEMORY.md

If you don't have a Xero developer app set up yet:
- Create one at developer.xero.com → "New App" → "Web app"
- Redirect URI: `http://localhost:3000/callback`
- Scopes needed: `accounting.transactions`, `accounting.contacts`, `accounting.settings`, `offline_access`

---

## PO CORRECTIONS NEEDED BEFORE NEXT ORDER (from gap analysis)

**Cem action required:**
1. Remove 11 EOL items from current PH order (saves ¥1,000)
2. Fix HTPCR-IPH17PRO quantity (shows -163 — data error, confirm correct qty)
3. Approve shipping split: 70% PH / 15% UK / 15% FL direct from China (saves ~$1,014/PO)

---

*Brief by Ava | 2026-04-05 | Upload to `Brain/Agents/Harry/` on GDrive*
