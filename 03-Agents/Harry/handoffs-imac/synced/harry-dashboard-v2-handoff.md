# Handoff: Sales Dashboard V2 → Harry for Cloud Run Deployment

**Updated: Mar 3, 2026 10:23 AM**

## Repo
- **GitHub:** https://github.com/gemc99-boop/sales-dashboard
- **Vercel (frontend only):** https://sales-dashboard-iota-six.vercel.app

## What's Built (V2)
- Express API server (server.js) + BigQuery live data (2.8M orders)
- **Date range selector** — 7d, 30d, 90d, YTD, 1Y, All, custom picker
- **Sales Channels tab** — Amazon, eBay, Own Sites, Rakuten, Walmart, B2B, Other
- **5-region territories** — US, UK, Europe, Japan, ROW
- **Brands tab** — Sales by license (Brand column from orders)
- **Design Groups tab** — JOINs headcase.tblLineups for readable lineup names
- **Designs tab** — Parent-Child level detail
- **Multi-currency → USD conversion** — GBP×1.27, EUR×1.08, JPY×0.0067, AUD×0.65, SEK×0.095, CHF×1.12, CAD×0.74, PLN×0.25
- **5-min query cache** to control BigQuery costs
- **Dockerfile** ready for Cloud Run

## 8 Tabs
Overview | Product Types | Devices | Brands | Design Groups | Designs | Top SKUs | Opportunities

## Deploy to Cloud Run
```bash
git clone https://github.com/gemc99-boop/sales-dashboard
cd sales-dashboard
gcloud run deploy sales-dashboard \
  --source=. \
  --project=opsecellglobal \
  --region=us-east1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi
```

## Env Vars (set in Cloud Run)
```
GOOGLE_CLOUD_PROJECT=instant-contact-479316-i4
BIGQUERY_DATASET=zero_dataset
BIGQUERY_TABLE=orders
PORT=8080
```

## BigQuery Tables Used
- `zero_dataset.orders` — 2.8M orders (2020–present)
- `headcase.tblLineups` — 10,265 lineups (for Design Groups readable names)

## Known Issue
- GCS permissions on `instant-contact-479316-i4` blocked direct deploy — try `opsecellglobal` project or fix IAM (175143437106-compute needs Storage Object Viewer)

## FX Rates
Hardcoded in server.js USD_CONVERSION CASE statement. Update periodically or replace with a live FX API later.
