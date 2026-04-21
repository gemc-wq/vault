# Weekly Listing Audit — Cross-Region Gap + PRUNE Analysis

## Data Available
- Local SQLite: `data/local_listings.db`
  - `listings_current` — 3.44M US Active Listings (Mar 21)
  - `listings_uk_current` — 5.1M UK Active Listings (Mar 21)
  - Both have: seller_sku, asin, item_name, price, quantity, open_date
- BQ Orders: accessible via `bq query` CLI
- SKU format: {PRODUCT_TYPE}-{DEVICE}-{DESIGN}-{VARIANT}
- F prefix = FBA (strip for canonical type). Exceptions: FLAG, F1309, FRND, FKFLOR

## Analysis Required

### 1. Cross-Region Gap Analysis
- Find designs selling well in UK that are NOT listed on US Amazon
- Find designs selling well in US that are NOT listed on UK Amazon
- "Selling well" = use BQ orders data for last 90 days, buyer_country filter
- Group by design (position 2-3 of SKU: DESIGN-VARIANT)
- Output: ranked gap list by revenue opportunity

### 2. PRUNE Correlation
- Find listings with open_date before 2025-06-01 (aged >9 months)
- Cross-reference with BQ orders: which have ZERO sales in all of 2025?
- Group by: design, license (brand prefix), product type, device
- Identify patterns: are there entire licenses, devices, or product types with no sales?
- Calculate: how many listings × $0.06/month fee = annual waste

### 3. Output
- Save results to: `projects/weekly-listing-audit/` as JSON + MD report
- Post sanitized summary (no revenue numbers) to Slack #eod-listings
