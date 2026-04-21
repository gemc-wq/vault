# PRUNE App — Codex Build Brief

## What to Build
A Next.js 16 dashboard app called **PRUNE** (Product Retirement & Unused iNventory Engine) that displays dead/underperforming Amazon listings for retirement decisions.

## Tech Stack
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS 4
- @google-cloud/bigquery (server-side API routes)
- Light theme: white bg (#ffffff), cobalt accents (#2563eb), black text
- Font: system stack (-apple-system, BlinkMacSystemFont, etc.)
- Same visual style as: https://pulse-dashboard-inky.vercel.app

## Data Source: BigQuery Views

All data comes from 4 pre-built BQ views in `instant-contact-479316-i4.zero_dataset`:

### 1. `v_prune_summary` — Dashboard overview cards
```
entity_type (STRING): 'designs' | 'devices'
recommendation (STRING): 'RETIRE' | 'TOO_NEW' | 'LOW_PERFORMER' | 'ACTIVE'
tier (INT64): 0 (active), 1 (dead designs), 3 (dead devices), 4 (low performers)
entity_count (INT64): number of designs/devices
listing_count (INT64): total listings affected
revenue_12mo (FLOAT64): 12-month revenue
est_annual_fee (FLOAT64): estimated annual Amazon listing fees
```

### 2. `v_prune_dead_designs` — Design-level detail
```
design_code (STRING), listing_count (INT64), fba_count (INT64),
earliest_listing (DATE), latest_listing (DATE),
revenue_12mo (FLOAT64), orders_12mo (INT64),
is_dead (BOOL), recommendation (STRING): RETIRE|TOO_NEW|LOW_PERFORMER|ACTIVE,
prune_tier (INT64): 0|1|4
```

### 3. `v_prune_dead_lineups` — Product type × design combos
```
product_type_code (STRING), design_code (STRING),
listing_count (INT64), earliest_listing (DATE),
revenue_12mo (FLOAT64), orders_12mo (INT64),
is_dead (BOOL), recommendation (STRING)
```

### 4. `v_prune_dead_devices` — Device-level analysis
```
device_code (STRING), listing_count (INT64), design_count (INT64),
earliest_listing (DATE), revenue_12mo (FLOAT64), orders_12mo (INT64),
last_sale_date (DATE), is_dead (BOOL), recommendation (STRING)
```

## BQ Connection (same pattern as PULSE)

```typescript
// lib/bq-client.ts
import { BigQuery } from "@google-cloud/bigquery";
const credJson = process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
const credentials = credJson ? JSON.parse(credJson) : undefined;
const bq = new BigQuery({ projectId: "instant-contact-479316-i4", credentials });
```

Env var `GOOGLE_APPLICATION_CREDENTIALS_JSON` is already set on Vercel team `ecells-projects-3c3b03d7`.

## Pages

### 1. `/` — Overview Dashboard
- **Summary cards** (top row):
  - Total Dead Listings (RETIRE tier) — count + est. fee savings
  - Low Performers (Tier 4) — count + revenue vs. fee comparison
  - Active Listings — count + revenue
  - Net Savings Opportunity — total fees on dead/low minus revenue
- **Pie chart** or donut: listing distribution by recommendation
- **Tier breakdown table**: tier, entity count, listings, revenue, fees, net impact

### 2. `/designs` — Design Explorer
- Sortable table of all designs from `v_prune_dead_designs`
- Columns: Design Code, Listings, FBA, Revenue (12mo), Orders, First Listed, Recommendation, Tier
- Filter by: recommendation (RETIRE / LOW_PERFORMER / ACTIVE / all), min/max revenue
- Color-code rows: red = RETIRE, orange = LOW_PERFORMER, green = ACTIVE
- Default sort: listing_count DESC (biggest impact first)
- Pagination (50 per page)

### 3. `/lineups` — Lineup Drill-Down
- Table from `v_prune_dead_lineups`
- Columns: Product Type, Design Code, Listings, Revenue (12mo), Orders, First Listed, Recommendation
- Filter by: product_type_code, recommendation
- Group-by toggle: show grouped by product_type_code with subtotals

### 4. `/devices` — Device Analysis
- Table from `v_prune_dead_devices`
- Columns: Device Code, Listings, Designs, Revenue (12mo), Orders, Last Sale, Recommendation
- Sort by listing_count DESC default
- Highlight devices with 0 sales in red

### 5. `/export` — CSV Export
- Select scope: All Dead / Tier 1 Only / Low Performers / Dead Devices / Custom
- Select columns to include
- Generate and download CSV
- Show preview of first 20 rows before download
- **Key output:** CSV with columns: seller_sku, asin1, action (CLOSE/REVIEW), reason, revenue_12mo
  - This requires an API route that JOINs the views back to `amazon_active_listings` to get individual SKUs

## API Routes

### `GET /api/summary`
Query `v_prune_summary`, return JSON array.

### `GET /api/designs?recommendation=RETIRE&sort=listing_count&order=desc&page=1&limit=50`
Query `v_prune_dead_designs` with filters. Return `{ rows, total, page, pages }`.

### `GET /api/lineups?product_type=HTPCR&recommendation=RETIRE&page=1`
Query `v_prune_dead_lineups` with filters.

### `GET /api/devices?recommendation=RETIRE&sort=listing_count`
Query `v_prune_dead_devices` with filters.

### `GET /api/export?scope=retire&format=csv`
Generate CSV by joining back to `amazon_active_listings`:
```sql
SELECT a.seller_sku, a.asin1, a.item_name, d.recommendation, d.revenue_12mo
FROM v_prune_dead_designs d
JOIN amazon_active_listings a
  ON SPLIT(a.seller_sku, '-')[SAFE_OFFSET(2)] = d.design_code
WHERE d.recommendation = 'RETIRE'
```

## Layout
- Sidebar nav (same as PULSE): Overview, Designs, Lineups, Devices, Export
- Header: "PRUNE" with subtitle "Product Retirement & Unused iNventory Engine"
- Responsive but desktop-first

## Mock Data
Include mock data fallback (same pattern as PULSE) for when BQ is unavailable. Use realistic numbers from the summary above.

## Dependencies
```json
{
  "@google-cloud/bigquery": "^8.1.1",
  "next": "^16.1.6",
  "react": "^19",
  "tailwindcss": "^4",
  "lucide-react": "^0.577.0"
}
```

## Deploy
After build passes (`npm run build`), deploy with:
```bash
npx vercel deploy --prod --token <token> --yes
```

Git user.email must be `gemc99@me.com`.
