# 2026-04-04

**Decisions**
- **Stock-out Monitoring Sources (per Cem):**
    - China: `cn.ben@foxmail.com` (Mandarin/Cantonese)
    - PH: `C.yunnun@ecellglobal.com` (Tagalog/English)
    - UK: `A.faulder@ecellglobal.com`, `d.migo@ecellglobal.com` (English)
    - FL: `c.rueda@ecellglobal.com` (Spanish/English)
    - Slack: `us-production-group`, `eod`, `printing`
- **UI Requirement:** App interface must support multi-lingual support (EN, ZH, ES, TL).

**Deliverables**
- **Finance Middleware Database Schema:** Created `sql/finance_middleware_schema.sql` (includes `purchase_orders`, `po_line_items`, `packing_lists`, `supplier_invoices`, `goods_receipts`, `stock_out_alerts`, `inventory_snapshots`, and `suppliers`).
- **Migration Script Update:** Updated `tmp/procurement-system/lib/migrate.ts` (executable via `npx ts-node lib/migrate.ts`).
- **Stock-Out Email Monitor:** Created `scripts/stock_out_airweave_monitor.mjs` (uses Airweave semantic search to parse SKUs, cross-reference Supabase, and trigger Telegram notifications).
- **BigQuery Sync Update:** Updated `scripts/bq_to_supabase_inventory_sync.mjs` with new alert logic.
- **Setup Documentation:** Created `outputs/inventory_control_setup_summary.md` (covers architecture, env vars, and cron recommendations).

**Blockers**
- `gog` authentication for Gmail access is pending.
- Xero US Write authentication is pending.
- Database migrations are pending execution.

**Knowledge**
- **Inventory Traffic Light Logic:**
    - **BLACK:** `free_stocks` = 0
    - **RED:** `days_of_stock` < 14
    - **YELLOW:** `days_of_stock` < 21
    - **GREEN:** `days_of_stock` >= 21

**Carry-forwards**
- Run database migrations.
- Set up `gog` Gmail authentication.
- Deploy updated inventory app with new traffic light levels.
- Complete Xero finance plugin authentication.