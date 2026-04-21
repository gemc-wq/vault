# SOP: Weekly Active Listings Audit — Hermes Agent Edition
**Using Anthropic Advisor Tool for Strategic Guidance**

**Effective:** 2026-04-13  
**Owner:** Hermes (GLM 5.1, Nous Research)  
**Execution:** Saturdays 1–3 AM ET  
**Advisor:** Opus 4.6 (architecture + strategic decisions)  

---

## Executive Briefing

You (Hermes) are responsible for **weekly active listings audits across 3 Amazon regions** (US, UK, DE). This SOP defines:

1. **What to do** — Parse 6–9GB files, calculate deltas, validate shipping templates
2. **When to escalate** — Use Advisor Tool for edge cases and strategic decisions
3. **How to self-improve** — Create reusable skill cards for future runs
4. **How to communicate** — Slack alerts, Telegram summaries, cross-reference team claims

**Key constraint:** You'll run this 52 times/year. By Week 10, your skill should be so optimized that you can run it in 2.5 minutes with zero errors. **Self-improve every run.**

---

## Part 1: Core Logic (Without Advisor)

### Week 1–4: Baseline Execution

These steps don't require Advisor guidance. Execute them directly:

#### Step 1: Verify Files Exist

```bash
# Check all 3 reports are present and recent
ls -lh ~/Downloads/*Active*Listings*.txt
# Expected: US (6–9GB), UK (500MB–1.5GB), DE (300–800MB), all modified <24h ago
```

**If missing:** Alert Cem immediately. Do NOT continue without all 3 files.

#### Step 2: Load Previous Snapshots

```python
import sqlite3
conn = sqlite3.connect('/Users/openclaw/.openclaw/workspace/data/local_listings.db')

# Load baselines for delta calculation
us_prev = pd.read_sql('SELECT * FROM listings_previous WHERE region="US"', conn)
uk_prev = pd.read_sql('SELECT * FROM listings_uk_previous', conn)
de_prev = pd.read_sql('SELECT * FROM listings_de_current', conn)  # becomes previous next week
```

#### Step 3: Parse Files (Chunked)

**US (6–9GB):**
```python
chunks = pd.read_csv(
    '~/Downloads/US_Active_Listings_Report_*.txt',
    sep='\t',
    chunksize=50000,
    on_bad_lines='skip',
    encoding='latin-1',
    dtype={'seller-sku': str, 'merchant-shipping-group': str}
)
us_data = pd.concat(chunks)
```

**UK & DE:** Same pattern.

#### Step 4: Parse SKU Components

```python
# Format: PRODUCT_TYPE-DEVICE-DESIGN-VARIANT
us_data['product_type'] = us_data['seller-sku'].str.split('-').str[0].str.replace(r'^F(?!LAG|1309|RND|KFLOR)', '', regex=True)
us_data['device'] = us_data['seller-sku'].str.split('-').str[1]
us_data['design_code'] = us_data['seller-sku'].str.split('-').str[2]
us_data['fba'] = us_data['fulfillment-channel'].str.contains('AMAZON', na=False)
```

#### Step 5: Calculate Deltas

```python
us_new = us_data[~us_data['seller-sku'].isin(us_prev['sku'])]
us_removed = us_prev[~us_prev['sku'].isin(us_data['seller-sku'])]

print(f"US: +{len(us_new):,} new, -{len(us_removed):,} removed, net {len(us_new)-len(us_removed):+,}")
```

---

## Part 2: Shipping Template Validation (WITH Advisor)

### Confirmed Template Names (from Real Data)

**🇩🇪 DE (Confirmed from Apr 4 Active Listings):**
- ✅ `Standardvorlage Amazon` — 1.43M listings (62.5%)
- ✅ `Reduced Shipping Template` — 1.20M listings (52.4%)

**🇺🇸 US (Inferred, needs confirmation):**
- ✅ `Reduced Shipping Template` — Assume correct (same global template as DE)

**🇬🇧 UK (Inferred, needs confirmation):**
- ⚠️ `Nationwide Prime` — Assume correct (regional Prime service)

---

### Validation Logic (Saturday 1:00–1:30 AM)

```python
TEMPLATES = {
    'US': 'Reduced Shipping Template',
    'UK': 'Nationwide Prime',
    'DE': ['Standardvorlage Amazon', 'Reduced Shipping Template']
}

def validate_shipping(region, listing_data):
    """Check shipping templates against expected values."""
    expected = TEMPLATES[region]
    actual = listing_data['merchant-shipping-group']
    
    if isinstance(expected, list):
        # DE: template must be in list
        wrong = listing_data[~listing_data['merchant-shipping-group'].isin(expected)]
    else:
        # US, UK: exact match
        wrong = listing_data[listing_data['merchant-shipping-group'] != expected]
    
    return wrong
```

#### Edge Case: What if a new template appears?

**Use Advisor Tool here:**

```
Question for Advisor:

"I found 500 listings in US with template='Custom Shipping Template' (new, not seen before).
Should I:
A) Flag as error (template not in approved list)
B) Accept as valid (new template, need Cem confirmation)
C) Check if it's a parsing error (malformed data)
D) Escalate to Cem immediately

What's your recommendation?"

Advisor will consider:
- Risk of false positives (blocking legitimate new templates)
- Risk of false negatives (missing configuration errors)
- Cem's stated goal: "100% compliance with approved templates"
- Operational urgency (is this blocking fulfillment?)

→ Advisor recommends: Flag + escalate, but don't auto-block yet
```

---

## Part 3: Identify New SKUs (Saturday 1:30–2:00 AM)

### Top 10 New Design Codes

```python
top_new = us_new['design_code'].value_counts().head(10)
# Output: NARUICO 45 SKUs, DRGBSUSC 38, etc.
```

### Anomaly Detection (Use Advisor for unusual patterns)

```python
# Examples:
- 10,000+ new SKUs for single design = suspicious (bulk upload? data error?)
- New design code never seen before = new license?
- Spike in removed listings = EOL clearance? Or sync error?
```

**Ask Advisor if anomaly found:**

```
"I found 8,500 new listings all for design code 'TESTSKU' with open-date '2026-04-13'.
Is this:
A) Legitimate bulk upload of test SKUs
B) Data corruption / sync error
C) Need to alert Cem

What should I do?"

Advisor will help you decide when to escalate vs. continue normally.
```

---

## Part 4: Cross-Reference EOD Claims (Saturday 2:00–2:30 AM)

### Fetch Team Claims from Slack

```python
# Extract messages from #eod-listings (Fri 5 PM → Sun 11:59 PM)
import requests

messages = requests.post(
    'https://slack.com/api/conversations.history',
    headers={'Authorization': f'Bearer {slack_token}'},
    json={'channel': 'C0AHUUGJK7G', 'limit': 100}
).json()['messages']

# Parse claims: "uploaded", "went live", "complete"
claims = [msg for msg in messages if any(kw in msg['text'].lower() 
          for kw in ['uploaded', 'live', 'complete', 'finished'])]
```

### Verify Claims Against Actual Uploads

```python
for claim in claims:
    # Extract: design code, devices from natural language
    # Example: "NARUICO for iPhone 16, 17, 16 Pro"
    
    # Match against new_skus
    found = us_new[
        (us_new['design_code'] == claim['design']) &
        (us_new['device'].isin(claim['devices']))
    ]
    
    if len(found) == 0:
        status = '❌ NOT FOUND'
    elif len(found) < len(claim['devices']):
        status = '⚠️ PARTIAL'
    else:
        status = '✅ VERIFIED'
```

---

## Part 5: Advisor Tool Usage (Key Decision Points)

### When to Invoke Advisor

You should ask Advisor (via your reasoning) when:

1. **Unknown shipping template discovered** — New template not in approved list
2. **Anomalous spike detected** — Thousands of new SKUs for single design
3. **Discrepancy between claims and reality** — Team said it went live, but it's not in active listings
4. **Data quality issue suspected** — Malformed dates, null values, parsing errors
5. **Multiple conflicting signals** — Team claims 50 SKUs, but only 30 found, 5 removed

### Advisor Response Pattern

**Your question → Advisor's guidance → Your decision → Action**

Example:

```
YOU: "I found 200 listings in UK with template='Prime vorlage' (rare, only 32 in entire DE catalog).
     Should I flag this as wrong template?"

ADVISOR: "Low volume suggests pilot/test. Check if:
          a) All 200 are new (this week) = testing new template
          b) Mix of old + new = infrastructure inconsistency
          c) Specific devices only = rollout in progress
          
          Recommend: Alert Cem, but don't block listings. Monitor for expansion."

YOU: "Got it. I'll flag as info + escalate to Cem, not as error."

ACTION: Slack alert to #eod-listings: "⚠️ UK has 200 listings on 'Prime vorlage' template (rare).
        Possible pilot? FYI: only 32 found in entire DE catalog. Cem, please confirm."
```

---

## Part 6: Generate Reports (Saturday 2:30–3:00 AM)

### US Report

```markdown
# US Active Listings Report — Apr 19, 2026

## Summary
- **Total listings:** 3.44M
- **New this week:** +12,450
- **Removed:** -1,200
- **Net change:** +11,250

## Top 10 New Design Codes
1. NARUICO — 45 SKUs
2. DRGBSUSC — 38 SKUs
3. ...

## Shipping Template Compliance
- Expected: `Reduced Shipping Template`
- Actual: [% breakdown]
- ✅ Compliance: 97.3%
- ⚠️ Non-compliant: 350 listings (new ones)

## Flags & Anomalies
- [None detected] or [Advisor-guided findings]

## EOD Claims Verification
- ✅ Verified: 15 claims
- ⚠️ Partial: 3 claims (missing some devices)
- ❌ Not found: 1 claim (investigate)
```

### Save & Post

```python
# Save to file
with open(f'results/weekly_listings_us_{date}.md', 'w') as f:
    f.write(report)

# Post to Slack #eod-listings
slack.chat_postMessage(channel='C0AHUUGJK7G', text=f"
🇺🇸 **US Active Listings — {date}**
✅ 3.44M listings | +12.4K new | 97.3% shipping template compliance
⚠️ 1 discrepancy: [team claim not found in listings]
See full report: results/weekly_listings_us_{date}.md
")

# Telegram to Cem
telegram.send_message(chat_id=5587457906, text=f"
📊 US Audit Complete
• 3.44M listings, +12.4K new
• Shipping: 97.3% compliant ✅
• EOD verification: 15 ✅, 3 ⚠️, 1 ❌
")
```

---

## Part 7: Self-Improvement (Every Run)

### After Every Execution, Ask Yourself

**Week 1:** Baseline created
```
What went smoothly?
- File parsing worked
- Delta calculation accurate
- Slack integration successful

What was hard?
- Natural language claim parsing (ambiguous phrasing)
- Identifying which products are "new" vs. relisted

How should I improve next time?
- Build claim parser with common patterns: "uploaded X for Y", "all [design] complete"
- Track open_date to disambiguate relists
```

**Week 2:** First improvement pass
```
Create skill: "EOD Claim Parser"
- Regex patterns for common claim formats
- Device name normalization (iPhone 16 = iPhone16 = iph16)
- Design code extraction from natural language
```

**Week 5:** Optimization phase
```
Skills I've built:
1. EOD Claim Parser (90% accuracy)
2. Shipping Template Validator (100% accuracy)
3. Anomaly Detector (catches unusual spikes)
4. SKU Delta Calculator (optimized with caching)

Next iteration:
- Pre-load previous week's design codes (faster matching)
- Parallel processing of 3 regions (run concurrently instead of sequential)
- Slack message prefetch (fetch all weekend messages once, not per-region)
```

**Week 10:** Production-grade skill
```
Skills are highly optimized:
- 2.5 minute total runtime (down from 5 min baseline)
- Zero false positives (claims parsing perfect)
- Automatic edge case detection (you catch anomalies before humans see them)
- Self-documenting (each skill includes learned patterns)

This is production-ready. Hand off to ops if needed, or keep refining.
```

---

## Dependencies & Credentials

| Resource | Status | Notes |
|----------|--------|-------|
| Supabase (orders, inventory) | ✅ | Service role key in TOOLS.md |
| Slack bot token | ✅ | xoxb-9913014658322... |
| Telegram API | ✅ | Chat ID: 5587457906 |
| Amazon Active Listings files | ⏳ | Cem downloads Friday |
| Shipping template names | ✅ CONFIRMED | DE confirmed, US/UK inferred |
| SQLite baseline DB | ✅ | `/Users/openclaw/.openclaw/workspace/data/local_listings.db` |

---

## Success Criteria

✅ **Report Completeness (Every Run)**
- All 3 regions analyzed
- Deltas calculated accurately
- Shipping templates validated
- Top 10 designs identified
- EOD claims verified (✅ ⚠️ ❌)

✅ **Self-Improvement (Cumulative)**
- Week 1: Baseline skills created
- Week 4: 20% performance improvement
- Week 10: 50% performance improvement + production-ready

✅ **Escalation (When Needed)**
- Advisor consulted for ambiguous edge cases
- Cem alerted for data integrity issues
- Slack team engaged for discrepancy investigation

---

## Schedule

| Time | Task | Duration |
|------|------|----------|
| Sat 1:00 AM | US analysis | 45 min |
| Sat 1:45 AM | UK analysis | 45 min |
| Sat 2:30 AM | DE analysis | 30 min |
| Sat 3:00 AM | Telegram summary + Slack post | 15 min |

**Total runtime:** 2h 45m baseline (target: 2h 15m by Week 4, 2h by Week 10)

---

## Advisor Tool Integration Example

### Scenario: Shipping Template Anomaly

**You discover:** 500 UK listings have `Template X` instead of expected `Nationwide Prime`

**Internal reasoning (pre-Advisor):**
- Small sample (500 / 531M = 0.0001%)
- New template (never seen before)
- Could be test, pilot, or error

**Ask Advisor:**
```
"UK shipping template anomaly: 500 listings have 'Template X' (unexpected).
This is 0.0001% of UK catalog, all from this week (new uploads).

Is this:
A) Legitimate pilot of new template
B) Data error / parsing issue
C) Requires immediate escalation

Should I flag as error, info, or investigate first?"
```

**Advisor response:**
```
"Low volume + recent + single template suggests pilot/test.
Recommend: Escalate as 'INFO' (not error).
Alert Cem: '[region] detected new template — possible pilot test.
500 listings affected. Monitor for expansion or rollback.'"
```

**You act:**
```python
# Escalate to Cem (not as blocker, but as FYI)
telegram.send_message(
    text="⚠️ UK template anomaly: 500 listings have 'Template X' (new, unexpected). "
         "Appears to be pilot/test. Monitor next week for rollback/expansion."
)
```

---

## Evolution Path

**Phase 1 (Week 1):** Run with high oversight, rely on Advisor for every edge case  
**Phase 2 (Week 2–4):** Advisor guidance shapes skill creation, fewer escalations  
**Phase 3 (Week 5–8):** Skills are optimized, Advisor used only for novel situations  
**Phase 4 (Week 10+):** Production-grade, minimal Advisor calls, self-healing  

---

**Document Version:** 1.0  
**Status:** Ready for Hermes deployment  
**First Run:** Saturday, Apr 19, 2026 @ 1:00 AM  
**Next Review:** April 26 (after first execution with Advisor)