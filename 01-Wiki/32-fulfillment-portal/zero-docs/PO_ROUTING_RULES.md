# PO Routing Rules

Source: `~/Downloads/zero/barcode/POFiltering.php`

## Purpose
`CustomLabelFiltering()` is the core warehouse-routing function for purchase-order generation. It decides whether each order line should be routed to:

- `ForPHProd` → Philippines (`ECELLMFG`)
- `ForUKProd` → UK (`ECELL UK`)
- `ForUSAProd` → Florida / US (`ECELLUSA`)
- `ForDEProd` → Germany (`ECELLDE`)
- or held / rejected (`HOLD`, `INVALID`, `EOL`)

The file also maps production remarks to Sage warehouses:

```php
$productions_arr = array(1=>'ForPHProd', 2=>'ForUKProd', 3=>'ForUSAProd', 4=>'ForDEProd');
$production_warehouse = array('ForPHProd'=>'ECELLMFG', 'ForUKProd'=>'ECELL UK', 'ForUSAProd'=>'ECELLUSA', 'ForDEProd'=>'ECELLDE');
```

## Stock inputs
The routing logic loads live stock from Sage per warehouse before evaluating lines:

```php
$uk_available_units = SageWarehouseRawMaterialsWithStocks(..., array('UK'), " > 0 ", "1");
$fl_available_units = SageWarehouseRawMaterialsWithStocks(..., array('Florida'), " > 0 ", "2");
$de_available_units = SageWarehouseRawMaterialsWithStocks(..., array('DE'), " > 0 ", "1");
$ph_eol_units = SageWarehouseRawMaterialsWithStocks($parsed_cl_to_rm, $exclude_items, array("DISC"), array(), array('PH'), " = 0 ", "7");
```

### Key behavior
- UK/FL/DE stock is only considered if free stock exists for the exact `brand+product+color-unit` code.
- Once allocated in-memory, the script decrements `FreeStock` so later lines do not over-allocate.
- PH is the default fallback warehouse.
- If PH is selected **and** the unit is in the PH end-of-life / discontinued stock set, the result becomes `EOL`.

## Core decision tree

```php
elseif($toup_buyer_country == ""){
    $remark_msg = "Hold";
    $information = "ForOrderDetailsVerification";
}
...
elseif(strpos($val['Sales_Record_Number'], "PO") === false && array_key_exists($amazon_parent_srn, $amazon_prime_orders)){
    ... prime routing ...
}
...
elseif($product_code == "54" && $unit_code == "POPS"){
    $remark_msg = $productions_arr[2];
}
...
elseif(in_array($toup_buyer_country, $country_exclusions)){
    $remark_msg = $productions_arr[1];
}
...
if($uk_available_units[$producttype_unitcode]['FreeStock'] > 0 && $uk_available_units[$producttype_unitcode]['FreeStock'] >= $quantity){
    $remark_msg = $productions_arr[2];
    $uk_available_units[$producttype_unitcode]['FreeStock'] -= $quantity;
}
```

## Pseudocode of all active IF/ELSE rules

```text
parse custom label -> brand/product_code/product_color/unit_code/family_code/design_code
producttype_unitcode = brand+product_code+product_color + '-' + unit_code
normalize HBCCR -> HC

IF custom label parse fails
  route = INVALID
  info = Un_ID CL
ELSE IF buyer country blank
  route = HOLD
  info = ForOrderDetailsVerification
ELSE IF full address equals hardcoded Morocco blocked address
  route = HOLD
  info = BlockedUser
ELSE IF family_code in discontinued_licenses_lineup
  route = HOLD
  info = DISCON License
ELSE IF non-PO SRN AND amazon parent SRN is in amazon_prime_orders
  IF prime site in [Amazon.co.uk, Amazon.es, Amazon.fr, Amazon.de, Amazon.it]
    IF buyer country in uk_countries
      route = UK
    ELSE IF prime site == Amazon.de AND buyer country in eligible_countries_for_de_filter
      route = DE
    ELSE
      route = PH
  ELSE IF prime site in [Amazon.com (US), Amazon.ca (US)]
    route = FL
  ELSE
    route = PH
ELSE IF non-PO SRN AND marketplace_site_id == 3 AND postage_service is expedited/non-standard and transactionid != Amazon.nl
  IF buyer country in eligible_countries_for_uk_filter -> UK
  ELSE IF buyer country in us_countries -> FL
  ELSE -> DE
ELSE IF product_code == 54 AND unit_code == POPS
  route = UK
ELSE IF family starts XBOX/HALO AND buyer country in US
  route = HOLD for CS refund
ELSE IF email/buyer matches coolcase.cz / Pavel Hluzek / Jiri Kabelka
  route = HOLD:Jiri
ELSE IF marketplace_site_id == 20
  route = FL
ELSE IF family-design is in special_3d_print
  route = PH
ELSE IF 1D license on IPADAIR2/IPAD5
  route = PH
ELSE IF buyer country in country_exclusions
  route = PH
ELSE IF SRN contains PO
  route = PH
ELSE IF family_code in familyfor_PH
  route = PH
ELSE IF product_code-specific family+design in family_design_for_ph
  route = PH
ELSE IF product_code-specific family in product_type_family_for_ph
  route = PH
ELSE IF family starts TWD AND product_code == BC
  route = PH
ELSE IF SRN in srn_multiple_orders_list
  route = PH
ELSE
  IF UK filtering enabled AND unit exists in uk_available_units AND buyer country not US AND DE-not-forced-out AND buyer country in eligible UK list
    IF unit disabled in t_po_filtering_units.f_is_disabled_uk -> PH
    ELSE IF FreeStock >= qty -> UK and decrement UK stock
    ELSE -> PH
  ELSE IF FL filtering enabled AND unit exists in fl_available_units AND buyer country in US AND marketplace_site_id != 4
    IF unit_code in items_exclusions -> PH
    ELSE IF unit disabled in t_po_filtering_units.f_is_disabled_fl -> PH
    ELSE IF FreeStock >= qty -> FL and decrement FL stock
    ELSE -> PH
  ELSE IF DE filtering enabled AND unit exists in de_available_units AND buyer country not US AND buyer country not eligible UK
    IF unit disabled in t_po_filtering_units.f_is_disabled_de -> PH
    ELSE IF buyer country not in eligible_countries_for_de_filter_non_prime -> PH
    ELSE IF FreeStock >= qty -> DE and decrement DE stock
    ELSE -> PH
  ELSE
    route = PH

IF final route == PH AND unit exists in ph_eol_units
  route = EOL

IF SRN is force-mapped in ForceSRNToWarehouse()
  override final route to forced warehouse code
```

## Warehouse/product mapping patterns

### Explicit product/family rules
| Condition | Warehouse |
|---|---|
| `product_code == "54" && unit_code == "POPS"` | UK |
| `special_3d_print` family/design combos | PH |
| `familyfor_PH` | PH |
| `family_design_for_ph[product_code]` match | PH |
| `product_type_family_for_ph[product_code]` match | PH |
| `TWD*` + `BC` | PH |
| `marketplace_site_id == 20` (Staples) | FL |

### Geographic routing
| Condition | Warehouse |
|---|---|
| buyer in `eligible_countries_for_uk_filter` and UK stock available | UK |
| buyer in US-country list and FL stock available | FL |
| buyer not US and not UK-eligible, but DE stock available and country is DE-eligible | DE |
| anything else | PH |

## Day/date overrides
There is **no weekday-specific branch** inside `CustomLabelFiltering()` itself.

The closest hardcoded date override is in PO generation, not filtering. Example from `generate_purchase_order_automated_uk_wh.php`:

```php
$date_now = date('Y-m-d');
if($date_now == "2022-04-15" || $date_now == "2022-04-18"){
    echo $add_msg. "Script Exit - {$date_now}";
    exit;
}
```

So routing is not day-of-week driven, but downstream automation has date-based shutdowns.

## Supporting tables / fields
- `t_temp_PO_table`
  - `Sales_Record_Number`, `Custom_Label`, `Quantity`, `Remarks`, `Sage_Country`, `Sage_DB_ID`, `Sage_DB_Name`, `Information`
- `order_tracker_xls`
  - `Sales_Record_Number`, `Buyer_Country`, `Notes_to_Yourself`, `Postage_Service`
- `t_po_filtering_units`
  - `f_product_unit_code`, `f_group_id`, `f_is_disabled_uk`, `f_is_disabled_fl`, `f_is_disabled_de`
- `t_po_force_srns`
  - used by `ForceSRNToWarehouse()` / forced-routing logic

## JSON rules object
```json
{
  "defaultWarehouse": "PH",
  "remarksToWarehouse": {
    "ForPHProd": "ECELLMFG",
    "ForUKProd": "ECELL UK",
    "ForUSAProd": "ECELLUSA",
    "ForDEProd": "ECELLDE"
  },
  "priorityRules": [
    "invalid custom label -> INVALID",
    "missing buyer country -> HOLD",
    "blocked address -> HOLD",
    "discontinued license family -> HOLD",
    "Amazon Prime UK geography -> UK/DE/PH",
    "non-standard Amazon postage -> UK/FL/DE",
    "PO SRNs -> PH",
    "special 3D / family overrides -> PH",
    "Staples marketplace -> FL"
  ],
  "stockRules": {
    "UK": "eligible country + unit exists + not disabled + FreeStock >= qty",
    "FL": "US country + unit exists + marketplace_site_id != 4 + not disabled + FreeStock >= qty",
    "DE": "non-US + non-UK-eligible country + unit exists + DE-eligible + not disabled + FreeStock >= qty"
  },
  "postProcessing": {
    "PH_EOLOutput": "ForPHProd + ph_eol_units match -> EOL",
    "forcedSRNOverride": "t_po_force_srns / ForceSRNToWarehouse overrides computed route"
  }
}
```

## Hardcoded values that should become config
- Blocked address string for Morocco order
- Specific customer/email blacklist (`info@coolcase.cz`, `Pavel Hluzek`, `Jiri Kabelka ...`)
- `marketplace_site_id == 20` => Staples => FL
- `product_code == 54 && unit_code == POPS` => UK
- `XBOX` / `HALO` US hold rule
- `Amazon.de` / `Amazon.co.uk` site lists embedded in code
- `include_DE_inUKPrinting` behavior split across code + globals

## What to Replicate
1. A deterministic routing engine separated from UI.
2. Config-driven rule groups for:
   - customer blacklists
   - country eligibility
   - family/design/product overrides
   - forced SRN routing
   - warehouse disable lists
3. Real-time free stock reservation during batch evaluation.
4. Explainable outputs: `route`, `reason_code`, `reason_detail`, `stock_before`, `stock_after`.
5. A rule-audit screen replacing opaque `Remarks` strings.
