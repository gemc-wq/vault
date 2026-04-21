# Walmart Listing Content Audit — Task Brief
*Created: 2026-03-07 | Author: Ava | Status: Ready for agent execution*

## Objective
Audit Walmart listing quality across 95,640 active SKUs to identify content gaps hurting conversion and search ranking.

## Why This Matters
- 99.9% of SKUs have zero reviews → content quality is the ONLY conversion lever we control
- Walmart's search algorithm weights title quality, feature bullets, description, and images
- Licensed products need strong brand storytelling to justify price vs. generic cases

## Data Source
- **Supabase table:** `walmart_listings` (loading status TBD — check with Cem)
- **Alternative:** Walmart Seller Center bulk export (CSV)
- **Fallback:** Walmart API item feed

## Audit Dimensions

### 1. Title Quality (HIGH IMPACT)
- [ ] Length: Walmart recommends 50-75 chars (Amazon allows 200+)
- [ ] Format: Brand + Product Type + Key Feature + Device
- [ ] Keywords: Are search terms present?
- [ ] Consistency: Same format across product types?
- **Score:** 1-5 per SKU

### 2. Feature Bullets (HIGH IMPACT)
- [ ] Count: Walmart allows up to 5 key features
- [ ] Are all 5 slots populated?
- [ ] Quality: Benefit-driven vs. generic filler?
- [ ] Licensed brand callouts present?

### 3. Description (MEDIUM IMPACT)
- [ ] Length: 500-1000 chars recommended
- [ ] Rich content vs. copy-paste from other channel?
- [ ] Brand story / license callout present?

### 4. Images (HIGHEST IMPACT on conversion)
- [ ] Main image: White background, product-only?
- [ ] Image count: Walmart allows up to 10
- [ ] Lifestyle images present?
- [ ] Device-specific mockups showing design on phone?
- [ ] Image resolution: min 2000x2000px recommended

### 5. Category & Attributes (MEDIUM IMPACT on search)
- [ ] Correct category assignment?
- [ ] All required attributes filled? (color, material, compatible device, etc.)
- [ ] Brand attribute set correctly?

### 6. Pricing (CONTEXT)
- [ ] Price within $10-30 sweet spot?
- [ ] Competitive vs. similar listings?

## Sampling Strategy
Given 95K SKUs, full audit is impractical manually. Approach:

1. **Automated scan (Atlas):** Pull all listings, score programmatically on measurable fields (title length, bullet count, image count, description length, attribute completeness)
2. **Sample deep dive (Echo):** Manually review 50 listings across:
   - Top 10 revenue SKUs
   - 10 from each product type (HTPCR, HC, HLBWH, HB401)
   - 10 random zero-revenue SKUs
3. **Output:** Scoring spreadsheet + summary report with fix priorities

## Deliverables
1. `walmart_listing_scores.csv` — All 95K SKUs with automated scores
2. `walmart_audit_report.md` — Executive summary with:
   - Distribution of scores (how many good/ok/poor)
   - Top 10 fixable issues by volume
   - Recommended fix priorities (quick wins vs. deep rework)
   - Template for "gold standard" listing (one per product type)
3. `walmart_listing_template.md` — Copy templates for Echo to batch-produce

## Agent Assignment
| Agent | Task | Dependency |
|-------|------|-----------|
| Atlas | Automated scoring of all 95K listings | Walmart listings data in Supabase or CSV |
| Echo | Deep-dive review of 50-sample listings + template creation | Atlas scoring complete |
| Ava | Review, synthesize, present to Cem | Both complete |

## Blockers
- **Primary:** Need `walmart_listings` table loaded in Supabase (Cem mentioned "loading" on Mar 7)
- **Alternative:** Can Atlas pull from Walmart Seller Center API directly?
- **⚠️ Check:** Do we have Walmart API credentials configured?

## Success Criteria
- Score distribution mapped for all 95K SKUs
- Top 500 SKUs have actionable fix list
- Gold-standard templates ready for Echo to batch-apply
- Estimated conversion lift quantified (even rough: "fixing titles on 500 SKUs from score 2→4 = est. +15% CVR")

---
*Next step: Confirm walmart_listings data availability, then spawn Atlas for automated scoring.*
