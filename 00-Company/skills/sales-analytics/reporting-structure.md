# Reporting Structure

> Weekly and periodic report formats, interpretation guides, and data flow.

## Weekly Reports

### PULSE Leaderboard
- **What**: Top designs ranked by sales velocity (units/day, 7-day moving average)
- **Granularity**: Design level, per marketplace
- **Columns**: Rank, Design Code, License, Units (7d), Revenue (7d), Velocity, Velocity Delta, CVR
- **Use**: Identify which designs to prioritize for FBA, ads, and new device expansion

### Active Listings Delta
- **What**: Net change in active listings vs previous week
- **Columns**: Marketplace, New Listings, Removed/Suppressed, Net Delta, Total Active
- **Use**: Track catalog coverage growth; catch bulk suppressions early
- **Alert**: Net delta negative for any marketplace = investigate immediately

### Movers Analysis
- **What**: Designs with significant week-over-week velocity changes
- **Accelerating**: Velocity up >20% WoW with >5 units/week baseline
- **Decelerating**: Velocity down >20% WoW with >5 units/week baseline
- **Use**: Catch trending designs early, flag declining designs for intervention

### Business Report (Child ASIN)
- **What**: SP-API Business Report data at child ASIN level
- **Columns**: ASIN, SKU, Sessions, Page Views, Units, Revenue, CVR, B2B Units
- **Use**: Variant-level performance, traffic source analysis, conversion optimization

## Interpretation Guide

| Term       | Definition                                            | Calculation                  |
|------------|-------------------------------------------------------|------------------------------|
| Velocity   | Units sold per day, smoothed                          | 7-day moving average         |
| Momentum   | Acceleration of velocity                              | (Velocity_thisWeek - Velocity_lastWeek) / Velocity_lastWeek |
| Coverage   | % of champion designs listed in a marketplace         | Listed_champions / 590       |
| Sell-through | Units sold / Units available                        | From FBA inventory reports   |

### Reading Momentum
- Momentum > +20%: design is accelerating -- consider increasing ad spend
- Momentum -10% to +10%: stable -- maintain current strategy
- Momentum < -20%: decelerating -- check for listing issues, competition, seasonality

### Reading Coverage
- Target: 100% of 590 champion designs listed in US, UK, DE
- FR, IT, ES: target 80% coverage (lower volume markets)
- Coverage gaps = missed revenue; prioritize listing creation

## Shipping Template Compliance

| Marketplace | Required Template               | Notes                     |
|-------------|----------------------------------|---------------------------|
| US          | Reduced Shipping Template        | Must be assigned to all FBM |
| DE          | Standardvorlage Amazon           | German name required       |
| UK          | TBC                              | Awaiting confirmation      |
| FR          | Default marketplace template     | --                         |
| IT          | Default marketplace template     | --                         |
| ES          | Default marketplace template     | --                         |

Non-compliance = longer delivery promise = lower Buy Box win rate = lower CVR.

## FBA vs FBM Analysis

### Identifying FBA Listings
- SKU starts with F-prefix (e.g., FHTPCR vs HTPCR)
- Same design + device but different fulfillment channel
- Pair them using base_sku (see sku-parsing-rules.md)

### Measuring FBA Lift
```
FBA_CVR_Lift = FBA_CVR / FBM_CVR
```
- Target: 2-3x CVR lift from FBA
- If lift < 1.5x: investigate pricing, images, Buy Box share
- If lift > 3x: strong signal to migrate more designs to FBA

### FBA Migration Priority
1. Champion designs (top 590) not yet in FBA
2. Designs with FBM CVR > 4% (already converting well, FBA will amplify)
3. High-session designs with low CVR (FBA badge may fix trust gap)

## Data Flow

```
SP-API Middleware (Cloud Run)
  -> Pulls reports automatically (daily/weekly)
  -> Writes to BigQuery (amazon_reports dataset)
    -> Hermes runs analysis queries
      -> Generates PULSE, Movers, Delta reports
        -> Stores in vault / sends via Telegram
          -> Ava reviews for strategic decisions
            -> Cem approves major changes
```

## BigQuery Tables (amazon_reports)

| Table                    | Refresh   | Key Columns                                    |
|--------------------------|-----------|------------------------------------------------|
| business_reports         | Weekly    | asin, sku, sessions, page_views, units, revenue|
| order_reports            | Daily     | order_id, asin, sku, quantity, price, date     |
| settlement_reports       | Monthly   | settlement_id, amount, type, marketplace       |
| active_listings          | Weekly    | sku, asin, status, price, quantity, marketplace |
| fba_inventory            | Daily     | sku, asin, fulfillable_qty, marketplace        |
