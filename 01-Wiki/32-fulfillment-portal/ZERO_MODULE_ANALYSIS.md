# ZERO Module Analysis

Source analyzed: `~/Downloads/zero/` via static code review only. No PHP executed.

## Environment / Database Context
### Purpose
Establish where Zero reads/writes data and how the ERP is split across order, product, and reporting systems.

### Key Files
- `~/Downloads/zero/ZERO_SYSTEM_SUMMARY.md`
- `~/Downloads/zero/ZERO_2.0_BUILD_PLAN.md`
- `~/Downloads/zero/barcode/*.php`
- `~/Downloads/zero/royalty-app/*`
- `~/Downloads/zero/design-catalogue/*`

### Business Rules
1. Root summary states **Aurora RDS** is the operational master for marketplace order/sales data.
2. Local `.160` database is used mainly for **product/design data** (`headcase`, `cfxb2b_db`, variation data), not primary order import.
3. Many PHP files reference `dirname(dirname(dirname(__FILE__))).'/config/barcode.php'`, but that config file is **not present in the extracted repo**. Existing root docs describe expected routing instead.
4. Legacy system is a monolith with many dated backups; file count alone overstates active logic.

### Database Tables Used
- Aurora/barcode tables inferred from code and summary docs:
  - `t_ebay_transaction`
  - `t_accessory`
  - `t_hardware`
  - `order_tracker_xls`
  - `t_temp_PO_table`
  - `POBySRN`
  - `t_amalgamated_po`
  - `t_amalgamated_po_line`
  - `t_royalty_information`
  - `t_royalty_rates`

### API Integrations
- Amazon MWS / SP-API transition
- Shopify API
- Walmart API
- Rakuten API
- SOAP integrations for ATG / GoHeadCase
- Sage connectors / internal HTTP endpoints

### What to Replicate vs What to Discard
- **Replicate:** data model knowledge, routing logic, license/royalty rules, warehouse-specific stock logic.
- **Discard:** raw `mysql_*` code, hardcoded credentials, dated backups, hidden side effects through HTTP POSTing to sibling scripts.

---

## Order Management
### Purpose
Import orders from multiple marketplaces into a common internal sales table, create downstream accessory/hardware records, and move shipped orders back out to marketplaces.

### Key Files
- `~/Downloads/zero/barcode/AmazonImportOrders.php`
- `~/Downloads/zero/barcode/ATGImportOrders.php`
- `~/Downloads/zero/barcode/ShopifyImportOrders.php`
- `~/Downloads/zero/barcode/WalmartImportOrders.php`
- `~/Downloads/zero/barcode/RakutenImportOrders.php`
- `~/Downloads/zero/barcode/bigcommerce_import_orders.php`
- `~/Downloads/zero/barcode/POFiltering.php`
- Related backups/variants: many dated `AmazonImportOrders*`, `POFiltering*`, dispatch scripts

### Business Rules
1. **Canonical order header table is `t_ebay_transaction`** even for non-eBay channels.
2. **Canonical line/item table is `t_accessory`** for normal items; `t_hardware` is used for hardware-type records.
3. Common import flow across channels:
   1. Fetch raw orders from marketplace/API/report.
   2. Normalize into internal fields (`f_sales_record_number`, status, address, title, custom label, etc.).
   3. Upsert into `t_ebay_transaction`.
   4. Insert line rows into `t_accessory` / `t_hardware` with initial `Pending` status.
   5. PO/routing later consumes those orders via `order_tracker_xls` and `t_temp_PO_table`.
4. **Amazon** (`AmazonImportOrders.php`):
   - Uses legacy **Amazon MWS Reports API**, not direct Orders API in this file.
   - Requests/downloads order reports, parses flat-file rows, and writes to `t_ebay_transaction`.
   - Uses `t_marketplace_prime_orders` to determine prime handling and dispatch restrictions.
   - Uses `t_amazon_despatched_items` to prevent duplicate shipment confirmation.
   - On import, can reduce `t_china_items_stock` and end active listings when China stock reaches zero.
5. **ATG / GoHeadCase** (`ATGImportOrders.php`):
   - Uses SOAP `retrieveOrders` against `services.goheadcase.com/ecellfulfillment/orderservices?wsdl`.
   - Imports only fully-paid orders (`PaymentAmount == Total_Payment_Received`).
   - Personalised products are transformed to custom-case labels and image URL goes into notes.
   - Updates `order_tracker_xls.f_ebay_dispatch_date` when shipped/completed.
6. **Shopify**:
   - Pulls `/admin/orders.xml` over authenticated API URL.
   - Inserts/updates `t_ebay_transaction`, then inserts `t_accessory` rows.
7. **Walmart**:
   - Imports released orders; records line status directly.
   - Special status mapping: `Created` becomes `UnAcknowledge` until later acknowledgement logic sets `Paid and Awaiting Shipment`.
8. **Rakuten**:
   - Uses Rakuten helper/API layer; comments show status updates occur back to Rakuten after import.
9. **BigCommerce**:
   - More manual/admin-assisted import path.
   - Writes to `t_ebay_transaction`, updates `order_tracker_xls`, and references `POBySRN` plus tracking tables for operational visibility.
10. **Status lifecycle observed in code:**
   - Marketplace header: `Paid and Awaiting Shipment` is the main “ready” state.
   - Line items in `t_accessory` / `t_hardware`: initially `Pending`.
   - `order_tracker_xls`: `Pending`, `Delivered`, refund flag `f_refunded = Yes`, dispatch timestamps.
   - PO generation excludes refunded and non-pending orders.
11. `POFiltering.php` is effectively the **bridge from imported marketplace orders to warehouse production routing**.

### Database Tables Used
- `t_ebay_transaction`
- `t_accessory`
- `t_hardware`
- `order_tracker_xls`
- `t_marketplace_prime_orders`
- `t_amazon_despatched_items`
- `t_china_items_stock`
- `t_custom_label_active`
- `t_system_log`
- `t_log`
- `cron_jobs`

### API Integrations
- Amazon MWS `MarketplaceWebService_Client`
- SOAP / ATG `retrieveOrders`
- Shopify Orders XML API
- Walmart API via `walmart.inc.php`
- Rakuten API via `rakuten.inc.php`

### What to Replicate vs What to Discard
- **Replicate:** marketplace normalization layer, duplicate prevention, shared internal order model, shipment sync/audit trail.
- **Discard:** using `t_ebay_transaction` as a universal table name, XML/manual imports, hardcoded SOAP credentials, MWS report polling architecture.

---

## PO Generation & Routing
### Purpose
Take imported sales records, decide which warehouse should print/fulfill each order, then generate, consolidate, amalgamate, and report purchase orders for PH, UK, FL, and DE.

### Key Files
- `~/Downloads/zero/barcode/POFiltering.php`
- `~/Downloads/zero/barcode/generate_purchase_order_automated_phAMG2_wh.php`
- `~/Downloads/zero/barcode/generate_purchase_order_automated_uk_wh.php`
- `~/Downloads/zero/barcode/generate_purchase_order_automated_fl_wh.php`
- `~/Downloads/zero/barcode/generate_purchase_order_automated_de_wh.php`
- Supporting targets called by HTTP POST:
  - `sage_generate_oos_all.php`
  - `sage_generate_purchase_orders_manual.php`
  - `consolidate_po_srns.php`
  - `amalgamate_po_upload_file.php`
  - `generate_sales_report_pdf.php`
  - `sage_generate_picking_list_allocated.php`
  - `generate_srn_po_amg_report.php`
  - `sync_database_for_render.php`

### Business Rules
1. **Primary routing outcomes** are encoded as remarks:
   - `ForPHProd` → warehouse `ECELLMFG`
   - `ForUKProd` → warehouse `ECELL UK`
   - `ForUSAProd` → warehouse `ECELLUSA` (Florida)
   - `ForDEProd` → warehouse `ECELLDE`
2. **POFiltering is the rules engine**. It parses each `Custom_Label` using `HeadCaseCustomLabel` into:
   - brand
   - product code
   - color
   - unit code
   - family code
   - design code
3. Internal routing key is built as:
   - `producttype_unitcode = brand + product_code + product_color + '-' + unit_code`
   - then normalized by replacing `HBCCR` with `HC`.
4. **Explicit PH-first / PH-forced rules:**
   - Invalid custom label → `INVALID`
   - Missing buyer country → `Hold` / order details verification
   - Blocked address → `Hold`
   - Discontinued license family → `HOLD`
   - `Sales_Record_Number` containing `PO` → forced to `ForPHProd`
   - Special 3D print families → `ForPHProd`
   - `familyfor_PH` set routes these families to PH:
     - `LFCKLOPPQ`, `LFCKLPICO`, `NUFCCRE`, `STREK3DCAP`, `STREK3DSPO`, `STREK3DICO1`
   - `family_design_for_ph` rules:
     - `BC`: `LFCKIT-LBA`, `LFCKIT-CAS`
     - `LB`: `LFCKIT-LLBA`, `LFCKIT-LCAS`
     - `TP`: `LFCKIT-LBA`, `LFCKIT-CAS`
   - `product_type_family_for_ph` rules:
     - for product code `BC`, families `GT3DSGL`, `GTCHAPO`, `GTDDSIG`, `GTGOSIG`, `GTHMOTT`, `GTKYART`, `GTS6FAC`, `GTS6FAC2`, `GTSGFLA`, `GTVMORG`
   - `TWD*` family + `BC` product → PH
   - Multiple-order SRNs (`srn_multiple_orders_list`) → PH
   - Country exclusions route to PH: `PH`, `JP`, `CL`, `GF`, `GP`, `MQ`, `MU`, `NC`, `NI`, `PF` and long-form names in array.
5. **Amazon Prime / premium routing:**
   - Prime lookup uses `t_marketplace_prime_orders`/helper arrays.
   - UK/ES/FR/DE/IT prime orders to UK domestic countries → `ForUKProd`
   - Amazon.de prime to DE-eligible countries (`DE`, `GERMANY`, `AT`, `AUSTRIA`) → `ForDEProd`
   - US/CAN Amazon prime sites → `ForUSAProd`
   - Unsupported prime combinations default to PH.
6. **Next-day / expedited shipping rules** (marketplace site 3 = Amazon):
   - If postage service is not standard and not Amazon.nl:
     - UK country → `ForUKProd`
     - US country → `ForUSAProd`
     - otherwise → `ForDEProd`
7. **Product-specific routing overrides:**
   - Product code `54` + unit `POPS` → `ForUKProd`
   - Marketplace site `20` (Staples) → `ForUSAProd`
   - License ID `1D` + units `IPADAIR2` or `IPAD5` → PH because `NoUKPackaging_DefaultToPH`
   - `(XBOX* or HALO*)` sold to US → `HOLD` for CS refund
8. **Warehouse stock-based routing** if not already caught by higher-priority rules:
   - UK filtering applies when:
     - unit exists in `uk_available_units`
     - buyer country is UK-eligible (`UK`, `UNITED KINGDOM`, `GB`, `GREAT BRITAIN`)
     - not US
     - DE-domestic-to-UK flag permits it
     - sufficient free stock exists
   - FL filtering applies when:
     - unit exists in `fl_available_units`
     - buyer country is US
     - marketplace site is not `4`
     - unit not in hardcoded `items_exclusions`
     - sufficient free stock exists
   - DE filtering applies when:
     - unit exists in `de_available_units`
     - buyer country is non-US and non-UK
     - country is in `eligible_countries_for_de_filter_non_prime` (`IT`, `FR`, `DE`, `ES` variants)
     - sufficient free stock exists
   - If none match, default is PH.
9. **Disabled-unit override tables:**
   - `t_po_filtering_units` can disable unit codes per warehouse (`f_is_disabled_uk`, `f_is_disabled_fl`, `f_is_disabled_de`).
   - If disabled, order falls back to PH.
10. **End-of-life PH protection:**
   - Even if an order routes to PH, if `producttype_unitcode` is found in `ph_eol_units` with zero PH stock, it is reclassified to `EOL`.
11. **Force-routing overrides:**
   - `t_po_force_srns` and force-to-warehouse lists can override the computed warehouse.
12. **Hardcoded unit exclusions from FL production** (`items_exclusions`) include many tablet/fire/ipad units such as `HD102021`, `IPADPRO11`, `IPDPRO129`, etc. These are not eligible for FL allocation.
13. **Generate-PO automation scripts all follow same pattern:**
   1. Generate OOS candidate orders by POSTing to `sage_generate_oos_all.php`
   2. Filter candidate SRNs through `POFiltering.php`
   3. Re-read filtered rows from `t_temp_PO_table` with warehouse remark (`ForPHProd`, `ForUKProd`, `ForUSAProd`)
   4. Exclude rows already having `PONumber`, non-empty remarks, custom/personalized codes, FBA records, refunded or non-pending orders
   5. Group by `Sage_DB_ID` + custom label
   6. POST into `sage_generate_purchase_orders_manual.php`
   7. Consolidate PO↔SRN mapping via `consolidate_po_srns.php`
   8. Amalgamate POs into HPT batches via `amalgamate_po_upload_file.php`
   9. Generate reports/barcodes/picking lists and email recipients
14. **Warehouse-specific PO suppliers:**
   - PH: `ECELLMFG`, unit price from `PORawMaterialItemPrice`
   - UK: `ECELL UK`, unit price hardcoded `0`
   - FL: `ECELLUSA`, unit price hardcoded `0`
15. **Prime/non-prime exclusions in automated scripts:**
   - UK automated PO excludes `RecordIsAmazonPrimeUK` and `NextDayDeliveryUKService`
   - FL automated PO excludes `NextDayDeliveryUSService`
   - This means dedicated automated runs are specifically for non-prime/non-premium queues.
16. **Wave timing:**
   - I did **not** find explicit strings for “Wave 1 / Wave 2 / Wave 3” or readable cron schedules in the analyzed PHP.
   - The business intent is visible in warehouse-specific automated scripts, but actual execution timing appears to live outside these files (likely cron/server config).
17. **Saturday/Monday and H89/HST/HDM rules:**
   - I did **not** find explicit hardcoded rules matching those exact strings in the active `POFiltering.php` analyzed.
   - If these rules exist, they may live in older backup variants, cron wrappers, or operational runbooks rather than the current active file.

### Routing Rules as Pseudocode
```pseudo
parse custom_label -> brand, product_code, color, unit_code, family_code, design_code
producttype_unitcode = normalize(brand + product_code + color + '-' + unit_code)

if invalid label: INVALID
else if buyer country missing: HOLD
else if blocked address or blocked customer: HOLD
else if discontinued license: HOLD
else if amazon prime:
  if UK/EU prime site and UK country: UK
  else if Amazon.de prime and DE/AT country: DE
  else if US prime site: FL
  else: PH
else if expedited amazon shipping:
  if UK country: UK
  else if US country: FL
  else: DE
else if special product/family/design PH overrides: PH
else if staples marketplace: FL
else if country exclusion: PH
else if SRN contains 'PO': PH
else if UK stock available and unit enabled and country UK-eligible: UK
else if FL stock available and unit enabled and buyer country US and unit not excluded: FL
else if DE stock available and unit enabled and country DE-nonprime eligible: DE
else: PH

if result == PH and producttype_unitcode has PH EOL zero stock:
  result = EOL

if forced warehouse override exists for SRN:
  result = forced warehouse
```

### Routing Rules as Structured JSON
```json
{
  "outputs": {
    "ForPHProd": "ECELLMFG",
    "ForUKProd": "ECELL UK",
    "ForUSAProd": "ECELLUSA",
    "ForDEProd": "ECELLDE"
  },
  "priority_rules": [
    "invalid_label -> INVALID",
    "missing_country -> HOLD",
    "blocked_address_or_customer -> HOLD",
    "discontinued_license -> HOLD",
    "prime_order -> warehouse by marketplace/country",
    "expedited_amazon -> UK/FL/DE by destination",
    "special_product_family_design rules -> PH",
    "Staples marketplace -> FL",
    "country_exclusions -> PH",
    "srn contains PO -> PH",
    "stock-allocation rules -> UK/FL/DE",
    "default -> PH",
    "PH zero-stock EOL override -> EOL",
    "force_srn_warehouse override -> forced warehouse"
  ],
  "uk_eligible_countries": ["UK", "UNITED KINGDOM", "GB", "GREAT BRITAIN"],
  "de_prime_countries": ["DE", "GERMANY", "AT", "AUSTRIA"],
  "de_nonprime_countries": ["IT", "ITALY", "FR", "FRANCE", "DE", "GERMANY", "ES", "SPAIN"],
  "ph_family_overrides": ["LFCKLOPPQ", "LFCKLPICO", "NUFCCRE", "STREK3DCAP", "STREK3DSPO", "STREK3DICO1"],
  "ph_family_design_overrides": {
    "BC": ["LFCKIT-LBA", "LFCKIT-CAS"],
    "LB": ["LFCKIT-LLBA", "LFCKIT-LCAS"],
    "TP": ["LFCKIT-LBA", "LFCKIT-CAS"]
  },
  "ph_product_type_family_overrides": {
    "BC": ["GT3DSGL", "GTCHAPO", "GTDDSIG", "GTGOSIG", "GTHMOTT", "GTKYART", "GTS6FAC", "GTS6FAC2", "GTSGFLA", "GTVMORG"]
  }
}
```

### Database Tables Used
- `t_temp_PO_table`
- `order_tracker_xls`
- `POBySRN`
- `t_po_force_srns`
- `t_po_filtering_units`
- `t_amalgamated_po`
- `t_amalgamated_po_line`
- Sage stock queries via helper functions

### API Integrations
- Internal HTTP POST orchestration between PHP pages on Zero (`do_post_request`)
- Sage connector/helper methods from `sage.inc.php`

### What to Replicate vs What to Discard
- **Replicate:** routing rule engine, forced warehouse overrides, disabled-unit controls, stock-aware allocation, PO consolidation/amalgamation workflow.
- **Discard:** page-to-page HTTP POST orchestration, HTML scraping of sibling PHP responses, hardcoded email lists, duplicate warehouse scripts per environment.

---

## Inventory Management
### Purpose
Track stock by warehouse, verify available stock against PO demand, manage reorder levels, and support production scanning from goods-in through printing.

### Key Files
- `~/Downloads/zero/prod_tracker/stock_checking/uk_po_functions.php`
- `~/Downloads/zero/prod_tracker/commons/production_scanning_processor.class.php`
- `~/Downloads/zero/barcode/sage_reorderlevel.php`
- `~/Downloads/zero/barcode/warehouse_prime_units_low_stock_alert_emailer.php`
- `~/Downloads/zero/barcode/sage_stock_levels.php`
- `~/Downloads/zero/barcode/sage_get_stock*.php`
- `~/Downloads/zero/barcode/get_mfg_free_stock.php`
- `~/Downloads/zero/barcode/uk_fl_stock_verification.php`
- `~/Downloads/zero/prod_tracker/goods_in/*`
- `~/Downloads/zero/prod_tracker/pre_scan*`, `printing*`, `post_printing*`

### Business Rules
1. **Stock is warehouse-specific** and commonly split across:
   - PH
   - UK
   - FL / Florida
   - DE
2. `POFiltering.php` consumes helper snapshots of warehouse free stock:
   - UK free stock via Sage warehouse `UK`
   - FL free stock via Sage warehouse `Florida`
   - DE free stock via Sage warehouse `DE`
   - PH EOL stock via Sage warehouse `PH`
3. `warehouse_prime_units_low_stock_alert_emailer.php` identifies low-stock “prime/premium” units:
   - UK/DE/FL each have alert thresholds (`<= 10` free stock)
   - Uses warehouse-specific added-date fields to determine relevant prime units
   - Excludes product group `DISC`
   - Emails operational teams per warehouse
4. `sage_reorderlevel.php` computes reorder level from historical sales in `t_material_orders`:
   - Sum sales over configurable rolling days
   - Multiply by configurable factor `x`
   - HLBWH and `Z-FS` packaging items get multiplier `(x + 2)` instead of `x`
   - PH note says reorder calculation may use combined sales from PH + UK + FL + DE
   - Result is pushed back to Sage via `SetReorderLevel`
5. `prod_tracker/stock_checking/uk_po_functions.php` cross-checks PO demand against `production_tracker.t_uk_stocks`:
   - Builds Sage stock code from custom label
   - Flags discrepancies where PO count exceeds in-stock count
6. `production_scanning_processor.class.php` shows manufacturing flow state tracking:
   - Split by UKPROD and USPROD databases
   - Logs scan timestamps for pre-print, printing, post-print
   - Tracks sent/received quantities per HPT PO
   - Resolves HPT PO numbers back to Sage order numbers from `t_amalgamated_po` and `t_amalgamated_po_line`
7. Core stock/production workflow appears to be:
   1. Order imported
   2. PO routed/amalgamated
   3. Goods-in and pre-goods-in logged
   4. Pre-print scan
   5. Printing batch/jig logging
   6. Post-print received logging
   7. Packing/dispatch

### Database Tables Used
- `t_material_orders`
- `t_uk_stocks`
- `t_amalgamated_po`
- `t_amalgamated_po_line`
- `t_pre_print_scan_logs`
- `t_pre_print_sent`
- `t_post_print_scan_logs`
- `t_post_print_received`
- Sage inventory tables via helper functions

### API Integrations
- Sage stock/reorder APIs via `sage.inc.php`
- Internal production tracker DB connections (`UKPROD`, `USPROD`)

### What to Replicate vs What to Discard
- **Replicate:** warehouse-level inventory ledger, reorder math, production scan events, HPT PO traceability, low-stock alerting.
- **Discard:** split UKPROD/USPROD duplicated logic, manual HTML forms for stock checks, direct Sage coupling at UI layer.

---

## Royalty Reporting
### Purpose
Maintain license master data, rate history, contract metadata, and produce royalty statements/reports by brand/licensor.

### Key Files
- Legacy PHP:
  - `~/Downloads/zero/barcode/royalty_report_manager.php`
  - `~/Downloads/zero/barcode/get_1d_sales.phpRON20211124`
  - `~/Downloads/zero/barcode/royalty_report_email_files_retriever.php`
  - `~/Downloads/zero/barcode/royalty_license_listings_reference.php`
  - `~/Downloads/zero/barcode/license_trademark.php`
  - `~/Downloads/zero/barcode/licensedboxreference.php`
- Modern app:
  - `~/Downloads/zero/royalty-app/app/routers/royalty.py`
  - `~/Downloads/zero/royalty-app/app/routers/licenses.py`
  - `~/Downloads/zero/royalty-app/sql/royalty_report_by_licensor.sql`
  - `~/Downloads/zero/royalty-app/sql/royalty_report_detailed.sql`
  - `~/Downloads/zero/royalty-app/app/report_configs/*.json`

### Business Rules
1. **Master license table** is `t_royalty_information`.
2. **Pending approval queue** is `t_royalty_information_temp`.
3. **Rate history table** is `t_royalty_rates`.
4. `royalty_report_manager.php` manages:
   - license master records
   - approval workflow
   - status values (`Active`, `Inactive`, `Duplicate`)
   - contact/payment/contract metadata
5. Rate resolution rule in both modern API and SQL:
   - use latest active `t_royalty_rates.f_rate` effective on or before order `Paid_Date`
   - if no history rate exists, fall back to `t_royalty_information.f_royalty_rate`
6. Royalty calculation rule:
   - if `f_royalty_rate_type = percentage` → `Net_Sale * rate / 100`
   - if `f_royalty_rate_type = unit` → `Quantity * rate`
7. Report exclusions:
   - `Status != Cancelled`
   - `Status != Cancel PO`
   - refunds excluded (`Is_Refunded != Yes/TRUE`)
   - only active royalty records included
8. Brand/license join logic in modern app:
   - `orders.Brand -> brands.Name -> brands.BrandID -> t_royalty_information.f_license_id_reference`
9. `licenses.py` normalizes the long-standing typo `Acrrue` -> `Accrue`.
10. License detail includes:
   - accounting type
   - territories
   - product types
   - channel
   - contract number/term
   - payment method / PayPal
   - minimum guarantee
   - production notes
11. `license_trademark.php` is a parallel trademark/reference registry:
   - trademark numbers
   - search images/text
   - market/country permissions (eBay, Amazon, UK, EU, worldwide)
12. `licensedboxreference.php` encodes **brand-to-packaging mappings** for licensed products, e.g. brand prefix + box size → packaging SKU (`Z-FS ... BOX ...`).
13. `get_1d_sales.php...` contains large hardcoded design/description mappings used to label statement outputs for legacy licensed brands.

### Database Tables Used
- `t_royalty_information`
- `t_royalty_information_temp`
- `t_royalty_rates`
- `t_license_trademark_information`
- `t_user_profile`
- BigQuery / warehouse tables in new app:
  - `orders`
  - `brands`

### API Integrations
- BigQuery via Google Cloud client in `royalty-app`
- Legacy Excel export/report generation

### What to Replicate vs What to Discard
- **Replicate:** license master, rate history with effective dating, percentage/unit royalty math, contract metadata, approval workflow, statement/report configs.
- **Discard:** giant hardcoded description arrays, mixed PHP UI/reporting logic, file-dump based report delivery, manual email retrieval flows.

---

## Design Catalog
### Purpose
Provide a browsable/exportable mapping between brands, lineups, designs, products, colors, and device units so designs can be listed and manufactured against valid SKU/device combinations.

### Key Files
- `~/Downloads/zero/design-catalogue/class/model/Designs.php`
- `~/Downloads/zero/design-catalogue/class/model/ProductDevices.php`
- `~/Downloads/zero/design-catalogue/class/model/Brands.php`
- `~/Downloads/zero/design-catalogue/class/controller/ExportController.php`
- `~/Downloads/zero/design-catalogue/view/designs/view_all.php`
- `~/Downloads/zero/design-catalogue/view/productdevices/view_all.php`
- Related barcode helpers:
  - `~/Downloads/zero/barcode/design.php`
  - `~/Downloads/zero/barcode/designs_export_excel*.php`
  - `~/Downloads/zero/barcode/get_top_selling_designs*.php`

### Business Rules
1. Design catalogue joins **headcase design tables** with **cfxb2b product/device tables**.
2. `Designs::GetByBrandId()` uses:
   - `headcase.tblDesigns`
   - `headcase.tblLineups`
   - `headcase.tblDesignProductAvailability` or `tblDesignGroupAvailability`
   - `cfxb2b_db.lineups_brand`
   - `cfxb2b_db.brands`
   - unit/product tables from `cfxb2b_db`
3. Output dimensions are effectively:
   - Brand
   - Lineup
   - Design
   - Product code / color
   - Unit/device
   - Unit type (phone / tablet / other)
4. Unit eligibility rules:
   - exclude groupings `TEMP`, `X`, and `TEMP%`
   - require non-null `UnitID`
   - require active grouping/unit status
5. Preview segmentation rules:
   - default `unit_type = 1` → phones
   - `tablet_preview` → unit types `2,4`
   - `others_preview` → laptop/skins/other accessory unit types `12,17..27`
6. `ProductDevices::GetAll()` materializes SKU/device combinations as:
   - `ProductColorUnit = H + ProductCode + ColorCode + '-' + UnitLabel`
   - normalized by replacing `HHCCR` with `HC`
   - This is the same naming convention used by fulfillment routing.
7. `ExportController` exports all designs for a brand using effectively unlimited pagination (`limit = 999999`).
8. This subsystem is the **reference layer for valid design × product × device combinations**, not the transactional order layer.

### Database Tables Used
- `headcase.tblDesigns`
- `headcase.tblLineups`
- `headcase.tblDesignProductAvailability`
- `headcase.tblDesignGroupAvailability`
- `cfxb2b_db.brands`
- `cfxb2b_db.brand_titles`
- `cfxb2b_db.lineups_brand`
- `cfxb2b_db.uv_product_colors`
- `cfxb2b_db.unit_groups`
- `cfxb2b_db.unit_groupings`
- `cfxb2b_db.units`
- `cfxb2b_db.unit_brand`

### API Integrations
- Internal PHP MVC only; no external marketplace API in analyzed catalogue code.

### What to Replicate vs What to Discard
- **Replicate:** normalized design/product/device graph, active/inactive filtering, export capability, shared SKU naming rules with fulfillment.
- **Discard:** direct SQL from controllers/models without service layer, query-string driven mode switching, tight coupling to old `headcase`/`cfxb2b_db` schema names.

---

## Other Core / Supporting Modules Identified
### Purpose
These are adjacent modules that materially support operations even if they were not the five primary focus areas.

### Key Files
- Dispatch/shipping:
  - `eBayConfirmDespatch*.php`
  - `AmazonLinkTrackingNumber*.php`
  - `WalmartDispatchOrders.php`
  - `RakutenDispatchOrders*.php`
- Listing/inventory sync:
  - `AmazonUpdateInventory*.php`
  - `amazon_update_inventory_db*.php`
  - `eBayReviseInventoryStatus*.php`
  - `PlayUpdateInventory*.php`
- Licensing/compliance:
  - `license_trademark.php`
  - `LicensesPackagingGuide.php`
  - `license_weekly_summary.php`
- Reporting/analytics:
  - `bestSellingDesigns*.php`
  - `head_case_designs_sales.php`
  - `stock_summary.php`

### Business Rules
1. Shipping sync is marketplace-specific and usually separate from import.
2. Inventory publish/update scripts push availability back to marketplace listings.
3. License/trademark metadata controls compliance, search references, and packaging.
4. Design/sales reports inform merchandising and licensing decisions.

### Database Tables Used
- Varies by script; often reuses `t_ebay_transaction`, `order_tracker_xls`, inventory and listing tables.

### API Integrations
- eBay API
- Amazon feeds / inventory sync
- Walmart / Rakuten dispatch APIs

### What to Replicate vs What to Discard
- **Replicate:** the business capability, not the one-script-per-channel implementation style.
- **Discard:** fragmented script sprawl and duplicated variants.

---

## Replication Recommendations by Module
| Module | Status | Replicate? | Owner |
|---|---|---:|---|
| Order Management | Critical | Yes | Zero 2.0 Order Agent / Integrations |
| PO Generation & Routing | Critical | Yes | Zero 2.0 Inventory + Production Agents |
| Inventory Management | Critical | Yes | Zero 2.0 Inventory Agent |
| Royalty Reporting | Important | Yes | Finance / Licensing Platform |
| Design Catalog | Important | Yes | Product Data / Merchandising |
| Dispatch & Tracking Sync | Critical | Yes | Fulfillment Agent |
| Marketplace Inventory Sync | Important | Yes | Integrations |
| License / Trademark Registry | Important | Yes | Licensing / Legal Ops |
| Legacy PHP UI Pages | Legacy | No | N/A |
| Dated Backup Script Copies | Legacy | No | N/A |

## Notes / Gaps
- `config/barcode.php` referenced by many scripts was not present in the extracted repo, so DB hosts were inferred from `ZERO_SYSTEM_SUMMARY.md` and in-code table usage.
- I did not find explicit readable cron schedules or wave labels (“Wave 1/2/3”) in the PHP itself.
- I did not find explicit active-code rules for `H89`, `HST`, `HDM never to PH`, or Saturday/Monday handling in the main `POFiltering.php`; those may exist in older backups, cron wrappers, or operational docs outside the code snapshot.
