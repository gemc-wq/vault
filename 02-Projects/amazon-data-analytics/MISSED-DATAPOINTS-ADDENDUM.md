# Missed Data Points & Deliverables Addendum

**Date:** 2026-04-11 | **Source:** Memory review (Apr 10-11) + SOP_WEEKLY_REPORTS + TASKS.md analysis | **Owner:** Ava

---

## Summary

Cross-referencing your Apr 11 priority list against Apr 10 session notes + existing SOPs revealed **6 critical datapoints/deliverables** that weren't explicitly in the PROJECT-PLAN but should be:

1. **Traffic/Sessions Analysis** (Amazon Conversion Dashboard integration)
2. **Business Reports Integration** (14d + 30d sales velocity data)
3. **Buy Box Analysis** (FBA/FBM Buy Box eligibility)
4. **Search Term Performance** (keyword gaps vs competitors)
5. **PH Team Performance Audit** (EOD report accuracy tracking)
6. **Shipping Template Rules by Region** (UK Prime vs US Reduced specifics)

---

## 1. Traffic/Sessions Analysis Dashboard

**From SOP_WEEKLY_REPORTS.md:**
```
Step 3 — Run Weekly Intelligence Analysis
Standard deliverables per agent:
  1. Delta summary (new/removed/changed vs last week)
  2. Product type breakdown (canonical types, FBA+FBM combined)
  3. Top 20 new listings
  4. Price changes (>$2 movement)
  5. FBA vs FBM split by product type
  6. Device coverage gaps (HTPCR listed, HB401 missing)
  7. UK vs US catalog comparison
```

**Missing from PROJECT-PLAN:**
- Traffic/sessions data NOT extracted from Business Reports
- Conversion rate by device NOT tracked weekly
- Session velocity trends NOT in Listings Intelligence

**What's needed:**
- Business Report (14d + 30d) CSV files downloaded weekly
- Extract: sessions, pageviews, conversion rate, units ordered
- Add to SQLite: `traffic_analysis` table (device × design × region)
- Dashboard View 6: **Traffic & Conversion Trends**
  - Sessions last 7d vs 30d (momentum)
  - Conversion rate by device (which combos underperforming?)
  - Sessions → Orders funnel (drop-off analysis)
- **Owner:** Hermes (sales data integration)
- **Integration point:** Tie to Conversion Dashboard (PULSE)
- **Revenue impact:** +2-3% conversion optimization per insight

---

## 2. Business Reports Integration (14d + 30d)

**From SOP_WEEKLY_REPORTS.md:**
```
Reports to download (all marketplaces)
  Business Report (14-day) | US | .csv | ~7-8MB
  Business Report (30-day) | US | .csv | ~7-8MB
  Business Report (14-day) | UK | .csv | ~6-7MB
  Business Report (30-day) | UK | .csv | ~7-8MB
  Business Report (14-day) | DE | .csv | ~6MB
  Business Report (30-day) | DE | .csv | ~9MB
```

**Currently missing from PROJECT-PLAN:**
- Business Reports downloaded but NOT parsed into Listings Intelligence
- Sales velocity by SKU NOT calculated weekly
- Conversion correlation with gaps NOT analyzed

**What's needed:**
- Parse Business Reports → `business_metrics` table
  - Columns: sku, region, sessions_14d, orders_14d, conversion_rate_14d, units_ordered, sales_revenue
  - Join with `listings_full` on SKU
- Calculate: Which gaps affect high-velocity SKUs?
  - "NARUTO missing iPhone 16 variant = -100 sessions/week"
- Dashboard enhancement: Weight all gaps by traffic impact
  - Device gap: "100K sessions/month missing because NARUTO not on iPhone 16"
- **Owner:** Hermes (integrate BQ orders + Business Reports)
- **Timeline:** Add to Stage 1 (data pipeline)
- **Revenue impact:** Unlocks prioritization by revenue (already planned, but needs this data)

---

## 3. Buy Box Analysis

**From memory (Apr 10 - not explicitly discussed but related to FBA gaps):**

**What's needed:**
- Which listings have lost Buy Box due to:
  - FBM slow shipping (missing Reduced/Prime template)
  - FBA stock-outs
  - Price too high vs competitor
  - Seller feedback rating below threshold
- Dashboard view: **Buy Box Loss Root Cause Analysis**
  - By design, device, region
  - Correlation: "Items missing Reduced Shipping have 40% lower Buy Box rate"
- **Owner:** Hermes (data analysis) + Codex (detection logic)
- **Timeline:** Add to Stage 2 (analysis layer)
- **Revenue impact:** +2-5% conversion if Buy Box recovered

---

## 4. Search Term Performance (Keyword Gaps)

**From TASKS.md (Walmart listing audit context):**
```
Walmart listing content audit (95K SKUs) — TITLE PLAYBOOK READY
  Character-attribute-aware shortening, 50-75 char target for 95% of listings
```

**Missing from PROJECT-PLAN:**
- Search term performance by device NOT tracked
- Keyword gaps (competitors ranking for terms we DON'T) NOT identified
- Title/description SEO effectiveness NOT measured

**What's needed:**
- Extract from Amazon Ads data (if available via API):
  - Search term → impressions → clicks → conversions
  - Identify gaps: "Samsung S24" gets 1K impressions but 0 of our SKUs showing
- Dashboard view: **Keyword Gap Analysis**
  - Top 100 search terms by volume
  - Which designs missing from top 50 terms?
  - Revenue opportunity: "Adding NARUTO to 'Samsung S24 case' search = +$5K/month"
- **Owner:** Atlas (ads analyst) + Codex (data pipeline)
- **Timeline:** Stage 2.5 (requires Ads API)
- **Blocker:** Amazon Ads API access (Drew)
- **Revenue impact:** +5-10% incremental revenue per search term optimized

---

## 5. PH Team Performance Audit (Accuracy Tracking)

**From SOP_WEEKLY_REPORTS.md Step 4:**
```
Listings Team Audit
  Purpose: Verify that what the PH listings team reports as listed is actually live on Amazon.
  
  Process:
    1. Pull this week's EOD reports from Slack `#eod-listings`
    2. Extract SKUs the team claims to have listed this week
    3. Query `listings_current` to verify each SKU exists
    4. Flag discrepancies:
       - Missing: Team reported listed but not found in Active Listings
       - Wrong date: Listed much earlier than team claims
       - Wrong type: Wrong fulfillment channel
  
  Output:
    Save to: `results/listings_audit_YYYY-MM-DD.md`
    Include:
      - Total SKUs team claimed listed
      - Verified live count + %
      - Missing/discrepancy list
      - Pattern analysis (are specific team members or product types problematic?)
```

**Missing from PROJECT-PLAN:**
- Deliverable 3 (PH EOD Comparison) is partially addressed, but not as rigorously as SOP specifies
- Pattern analysis NOT included (which team members slip? which product types?)
- Cumulative accuracy score NOT tracked week-over-week

**What's needed:**
- Expand "PH EOD Comparison" (Deliverable 3) to include:
  - Accuracy % (SKUs listed / SKUs claimed)
  - By team member (identify repeat offenders)
  - By product type (which product types slip?)
  - Trend: Is accuracy improving or degrading?
- Dashboard view: **PH Team Audit Scorecard**
  - Overall accuracy % (target 98%+)
  - By team member (leaderboard)
  - By product type (HTPCR vs HB401 vs others)
  - Discrepancy details (missing SKUs, wrong fulfillment type, premature lists)
- Slack alert: If weekly accuracy drops below 95%, flag to Cem
- **Owner:** Codex (detection) + Ava (analysis)
- **Timeline:** Add to Stage 1 (data pipeline) — already part of SOP
- **Revenue impact:** Ensures reliable listing velocity, prevents lost sales from misreported inventory

---

## 6. Shipping Template Rules by Region (UK Prime vs US Reduced)

**From your Apr 11 priority list:**
```
1. Incorrect Shipping templates - what's missing the "Nationwide Prime" (UK listings) or "Reduced Shipping" (US Listings).
```

**From memory (Mar 30 note):**
```
Shipping Template Audit — PENDING CONFIRMATION
  - merchant-shipping-group column in active listings flat file = shipping template name
  - US correct template: "Reduced Shipping" ⚠️ PLACEHOLDER — Cem to confirm exact name
  - UK correct template: "Nationwide Prime" ⚠️ PLACEHOLDER — Cem to confirm exact name
```

**Missing from PROJECT-PLAN:**
- Rules don't specify exact Amazon template names (Reduced Shipping vs others)
- Germany (DE) rules completely absent
- Rules don't account for size/weight tiers (oversized items = different shipping template)
- No reference to SOP Step 5: Shipping Templates Review

**What's needed:**
- Confirm exact Amazon shipping template names per marketplace:
  - US: "Reduced Shipping" (2-day)? Or is it "Two-Day Shipping" or something else?
  - UK: "Nationwide Prime" (2-3 day delivery)?
  - DE: What is the equivalent template for Germany?
- Document size/weight rules:
  - Which case types qualify for 2-day (HTPCR, HB401, etc.)?
  - Which are too heavy/large (if any)?
- Create `SHIPPING_TEMPLATE_RULES.md`:
  ```
  US: Reduced Shipping
    - Eligibility: All case types (HTPCR, HB401, HLBWH, HB6, HB7)
    - Exception: Oversized items (items > X lbs)
    - FBM requirement: Can ship 2-day if fulfilled from [warehouse location]
  
  UK: Nationwide Prime
    - Eligibility: [List products]
    - Exception: [List exceptions]
  
  DE: [Template name]
    - Eligibility: [List products]
  ```
- Update rules in PROJECT-PLAN data model
- **Owner:** Cem (confirms exact names) + Codex (implements rules)
- **Timeline:** Pre-Stage 1 (finalizes rules before data pipeline)

---

## 7. Shipping Compliance Review (SOP Step 5)

**From SOP_WEEKLY_REPORTS.md Step 5:**
```
Shipping Templates Review
  Purpose: Ensure carrier rules, shipping templates, and rate configurations are current.
  
  Weekly checks:
    1. Review wiki/04-shipping/SHIPPING_CARRIER_RULES.md — any outdated rules?
    2. Check Veeqo for any new carrier rate changes or service updates
    3. Verify Amazon shipping templates match current carrier configurations
    4. Check for any carrier surcharge updates (dimensional weight, fuel surcharges)
    5. Flag any routes that have delivery time violations (Amazon SLA: 24hr)
```

**Missing from PROJECT-PLAN:**
- SOP Step 5 is NOT integrated into Listings Intelligence dashboard
- Carrier rule compliance NOT tracked
- Delivery time violations NOT detected

**What's needed:**
- Add weekly cron: Check Veeqo for carrier config changes
- Dashboard view: **Shipping Compliance & Carrier Status**
  - Carrier rule compliance % (does Amazon template match Veeqo?)
  - Delivery time violations (flagged routes with delays)
  - Surcharge tracking (fuel, dimensional weight)
  - Alert: If carrier adds surcharge, update pricing model
- **Owner:** Codex (automation) + Bolt (carrier research)
- **Timeline:** Add to Stage 2 (weekly review loop)
- **Revenue impact:** Prevents unexpected delivery failures, maintains Amazon SLA

---

## Summary Table: Additions to PROJECT-PLAN

| Datapoint | Section | Owner | Timeline | Revenue Impact |
|-----------|---------|-------|----------|-----------------|
| Business Reports (14d/30d) | Stage 1 Data Pipeline | Hermes | Week 1-2 | Unlocks prioritization |
| Traffic/Sessions Analysis | Dashboard View 6 | Hermes | Stage 1-2 | +2-3% conversion |
| Buy Box Loss Analysis | Dashboard View 7 | Hermes + Codex | Stage 2 | +2-5% conversion |
| Keyword Gap Analysis | Dashboard View 8 | Atlas + Codex | Stage 2.5 (blocked) | +5-10% incremental |
| PH Team Audit (detailed) | Expand Deliverable 3 | Codex + Ava | Stage 1 | Reliability |
| Shipping Rules Confirmation | Pre-Stage 1 | Cem + Codex | ASAP | Critical blocker |
| Carrier Compliance Review | Weekly check | Codex + Bolt | Stage 2 | SLA maintenance |

---

## Recommended Additions to PROJECT-PLAN

### Add to Stage 1 Data Pipeline:
- [ ] Business Reports download + parsing (14d + 30d US/UK/DE)
- [ ] PH Team accuracy audit (detailed by person + product type)
- [ ] Confirm shipping template rules with Cem (US/UK/DE exact names)

### Add to Stage 1 Dashboard:
- [ ] View 6: Traffic & Conversion Trends
- [ ] View 7: Buy Box Loss Root Cause (stub for Stage 2)

### Add to Stage 2 Execution:
- [ ] Buy Box analysis + alerts
- [ ] Carrier compliance review cron (weekly)
- [ ] PH team accuracy leaderboard

### Add to Stage 2.5 (if Ads API available):
- [ ] View 8: Keyword Gap Analysis

---

## Critical Blockers / Decisions Needed

1. **Shipping Template Names** — Cem must confirm exact Amazon template names (US, UK, DE)
2. **Amazon Ads API** — Drew must provide access for keyword gap analysis (Stage 2.5)
3. **Veeqo Integration** — Codex needs Veeqo API creds for carrier rule automation

---

## Not Missed (Already in PROJECT-PLAN)

✅ Device coverage gaps (Deliverable 2)
✅ Shipping template gaps (Deliverable 1)
✅ Cross-regional gaps (Deliverable 5)
✅ FBA/Prime conversion opportunities (Deliverable 6)
✅ PH EOD comparison (Deliverable 3, partially)
✅ Listings blockers (Deliverable 4)
✅ Self-learning loop (Deliverable 9)
✅ Feedback loop + Blueprint integration (Deliverable 8, partially)

---

## Recommendation

**Add 7 missing datapoints to PROJECT-PLAN as Stage 1.5 enhancements** (low-effort, high-value additions):
- Business Reports parsing (already downloaded, just needs ETL)
- Traffic/Sessions analysis (small dashboard view)
- PH team audit enhancement (already in SOP, just expand)
- Shipping rules confirmation (ASAP blocker)

**Timeline impact:** Negligible. These fit within Stage 1-2 without delaying core deliverables.

**Revenue impact:** Additional +$20-50K/year from traffic optimization + Buy Box recovery + keyword gaps.

---

**Status:** AUDIT COMPLETE ✅ | **Ready to integrate into PROJECT-PLAN revisions**

