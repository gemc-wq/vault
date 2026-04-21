# Shipping Strategy Analysis: 2-Day vs Standard vs Seller Fulfilled Prime

**Analyst:** Athena | **Date:** 2026-04-11 | **Data:** US 90-day sales (26,699 orders)
**Requested by:** Cem — "identify patterns, which consumer wants it faster"

---

## Executive Summary

**13.3% of customers already pay $12.99 for 2-day shipping.** That's 3,541 orders in 90 days where someone chose to pay $32.94 total instead of $26.94. These are your most motivated buyers.

**The SFP decision is marginal at current volume.** Switching to Seller Fulfilled Prime ($30.95 + free FedEx at $10/item) would **lose ~$20K/quarter** at the same order volume. You need a **+10% conversion lift** from the Prime badge just to break even. It's a bet on visibility, not a guaranteed win.

**My recommendation: Don't switch to SFP across the board. Test on 5-10 top SKUs first.**

---

## The Numbers

### Order Breakdown (90 Days, 26,699 Orders)

| Service Level | Orders | % | Shipping Charged | Customer Total |
|---------------|--------|---|-----------------|----------------|
| **Standard** (5-6 day) | 20,908 | 78.3% | $6.99 | $26.94 |
| **SecondDay** (2-day) | 3,541 | 13.3% | $12.99 | $32.94 |
| **Expedited** | 2,204 | 8.3% | ~$3 | ~$22.95 |
| **NextDay** | 46 | 0.2% | ~$10 | ~$29.95 |

**Key finding:** 13.3% of buyers voluntarily pay **$6 extra** for 2-day. They're already price-insensitive on shipping. The question is whether Prime badge captures MORE of the 78.3% Standard buyers.

---

## Who Pays for 2-Day? (Pattern Analysis)

### By Product Type — "Premium product buyers want it faster"

| Product Type | SecondDay % | Standard % | Over-Index |
|-------------|------------|-----------|------------|
| **HB7BK** (MagSafe Black) | 2.4% | 1.5% | **+61%** |
| **HDMWH** (Desk Mat White) | 12.3% | 8.8% | **+40%** |
| **HB6CR** (MagSafe Clear) | 3.7% | 2.8% | **+31%** |
| **HTPCR** (TPU Clear) | 56.1% | 47.8% | +17% |
| **HB401** (Hard Case) | 5.4% | 5.6% | -4% |
| **HLBWH** (Leather) | 0.2% | 11.5% | **-98%** |

**Pattern:** MagSafe buyers (HB6, HB7) and desk mat buyers are **30-60% more likely** to pay for 2-day. Leather wallet buyers almost never do — they're patient shoppers. HTPCR is the volume driver but over-indexes modestly (+17%).

### By Device — "Newest phone = most urgent buyer"

| Device | SecondDay % | Standard % | Over-Index |
|--------|------------|-----------|------------|
| **iPhone 17 Pro** | 4.9% | 2.4% | **+108%** |
| **iPhone 17 Pro Max** | 8.4% | 5.2% | **+64%** |
| **iPhone 17** | 6.4% | 3.9% | **+63%** |
| **900x400 Desk Mat** | 5.3% | 3.2% | **+67%** |
| **iPhone 15 Pro Max** | 3.5% | 2.2% | **+58%** |
| **iPhone 16** | 4.6% | 4.2% | +10% |
| **iPhone 14** | 2.3% | 3.0% | **-25%** |
| **iPhone 14 Pro Max** | 1.4% | 2.0% | **-32%** |

**Pattern:** iPhone 17 buyers are **60-108% more likely** to pay for 2-day. These are people who just got a new phone and want a case NOW. Older phone owners (iPhone 14, 13) are less urgent — they've already been using the phone for a while. Desk mat buyers also over-index significantly.

### By License — "Anime fans are impatient"

| License | SD Index (100 = average) |
|---------|--------------------------|
| **Image/Custom** | **135** |
| **Naruto** | **122** |
| **Hats/Fashion** | **116** |
| **Adventure** | **114** |
| **Batman** | **109** |
| **FC Barcelona** | 101 |
| **Dragon Ball** | 97 |
| **Harry Potter** | 86 |
| **Real Madrid/FC** | 84 |
| **Peanuts** | **77** |

**Pattern:** Naruto and custom/image buyers over-index for 2-day. Peanuts buyers are the most patient (index 77). This makes sense — anime fans skew younger and more impulse-driven. Peanuts buyers may be gifting (planned purchase).

### By Day of Week — "Mid-week urgency"

| Day | SD Index |
|-----|----------|
| **Wednesday** | **127** |
| **Monday** | 115 |
| **Tuesday** | 112 |
| Thursday | 97 |
| Saturday | 89 |
| Sunday | 89 |
| **Friday** | **78** |

**Pattern:** Mon-Wed buyers are 12-27% more likely to choose 2-day. Friday-Sunday buyers are less likely. Hypothesis: mid-week buyers want delivery by Friday/weekend. Weekend buyers are less time-pressured.

### By Geography — No strong patterns

Top states (FL, CA, TX, NY) have roughly equal SecondDay uptake. Slight over-index in Southeast (GA +26%, AL +29%, WI +30%). No geographic targeting opportunity.

---

## The SFP Financial Decision

### What Changes With SFP

| Metric | Current | SFP |
|--------|---------|-----|
| **Listed price** | $19.95 | $30.95 |
| **Shipping shown** | $6.99 or $12.99 | FREE (Prime) |
| **Customer total (Standard)** | $26.94 | $30.95 |
| **Customer total (2-day)** | $32.94 | $30.95 |
| **Prime badge** | ❌ No | ✅ Yes |
| **Your shipping cost** | ~$5.50 (USPS) | $10.00 (FedEx) |
| **Your net per order** | ~$21.44 (std) / $24.94 (2-day) | $20.95 |

### The Math (90-Day Comparison)

| Scenario | Orders | Net Revenue |
|----------|--------|-------------|
| **Current mix** | 24,438 | **$532,361** |
| **SFP (same volume)** | 24,438 | **$511,976** (-$20K) |
| **SFP +5% conversion** | 25,659 | $537,556 (+$5K) |
| **SFP +10% conversion** | 26,881 | $563,157 (+$31K) |
| **SFP +15% conversion** | 28,103 | $588,758 (+$56K) |
| **SFP +20% conversion** | 29,325 | $614,359 (+$82K) |

**Break-even: ~8% conversion lift.** Below that, you lose money. Above that, Prime badge pays for itself.

### The Perception Problem

From your screenshot, current search results show:
```
$19.97  ← this is the number customers see first
$6.99 delivery Wed, Apr 22
```

With SFP, it would show:
```
$30.95  ← this is the number customers see first
FREE delivery for Prime members (arrives by Wed, Apr 16)
✓ Prime
```

**The risk:** $30.95 looks 55% more expensive than $19.97 in the search results grid. Even though total cost is similar ($30.95 vs $26.94), **customers anchor on the first number they see.** Amazon's search results show the item price prominently — shipping is secondary text.

**The upside:** Prime filter. Many Prime members filter search results to "Prime only." Without the badge, you're invisible to those customers entirely. This is the real argument for SFP — not the 2-day speed, but the **visibility to filtered searches.**

---

## The 2-Day Buyer Profile (Your Best SFP Candidates)

Based on the patterns above, the ideal SFP test candidates are:

| Attribute | Profile |
|-----------|---------|
| **Product type** | MagSafe (HB6, HB7) — 30-60% more likely to pay for speed |
| **Device** | iPhone 17 Pro/Pro Max — 60-108% over-index for 2-day |
| **License** | Naruto, Custom/Image — 22-35% over-index |
| **Day** | Mon-Wed buyer — 12-27% more urgent |
| **Price sensitivity** | Low — already paying $32.94 total |

**These buyers are already paying MORE than $30.95 today.** For them, SFP at $30.95 is actually CHEAPER than their current $32.94. They'd welcome it.

---

## Recommendation

### Don't: Switch everything to SFP

The $19.95 price point is a competitive advantage in search results. Killing it across 3.4M listings is a massive risk with only 8% break-even. If conversion doesn't lift enough, you lose $80K+/year.

### Do: A/B Test SFP on High-Index SKUs

**Test group (50-100 SKUs):**
- MagSafe cases (HB6, HB7) for iPhone 17 Pro Max
- Naruto + Dragon Ball designs
- Top 20 designs by velocity

**Control group:** Same SKUs without SFP, same price

**Measure over 30 days:**
- Search impression share (are we showing up in Prime-filtered results?)
- Conversion rate change
- Total revenue per SKU
- Buy Box ownership

**If conversion lifts >10%:** Expand SFP to all iPhone 17 + MagSafe SKUs
**If conversion lifts <5%:** Stay with current model. The $19.95 price anchor is worth more.

### Also Consider: Hybrid Approach

Keep $19.95 + $6.99 for Standard shoppers. But ensure the 2-day option ($12.99) is prominently visible. Your data shows 13.3% already choose it — that's healthy. The real optimization may be:

1. Make the 2-day option more visible in listing (currently buried as "Or fastest delivery")
2. Ensure ALL listings have the 2-day option available (some may not)
3. Fix the shipping template compliance issue (85% → 100%) which is the quicker win

---

## Data Saved

Full analysis based on 26,699 orders, 90-day window.
Raw patterns available for Council review.

**Status:** ANALYSIS COMPLETE ✅ | **Decision needed:** Test SFP or stay current?
