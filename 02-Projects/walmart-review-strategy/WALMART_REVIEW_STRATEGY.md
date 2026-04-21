# Walmart Review Strategy — Ecell Global
*Draft: 2026-03-07 | Author: Ava | Status: VALIDATED 2026-03-08 (web research complete)*

## Problem
- 95,640 active Walmart SKUs
- 99.9% have ZERO reviews
- Zero reviews = low conversion, low search rank, no social proof
- Phone cases are impulse/trust purchases — reviews matter enormously

## Walmart's Review Ecosystem (Key Differences from Amazon)

### 1. Reviews Are ITEM-Level, Not Seller-Level
- Unlike Amazon where reviews attach to the ASIN (shared across sellers), Walmart reviews attach to the **item page**
- If you're the only seller for an item, you own all reviews
- Licensed phone cases = almost certainly sole seller → reviews are YOURS

### 2. Walmart Review Syndication (Bazaarvoice)
- Walmart uses **Bazaarvoice** for review infrastructure
- Reviews from your own DTC site (goheadcase.com / headcasedesigns.com) can potentially **syndicate to Walmart** if both use Bazaarvoice
- **⚠️ VALIDATE:** Check if Bazaarvoice syndication is available for 3P marketplace sellers or only 1P/DSV suppliers
- This could be the single biggest unlock — existing reviews from other channels flowing to Walmart listings

### 3. Walmart Post-Purchase Reviews (Review Accelerator) ✅ VALIDATED
- Program now called **Post-Purchase Reviews** (under Growth → Review Accelerator in Seller Center)
- Sellers enroll eligible items; after purchase, customer is offered a digital reward for feedback
- **Cost structure (confirmed March 2026):**
  - **$5 service fee** per review (Walmart's cut)
  - **Incentive amount:** $5 minimum, max = lesser of 25% of item price or $25
  - **Total cost per review: $10–$30** depending on item price and incentive chosen
- **Target reviews:** 5–20 per item (you choose)
- **Eligibility:** Open to marketplace sellers ✅ — eligible items refreshed weekly (Wednesdays)
- **Key constraint:** Only ONE seller can enroll a given item at a time (first-mover advantage for sole-seller items like ours)
- **Variants are enrolled individually** — each variant is a separate enrollment
- **Auto-unenroll:** Items removed once target reviews reached; customers can still submit up to 48h after
- At 95K SKUs, can't do all — need to be surgical (top 200-500 SKUs only)

### 4. No Post-Purchase Email Automation (Unlike Amazon) ✅ VALIDATED
- Walmart does NOT allow sellers to email buyers directly
- No equivalent to Amazon's "Request a Review" button
- **The Post-Purchase Reviews program IS Walmart's mechanism** — it handles the ask automatically after purchase
- No separate seller-initiated review request feature exists as of March 2026

---

## Recommended Strategy (Tiered)

### Tier 1: Post-Purchase Reviews (Top 200 SKUs) — REVISED COST ✅
**What:** Enroll top-selling/highest-potential SKUs in Post-Purchase Reviews program
**Why:** Fastest path to reviews on hero products; Walmart handles the ask post-purchase
**Cost (validated):**
- 200 SKUs × 5 reviews each × ($5 service fee + $5 min incentive) = **$10,000** at minimum incentive
- 200 SKUs × 5 reviews each × ($5 + $10 incentive) = **$15,000** at mid incentive
- **Recommended: Start with $5 incentive on 100 SKUs = $5,000 for 500 reviews**
**ROI:** Even 3-5 reviews per listing can increase conversion 15-30%
**Selection criteria:**
- Top revenue designs from PIE analysis
- iPhone 16/Galaxy S25 (current gen devices)
- Products with best margins (HTPCR, HC types)
- **Sole-seller items prioritized** (we lock out competitors from enrolling)

### Tier 2: Bazaarvoice Syndication Investigation — REVISED ✅
**What:** Syndicate existing DTC reviews to Walmart via Bazaarvoice network
**Why:** Reviews at scale if eligible — Walmart IS in the Bazaarvoice network (2,300+ retailers)
**Reality check (validated):**
- Bazaarvoice syndication is a **paid enterprise SaaS product** — not free
- Requires Ecell to become a Bazaarvoice client (brand subscription)
- Walmart is in the network, so syndication IS technically possible
- BUT: Cost likely $10K-50K+/year for a Bazaarvoice contract (enterprise pricing, needs quote)
- ROI only makes sense if DTC site (goheadcase.com) already has significant review volume
**Action items:**
1. Check if BigCommerce store already uses Bazaarvoice (or compatible review platform)
2. Assess current DTC review volume — if low, syndication won't help regardless
3. Request Bazaarvoice pricing quote only if DTC review volume justifies it
4. **Deprioritized vs. Tier 1** — Post-Purchase Reviews is faster and cheaper to start

### Tier 3: Insert Cards (Compliant) — Low cost, high effort
**What:** Include review request cards in Walmart shipments
**Why:** Direct ask to buyers post-delivery
**Rules:**
- ✅ CAN ask for honest review with QR code to Walmart product page
- ❌ CANNOT offer incentive/discount for reviews (Walmart TOS violation)
- ❌ CANNOT direct to non-Walmart site
- **⚠️ VALIDATE:** Confirm Walmart's current policy on review request inserts for FBM sellers

### Tier 4: Walmart Connect Ads → Review Velocity — Ongoing
**What:** Run Walmart Connect (PPC) on review-targeted SKUs to drive volume
**Why:** More sales = more organic review opportunities
**Logic:** If 1-3% of buyers leave reviews, need 100-300 sales per SKU for first few reviews
**Budget:** Start $500-1K/month on top 50 SKUs
**Synergy:** Pair with Tier 1 — ads drive volume, accelerator seeds initial reviews

### Tier 5: Product Bundling / Variation Consolidation
**What:** Consolidate color/design variations under parent items where possible
**Why:** Reviews aggregate at parent level = fewer but better-reviewed listings
**Risk:** May not apply well to licensed designs (each design is unique)
**✅ VALIDATED (Mar 9):** Walmart variation grouping rules:
- Up to 49 items per group via Catalog UI, 500+ via bulk template
- Items must share same product type category
- Group by up to 3 attributes (color, size, etc.)
- Primary variant controls which item shows in search
- **For phone cases:** Could group same-design across device variants (e.g., "NBA Lakers HB401" in iPhone 16/Pro/Pro Max = 1 group)
- **Limitation:** Different designs are NOT variants — each unique design is a separate listing
- **Net impact: LOW for review consolidation** — our SKU explosion is design × device, not color variants. Each design is unique art, so grouping won't collapse 95K into fewer reviewed listings. Tier 5 stays P2.

---

## Priority Matrix

| Tier | Impact | Cost | Effort | Timeline | Priority |
|------|--------|------|--------|----------|----------|
| T1: Post-Purchase Reviews | HIGH | $5-15K | LOW | 2-4 weeks | 🔴 P0 |
| T2: Bazaarvoice Syndication | MEDIUM | $10K+/yr | HIGH | 8-12 weeks | 🟢 P2 (deprioritized) |
| T3: Insert Cards | MEDIUM | ~$500 | MEDIUM | 2 weeks | 🟡 P1 |
| T4: Walmart Connect | MEDIUM | $500+/mo | LOW | Ongoing | 🟡 P1 |
| T5: Variation Consolidation | LOW-MED | $0 | HIGH | 4+ weeks | 🟢 P2 |

## Immediate Next Steps
1. **Cem/Harry:** Go to Seller Center → Growth → Review Accelerator → Post-Purchase Reviews — check eligible items list
2. **Atlas:** Identify top 100-200 Walmart SKUs by revenue potential (cross-reference PIE design rankings)
3. **Ava:** Build enrollment priority spreadsheet (design × device × margin) once Atlas delivers SKU list
4. **Echo:** Draft compliant insert card copy (if Tier 3 approved)
5. **Deferred:** Bazaarvoice investigation only after DTC review volume assessed

## Key Metrics to Track
- Reviews per SKU (target: 5+ on hero SKUs within 60 days)
- Conversion rate before/after reviews (Walmart Seller Center analytics)
- Review Accelerator ROI (cost per review vs. incremental revenue)
- Organic review rate (reviews ÷ units sold)

---

## Risks & Watchouts
- **Walmart TOS changes:** Review policies evolve — check quarterly
- **Licensed product nuance:** Review Accelerator may require sending physical product — need to ensure licensed items can be sampled
- **Scale reality:** 95K SKUs will NEVER all have reviews — focus on top 500-1000, let long tail be zero
- **Competitor intel:** Check if Casetify/OtterBox have reviews on their Walmart listings (benchmark)

---

*✅ Validated 2026-03-08 via web research (Walmart Marketplace docs, Bazaarvoice site).*
*Key correction: Bazaarvoice syndication downgraded from P0 to P2 — it's enterprise SaaS, not free.*
*Review Accelerator costs confirmed higher than initial estimate ($10-30/review vs. $10-15).*
*Next review: After Cem checks eligible items in Seller Center.*
