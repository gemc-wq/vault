# UK/DE Amazon Active Listings Reminder

Cem, to complete the regional ASIN→SKU bridges (which will push our match rate from ~84% to 95%+), I need the Active Listings CSVs from Seller Central for UK and DE.

## How to pull:
1. Go to Amazon Seller Central (UK / DE).
2. Reports -> Inventory Reports.
3. Select "Active Listings Report".
4. Request Report.
5. Download and save to `data/amazon/uk_active_listings.csv` and `data/amazon/de_active_listings.csv`.

Once those are in the workspace, I can run the parsing script to match up the missing regional variants.