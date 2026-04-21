# PROJECT BRIEF: Weekly Amazon Data Analysis & AI-Driven Advertising Management

**Owner:** Ava (Strategy Lead) | **Operator:** Hermes (Sales Strategist) | **Version:** 1.0 | **Date:** 2026-04-10

---

## Executive Summary

Ecell Global spends **$5,000+ per month** on Amazon advertising across 1,000+ active campaigns. Current approach is reactive: download reports weekly, analyze in isolation, optimize manually. 

**Opportunity:** Build an integrated **AI-driven advertising management system** that:
1. Automates weekly reporting + analysis (6 data pipelines)
2. Identifies optimization opportunities in real-time
3. Makes autonomous recommendations (negate terms, realloc budget, pause underperformers)
4. Manages campaign lifecycle (creation, optimization, scaling, retirement)
5. Ties advertising ROI back to inventory/product planning (PULSE)

**Expected Impact:** 
- Reduce manual work: 40 hrs/month → 4 hrs/month (90% automation)
- Improve ROAS: Current 5.74x → Target 6.5x+ (via AI optimization)
- Reduce ACOS: Current 17.42% → Target <15% (better term management)
- Accelerate license obligation catch-up (NBA: -$200K gap, NFL: renewal decision)

---

## Current State (Baseline — March 2026)

### Amazon Advertising Performance
- **Monthly Spend:** $5,000+
- **Blended ROAS:** 5.74x (industry avg: 3.3x) ✅ **Excellent baseline**
- **ACOS:** 17.42% (industry avg: 30%) ✅ **Well-optimized**
- **CPC:** $0.18 (industry avg: $1.18) ✅ **Highly competitive**
- **Halo Effect:** True ROAS ~4.7x (accounting for organic sales lift)

### Campaign Portfolio
- **1** Star campaign (>10x ROAS)
- **8** Cash Cows (3-10x ROAS, high volume)
- **35** Question Marks (1-3x ROAS, needs optimization)
- **26** Dogs (<1x ROAS, should pause)

### Conversion Performance
- **Overall US:** 2.89% (vs category avg 1.5%) ✅
- **HB401 cases:** 11.81% (4x higher than HTPCR) ⭐ **Hero product type**
- **HB6/HB7 MagSafe:** 6-8% (exceptional, low volume)
- **Desk Mats:** 3.16%
- **Leather Wallets:** 1.88% (underperforming)

### Data Infrastructure
- ✅ BigQuery: Sales data (nightly sync)
- ✅ Supabase: Orders + inventory
- ✅ Amazon Business Reports: Manual weekly downloads (Mac Studio)
- ❌ Amazon Advertising Reports: Manual downloads (5.6K file project exists, not automated)
- ❌ Amazon SP-API for ads: In development (not yet available)

### Manual Workflow (Current Friction)
1. **Friday 5 PM:** Cem downloads 6 Amazon reports manually → Mac Studio
2. **Saturday morning:** Hermes analyzes, creates spreadsheets
3. **Saturday afternoon:** Recommendations emailed (no automation)
4. **Sunday-Friday:** Manual campaign updates (Seller Central UI)
5. **Result:** 40 hrs/month, laggy insights, reactive decisions

---

## Weekly Data Analysis Pipeline (Current Schedule)

### Automated Cron Tasks (Saturday Mornings)

| Time | Task | Agent | Data Source | Output | Status |
|------|------|-------|-------------|--------|--------|
| 1:00 AM | Listings US Analysis | Gemini Flash | Amazon Active Listings | Delta report (new/removed) | ✅ SCHEDULED |
| 2:00 AM | Listings UK Analysis | Gemini Flash | Amazon UK Active Listings | Regional comparison | ✅ SCHEDULED |
| 3:00 AM | Listings DE + Movers | Gemini Flash | Amazon DE Active Listings | Top movers by product type | ✅ SCHEDULED |
| 5:00 AM | PULSE Leaderboard | Gemini Flash | BigQuery (sales velocity) | Weekly sales ranking + alerts | ✅ SCHEDULED |
| 6:00 AM | Amazon Reports API | Cloud Run | Amazon SP-API | Download Business + Child ASIN reports | ⏳ PENDING TEST |
| 7:00 AM | Amazon Ads Analysis | Hermes (Kimi K2.5) | Amazon Advertising Reports | ROAS/ACOS by campaign, negate candidates | ❌ NOT YET AUTOMATED |

### Weekly Manual Downloads (Needed Saturday Morning)

**Cem downloads to `~/Downloads/` → Ava/Hermes pick up Saturday:**

1. **Child ASIN Report (14-day)** — Sales per ASIN variant
2. **Child ASIN Report (30-day)** — 30-day trend
3. **Business Report (14-day & 30-day)** — Overall traffic + conversion
4. **Campaign Report** — Spend, sales, ACOS, ROAS by campaign
5. **Search Term Report** — Keywords triggering ads (negate candidates)
6. **Placement Report** — Top of Search vs Product Page performance
7. **Advertised Product Report** — Per-ASIN ad metrics
8. **Purchased Product Report** — Post-click purchase halo

---

## Weekly Report Analysis Framework & Optimization Actions

**This section defines HOW we extract intelligence from each report and WHAT actions we take to optimize sales.**

---

### 1. CHILD ASIN REPORT (14-day & 30-day)

**What It Shows:**
- Sales volume per ASIN (variant)
- Conversion rate per variant
- Revenue per variant
- Device family performance

**Key Metrics to Extract:**
- **Top 20 ASINs** — which variants are selling best?
- **Velocity trend** — 30-day vs 14-day (accelerating or declining?)
- **Variant mix** — which device sizes dominate per design?
- **Conversion outliers** — which variants convert 2x better than average?

**Gap Analysis:**
- Compare SKUs live on Amazon vs our inventory
- Identify designs with **high ASIN volume but missing variants**
- Identify **low-velocity ASINs** that should be retired

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Variant missing but high velocity | Create listing | Marketplace Ops | 1 week |
| Variant converting 2x better | Increase ad spend | Hermes | Immediate |
| Variant declining <0.5x baseline | Pause ads, audit | Ava + CRO | 3 days |
| ASIN >90 days zero sales | Retire | Catalog Ops | 2 weeks |

---

### 2. BUSINESS REPORT (14-day & 30-day)

**What It Shows:**
- Total sessions, units sold, conversion rate, revenue
- Ad impressions + clicks
- Blended metrics (organic + paid)

**Key Metrics to Extract:**
- **Overall conversion % (14d vs 30d)** — trending up or down?
- **Traffic per unit** — session efficiency
- **Traffic source mix** — organic vs paid

**Gap Analysis:**
- Identify **traffic spikes without sales** (low conversion)
- Identify **low-traffic, high-conversion** designs (need ads)

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Conversion ↓ >0.2% | Audit listing quality | Ava + CRO | 1 week |
| Conversion ↑ >0.2% | Increase ad budget | Hermes | Immediate |
| Traffic spike no sales | Check competitor pricing | Hermes | 1 day |
| Low traffic + high conversion | Increase ad spend | Hermes | 2 days |
| High traffic + low conversion | Fix listing/price | CRO | 1 week |

---

### 3. CAMPAIGN REPORT

**What It Shows:**
- Spend, sales, ACOS, ROAS, units per campaign

**Key Metrics to Extract:**
- **Campaign ROAS ranking** — which 10 are most profitable?
- **ACOS outliers** — best (<10%), worst (>50%)
- **Portfolio composition** — Stars/Cows/Marks/Dogs

**Gap Analysis:**
- **Dogs** (ROAS <1.5x) — pause or cut
- **Question Marks** (ROAS 1-3x) — optimize
- **Cash Cows** (ROAS 3-10x) — maintain
- **Stars** (ROAS >10x) — scale

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Star (ROAS >10x) | Increase budget 20-30% | Hermes | Immediate |
| Cow (ROAS 3-10x) | Maintain + monitor | Hermes | Weekly |
| Mark (ROAS 1-3x) | Optimize targeting | Hermes | 3 days |
| Dog (ROAS <1.5x) | Pause or cut 50% | Hermes | 2 days |

---

### 4. SEARCH TERM REPORT ⭐ **CRITICAL FOR REVENUE OPTIMIZATION**

**What It Shows:**
- Keywords triggering ads
- Impressions, clicks, spend, sales, ACOS per term

**Key Metrics to Extract:**
- **Profitable terms** (ACOS <20%, high volume)
- **Waste terms** (ACOS >50%)
- **High impression, zero click** (irrelevant)
- **High impression, low conversion** (mismatch)

**Gap Analysis:**
- **Negate candidates** — top 10 waste terms
- **Bid optimization targets** — profitable but underbidding
- **New opportunities** — competitors bidding, we're not

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| ACOS >50% | Add to negatives | Hermes (auto) | Same day |
| High imp, zero clicks | Check bid + relevance | Hermes | 3 days |
| High imp, low conv | Audit landing page | CRO | 1 week |
| ACOS <20%, high vol | Increase bid 10-20% | Hermes | Immediate |
| Competitor bidding | Create campaign | Hermes | 1 week |

**Expected Impact:**
- Remove $300-500 waste/month
- Improve ROAS: 5.74x → 6.2x+

---

### 5. PLACEMENT REPORT

**What It Shows:**
- Performance by placement: Top of Search, Product Page, Rest
- Spend, sales, ROAS, ACOS per placement

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Top of Search ROAS >8x | Increase bid +20% | Hermes | Immediate |
| Product Page ROAS <2x | Reduce bid | Hermes | 1 week |
| Imbalanced (90% ToS) | Balance budget | Hermes | 1 week |

---

### 6. ADVERTISED PRODUCT REPORT (Per-ASIN)

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| High spend + ROAS <1.5x | Pause ads | Marketplace Ops | 2 days |
| High conversion (>5%) | Increase spend 30% | Hermes | Immediate |
| Zero clicks on high imp | Review targeting | Hermes | 3 days |

---

### 7. PURCHASED PRODUCT REPORT (Halo Effect)

**Key Insight:**
- True ROAS (4.7x) < Reported ROAS (5.74x)
- Halo multiplier: 0.82x

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| 1.5x+ halo multiplier | Feature in bundles | Merchandising | 2 weeks |
| High halo + low traffic | Increase ad spend | Hermes | Immediate |

---

### 8. DAYPARTING REPORT (Hourly)

**Optimization Actions:**
| Finding | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Peak hour ROAS >1.5x avg | Increase bid multiplier | Hermes | Immediate |
| Low hour ROAS <0.7x avg | Decrease bid | Hermes | 1 week |

---

## Weekly Reporting Scorecard

**Every Saturday (8 AM), generate:**

```
WEEKLY AMAZON DASHBOARD — Week of [DATE]

📊 HEALTH METRICS
├─ Conversion: [%] vs baseline ✅/⚠️/❌
├─ ROAS: [x] vs target 6.5x+ ✅/⚠️/❌
├─ ACOS: [%] vs target <15% ✅/⚠️/❌
├─ Shipping Compliance: [%] vs target 100% ✅/⚠️/❌
└─ FBA Penetration: [%] vs target 80% ✅/⚠️/❌

📈 ACTION ITEMS (This Week)
├─ Negate waste terms: [X] (ACOS >50%)
├─ Budget reallocation: Dogs → Stars ($[amt])
├─ Fix listings: [X] products
├─ Pause underperformers: [X] campaigns
└─ Expand FBA: [X] designs

🎯 OPPORTUNITIES (Next Week)
├─ Top search term: [term]
├─ Placement bid increase: [placement]
├─ High-halo design: [design]
└─ License fast-track: [design]

📋 ESCALATIONS
├─ [Issue] → Owner → Timeline
```

---

## Related Tasks & Blockers

### Task 1: FBA Conversion Optimization ⭐ **HIGH PRIORITY**

**Current State:**
- HB401 (Hard Case, FBA-friendly): 11.81% conversion — **4x higher than HTPCR**
- HTPCR (Soft Gel, FBM-only): 2.96% conversion
- HB6/HB7 MagSafe (FBA): 6-8% conversion

**Insight:** FBA drives higher conversion (2-day delivery visible in search results). HTPCR underperformance likely due to FBM's longer delivery times.

**Actions Needed:**
1. **Analyze FBA penetration** — Which top 50 designs are FBA vs FBM?
2. **Identify FBA expansion targets** — Designs with high volume but FBM-only
3. **Model revenue impact** — Migrate HTPCR HTPCR to HB401 where possible (HB401 is $1.99 higher price point)
4. **Shipping template audit** — Ensure all Amazon listings have "Reduced Shipping Template" (currently missing on increasing %)

**Owner:** Hermes (analysis) + Harry (inventory planning)
**Data:** BigQuery (sales by product type), Supabase (current FBA inventory), Amazon reports
**Next Step:** Codex to query "which top 100 designs are FBA vs FBM"

### Task 2: Inventory Restock Planning ✅ **IN PROGRESS**

**Current Tools:**
- **FBA Planner** (Streamlit on Cloud Run) — Inventory analysis + restock recommendations
- **Zero system** — Historical demand patterns

**Data Needed:**
- Amazon FBA inventory (real-time from SP-API `GET /fba/inventory/v1/summaries`)
- Historical velocity (90-day run rate per SKU)
- Lead times (Veeqo)
- Vendor costs (cost sheet)

**Current Process:** Manual CSV uploads (not API-driven)

**Blockers:**
- Amazon SP-API FBA Inventory endpoint needs wiring (Drew to provide AWS creds)
- Veeqo carrier lead time data incomplete

**Owner:** Harry (FBA Planner) | **Status:** 60% complete, waiting for SP-API creds

### Task 3: Shipping Template Compliance 🚨 **CRITICAL**

**Issue (Apr 10):** Increasing Amazon listings missing "Reduced Shipping Template" → default template shows long delivery → lower conversion.

**Impact:** 
- Items with Reduced Shipping → 2-day delivery visible → higher conversion
- Items with default template → 5-7 day delivery → lower conversion
- Correlation: Proven in conversion dashboard (HB401 with FBA = higher)

**What's Needed:**
1. **Audit:** How many of our 3.43M Amazon listings are missing Reduced Shipping?
2. **Edit capability:** Can SP-API `PutListingsItem` endpoint modify shipping template?
3. **Bulk update:** Automate template assignment once capability confirmed

**Cron Status:** "Shipping Template Audit" runs Wed 2 AM (only verifies correctness, not compliance %)

**Owner:** Ava (strategy) + Codex (analysis) | **Status:** Analysis queued for tonight
**Next Step:** Confirm Cloud Run can EDIT listings via SP-API

### Task 4: Amazon Ads AI Management 🤖 **NEW - STRATEGIC**

**Current State:**
- Manual campaign creation (Seller Central UI)
- Manual budget allocation (spreadsheets)
- Manual negate term management (keyword by keyword)
- No automated rule-based optimization

**Opportunity:**
- **AI campaign creation:** Based on PULSE velocity signals, auto-create campaigns for high-demand designs
- **AI budget allocation:** Based on ROAS targets, auto-adjust spend across portfolios
- **AI negate management:** Search term report → identify waste terms → auto-add to negative lists
- **AI bid optimization:** Dayparting analysis → adjust bids by time of day

**Key Reports Needed (6 types):**

1. **Campaign Report**
   - Metric: Spend, sales, ACOS (%), ROAS (x), units sold
   - Grouped by: Campaign portfolio (Star / Cash Cow / Question Mark / Dog)
   - Action: Budget reallocation (cut Dogs, increase Stars)

2. **Search Term Report** ⭐ **CRITICAL FOR AI**
   - Metric: Query, impressions, clicks, spend, sales, ACOS
   - Filter: ACOS >50% (waste candidates)
   - Action: Auto-generate negate term list

3. **Placement Report**
   - Metric: Top of Search vs Product Page vs Rest (spend, ROAS, ACoS)
   - Action: Bid multiplier optimization (Top of Search premium)

4. **Advertised Product Report** (ASINs)
   - Metric: Per-ASIN spend, sales, conversion, ROAS
   - Filter: High spend + low ROAS (underperformers)
   - Action: Pause or revise targeting

5. **Purchased Product Report** (Halo Effect)
   - Metric: Did buyers purchase non-advertised items?
   - Action: Validate true ROAS (currently 4.7x vs reported 5.74x)
   - Use case: Identify designs with high halo value

6. **Dayparting Report**
   - Metric: Hourly performance (impressions, clicks, ROAS)
   - Action: Bid by hour (peak conversion windows)

---

## Key Metrics & Targets

| Metric | Current | Target | Frequency |
|--------|---------|--------|-----------|
| **Blended ROAS** | 5.74x | 6.5x+ | Weekly |
| **ACOS** | 17.42% | <15% | Weekly |
| **Campaign Quality** | 1 Star, 35 Question Marks | 3 Stars, 20 Question Marks | Monthly |
| **Shipping Template Compliance** | Unknown | 100% | Weekly (new metric) |
| **FBA Coverage (Top 50 designs)** | Unknown | 80%+ | Monthly (new metric) |
| **License Gap Ratio (NBA)** | Critical (-$200K) | <1.5x | Monthly |
| **NFL Renewal Status** | Expired Mar 31 | Decision needed | ASAP |

---

## Architecture: From Manual to AI-Driven

### Phase 1 (Current — Apr 10)
```
Amazon Seller Central
    ↓ (manual download, Cem)
Mac Studio ~/Downloads/
    ↓ (manual analysis)
Hermes (spreadsheet)
    ↓ (manual campaign edits)
Amazon Seller Central
```
**Time Cost:** 40 hrs/month

### Phase 2 (Proposed — Apr 30)
```
Amazon SP-API (automated via Cloud Run)
    ↓ (cron: Sat 6 AM)
BigQuery / Supabase (auto-ingest)
    ↓ (cron: Sat 7 AM)
Hermes (AI analysis + recommendations)
    ↓ (cron: Sat 8 AM)
Recommendation Engine (rule-based)
    ↓ (awaiting approval)
Amazon SP-API (auto-execute)
```
**Time Cost:** 4 hrs/month (review + exceptions only)

### Phase 3 (Future — May 30)
```
Real-time monitoring (continuous)
    ↓
AI anomaly detection (ACOS spike? ROAS drop?)
    ↓
Auto-pause underperformers
    ↓
Auto-reallocate budget
    ↓
Slack alerts (no action required unless exception)
```
**Time Cost:** 1 hr/week (exception handling)

---

## Implementation Roadmap

### Milestone 1: Data Automation (Apr 10-20)
- [ ] Test Amazon Reports API on Cloud Run (Codex investigation)
- [ ] Confirm SP-API can pull all 6 report types
- [ ] Wire Cloud Run → BigQuery pipeline (Sat 6 AM cron)
- [ ] Test report format matches manual downloads
- [ ] Decommission manual downloads (Cem no longer needed)

**Owner:** Cem (decision) + Codex (implementation) | **Blocker:** SP-API scope permissions

### Milestone 2: Analysis Automation (Apr 21-30)
- [ ] Build Hermes analysis cron (Sat 7 AM)
  - Search term analysis (negate candidates)
  - Campaign portfolio scoring (Star/Cow/Mark/Dog)
  - ROAS/ACOS by product type
  - Shipping template compliance scan
  - FBA penetration analysis
  
- [ ] Create recommendation engine
  - Budget reallocation logic
  - Pause/scale/bid rules
  - Negate term auto-generation

- [ ] Wire output to dashboard + Slack alerts

**Owner:** Hermes (analysis) + Harry (dashboard) | **Blocker:** None if data automation complete

### Milestone 3: Autonomous Execution (May 1-31)
- [ ] Amazon SP-API `PutListingsItem` capability (shipping template edit)
- [ ] Budget allocation rules (SafetyGuard: no single campaign >20% reallocated/week)
- [ ] Negate term auto-implementation (with human approval queue)
- [ ] Bid optimization engine (dayparting analysis)

- [ ] Approval workflow
  - Auto-execute low-risk changes (negate terms, small reallocations)
  - Human approval for large budget moves (>$100/campaign)

**Owner:** Harry (implementation) + Ava (governance) | **Blocker:** SP-API edit permissions

### Milestone 4: Real-Time Intelligence (Jun 1+)
- [ ] 24/7 monitoring (not weekly)
- [ ] Auto-anomaly detection (ROAS drops >10%, ACOS spikes >5%)
- [ ] Continuous budget optimization
- [ ] Predictive bidding (ML model trained on historical dayparting)

**Owner:** TBD (requires data scientist or advanced ML) | **Blocker:** Model training data (3-6 months)

---

## Strategy & Key Actions

### Immediate Actions (This Week)

**1. Shipping Template Audit** (Critical Path)
- Codex: Query "how many listings missing Reduced Shipping Template"
- Codex: Check if SP-API can EDIT template assignment
- Ava: Document findings + blockers
- **Deliverable:** Compliance audit + edit capability status (by Apr 12)

**2. Cloud Run API Investigation** (Critical Path)
- Codex: Inspect Cloud Run `ecell-dashboard` service
- Codex: List all SP-API endpoints currently available
- Codex: Test Amazon reports API (can it pull Search Term Report?)
- **Deliverable:** SP-API capability matrix (by Apr 12)

**3. FBA Expansion Analysis**
- Codex: Query "top 50 designs by revenue — how many are FBA vs FBM?"
- Hermes: Model revenue lift if moved to HB401 (FBA)
- **Deliverable:** FBA expansion opportunity list (by Apr 13)

### Short-Term Strategy (Apr 11-30)

**1. Wire Data Automation (Phase 1 → Phase 2)**
- Test Amazon Reports API on Cloud Run
- Confirm all 6 report types available
- Build Sat 6 AM cron for auto-download
- **Goal:** Stop manual downloads by Apr 20

**2. Launch Weekly Analysis Cron**
- Hermes analysis job: Sat 7 AM
- Outputs: Campaign portfolio, negate candidates, ROAS by product type, shipping audit
- Delivery: Slack #ai + email to Cem
- **Goal:** Fully automated reporting by Apr 25

**3. Build Recommendation Engine**
- Rules: Budget cuts for Dogs (<1.5x ROAS), reallocations to Stars
- Rules: Auto-generate negate term list from Search Term Report
- Rules: Flag shipping template gaps for bulk edit
- **Goal:** Enable autonomous recommendations by Apr 30

### Medium-Term Strategy (May 1-31)

**1. Autonomous Campaign Execution**
- Implement safe budget reallocation (phase-in: $100/campaign/week)
- Auto-add negate terms (with approval queue for first 100)
- Auto-modify shipping templates (once SP-API edit confirmed)
- **Goal:** Reduce manual campaign edits 90% by May 31

**2. FBA Expansion Campaign**
- Create campaigns for top 20 designs in HB401 (FBA)
- Allocate initial budget ($500/campaign) from Dogs pool
- Monitor for conversion lift
- **Goal:** Increase FBA penetration in top 50 from current to 80%

**3. License Obligation Fast-Track**
- NBA: Fast-track high-velocity designs ($200K gap priority)
- NFL: Decision on renewal (expired Mar 31, sell-off window ends Jun 29)
- **Goal:** Close NBA gap to <$150K shortfall by May 31

---

## Success Criteria

### Data Quality (Phase 1)
- [ ] All 6 report types flowing to BigQuery weekly
- [ ] Report format identical to manual download baseline
- [ ] Zero failed cron jobs for 4 consecutive weeks
- [ ] Data latency <2 hours from Amazon API to dashboard

### Analysis Quality (Phase 2)
- [ ] Recommendations validated (Search Term negate terms confirmed waste)
- [ ] ROAS/ACOS change month-over-month tracked
- [ ] All 4 quadrants (Star/Cow/Mark/Dog) identified with 90% confidence
- [ ] Shipping template compliance audit automated + accurate

### Business Impact (Phase 3)
- [ ] ROAS improvement: 5.74x → 6.5x+ (month-over-month)
- [ ] ACOS reduction: 17.42% → <15%
- [ ] Manual work: 40 hrs/mo → <4 hrs/mo
- [ ] Campaign quality: 35 Question Marks → 20 (better focused portfolio)

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **SP-API scope missing** | Can't edit listings or pull all reports | Verify permissions with Cem + Drew before Phase 2 |
| **Data format mismatch** | Analysis breaks if API format differs from manual | Test with real data before decommission manual process |
| **Campaign execution failure** | Auto-pause kills live campaigns | Implement SafetyGuard: max 10% reallocated/week, require approval >$100 |
| **Report delay** | Hermes analysis waiting for data | Set SLA: reports delivered by 8 AM Sat; alert if delayed past 7:30 AM |
| **License gap widening** | NFL expires, NBA renewal pressure | Prioritize fast-track high-velocity designs; decide NFL renewal by May 1 |

---

## Resource Requirements

| Role | Time/Week | Status | Notes |
|------|-----------|--------|-------|
| **Cem** | 2 hrs | Make decisions (SP-API scopes, automation approval) | |
| **Ava** | 4 hrs | Oversee, approve rule changes, risk management | |
| **Hermes** | 3 hrs | Analysis setup, rule validation | Reduced from 10 hrs when automated |
| **Codex** | 8 hrs | Implementation (API, crons, dashboards) | Temporary; mainly setup work |
| **Harry** | 2 hrs | Infrastructure (Cloud Run, BigQuery) | Occasional tweaks |

**Total Team Effort:** ~19 hrs/week (setup) → 4 hrs/week (steady-state maintenance)

---

## Deliverables

### Phase 1 Deliverable (Apr 20)
- [ ] Amazon Reports API validation report (Codex)
- [ ] SP-API capability matrix (Codex)
- [ ] Shipping template audit + edit feasibility (Codex + Ava)
- [ ] FBA expansion opportunity list (Hermes)

### Phase 2 Deliverable (Apr 30)
- [ ] Automated data pipeline (Cloud Run → BigQuery)
- [ ] Weekly analysis cron (Hermes Sat 7 AM)
- [ ] Recommendation engine (rules-based)
- [ ] Dashboard + Slack integration
- [ ] SOP documentation

### Phase 3 Deliverable (May 31)
- [ ] Autonomous execution capability (with SafetyGuard)
- [ ] Approval workflow for high-impact changes
- [ ] FBA expansion campaign (first 20 designs)
- [ ] License obligation fast-track results

---

## Next Steps

1. **Cem Decision:** Approve Codex investigation of Cloud Run + SP-API (tonight)
2. **Codex Investigation:** SP-API capability audit (completed by morning)
3. **Ava + Cem Alignment:** Review findings, confirm Phase 1-3 roadmap
4. **Phase 1 Execution:** Data automation setup (Apr 11-20)

---

## Questions for LLM Council Review

1. **Data automation priority:** Should we pause all manual downloads immediately (risky) or run parallel for 2 weeks (safe but redundant)?
2. **Autonomous execution governance:** What approval thresholds are acceptable? (Current proposal: auto-execute negate terms + reallocations <$100, require approval for >$100)
3. **Regional strategy:** Should we treat each marketplace (US/UK/DE) separately, or optimize globally? (Current data only US)
4. **AI model training:** Should we invest in ML-driven bidding optimization (3-6 month lead time) or stick with rule-based for now?
5. **License obligation fast-track:** NBA is $200K behind. Should we aggressively reallocate budget to all NBA designs, or target only top-velocity ones?

---

## References

- **Hermes Sales Strategist Setup:** `/Users/openclaw/Vault/03-Agents/Hermes/HERMES_SALES_STRATEGIST_SETUP.md`
- **PULSE Intelligence Framework:** OPERATIONAL_BLUEPRINT_V3.md
- **Amazon SP-API Guide:** `/Users/openclaw/Vault/03-Agents/Harry/projects/amazon-sp-api/SP-API-GUIDE.md`
- **Conversion Dashboard:** https://conversion-dashboard-kohl.vercel.app
- **Weekly Listings SOP:** `/Users/openclaw/Vault/01-Wiki/31-listings-management/SOP_WEEKLY_REPORTS.md`
- **FBA Planner:** Cloud Run `fba-planner` service (Streamlit)

---

**Status:** Ready for LLM Council Review | **Owner:** Ava | **Last Updated:** 2026-04-10

