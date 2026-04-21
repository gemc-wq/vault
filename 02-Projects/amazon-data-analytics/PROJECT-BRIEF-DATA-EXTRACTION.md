# PROJECT BRIEF: Amazon Active Listings + Child ASIN Reports — Data Extraction & Usage

**Owner:** Ava (Strategy Lead) | **Operator:** Hermes (Sales Strategist) | **Version:** 1.0 | **Date:** 2026-04-10

---

## Executive Summary

We download two critical Amazon reports every week to track catalog health and sales performance:
1. **Active Listings Report** — What's live on Amazon (inventory snapshot)
2. **Child ASIN Report (14-day & 30-day)** — How each variant is selling

This brief documents **what data we extract**, **how we use it**, and **why it matters** for sales optimization.

---

## Report 1: ACTIVE LISTINGS REPORT

**What It Is:** A complete snapshot of every SKU currently live on Amazon (approx 3.43M listings)

**Format:** TSV (tab-separated values), ~6-7GB file

**Frequency:** Weekly download (Saturday morning)

**Data Provider:** Amazon Seller Central → Reports → Inventory → Active Listings Report

---

### Key Data Fields Extracted

| Field | Example | What It Shows | Why We Use It |
|-------|---------|---------------|---------------|
| **seller-sku** | HTPCR-IPH17PM-NARUICO-BLK | Our internal SKU | Link to inventory + designs |
| **asin** | B0DHXYZ123 | Amazon product ID | Track ASIN creation date |
| **product-name** | Naruto for iPhone 17 Pro Max Hybrid MagSafe Case | Customer-facing title | SEO keyword analysis, title quality |
| **quantity** | 250 | FBA units in Amazon fulfillment | Inventory health, restock triggers |
| **price** | 19.95 | List price (not current selling price) | Pricing strategy baseline |
| **status** | Active | Listing status | Identify inactive/suppressed listings |
| **open-date** | 2026-02-15 | When listing was created | Age of listing, new vs old |
| **fulfillment-channel** | FBA (or FBM) | Amazon FBA vs Merchant fulfillment | Conversion rate correlation (FBA >2x) |
| **asin1** | B0DHXYZ123 | Parent ASIN | Group variants together |
| **title-length** | 87 characters | Character count | SEO compliance check |
| **description-length** | 2,450 characters | Character count | Listing richness indicator |

---

### Gap Analysis: What We Check

**1. Device Coverage Gaps**
- Query: "Which designs are listed for iPhone 17 Pro Max but missing iPhone 17 base model?"
- Action: Create missing variant listing (marketplace ops)
- Impact: Recover ~$5-10K/month revenue per design (assumes 10% of top 50)

**2. Case Type Completeness**
- Query: "Which designs have HTPCR but missing HB401?"
- Action: Create HB401 variant (FBA-friendly, 4x higher conversion)
- Impact: Shift revenue from 2.96% → 11.81% conversion

**3. Variant Age Analysis**
- Query: "Which variants are >180 days old with zero sales?"
- Action: Retire or update listing
- Impact: Clean catalog, reduce clutter

**4. Fulfillment Channel Mismatch**
- Query: "Which high-velocity designs are FBM-only (should be FBA)?"
- Action: Switch to FBA, expect conversion lift
- Impact: 2x+ conversion improvement (proven by HB401 data)

**5. Listing Suppression Detection**
- Query: "Which SKUs show 'Inactive' status?"
- Action: Investigate suppression reason (review, stranding, etc.)
- Impact: Prevent revenue leakage

---

### Current Usage

**Saturday Morning Workflow:**
1. Download Active Listings Report → Mac Studio
2. Load into SQLite (`listings_current` table)
3. Run delta analysis vs previous week (`listings_previous`)
4. Extract: New listings, removed listings, price changes, status changes
5. Output: `weekly_delta_YYYY-MM-DD.json` (top 1,000 changes)

**Analytics Questions We Ask:**
- "How many SKUs are we active on across all marketplaces?"
- "Which designs have the best device coverage?"
- "What's the FBA penetration in our top 50 designs?"
- "How many listings are suppressed/inactive?"

---

### Suggested New Data Points to Extract

**1. LISTING QUALITY SCORE** (Composite)
```
Score = (description_length / 1500) × title_keyword_match × (asin_age_days / 30) × fulfillment_channel_conversion_multiplier
```
- Identifies listings needing updates
- Highlights underoptimized content
- Correlates with conversion rates

**2. DEVICE COVERAGE RATIO** (Per Design)
```
Coverage % = (devices_listed / total_target_devices) × 100
Target devices: iPhone 17 PM, 17 Pro, 17, 16 PM, 16 Pro, 16
```
- Measure completeness per design
- Identify expansion targets
- Flag designs missing >2 key devices

**3. CASE TYPE PENETRATION** (Per Design)
```
For each design:
- % listed as HTPCR (budget)
- % listed as HB401 (premium, FBA)
- % listed as HB6/HB7 MagSafe
- % listed as HLBWH (luxury)
```
- Identify designs with no premium options
- Optimize product mix per design
- Model price point mix

**4. LISTING AGE COHORT ANALYSIS**
```
Cohorts:
- 0-30 days (new, high launch momentum)
- 31-90 days (early adoption)
- 91-180 days (mature)
- 180+ days (aging, review risk)
```
- Correlate listing age with conversion
- Identify optimal refresh cycle
- Plan content updates

**5. ASIN LINKAGE QUALITY CHECK**
```
Validate: asin1 (parent) properly linked to seller-sku (child)
Flag: Orphaned ASINs (no parent linkage)
```
- Prevent duplicate ASINs
- Ensure proper variant grouping
- Identify Amazon mistakes

**6. SUPPRESSION ROOT CAUSE** (When Status = Inactive)
```
Currently: We see "Inactive" but don't know why
Suggested: Add reason code:
- Stranding (low velocity)
- Compliance review
- Price out of bounds
- Missing required fields
- Competitor complaint
```
- Action different suppression types differently
- Prevent recurrence
- Monitor by design/license

**7. TITLE KEYWORD ALIGNMENT** (Per Design)
```
Check if title contains:
- Design name (e.g., "Naruto")
- Device (e.g., "iPhone 17 Pro Max")
- Case type (e.g., "Hybrid MagSafe")
- "Officially Licensed"
```
- Identify underoptimized titles
- Benchmark against competitors
- Template consistency check

**8. PRICE TIER CLASSIFICATION** (Per SKU)
```
Category:
- Budget (<$15)
- Standard ($15-20)
- Premium ($20-30)
- Luxury (>$30)
By design + case type
```
- Analyze price elasticity per segment
- Identify pricing gaps
- Optimize price point mix per design

---

## Report 2: CHILD ASIN REPORT (14-day & 30-day)

**What It Is:** Sales performance data for every variant (child ASIN) of every design

**Format:** CSV, ~8-15MB per period

**Frequency:** Weekly download (Saturday morning) — 14-day and 30-day versions

**Data Provider:** Amazon Seller Central → Reports → Business Reports → Child ASIN Report

---

### Key Data Fields Extracted

| Field | Example | What It Shows | Why We Use It |
|-------|---------|---------------|---------------|
| **asin** | B0DHXYZ123 | Child ASIN (variant ID) | Tie sales to specific variant |
| **sku** | HTPCR-IPH17PM-NARUICO-BLK | Our seller SKU | Link to Active Listings |
| **sessions** | 1,245 | Number of customer visits | Traffic metric |
| **conversions** | 36 | Number of purchases | Sales metric |
| **conversion-rate** | 2.89% | Sessions → purchases | Quality metric (vs category avg 1.5%) |
| **revenue** | $719.20 | Total sales revenue | Revenue metric |
| **units-ordered** | 36 | Units sold | Volume metric |
| **average-selling-price** | $19.98 | Actual selling price (not list price) | Real pricing (includes discounts) |
| **b2b-revenue** | $0 | B2B sales | Separate from B2C (usually $0) |
| **browser-sessions** | 1,100 | Desktop/laptop traffic | Device split analysis |
| **mobile-sessions** | 145 | Mobile phone traffic | Mobile dominance (88% for us) |

---

### Gap Analysis: What We Check

**1. Variant Performance Ranking**
- Query: "Rank all variants by conversion rate — which are stars, which are dogs?"
- Action: Scale high-conversion, pause low-conversion
- Impact: Redirect $500-1000/month budget from low → high performers

**2. Velocity Trends (14d vs 30d)**
- Query: "Which designs are accelerating vs decelerating?"
- Formula: `velocity = 14d_revenue / 30d_revenue` 
  - >1.0 = accelerating (trend up)
  - <0.9 = decelerating (trend down)
- Action: Fast-track accelerating, reduce slow designs
- Impact: Optimize design portfolio

**3. Device Performance by Design**
- Query: "For Naruto design, does iPhone 17 Pro Max convert better than iPhone 16?"
- Action: Increase pricing or inventory allocation for better-converting devices
- Impact: Revenue uplift per device mix

**4. Conversion Outliers**
- Query: "Which individual variants have conversion >5% (vs design average 2.89%)?"
- Hypothesis: Better images, better title, price sweet spot, or device preference
- Action: Analyze outlier and replicate (copycat listing, increase inventory)
- Impact: Identify replicable winning factors

**5. Session Efficiency**
- Query: "Which variants have high sessions but low conversions (traffic quality issue)?"
- Action: Audit listing quality, test different titles, check for competitor complaints
- Impact: Recover wasted ad spend

**6. Mobile vs Desktop Split**
- Query: "For each design, what's the mobile:desktop ratio?"
- Current: Likely ~88% mobile (US Amazon)
- Action: Optimize images for mobile viewing
- Impact: Better conversion on primary traffic source

**7. Low-Volume, High-Conversion Opportunity**
- Query: "Which variants have <100 sessions but >3% conversion?"
- Action: Increase ad spend (ROAS justified)
- Impact: Scale winners with proven conversion

---

### Current Usage

**Saturday Morning Workflow:**
1. Download Child ASIN Report (14-day + 30-day) → Mac Studio
2. Load into SQLite
3. Calculate conversion rate, velocity, top performers
4. Compare to baseline (previous week)
5. Output: Top 20 performers, bottom 20, velocity gainers/losers

**Analytics Questions We Ask:**
- "Which 10 variants are driving 80% of revenue?"
- "Which designs are accelerating vs slowing?"
- "What's the overall conversion rate trend?"
- "Which device sizes sell best per design?"

---

### Suggested New Data Points to Extract / Calculate

**1. CONVERSION DECILE ANALYSIS**
```
Rank all variants by conversion rate, group into 10 tiers:
- Decile 1 (top 10%): >5% conversion
- Decile 2: 4-5%
- ...
- Decile 10: <1%

For each decile:
- Average price
- Average sessions
- Average revenue
- Product type (HTPCR, HB401, etc.)
- Design type (character, brand, etc.)
```
- Identify patterns in top performers
- Find underpriced/overpriced variants
- Spot product type performance gaps

**2. VELOCITY ACCELERATION SCORE** (Per Variant)
```
velocity_score = (14d_revenue / 30d_revenue) × 100
- >110 = strong acceleration (priority for scaling)
- 100-110 = stable/slight growth
- 90-100 = slight decline
- <90 = sharp decline (flag for review)
```
- Auto-flag accelerating designs for ad budget increase
- Auto-flag decelerating designs for investigation
- Track month-over-month momentum

**3. CONVERSION LEVERAGE** (Sensitivity Analysis)
```
For each design:
- If conversion improved +0.5%, what's revenue impact?
- Example: 1000 sessions × +0.5% × $20 = $100 additional revenue/day
```
- Prioritize CRO efforts on high-leverage designs
- Model ROI of listing improvements
- Identify designs worth A/B testing

**4. DEVICE MIX OPTIMIZATION** (Per Design)
```
For each design, calculate:
- iPhone 17 Pro Max: X% of sales, Y% conversion
- iPhone 17 Pro: X% of sales, Y% conversion
- ...all 6 target devices

Identify:
- Best-converting device (may warrant price increase)
- Worst-converting device (audit listing)
- Device with highest volume (ensure inventory)
```
- Optimize pricing by device
- Identify device-specific listing issues
- Improve inventory allocation

**5. REVENUE PER SESSION** (Efficiency Metric)
```
RPS = revenue / sessions
Example: $5,000 revenue / 2,000 sessions = $2.50 RPS

Benchmark:
- >$3.00 RPS = premium variant
- $2.00-3.00 = standard
- <$2.00 = budget or underperforming
```
- Measure traffic quality
- Identify underpriced variants
- Compare efficiency across designs

**6. SESSIONS PER UNIT** (Conversion Quality)
```
SPU = sessions / units_ordered
Example: 2,000 sessions / 40 units = 50 SPU

Interpretation:
- Low SPU (30) = sticky conversion, good margins
- High SPU (100+) = low conversion, needs CRO
```
- Identify listing quality issues
- Measure session "stickiness"
- Predict conversion improvement ROI

**7. PRICE ELASTICITY PROXY** (Variant Comparison)
```
Within a design, compare variants at different prices:
- HTPCR ($19.95): X sessions, Y conversion, Z revenue
- HB401 ($21.95): X sessions, Y conversion, Z revenue
- HB6/HB7 ($24.95): X sessions, Y conversion, Z revenue

Calculate: Revenue per price tier
```
- Identify optimal price points
- Understand customer willingness to pay
- Optimize product mix

**8. SESSIONS ALLOCATION EFFICIENCY** (Traffic Distribution)
```
For a design with 10 variants:
- What % of sessions go to each variant?
- Should allocation match inventory allocation?

Example: If Naruto-iPhone17PM gets 40% of sessions but only 10% of inventory → scale inventory
```
- Spot inventory misalignment
- Identify constrained variants
- Optimize fulfillment allocation

**9. CONVERSION ATTRIBUTION BY TRAFFIC SOURCE** (If Available)
```
Currently: Report shows total conversions
Suggested: Split by source (if Amazon provides)
- Organic search
- Sponsored ads (PPC)
- A9 recommendations
- Brand lookup

Why: Understand which channels drive real sales vs halo
```
- Measure true ad ROI (organic vs paid)
- Optimize ad spend allocation
- Identify natural search winners

**10. ANOMALY DETECTION FLAGS**
```
Auto-flag variants that:
- Conversion dropped >1% vs previous week (investigate)
- Sessions spiked >50% with no revenue lift (traffic quality issue)
- Revenue declined >30% despite stable sessions (price check)
- Price doesn't match expected range (data error or unauthorized seller?)
```
- Proactive problem detection
- Quick response to issues
- Prevent revenue leakage

---

## Data Integration: Linking the Two Reports

**The Power:** Combine Active Listings (what's live) + Child ASIN (how it's selling)

**Example 1: Identify Missing Variants**
```
Active Listings Report shows:
- Naruto design: Listed for iPhone 17PM, 17Pro, 17

Child ASIN Report shows:
- iPhone 17: High conversion (3.5%)
- iPhone 17PM: Moderate conversion (2.8%)
- iPhone 17Pro: Zero sales

Gap: iPhone 17Pro variant likely missing or suppressed
Action: Check Active Listings status, recreate if needed
```

**Example 2: Identify Underperforming Listings**
```
Active Listings Report shows:
- SKU HTPCR-IPH16PM-ONEPIECE-RED is Active, price $19.95, open 60 days

Child ASIN Report shows:
- Same SKU: 50 sessions, 0 conversions (0% conversion)

Gap: Listed product, but converts zero
Action: Audit title/images/review score, compare to similar SKUs
```

**Example 3: Identify FBA Opportunity**
```
Active Listings Report shows:
- SKU is FBM-only (fulfillment-channel = Merchant)

Child ASIN Report shows:
- Conversion 2.5% (below design average 3.2%)

Hypothesis: FBM slower shipping hurts conversion
Action: Move to FBA if inventory allows (expect 4x conversion lift like HB401)
```

---

## Current Workflow vs Ideal Workflow

### **Current (Manual)**
```
Friday 5 PM: Cem downloads 2 reports → Mac Studio
Saturday 8 AM: Load into SQLite
Saturday 9 AM: Hermes manually creates pivot tables
Saturday 11 AM: Identify top 20 performers, top 20 underperformers
Saturday 1 PM: Email recommendations
Result: 5-6 hours manual work per week
```

### **Ideal (Automated)**
```
Saturday 6 AM: Cloud Run auto-downloads both reports → BigQuery
Saturday 6:30 AM: Auto-load + transform (SQLite)
Saturday 7 AM: Hermes analysis cron runs:
  - Calculates all 10 suggested data points
  - Flags anomalies
  - Generates recommendations
Saturday 7:30 AM: Dashboard updated + Slack alert sent
Result: 0 manual work, 30min to review + approve
```

---

## Recommended Data Extraction Pipeline

**Step 1: Ingest**
- Active Listings Report → `listings_current` table
- Child ASIN Report → `child_asin_current` table
- Previous week → `listings_previous`, `child_asin_previous`

**Step 2: Clean**
- Remove test listings (SKU contains "TEST")
- Remove suppressed status
- Join on SKU + ASIN

**Step 3: Calculate Core Metrics**
- Conversion rate (conversions / sessions)
- Revenue per session
- Velocity (14d / 30d)
- Device split

**Step 4: Calculate Suggested Metrics**
- Listing quality score
- Device coverage ratio
- Case type penetration
- Conversion deciles
- Velocity acceleration
- Sessions per unit

**Step 5: Generate Recommendations**
- Top 20 variants to scale (high conversion + growing)
- Top 20 variants to investigate (low conversion + stable sessions)
- Missing variants to create (device gaps)
- Underpriced variants (high RPS, should raise price)
- FBA migration candidates

**Step 6: Deliver**
- Dashboard (updated, real-time)
- Slack digest (Saturday 8 AM, high-level summary)
- Email to Cem (detailed recommendations, action items)

---

## FAQ: Why These Data Points?

**Q: Why "Conversion Decile Analysis"?**
A: Identify patterns in top 10% performers (price, device, case type) → replicate for bottom performers

**Q: Why "Velocity Acceleration Score"?**
A: Separate growing designs (invest) from declining (investigate) automatically

**Q: Why "Revenue Per Session"?**
A: Measure listing quality + pricing effectiveness in one metric

**Q: Why "Sessions Per Unit"?**
A: Know if session traffic is converting or just browsing

**Q: Why "Device Mix Optimization"?**
A: iPhone 17PM may convert 2x better than iPhone 16 → price accordingly

**Q: Why "Anomaly Detection"?**
A: Catch problems (suppression, price glitches, review attacks) same week, not month later

---

## Success Metrics (After Implementation)

| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| **Data freshness** | Manual, 24h delay | Automated, <2h | Week 1 |
| **Variants analyzed per week** | ~1,000 (top designs only) | All 1,800+ variants | Week 2 |
| **Anomalies detected** | 2-3 per week (manual) | 10+ per week (automated) | Week 2 |
| **Recommendations generated** | 15-20 per week (email) | 50+ per week (dashboard) | Week 3 |
| **Action time** | Cem + team: 4-5 hours to review | Cem: 30 min to approve/execute | Week 4 |
| **Revenue impact** | $0 (analysis-only) | +$5-10K/month (from gap closing) | Month 2 |

---

## Implementation Phases

### **Phase 1: Data Extraction (Week 1)**
- Automate report downloads (Cloud Run)
- Build SQLite schema (Active + Child ASIN tables)
- Create core metrics (conversion rate, velocity, device split)

### **Phase 2: Suggested Metrics (Week 2)**
- Add 10 suggested data points (quality score, deciles, etc.)
- Build anomaly detection (flag down >1%, up >50%, etc.)
- Create output tables (ready for dashboard)

### **Phase 3: Automation (Week 3)**
- Wire Hermes analysis cron (Sat 7 AM)
- Build dashboard (live metrics)
- Add Slack integration (auto-alert on anomalies)

### **Phase 4: Actionable Insights (Week 4)**
- Create recommendation engine (rules-based)
- Link to Cem's calendar (Saturday review slot)
- Measure impact (track actions taken + revenue impact)

---

## Questions for Implementation

1. **Data Storage:** Use BigQuery (cloud) or SQLite (local Mac Studio)?
   - BigQuery: Better for scale, real-time dashboard, historical analysis
   - SQLite: Simple, local, faster to implement

2. **Metric Priority:** Which 3 of the 10 suggested metrics are most critical?
   - Conversion Decile Analysis (understand winners)
   - Velocity Acceleration (fast-track growth)
   - Device Mix Optimization (price by device)

3. **Anomaly Thresholds:** What's the right sensitivity?
   - Flag conversion drop >0.5%? >1%? >2%?
   - Flag sessions spike >30%? >50%? >100%?

4. **Dashboard Frequency:** Update real-time or daily at 8 AM?
   - Real-time: Better for tracking, higher compute cost
   - Daily (8 AM): Good enough, lower cost

---

## Next Steps

1. **Cem decision:** Which data points are highest priority?
2. **Codex implementation:** Build Phase 1 (auto-download + core metrics)
3. **Hermes validation:** Test Phase 2 metrics against manual analysis
4. **Deploy Phase 3-4:** Full automation by end of month

---

**Status:** Ready for implementation | **Owner:** Ava | **Last Updated:** 2026-04-10

