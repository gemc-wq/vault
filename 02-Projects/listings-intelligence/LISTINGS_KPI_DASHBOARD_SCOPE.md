# Listings US KPI Dashboard — Scope Document
**Status:** DRAFT | **Date:** 2026-04-10 | **Owner:** Athena
**Goal link:** G1 (Coverage) + G5 (Walmart Expansion)

---

## Problem

Weekly listing reports are generated but not aggregated. No week-over-week trending. No alerts on gaps. No single view that answers: "Is the catalog healthy, and what should we do about it?"

---

## Solution

A Listings KPI Dashboard that:
1. Tracks 7 KPI categories week-over-week
2. Auto-alerts on gaps and anomalies
3. Connects listing data to sales velocity (PULSE)
4. Delivers a Saturday intelligence brief to Cem via Telegram

---

## KPI Categories & Metrics

### 1. Delta Summary (Week-over-Week)

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| New listings added | Active Listings snapshot delta | <1,000 new/week (team underperforming) |
| Listings removed | Snapshot delta | >5,000 removed (suppression event?) |
| Net change | Current - Previous total | Negative for 2+ weeks |
| Price changes (>$2 movement) | Price column delta | >500 price changes (bulk error?) |

### 2. Product Type Breakdown

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| HTPCR total listings | SKU parse position [0] | N/A (baseline) |
| HB401 total listings | SKU parse position [0] | <3% of catalog (underrepresented — converts 4x) |
| HB6CR / HB7BK counts | SKU parse position [0] | New types: flag if >10K in one week |
| HLBWH total listings | SKU parse position [0] | UK > US gap flag |
| HC listings (phasing out) | SKU parse position [0] | Should be declining — alert if growing |
| FBA vs FBM split per type | fulfillment_channel | FBA < 1% on any high-volume type |

### 3. Device Coverage

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Top 50 devices by listing count | SKU parse position [1] | Device drops out of top 50 |
| HB401 device coverage % | Cross-reference HB401 SKUs vs all devices | <80% of HTPCR device coverage |
| New device appearances | Devices not in previous week | Flag new devices for review |
| Device coverage gaps | Devices with HTPCR but no HB401 | List top 20 gap devices |

### 4. Top Performers & Activity

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Top 20 new design codes (by SKU count) | SKU parse position [2] + open_date | N/A (informational) |
| Top 20 new listings by revenue potential | Cross-ref with PULSE champions | Flag if top seller designs not in new listings |
| Price change log | Price column delta | >$5 change on any single SKU |
| SKU aging distribution | open_date histogram | >50% of catalog older than 6 months |

### 5. Fulfillment Channel

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| FBA % by product type | fulfillment_channel | FBA <1% on HTPCR or HB401 |
| FBA total count | fulfillment_channel = AMAZON_NA | Week-over-week decline |
| FBM-only top sellers | Cross-ref PULSE top 100 vs FBA status | Top seller on FBM = lost Prime badge |
| Shipping template compliance | merchant_shipping_group | Any listing NOT on 'Reduced Shipping Template' (US) |

### 6. Quality Metrics

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Listings team claims vs live | Slack #eod-listings vs Active Listings delta | >20% discrepancy |
| Missing listings (claimed but not found) | Cross-reference | Any count >0 |
| Wrong fulfillment channel | Expected vs actual | Any count >0 |
| Suppressed/inactive SKUs | status column | >1,000 suppressed |
| Duplicate ASINs | asin1 groupby count >1 | Flag duplicates |

### 7. Regional Comparison

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| US total vs UK total | Both listing snapshots | Gap widens >5% in either direction |
| US-only designs (not on UK) | Design code cross-reference | Top 100 US sellers missing from UK |
| UK-only designs (not on US) | Design code cross-reference | Any count >100 (unexpected) |
| Product type distribution US vs UK | Type counts per region | HB401 penetration gap |
| DE coverage vs US/UK | DE snapshot when available | <20% of US catalog |

---

## Shipping Template Impact Report (NEW — crosses into conversion)

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Listings on wrong template | Wednesday audit | Any count >0 |
| CVR: correct template vs wrong template | Sales & Traffic by Child ASIN | >0.5% CVR difference |
| Estimated revenue loss from wrong templates | CVR gap x traffic volume x AOV | >$500/week |
| Time-to-fix from flagged to corrected | Wednesday audit vs next Saturday | >7 days unfixed |

**Requires:** Sales & Traffic by Child ASIN report (manual download from Seller Central, or SP-API automation).

---

## Data Architecture

```
DATA SOURCES                      PROCESSING                    OUTPUT
─────────────                     ──────────                    ──────

Active Listings (US)  ─┐
Active Listings (UK)  ─┤
Active Listings (DE)  ─┼──► SQLite (local_listings.db)  ──► Weekly KPI JSON
Sales & Traffic       ─┤         ↓ SKU parsing                    ↓
                       │         ↓ Delta calc                     ↓
PULSE / Supabase     ─┤         ↓ Cross-reference           KPI Dashboard
  champions data      ─┘                                    (Markdown + SQLite)
                                                                  ↓
Slack #eod-listings  ──► Digest script ──► Quality cross-ref      ↓
                                                                  ↓
                                                        ┌─────────┴──────────┐
                                                        │                    │
                                                   Telegram Brief    Vault Report
                                                   (Saturday AM)    (weekly archive)
```

### Storage

| Layer | What | Where |
|-------|------|-------|
| Raw snapshots | Active Listings TSV files | ~/Downloads/ (temporary) |
| Parsed data | SQLite tables (current/previous per region) | data/local_listings.db |
| Weekly KPIs | JSON per week | data/compiled/listings/YYYY-Wxx_kpis.json |
| Dashboard state | SQLite (week-over-week trends) | data/listings_dashboard.db |
| Reports | Markdown | Vault/02-Projects/listings-intelligence/weekly/ |
| Alerts | Telegram voice + text | Cem's Telegram |

---

## Presentation Layer

### Saturday Morning Brief (Telegram Voice)

Delivered after listing crons complete (~4 AM ET). Format:

```
📊 Weekly Listings Intelligence — Week of [DATE]

CATALOG HEALTH: [GREEN/AMBER/RED]
• US: X.XXM listings (+/-XX,XXX this week)
• UK: X.XXM listings (+/-XX,XXX this week)
• Net new: XX,XXX across all regions

TOP 3 ACTIONS (ranked by revenue impact):
1. [Action] — estimated $X,XXX/month impact
2. [Action] — estimated $X,XXX/month impact
3. [Action] — estimated $X,XXX/month impact

ALERTS:
• [Any threshold breaches from KPI categories above]

Full report saved to vault.
```

### Weekly Markdown Report (Vault Archive)

Full 7-section report following existing SOP template, plus:
- Week-over-week trend arrows for every metric
- 4-week rolling average for key metrics
- Action tracker: last week's recommendations + outcomes

---

## Build Phases

### Phase 1: Fix & Collect (This Week)
- [ ] Fix Google API key on pixel agent (listing crons broken)
- [ ] Increase PULSE leaderboard timeout
- [ ] Verify listing crons run successfully this Saturday
- [ ] Confirm data lands in local_listings.db correctly

### Phase 2: KPI Engine (Week 2)
- [ ] Build KPI extraction script (reads SQLite, computes all 7 categories)
- [ ] Output weekly KPI JSON to data/compiled/listings/
- [ ] Build week-over-week comparison logic
- [ ] Implement alert thresholds (flag/alarm system)
- [ ] Cross-reference with PULSE/Supabase champions data

### Phase 3: Dashboard & Delivery (Week 3)
- [ ] Build listings_dashboard.db (trending SQLite store)
- [ ] Saturday Telegram voice brief (same pattern as daily briefing)
- [ ] Markdown report auto-saved to vault
- [ ] Action tracker: log recommendations, show follow-up next week

### Phase 4: Automation & Shipping Impact (Week 4)
- [ ] SP-API integration for automated Active Listings download (Jay Mark)
- [ ] Shipping template impact report (needs Sales & Traffic data)
- [ ] Conversion cross-reference (correct vs wrong template CVR)
- [ ] Remove manual download dependency entirely

---

## Success Criteria

| Metric | Current State | Target (Week 4) |
|--------|--------------|-----------------|
| Manual downloads required | Every Saturday | Zero (SP-API automated) |
| Time from data to Cem's phone | Hours (if at all) | <1 hour after cron completes |
| Actionable recommendations per week | 0 | 3-5, ranked by revenue impact |
| Weeks of trending data | 0 | 4+ weeks rolling |
| Cross-region gap identification | Manual/ad-hoc | Automated, every Saturday |
| Shipping template revenue impact | Unknown | Quantified weekly |

---

## Dependencies

| Dependency | Owner | Status | Blocker? |
|------------|-------|--------|----------|
| Google API key for pixel agent | Athena | Broken | YES — blocks Phase 1 |
| Active Listings manual download | Cem | Weekly chore | Blocks until Phase 4 |
| Sales & Traffic report | Cem | Not started | Blocks Shipping Impact |
| SP-API access on Zero 2 | Jay Mark | Available | Needs scoping for Phase 4 |
| Supabase PULSE data | Jay Mark | Active | Working |
| Slack bot token | Configured | Active | No |

---

## DelegAIt Opportunity

This dashboard pattern is highly generalizable:
- **Any e-commerce brand** needs listings health monitoring
- **Multi-marketplace sellers** need cross-region gap detection
- **Data-to-action pipeline** (collect → analyze → alert → recommend) is a SaaS feature
- Potential DelegAIt module: "Marketplace Intelligence Dashboard"

---

*DRAFT — Awaiting Cem approval to proceed with Phase 1.*
