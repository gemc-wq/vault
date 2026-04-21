# Order Import Flow

## Core pattern
Most importers normalize marketplace payloads into Zero's legacy order tables:

- `t_ebay_transaction` = canonical imported order-line table across many marketplaces
- `t_accessory` = accessory / fulfillment queue helper table
- `order_tracker_xls` = operational order tracker used later for PO routing, picking, dispatch, and tracking

Many importers fake an "eBay-like" shape even for non-eBay channels.

## Shopify
Source: `barcode/ShopifyImportOrders.php`

### Writes
- `t_ebay_transaction`
- `t_accessory`

### Key code
```php
$sql = "SELECT COUNT(f_sales_record_number) AS 'CountExist' FROM t_ebay_transaction WHERE f_sales_record_number='...'
```

```php
INSERT INTO t_ebay_transaction (
  f_sales_record_number, f_order_sales_record_number, f_status, ... f_custom_label, f_date_added, f_ebay_site
)
```

### Behavior
- Checks duplicates with `ExistIn_tebay()` and `ExistIn_tacc()`.
- Updates existing rows via `UpdateRecordTET()`.
- Inserts new rows via `InsertRecordTET()` / `InsertRecordTACC()`.
- Rejects malformed custom labels unless they split into 4 segments.
- Uses marketplace-specific `f_ebay_site` to distinguish Shopify from eBay.

## BigCommerce
Source: `barcode/bigcommerce_import_orders.php`

### Import method
CSV-style export parsing; each order is split into line items and converted to the `t_ebay_transaction` / `t_accessory` schema.

### Key transforms
```php
$tmp['f_status'] = "Paid and Awaiting Shipment";
$tmp['f_transaction_id'] = $data['SalesRecordNumber'] . "-" . $data['ItemNumber'];
$tmp['f_payment_method'] = $payment_method;
```

```php
$tmp['f_status'] = "Pending";   // t_accessory staging row
```

### Operational feedback loop
If a BC order is already shipped, the importer updates Zero tracker state:

```php
UPDATE order_tracker_xls
SET Feedback_Left = '{$market_dispatch_date}'
WHERE Sales_Record_Number = '{$srn}'
  AND (Feedback_Left IS NULL)
  AND f_ship_tracking IS NOT NULL
```

### Filters
- ignores test customers (`Andrew Ramos`, `Ron Gutierrez`)
- allows only `Shipped` / `Awaiting Fulfillment`
- skips bogus / short / non-numeric order IDs

## Amazon
Source: `barcode/AmazonImportOrders.php`

### Import method
Amazon MWS report download / processing; historical script also performs dispatch-side effects and China OOS listing shutdowns.

### Key code
```php
$sites = array(
 'UK' => array('ACCESS_KEY' => AWS_ACCESS_KEY_ID, ... 'SERVICE_URL' => SERVICE_URL)
);
```

```php
mysql_query("INSERT INTO cron_jobs (f_cron_name,f_datetime_start,f_process) VALUES (...)" , $connection_listing);
```

### Related tables observed
- `cron_jobs`
- `t_china_items_stock`
- `t_custom_label_active`
- downstream order tables not fully visible in the snippet, but this family of scripts feeds `order_tracker_xls` / marketplace tracking tables used everywhere else.

### Side effect: China stock depletion
```php
$sqlUpdatCNStockTable = "UPDATE t_china_items_stock SET f_qty = $remainingFreeStockLessQtyOrder, f_last_stock_movement = NOW() WHERE f_code = '...'";
```

When stock drops to zero, it ends active marketplace listings from `t_custom_label_active`.

## Walmart
Source: `barcode/walmart.inc.phpRON20190813`

### API endpoints
- `SERVICE_URL/released?createdStartDate=...`
- `SERVICE_URL?createdStartDate=...`
- `SERVICE_URL/{purchase_order_id}/acknowledge`
- `SERVICE_URL/{purchase_order_id}/shipping`
- `SERVICE_URL/{purchase_order_id}/cancel`
- `SERVICE_URL/{purchase_order_id}/refund`

### Import parsing
`ImportOrdersXMLObjectsToArray()` and `CheckOrdersXMLObjectsToArray()` flatten Walmart XML into line arrays.

### Captured fields
- `PurchaseOrderID`
- `CustomerID`
- `O_CustomLabel`
- `O_LineNumber`
- `O_LineStatus`
- `O_TrackingNumber`
- `O_TrackingURL`
- `SpareText1`

These map later into Zero tables in the dedicated import scripts.

## eBay
Source: `barcode/eBayGetTransactions.php`

### Pattern
Classic eBay Trading API importer. The wider codebase uses `t_ebay_transaction` as the main persistence table and `order_tracker_xls` for operational workflow.

### Zero field vocabulary reused everywhere
- `f_sales_record_number`
- `f_order_sales_record_number`
- `f_item_id`
- `f_transaction_id`
- `f_paid_on_date`
- `f_dispatch_date`
- `f_custom_label`
- `f_ebay_site`

## Rakuten
Source: `barcode/RakutenImportOrders.php`

Observed as another marketplace-specific importer that normalizes into the same Zero operational model. The picking-list generator explicitly contains Rakuten-specific text handling:

```php
function ConvertJPCharRakuten($text, $convert = false){
    if($convert){
        return mb_convert_encoding($text, "UTF-8", "auto");
    }
    else{
        return $text;
    }
}
```

That implies Rakuten orders eventually flow into the same downstream picking / shipping stack.

## Status lifecycle
There is no single clean enum, but the observed lifecycle is:

1. **Import inserted**
   - `t_ebay_transaction.f_status = 'Paid and Awaiting Shipment'`
   - `t_accessory.f_status = 'Pending'`
2. **Operational queue**
   - `order_tracker_xls.f_status = 'Pending'`
3. **Picking / ready to dispatch**
   - `order_tracker_xls.f_ready_for_despatch = 'Yes'`
4. **Dispatched / shipped**
   - marketplace-specific dispatch date + tracking written back
5. **Delivered**
   - some dispatch/manual flows update `f_status = 'Delivered'`
6. **Refunded / cancelled**
   - `f_refunded = 'Yes'` or marketplace cancellation/refund flows

## Error handling and retry patterns
The codebase is mostly procedural and retry-light.

### Common strategies
- duplicate detection before insert
- `INSERT IGNORE`
- cron logging to `cron_jobs`
- `MaxErrorRetry => 3` in Amazon Merchant Fulfillment clients
- `try/catch` around custom-label parsing and API calls
- manual backtrack/date-specific scripts for reruns (`*BackTrack*`, `*datespecific*`)

### Representative examples
```php
if(count($cl_arr) != 4){
    echo "Invalid CL ...";
    return 0;
}
```

```php
catch (MWSMerchantFulfillmentService_Exception $ex) { ... }
```

## Tables used
- `t_ebay_transaction`
- `t_accessory`
- `order_tracker_xls`
- `cron_jobs`
- `t_china_items_stock`
- `t_custom_label_active`
- `t_trackingnumbers` (used later for carrier/tracking reconciliation)

## Hardcoded values to externalize
- marketplace site IDs (`31`, `20`, `3`, etc.)
- order-status allowlists (`Shipped`, `Awaiting Fulfillment`)
- test account names
- Amazon credentials / service URLs in PHP
- importer-specific currency-to-payment-method mappings

## What to Replicate
1. Build one normalized `orders` table, not per-channel copy-paste.
2. Separate ingest from operational workflow.
3. Store source payload and normalized payload side-by-side.
4. Replace fake `t_ebay_transaction` cross-marketplace schema with typed marketplace adapters.
5. Add idempotency keys: `marketplace + order_id + line_id`.
6. Add structured retry queues for API/network failures.
