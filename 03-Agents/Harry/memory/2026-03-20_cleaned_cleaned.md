# Memory — 2026-03-20

## Decisions
- **COGS Confirmation (Cem)**: Updated rates confirmed: HTPCR/XINTAI (¥3.50 RMB), HB6/HB7 ($1.90 USD), and HB401/ECELLSZ (¥6.50 RMB).
- **Data Source of Truth**: `t_purchase_order_return_line.f_buying_price` is the official source for unit cost.

## Deliverables
- **Procurement System (Phase 1 LIVE)**: 
    - URL: https://procurement-system-one.vercel.app
    - Supabase ID: `auzmjawughepxbtwuhe` (Stack: Next.js 16 / Tailwind / pg)
    - Features: Dashboard (inventory alerts), Inventory table, Reorder engine, and PO workflow (supplier × warehouse split).
- **Database Schema Updates**: Created `supplier_currency_mapping`, `reorder_suggestions`, `po_batches`, `po_supplier_orders`, and `po_order_lines`.
- **QMD Memory