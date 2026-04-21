# AutoResearch Pricing Optimizer — Project Spec

> **Owner:** Ava | **Created:** 2026-03-21 | **Status:** Spec
> **Inspired by:** Karpathy's AutoResearch + Claude Code autonomous loop
> **SaaS candidate:** ✅ Generalizable to any marketplace seller

---

## Concept

An autonomous AI agent that experiments with pricing to maximize revenue per session. It follows the AutoResearch pattern: hypothesize → test → measure → keep/revert → repeat.

**Two requirements met (from video):**
1. ✅ **Objective metric** — Conversion rate (measurable, unambiguous)
2. ✅ **API to modify inputs** — Walmart API (price update), Amazon SP-API (once roles added)

---

## The Loop

```
┌─────────────────────────────────────────────────────┐
│  1. IDENTIFY — Pull conversion data weekly          │
│     Source: Amazon Business Reports (sessions/conv)  │
│     Classify each ASIN into quadrant:               │
│     ⭐ Star | ❓ Q-Mark | 🐄 Cash Cow | 🐕 Dog      │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  2. HYPOTHESIZE — Generate price test               │
│     Stars: "Test $21.95 (+$2) — will conv hold?"    │
│     Q-Marks: "Test $17.95 (-$2) — will conv lift?"  │
│     Log hypothesis to resource.md                    │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  3. DEPLOY — Change price via API                   │
│     Walmart: POST /v3/feeds (price update feed)     │
│     Amazon: SP-API pricing endpoint                 │
│     Max 20 SKUs per test cycle                      │
│     Record: SKU, old price, new price, test start   │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  4. WAIT — 14-day attribution window                │
│     Amazon needs 14 days for reliable conversion    │
│     Walmart similar (7-14 day stabilization)        │
│     No touching test SKUs during window             │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  5. MEASURE — Pull fresh conversion data            │
│     Compare: test period conv vs baseline conv      │
│     Calculate: revenue impact (conv × margin)       │
│     Statistical significance check (min sessions)   │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  6. DECIDE — Keep or revert                         │
│     If conv lift > margin loss → KEEP new price     │
│     If conv unchanged but margin down → REVERT      │
│     If conv dropped → REVERT immediately            │
│     Log result to learnings database                │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  7. LEARN — Update resource.md with findings        │
│     "Peanuts designs are price-sensitive below $18" │
│     "Football clubs accept premium pricing > $22"   │
│     Feed learnings into next hypothesis             │
│     → REPEAT from Step 1                            │
└─────────────────────────────────────────────────────┘
```

---

## Test Strategies

### Strategy 1: Price Reduction on Question Marks
**Candidates:** 13 designs with high sessions + below-avg conversion

| Design | Sessions | Current Conv | Current Price | Test Price | Expected Outcome |
|---|---|---|---|---|---|
| PNUTSNF-CLA | 3,396 | 1.7% | $19.95 | $17.95 | Conv lift to 2.5%+ |
| RMORGRA-TSP | 3,840 | 2.2% | $19.95 | $17.95 | Conv lift to 3.0%+ |
| PNUTCHA-SNO | 3,427 | 2.8% | $19.95 | $17.95 | Conv lift to 3.5%+ |
| HPOTGRA-MAR | 1,774 | 2.8% | $19.95 | $17.95 | Conv lift to 3.5%+ |

**Break-even math:**
- Current: 3,396 sessions × 1.7% conv × $19.95 = $1,152/month
- Test: 3,396 sessions × 2.5% conv × $17.95 = $1,524/month → **+32% revenue**
- Even a small conversion lift at lower price can increase total revenue

### Strategy 2: Price Increase on Stars
**Candidates:** 30 designs with high sessions + above-avg conversion

| Design | Sessions | Current Conv | Current Price | Test Price | Risk |
|---|---|---|---|---|---|
| DRGBSUSC-GOK | 4,612 | 4.6% | $19.95 | $21.95 | Low — strong demand |
| NARUICO-AKA | 4,098 | 4.1% | $19.95 | $21.95 | Low — fan loyalty |
| FCBCKT8-AWY | 1,768 | 6.3% | $19.95 | $22.95 | Low — 2x avg conv |

**Break-even math:**
- Current: 4,612 sessions × 4.6% conv × $19.95 = $4,233/month
- Test: 4,612 sessions × 3.8% conv × $21.95 = $3,843/month → needs conv to hold above 3.8%
- At 4.0% conv: $4,051 → still profitable
- If conv holds at 4.6%: $4,661 → **+10% revenue increase for free**

### Strategy 3: Free Shipping Test
**Hypothesis:** $24.95 with free shipping converts better than $19.95 + $6.99 shipping ($26.94 total)

| Current | Test | Customer Pays | Margin Impact |
|---|---|---|---|
| $19.95 + $6.99 shipping | $24.95 + FREE shipping | -$1.99 less | Absorb shipping cost |

**Target:** 20 high-session Q-Mark SKUs
**Metric:** Conversion rate change
**Duration:** 14 days

### Strategy 4: Device-Specific Pricing
**Hypothesis:** Newer devices (iPhone 17) command premium over older (iPhone 12)

| Device | Avg Conv | Current Price | Test Price |
|---|---|---|---|
| iPhone 17 Pro Max | 3.7% | $19.95 | $21.95 |
| iPhone 17 Pro | 5.6% | $19.95 | $22.95 |
| iPhone 12 | 2.6% | $19.95 | $17.95 |
| iPhone 7 | 1.7% | $19.95 | $15.95 |

---

## Guardrails

| Rule | Detail |
|---|---|
| **Price floor** | Never below COGS + royalty = ~$8-10/unit |
| **Price ceiling** | Never above $29.95 (category expectation) |
| **Test size** | Max 20 SKUs per cycle (statistical significance) |
| **Duration** | Minimum 14 days per test (Amazon attribution window) |
| **Revert trigger** | If conversion drops >30% from baseline in first 7 days |
| **No double-testing** | Each SKU only in one test at a time |
| **Revenue floor** | Never test on SKU with <50 sessions/week (not enough data) |
| **License sensitivity** | Licensed products may have MAP (minimum advertised price) — check per license |

---

## Data Architecture

### Supabase Tables

```sql
CREATE TABLE pricing_experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_name TEXT NOT NULL,
    strategy TEXT NOT NULL, -- 'price_reduction', 'price_increase', 'free_shipping', 'device_pricing'
    status TEXT DEFAULT 'planned', -- planned, active, measuring, completed, reverted
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE pricing_test_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id UUID REFERENCES pricing_experiments(id),
    sku TEXT NOT NULL,
    asin TEXT,
    marketplace TEXT DEFAULT 'amazon_us',
    baseline_price DECIMAL NOT NULL,
    test_price DECIMAL NOT NULL,
    baseline_conversion DECIMAL, -- 30d pre-test avg
    baseline_sessions INTEGER,
    test_conversion DECIMAL, -- measured after 14d
    test_sessions INTEGER,
    result TEXT, -- 'winner', 'neutral', 'loser'
    revenue_impact DECIMAL,
    final_price DECIMAL, -- kept test price or reverted
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE pricing_learnings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id UUID REFERENCES pricing_experiments(id),
    learning TEXT NOT NULL, -- e.g., "Peanuts designs are price-sensitive below $18"
    confidence TEXT, -- 'high', 'medium', 'low'
    applicable_to TEXT, -- 'license:Peanuts', 'device:IPH12', 'product_type:HTPCR'
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Resource.md (AutoResearch Pattern)
```markdown
# Pricing Learnings

## Cycle 1 (Mar 28 - Apr 11)
- PNUTSNF-CLA: $19.95→$17.95 | Conv 1.7%→2.9% | WINNER — keep $17.95
- DRGBSUSC-GOK: $19.95→$21.95 | Conv 4.6%→4.2% | NEUTRAL — keep $21.95 (margin gain)
- Learning: "Peanuts MagSafe fans are price-sensitive. Anime fans accept premium."

## Cycle 2 (Apr 14 - Apr 28)
- ...
```

---

## Implementation Timeline

| Week | Task |
|---|---|
| 1 | Build Supabase schema + baseline data loader |
| 2 | Build experiment manager (create/track/measure tests) |
| 3 | Connect Amazon SP-API for automated price changes (need Reporting role first) |
| 4 | First test cycle: 10 Q-Mark SKUs at $17.95, 10 Stars at $21.95 |
| 6 | Measure results, log learnings, generate Cycle 2 |
| 8 | Add Walmart API pricing (already connected) |
| 12 | Fully autonomous — agent runs tests without human intervention |

---

## Success Metrics

| Metric | Baseline | Target (90 days) |
|---|---|---|
| Revenue per session | $0.65 | >$0.80 |
| Overall conversion | 2.89% | >3.5% |
| Q-Mark conversion | 2.2% avg | >3.0% avg |
| Star margin | $19.95 | $21.50 avg (blended) |
| Experiments completed | 0 | 6 cycles |
| Learnings logged | 0 | 20+ insights |

---

## SaaS Product Angle

This becomes: **"AutoPrice — AI-Powered Marketplace Pricing Optimizer"**
- Input: Amazon Business Reports (or API)
- Output: Weekly pricing recommendations + autonomous testing
- Value prop: "Increase revenue 10-20% without additional traffic"
- Target: Any Amazon/Walmart seller with >1,000 SKUs
- Pricing: $99-499/month based on SKU count
- Differentiation: Uses actual conversion data, not just competitor scraping

---

*Connects to: Conversion Baselines (wiki/25-pulse-dashboard/CONVERSION_BASELINES.md), Listings Management System Spec, Master Architecture (MEMORY.md), AutoResearch takeaways (research/claude-code-autoresearch-takeaways.md)*
