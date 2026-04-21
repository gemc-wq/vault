# 2026-04-04

**Decisions**
- **Stock-out Monitoring Sources (per Cem):**
    - China: `cn.ben@foxmail.com`
    - PH: `C.yunnun@ecellglobal.com`
    - UK: `A.faulder@ecellglobal.com`, `d.migo@ecellglobal.com`
    - FL: `c.rueda@ecellglobal.com`
    - Slack: `#us-production-group`, `#eod`, `#printing`
- **UI Requirement:** App interface must support multi-lingual support (EN, ZH, ES, TL).

**Deliverables**
- **Finance Middleware Database Schema:** Created `sql/finance_middleware_schema.sql` (includes `purchase_orders`, `po_line_items`, `packing_lists`, `supplier_invoices`, `goods_receipts`, `stock_out_alerts`, `inventory_snapshots`, and `suppliers`).
- **Migration Script Update:** Updated `tmp/procurement-system/lib/migrate.ts` (executable via `npx ts-node lib/migrate.ts`).
- **Stock-Out Email Monitor:** Created `scripts/stock_out_airweave_monitor.mjs` (uses Airweave semantic search to parse SKUs, cross-reference Supabase, and trigger Telegram notifications).
- **BigQuery Sync Update:** Updated `scripts/bq_to_supabase_inventory_sync.mjs` with new alert logic.
- **Setup Documentation:** Created `outputs/inventory_control_setup_summary.md` (covers architecture, env vars, and cron recommendations).

**Blockers**
- Pending authentication: `gog` (Gmail access) and Xero US Write.
- Database