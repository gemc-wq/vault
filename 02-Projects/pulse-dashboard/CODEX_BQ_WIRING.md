# CODEX BRIEF: Wire PULSE Dashboard to Live BigQuery

## Objective
Replace all mock data in the PULSE dashboard with live BigQuery queries. Currently all 6 API routes serve static JSON from `lib/mock-data.ts`. Wire them to real BQ tables.

## BQ Connection Setup

### 1. Install dependency
```bash
npm install @google-cloud/bigquery
```

### 2. Create `lib/bq-client.ts`
```typescript
import { BigQuery } from '@google-cloud/bigquery';

let bqClient: BigQuery;

export function getBQ(): BigQuery {
  if (!bqClient) {
    // Option 1: Service account JSON from env (Vercel)
    const credJson = process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
    if (credJson) {
      const credentials = JSON.parse(credJson);
      bqClient = new BigQuery({
        projectId: process.env.BIGQUERY_PROJECT_ID || 'instant-contact-479316-i4',
        credentials,
      });
    } else {
      // Option 2: ADC (local dev)
      bqClient = new BigQuery({
        projectId: process.env.BIGQUERY_PROJECT_ID || 'instant-contact-479316-i4',
      });
    }
  }
  return bqClient;
}

export const DATASET = process.env.BIGQUERY_DATASET_ID || 'zero_dataset';
```

### 3. Add to `.env.local` (already partial in `.env`):
```
BIGQUERY_PROJECT_ID=instant-contact-479316-i4
BIGQUERY_DATASET_ID=zero_dataset
```

## API Route Rewrites

### `/api/velocity/route.ts` — Velocity Data
Query the orders table for design velocity (last 60 days vs prior 60 days):
```sql
WITH recent AS (
  SELECT design_code, COUNT(*) as recent_orders, 
    SUM(SAFE_CAST(Net_Sale AS FLOAT64)) as recent_rev
  FROM `instant-contact-479316-i4.zero_dataset.orders`
  WHERE Paid_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
  GROUP BY 1
),
prior AS (
  SELECT design_code, COUNT(*) as prior_orders,
    SUM(SAFE_CAST(Net_Sale AS FLOAT64)) as prior_rev
  FROM `instant-contact-479316-i4.zero_dataset.orders`
  WHERE Paid_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 120 DAY)
    AND Paid_Date < DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
  GROUP BY 1
)
SELECT r.design_code, r.recent_orders, r.recent_rev,
  COALESCE(p.prior_orders, 0) as prior_orders,
  COALESCE(p.prior_rev, 0) as prior_rev,
  SAFE_DIVIDE(r.recent_orders - COALESCE(p.prior_orders,0), COALESCE(p.prior_orders,1)) as velocity_change
FROM recent r
LEFT JOIN prior p ON r.design_code = p.design_code
ORDER BY r.recent_rev DESC
LIMIT 200
```

Keep the response shape matching existing `velocityRows` type. Preserve `summary` and `trend` fields but compute them from live data.

### `/api/licenses/route.ts` — License Performance
```sql
SELECT 
  -- Parse license from design_code or join with headcase.tblDesigns if available
  design_code,
  COUNT(*) as total_orders,
  SUM(SAFE_CAST(Net_Sale AS FLOAT64)) as total_rev,
  COUNT(DISTINCT device_code) as device_coverage
FROM `instant-contact-479316-i4.zero_dataset.orders`
WHERE Paid_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY 1
ORDER BY total_rev DESC
LIMIT 100
```

### `/api/alerts/route.ts` — PULSE Alerts
Cross-reference velocity designs with marketplace existence:
```sql
WITH velocity AS (
  SELECT design_code, COUNT(*) as orders_60d,
    SUM(SAFE_CAST(Net_Sale AS FLOAT64)) as rev_60d
  FROM `instant-contact-479316-i4.zero_dataset.orders`
  WHERE Paid_Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
  GROUP BY 1
  HAVING orders_60d >= 5
),
walmart_designs AS (
  SELECT DISTINCT 
    REGEXP_EXTRACT(sku, r'^[A-Z0-9]+-[A-Z0-9]+-([A-Z0-9]+)') as design_code
  FROM `instant-contact-479316-i4.zero_dataset.walmart_active_listings`
),
amazon_designs AS (
  SELECT DISTINCT
    REGEXP_EXTRACT(seller_sku, r'^[A-Z0-9]+-[A-Z0-9]+-([A-Z0-9]+)') as design_code
  FROM `instant-contact-479316-i4.zero_dataset.amazon_active_listings`
)
SELECT v.design_code, v.orders_60d, v.rev_60d,
  wd.design_code IS NOT NULL as on_walmart,
  ad.design_code IS NOT NULL as on_amazon
FROM velocity v
LEFT JOIN walmart_designs wd ON v.design_code = wd.design_code
LEFT JOIN amazon_designs ad ON v.design_code = ad.design_code
ORDER BY v.rev_60d DESC
```

### `/api/listings/route.ts` — Listing Status
```sql
SELECT 
  'walmart' as marketplace,
  COUNT(*) as total_listings,
  COUNT(DISTINCT REGEXP_EXTRACT(sku, r'^[A-Z0-9]+-[A-Z0-9]+-([A-Z0-9]+)')) as unique_designs,
  COUNTIF(buy_box_eligible) as buybox_eligible
FROM `instant-contact-479316-i4.zero_dataset.walmart_active_listings`
UNION ALL
SELECT 
  'amazon' as marketplace,
  COUNT(*) as total_listings,
  COUNT(DISTINCT REGEXP_EXTRACT(seller_sku, r'^[A-Z0-9]+-[A-Z0-9]+-([A-Z0-9]+)')) as unique_designs,
  0 as buybox_eligible
FROM `instant-contact-479316-i4.zero_dataset.amazon_active_listings`
```

### `/api/sessions/route.ts` — Session/Conversion Data  
Keep as mock for now — we don't have session data in BQ yet. Add a `source: "mock"` flag.

### `/api/tracking/route.ts` — Closed-Loop Tracking
Keep as mock for now — tracking hasn't been implemented yet. Add a `source: "mock"` flag.

## Important Notes
- All BQ queries must use `SAFE_CAST(Net_Sale AS FLOAT64)` — Net_Sale is STRING type
- Column names are PascalCase: `Custom_Label`, `Net_Sale`, `Paid_Date`, `Marketplace`
- Pre-parsed columns exist on orders: `design_code`, `device_code`, `product_type_code`, `design_variant` — USE THESE, don't re-parse Custom_Label
- Amazon listings table column for SKU is `seller_sku` (check schema before querying)
- Add error handling: if BQ query fails, fall back to existing mock data with `source: "fallback-mock"`
- Add response caching: cache BQ results for 5 minutes (use simple in-memory Map with TTL)
- Keep all existing TypeScript types in `lib/types.ts` — shape the BQ response to match

## Verification
After wiring, run `npm run dev` and verify:
1. `/api/velocity` returns live data (check a known design_code against BQ)
2. `/api/alerts` shows real marketplace gaps
3. `/api/listings` shows correct counts (95,640 Walmart, ~3.44M Amazon)
4. No TypeScript errors (`npm run build`)

## DO NOT
- Change the UI/frontend components
- Modify the theme/styling
- Remove mock data files (keep as fallback)
- Deploy to Vercel (no service account key yet)
