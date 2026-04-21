# Priority Zero: Shipping Template Conversion Strategy
## Advisor-Guided Analysis (Opus 4.6)

**Date:** 2026-04-11 | **Owner:** Ava | **Priority:** CRITICAL (P0) | **Timeline:** This week

---

## Problem Statement (Clarified by Cem)

### Current Workflow (Broken)
1. New listing created on Amazon → defaults to "Standard" shipping template
2. Philippines fulfillment script runs → converts to "Reduced Shipping" (2-day US, Prime UK)
3. **Script timeouts/errors** → leaves items on Standard template indefinitely
4. **Result:** 15% of listings stuck on Standard → lower conversion rates

### Regional Shipping Templates
- **US:** "Reduced Shipping" (2-day) = 2-4% conversion lift vs Standard
- **UK:** "Prime" (nationwide) = 2-4% conversion lift vs Standard  
- **Conversion impact:** Direct correlation proven by historical analysis

### Root Cause
Philippines script (currently converting listings) is **unreliable:**
- Timeouts on large batch conversions
- No error handling for failed templates
- No retry logic
- Leaves listings orphaned on defaults

### Business Impact
**Current state (85% compliance):** 502K SKUs on Standard template
**Potential loss:** 502K × 2.5% baseline conv × 2% missed uplift × ~$15 AOV = **$37.5K/month revenue loss**

---

## Proposed Solution: Multi-Layer Approach

### Layer 1: **Opportunity Finder** (Dashboard + Rules Engine)
**Purpose:** Identify which SKUs SHOULD be on reduced/prime templates

**Rules (driven by inventory + design):**
```
Rule Set for US:
  IF inventory_status = 'FBA'
     AND design_revenue_rank <= TOP_500
     THEN priority = "CONVERT_IMMEDIATELY"
  
  IF inventory_status = 'FBA'
     AND design_revenue_rank > TOP_500
     THEN priority = "CONVERT_THIS_WEEK"
  
  IF inventory_status = 'FBM'
     AND fulfillment_location = 'US'
     AND capable_2day_shipping = TRUE
     THEN priority = "CONVERT_CONDITIONAL"

Rule Set for UK:
  IF inventory_status = 'FBA'
     AND design_revenue_rank <= TOP_300
     THEN priority = "APPLY_PRIME"
  
  IF geography = 'UK'
     AND can_fulfill_nationally = TRUE
     THEN priority = "APPLY_PRIME"
```

**Inventory Dependency:**
- Rule engine needs: `inventory_status`, `fulfillment_capable`, `days_to_stock`
- This is why Harry's inventory module is CRITICAL blockers
- Until Harry delivers inventory data, we work with approximations (design tier, historical velocity)

### Layer 2: **Automatic Conversion Cron** (Codex, daily or every 2 days)
**Purpose:** Fix missed conversions without waiting for Philippines script

**What it does:**
1. Query Active Listings Report (weekly via Cloud Run OR manual download)
2. Identify listings NOT on Reduced/Prime templates
3. Cross-reference with Opportunity Finder rules
4. For each eligible SKU:
   - Call Amazon SP-API to update shipping template
   - Log result (success/fail)
   - Retry on failure
5. Generate daily report (items converted, failures, next batch)

**Key advantage:** Codex runs reliably, with error handling, no timeouts

**Frequency:** 
- **Option A:** Daily (most aggressive, immediate fixes)
- **Option B:** Every 2 days (balanced, reduces API load)
- **Recommended:** Daily, starting at 11 PM after inventory sync

### Layer 3: **Dashboard Visibility**
**Purpose:** Monitor conversion health, spot gaps

**Views:**
1. **Conversion Status Scorecard**
   - % on Reduced/Prime (target: 100%)
   - % on Standard (target: 0%)
   - Items converted today/week
   - Items pending conversion

2. **Opportunity Pipeline**
   - By design (which designs need conversion)
   - By device (which model combos need work)
   - By priority (IMMEDIATE, THIS_WEEK, CONDITIONAL)
   - Revenue impact of each opportunity

3. **Conversion Velocity**
   - Daily conversions (should trend toward 100%)
   - Failed conversions (retry status)
   - Why items couldn't convert (inventory, SP-API errors, etc.)

4. **Before/After Metrics**
   - Conversion rate by template (Standard vs Reduced vs Prime)
   - Revenue lift realized per wave of conversions
   - Track ROI of Codex cron vs Philippines script

---

## Implementation Plan

### Phase 0: Rules Definition (This Week, 1-2 days)

**Deliverable:** `SHIPPING_CONVERSION_RULES.yaml`

```yaml
regions:
  US:
    reduced_shipping:
      eligible_inventory_types:
        - FBA
        - FBM (if 2-day capable)
      priority_by_design_tier:
        top_500_designs: "IMMEDIATE"
        top_501_1000: "THIS_WEEK"
        others: "NEXT_WEEK"
      priority_by_inventory:
        in_stock: "IMMEDIATE"
        low_stock: "THIS_WEEK"
        backorder: "DEFER"
  
  UK:
    prime_nationwide:
      eligible_inventory_types:
        - FBA
      priority_by_design_tier:
        top_300_designs: "IMMEDIATE"
        others: "THIS_WEEK"
      priority_by_location:
        UK_warehouse: "IMMEDIATE"
        EU_warehouse: "DEFER"

conversion_rules:
  retry_logic:
    max_retries: 3
    backoff: "exponential"
    timeout_seconds: 30
  
  batch_size: 100  # items per API batch
  rate_limit: "5 per second"  # respect Amazon SP-API limits
```

**Owner:** Cem + Ava (define priority, inventory dependencies)

### Phase 1: Dashboard + Opportunity Finder (Apr 11-15, 2-3 days)

**Build:**
1. SQLite table: `shipping_opportunities` (design, sku, current_template, should_be_template, priority, reason)
2. Dashboard view: "Opportunity Finder" (shows priority pipeline, revenue impact)
3. API endpoint: `/api/shipping/opportunities?priority=IMMEDIATE` (for Codex cron to query)

**Data source:** 
- Active Listings Report (weekly, already processed by Codex)
- Rules engine (cross-reference with SHIPPING_CONVERSION_RULES.yaml)
- Inventory data (once Harry delivers, update rules in real-time)

**Timeline:** 2-3 days, can run in parallel with Codex cron setup

### Phase 2: Codex Cron Setup (Apr 11-13, 1-2 days)

**Build:** `shipping_template_converter.py`

```python
#!/usr/bin/env python3
"""
Daily cron: Fix shipping template gaps.

1. Query /api/shipping/opportunities?priority=IMMEDIATE
2. For each eligible SKU:
   - Call SP-API to update shipping template
   - Log result
   - Retry on failure (3x exponential backoff)
3. Generate daily report (summary + failures)
4. Alert on critical failures (>10% failure rate)
"""

import requests
from amazon_sp_api import AmazonSpAPI
from datetime import datetime

def get_opportunities(priority='IMMEDIATE'):
    """Get eligible items for conversion from dashboard."""
    resp = requests.get(
        f'http://localhost:3000/api/shipping/opportunities?priority={priority}'
    )
    return resp.json()['items']

def convert_template(sku, marketplace, template_type):
    """Call SP-API to update shipping template."""
    sp_api = AmazonSpAPI(region=marketplace)
    try:
        result = sp_api.Listings.patch_listings_item(
            sku=sku,
            body={
                'attributes': {
                    'fulfillment_availability': [{
                        'fulfillment_channel_code': 'DEFAULT',
                        'quantity': <from_inventory>
                    }],
                    'shipping_template': template_type  # 'REDUCED' or 'PRIME'
                }
            }
        )
        return result
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}

def run_daily_conversion():
    """Main cron job."""
    start_time = datetime.now()
    
    # Get IMMEDIATE priority items
    items = get_opportunities(priority='IMMEDIATE')
    
    converted = 0
    failed = 0
    
    for item in items:
        for attempt in range(3):  # 3 retries
            result = convert_template(
                sku=item['sku'],
                marketplace=item['region'],
                template_type=item['should_template']
            )
            if result['status'] == 'SUCCESS':
                converted += 1
                break
            else:
                failed += 1
                if attempt < 2:
                    time.sleep(2 ** attempt)  # exponential backoff
    
    # Report
    report = {
        'date': start_time.isoformat(),
        'converted': converted,
        'failed': failed,
        'total': len(items),
        'success_rate': (converted / len(items)) * 100
    }
    
    # Log to CloudWatch + Slack alert
    print(json.dumps(report))
    
    if report['success_rate'] < 90:
        alert_slack(f"⚠️ Shipping conversion cron: {report['success_rate']}% success")
    
    return report

if __name__ == '__main__':
    run_daily_conversion()
```

**Deployment:**
- Add cron job: `0 23 * * * python3 /path/to/shipping_template_converter.py`
- Runs at 11 PM daily (after inventory sync, before dashboard midnight refresh)
- Output: JSON report stored in S3 for dashboard visualization

**Timeline:** 1-2 days, can be done in parallel with dashboard

### Phase 3: Inventory Integration (Blocked on Harry, then 1-2 days)

**Once Harry delivers inventory module:**
1. Wire inventory data into rules engine
2. Update opportunity priorities in real-time
3. Refine retry logic (don't convert if out of stock, etc.)
4. Track fulfillment capability per SKU

**Until then:** Use design tier + historical velocity as proxy

---

## Advisor Recommendation: Architecture

### Why Multi-Layer?

**Layer 1 (Dashboard + Rules)** = Visibility + Decision Logic
- No risk
- Real-time understanding of opportunities
- Can be tested independently

**Layer 2 (Codex Cron)** = Automated Fix
- Reliable (unlike Philippines script)
- Error handling + retry
- Daily cadence
- Can be started immediately, doesn't depend on dashboard

**Layer 3 (Monitoring)** = Accountability
- Track conversion rates
- Measure revenue impact
- Alert on failures

### Why Not Just Dashboard?

Dashboard alone is reactive. Operators see the problem but still have to manually click "convert" on each item.

**Why not just Codex cron without dashboard?**

Cron alone is blind. Can't see if conversion is working. Can't understand why items aren't being converted.

**Together:** Codex runs the conversion, Dashboard monitors progress, Operators understand ROI.

---

## Priority Sequencing (Critical)

**This week:**
1. ✅ Define Rules (Cem + Ava) — 1-2 days
2. ✅ Build Codex Cron (Codex) — 1-2 days
3. ⏳ Build Dashboard Opportunity Finder (Forge) — 2-3 days (parallel)

**Next week:**
4. Test full flow (1 day)
5. Deploy to production (1 day)
6. Integrate inventory (1-2 days, pending Harry)

**Go-live:** By Apr 20

---

## Success Metrics

| Metric | Target | Measure |
|--------|--------|---------|
| **Conversion adoption** | 95%+ items on Reduced/Prime | Weekly dashboard review |
| **Cron reliability** | 99%+ success rate | Daily logs, <1% failures |
| **Conversion speed** | <24h from "new listing" to "Reduced" | Track time delta |
| **Revenue lift** | +$50K-100K/month | Conversion rate × revenue |
| **User adoption** | Cem reviews dashboard weekly | Slack notification |

---

## Blocker Dependency: Harry's Inventory Module

**Why critical:**
- Current rules use design tier + velocity (approximations)
- Real rules need: `inventory_status`, `fulfillment_capable`, `days_to_stock`
- Without inventory, we miss conditional conversions (FBM with 2-day capability)

**What Harry needs to deliver:**
- Inventory table: `inventory(sku, location, quantity, days_to_stock, fulfillment_capable)`
- API endpoint: `/api/inventory/{sku}` (for Codex cron to query during conversion)
- Sync: Nightly (not real-time, but acceptable for daily cron)

**Timeline:** If Harry delivers by Apr 20, we refine rules. If not, we ship with design-tier rules and iterate.

---

## Decision: Dashboard-First vs Cron-First?

**Cem's call:**

**Option A: Dashboard-First** (2 weeks total)
- Build dashboard Opportunity Finder (Apr 11-15)
- See full pipeline of what needs converting
- Then deploy Codex cron (Apr 15-18)
- Risk: Codex cron waits, delays fixes by 1 week

**Option B: Cron-First** (1.5 weeks total)
- Deploy Codex cron immediately (Apr 11-13)
- Starts fixing items right away
- Dashboard follows (Apr 13-18) for visibility
- Risk: Cron runs blind for 5 days (no visibility into what's being converted)

**Recommendation (Advisor):** **Hybrid**
- Start both in parallel (Apr 11-13)
- Codex cron reads from hard-coded rules (simple YAML file)
- Dashboard built simultaneously (different team)
- Both go live together (Apr 15-18)
- Best of both: visibility + automation

---

## Tactical: What Codex Should Use While Dashboard Builds

**Hard-coded rules (simple YAML, no API dependency):**

```yaml
# priority_zero_rules.yaml
US:
  IMMEDIATE:
    - designs: [NARUTO, ONEPIECE, PEANUTS, HARRYPOTTER]  # top 500
      min_inventory: 10
      template: "REDUCED"
  THIS_WEEK:
    - designs: [NFL_*, NBA_*]  # urgent license issues
      template: "REDUCED"

UK:
  IMMEDIATE:
    - designs: [NARUTO, ONEPIECE, PEANUTS]  # top 300 UK-approved
      template: "PRIME"
```

Codex cron reads this file, converts SKUs matching these rules.

Once dashboard is live, cron switches to reading from API endpoint (`/api/shipping/opportunities?priority=IMMEDIATE`).

---

## Document to Create: Shipping Conversion Playbook

**File:** `SHIPPING_CONVERSION_PLAYBOOK.md`

Contains:
1. Rules definition (YAML)
2. Codex cron script (Python)
3. Dashboard integration (API spec)
4. Monitoring + alerts (Slack integration)
5. Rollback plan (if cron causes issues)
6. Revenue tracking (how to measure impact)

---

## Status

**Ready:** Rules definition (just need Cem input on priority tiers)
**Ready:** Codex cron skeleton (ready to code, no blockers)
**Ready:** Dashboard spec (leveraging existing DASHBOARD-DESIGN-SPEC.md)
**Blocked:** Inventory integration (pending Harry)

**Recommendation:** Start this week. Deploy Codex + Dashboard by Apr 18. Integrate inventory by Apr 25.

---

**Owner:** Ava (strategy) | **Executor:** Codex (cron) + Forge (dashboard) + Harry (inventory) | **Advisor-Reviewed:** ✅

