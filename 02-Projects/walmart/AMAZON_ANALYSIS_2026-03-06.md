# Amazon Active Listings Analysis
> Source: Active+Listings+Report_03-05-2026.txt (6.87GB, mislabeled in Walmart folder)
> Analyzed: 2026-03-06

## Summary
- **3,441,323 total listings** across **3,435,585 unique ASINs**
- **100% Merchant Fulfilled (FBM)** — zero FBA listings
- **144,244 out of stock (qty=0)** — 4.2% of catalog
- This is the full Head Case Designs Amazon catalog

## Price Distribution
| Range | SKUs | % |
|-------|------|---|
| $5-10 | 75,818 | 2.2% |
| $10-20 | 2,261,979 | 65.7% |
| $20-30 | 1,072,287 | 31.2% |
| $30-50 | 31,089 | 0.9% |
| $50+ | 150 | <0.1% |

## Key Observations

### 🔴 Critical: Zero FBA
- **All 3.4M listings are FBM** — no Fulfillment by Amazon
- This is a massive competitive disadvantage: FBA gets Buy Box priority, Prime badge, faster shipping
- March 5 notes mention "Amazon FBA conversions" as a Revenue Growth pillar — this confirms why

### Scale Context
- **Amazon: 3.4M SKUs** vs **Walmart: 95.6K SKUs** (36x larger on Amazon)
- Amazon is clearly the primary marketplace by catalog size
- With 3.4M FBM listings, even converting 1% to FBA (34K SKUs) would be a significant operation

### FBA Conversion Strategy (from March 5 strategic realignment)
- Priority: Convert top-velocity SKUs to FBA first
- Need Amazon sales data to identify top sellers (currently unavailable — no Amazon data pipeline)
- FBA conversion requires: shipment plans, labeling, inventory shipment to Amazon warehouses
- At $10-20 avg price point, FBA fees (~$3-5/unit) need careful margin analysis

### Out of Stock Analysis
- 144K listings (4.2%) show qty=0
- These are dead weight — hurting account health metrics
- Should be either restocked or deactivated

## Cross-Platform Comparison
| Metric | Amazon | Walmart |
|--------|--------|---------|
| Total SKUs | 3,441,323 | 95,640 |
| Fulfillment | 100% FBM | 100% Seller |
| Price sweet spot | $10-20 (66%) | $20-30 (51%) |
| Reviews | Unknown | 99.9% zero |
| Buy Box | Unknown | 99.9% eligible |

## Recommended Actions
1. **Get Amazon Business Reports** — need sales velocity data to prioritize FBA conversions
2. **Clean up 144K OOS listings** — deactivate or restock
3. **Identify top 1,000 ASINs by revenue** → first FBA conversion batch
4. **Price harmonization** — Amazon skews cheaper ($10-20) vs Walmart ($20-30); investigate if Walmart prices should come down
5. **Amazon Ads data** → feed into Sales Dashboard V2 Opportunities tab
