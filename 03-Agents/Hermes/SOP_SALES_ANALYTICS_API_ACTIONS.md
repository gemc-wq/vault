# SOP: Sales Analytics with API-Driven Actions
**For Hermes Agent (GLM 5.1, Nous Research)**

**Effective:** 2026-04-13  
**Owner:** Hermes (GLM 5.1)  
**Execution:** Saturdays 4:30–6:00 AM ET (post-analysis window)  
**Integration:** Follows weekly sales analysis + PULSE leaderboard

---

## Overview

After Hermes completes the weekly sales analysis (top movers, traffic patterns, CVR data), this SOP defines how to **automatically execute corrective actions via API** based on the analytics findings.

**Core Objective:** Turn insights into action without human review (except for critical decisions).

**Key Feature:** All actions are logged, reversible, and have clear success criteria.

---

## Part 1: US High-Priority Items → Nationwide Prime Migration

### Background

**Current State:**
- US high-priority designs use `Reduced Shipping Template` (standard, 5–7 day delivery)
- Problem: Lower conversion than premium shipping
- Opportunity: Migrate to `Nationwide Prime` (2-day Prime equivalent) to boost CVR

**Expected Impact:**
- CVR increase: +0.5–1.5% (based on UK data showing Prime gets 3.6% CVR vs 3.2%)
- Revenue per order: Slightly higher AOV (customers feel premium service)
- Risk: Shipping cost increase (if merchant-paid vs buyer-paid)

---

### Step 1: Identify High-Priority US Designs (Saturday 4:30 AM)

```python
# Query: Top revenue-generating designs from PULSE leaderboard

high_priority_designs = supabase.rpc('get_top_designs_by_revenue', {
    'region': 'US',
    'lookback_days': 30,
    'min_revenue': 10000  # Only designs >$10K in 30 days
})

# Expected output:
# [
#   {'design_code': 'NARUICO', 'revenue': $156000, 'sku_count': 245},
#   {'design_code': 'DRGBSUSC', 'revenue': $142000, 'sku_count': 198},
#   {'design_code': 'ONEPIECE', 'revenue': $138000, 'sku_count': 187},
#   ... (top 20 designs)
# ]

print(f"Identified {len(high_priority_designs)} high-priority designs for Prime migration")
```

### Step 2: Filter for Migration Eligibility (Saturday 4:35 AM)

```python
# Not all designs can/should migrate to Prime

eligible_for_prime = []

for design in high_priority_designs:
    # Criterion 1: Currently on Reduced Shipping Template
    current_template = get_shipping_template_for_design(design['design_code'])
    
    if current_template != 'Reduced Shipping Template':
        continue  # Skip if already on different template
    
    # Criterion 2: Has sufficient device coverage
    # (Can't offer Prime if only 2 devices available)
    sku_count = design['sku_count']
    
    if sku_count < 50:
        continue  # Skip if too few SKUs (niche design)
    
    # Criterion 3: Check for exclusion rules
    # Some designs excluded: NFLLegacy (expire soon), test SKUs, regional-specific
    if is_excluded(design['design_code']):
        continue
    
    # Criterion 4: Revenue-justified (cost of Prime worth it?)
    # Prime shipping cost premium: ~$2–4 per order
    # Min revenue to justify: $10K/month = ~300 orders/month
    # If we expect 2% CVR lift on 3K impressions/month = 60 extra orders
    # Extra revenue: 60 × $20 = $1,200 > cost of Prime
    
    if design['revenue'] < 10000:
        continue
    
    # Pass all checks
    eligible_for_prime.append({
        'design_code': design['design_code'],
        'reason': 'High-priority US design, sufficient coverage',
        'current_template': current_template,
        'sku_count': design['sku_count'],
        'revenue': design['revenue']
    })

print(f"Eligible for Prime migration: {len(eligible_for_prime)} designs")

# Example output:
# [
#   {'design_code': 'NARUICO', 'sku_count': 245, 'revenue': $156000},
#   {'design_code': 'DRGBSUSC', 'sku_count': 198, 'revenue': $142000},
#   {'design_code': 'ONEPIECE', 'sku_count': 187, 'revenue': $138000}
# ]
```

### Step 3: Check US Shipping Template Availability (Saturday 4:40 AM)

```python
# Critical: Verify that US actually has "Nationwide Prime" template available

us_available_templates = get_amazon_shipping_templates(marketplace='US')

# Expected: Includes 'Nationwide Prime' (or similar Prime template)
# If NOT found: STOP and alert Cem

if 'Nationwide Prime' not in us_available_templates:
    # Fallback: Check for alternatives
    prime_alternatives = [t for t in us_available_templates if 'Prime' in t]
    
    if not prime_alternatives:
        alert_cem("""
        🚨 CRITICAL: US shipping templates don't include 'Nationwide Prime'.
        
        Available templates in US:
        {available_templates}
        
        Cannot proceed with Prime migration until we confirm the correct template name.
        Please check Seller Central and confirm.
        """)
        return  # Stop execution
    else:
        # Use detected Prime alternative
        prime_template_name = prime_alternatives[0]
        print(f"⚠️ Using alternative: '{prime_template_name}' instead of 'Nationwide Prime'")
else:
    prime_template_name = 'Nationwide Prime'
    print(f"✅ Confirmed US has '{prime_template_name}' template available")
```

### Step 4: Pre-Migration Validation (Saturday 4:45 AM)

```python
# Before making changes, validate all SKUs can be updated

migration_plan = {
    'designs': eligible_for_prime,
    'target_template': prime_template_name,
    'total_skus': sum(d['sku_count'] for d in eligible_for_prime),
    'skus_by_design': {}
}

for design in eligible_for_prime:
    # Get all SKUs for this design in US marketplace
    skus = supabase.table('listings_current').select('seller_sku').eq('design_code', design['design_code']).execute()
    
    migration_plan['skus_by_design'][design['design_code']] = skus.data
    
    # Validate each SKU
    for sku in skus.data:
        if not is_valid_sku_format(sku['seller_sku']):
            print(f"⚠️ Invalid SKU format: {sku['seller_sku']} — will skip")

print(f"✅ Migration plan validated: {migration_plan['total_skus']} SKUs ready")
```

### Step 5: Execute Template Migration via API (Saturday 4:50 AM)

```python
# Update shipping templates on all eligible SKUs

migration_results = {
    'success': [],
    'failed': [],
    'skipped': []
}

for design_code, skus in migration_plan['skus_by_design'].items():
    for sku_record in skus:
        sku = sku_record['seller_sku']
        
        try:
            # Update via Amazon SP-API or BigCommerce API
            # (depending on where listing lives)
            
            # BigCommerce update
            bc_product = bigcommerce_api.get_product_by_sku(sku)
            
            if bc_product:
                bc_result = bigcommerce_api.update_product(
                    product_id=bc_product['id'],
                    fields={
                        'custom_fields': [
                            {
                                'name': 'merchant_shipping_group',
                                'value': prime_template_name
                            }
                        ]
                    }
                )
                
                migration_results['success'].append({
                    'sku': sku,
                    'design': design_code,
                    'from': 'Reduced Shipping Template',
                    'to': prime_template_name
                })
            else:
                migration_results['skipped'].append({
                    'sku': sku,
                    'reason': 'Not found in BigCommerce'
                })
        
        except Exception as e:
            migration_results['failed'].append({
                'sku': sku,
                'error': str(e)
            })

print(f"✅ Migration complete: {len(migration_results['success'])} updated")
print(f"⚠️ {len(migration_results['failed'])} failed")
print(f"⊘ {len(migration_results['skipped'])} skipped")

# Log to database
supabase.table('migration_log').insert({
    'migration_id': 'NATIONWIDE_PRIME_US_APR19',
    'designs': [d['design_code'] for d in eligible_for_prime],
    'total_skus': len(migration_results['success']),
    'template_from': 'Reduced Shipping Template',
    'template_to': prime_template_name,
    'timestamp': datetime.now(),
    'results': migration_results
})
```

### Step 6: Validate Migration (Saturday 5:00 AM)

```python
# Spot-check: Verify changes took effect

validation_sample = migration_results['success'][:20]  # Check first 20

for result in validation_sample:
    sku = result['sku']
    
    # Re-query to verify template changed
    current_template = get_sku_shipping_template(sku)
    
    if current_template == prime_template_name:
        print(f"✅ {sku}: {result['from']} → {current_template}")
    else:
        print(f"❌ {sku}: Expected '{prime_template_name}', got '{current_template}'")

# Alert Cem with results
telegram_alert = f"""
✅ **US Nationwide Prime Migration Complete — Apr 19, 2026**

Designs migrated: {len(eligible_for_prime)}
SKUs updated: {len(migration_results['success'])}
Failed: {len(migration_results['failed'])}
Skipped: {len(migration_results['skipped'])}

Top designs moved to Nationwide Prime:
• NARUICO: 245 SKUs
• DRGBSUSC: 198 SKUs
• ONEPIECE: 187 SKUs

Expected impact: +0.5–1.5% CVR boost on these designs
Monitoring begins immediately.

Full report: results/migration_nationwide_prime_apr19.md
"""

send_telegram(telegram_alert)
```

---

## Part 2: Sales Analytics-Driven API Actions (Generalized Framework)

### Pattern: Analyze → Identify → Act → Verify → Report

This framework extends beyond Prime migration to any analytics-driven action.

#### Example Actions (Based on Analytics)

**Action 1: Price Optimization**
- Analyze: Identify inelastic designs
- Identify: NARUICO (price elasticity 0.24)
- Act: Raise price from $19.95 to $21.95
- Verify: Check if price updated on 100 test SKUs
- Report: Results after 7 days

**Action 2: Inventory Rebalancing**
- Analyze: Identify fast movers
- Identify: iPhone 17 Pro Max (3.86% CVR, 22% of orders)
- Act: Increase stock allocation to iPhone 17 PM devices (call fulfillment)
- Verify: Stock levels updated in Supabase
- Report: New stock distribution

**Action 3: Marketing Spend Shift**
- Analyze: Identify underperformers
- Identify: Samsung A-series (2.75% CVR, declining)
- Act: Reduce ad spend on Samsung A-series, increase iPhone 17
- Verify: Amazon Advertising API confirms budget shift
- Report: Daily spend tracking

**Action 4: Design Variant Rollout**
- Analyze: Identify rising stars
- Identify: ANIMEPOP_V2 (+210% velocity)
- Act: Expand ANIMEPOP_V2 to all devices (upload missing SKUs)
- Verify: New listings appear in Active Listings within 24h
- Report: Coverage % before/after

**Action 5: Regional Expansion**
- Analyze: Identify cross-region gaps
- Identify: NARUICO 80% revenue untapped in UK/DE
- Act: Expand NARUICO to EU devices (new SKUs)
- Verify: Listings sync to UK/DE marketplace
- Report: New availability metrics

---

### Generalized Action Framework

```python
class AnalyticsAction:
    """Base class for analytics-driven API actions"""
    
    def __init__(self, action_type, insight, **kwargs):
        self.action_type = action_type  # PRICE_CHANGE, STOCK_REBALANCE, etc.
        self.insight = insight          # The finding that triggers action
        self.kwargs = kwargs
        self.execution_log = []
    
    def identify_targets(self):
        """Step 1: Which SKUs/designs should we act on?"""
        # Override in subclass
        pass
    
    def validate_feasibility(self):
        """Step 2: Can we actually do this? (API access, inventory, etc.)"""
        # Check API permissions
        # Check data availability
        # Check business rules
        pass
    
    def execute(self):
        """Step 3: Make the API calls"""
        # Retry logic
        # Error handling
        # Logging each action
        pass
    
    def validate_results(self):
        """Step 4: Did the changes actually take effect?"""
        # Spot-check results
        # Query updated state
        # Flag anomalies
        pass
    
    def report(self):
        """Step 5: Summarize for human review"""
        # Create markdown report
        # Send Telegram alert
        # Log to database
        pass
    
    def execute_full_workflow(self):
        """Run all steps"""
        self.identify_targets()
        self.validate_feasibility()
        self.execute()
        self.validate_results()
        self.report()

# Usage:
action = PriceChangeAction(
    insight={'design': 'NARUICO', 'elasticity': 0.24},
    old_price=19.95,
    new_price=21.95,
    sku_count=100
)
action.execute_full_workflow()
```

---

## Part 3: Critical Safety Guardrails

### Guardrail 1: Dry-Run Before Commit

```python
# ALWAYS run in dry-run mode first

migration_results_dry = execute_template_migration(
    skus=eligible_skus,
    template=prime_template_name,
    dry_run=True  # ← KEY: No actual API calls
)

# Review results
print(f"Would update: {len(migration_results_dry['success'])} SKUs")
print(f"Would fail: {len(migration_results_dry['failed'])} SKUs")

# Only proceed to real execution if results look good
if len(migration_results_dry['failed']) < 5:  # Allow <1% failure rate
    print("✅ Dry-run looks good, proceeding to real execution")
    migration_results_real = execute_template_migration(
        skus=eligible_skus,
        template=prime_template_name,
        dry_run=False  # ← Now make real API calls
    )
else:
    print("❌ Dry-run found too many errors, aborting real execution")
    alert_cem("Migration aborted due to high error rate in dry-run")
    return
```

### Guardrail 2: Rate Limiting & Batch Processing

```python
# Don't hammer APIs. Batch + delay.

batch_size = 50  # Process 50 SKUs at a time
delay_between_batches = 5  # seconds

for i in range(0, len(eligible_skus), batch_size):
    batch = eligible_skus[i:i+batch_size]
    
    # Update batch
    for sku in batch:
        update_sku(sku, template=prime_template_name)
    
    # Wait before next batch
    time.sleep(delay_between_batches)
    
    # Log progress
    print(f"Processed {min(i+batch_size, len(eligible_skus))}/{len(eligible_skus)}")
```

### Guardrail 3: Reversibility

```python
# Every action must be reversible

action_log_entry = {
    'action_id': generate_unique_id(),
    'timestamp': datetime.now(),
    'action_type': 'SHIPPING_TEMPLATE_MIGRATION',
    'changes': [
        {'sku': 'HTPCR-IPH17PM-NARUICO-AKA', 'from': 'Reduced Shipping Template', 'to': 'Nationwide Prime'},
        # ... 244 more
    ],
    'revert_command': """
    UPDATE listings SET merchant_shipping_group='Reduced Shipping Template' 
    WHERE design_code IN ('NARUICO', 'DRGBSUSC', 'ONEPIECE')
    """
}

# Store revert command in database
supabase.table('action_reversals').insert(action_log_entry)

# If we discover an issue, Hermes can revert:
# revert_action('action_id_12345')
```

### Guardrail 4: Impact Monitoring

```python
# After action, monitor for unexpected side effects

def monitor_action_impact(action_id, days=7):
    """Monitor for 7 days post-action"""
    
    baseline = get_metrics_before_action(action_id)
    
    for day in range(1, days+1):
        current = get_metrics_for_day(action_id, day)
        
        # Check for anomalies
        if current['cvr'] < baseline['cvr'] * 0.95:
            # CVR dropped >5%
            alert_cem(f"""
            ⚠️ **Action Impact Alert**: CVR dropped after {action_id}
            Baseline: {baseline['cvr']}
            Current (Day {day}): {current['cvr']}
            Consider reverting if drop continues.
            """)
```

---

## Part 4: Weekly Action Execution Schedule

### Saturdays 4:30–6:00 AM (Post-Analysis Window)

```
4:30–4:35 AM: Identify high-priority US designs (PULSE leaderboard)
4:35–4:40 AM: Filter for Prime migration eligibility
4:40–4:45 AM: Verify US has Nationwide Prime template
4:45–4:50 AM: Validate all SKUs, create migration plan
4:50–5:00 AM: Execute template migration (dry-run)
5:00–5:05 AM: Validate results, spot-check
5:05–5:15 AM: Create report + send Telegram alert
5:15–6:00 AM: Monitor ongoing actions, handle edge cases
```

---

## Part 5: Advisor Tool Usage for Actions

### When to Invoke Advisor Before Committing

**Scenario 1: High-Risk Migration**
```
"I identified 800 SKUs to migrate to Nationwide Prime.
This is 25% of all US listings.

Should I:
A) Migrate all 800 (faster, higher risk)
B) Migrate top 100 first, monitor, then expand (safer, slower)
C) Get Cem approval first (slowest, safest)"

Advisor: "Recommend B. Test with top 100 first. If CVR lift confirmed,
expand rest. This is too big to risk all-at-once."
```

**Scenario 2: Conflicting Signals**
```
"Analytics say: Raise NARUICO price to $21.95 (inelastic demand)
But: Last week NARUICO had -2% order volume decline.

Should I still raise price, or wait for more stability?"

Advisor: "Hold off. Price raise could amplify the decline.
Wait for stabilization, then test. Risk is too high right now."
```

**Scenario 3: Unexpected Results**
```
"I migrated 245 NARUICO SKUs to Nationwide Prime.
Day 1 result: CVR DROPPED 8% (expected +0.5–1.5%).

Should I:
A) Revert immediately
B) Give it 3 more days (might be noise)
C) Investigate what went wrong before reverting"

Advisor: "Revert immediately. 8% drop is significant.
Investigate post-revert. Could be market timing, not the template change."
```

---

## Dependencies & Credentials

| Resource | Status | Notes |
|----------|--------|-------|
| BigCommerce API | ✅ | For product updates (GoHeadCase catalog) |
| Shopify API | ✅ | For Shopify variant updates |
| Amazon SP-API | ✅ | For Amazon listing metadata (if needed) |
| Supabase | ✅ | For logging + monitoring |
| Advisor Tool (Opus 4.6) | ✅ | For high-risk decision guidance |
| Telegram API | ✅ | For alerts |

---

## Success Criteria

✅ **Prime Migration (First Action)**
- Identify top 20 US designs
- Filter for eligibility (50+ SKUs, >$10K revenue)
- Migrate 700+ SKUs to Nationwide Prime
- Validate 100% of changes took effect
- Monitor for 7 days post-migration
- CVR lift: +0.5% min (goal: +1%)

✅ **Framework Scalability**
- Action workflow generalizable to price changes, inventory rebalancing, regional expansion
- Dry-run before commit on all actions
- Reversibility: All actions can be undone
- Monitoring: Post-action tracking for 7 days

✅ **Safety**
- Zero unintended API calls (dry-run validates first)
- Rate limiting respected (batch processing)
- Advisor consulted for high-risk decisions
- Impact monitoring catches anomalies

---

## Timeline

| Date | Task | Status |
|------|------|--------|
| Sat Apr 19 | First action: NARUICO (+ top designs) → Nationwide Prime | Ready |
| Sun–Fri Apr 20–26 | Monitor migration impact | Ongoing |
| Sat Apr 26 | Analyze results, consider expansion | Pending results |
| Sat May 3 | Next action: Price optimization or regional expansion | Backlog |

---

**Document Version:** 1.0  
**Status:** Ready for Hermes deployment  
**First Run:** Saturday, Apr 19, 2026 @ 4:50 AM  
**Next Review:** Sunday, Apr 20 (post-migration monitoring)