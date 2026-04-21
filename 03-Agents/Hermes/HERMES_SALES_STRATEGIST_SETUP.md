# Hermes — Sales Analytics & Strategist Setup
**Date:** 2026-04-01  
**Context:** Role transition from Operations Librarian to Sales Analytics & Strategist  
**Status:** Active  

---

## Core Purpose

**Revenue Accelerator**, not just a data reporter. Turn raw sales data into actionable strategies that drive growth across all channels, with Amazon as the primary engine.

---

## Data Access Configuration

| Data Source | Location | Access Method | Status |
|-------------|----------|---------------|--------|
| **BigQuery** | Cloud | Direct API | ✅ Available |
| **Amazon Business Reports** | Mac Studio local (`~/Downloads/` or similar) | Weekly downloads by Cem | ⚠️ Manual process |
| **Amazon Advertising Reports** | Mac Studio local | Weekly downloads by Cem | 🔄 API being built |
| **Supabase** | Cloud | Direct API | ✅ Available |
| **Shopify** | Cloud | Admin API | ✅ Available |

---

## Amazon Advertising Reports Needed

**Priority Order:**

1. **Campaign Report** — Spend, sales, ACOS, ROAS by campaign
2. **Search Term Report** — Which queries triggered ads (critical for negate candidates)
3. **Placement Report** — Top of Search vs Product Page vs Rest (bid multiplier optimization)
4. **Advertised Product Report** — Per-ASIN performance
5. **Purchased Product Report** — What people actually bought (halo effect validation)
6. **Dayparting Report** — Hourly performance (peak conversion windows)

**Current Process:** Cem downloads weekly → saves to Mac Studio → Hermes analyzes
**Future Process:** SP-API integration for automated pulls (in development)

---

## Regional Sales Trends — Critical Context

### Soccer/Football Licensing

| Team/Market | Strong Region | Context |
|-------------|---------------|---------|
| **Barcelona** | USA | Brand recognition transcends local league; big domestic seller |
| **Real Madrid** | USA | Brand recognition transcends local league; big domestic seller |
| **Premier League** (Liverpool, Arsenal, Man City, Chelsea) | UK | Home market dominance; natural affinity |
| **La Liga (non-Barca/Real)** | Spain/LATAM | Regional strength |

**Key Insight:** Don't assume global popularity = regional sales. Barcelona/Real Madrid have US brand power that other European clubs lack despite being "bigger" globally.

**Implication for PULSE:**
- Weight Barcelona/Real designs higher for US gap analysis
- Weight Premier League designs higher for UK gap analysis
- Cross-reference license urgency with regional strength

### Other Regional Considerations to Analyze

- **NFL** — Primarily USA; limited UK appeal?
- **NBA** — Growing globally; strong US/China
- **Anime** (Naruto, Dragon Ball) — Universal appeal; check LATAM specifically
- **WWE** — US-centric but international growth
- **NHL** — Canada/USA northern markets

---

## Five Key Focus Areas

### 1. PULSE Intelligence

**Weekly Velocity Analysis:**
- Baseline: 6-month historical run rate
- Velocity: 1-2 month current performance
- Signal = velocity_revenue ÷ baseline_monthly_avg

**Six Action Types:**
| Action | Definition | Routes To |
|--------|-----------|-----------|
| **LIST IT** | SKU exists internally, not live on target marketplace | Marketplace ops |
| **COMPLETE IT** | Missing device-family variants | Marketplace ops |
| **BUILD IT** | New design × form factor justified by demand | Design/merch team |
| **FIX IT** | High sessions + low conversion = listing problem | Content/CRO team |
| **BOOST IT** | High conversion + low sessions = needs visibility | Advertising team |
| **RETIRE IT** | Velocity <0.3x for 90+ days | Catalog ops |

**License Obligation Layer:**
Track gap ratio = (MG_remaining / months_remaining) ÷ (current_annualized_pace / 12)
- >1.5 → 🔴 BEHIND — boost ALL designs under this license
- 0.8–1.5 → ⚠️ WATCH — slight scoring boost
- <0.8 → ✅ AHEAD — normal scoring

**Current Alerts:**
- NBA: $200K MG, $13K revenue — critical gap
- NFL: Expired March 31 — renewal decision needed
- Shelby: $27.5K MG, $1.5K revenue — behind pace

### 2. Conversion Optimization

**Current Baselines (March 2026):**
- US Overall: 2.89% (vs category avg 1.5%) ✅
- HTPCR (Soft Gel): 2.96%
- HB401 (Hard Case): 11.81% — **4x higher than HTPCR**
- HB6/HB7 MagSafe: 6-8% — exceptional but low volume
- Desk Mats: 3.16%
- Leather Wallets: 1.88% — underperforming

**Quadrant Strategy:**
| Quadrant | Definition | Action |
|----------|-----------|--------|
| **STARS** | High sessions + High conversion | Test price increase ($19.95 → $21.95) |
| **QUESTION MARKS** | High sessions + Low conversion | Price decrease OR fix listing quality |
| **CASH COWS** | Low sessions + High conversion | Increase PPC budget |
| **DOGS** | Low sessions + Low conversion | Deprioritize |

### 3. Amazon Advertising Strategy

**Current Performance (March 23 PPC AutoResearch):**
- 30d Blended ROAS: 5.74x (industry avg: 3.3x) ✅
- 30d ACOS: 17.42% (industry avg: 30%) ✅
- CPC: $0.18 (industry avg: $1.18) ✅
- Halo Effect: True ROAS ~4.7x campaign reports
- Portfolio: 1 Star, 8 Cash Cows, 35 Question Marks, 26 Dogs

**Immediate Actions:**
1. Negate waste terms ("cody rhodes" $13.52, "roman reigns" $12.16)
2. Pause Dogs under 1.5x ROAS ($1,256 spend → cut 50%)
3. Increase Star budgets 20-30%
4. Add "snoopy" as UK campaign negative (£18.98 wasted)

### 4. Microsite & DTC Strategy

**GoHeadCase Target:** 10x own-site units (2,609 → 26,000/year)

**Current Status:**
- 76% Amazon dependency — critical risk
- Shopify store live (limited products)
- 1,803 HB401 gaps have EANs and ready for bulk upload

**Hero Product Priority (by momentum):**
1. Peanuts ($273K/90d)
2. Harry Potter ($244K/90d)
3. Liverpool FC ($189K/90d) — UK focus
4. Arsenal ($161K/90d) — UK focus
5. Naruto ($127K/90d)

### 5. Cross-Channel Gap Analysis

**Walmart Gap:**
- 120/200 top champions already listed
- 80 genuine gaps remain
- Value: ~$381K/90d

**Target+:**
- Growing via Shopify (29 orders/4 days discovered March 23)

**eBay:**
- UK focus needed
- Check Premier League product-market fit

---

## Key Metrics Dashboard

| Metric | Current | Target | Frequency |
|--------|---------|--------|-----------|
| US Overall Conversion | 2.89% | >3.0% | Weekly |
| HB401 Conversion | 11.81% | Maintain >10% | Weekly |
| Blended ROAS | 5.74x | >6.0x | Bi-weekly |
| Coverage (Top 200) | 40% Walmart | 80% | Monthly |
| DTC Units/Year | 2,609 | 26,000 | Quarterly |
| License Gap Ratio (NBA) | Critical | <1.5 | Monthly |

---

## Deliverables Schedule

| Frequency | Deliverable | Contents |
|-----------|-------------|----------|
| **Weekly** | PULSE Alert | Velocity signals, 6 action types, license urgencies |
| **Bi-weekly** | PPC Performance Review | ROAS/ACOS by campaign, reallocation recommendations |
| **Monthly** | Cross-Channel Coverage Report | Traffic light dashboard, gap prioritization, regional trends |
| **Quarterly** | License Health Check | MG obligation status, renewal recommendations, regional analysis |

---

## Regional Trend Analysis — To Be Built

**Data Sources Needed:**
- Amazon Business Reports by marketplace (US/UK/DE/FR/IT/ES)
- Google Trends for brand search volume by region
- Social listening (Apify) for geo-tagged mentions

**Hypotheses to Test:**
- Barcelona/Real Madrid have higher US search volume than UK
- Premier League clubs have near-zero US organic search
- Anime brands have LATAM strength not captured in current data
- NFL has limited UK appeal (verify with sales data)

---

## Next Actions

1. **Immediate:** Analyze weekly Amazon Business Report + Advertising Reports when provided
2. **This Week:** Deep-dive on NBA license ($200K MG shortfall) — which designs are live vs potential
3. **This Month:** Build regional sales correlation (soccer teams by country) from BigQuery
4. **Ongoing:** PPC audit — identify top 10 negate candidates from Search Term Report

---

## Notes

- API for Amazon advertising in development; manual reports for now
- Regional trends are critical for gap prioritization — don't treat all markets equally
- Barcelona/Real Madrid insight came from Cem directly — operational knowledge not in data yet
- Save observations like this to improve PULSE scoring algorithms

---

*Last updated: 2026-04-01 by Hermes*  
*Status: Active role configuration*