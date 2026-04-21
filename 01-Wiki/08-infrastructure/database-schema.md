# database-schema
*Auto-created by vault compiler on 2026-04-13*

- **Source of Truth**: `t_purchase_order_return_line.f_buying_price` is the authoritative source for unit cost.
- **Deprecated/Avoid**: Do not use `t_mfg_supplier_price` for unit costs as it contains stale data (e.g., HTPCR showing ¥1.80 instead of the actual ¥3.50-5).
- **New Tables**:
- `supplier_currency_mapping` (mapping for 21 suppliers)
- `reorder_suggestions`
- `po_batches`
- `po_supplier_orders`
- `po_order_lines`
