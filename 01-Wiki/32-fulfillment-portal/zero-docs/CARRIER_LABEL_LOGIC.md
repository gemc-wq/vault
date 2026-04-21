# Carrier / Label Logic

## Amazon Buy Shipping / Merchant Fulfillment
Source: `barcode/process_amazon_prime_orders.php`

### API stack
- `MWSMerchantFulfillmentService/Client.php`
- endpoint: `.../MerchantFulfillment/2017-10-01`

### Label request construction
```php
$request = new MWSMerchantFulfillmentService_Model_CreateShipmentRequest();
$request->setSellerId($vars['MERCHANT_ID']);
$request->setShippingServiceId("AMZN_UK");
```

```php
$ship_from_address->setName("Ecell Global Ltd");
$ship_from_address->setAddressLine1("C1 Barrow Close");
$ship_from_address->setPostalCode("FY4 5PS");
$ship_from_address->setCountryCode("GB");
```

```php
$package_dimension->setLength(14.6);
$package_dimension->setWidth(9.1);
$package_dimension->setHeight(1);
$weight->setValue(1.20);
$weight->setUnit("oz");
```

### Processing result
On success, the script marks `t_marketplace_prime_orders` rows processed:

```php
$db_fields['f_is_processed'] = "1";
$db_fields['f_processed_date'] = "NOW()";
$mysql->UpdateQuerySpecific($db_fields, $fieldstoupdate, "t_marketplace_prime_orders", true, true);
```

## Royal Mail SOAP integration
The clearest SOAP calls found are in `barcode/ATGImportOrders_ALL.php` / `ATGImportOrdersUAT.php`:

```php
$wsdl = "https://services.goheadcase.com/ecellfulfillment/orderservices?wsdl";
$client = new SoapClient($wsdl, array('login' => 'ecell-uat', 'password' => '3c311u4tt35t', 'soap_version' => SOAP_1_1, 'trace' => 1));
$response = $client->__soapCall('retrieveOrders', array('parameters' => array("fromDate" => $date)));
```

This is SOAP-based fulfillment integration tied to goheadcase/e2x. It is not a Royal Mail label-create SOAP call, but it is the SOAP transport in the shipping/fulfillment area of the codebase.

### Royal Mail service codes in shipping logic
`barcode/dhl_handler.php` maps Royal Mail services:

```php
case "Royal Mail Tracked 24": $code = "24";
case "Royal Mail Tracked 24 (Signature)": $code = "24";
case "Royal Mail Tracked 48": $code = "48";
case "Royal Mail Tracked 48 (Signature)": $code = "48";
```

There is also a CSV-style Royal Mail import helper in `create_prime_rmdmo_shipment_Vhey01042018.php` that outputs columns like service `24`, weight, postcode, and reference for bulk import.

## Stamps.com / Endicia
Source: `barcode/endicia_stamps_report.php` (file identified) and carrier-reporting flow elsewhere.

The codebase contains Stamps/Endicia-era scripts for US/UK postage reporting, but the main carrier abstraction visible in the current snippets is operational writeback rather than a clean API client.

## DHL / Evri / Hermes
### DHL
Source: `barcode/dhl_handler.php`
- maps customer-facing postage services to carrier codes
- contains Royal Mail code branching too, implying it acts as a generic dispatch handler

### Evri / Hermes
The codebase historically uses Hermes naming in places. In the available snippets, carrier normalization appears to happen through dispatch handlers and `t_trackingnumbers` rather than a dedicated isolated Evri service module.

## Tracking-number writeback to Zero
Tracking is written to `order_tracker_xls` and/or `t_trackingnumbers`.

### Direct update examples
```php
UPDATE order_tracker_xls SET f_ship_tracking = '{$tracking_number}', Postage_Service = 'UPS ClickAndCollect' WHERE Sales_Record_Number = '{$srn}'
```

```php
$sql .= " f_status = 'Delivered', f_imei = '{$order_v2['f_imei']}',f_ship_tracking = '{$order_v2['f_tracking_number']}', Dispatch_Date = '...'",
```

### Tracking lookup usage
BigCommerce pending-orders query reads latest carrier from `t_trackingnumbers`:

```php
(SELECT f_carriername FROM t_trackingnumbers WHERE f_srn = Sales_Record_Number ORDER BY f_date_inserted DESC LIMIT 1) AS 'Carrier'
```

So the pattern is:
1. carrier handler creates/collects label + tracking
2. tracking lands in `t_trackingnumbers` and/or `order_tracker_xls.f_ship_tracking`
3. marketplace dispatch/reconciliation jobs read it back and notify channels

## Tables used
- `t_marketplace_prime_orders`
- `order_tracker_xls`
- `t_trackingnumbers`

## Hardcoded values to externalize
- Amazon ship-from address and contact details
- fixed package dimensions/weight
- Amazon shipping service id `AMZN_UK`
- SOAP WSDL URL and UAT credentials
- DHL/Royal Mail service-code mappings (`24`, `48`, etc.)

## What to Replicate
1. One carrier abstraction with methods: `quote`, `create_label`, `void_label`, `track`.
2. Persist every request/response payload for audit.
3. Separate label creation from order-status mutation.
4. Make service mappings admin-configurable.
5. Unify all tracking writes through one table + event stream.
