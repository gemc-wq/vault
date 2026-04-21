# SOP: Weekly Movers & Sales Traffic Analysis + Karpathy Loop Price Changes
**For Hermes Agent (GLM 5.1, Nous Research)**

**Effective:** 2026-04-13  
**Owner:** Hermes (GLM 5.1)  
**Execution:** Saturdays 3:00–4:30 AM ET + Monday 5:00 AM  
**Handoff from:** PULSE Leaderboard analysis (part of existing weekly cron infrastructure)  
**New addition:** Karpathy loop implementation for price optimization (small SKU cohorts)

---

## Overview

This SOP defines the **movers & shakers analysis** (top performers, rising stars, watch-list designs) combined with **sales traffic pattern analysis** (weekly CVR, AOV, traffic by device) plus the **Karpathy loop price optimization** process for small SKU cohorts.

**Core Objective:** Identify high-momentum designs, understand traffic patterns, and autonomously optimize prices on small test cohorts to maximize revenue.

---

## Part 1: Weekly PULSE Leaderboard (Monday 5:00 AM)

### Current Status
✅ **Already running** (Cron #10 in ACTIVE_CRONS.md)  
**Agent:** Hermes (reassigned from main, using openai-codex/gpt-5.4)  
**Duration:** 2–3 minutes  
**Output:** Top devices, top designs, movers + 1 Telegram summary

### What the Leaderboard Generates

```python
# PULSE Leaderboard queries:

1. TOP 10 DEVICES (US, HTPCR, 6-month)
   - iPhone 17 Pro Max: $52,000 revenue, 89% market share
   - iPhone 17: $48,000, 87%
   - iPhone 16: $28,000, 64%
   
2. TOP 20 DESIGNS (US, HTPCR, 6-month)
   - NARUICO: $156,000 revenue, 245 SKUs
   - DRGBSUSC: $142,000, 198 SKUs
   - ONEPIECE: $138,000, 187 SKUs
   
3. TOP 20 CHAMPIONS (child designs, highest velocity)
   - NARUICO_AKA: $89,000 (Akatsuki version)
   - DRGBSUSC_VEGETA: $76,000 (Vegeta design)
   - ONEPIECE_LUFFY: $68,000
   
4. TOP MOVERS (30d vs 90d acceleration)
   - ↗️ NEWLICENSE: +340% velocity (new license, high growth)
   - ↗️ ANIMEPOP_V2: +210% velocity (redesign version)
   - ↘️ NFL_LEGACY: -95% velocity (expired license, sell-off)
   
5. CROSS-REGION GAPS
   - NARUICO: US $156K, UK $32K, DE $18K
   - Gap: Only 20% of US revenue in UK/DE combined
   - Recommendation: Expand NARUICO to EU variants
```

### Output Format (Telegram to Cem)

```
📊 **Weekly PULSE Leaderboard — Apr 21, 2026**

🏆 Top Device: iPhone 17 Pro Max (+$52K, 89%)
🎨 Top Design: NARUICO (+$156K, 245 SKUs)
⭐ Rising Star: NEWLICENSE (+340% velocity)
📉 Watch List: NFL_LEGACY (-95%, expire Jun 29)

Top movers: 6 up, 3 down, 11 stable
Region gaps: NARUICO 80% upside in UK/DE

See full report: results/weekly_pulse_leaderboard_2026-04-21.md
```

---

## Part 2: Weekly Sales Traffic Analysis (Saturday 3:00–3:30 AM)

### New Task (First Run: Apr 19, 2026)

You'll create this analysis by querying the sales data + calculating traffic patterns.

### What to Analyze

#### 2.1: Conversion Rate by Product Type

```python
# Query: Supabase orders + impressions (from Amazon/Walmart APIs)

cvr_by_type = {
    'HTPCR': {
        'orders': 4250,
        'impressions': 142000,
        'cvr': 2.99%,
        'trend': '+0.15% vs last week',
        'aov': '$19.95'
    },
    'HB401': {
        'orders': 1890,
        'impressions': 76000,
        'cvr': 2.48%,
        'trend': '+0.22% vs last week',
        'aov': '$19.95'
    },
    'HLBWH': {
        'orders': 612,
        'impressions': 18000,
        'cvr': 3.40%,
        'trend': '-0.08% vs last week',
        'aov': '$24.95'
    },
    'HB6': {
        'orders': 548,
        'impressions': 16000,
        'cvr': 3.42%,
        'trend': '+0.45% vs last week',
        'aov': '$24.95'
    },
    'HB7': {
        'orders': 501,
        'impressions': 14000,
        'cvr': 3.57%,
        'trend': '+0.33% vs last week',
        'aov': '$24.95'
    }
}
```

**Query (Supabase):**
```sql
SELECT 
  product_type,
  COUNT(DISTINCT order_id) as orders,
  SUM(impressions) as impressions,
  ROUND(100.0 * COUNT(DISTINCT order_id) / SUM(impressions), 2) as cvr,
  AVG(order_value) as aov,
  marketplace,
  device_family
FROM orders o
LEFT JOIN impressions i ON o.design_code = i.design_code
WHERE o.paid_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY product_type, marketplace
ORDER BY orders DESC;
```

#### 2.2: Traffic by Device Family

```python
# Which devices drive the most traffic?

traffic_by_device = {
    'iPhone 17 Pro Max': {
        'orders': 1456,
        'impressions': 38000,
        'cvr': 3.83%,
        'aov': '$22.15'
    },
    'iPhone 17': {
        'orders': 1389,
        'impressions': 36000,
        'cvr': 3.86%,
        'aov': '$21.88'
    },
    'iPhone 16': {
        'orders': 892,
        'impressions': 28000,
        'cvr': 3.18%,
        'aov': '$20.12'
    },
    'Samsung Galaxy A55': {
        'orders': 412,
        'impressions': 15000,
        'cvr': 2.75%,
        'aov': '$18.95'
    },
    'Google Pixel 9 Pro': {
        'orders': 389,
        'impressions': 14000,
        'cvr': 2.78%,
        'aov': '$19.45'
    }
}
```

#### 2.3: Top Performers by Marketplace

```python
# Revenue + CVR by Amazon region

amazon_performance = {
    'US': {
        'revenue': '$142,500',
        'orders': 4800,
        'impressions': 142000,
        'cvr': 3.38%,
        'top_design': 'NARUICO',
        'top_device': 'iPhone 17 Pro Max'
    },
    'UK': {
        'revenue': '$28,900',
        'orders': 980,
        'impressions': 31000,
        'cvr': 3.16%,
        'top_design': 'NARUICO',
        'top_device': 'iPhone 17'
    },
    'DE': {
        'revenue': '$19,200',
        'orders': 650,
        'impressions': 18000,
        'cvr': 3.61%,
        'top_design': 'DRGBSUSC',
        'top_device': 'iPhone 17 Pro Max'
    }
}
```

#### 2.4: Weekly Traffic Trends

```python
# Week-over-week changes

trends = {
    'Total Orders': {
        'this_week': 6430,
        'last_week': 6180,
        'change': '+4.0%',
        'trajectory': '↗️ Accelerating'
    },
    'Overall CVR': {
        'this_week': 3.42%,
        'last_week': 3.36%,
        'change': '+0.06%',
        'trajectory': '↗️ Stable improvement'
    },
    'AOV': {
        'this_week': '$21.15',
        'last_week': '$20.98',
        'change': '+0.81%',
        'trajectory': '↗️ Slight increase'
    },
    'Impressions': {
        'this_week': 187600,
        'last_week': 184000,
        'change': '+1.96%',
        'trajectory': '→ Flat'
    }
}
```

### Output Format (Markdown Report)

```markdown
# Weekly Sales Traffic Analysis — Apr 19, 2026

## Summary
- **Orders:** 6,430 (+4.0% vs last week) ✨
- **CVR:** 3.42% (+0.06% vs last week) ↗️
- **Revenue:** $190,600 (+4.2% vs last week) 📈
- **AOV:** $21.15 (+0.81% vs last week) ↗️

## By Product Type
| Type | Orders | CVR | AOV | Trend |
|------|--------|-----|-----|-------|
| HTPCR | 4,250 | 2.99% | $19.95 | +0.15% ↗️ |
| HB401 | 1,890 | 2.48% | $19.95 | +0.22% ↗️ |
| HLBWH | 612 | 3.40% | $24.95 | -0.08% ↘️ |
| HB6 | 548 | 3.42% | $24.95 | +0.45% ↗️ |
| HB7 | 501 | 3.57% | $24.95 | +0.33% ↗️ |

## Top Devices
1. iPhone 17 Pro Max: 3.83% CVR, +$32.1K
2. iPhone 17: 3.86% CVR, +$29.8K
3. iPhone 16: 3.18% CVR, +$17.9K

## By Region
- US: $142.5K (75% of revenue), 3.38% CVR
- UK: $28.9K (15%), 3.16% CVR
- DE: $19.2K (10%), 3.61% CVR

## Insights
- iPhone 17 Pro Max dominates (22.6% of orders)
- HB7 highest CVR (3.57%), premium pricing working
- HTPCR highest volume (66% of orders), steady growth
```

### Telegram Summary (Saturday 3:30 AM)

```
📊 **Weekly Sales Traffic Analysis — Apr 19, 2026**

**Orders:** 6,430 (+4.0%) | **CVR:** 3.42% (+0.06%) | **Revenue:** $190,600 (+4.2%)

🏆 Top Device: iPhone 17 Pro Max (3.83% CVR, $32.1K revenue)
📱 Top Type: HTPCR (4,250 orders, 66% of total)
🌍 Top Region: US ($142.5K, 75% of revenue)

⭐ Insights:
- Premium cases (HB7: 3.57% CVR) outperforming budget
- iPhone 17 series = 87% of traffic
- DE showing higher CVR (3.61%) — test EU expansion?

Full report: results/weekly_sales_traffic_2026-04-19.md
```

---

## Part 3: Karpathy Loop Price Optimization (New Feature)

### What is Karpathy Loop?

The **Karpathy Loop** is an autonomous optimization process where Hermes:

1. **Observes** — Real-time price → conversion feedback
2. **Hypothesizes** — "What if we lower/raise price for this cohort?"
3. **Experiments** — Small price change on 50–100 SKU cohort
4. **Learns** — Measures CVR change, AOV impact, revenue outcome
5. **Adjusts** — Applies winning price to broader catalog
6. **Repeats** — Continuous improvement cycle

**Key constraint:** Only test on **small cohorts** (50–100 SKUs, 1 design × multiple devices).

---

### Step 1: Identify Candidate Cohorts (Saturday 3:30–4:00 AM)

```python
# Query: Designs with stable performance + price inelasticity signals

candidates = {}

for design in top_designs:
    if design.revenue_7d > $10000 and design.order_count_7d > 100:
        # Stable performers worth testing
        
        # Calculate price elasticity proxy
        # (Does demand change when we change price?)
        elasticity = calculate_elasticity(design, lookback=30d)
        
        # If elasticity is LOW → price is inelastic → we can raise price
        if elasticity < 0.3:  # inelastic (demand doesn't drop much)
            candidates.append({
                'design': design.code,
                'current_price': design.price,
                'revenue_7d': design.revenue_7d,
                'cvr': design.cvr,
                'elasticity': elasticity,
                'recommendation': 'RAISE (inelastic demand)'
            })
        
        # If elasticity is HIGH → price is elastic → lower price to increase volume
        elif elasticity > 1.2:
            candidates.append({
                'design': design.code,
                'current_price': design.price,
                'revenue_7d': design.revenue_7d,
                'cvr': design.cvr,
                'elasticity': elasticity,
                'recommendation': 'LOWER (elastic demand)'
            })

# Select top 3 candidates for testing
top_candidates = sorted(candidates, key=lambda x: x['revenue_7d'], reverse=True)[:3]
```

**Example candidates:**

```
1. NARUICO (Inelastic)
   - Current price: $19.95
   - Revenue (7d): $12,400
   - CVR: 3.12%
   - Elasticity: 0.24 (very inelastic)
   - Recommendation: RAISE to $21.95 (+10% price)

2. DRGBSUSC (Elastic)
   - Current price: $19.95
   - Revenue (7d): $11,200
   - CVR: 2.89%
   - Elasticity: 1.38 (elastic)
   - Recommendation: LOWER to $17.95 (-10% price)

3. ANIMEPOP (Neutral)
   - Current price: $24.95
   - Revenue (7d): $10,800
   - CVR: 3.40%
   - Elasticity: 0.87 (neutral)
   - Recommendation: HOLD or test small increase
```

---

### Step 2: Design Test Cohorts (Saturday 4:00–4:15 AM)

For **NARUICO (raise to $21.95):**

```python
# Test cohort: NARUICO on top 5 devices (by volume)

test_cohort = {
    'design': 'NARUICO',
    'test_name': 'NARUICO_PRICE_RAISE_APR19',
    'control_price': '$19.95',
    'test_price': '$21.95',
    'price_change': '+10%',
    'skus': [
        'HTPCR-IPH17PMAX-NARUICO-AKA',
        'HTPCR-IPH17-NARUICO-AKA',
        'HTPCR-IPH16PMAX-NARUICO-AKA',
        'HTPCR-IPH16-NARUICO-AKA',
        'HTPCR-IPH15PMAX-NARUICO-AKA',
        # ... 95 more SKUs in test cohort
    ],
    'sku_count': 100,
    'device_coverage': ['iPhone 17 PM', 'iPhone 17', 'iPhone 16 PM', 'iPhone 16', 'iPhone 15 PM', 'etc.'],
    'expected_outcome': 'Revenue increase if demand is truly inelastic'
}

# Store test metadata in Supabase
supabase.table('price_experiments').insert({
    'test_id': 'NARUICO_PRICE_RAISE_APR19',
    'design_code': 'NARUICO',
    'test_type': 'PRICE_RAISE',
    'control_price': 19.95,
    'test_price': 21.95,
    'sku_list': test_cohort['skus'],
    'sku_count': 100,
    'start_date': '2026-04-19',
    'end_date': '2026-04-26',
    'status': 'ACTIVE'
})
```

---

### Step 3: Implement Price Change (Saturday 4:15 AM)

**Use advisor tool for this:** Should we batch all 3 tests or stagger them?

```
Question for Advisor:

"I want to run 3 price tests simultaneously:
1. NARUICO: Raise to $21.95
2. DRGBSUSC: Lower to $17.95
3. ANIMEPOP: Hold at $24.95

Should I:
A) Run all 3 simultaneously (faster, more data contamination risk)
B) Stagger them 1 week apart (cleaner data, slower learning)
C) Run tests in pairs (balanced)

What's your recommendation?"

Advisor: "Stagger them. Simultaneous tests make it hard to isolate
price effect from seasonal factors. Start with NARUICO (highest revenue),
wait 7 days, then DRGBSUSC."

→ You implement: NARUICO only on Apr 19. DRGBSUSC on Apr 26.
```

#### Actual Price Update

```python
# Update BigCommerce / Amazon / Shopify prices for test cohort

import shopify_api
import bigcommerce_api

test_skus = test_cohort['skus']

for sku in test_skus:
    # Shopify
    shopify_api.update_variant_price(sku, new_price=21.95)
    
    # BigCommerce (if different platform)
    bigcommerce_api.update_product_price(sku, new_price=21.95)
    
    # Log change
    supabase.table('price_change_log').insert({
        'sku': sku,
        'old_price': 19.95,
        'new_price': 21.95,
        'test_id': 'NARUICO_PRICE_RAISE_APR19',
        'timestamp': datetime.now()
    })

# Verify prices updated
print(f"✅ Updated {len(test_skus)} SKUs to $21.95")
```

---

### Step 4: Monitor Test (Saturday 4:15 AM → Following Saturday 3:00 AM)

**Real-time monitoring (automated):**

```python
# Every 12 hours during test week, query results

def monitor_price_experiment(test_id):
    # Get test metadata
    test = supabase.table('price_experiments').select('*').eq('test_id', test_id).single()
    
    # Query orders for test cohort
    test_results = {}
    for sku in test['sku_list']:
        orders = supabase.rpc(
            'get_orders_by_sku',
            {'sku': sku, 'days': 7}
        )
        
        test_results[sku] = {
            'orders': len(orders),
            'revenue': sum(o['order_value'] for o in orders),
            'cvr': calculate_cvr(sku, orders),
            'aov': mean([o['order_value'] for o in orders])
        }
    
    # Aggregate cohort metrics
    aggregate = {
        'test_id': test_id,
        'total_orders': sum(r['orders'] for r in test_results.values()),
        'total_revenue': sum(r['revenue'] for r in test_results.values()),
        'avg_cvr': mean([r['cvr'] for r in test_results.values()]),
        'avg_aov': mean([r['aov'] for r in test_results.values()]),
        'vs_control': {
            'cvr_delta': avg_cvr - control_cvr,  # Compare to previous week
            'revenue_delta': total_revenue - control_revenue,
            'aov_delta': avg_aov - control_aov
        }
    }
    
    return aggregate
```

**Telegram daily update (if meaningful change detected):**

```
⚠️ **Price Test Update: NARUICO Raise**

After 24h:
• Orders: 142 (vs control avg 148) = -4.1%
• Revenue: $3,121 (vs control $2,950) = +5.8%
• CVR: 3.09% (vs control 3.12%) = -0.09%
• AOV: $21.98 (vs control $19.95) = +10.2%

📊 Early signal: INELASTIC demand confirmed!
Revenue up despite slight order drop. Raising price is working.

One more day of data before decision.
```

---

### Step 5: Results Analysis (Following Saturday 3:00 AM)

**After 7 days, evaluate:**

```python
# Compare test week vs control week (previous 7 days)

analysis = {
    'test_id': 'NARUICO_PRICE_RAISE_APR19',
    'duration_days': 7,
    
    'test_metrics': {
        'orders': 987,
        'revenue': '$21,703',
        'cvr': 3.08%,
        'aov': '$21.98'
    },
    
    'control_metrics': {
        'orders': 1028,
        'revenue': '$20,508',
        'cvr': 3.12%,
        'aov': '$19.95'
    },
    
    'deltas': {
        'orders': '-41 (-3.9%)',
        'revenue': '+$1,195 (+5.8%)',
        'cvr': '-0.04 (-1.3%)',
        'aov': '+$2.03 (+10.2%)'
    },
    
    'verdict': '✅ SUCCESS — Raise was correct',
    'next_action': 'Expand price to all NARUICO SKUs by end of week'
}
```

---

### Step 6: Expansion (Following Saturday 4:00 AM)

**If test succeeds:** Roll out to entire design.

```python
# Expand winning price to all NARUICO SKUs (not just test cohort)

all_naruico_skus = supabase.rpc('get_skus_by_design', {'design': 'NARUICO'})
# Returns: ~245 SKUs

for sku in all_naruico_skus:
    shopify_api.update_variant_price(sku, new_price=21.95)
    bigcommerce_api.update_product_price(sku, new_price=21.95)

# Log expansion
supabase.table('price_experiment_results').insert({
    'test_id': 'NARUICO_PRICE_RAISE_APR19',
    'verdict': 'SUCCESS',
    'revenue_lift': 1195,
    'order_impact': -41,
    'expanded_at': datetime.now(),
    'skus_expanded': len(all_naruico_skus)
})

print(f"✅ Expanded winning price to {len(all_naruico_skus)} NARUICO SKUs")
```

---

## Part 4: Full Integration Timeline

### Week 1 (Apr 19)
- Sat 3:00 AM: Sales traffic analysis
- Sat 3:30 AM: Identify 3 price test candidates
- Sat 4:00 AM: Design NARUICO test cohort
- Sat 4:15 AM: Update 100 NARUICO SKUs to $21.95
- Mon 5:00 AM: PULSE leaderboard report

### Week 2 (Apr 26)
- Sat 3:00 AM: Sales traffic analysis
- Sat 3:30 AM: **Analyze NARUICO results** → ✅ SUCCESS
- Sat 4:00 AM: **Expand NARUICO to all 245 SKUs**
- Sat 4:15 AM: **Launch DRGBSUSC test** (lower to $17.95)
- Mon 5:00 AM: PULSE leaderboard report

### Week 3–4 (May 3, May 10)
- Continue staggered tests
- Each successful test gets rolled out
- ANIMEPOP test (neutral case)

### Month 2+ (May onwards)
- Rotation: New designs enter test queue
- Advisor tool helps prioritize candidates
- Continuous learning: Which designs respond to price changes?

---

## Success Criteria

✅ **Revenue Optimization:**
- Week 1–4: Implement 3 tests
- Expected cumulative revenue lift: +$5K–$10K/month
- By end of Q2: Pricing is optimized for all champion designs

✅ **Methodology:**
- All tests have control groups (comparison to previous week)
- Price changes staggered (one per week)
- Results analyzed before expansion

✅ **Learning Loop:**
- After each test, create a "price elasticity" learning card
- Hermes self-improves: Which designs are price-sensitive? Which can absorb higher prices?
- By month 3: Hermes can autonomously predict which designs need price adjustments

---

## Dependencies & Tools

| Resource | Status | Notes |
|----------|--------|-------|
| Supabase (orders, experiments table) | ✅ | Service role key in TOOLS.md |
| BigCommerce API | ✅ | For price updates |
| Shopify API | ✅ | For Shopify variants |
| Amazon SP-API | ✅ | For Amazon listing prices (if needed) |
| Advisor Tool (Opus 4.6) | ✅ | For test design decisions |
| Telegram API | ✅ | For daily updates |

---

## Handoff from Previous SOPs

| Previous Task | Now Owned By | When |
|---------------|-------------|------|
| Weekly PULSE Leaderboard | Hermes | Mon 5:00 AM |
| Weekly Listings Analysis (US/UK/DE) | Hermes | Sat 1:00–3:00 AM |
| Weekly Shipping Template Audit | Hermes | Wed 2:00 AM |
| **NEW: Sales Traffic Analysis** | Hermes | Sat 3:00 AM |
| **NEW: Price Optimization (Karpathy)** | Hermes | Sat 3:30–4:15 AM |

---

**Document Version:** 1.0  
**Status:** Ready for deployment  
**First Run:** Saturday, Apr 19, 2026 (Sales traffic + PULSE)  
**First Price Test:** Saturday, Apr 19, 2026 (NARUICO raise)  
**Next Review:** Apr 26 (after first complete cycle)