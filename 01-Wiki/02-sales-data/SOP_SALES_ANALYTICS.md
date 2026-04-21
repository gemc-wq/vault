# SOP: Sales Data Analytics
*Version: 1.0 | Created: 2026-03-07 | Owner: Ava (CPSO)*

---

## Purpose
Standard operating procedure for running sales analytics that inform SKU selection, marketplace strategy, and business decisions. Ensures data integrity, recency, and actionable output.

---

## 1. Data Freshness Requirements

### Rule: ALWAYS CHECK DATA RECENCY FIRST
Before any analysis, verify:
```
Latest paid_date in orders table → compare to today's date
If gap > 7 days → FLAG AS STALE in every output
If gap > 30 days → HALT analysis, escalate to get fresh data
```

### Current State (as of 2026-03-07)
| Source | Latest Data | Gap | Status |
|--------|------------|-----|--------|
| Supabase `orders` | 2026-02-17 | **18 days stale** | ⚠️ Needs refresh |
| BigQuery | Continuously updated | Live | ✅ Source of truth |
| Walmart listings | Partial (10K of 95K) | Incomplete | ⚠️ Needs full load |

### Action: Data Refresh Pipeline
1. **Immediate:** Get `gcloud` CLI installed on Mac Studio for BigQuery access
2. **Target:** Daily automated sync from BigQuery → Supabase
3. **Until automated:** Manual export + import when analysis needed

---

## 2. Lookback Period Strategy

### Standard Lookback Windows
| Window | Use Case | Why |
|--------|----------|-----|
| **1 month** | Launch tracking, trend detection | New licenses (Naruto, NBA) only show true velocity here |
| **3 months** | SKU selection for Walmart/Target+ | Captures current device momentum without legacy noise |
| **6 months** | Brand strength, seasonal adjustment | Balances recency with sample size |
| **12 months** | Baseline rankings, annual planning | Full picture including Q4 spike |
| **All-time** | Historical reference only | ⚠️ Overweights legacy devices (iPhone 7/8), underweights new licenses |

### Critical Lookback Scenarios
| Scenario | Best Window | Rationale |
|----------|-------------|-----------|
| iPhone 17 family launch (Oct 2026) | 3 months post-launch | Shows adoption curve without pre-launch iPhone 16 dominance |
| Naruto/NBA SKU selection | 1-3 months | New licenses — all-time data dilutes their actual velocity |
| Target+ initial catalog | 3 months | Current momentum = best predictor of new channel performance |
| Walmart optimization | 3-6 months | Enough data for statistical significance, recent enough for relevance |
| UK marketplace (OnBuy) | 3 months, UK-only | Regional filter essential — US data irrelevant for UK channel |
| Germany (Kaufland) | 3 months, EU-only (currency=EUR, country filter DE) | German market differs from FR/IT/ES |

### Rule: ALWAYS SHOW MULTI-LOOKBACK COMPARISON
When ranking designs for SKU selection, show how ranks change:
```
| Design | 1mo Rank | 3mo Rank | 6mo Rank | All-Time Rank | Momentum |
|--------|----------|----------|----------|---------------|----------|
| NARUICO | #8       | #15      | #22      | #15           | 🔥 Rising |
| LFCKIT25| #14      | #7       | #10      | #14           | ➡️ Stable |
| HPOTDH13| #25      | #6       | #4       | #6            | 📉 Fading |
```
The **Momentum** column (1mo rank vs all-time rank) is THE key signal for SKU selection.

---

## 3. Regional Analysis Requirements

### Region Derivation
| Signal | Region | Notes |
|--------|--------|-------|
| currency=USD | US | Primary signal |
| currency=GBP | UK | |
| currency=EUR | EU | Further split by buyer_country when needed |
| currency=JPY | JP | Small volume but distinct preferences |
| buyer_country | Override | More precise when available |

### Region-Specific Reports Required For:
| Marketplace | Region Filter | Notes |
|-------------|---------------|-------|
| Amazon US | US only | iPhone-heavy, Harry Potter/Peanuts/WWE |
| Amazon UK | UK only | Samsung A16 5G top 10, football kits dominate |
| Amazon DE | EU, country=Germany | FC Barcelona, Inter Milan strong |
| Target+ | US only | **NO US Sports** (NFL/NBA/NHL/NCAA) |
| Walmart | US only | 95K SKUs, zero reviews |
| OnBuy | UK only | New UK marketplace — needs UK-specific catalog |
| Kaufland | EU, country=Germany | German market entry |
| GoHeadCase DTC | All regions | Full catalog, no license restrictions |

### Rule: Device Preferences Vary by Region
- **US:** iPhone-dominant, desk mats significant, Samsung S series
- **UK:** Samsung A16 5G in top 10 (!), older iPhones persist longer, console skins strong
- **EU:** Mix — Barcelona/Inter Milan fans, broader device spread
- **JP:** Unique preferences, small volume

---

## 4. SKU Selection Analytics Workflow

### Step 1: Data Integrity Check
- [ ] Verify data freshness (paid_date range)
- [ ] Check row counts match expectations
- [ ] Verify currency distribution (any new currencies?)
- [ ] Check for nulls in key columns (design_code, device_code, net_sale)

### Step 2: Design-Level Revenue Rankings
- Group by `design_code`
- Aggregate: order_count, total_revenue_usd, unique_devices, unique_regions
- **Multi-lookback:** 1mo, 3mo, 6mo, all-time (parallel columns)
- **Momentum score:** (1mo_rank - all_time_rank) → positive = rising, negative = fading

### Step 3: Device Family Analysis
- Group by device family (not individual models)
- iPhone 16 family = IPH16 + IPH16PLUS + IPH16PRO + IPH16PMAX
- Show: family revenue, order count, top designs per family
- **Regional split:** Same family may rank differently US vs UK

### Step 4: Concentration Analysis
- Cumulative revenue % curve
- Find elbow point (marginal < 0.1% per design)
- **Per lookback window:** Elbow may shift (fewer designs dominate in shorter windows)

### Step 5: Cross-Reference Against Target Marketplace
- Apply marketplace-specific rules (e.g., Target+ = no US Sports)
- Filter catalog to eligible designs
- Re-rank within filtered set

### Step 6: Output
- Markdown report with all tables
- Save to `~/results/` with timestamp
- Include: data freshness, lookback, methodology, SQL queries used

---

## 5. Scheduled Analysis Cadence

| Report | Frequency | Agent | Trigger |
|--------|-----------|-------|---------|
| Design rankings (multi-lookback) | Weekly (Monday AM) | Atlas | Cron |
| Regional device trends | Bi-weekly | Atlas | Cron |
| New license velocity report | Weekly | Atlas | Cron |
| Data freshness check | Daily | Atlas | Heartbeat |
| Full SKU selection refresh | On-demand (before marketplace submission) | Atlas + Ava | Manual |

---

## 6. Data Quality Rules

### Always Verify
1. **No duplicate orders:** `sales_record_number` should be unique
2. **Currency coverage:** Every order must have a currency
3. **Net sale > 0:** Filter out $0 orders (samples, replacements)
4. **Status filter:** Use `status = 'Delivered'` for revenue analysis, include all for volume
5. **Refund flag:** Exclude `is_refunded = true` for net revenue

### Known Issues
- `gbp_price` and `gbp_exchange_rate` columns mostly NULL — don't rely on them
- Some dates show unusual values — filter date range sanity checks
- Walmart listings table only has 10K of 95K (pagination bug)

---

*This SOP is the reference for all sales analytics work. Atlas's MEMORY.md contains the operational details (connection strings, column mappings). This SOP contains the WHY and WHEN.*
