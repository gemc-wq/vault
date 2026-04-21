# SOP: Weekly Active Listings Audit
**Effective:** 2026-04-13  
**Owner:** Ava (via Hermes agent, Saturday 1–3 AM)  
**Platforms:** Amazon US, UK, DE  
**Frequency:** Weekly (Saturday mornings)  
**Trigger:** Cem downloads Active Listings reports Friday → Hermes runs audit Saturday

---

## Overview

This SOP defines the end-to-end process for auditing weekly Amazon Active Listings across three regions, validating shipping templates, identifying new SKUs, and cross-referencing team claims in EOD emails/Slack against actual uploaded data.

**Core Objective:** Ensure listings match what the PH team says went live + catch shipping template errors + identify anomalies (ghost listings, unexpected uploads, etc.)

---

## Prerequisites

### Required Files (Cem downloads Friday evening)
- **US Active Listings Report** (`~/Downloads/US_Active_Listings_Report_YYYY-MM-DD.txt`)
  - Size: ~6–9GB (tabular format, tab-separated)
  - From: Amazon Seller Central → Reports → Inventory → Active Listings

- **UK Active Listings Report** (`~/Downloads/UK_Active_Listings_Report_YYYY-MM-DD.txt`)
  - Size: ~500MB–1.5GB
  - From: UK Seller Central → Reports → Inventory → Active Listings

- **DE Active Listings Report** (`~/Downloads/DE_Active_Listings_Report_YYYY-MM-DD.txt`)
  - Size: ~300–800MB
  - From: DE Seller Central → Reports → Inventory → Active Listings

### EOD Email/Slack Context (from PH team Friday–Sunday)
- **Slack Channel:** #eod-listings (C0AHUUGJK7G)
- **Search window:** Friday 5 PM → Sunday 11:59 PM
- **Team claims to extract:**
  - "We uploaded X designs"
  - "Y new SKUs went live"
  - "Listings for [design] complete"

---

## Workflow: Saturday 1–3 AM (Hermes Agent)

### PART 1: US Active Listings Analysis (Sat 1:00 AM)

#### Step 1.1: Verify file exists + integrity check
```bash
# Check file presence and size
ls -lh ~/Downloads/US_Active_Listings_Report_*.txt
# Expected: 6–9GB, modified within 24 hours

# Verify not corrupted (spot-check first 10K lines)
head -10000 ~/Downloads/US_Active_Listings_Report_*.txt | wc -l
# Expected: ~10K lines
```

**If file missing:** Alert Cem immediately via Telegram
```
⚠️ US Active Listings file missing. Download from Seller Central and retry.
```

#### Step 1.2: Load previous snapshot from SQLite
```python
import sqlite3, pandas as pd

# Load last week's snapshot (current → previous)
conn = sqlite3.connect('/Users/openclaw/.openclaw/workspace/data/local_listings.db')
prev = pd.read_sql('SELECT * FROM listings_current WHERE region = "US"', conn)
# This becomes the delta baseline

# Create new table for this week's data
# columns: sku, asin, product_type, device, design_code, fba, 
#          open_date, merchant_shipping_group, price, quantity
```

#### Step 1.3: Parse US Active Listings (chunked)
```python
# Files are 6–9GB, read in chunks
chunks = pd.read_csv(
    '~/Downloads/US_Active_Listings_Report_*.txt',
    sep='\t',
    chunksize=50000,
    on_bad_lines='skip',
    encoding='latin-1',
    dtype={'seller-sku': str, 'open-date': str, 'merchant-shipping-group': str}
)

us_data = pd.concat(chunks)
print(f"Total US listings: {len(us_data):,}")

# Parse SKU: PRODUCT_TYPE-DEVICE-DESIGN-VARIANT
us_data['product_type'] = us_data['seller-sku'].str.split('-').str[0].str.replace(r'^F(?!LAG|1309|RND|KFLOR)', '', regex=True)
us_data['device'] = us_data['seller-sku'].str.split('-').str[1]
us_data['design_code'] = us_data['seller-sku'].str.split('-').str[2]
us_data['fba'] = us_data['fulfillment-channel'].str.contains('AMAZON', na=False)
us_data['open_date_clean'] = pd.to_datetime(us_data['open-date'], errors='coerce')
us_data['days_old'] = (pd.Timestamp.now() - us_data['open_date_clean']).dt.days
```

#### Step 1.4: Calculate delta (new SKUs vs last week)
```python
new_skus = us_data[~us_data['seller-sku'].isin(prev['sku'])]
removed_skus = prev[~prev['sku'].isin(us_data['seller-sku'])]

print(f"New listings this week: {len(new_skus):,}")
print(f"Removed listings: {len(removed_skus):,}")
print(f"Net change: {len(new_skus) - len(removed_skus):,}")

# By product type
new_by_type = new_skus.groupby('product_type').size()
```

#### Step 1.5: **SHIPPING TEMPLATE VALIDATION (US)**
```python
# CRITICAL: Confirm template name before validating
# Current assumption: US template = "Reduced Shipping Template"
# STATUS: ⚠️ UNCONFIRMED — waiting on Cem confirmation

CORRECT_US_TEMPLATE = "Reduced Shipping Template"  # PLACEHOLDER

# Flag NEW listings with wrong template
wrong_template_new = new_skus[
    (new_skus['merchant_shipping_group'] != CORRECT_US_TEMPLATE) &
    (new_skus['days_old'] <= 14)  # Only new listings
]

if len(wrong_template_new) > 0:
    print(f"⚠️ {len(wrong_template_new)} new US listings with WRONG shipping template!")
    print(wrong_template_new[['seller-sku', 'merchant_shipping_group']].to_string())
    # Will be flagged in Slack alert (Step 1.7)
```

#### Step 1.6: Identify top 10 new design codes (by SKU count)
```python
top_new_designs = new_skus['design_code'].value_counts().head(10)

# Enrich with brand/license info (from wiki/design-master.csv if available)
# Example output:
# NARUICO: 45 SKUs (Naruto)
# DRGBSUSC: 38 SKUs (Dragon Ball Super)
# etc.
```

#### Step 1.7: FBA penetration by product type
```python
fba_pct = us_data.groupby('product_type')['fba'].mean() * 100

# Example:
# HTPCR: 15% FBA, 85% FBM
# HB401: 8% FBA, 92% FBM
# HLBWH: 22% FBA, 78% FBM
```

#### Step 1.8: Save report to file
```python
# Create detailed report
report = f"""
# Weekly US Active Listings Report — {pd.Timestamp.now().strftime('%Y-%m-%d')}

## Summary
- **Total listings:** {len(us_data):,}
- **New listings:** {len(new_skus):,}
- **Removed listings:** {len(removed_skus):,}
- **Net change:** {len(new_skus) - len(removed_skus):,}

## Top 10 New Design Codes
{top_new_designs.to_string()}

## FBA Penetration (by product type)
{fba_pct.to_string()}

## ⚠️ Shipping Template Issues
{f"{len(wrong_template_new)} new listings with wrong template" if len(wrong_template_new) > 0 else "✅ All new listings have correct template"}

## Flags & Anomalies
{list_anomalies(us_data)}
"""

with open('results/weekly_listings_us_2026-04-19.md', 'w') as f:
    f.write(report)
```

#### Step 1.9: Post to Slack #eod-listings
```
🇺🇸 **US Active Listings — Week of Apr 19, 2026**

✅ 3.44M total listings
✨ 12,450 new SKUs (50 designs × 249 devices)
⚠️ 1,200 listings removed (EOL clearance)

**Top new:** NARUICO (45), DRGBSUSC (38), DBZGEARFIV (35)

**FBA Split:** HTPCR 15%, HB401 8%, HLBWH 22%

**Shipping Templates:** ✅ All new listings correct

See full report: results/weekly_listings_us_2026-04-19.md
```

#### Step 1.10: Update SQLite (this week becomes next week's baseline)
```python
us_data.to_sql('listings_current', conn, if_exists='replace', index=False)
conn.commit()
# Next week, this will be loaded as 'prev' for delta calculation
```

---

### PART 2: UK Active Listings Analysis (Sat 2:00 AM)

**Same workflow as US, but UK-specific flags:**

#### Step 2.1–2.8: (Same as US Steps 1.1–1.8)

#### Step 2.5: **SHIPPING TEMPLATE VALIDATION (UK)**
```python
# CRITICAL: Confirm template name before validating
# Current assumption: UK template = "Nationwide Prime"
# STATUS: ⚠️ UNCONFIRMED — waiting on Cem confirmation

CORRECT_UK_TEMPLATE = "Nationwide Prime"  # PLACEHOLDER

wrong_template_new_uk = new_skus_uk[
    (new_skus_uk['merchant_shipping_group'] != CORRECT_UK_TEMPLATE) &
    (new_skus_uk['days_old'] <= 14)
]

if len(wrong_template_new_uk) > 0:
    # Alert Slack: "X UK listings with wrong template (should be Nationwide Prime)"
```

#### Step 2.6: UK-specific flags
```python
# Flag 1: Samsung A-series dominance
samsung_a = new_skus_uk[new_skus_uk['device'].str.contains('A1[0-9]', regex=True)]

# Flag 2: Football licenses (UK market specialty)
football_designs = new_skus_uk[new_skus_uk['design_code'].isin(['LFC', 'MCITY', 'SPURS', 'ARSENAL'])]

# Flag 3: HLBWH (wallet) distribution in UK vs US
hlbwh_uk_pct = (new_skus_uk['product_type'] == 'HLBWH').mean() * 100
hlbwh_us_pct = (new_skus['product_type'] == 'HTPCR').mean() * 100  # from Part 1
```

#### Step 2.9: Post to Slack #eod-listings
```
🇬🇧 **UK Active Listings — Week of Apr 19, 2026**

✅ 531M total listings
✨ 8,230 new SKUs
⚠️ 450 listings removed

**Top new:** Football licenses (LFC, Man City, Spurs) — 28% of new SKUs
**Samsung A-series:** 35% of new device variants

**Shipping Templates:** ✅ All use Nationwide Prime

See full report: results/weekly_listings_uk_2026-04-19.md
```

---

### PART 3: DE Active Listings Analysis (Sat 3:00 AM)

**Same workflow, DE-specific flags:**

#### Step 3.1–3.8: (Same as Parts 1 & 2)

#### Step 3.5: **SHIPPING TEMPLATE VALIDATION (DE)**
```python
# DE uses FBM (Fulfillment by Merchant)
# Assumption: No shipping template required
# STATUS: ⚠️ UNCONFIRMED — waiting on Cem confirmation

# If DE has a template, extract it here
# If not, skip template validation for DE
```

#### Step 3.9: Champions Movers Analysis (tied to DE report)
```python
# Query Supabase for 30d vs 90d champion velocity
# Compare top 20 designs from 30 days vs 90 days

movers_up = designs_30d.isin(designs_90d) == False  # New entries (rising stars)
movers_down = designs_90d.isin(designs_30d) == False  # Dropped out (watch list)

# Hermes auto-learns patterns here:
# "Which designs are accelerating?"
# "Which designs are losing momentum?"
```

---

## PART 4: Cross-Reference EOD Listings Emails & Slack

### Step 4.1: Fetch EOD team claims from Slack
```python
import requests

# Fetch #eod-listings messages from Friday 5 PM → Sunday 11:59 PM
slack_token = "[REDACTED_SLACK_BOT_TOKEN]"
response = requests.post(
    'https://slack.com/api/conversations.history',
    headers={'Authorization': f'Bearer {slack_token}'},
    json={'channel': 'C0AHUUGJK7G', 'limit': 100}
)

messages = response.json()['messages']

# Extract claims: "uploaded", "went live", "complete", "finished"
claims = []
for msg in messages:
    text = msg.get('text', '').lower()
    if any(keyword in text for keyword in ['uploaded', 'live', 'complete', 'finished', 'ready']):
        claims.append({
            'user': msg.get('user'),
            'text': msg.get('text'),
            'timestamp': msg.get('ts')
        })
```

### Step 4.2: Parse team claims into actionable items
```python
# Pattern matching examples:
# "We uploaded NARUICO for iPhone 16, 17, 16 Pro" 
#   → Extract: design=NARUICO, devices=[iPhone 16, 17, 16 Pro]

# "All HB401 variants for Naruto are now live"
#   → Extract: product_type=HB401, design=NARUICO

claims_parsed = []
for claim in claims:
    # Use regex or NLP to extract design codes, devices, product types
    # Store in structured format for comparison
```

### Step 4.3: Cross-reference claims against actual uploads
```python
# For each team claim, verify it appears in new_skus

claim_verification = []
for claim in claims_parsed:
    claimed_skus = new_skus[
        (new_skus['design_code'] == claim['design_code']) &
        (new_skus['device'].isin(claim['devices']))
    ]
    
    if len(claimed_skus) == 0:
        # 🚨 DISCREPANCY: Team said it went live, but it's not in Active Listings
        claim_verification.append({
            'status': '❌ NOT FOUND',
            'claim': claim['text'],
            'expected': len(claim['devices']),
            'actual': 0
        })
    elif len(claimed_skus) < len(claim['devices']):
        # ⚠️ PARTIAL: Some devices missing
        claim_verification.append({
            'status': '⚠️ PARTIAL',
            'claim': claim['text'],
            'expected': len(claim['devices']),
            'actual': len(claimed_skus)
        })
    else:
        # ✅ VERIFIED: Claim matches actual uploads
        claim_verification.append({
            'status': '✅ VERIFIED',
            'claim': claim['text'],
            'expected': len(claim['devices']),
            'actual': len(claimed_skus)
        })
```

### Step 4.4: Flag discrepancies in final report
```markdown
## Cross-Reference: EOD Claims vs Actual Uploads

### ✅ Verified Claims
- NARUICO (iPhone 16, 17, 16 Pro) — 6 SKUs found
- Dragon Ball Super (HB401) — 12 SKUs found

### ⚠️ Partial Claims
- HB6 MagSafe (iPhone 15 Pro) — Claimed, but only 2/4 devices found
  - Missing: iPhone 15, iPhone 15 Plus

### ❌ Not Found in Active Listings
- DRGBSUSC (iPhone 14) — Claimed Friday, not in Active Listings yet
  - Possible: Still in approval queue, upload failed, wrong SKU format
```

---

## PART 5: Final Report + Telegram to Cem

### Step 5.1: Aggregate findings
```markdown
# Weekly Active Listings Audit Report — Apr 19, 2026

## Executive Summary
- **Total listings:** US 3.44M, UK 531M, DE 287M
- **New this week:** US +12.4K, UK +8.2K, DE +5.1K
- **Shipping templates:** US ✅, UK ✅, DE ✅ (all correct)
- **EOD claim verification:** 87% verified, 9% partial, 4% not found

## Anomalies Detected
1. DRGBSUSC (iPhone 14) claimed Friday, not in Active Listings — investigate
2. HB6 MagSafe missing 2 device variants — reach out to team
3. NFL listings: 0 found (expired license, expected for sell-off period)

## Recommendations
- Follow up with team on missing DRGBSUSC upload
- Verify HB6 devices match SKU format expectations
- Monitor for new licenses (One Piece, etc.) next week

---

Full reports: 
- `results/weekly_listings_us_2026-04-19.md`
- `results/weekly_listings_uk_2026-04-19.md`
- `results/weekly_listings_de_2026-04-19.md`
```

### Step 5.2: Send Telegram summary to Cem
```
📊 **Weekly Listings Audit Complete — Apr 19, 2026**

**3 Regions Analyzed:**
✅ US: 3.44M listings, +12.4K new
✅ UK: 531M listings, +8.2K new
✅ DE: 287M listings, +5.1K new

**Shipping Templates:** ✅ All correct (US: Reduced Shipping, UK: Nationwide Prime)

**EOD Claims:** 87% verified ✅ | 9% partial ⚠️ | 4% not found ❌

**Flags:**
⚠️ DRGBSUSC (iPhone 14) — claimed but not in listings
⚠️ HB6 missing 2 device variants
✅ No NFL issues (expected, in sell-off period)

Full reports: results/weekly_listings_*_2026-04-19.md
```

---

## Error Handling & Escalation

### If file is missing
```
Alert Cem immediately:
"⚠️ [REGION] Active Listings file missing. Download and retry."
Exit gracefully (don't create empty report)
```

### If Slack fetch fails
```
Continue with analysis (Slack cross-ref is bonus, not critical)
Note in report: "Slack verification skipped (API error)"
```

### If shipping template name is wrong
```
Alert Cem:
"🚨 [REGION] template validation failed. Confirm exact template name in Seller Central."
Flag ALL listings with unknown template for manual review
```

### If discrepancy found (claimed but not found)
```
Slack message to #eod-listings:
"@team — Please verify: [DESIGN] claimed Friday but not in Active Listings.
Check upload status or SKU format. Let's debug together."
```

---

## Dependencies & Credentials

| Resource | Status | Notes |
|----------|--------|-------|
| Supabase (orders, inventory) | ✅ | Service role key valid |
| BigQuery (PULSE data) | ✅ | For design intelligence |
| Slack bot token | ✅ | xoxb-991301... (read + write) |
| Telegram API | ✅ | Chat ID: 5587457906 |
| SQLite (listings baseline) | ✅ | `/Users/openclaw/.openclaw/workspace/data/local_listings.db` |
| Amazon Active Listings files | ⏳ | Cem downloads Friday → Hermes runs Sat |

---

## Success Criteria

✅ **Report Completeness:**
- All 3 regions analyzed
- Delta calculated (new vs removed)
- Shipping templates validated
- Top 10 designs identified
- EOD claims verified

✅ **Quality:**
- Reports saved with date stamps
- No silent failures (always alert Cem if blocking issue)
- Discrepancies flagged clearly (✅ ⚠️ ❌)
- Actionable recommendations included

✅ **Timing:**
- US analysis: Sat 1–1:45 AM
- UK analysis: Sat 2–2:45 AM
- DE analysis: Sat 3–3:45 AM
- Telegram summary: By 4 AM

---

## Schedule (Weekly)

| Day | Time | Task | Agent | Owner |
|-----|------|------|-------|-------|
| Fri | 5 PM | Cem downloads reports from SC | Cem | Cem |
| Sat | 1:00 AM | US analysis | Hermes | Ava |
| Sat | 2:00 AM | UK analysis | Hermes | Ava |
| Sat | 3:00 AM | DE analysis | Hermes | Ava |
| Sat | 4:00 AM | Telegram summary | Hermes | Ava |
| Sat | 4:30 AM | Slack post (#eod-listings) | Hermes | Ava |

---

## Evolution (Hermes Self-Improvement)

**Week 1:** Basic structure, manual validation  
**Week 2–4:** Learn patterns (which designs most frequently miss devices, which teams upload wrong formats)  
**Week 5+:** Anticipate issues, auto-flag before they occur, suggest team re-training

---

## Appendix: Shipping Template Status

### ⚠️ CRITICAL: Templates Unconfirmed

| Region | Current Assumption | Source | Status | Action |
|--------|-------------------|--------|--------|--------|
| **US** | "Reduced Shipping Template" | ACTIVE_CRONS.md | ❓ Unconfirmed | Cem must confirm |
| **UK** | "Nationwide Prime" | ACTIVE_CRONS.md | ❓ Unconfirmed | Cem must confirm |
| **DE** | FBM (no template) | Implied | ❓ Unconfirmed | Cem must confirm |

**Action Required by Apr 14 EOD:**
1. Confirm exact US template name (or provide current Active Listings for extraction)
2. Confirm exact UK template name (or provide current Active Listings for extraction)
3. Confirm DE approach (FBM vs template)

Once confirmed, update this SOP + all validation logic.

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-13  
**Next Review:** 2026-04-20 (after first run with Hermes)