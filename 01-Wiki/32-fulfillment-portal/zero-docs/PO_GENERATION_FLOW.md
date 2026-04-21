# PO Generation Flow

## Main sources
- `barcode/generate_purchase_order_automated_uk_wh.php`
- `barcode/generate_purchase_order_automated_fl_wh.phpRON20220120`
- `POAmalgamation/amalgamate_po_upload_file.php`
- `barcode/sage_generate_picking_list_split.phpRON20200921`

## Stage 1: generate OOS candidate pool
Automated PO scripts do not start from raw orders. They first call Zero's own OOS generator remotely:

```php
$url = "sage_generate_oos_all.php";
$data = "cmdexecute=1&submit_button=true&date_from={$oos_from}&date_to={$oos_to}&select_company_id[1]=1&select_company_id[2]=2";
$page = do_post_request($url, "barcode", $data);
```

The response HTML is parsed and converted into arrays, then filtered to eligible SRNs.

## Stage 2: exclude invalid/processed orders
Both UK and FL scripts remove rows that are already PO'd, refunded, non-pending, FBA, or custom-made.

```php
if($data['PONumber'] != "") continue;
if($data['Remarks'] != "") continue;
if(strpos($data['ItemCode'], "CUS") !== false ... ) continue;
if(array_key_exists($data['Sales_Record_Number'], $fba_srns)) continue;
if(array_key_exists($data['Sales_Record_Number'], $srns_status)) continue;
```

Relevant lookups:
- `t_po_force_srns`
- `POBySRN`
- `order_tracker_xls`
- `t_temp_PO_table`

## Stage 3: warehouse-specific PO selection
### UK
```php
FROM t_temp_PO_table a
LEFT JOIN order_tracker_xls b ON a.Sales_Record_Number = b.Sales_Record_Number
WHERE a.Sales_Record_Number IN ('...')
AND a.Remarks = 'ForUKProd'
AND a.Information NOT LIKE '%RecordIsAmazonPrimeUK%'
AND a.Information NOT LIKE '%NextDayDeliveryUKService%'
```

### FL
```php
WHERE a.Sales_Record_Number IN ('...')
AND a.Remarks = 'ForUSAProd'
AND a.Information NOT LIKE '%NextDayDeliveryUSService%'
```

So the automated PO scripts consume the routing output from `POFiltering.php` rather than recalculating routing.

## Stage 4: force-SRN overrides
UK and FL both allow manual rescue/override through `t_po_force_srns`.

```php
SELECT f_srn FROM t_po_force_srns WHERE f_date_processed IS NULL
```

These SRNs are injected into the PO candidate list even if they would normally be filtered out.

## Stage 5: amalgamation
Source: `POAmalgamation/amalgamate_po_upload_file.php`

This layer groups multiple Sage purchase orders into a printable / production-friendly aggregate PO.

### Main storage tables
- `t_amalgamated_po`
- `t_amalgamated_po_line`

### Insert code
```php
INSERT INTO t_amalgamated_po (f_HptId, f_Status, f_PhoneCode, f_DateAdded, f_POBatchNo, f_POBatch, f_WarehouseName) VALUES ...
```

```php
INSERT IGNORE INTO t_amalgamated_po_line (f_HptId, f_CustomLabel, f_ProductCode, f_Quantity, f_SageServer, f_POType, f_SageDocumentNumber, f_SageDateCreated, f_DateAdded) VALUES ...
```

### Sage environments
```php
$sage_connections = array(
  'UK'=> array('dbip'=>$sage_ip_address, 'dbname'=>'Ecell_UK'),
  'US'=> array('dbip'=>$sage_ip_address, 'dbname'=>'Ecell_US'),
  'DE'=> array('dbip'=>$sage_ip_address, 'dbname'=>'Ecell_DE')
);
```

This confirms warehouse/server separation is handled at the amalgamation layer too.

## Stage 6: picking-list generation
Source: `barcode/sage_generate_picking_list_split.phpRON20200921`

The picking-list generator uploads SRNs into `t_poed_srns`, checks current order states, then marks orders as ready.

### Key writes
```php
INSERT IGNORE INTO t_poed_srns (Sales_Record_Number, f_status, Date_PO_Inserted, Date_PO_Updated) VALUES ...
```

```php
UPDATE order_tracker_xls SET f_ready_for_despatch = 'Yes', f_last_picking_list_date = NOW() WHERE Sales_Record_Number = '{$srn}'
```

```php
INSERT IGNORE INTO t_temp_picking_list (f_srn, f_date_added, f_date_printed, f_picker, f_picked_for, f_picker_ph) VALUES (...)
```

### Picking grouping
The script groups by address to detect multiple orders:

```php
SELECT GROUP_CONCAT(Sales_Record_Number separator ',') AS mo
FROM order_tracker_xls
WHERE Sales_Record_Number IN ($wheresrn)
GROUP BY Email_Address, Buyer_Address_1, Buyer_Address_2, Buyer_City, Buyer_State, Buyer_Zip, Buyer_Country
HAVING COUNT(*) > 1
```

## Special controls / hardcoded pauses
UK automated PO generation contains a hard stop for 2022-04-15 and 2022-04-18.

## What tables matter most
- `t_temp_PO_table`
- `order_tracker_xls`
- `t_po_force_srns`
- `POBySRN`
- `t_amalgamated_po`
- `t_amalgamated_po_line`
- `t_poed_srns`
- `t_temp_picking_list`

## Hardcoded values to externalize
- remote Zero host `http://34.196.137.61/barcode/`
- exclusion phrases for Prime / NextDay orders
- magic company IDs in OOS requests
- hardcoded email recipients and SMTP credentials
- hardcoded Sage DB map (`Ecell_UK`, `Ecell_US`, etc.)

## What to Replicate
1. Replace HTML-scraping between internal scripts with API/job events.
2. Model PO lifecycle explicitly: `candidate -> allocated -> generated -> amalgamated -> picked`.
3. Keep warehouse routing immutable once PO-candidate set is frozen.
4. Add audit trail for manual force-SRN overrides.
5. Store PO batch metadata as first-class objects, not inferred from filenames/scripts.
