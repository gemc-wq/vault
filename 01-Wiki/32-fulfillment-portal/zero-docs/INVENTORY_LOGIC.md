# Inventory Logic

## Sage free-stock integration
The codebase repeatedly computes free stock from Sage using the same formula:

```sql
(ConfirmedQtyInStock + UnconfirmedQtyInStock - QuantityAllocatedSOP) AS FreeStock
```

Observed in `barcode/sage.inc_add_beta_sage2013.php010916.php` and related Sage helper files.

## Warehouse-level stock tracking
`POFiltering.php` asks Sage for available raw materials by warehouse:

```php
$uk_available_units = SageWarehouseRawMaterialsWithStocks(..., array('UK'), " > 0 ", "1");
$fl_available_units = SageWarehouseRawMaterialsWithStocks(..., array('Florida'), " > 0 ", "2");
$de_available_units = SageWarehouseRawMaterialsWithStocks(..., array('DE'), " > 0 ", "1");
```

That means routing uses real-time per-warehouse free stock snapshots, not a static table.

## PH end-of-life / zero-stock logic
```php
$ph_eol_units = SageWarehouseRawMaterialsWithStocks(..., array('PH'), " = 0 ", "7");
```

If a line falls back to PH and the SKU exists in this set, the order is marked `EOL`.

## China stock integration in Amazon importer
`AmazonImportOrders.php` also maintains a simpler stock ledger for China items:

```php
SELECT f_qty FROM t_china_items_stock WHERE f_code = '...'
UPDATE t_china_items_stock SET f_qty = $remainingFreeStockLessQtyOrder, f_last_stock_movement = NOW() WHERE f_code = '...'
```

If free stock reaches zero, related marketplace listings in `t_custom_label_active` are ended.

## Low-stock / OOS triggers
There is no single dedicated low-stock service; instead the system relies on:

1. Sage free-stock reads
2. OOS report generation via `sage_generate_oos_all.php`
3. Listing shutdown for China items when stock <= 0
4. PO routing fallback if UK/FL/DE cannot allocate

So the effective alert trigger is often **workflow-generated**, not a notification table.

## Picking and inventory reservation
Picking-list scripts mark orders as ready and track them separately:

- `t_poed_srns`
- `t_temp_picking_list`
- `order_tracker_xls.f_ready_for_despatch`

This is not pure inventory reservation, but operationally it serves that purpose.

## prod_tracker scanning logic
Source: `prod_tracker/commons/production_scanning_processor.class.php`

Production scanning records movement between production stages in separate UK/US production databases.

### Pre-print logging
```php
INSERT IGNORE INTO t_pre_print_scan_logs (f_scan_id, f_date_time_scanned, f_user, f_token_link) VALUES ...
INSERT INTO t_pre_print_sent (f_hpt_po, f_sent_qty, f_date_time, f_token_link) VALUES ...
```

### Post-print logging
```php
INSERT IGNORE INTO t_post_print_scan_logs (f_scan_id, f_date_time_scanned, f_user, f_token_link) VALUES ...
INSERT INTO t_post_print_received (f_hpt_po, f_received_qty, f_date_time, f_token_link) VALUES ...
```

### Printer/jig logging
```php
INSERT IGNORE INTO {$table} (f_scan_id, f_date_time_scanned, f_printer_number, f_jig_id, f_print_type, f_batch_id, f_user) VALUES ...
```

### Multi-database split
```php
$db = new DatabaseConnection("UKPROD");
$db = new DatabaseConnection("USPROD");
```

This means production inventory / work-in-progress is tracked separately from the main Zero order DB.

## Tables used
- Sage `WarehouseItem` / `BinItem` tables (via Sage SQL helpers)
- `t_china_items_stock`
- `t_custom_label_active`
- `t_pre_print_scan_logs`
- `t_post_print_scan_logs`
- `t_pre_print_sent`
- `t_post_print_received`
- `t_poed_srns`
- `t_temp_picking_list`

## Hardcoded values to externalize
- warehouse names: `UK`, `Florida`, `DE`, `PH`
- ERP type IDs: `1`, `2`, `7`
- production DB names: `UKPROD`, `USPROD`

## What to Replicate
1. Central stock service with warehouse snapshots + reservations.
2. Separate **available**, **allocated**, **WIP**, and **discontinued** states.
3. Production-scan events should feed the same inventory ledger, not separate hidden DBs.
4. OOS decisions should emit notifications/webhooks, not only affect routing silently.
