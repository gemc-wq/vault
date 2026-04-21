# PULSE Dashboard — Build Brief for Codex

## What You're Building
A Next.js + React + TypeScript + Tailwind CSS dashboard called **PULSE** (Product Uplift & Listing Signal Engine). It's an e-commerce analytics dashboard that identifies sales velocity opportunities and gaps across multiple marketplace channels.

## Tech Stack
- **Next.js 14+** (App Router)
- **React 18+** with TypeScript
- **Tailwind CSS** for styling
- **Supabase** for postgres data (via `@supabase/supabase-js`)
- **BigQuery** for read-only order data (via `@google-cloud/bigquery`)
- **Chart.js** or **Recharts** for visualizations
- **Vercel** deployment target

## Supabase Connection
```
URL: https://auzjmawughepxbtpwuhe.supabase.co
Anon Key: [REDACTED_SUPABASE_ANON_KEY]
Service Role Key: [REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc
```

## BigQuery Connection
- Project: `instant-contact-479316-i4`
- Dataset: `zero_dataset`
- Table: `orders` (VIEW, 2.8M rows)
- Auth: Application Default Credentials (gcloud auth already configured on this machine)
- Key columns: `design_code`, `device_code`, `product_type_code`, `paid_date`, `total_sale`, `currency`, `net_sale_usd`, `marketplace`

## Data Files (local, for initial ETL/loading)
- Amazon Active Listings: `../../data/amazon/Active+Listings+Report_03-05-2026.txt` (6.4GB, tab-delimited, 3.44M rows)
  - Columns: item-name, item-description, listing-id, seller-sku, price, quantity, open-date, image-url, item-is-marketplace, product-id-type
- Amazon Child ASIN Report: `../../data/amazon/BusinessReportbychildAmazonUS_Jan1_Feb24 1.xlsx` (80K rows)
  - Columns: (Parent) ASIN, (Child) ASIN, SKU, Sessions - Total, Page Views - Total, Featured Offer (Buy Box) Percentage, Units Ordered, Unit Session Percentage, Ordered Product Sales
- License Obligations: `../../data/Royalty_Advance_summary.xlsx` (37 licenses)

## Dashboard Pages (8 total)

### 1. Velocity Overview (Home/Landing)
- All designs ranked by velocity ratio (2mo revenue ÷ 6mo monthly avg)
- Color-coded signal tiers: 🚀 Surging (>2x), 📈 Accelerating (1.3-2x), ➡️ Steady, 📉 Declining, 💀 Dying
- Filters: license/brand, product type, device, signal tier
- Summary cards at top: total designs tracked, # surging, # dying, total 90d revenue
- Data source: BigQuery orders

### 2. LIST IT Alerts
- Table of surging SKUs with channel distribution gaps
- Columns: Design, Brand/License, Velocity Ratio, Conversion Rate, Amazon ✅/❌, Walmart ✅/❌, Target+ ✅/❌, eBay ✅/❌, GoHeadCase ✅/❌, Est. Gap Revenue
- License urgency badge on each row
- Sortable by velocity, gap revenue, license urgency
- Data: BQ velocity × Amazon Active Listings cross-reference

### 3. COMPLETE IT Alerts
- Device family gap analysis
- Shows designs where some devices in a family are listed but others aren't
- E.g., iPhone 16 Pro Max ✅ but iPhone 16 / Plus / Pro ❌
- Grouped by design, showing which family members are missing

### 4. BUILD IT Matrix
- Cross-leaderboard matrix (THE CORE VIEW)
- Rows: Top designs by composite opportunity score
- Columns: Product types (HTPCR, HLBWH, HB401, HDMWH, HC, Console Wrap)
- Cells: Show revenue + conversion + sessions if LIVE; show opportunity SCORE if gap
- Gap cells highlighted (green = high opportunity, yellow = medium, gray = low)
- Click any gap cell → drill-down report (modal or new page)
- Heatmap visualization

### 5. BUILD IT Drill-Down (modal or page)
- Individual opportunity report
- Sections: Design Evidence, Form Factor Evidence, Analog Evidence, License Context
- Proposed product list with device matrix
- Estimated quarterly revenue
- Confidence score (triple-validated = HIGH)

### 6. FIX IT / BOOST IT
- Two tabs or split view
- FIX IT: High sessions (>500/mo) + low conversion (<2%) + good Buy Box (>80%). Table with design, sessions, conversion, Buy Box, suggested fix action
- BOOST IT: High conversion (>5%) + low sessions (<200/mo). Table with design, conversion, sessions, suggested boost action

### 7. License Dashboard
- All 37 licenses with: name, MG amount (USD), annual cost, current run rate (90d annualized), gap ratio, months remaining, expiry date
- Color-coded urgency: 🔴 Behind, ⚠️ Watch, ✅ Ahead, 💀 Expired
- Click license → see all PULSE alerts for designs under that license
- Summary cards: total MG committed, total at risk, total covered

### 8. Tracking (Closed-Loop)
- Action log: alerts acted on, date, type, predicted revenue
- Outcome tracker: 30/60/90-day actual vs predicted
- Hit rate metrics: % of alerts that met or exceeded prediction
- Chart: predicted vs actual over time

## Design Guidelines
- Dark theme (dark background, light text) — professional analytics dashboard
- Use a sidebar navigation (like Sales Dashboard V2)
- Responsive but desktop-first (this is an internal tool)
- Use consistent color coding for signal tiers across all pages
- Cards with shadow for summary metrics
- Tables should be sortable and filterable

## API Routes (Next.js API routes for data)
- `/api/velocity` — fetch velocity data from BQ (design-level, with baseline + velocity windows)
- `/api/listings` — fetch Amazon active listings status (from Supabase once loaded)
- `/api/sessions` — fetch Amazon session/conversion data (from Supabase once loaded)
- `/api/licenses` — fetch license obligations (from Supabase once loaded)
- `/api/alerts` — generate PULSE alerts (combine velocity + listings + sessions)
- `/api/tracking` — CRUD for closed-loop tracking data

## Important Notes
1. Start with the Velocity Overview page and License Dashboard — these can work with just BigQuery data
2. The BUILD IT Matrix and LIST IT alerts need the Amazon data loaded into Supabase first — you can scaffold the pages with mock data and wire up later
3. Use server components where possible for data fetching
4. The velocity calculation is: (sum of revenue in last 2 months) ÷ (average monthly revenue over last 6 months)
5. Git commits must use email `gemc99@me.com` for Vercel deployment

## Scaffold First
Create the full project structure, all pages, navigation, and layout FIRST with placeholder/mock data. Then wire up real data connections one page at a time. This lets us deploy and iterate.

When completely finished, run this command to notify me:
openclaw system event --text "Done: PULSE Dashboard scaffolded — all 8 pages, navigation, dark theme, mock data. Ready for data wiring." --mode now
