# Amazon Active Listings + Child ASIN Reports — Data Extraction & Optimization Guide

**Owner:** Ava (Strategy Lead) | **Operator:** Hermes (Sales Strategist) | **Version:** 1.0 | **Date:** 2026-04-10

---

## Executive Summary

We download two critical Amazon reports weekly to optimize sales:
1. **Active Listings Report** — Inventory snapshot of 3.43M+ SKUs live on Amazon
2. **Child ASIN Report (14-day & 30-day)** — Sales performance for each variant

This guide documents **what data we extract**, **how we use it**, **why it matters**, and **critical file size constraints** affecting automation.

---

## CRITICAL ISSUE: Active Listings Report File Size

### The Problem

**File Size:** 6-7 GB per download (some weeks >10 GB)

**Impact on Automation:**
| Constraint | Problem | Effect |
|-----------|---------|--------|
| **Download time** | ~15-30 minutes on broadband | Delays Saturday morning pipeline |
| **Storage capacity** | Mac Studio has 460GB total | Filling up with weekly downloads |
| **Transfer speed** | ~20-30 MB/s typical | Bottleneck in automation |
| **Memory usage** | Loading 6GB file into memory = crash | Can't process entire file at once |
| **Cloud Run timeouts** | API call timeouts after 3600s | Can't reliably download via Cloud Run |
| **Network interruption** | 15-30min download = high failure rate | Interrupted downloads = corrupted files |

### Why It's So Large

The Active Listings Report contains **3.43M+ rows** of data:

```
Columns: ~25 fields per SKU
- seller-sku, asin, product-name, quantity, price, status
- fulfillment-channel, open-date, review-score, review-count
- +15 other metadata fields

File format: TSV (tab-separated values)
- Not compressed
- Each row ~200-500 bytes
- 3.43M rows × 300 bytes avg = 1GB+

Reality: File grows with catalog expansion
- Feb 2026: 6GB
- Mar 2026: 7GB
- Apr 2026: 7.5GB+ (growing 0.5GB/month)
```

### Current Workaround (Manual Download)

**Friday 5 PM:** Cem manually downloads via Amazon Seller Central
- ✅ Seller Central has aggressive timeouts
- ✅ Seller Central resumes failed downloads
- ✅ Downloads to local Mac Studio (fast local network)
- ❌ Manual process, 5-10 minutes of Cem's time

---

## Report 1: ACTIVE LISTINGS REPORT

### Overview

| Property | Value |
|----------|-------|
| **What It Is** | Complete inventory snapshot of every SKU live on Amazon |
| **Size** | 6-7 GB per download (growing ~0.5GB/month) |
| **Frequency** | Weekly (Saturday morning) |
| **Format** | TSV (tab-separated values), not compressed |
| **Scope** | 3.43M+ rows (all marketplaces: US, UK, DE, etc.) |
| **Freshness** | Updated daily by Amazon, report is point-in-time snapshot |
| **Source** | Amazon Seller Central → Reports → Inventory → Active Listings Report |

### Key Data Fields

| Field | Example | What It Shows | Why We Use It |
|-------|---------|---------------|---------------|
| **seller-sku** | HTPCR-IPH17PM-NARUICO-BLK | Our internal SKU identifier | Link to inventory system, design, case type, device |
| **asin** | B0DHXYZ123 | Amazon's product ID for variant | Tie to sales data, track ASIN creation date |
| **product-name** | Naruto for iPhone 17 Pro Max Hybrid MagSafe Case | Customer-facing title | SEO analysis, keyword alignment, title quality |
| **quantity** | 250 | Units in Amazon FBA fulfillment center | Inventory health, restock triggers, stock-out risks |
| **price** | 19.95 | List price (not current selling price) | Pricing strategy baseline, compare to actual selling price |
| **status** | Active | Listing status code | Identify inactive, suppressed, or stranded listings |
| **open-date** | 2026-02-15 | Date listing was first created | Age of listing, correlate with conversion performance |
| **fulfillment-channel** | FBA | Amazon FBA vs Merchant fulfillment | Critical: FBA shows 2-day delivery (4x higher conversion than FBM) |
| **asin1** | B0DHXYZ123 | Parent ASIN | Group variants together, identify variant family |
| **title-length** | 87 characters | Character count of product title | Check SEO compliance, avoid truncation |
| **description-length** | 2,450 characters | Rich description character count | Indicator of listing completeness |
| **review-score** | 4.5 | Average customer rating (1-5 stars) | Quality signal, impacts conversion |
| **review-count** | 247 | Total reviews | Social proof, older listings have more reviews |

---

### What We Extract: Gap Analysis

We currently analyze **5 key gaps**:

#### **Gap 1: Device Coverage Gaps**

**Question:** Which designs are listed for iPhone 17 Pro Max but missing other key devices?

**Target Devices (6):**
- iPhone 17 Pro Max
- iPhone 17 Pro
- iPhone 17 (base)
- iPhone 16 Pro Max
- iPhone 16 Pro
- iPhone 16 (base)

**Example Finding:**
```
Naruto design:
- Listed: iPhone 17PM ✅, iPhone 17Pro ✅, iPhone 17 ✅
- Missing: iPhone 16PM ❌, iPhone 16Pro ❌, iPhone 16 ❌

Gap: 3 missing variants
Expected Revenue: $500-1,000/month (assume 2% conversion, $20 ASP)
Action: Create iPhone 16 variants
Timeline: 1 week
```

**Revenue Opportunity:** $5-10K/month from gap closure (across all designs)

---

#### **Gap 2: Case Type Completeness**

**Question:** Which designs have soft-gel HTPCR but are missing premium case types (HB401, HB6, HB7)?

**Case Types:** 
- HTPCR: Soft gel, $19.95 (budget, FBM-only)
- HB401: Hard case, $19.95 (FBA-friendly, 4x higher conversion than HTPCR)
- HB6CR: Hard + MagSafe, $24.95 (premium, FBA)
- HB7BK: Hard + MagSafe black, $24.95 (premium, FBA)
- HLBWH: Leather wallet, $24.95 (luxury)

**Example Finding:**
```
Naruto design:
- HTPCR: Listed on 4 devices ✅
- HB401: Listed on 0 devices ❌ (MISSING!)
- HB6CR: Listed on 2 devices ✅
- HB7BK: Listed on 0 devices ❌ (MISSING!)
- HLBWH: Listed on 1 device ✅

Gap: HB401 completely missing
Data Point: HB401 converts 11.81% vs HTPCR 2.96% (4x better)
Revenue Opportunity: $2-5K/month if created and advertised
Action: Create HB401 across all iPhone variants
Timeline: 2 weeks
```

---

#### **Gap 3: Variant Age Analysis**

**Question:** Which variants are >180 days old with zero sales?

**Why It Matters:**
- Old listings accumulate negative reviews
- Amazon may suppress old low-performing listings
- Clutters catalog, increases suppression risk
- Taking up inventory slots for winners

**Example Finding:**
```
Old One Piece variants:
- HTPCR-IPH15PM-ONEPIECE-RED: open-date 2025-08-10 (241 days old)
  → Child ASIN report: 0 sales in last 30 days ❌
  
- HTPCR-IPH15-ONEPIECE-BLU: open-date 2025-07-20 (254 days old)
  → Child ASIN report: 2 sales in last 30 days (declining)

Action: Retire HTPCR-IPH15PM (dead weight), or refresh with new images
Timeline: 2 weeks (get new images from Sven)
```

---

#### **Gap 4: Fulfillment Channel Mismatch**

**Question:** Which high-velocity designs are FBM-only but should be FBA?

**Critical Data Point:** FBA = 2-day delivery visible in search results = 4x higher conversion

**Example Finding:**
```
NFL designs (active licenses, high velocity):
- Patrick Mahomes: HTPCR-IPH17PM-PATMAH-RED = FBM
  Expected velocity: High (top player)
  Expected conversion: 2.96% (HTPCR + FBM)
  If moved to FBA: Expect 4x conversion (11.81% like HB401)
  
- Travis Kelce: HTPCR-IPH17PM-TKELCE-RED = FBM
  Expected velocity: High
  Expected conversion: 2.96% (FBM hurts)
  If moved to FBA: Potential +4x conversion

Action: Inventory planning to move top 10 NFL designs to FBA
Expected Impact: $10-15K/month revenue uplift
Timeline: 1 month (depends on inventory)
```

---

#### **Gap 5: Listing Suppression Detection**

**Question:** Which SKUs show 'Inactive' or 'Suppressed' status?

**Why It Matters:**
- Suppressed listings = zero visibility, zero sales
- Root causes vary: review issues, compliance, stranding, price out of bounds
- Need to diagnose and fix quickly

**Example Finding:**
```
Status = Suppressed:
- HTPCR-IPH16PM-PEANUTS-RED: Last sale 180 days ago, now suppressed
  Reason: Likely "Stranding" (low velocity)
  Action: Retire (don't try to revive low sellers)

- HB401-IPH17PM-NARUTO-BLK: Suppressed for unknown reason
  Expected: High seller (Naruto is top 5 design)
  Action: Investigate (review bombing? compliance? listing error?)
  Fix: Update content, request review reinstatement
  Timeline: 5 days
```

---

### Suggested New Data Points to Extract

#### **1. LISTING QUALITY SCORE** (Composite Metric)

Calculate a score 0-100 for each SKU:

```
quality_score = (
  (description_length / 2000) × 30 +           # Content completeness (max 30 pts)
  (title_keyword_match / 1.0) × 20 +          # Title relevance (max 20 pts)
  (review_score / 5.0) × 25 +                 # Review rating (max 25 pts)
  (images_count / 6) × 15 +                   # Image count (max 15 pts)
  (fulfillment_channel == 'FBA' ? 10 : 0)     # FBA bonus (max 10 pts)
) × (age_multiplier)                          # Decay over time

Example Results:
- NARUTO-IPH17PM-HB401 = 92 (excellent, FBA, good reviews, great images)
- PEANUTS-IPH16-HTPCR = 34 (poor, FBM, short description, few reviews, old)
```

**Use Case:** Identify which listings need urgent updates

---

#### **2. DEVICE COVERAGE RATIO** (Per Design)

Calculate coverage % for each design:

```
coverage_ratio = (devices_currently_listed / target_devices) × 100

Target Devices: 6 (iPhone 17PM, 17Pro, 17, 16PM, 16Pro, 16)

Example Results:
- Naruto: 5/6 devices = 83% (missing iPhone 16)
- Peanuts: 6/6 devices = 100% ✅
- Harry Potter: 2/6 devices = 33% ⚠️ (major gap)
```

**Use Case:** Identify expansion targets, measure catalog completeness

---

#### **3. CASE TYPE PENETRATION** (Per Design)

For each design, calculate % listed in each case type:

```
For Naruto Design:
- HTPCR (budget, FBM): 6 devices = 67%
- HB401 (premium, FBA): 0 devices = 0% ❌ MISSING
- HB6/HB7 (luxury): 3 devices = 33%
- HLBWH (wallet): 1 device = 11%

Action: CREATE HB401 for all 6 devices (0% → 100%)
Expected Impact: +$2-5K/month revenue
```

**Use Case:** Optimize product mix per design, identify FBA gaps

---

#### **4. LISTING AGE COHORT ANALYSIS**

Group all SKUs by age:

```
Cohorts:
- NEW (0-30 days): High launch momentum, frequent changes
- EARLY (31-90 days): Early adoption phase, reviews accumulating
- MATURE (91-180 days): Stable performer, review count peak
- AGING (180+ days): Risk of suppression, declining velocity

Example Distribution:
- NEW: 120 SKUs (8%)
- EARLY: 350 SKUs (23%)
- MATURE: 800 SKUs (54%)
- AGING: 230 SKUs (15%)

Action: Investigate AGING cohort for suppression/retirement decisions
```

**Use Case:** Correlate listing age with conversion performance, plan refresh cycles

---

#### **5. ASIN LINKAGE QUALITY CHECK**

Validate parent-child ASIN relationships:

```
Check: Does asin1 (parent) match seller-sku family?
Example:
✅ HTPCR-IPH17PM-NARUTO-BLK → asin1=B0DHXYZ123 (correct parent)
❌ HTPCR-IPH17PM-NARUTO-RED → asin1=B0DHXYZ999 (wrong parent! orphaned variant)

Action: Relink orphaned variants to correct parent ASIN
Impact: Prevent duplicate ASIN creation, ensure proper variant grouping
```

**Use Case:** Catch Amazon data errors, prevent catalog fragmentation

---

#### **6. SUPPRESSION ROOT CAUSE ANALYSIS**

Add reason codes for suppressed listings:

```
Currently: status="Suppressed" (no context)
Suggested: status="Suppressed", suppression_reason="stranding|compliance|price|review|other"

Example:
- PEANUTS-IPH16PM-HTPCR: suppression_reason="stranding" (low velocity, no sales)
  Action: Retire, don't waste time fixing
  
- NARUTO-IPH17PM-HB401: suppression_reason="compliance" (might be fixable)
  Action: Investigate, request reinstatement
  
- ONEPIECE-IPH17PM-HB6: suppression_reason="price" (price out of bounds)
  Action: Adjust price, reactivate

Use Case: Triage suppressed listings, prioritize fixes
```

---

#### **7. TITLE KEYWORD ALIGNMENT CHECK**

Validate each title contains required elements:

```
Required Keywords (SEO Best Practice):
1. Design name (e.g., "Naruto")
2. Device (e.g., "iPhone 17 Pro Max")
3. Case type (e.g., "Hybrid MagSafe")
4. License claim (e.g., "Officially Licensed")

Example Titles:
✅ "Naruto for iPhone 17 Pro Max Hybrid MagSafe Case Officially Licensed"
❌ "Character Case" (missing all 4 keywords!)
⚠️  "Naruto Case" (missing device, case type, license)

Score: (keywords_present / 4) × 100
- 4/4 = 100 (excellent)
- 3/4 = 75 (good)
- 2/4 = 50 (poor)
- <2/4 = critical (rewrite needed)

Use Case: Identify underoptimized titles for SEO improvement
```

---

#### **8. PRICE TIER CLASSIFICATION**

Classify each SKU by price point:

```
Budget: <$15
Standard: $15-20
Premium: $20-30
Luxury: >$30

By Design + Case Type:
Example Naruto:
- HTPCR ($19.95) = Standard
- HB401 ($21.95) = Premium (slight premium)
- HB6 ($24.95) = Premium
- HLBWH ($29.95) = Luxury

Use Case: Analyze price elasticity, optimize product mix
```

---

### Current Processing Workflow

**Saturday Morning:**
1. Download Active Listings Report → Mac Studio `~/Downloads/`
2. Load into SQLite:
   - Copy previous week's data: `listings_current` → `listings_previous`
   - Load new file into: `listings_current`
3. Calculate delta: New listings, removed listings, price changes
4. Output: `weekly_delta_YYYY-MM-DD.json` (top 1,000 changes)
5. Store: Keep file for 2 weeks, then delete (to save space)

**Hermes Analysis:**
- Top 20 new designs
- Top 20 removed designs
- Device coverage gaps
- FBA penetration analysis

---

### File Size Management Strategy

#### **Option A: Keep Current (Manual Download)**
- ✅ Works reliably (Seller Central handles large files)
- ✅ Fast (downloads to local Mac Studio network)
- ❌ Manual process (5-10 min per week)
- ❌ Storage fills up (460GB, growing 0.5GB/month)

**Action:** Delete files after 2-week analysis window

---

#### **Option B: Stream Processing (Recommended)**
Instead of loading entire 6GB file into memory:

```
1. Download file in chunks (1GB at a time)
2. Process chunk → extract key fields only
3. Write to SQLite immediately
4. Move to next chunk
5. Delete source file when done

Benefits:
✅ No memory crashes
✅ Can be automated (fits in Cloud Run 1GB limit)
✅ Storage-efficient (process and delete same day)
❌ Slower (15-30 min processing vs instant)

Tool: Use pandas chunked reading
```

```python
# Pseudocode
import pandas as pd

for chunk in pd.read_csv('active_listings.tsv', chunksize=50000, sep='\t'):
    # Extract: seller_sku, asin, quantity, price, status, fulfillment_channel, open_date
    chunk_subset = chunk[['seller-sku', 'asin', 'quantity', 'price', 'status', 'fulfillment-channel', 'open-date']]
    
    # Load to SQLite
    chunk_subset.to_sql('listings_current', conn, if_exists='append')
    
    # Delete chunk from memory
    del chunk_subset
```

---

#### **Option C: API-based Delta Only (Future)**
Once Amazon SP-API improves:

```
Instead of downloading full 6GB weekly:
1. Query SP-API for changes since last sync
2. Pull only new/modified/removed listings (likely <50MB)
3. Merge with existing data

Timeline: Not available yet (Amazon still developing)
```

---

## Report 2: CHILD ASIN REPORT (14-day & 30-day Sales Data)

### Overview

| Property | Value |
|----------|-------|
| **What It Is** | Sales performance data for every variant (child ASIN) |
| **Size** | 8-15 MB per period (compressed, manageable) |
| **Frequency** | Weekly (14-day and 30-day versions) |
| **Format** | CSV, can be gzipped |
| **Scope** | ~1,800+ child ASINs (variants) |
| **Freshness** | Reports lag by 1-2 days (Amazon data pipeline) |
| **Source** | Amazon Seller Central → Reports → Business Reports → Child ASIN Report |

---

### Key Data Fields

| Field | Example | What It Shows | Why We Use It |
|-------|---------|---------------|---------------|
| **asin** | B0DHXYZ123 | Child ASIN (variant ID) | Tie sales to specific variant |
| **sku** | HTPCR-IPH17PM-NARUICO-BLK | Our seller SKU | Join with Active Listings data |
| **sessions** | 1,245 | Customer visits to product detail page | Traffic metric |
| **conversions** | 36 | Number of units purchased | Sales metric |
| **conversion-rate** | 2.89% | Sessions → conversions (%) | Quality metric (vs 1.5% category avg) |
| **revenue** | $719.20 | Total sales revenue | Revenue metric |
| **units-ordered** | 36 | Units sold | Volume metric |
| **average-selling-price** | $19.98 | Actual selling price (after discounts) | Real pricing, compare to list price |
| **browser-sessions** | 1,100 | Desktop/laptop visits | Device traffic split |
| **mobile-sessions** | 145 | Mobile phone visits | Mobile dominance (88% for us) |

---

### What We Extract: Gap Analysis

#### **Gap 1: Variant Performance Ranking**

**Question:** Rank all variants by conversion rate — which are top performers (stars), which are bottom performers (dogs)?

**Current Analysis:**
```
Top 10 Variants (by conversion rate):
1. NARUTO-IPH17PM-HB401: 15.2% conversion ⭐
2. ONEPIECE-IPH17PM-HB401: 14.8% conversion ⭐
3. PEANUTS-IPH17PM-HB6: 9.5% conversion ✅
... (cut for brevity)

Bottom 10 Variants (by conversion rate):
1. OLDDESIGN-IPH15-HTPCR: 0.2% conversion ❌ (retire)
2. FAILEDLAUNCH-IPH16PM-HB401: 0.5% conversion ❌ (investigate)
```

**Action:** Scale ads for top performers, pause bottom performers

---

#### **Gap 2: Velocity Trends (14-day vs 30-day)**

**Question:** Which designs are accelerating vs decelerating?

**Formula:**
```
velocity_score = (14d_revenue / 30d_revenue) × 100

>110 = Strong acceleration (trending up, invest in ads)
100-110 = Stable growth
90-100 = Slight decline
<90 = Sharp decline (investigate or retire)
```

**Example Finding:**
```
Naruto Design:
- 30d revenue: $5,000
- 14d revenue: $3,200
- Velocity: (3,200 / 5,000) × 100 = 64 ❌ DECLINING

Likely causes:
1. Competitor price drop
2. Running out of inventory (constrained)
3. Ad budget cut
4. Seasonal trend (e.g., anime convention ended)

Action: Investigate root cause, consider fast-track investment if good ROI
```

---

#### **Gap 3: Device Performance by Design**

**Question:** For a single design (e.g., Naruto), does iPhone 17 Pro Max convert better than iPhone 16?

**Example Data:**
```
Naruto Design Variants:
- NARUTO-IPH17PM-HB401: 150 sessions, 12 conversions = 8% conversion
- NARUTO-IPH17PM-HB401: 180 sessions, 10 conversions = 5.6% conversion
- NARUTO-IPH16PM-HB401: 100 sessions, 3 conversions = 3% conversion
- NARUTO-IPH16-HB401: 80 sessions, 1 conversion = 1.25% conversion

Finding: Newer devices (iPhone 17) convert 2-3x better than older (iPhone 16)
Hypothesis: Newer device owners have better age/income profile, more willing to pay
Action: Price newer devices +$2-3 (e.g., 17PM at $24.95 vs 16 at $19.95)
```

---

#### **Gap 4: Conversion Outliers**

**Question:** Which individual variants have conversion >5% (vs design average 2.89%)?

**Why It Matters:**
- Outliers = special success factors (better images? better price? better title?)
- Replicate = increase inventory, duplicate design element

**Example Finding:**
```
Peanuts Design Analysis:
- Average conversion: 2.1%
- PEANUTS-IPH17PM-HB6: 7.8% conversion ⭐⭐⭐ OUTLIER

Why? Likely:
- HB6 = premium case (attracts quality buyers)
- iPhone 17PM = newest flagship (early adopters, higher spending)
- Limited inventory = scarcity effect

Action: 
1. Stock more PEANUTS-HB6 (proven winner)
2. Increase ad spend for this variant (ROAS justified)
3. Test iPhone 17Pro/17 with HB6 (same formula)
4. Consider price increase ($24.95 → $25.95)
```

---

#### **Gap 5: Session Efficiency**

**Question:** Which variants have high sessions but low conversions (traffic quality issue)?

**Formula:**
```
session_efficiency = conversions / sessions

Healthy: >2.5% (good quality traffic)
Concerning: 1-2.5% (something off)
Poor: <1% (traffic quality issue, listing problem)
```

**Example Finding:**
```
NARUTO-IPH16PM-HTPCR:
- Sessions: 500
- Conversions: 2
- Conversion rate: 0.4% ❌

Diagnosis: High traffic but zero conversions
Likely causes:
1. Title doesn't match search query (misleading)
2. Images don't match product (wrong color, variant)
3. Listing suppressed review score (customer complaints)
4. Price too high vs competition

Action: Audit listing quality, rewrite title, update images
Timeline: 1 week
```

---

#### **Gap 6: Mobile vs Desktop Split**

**Question:** For each design, what's the mobile:desktop ratio?

**Typical Finding:**
```
Naruto Design:
- Browser sessions (desktop): 400 (25%)
- Mobile sessions: 1,200 (75%)
- Ratio: 1:3 (mobile dominates)

Industry avg: 1:2 (50% mobile, 50% desktop)
Our avg: 1:3.5 (74% mobile, 26% desktop)

Implication: Mobile users buy more from us (or older devices skew toward mobile)
Action: Optimize mobile experience (images, loading time, one-click checkout)
```

---

#### **Gap 7: Low-Volume, High-Conversion Opportunities**

**Question:** Which variants have <100 sessions but >3% conversion (underinvested)?

**Example Finding:**
```
HARRYPOTTER-IPH17PM-HB401:
- Sessions: 45
- Conversions: 2
- Conversion rate: 4.4% ⭐ (vs design avg 2.1%)

Data interpretation:
- Small sample (45 sessions), but trending well
- Likely needs more ads to reach volume
- ROAS justified (4.4% > 2.89% baseline)

Action: Allocate $200/month ad budget test
Expected: 500 sessions/month × 4.4% × $20 = $440 revenue
Ad cost: ~$80 (assuming 5.74x ROAS, 17.42% ACOS)
Profit: $360/month, break-even in 2 weeks
Timeline: Start immediately
```

---

### Suggested New Data Points to Extract / Calculate

#### **1. CONVERSION DECILE ANALYSIS**

Rank all variants into 10 tiers by conversion rate:

```
Decile 1 (Top 10%): >5% conversion
Decile 2: 4-5% conversion
Decile 3: 3.5-4% conversion
Decile 4: 3-3.5% conversion
Decile 5: 2.5-3% conversion (baseline)
Decile 6: 2-2.5% conversion
Decile 7: 1.5-2% conversion
Decile 8: 1-1.5% conversion
Decile 9: 0.5-1% conversion
Decile 10 (Bottom 10%): <0.5% conversion

For each decile, analyze:
- Average price point
- Average sessions
- Average revenue
- Product type distribution (HTPCR, HB401, HB6, etc.)
- Design type distribution (character, brand, etc.)
- Average age of listing
- FBA vs FBM split

Finding: Decile 1 is 80% HB401 + HB6/7 (premium) + FBA
Implication: Premium + FBA = higher conversion
Action: Shift portfolio toward premium case types
```

---

#### **2. VELOCITY ACCELERATION SCORE**

Auto-flag variants by momentum:

```
velocity_score = (14d_revenue / 30d_revenue) × 100

>120 = Explosive acceleration ⚡ (scale aggressively)
110-120 = Strong growth 📈 (increase budget)
100-110 = Stable/slight growth ✅ (maintain)
90-100 = Slight decline ⚠️ (monitor)
80-90 = Moderate decline ⚠️⚠️ (investigate)
<80 = Sharp decline 📉 (pause or retire)

Use Case: Auto-generate scaling recommendations
Example: NARUTO-IPH17PM-HB401 score = 115 → "Increase ad budget 20%"
```

---

#### **3. CONVERSION LEVERAGE** (Sensitivity Analysis)

Calculate ROI of listing improvements:

```
For each variant, if conversion improved by 0.5%:
  leverage = (sessions × 0.005) × average_price

Example:
PEANUTS-IPH16PM-HB401:
- Sessions: 1,000
- Avg price: $21.95
- Current conversion: 2.1%

If conversion → 2.6% (+0.5%):
- Additional sales: 1,000 × 0.005 = 5 units
- Additional revenue: 5 × $21.95 = $109.75/week
- Annual impact: $109.75 × 52 = $5,707

Use Case: Prioritize CRO (conversion rate optimization) efforts on high-leverage designs
Action: If improvement cost <$1,000, pursue (ROI >5x first year)
```

---

#### **4. DEVICE MIX OPTIMIZATION**

For each design, break down by device:

```
Naruto Design Device Performance:
Device | Sessions | Conversions | Conv% | Revenue | Avg Price
17PM   | 500      | 48          | 9.6%  | $1,000  | $20.83 ⭐
17Pro  | 400      | 36          | 9.0%  | $792    | $22.00 ⭐
17     | 300      | 21          | 7.0%  | $420    | $20.00 ✅
16PM   | 200      | 10          | 5.0%  | $200    | $20.00 ⚠️
16Pro  | 150      | 6           | 4.0%  | $120    | $20.00 ⚠️
16     | 100      | 2           | 2.0%  | $40     | $20.00 ❌

Finding: iPhone 17 devices (PM, Pro, base) convert 2-5x better than iPhone 16 devices
Hypothesis: Product life cycle (newer = higher intent buyers)
Action: Price iPhone 17PM at $22.95 (vs 16 at $19.95)
Expected: Maintain same conversion, +4% revenue uplift
```

---

#### **5. REVENUE PER SESSION (RPS)**

Efficiency metric for listing quality:

```
RPS = revenue / sessions

Example:
NARUTO-IPH17PM-HB401: $1,000 revenue / 500 sessions = $2.00 RPS
PEANUTS-IPH17PM-HLBWH: $600 revenue / 150 sessions = $4.00 RPS ⭐

Interpretation:
- >$3.00 RPS = Premium variant (luxury, high ASP)
- $2.00-3.00 RPS = Standard (healthy, balanced)
- <$2.00 RPS = Budget or underperforming (investigate)

Use Case: Identify underpriced variants
Example: ONEPIECE-IPH17PM at $1.50 RPS (vs $2.00 avg) → raise price to $22.95
```

---

#### **6. SESSIONS PER UNIT (SPU)**

Conversion quality metric:

```
SPU = sessions / units_ordered

SPU Ranges:
- <25 = Excellent (very sticky conversion)
- 25-50 = Good (healthy conversion)
- 50-100 = Fair (needs improvement)
- >100 = Poor (listing quality issue)

Example:
NARUTO-IPH17PM-HB401: 500 sessions / 48 units = 10.4 SPU ⭐ (excellent)
PEANUTS-IPH16-HTPCR: 300 sessions / 3 units = 100 SPU ❌ (poor)

Use Case: Quickly identify which listings need content updates
Action: SPU >75 = audit and rewrite listing
```

---

#### **7. PRICE ELASTICITY PROXY**

Compare variants at different price points:

```
For Naruto Design, compare case types at different prices:

Case Type | Price | Sessions | Conversions | Conv% | Revenue | RPS
HTPCR     | $19.95 | 300     | 6           | 2.0%  | $119    | $0.40
HB401     | $21.95 | 500     | 48          | 9.6%  | $1,056  | $2.11
HB6       | $24.95 | 250     | 30          | 12%   | $748    | $2.99
HLBWH     | $29.95 | 100     | 15          | 15%   | $449    | $4.49

Finding: Higher price = higher conversion % (quality buyers self-select)
Action: Increase prices gradually across all case types (+$1-2)
Expected: Maintain conversions, +4-8% revenue uplift
```

---

#### **8. SESSIONS ALLOCATION EFFICIENCY**

Detect inventory misalignment:

```
For design with 10 variants, ideal allocation:
- Sessions % should match inventory % (demand meets supply)

Example Naruto Problem:
Variant              | Session % | Inventory % | Ratio | Issue
IPH17PM-HB401       | 28%       | 5%          | 5.6x  | 🚨 CONSTRAINED (out of stock risk)
IPH17Pro-HB401      | 22%       | 8%          | 2.75x | ⚠️ Constrained
IPH17-HB6           | 18%       | 20%         | 0.9x  | ✅ Balanced
IPH16PM-HTPCR       | 12%       | 30%         | 0.4x  | 😕 Overstock

Action: Rebalance inventory (pull from IPH16PM, push to IPH17PM-HB401)
Expected: Prevent stockout, improve fulfillment efficiency
```

---

#### **9. CONVERSION ATTRIBUTION BY TRAFFIC SOURCE**

Split conversions by where traffic comes from:

```
Currently: Child ASIN report shows total conversions (no breakdown)

If Available (Amazon expanding reports):
Traffic Source | Sessions | Conversions | Conv% | Revenue
Organic Search | 300      | 24          | 8.0%  | ✅ (organic winners)
Sponsored Ads  | 150      | 12          | 8.0%  | ✅ (ads working)
A9 Recommend  | 50       | 8           | 16%   | 🎉 (halo effect!)
Brand Lookup   | 200      | 4           | 2.0%  | ❌ (low intent)

Use Case: Measure true ad ROI (organic vs paid)
Finding: A9 recommendations drive 16% conversion (halo) → prioritize overall quality
```

---

#### **10. ANOMALY DETECTION FLAGS**

Auto-alert on unusual patterns:

```
Flag Condition | Severity | Action
Conversion ↓ >1% vs week-ago | 🔴 CRITICAL | Investigate (price? review? competitor?)
Sessions ↑ >50% with no revenue | 🟠 HIGH | Traffic quality issue (misleading title?)
Revenue ↓ >30% same sessions | 🟠 HIGH | Price check (competitor undersold?)
Sessions 0 but open-date recent | 🟡 MEDIUM | Listing might be suppressed/stranded
Conversion 0 but sessions >50 | 🟡 MEDIUM | Listing quality issue (images? reviews?)

Use Case: Catch problems same week, not month later
Example: NARUTO-IPH16PM-HTPCR: sessions 400 (↑80% from prev week), revenue flat
→ Flag: "Possible misleading title or competitor price drop. Investigate."
```

---

## Data Integration: Linking Both Reports

**The Magic:** Combine Active Listings (what's live) + Child ASIN (how it's selling)

### **Integration Example 1: Identify Missing Variants**

```
Active Listings Report:
✅ Naruto listed for: iPhone 17PM, 17Pro, 17 (open-date 2026-02-15, FBA)
❌ Naruto MISSING for: iPhone 16PM, 16Pro, 16

Child ASIN Report (14-day):
- NARUTO-IPH17PM-HB401: 48 conversions, 9.6% conversion
- NARUTO-IPH17PRO-HB401: 36 conversions, 9.0% conversion
- NARUTO-IPH17-HB401: 21 conversions, 7.0% conversion
- NARUTO-IPH16PM-*: NO DATA (variant doesn't exist)

Gap Analysis:
- iPhone 17 devices: 105 conversions, 8.5% avg conversion
- iPhone 16 devices: 0 conversions (not listed)
- Opportunity: Create iPhone 16 variants (expect 7-8% conversion)
- Revenue opportunity: ~$2,000/month (assume 40 units/month × $20 × 3 variants)

Action: Create NARUTO-IPH16PM/PRO/BASE variants, all case types
Timeline: 1 week
Owner: Marketplace Ops
```

---

### **Integration Example 2: Identify Underperforming Listings**

```
Active Listings Report:
- SKU: HTPCR-IPH16PM-ONEPIECE-RED
- Status: Active ✅
- Open-date: 2025-08-10 (241 days old)
- Price: $19.95
- Fulfillment: FBM

Child ASIN Report (14-day & 30-day):
- Sessions (14d): 50
- Conversions (14d): 0
- Conversion rate: 0% ❌
- Revenue: $0

Gap Analysis:
- Listed product, zero sales for 2 weeks
- Old listing (241 days), shows age-related decay
- FBM fulfillment (slower shipping)
- Hypothesis: Poor images, bad reviews, high price, or low brand appeal

Action Options:
1. Retire variant (easiest, free up inventory slot)
2. Update listing (new images from Sven, rewrite title)
3. Move to FBA (expect 2x conversion lift)

Decision: Retire (data shows it's a dog, not worth fixing)
Timeline: Immediate
Owner: Catalog Ops
```

---

### **Integration Example 3: Identify FBA Opportunity**

```
Active Listings Report:
- SKU: HTPCR-IPH17PM-NFL-MAHOMES-RED
- Status: Active ✅
- Quantity: 150 (units in FBM warehouse)
- Fulfillment: FBM ❌ (merchant fulfillment)
- Price: $19.95

Child ASIN Report (14-day):
- Sessions: 600
- Conversions: 12
- Conversion rate: 2.0% ⚠️
- Revenue: $240

Benchmark Data (from Active Listings + Child ASIN):
- HB401 (FBA) variants: 9.6% avg conversion
- HTPCR (FBM) variants: 2.96% avg conversion
- FBA multiplier: 3.2x higher conversion

Gap Analysis:
- NFL designs are high-velocity (license is active, hot topic)
- HTPCR is limiting conversion (FBM delivery showing long times)
- Moving to FBA could lift conversion 2.96% → 9.5% (3.2x)

Opportunity Calculation:
- Current: 600 sessions × 2.0% × $20 = $240/week = $960/month
- If FBA: 600 sessions × 6.4% × $20 = $768/week = $3,072/month ⭐
- Revenue lift: +$2,112/month
- Investment: Move 150 units to FBA (inventory cost ~$1,000)
- ROI: Payback in <1 week

Action: Move to FBA immediately (constrain FBM once FBA is live)
Timeline: 2-3 weeks (inventory transfer)
Owner: Harry (FBA Planner)
Expected Impact: +$2K-3K/month revenue
```

---

## Current Workflow vs Ideal Workflow

### **Current (Manual)**
```
Timeline: 
  Fri 5 PM: Cem downloads Active Listings + Child ASIN reports → Mac Studio
  Sat 8 AM: Hermes loads into SQLite (5 minutes)
  Sat 9-11 AM: Manual pivot tables, analysis (2 hours)
  Sat 12 PM: Email recommendations (30 minutes)
  
Total Manual Effort: 5-6 hours per week
Bottleneck: File size (6GB download, slow), manual analysis
```

### **Ideal (Automated)**
```
Timeline:
  Sat 6:00 AM: Cloud Run auto-downloads reports (chunked streaming)
  Sat 6:30 AM: Auto-load → SQLite (parallel processing)
  Sat 7:00 AM: Hermes analysis cron runs:
    - Calculates all 10 suggested data points
    - Generates anomaly flags (10+ alerts)
    - Ranks variants by opportunity size
  Sat 7:30 AM: Dashboard updated (real-time)
  Sat 7:45 AM: Slack notification sent (high-level summary)
  Sat 8:00 AM: Email generated (detailed recommendations + action items)

Total Manual Effort: 30 minutes (Cem review + approval)
Bottleneck: None (fully automated)
```

---

## Recommended Data Extraction Pipeline

### **Step 1: Ingest (Chunks)**
- **Active Listings Report** → Stream in 1GB chunks → SQLite `listings_current`
- **Child ASIN Report** → Load in chunks → SQLite `child_asin_current`
- **Archive Previous** → Rotation: `listings_previous` = old `listings_current`

### **Step 2: Clean**
- Remove test listings (SKU contains "TEST")
- Remove suppressed status (optional — keep for analysis)
- Join on SKU + ASIN (link the two reports)

### **Step 3: Core Metrics**
- Conversion rate = conversions / sessions
- Revenue per session = revenue / sessions
- Velocity = (14d revenue / 30d revenue) × 100
- Device split = {browser_sessions, mobile_sessions}

### **Step 4: Suggested Metrics** (10 new data points)
1. Listing Quality Score (composite)
2. Device Coverage Ratio (per design)
3. Case Type Penetration (per design)
4. Listing Age Cohort (0-30d / 31-90d / 91-180d / 180+d)
5. ASIN Linkage Quality (validation check)
6. Suppression Root Cause (if suppressed)
7. Title Keyword Alignment (SEO check)
8. Price Tier Classification (budget / standard / premium / luxury)
9. Conversion Decile Analysis (rank by conversion %)
10. Velocity Acceleration Score (>110 = scale, <80 = pause)

### **Step 5: Generate Recommendations**
- Top 20 variants to scale (high conversion + growing)
- Top 20 variants to investigate (low conversion + high sessions)
- Top 20 missing variants (device coverage gaps)
- Top 20 underpriced variants (high RPS, raise price)
- Top 10 FBA migration candidates (FBM, high velocity, good conversion)
- Top 10 suppressed listings (investigate/retire decisions)

### **Step 6: Deliver**
- **Dashboard** (updated Sat 8 AM, real-time refresh)
- **Slack Digest** (high-level summary, action items)
- **Email to Cem** (detailed recommendations, data tables, owner assignment)

---

## Success Metrics (After Automation)

| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| **Download + load time** | 30 min (manual) | <5 min (automated) | Week 1 |
| **Analysis time** | 120 min (manual) | <5 min (automated cron) | Week 2 |
| **Data freshness** | 24h delay | <2h delay | Week 1 |
| **Variants analyzed** | ~1,000 (top designs only) | All 1,800+ variants | Week 2 |
| **Anomalies detected** | 2-3 per week (manual) | 10+ per week (automated) | Week 2 |
| **Recommendations/week** | 15-20 (email) | 50+ (dashboard + Slack) | Week 3 |
| **Review time** | 60 min per week | 30 min per week | Week 4 |
| **Revenue impact** | $0 (analysis only) | +$5-10K/month (gaps closed) | Month 2 |

---

## Implementation Phases

### **Phase 1: Data Extraction (Week 1)**
- ✅ Automate Active Listings download (chunked streaming)
- ✅ Automate Child ASIN download
- ✅ Build SQLite schema (listings + child_asin tables)
- ✅ Create core metrics (conversion rate, velocity, device split)
- 🚀 **Owner:** Codex

### **Phase 2: Suggested Metrics (Week 2)**
- ✅ Add 10 suggested data points (quality score, deciles, efficiency, etc.)
- ✅ Build anomaly detection (flags for problems)
- ✅ Create output tables (ready for dashboard)
- 🚀 **Owner:** Hermes + Codex

### **Phase 3: Automation (Week 3)**
- ✅ Wire Hermes analysis cron (Sat 7 AM)
- ✅ Build dashboard (live metrics, trends)
- ✅ Add Slack integration (auto-alert on anomalies)
- 🚀 **Owner:** Harry + Hermes

### **Phase 4: Actionable Insights (Week 4)**
- ✅ Create recommendation engine (rules-based: scale, investigate, retire)
- ✅ Link to Cem's calendar (Saturday review slot)
- ✅ Measure impact (track actions taken, revenue impact)
- 🚀 **Owner:** Ava

---

## Implementation Questions for Cem

1. **File Size Strategy:** 
   - Keep current manual download (easy but tedious)?
   - Implement chunked streaming (recommended, handles 6GB)?
   - Wait for Amazon to improve SP-API (future)?

2. **Metric Priority:** Which 3 of 10 suggested metrics are most critical?
   - Conversion Decile Analysis (understand winners)
   - Velocity Acceleration Score (identify growth)
   - Device Mix Optimization (price by device)

3. **Anomaly Thresholds:** What's the right sensitivity?
   - Flag conversion drop >0.5%? >1%? >2%?
   - Flag sessions spike >30%? >50%? >100%?

4. **Dashboard Frequency:**
   - Update real-time (better, higher cost)?
   - Update daily at 8 AM (good enough, lower cost)?

5. **Recommended Order:**
   - Phase 1 (core metrics) ASAP, then Phase 2-4 over next 4 weeks?

---

## Next Steps

1. **Cem Decision:** Approve Phase 1 (chunked streaming + core metrics)
2. **Codex Implementation:** Build Phase 1 (target: 1 week)
3. **Hermes Validation:** Test Phase 2 metrics vs manual analysis (validate accuracy)
4. **Harry Infrastructure:** Set up dashboard framework, Slack integration
5. **Deploy Phase 3-4:** Full automation by end of month

---

**Status:** Ready for implementation | **Owner:** Ava | **Last Updated:** 2026-04-10

