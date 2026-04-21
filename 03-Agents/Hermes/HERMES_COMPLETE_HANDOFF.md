# HERMES COMPLETE HANDOFF — Master SOP Index
**Effective:** 2026-04-13  
**Created:** Ava (with Advisor tool guidance)  
**Target:** Hermes (GLM 5.1, Nous Research)

---

## Executive Summary

You (Hermes) are taking over **5 weekly analysis crons + 1 new optimization loop** from Ava. This document is your master index for everything you need to run.

**Total weekly commitment:** 7–9 hours (spread across Sat/Mon)  
**Self-improvement:** By Week 10, you'll optimize this to 5–6 hours with zero errors.

---

## Your SOPs (Read These First)

### 1. **SOP_WEEKLY_ACTIVE_LISTINGS_AUDIT_HERMES.md** (14 KB)
**When:** Saturdays 1:00–3:00 AM ET  
**What:** Parse 6–9GB Active Listings files (US, UK, DE). Validate shipping templates. Cross-reference team claims.  
**Output:** Slack alerts + Telegram summary  
**Advisor Usage:** Edge cases (unknown templates, anomalies, discrepancies)  
**Read this FIRST if:** You're starting the weekly audit workflow

### 2. **SOP_WEEKLY_MOVERS_SALES_ANALYSIS.md** (19 KB)
**When:** Saturdays 3:00–4:30 AM + Mondays 5:00 AM  
**What:** Sales traffic analysis (CVR by type, device, region) + PULSE leaderboard + Karpathy loop price optimization  
**Output:** Markdown reports + Telegram summaries + price test implementation  
**Advisor Usage:** Test design decisions (stagger tests or run parallel?)  
**Read this SECOND if:** You're handling movers/sales analysis or price optimization

### 3. **SOP_SALES_ANALYTICS_API_ACTIONS.md** (19 KB)
**When:** Saturdays 4:30–6:00 AM ET (post-analysis window)  
**What:** Execute API-driven actions based on analytics insights. Example: Migrate US high-priority designs to Nationwide Prime template.  
**Output:** Dry-run validation, real execution, post-action monitoring, detailed reports  
**Advisor Usage:** High-risk decisions (migrate 800 SKUs? revert anomaly?)  
**Read this THIRD if:** You're implementing automated corrective actions  
**New Feature:** US Nationwide Prime migration for top designs

---

## Weekly Schedule

| Day/Time | Task | SOP | Duration | Status |
|----------|------|-----|----------|--------|
| **Sat 1:00 AM** | US Listings Analysis | SOP #1 | 45 min | Hermes takes over (was main) |
| **Sat 2:00 AM** | UK Listings Analysis | SOP #1 | 45 min | Hermes takes over (was main) |
| **Sat 3:00 AM** | DE Listings Analysis + Sales Traffic | SOP #1 + #2 | 30 min | Hermes takes over (was main) |
| **Sat 3:30 AM** | Karpathy Price Optimization | SOP #2 | 45 min | **NEW — Hermes autonomous** |
| **Sat 4:30 AM** | API-Driven Actions (Prime migration, etc.) | SOP #3 | 90 min | **NEW — Hermes autonomous** |
| **Sat 6:00 AM** | Telegram summary + Slack posts | All | 15 min | Hermes delivers |
| **Mon 5:00 AM** | PULSE Leaderboard Report | SOP #2 | 30 min | Hermes takes over (was main) |

**Total weekly time:** 5h 15m baseline (target: 3h 30m by Week 10)

---

## What You're Inheriting

### From Ava (Main Session)

**5 existing crons being handed over:**

1. ✅ **Weekly Listings Analysis — US** (Sat 1 AM)
   - Parse 6–9GB CSV, delta calculation
   - Validate shipping templates
   - Cross-reference EOD Slack claims

2. ✅ **Weekly Listings Analysis — UK** (Sat 2 AM)
   - Same as US, UK-specific flags
   - Samsung A-series, football licenses, HLBWH distribution

3. ✅ **Weekly Listings Analysis — DE** (Sat 3 AM)
   - Same as US/UK, champions movers analysis

4. ✅ **Weekly PULSE Leaderboard** (Mon 5 AM)
   - Top devices, designs, movers
   - Cross-region gap analysis
   - Champion velocity tracking

5. ⏳ **Mid-Week Shipping Template Audit** (Wed 2 AM)
   - Validate new listings (< 14 days)
   - Check against confirmed shipping templates

### New Features (Ava Created, Hermes Will Execute)

1. **Shipping Template Validation**
   - Confirmed from real data (DE Active Listings)
   - US: `Reduced Shipping Template`
   - UK: `Nationwide Prime` (inferred, needs confirmation via files)
   - DE: `Standardvorlage Amazon` + `Reduced Shipping Template`

2. **EOD Claims Cross-Reference**
   - Parse Slack #eod-listings Fri–Sun
   - Verify team claims against actual uploads
   - Flag discrepancies (✅ verified | ⚠️ partial | ❌ not found)

3. **Karpathy Loop Price Optimization** (NEW)
   - Autonomous testing on small SKU cohorts
   - Week 1: NARUICO raise test
   - Week 2+: Staggered tests + expansion of winners
   - Expected ROI: +$5K–$10K/month

4. **Advisor Tool Integration**
   - Use Opus 4.6 for edge cases
   - Ask when: unknown templates, anomalies, test design decisions
   - Let Advisor guide your judgment on escalation priority

---

## Key Data & Schemas

### Supabase Tables You'll Query

```sql
-- Orders
SELECT * FROM orders WHERE paid_date >= CURRENT_DATE - INTERVAL '7 days'

-- Price experiments (new)
CREATE TABLE price_experiments (
  test_id TEXT PRIMARY KEY,
  design_code TEXT,
  test_type TEXT,  -- PRICE_RAISE, PRICE_LOWER
  control_price DECIMAL,
  test_price DECIMAL,
  sku_list TEXT[],
  start_date DATE,
  end_date DATE,
  status TEXT  -- ACTIVE, COMPLETED, FAILED
)

-- Price change log
CREATE TABLE price_change_log (
  sku TEXT,
  old_price DECIMAL,
  new_price DECIMAL,
  test_id TEXT,
  timestamp TIMESTAMP
)

-- Active listings (weekly snapshots)
SELECT seller_sku, asin, price, quantity, fulfillment_channel FROM listings_current
```

### Amazon Active Listings Columns (You'll Parse)

```
Column 1: item-name
Column 10: product-id-type
Column 27: fulfillment-channel  (AMAZON vs MERCHANT)
Column 40: merchant-shipping-group  (CRITICAL for validation)
Column 5: price
Column 6: quantity
Column 7: open-date
```

### Shipping Templates (Confirmed)

**DE (Real data, Apr 4, 2026):**
- `Standardvorlage Amazon` — 1.43M listings (62.5%)
- `Reduced Shipping Template` — 1.20M listings (52.4%)
- `Prime vorlage` — 32 listings (0.001%)

**US (Inferred):**
- `Reduced Shipping Template` — Assume correct

**UK (Inferred):**
- `Nationwide Prime` — Assume correct (needs confirmation)

---

## Advisor Tool Usage — When to Invoke

### Scenario 1: Unknown Shipping Template

```
Question: "I found 500 UK listings with template='Mystery Template'.
Is this a test, error, or needs investigation?"

Advisor helps: Risk assessment, escalation priority, next steps
```

### Scenario 2: Anomalous Spike

```
Question: "Found 8,500 new listings for single design with today's date.
Is this a bulk upload, data error, or legitimate?"

Advisor helps: Pattern analysis, decision (flag vs. continue)
```

### Scenario 3: Test Design Decision

```
Question: "Should I run 3 price tests simultaneously or stagger them?"

Advisor helps: Tradeoff analysis (speed vs. data quality)
```

### Scenario 4: Discrepancy Escalation

```
Question: "Team claimed design went live Friday, but 0 listings found.
Should I flag this as high-priority or investigate first?"

Advisor helps: Risk severity, communication strategy
```

---

## Self-Improvement Path

### Week 1: Baseline Execution
- Run all crons exactly as documented
- Ask Advisor frequently (high oversight)
- Document what went smoothly + what was hard

### Week 2–4: Skill Creation Phase
- After each cron, create a skill card (`memory/skills/`)
  - SKU parsing patterns
  - Claim extraction regex
  - Anomaly detection heuristics
  - Price test design decisions
- Add to `memory/skills/SKILL_INDEX.md`
- Update SOP with learned patterns

### Week 5–8: Optimization Phase
- Skills are now mature
- Use skills before invoking Advisor (Advisor only for novel cases)
- Performance: 3h 30m → 2h 30m
- Error rate: High → Near zero

### Week 10+: Production Grade
- You run these crons autonomously
- Advisor only for truly novel edge cases
- Can hand off to another agent if needed (well-documented)
- Continuous learning continues

---

## Handoff Checklist

Before you start on Saturday, Apr 19:

- [ ] Read SOP_WEEKLY_ACTIVE_LISTINGS_AUDIT_HERMES.md
- [ ] Read SOP_WEEKLY_MOVERS_SALES_ANALYSIS.md
- [ ] Verify shipping template names (US/UK confirmation pending)
- [ ] Confirm Supabase tables exist + you have access
- [ ] Test Slack bot token (post test message to #eod-listings)
- [ ] Test Telegram API (send test message to Cem)
- [ ] Verify Big Commerce API credentials
- [ ] Verify Shopify API credentials
- [ ] Create `memory/skills/SKILL_INDEX.md` (empty, ready to populate)

---

## Critical Confirmations Needed from Cem (by Apr 18)

1. ✅ US shipping template: `Reduced Shipping Template` — CONFIRM?
2. ✅ UK shipping template: `Nationwide Prime` — CONFIRM?
3. ✅ DE approach: Uses both `Standardvorlage Amazon` + `Reduced Shipping Template` — CONFIRM?

If NOT confirmed, I'll extract from your upcoming Active Listings files.

---

## Escalation Matrix

| Situation | Advisor? | Escalate to Cem? | Action |
|-----------|----------|------------------|--------|
| Unknown shipping template | ✅ Ask | After Advisor | Alert as INFO |
| Data anomaly detected | ✅ Ask | After Advisor | Flag for investigation |
| Price test fails (negative ROI) | ✅ Ask | YES | Halt expansion, revert price |
| Discrepancy: claimed ≠ actual | ✅ Ask | After Advisor | Tag team in Slack |
| Novel situation (never seen before) | ✅ Ask | After Advisor | Let Advisor guide |
| Routine execution (parsing, deltas) | ❌ No | NO | Just execute |

---

## Communication Templates

### Slack #eod-listings Alert (Shipping Template Issue)

```
⚠️ **US Listings Alert — Shipping Template**

I found 350 new listings with template='Standard Shipping' (not 'Reduced Shipping Template').

Status: Unclear if this is legitimate or configuration error.

@team — Can you confirm if this is a test or if templates changed?

I'll monitor for expansion or rollback next week. FYI @Cem
```

### Telegram Summary (Weekly Results)

```
📊 **Weekly Audit Complete — Apr 19, 2026**

✅ US: 3.44M listings, +12.4K new, 97.3% template compliance
✅ UK: 531M listings, +8.2K new, 100% template compliance
✅ DE: 287M listings, +5.1K new, 99.8% template compliance

⚠️ 1 discrepancy: DRGBSUSC (claimed Fri, not in listings yet)

📈 Top mover: NEWLICENSE (+340% velocity)
📉 Watch list: NFL_LEGACY (-95%, expires Jun 29)

🎯 Price test: NARUICO raise to $21.95 (100 SKUs monitoring)

See full reports: results/weekly_*_2026-04-19.md
```

### Advisor Consultation Template

```
**Your question:**
"I found [SITUATION]. Should I [OPTION A] or [OPTION B]?"

**Context:**
- Frequency: [How often does this occur?]
- Risk: [What's at stake?]
- Data: [What do we know?]

**Advisor will help:**
- Tradeoff analysis
- Escalation priority
- Risk assessment
- Next steps

→ You decide and act (not Advisor)
```

---

## Reference Files

| Path | Purpose |
|------|---------|
| `~/Vault/01-Wiki/31-listings-management/SHIPPING_TEMPLATE_MASTER.md` | Confirmed shipping template names + extraction process |
| `~/Vault/01-Wiki/04-shipping/amazon_shipping_templates.md` | Business rule: 100% Reduced Shipping compliance target |
| `~/Vault/01-Wiki/infrastructure/ACTIVE_CRONS.md` | Master cron schedule (7 crons you inherit, plus details) |
| `~/Vault/03-Agents/Hermes/CRON_ASSIGNMENTS.md` | Your role + responsibilities (created Apr 13) |
| `/Users/openclaw/.openclaw/workspace/TOOLS.md` | API keys, credentials, service configs |
| `/Users/openclaw/.openclaw/workspace/data/local_listings.db` | SQLite baseline for delta calculations |

---

## Success Criteria

✅ **Execution (Week 1–2)**
- All 5 crons run on schedule
- Reports are complete + accurate
- Slack/Telegram alerts fire when needed
- Advisor tool consulted for ambiguous cases

✅ **Self-Improvement (Week 3–10)**
- Skills created: 5+ reusable skill cards
- Performance: 20% time reduction by Week 4
- Error rate: Near zero by Week 8
- Production-grade by Week 10

✅ **Price Optimization (Week 1+)**
- Test cohorts designed + implemented
- 7-day monitoring windows completed
- Winning prices expanded to full designs
- Learning captured: elasticity models for champions

---

## Contact & Support

**Questions about:**
- Execution: Ask Advisor, then escalate to Cem if needed
- SOP clarity: Check relevant SOP, then ask Cem
- Edge cases: Invoke Advisor tool
- Novel situations: Advisor + escalate to Cem

**Cem's contact:** Telegram 5587457906  
**Advisor (Opus 4.6):** Invoke mid-thought via reasoning

---

## Final Notes

1. **This is autonomous work.** You run these crons independently. Advisor is guidance, not approval.

2. **Self-improvement is mandatory.** Each week, you get better. By Week 10, this is production-grade.

3. **Escalate intelligently.** Not every anomaly needs Cem. Advisor helps you decide.

4. **Karpathy loop is the future.** Price optimization scales with your learning. Week 10 you'll run tests that Ava would never have thought of.

5. **You own the data.** These reports are your deliverables. Quality matters.

---

**Document Version:** 1.0  
**Status:** Ready for Hermes to take over  
**Start Date:** Saturday, Apr 19, 2026 @ 1:00 AM  
**First Review:** Monday, Apr 21, 2026 (after first weekend)

**Good luck, Hermes. Make us proud.** 🚀