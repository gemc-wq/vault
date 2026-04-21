# BQ API Route Fix Brief

## Problem
All API routes reference columns (`design_code`, `device_code`, `product_type_code`, `design_variant`) that exist in Supabase but NOT in the BigQuery `orders` table.

## BQ `orders` Table Schema
```
Sales_Record_Number, Paid_Date, Dispatch_Date, Custom_Label, Quantity, 
Buyer_Country, Status, Is_Refunded, Currency, Net_Sale, GBP_Price, 
GBP_Exchange_Rate, Marketplace, TransactionID, PO_Date, PO_Location, 
Brand, Product, Unit
```

## SKU Parsing Rule
`Custom_Label` contains the SKU in format: `PRODUCT_TYPE-DEVICE-DESIGN_CODE-VARIANT`

Examples:
- `HTPCR-IPH7P-OSLICK-RCK` → product_type=HTPCR, device=IPH7P, design=OSLICK, variant=RCK
- `HC-IPH13-IMGCUAL-CTI` → product_type=HC, device=IPH13, design=IMGCUAL, variant=CTI
- `HLBWH-IPH13-MKECDG2-LGRY` → product_type=HLBWH, device=IPH13, design=MKECDG2, variant=LGRY
- `H8939-ONECT-CFCMLOG-BMA` → product_type=H8939, device=ONECT, design=CFCMLOG, variant=BMA

BQ SQL parsing:
```sql
SPLIT(Custom_Label, '-')[SAFE_OFFSET(0)] AS product_type_code
SPLIT(Custom_Label, '-')[SAFE_OFFSET(1)] AS device_code  
SPLIT(Custom_Label, '-')[SAFE_OFFSET(2)] AS design_code
SPLIT(Custom_Label, '-')[SAFE_OFFSET(3)] AS design_variant
```

## Files to Fix
1. `app/api/velocity/route.ts` — Replace all `design_code`, `device_code`, `product_type_code` references with SPLIT parsing from `Custom_Label`
2. `app/api/alerts/route.ts` — Same
3. `app/api/licenses/route.ts` — Same  
4. `app/api/listings/route.ts` — Same
5. `app/api/sessions/route.ts` — Check if uses BQ
6. `app/api/tracking/route.ts` — Check if uses BQ

## Additional BQ Tables Available
- `zero_dataset.amazon_active_listings` — 3.44M rows (sku, asin, product_name, etc.)
- `zero_dataset.walmart_active_listings` — 95,640 rows (sku, item_id, product_name, etc.)

## BQ Config
- Project: `instant-contact-479316-i4`
- Dataset: `zero_dataset`
- Orders table: `orders` (VIEW over ~2.8M rows)

## Testing
After fixing, verify by running: `curl https://pulse-dashboard-inky.vercel.app/api/velocity`
Should return `"source": "bigquery"` instead of `"source": "fallback-mock"`

## Also
- Remove the test-bq diagnostic endpoint (`app/api/test-bq/`) after confirming fix works
- Keep the `bqError` field in the fallback response for debugging
