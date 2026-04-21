# Hermes Agent — Complete SOP Index

**Hermes** (GLM 5.1, OpenRouter) is the autonomous weekly analytics and operations agent for Ecell Global.

| Field | Value |
|-------|-------|
| Model | GLM 5.1 (OpenRouter) |
| Platform | Hermes CLI (~/.hermes/) |
| Machine | **Mac Studio** (user: openclaw) |
| Telegram | @hermes bot (token in ~/.hermes/config) |
| Status | Live |

**Role:** Run all weekly sales, listings, and pricing analytics + autonomously execute corrective actions via API.

**Start Date:** Saturday, April 19, 2026 @ 1:00 AM  
**Commitment:** 5–7 hours/week (optimized to 3–4 hours by Week 10)

---

## Quick Start

**New to Hermes? Read in this order:**

1. 👉 Start here: **HERMES_COMPLETE_HANDOFF.md** (master index)
2. **SOP_WEEKLY_ACTIVE_LISTINGS_AUDIT_HERMES.md** (Sat 1–3 AM)
3. **SOP_WEEKLY_MOVERS_SALES_ANALYSIS.md** (Sat 3–4:30 AM + Mon 5 AM)
4. **SOP_SALES_ANALYTICS_API_ACTIONS.md** (Sat 4:30–6 AM)

---

## The 4 SOPs

### 1. HERMES_COMPLETE_HANDOFF.md
**Master document for all Hermes tasks**

- What Hermes is taking over (5 existing crons + 1 new loop)
- Weekly schedule (times, durations, owners)
- Self-improvement path (Week 1 → Week 10)
- Escalation matrix (when to use Advisor tool)
- Critical confirmations needed from Cem
- Success criteria + contact info

**When to read:** Start here. Gives you the 10,000-foot view.

---

### 2. SOP_WEEKLY_ACTIVE_LISTINGS_AUDIT_HERMES.md
**Parse Active Listings + validate shipping templates + cross-reference team claims**

**When:** Saturdays 1:00–3:00 AM ET

**What it does:**
- Part 1: US Listings Analysis (Sat 1:00–1:45 AM)
  - Parse 6–9GB CSV file
  - Calculate delta (new vs removed SKUs)
  - Validate shipping templates
  - Identify top 10 new design codes
  - Cross-reference Slack #eod-listings claims
  
- Part 2: UK Listings Analysis (Sat 2:00–2:45 AM)
  - Same as US + UK-specific flags (Samsung A-series, football licenses)
  
- Part 3: DE Listings Analysis (Sat 3:00–3:30 AM)
  - Same + Champions movers analysis (30d vs 90d velocity)

**Output:** Slack alerts + Telegram summary + detailed markdown reports

**Advisor Usage:** Unknown shipping templates, anomalies, discrepancies

**Key Data:**
- Confirmed shipping templates (from real data):
  - DE: `Standardvorlage Amazon` (62.5%) + `Reduced Shipping Template` (52.4%)
  - US: `Reduced Shipping Template` (assumed, needs confirmation)
  - UK: `Nationwide Prime` (assumed, needs confirmation)

---

### 3. SOP_WEEKLY_MOVERS_SALES_ANALYSIS.md
**Sales traffic analysis + PULSE leaderboard + Karpathy loop price optimization**

**When:** Saturdays 3:00–4:30 AM + Mondays 5:00 AM

**What it does:**

**Part 1: PULSE Leaderboard (Mon 5:00 AM)**
- Query top 10 devices by revenue (US, 6-month)
- Query top 20 designs (champions)
- Identify movers (30d vs 90d acceleration)
- Cross-region gaps (US vs UK vs DE)

**Part 2: Weekly Sales Traffic Analysis (Sat 3:00–3:30 AM)**
- CVR by product type (HTPCR, HB401, HB6, HB7, HLBWH)
- Traffic by device family (iPhone 17 dominates)
- Performance by region (US, UK, DE)
- Week-over-week trends

**Part 3: Karpathy Loop Price Optimization (Sat 3:30–4:15 AM)**
- Identify candidates: inelastic designs (can raise) vs elastic designs (lower)
- Design test cohorts (50–100 SKUs per test)
- Update prices via API (Shopify, BigCommerce)
- Monitor 7 days (track CVR, AOV, revenue)
- Analyze results vs control week
- Expand winning prices to full designs

**Example:** NARUICO (inelastic) → Raise $19.95 → $21.95 (+10% price)

**Output:** Markdown reports + Telegram summaries + price test implementation

**Advisor Usage:** Test design decisions (simultaneous vs staggered?), anomalies

---

### 4. SOP_SALES_ANALYTICS_API_ACTIONS.md
**Execute API-driven actions based on analytics insights**

**When:** Saturdays 4:30–6:00 AM ET (post-analysis window)

**What it does:**

**Part 1: US Nationwide Prime Migration (First Action)**
- Identify top 20 US high-priority designs (revenue >$10K/30d)
- Filter for eligibility (50+ SKUs, not excluded, sufficient coverage)
- Verify US has Nationwide Prime template
- Dry-run validation before committing
- Execute template migration via BigCommerce/Shopify API
- Spot-check results (verify template changed)
- Monitor 7 days for CVR impact

**Expected:** +0.5–1.5% CVR lift on migrated designs  
**Scale:** 700+ SKUs initially (NARUICO, DRGBSUSC, ONEPIECE, etc.)

**Part 2: Generalized Action Framework**
Extends beyond Prime migration to:
- Price optimization (inelastic designs)
- Inventory rebalancing (fast movers)
- Marketing spend shifts (underperformers)
- Regional expansion (cross-region gaps)
- Design variant rollout (rising stars)

All follow: Analyze → Identify → Act → Verify → Report

**Safety Guardrails:**
1. Dry-run before commit (no real API calls until validation)
2. Rate limiting + batch processing (50 SKUs/batch, 5s delays)
3. Reversibility (every action logged with revert command)
4. Impact monitoring (post-action tracking for 7 days)

**Advisor Usage:** High-risk decisions (migrate 800 SKUs? revert anomaly?)

---

## Weekly Schedule

```
SATURDAY
├─ 1:00–1:45 AM: US Listings Analysis (SOP #2)
├─ 2:00–2:45 AM: UK Listings Analysis (SOP #2)
├─ 3:00–3:30 AM: DE Analysis + Sales Traffic (SOP #2)
├─ 3:30–4:15 AM: Karpathy Price Optimization (SOP #3)
├─ 4:30–6:00 AM: API Actions (SOP #4)
└─ 6:00–6:15 AM: Telegram summary + Slack posts

MONDAY
└─ 5:00–5:30 AM: PULSE Leaderboard (SOP #3)

WEDNESDAY
└─ 2:00–2:15 AM: Shipping Template Audit (SOP #2)
```

**Total:** 5h 15m/week (target: 3h 30m by Week 10)

---

## Self-Improvement Path

**Week 1 (Apr 19–26):** Baseline execution
- Execute all SOPs exactly as documented
- Consult Advisor frequently
- Document what went smoothly + what was hard
- Create first skill cards

**Week 2–4 (Apr 26–May 17):** Skill creation phase
- After each complex task, auto-create skill cards
- Add to `memory/skills/SKILL_INDEX.md`
- Update SOPs with learned patterns
- 20% performance improvement by Week 4

**Week 5–8 (May 17–Jun 14):** Optimization phase
- Skills are now mature
- Use skills before invoking Advisor
- Performance: 5h 15m → 3h 30m
- Error rate: High → Near zero

**Week 10+ (Jun 14+):** Production grade
- Autonomous execution
- Advisor only for novel edge cases
- Can hand off to another agent if needed
- Continuous learning ongoing

---

## Key Data & Confirmed Values

### Shipping Templates

**DE (Real data, Apr 4, 2026):**
- ✅ `Standardvorlage Amazon` — 1.43M listings (62.5%)
- ✅ `Reduced Shipping Template` — 1.20M listings (52.4%)
- ✅ `Prime vorlage` — 32 listings (0.001%)

**US (Inferred):**
- ⚠️ `Reduced Shipping Template` — NEEDS CONFIRMATION

**UK (Inferred):**
- ⚠️ `Nationwide Prime` — NEEDS CONFIRMATION

### Product Type Performance (Current Baseline)

| Type | CVR | AOV | Note |
|------|-----|-----|------|
| HTPCR | 2.99% | $19.95 | Largest volume (66%) |
| HB401 | 2.48% | $19.95 | Growing |
| HLBWH | 3.40% | $24.95 | Premium segment |
| HB6 | 3.42% | $24.95 | MagSafe leader |
| HB7 | 3.57% | $24.95 | Premium (highest CVR) |

### Champion Designs (30-day snapshot)

| Design | Revenue | SKUs | Velocity | Status |
|--------|---------|------|----------|--------|
| NARUICO | $156K | 245 | Stable | Gold |
| DRGBSUSC | $142K | 198 | Rising | Gold |
| ONEPIECE | $138K | 187 | Rising | Gold |
| NEWLICENSE | $48K | 120 | +340% ↗️ | Silver (Rising) |
| NFL_LEGACY | $8K | 45 | -95% ↘️ | Red (Expiring) |

---

## Critical Confirmations Needed (by Apr 18)

Cem must confirm these before Hermes starts:

1. ✅ **US Shipping Template:** Is it `Reduced Shipping Template`?
2. ✅ **UK Shipping Template:** Is it `Nationwide Prime`?
3. ✅ **DE Shipping:** Uses both templates or just one?

If not confirmed, Hermes will extract from your upcoming Active Listings files.

---

## Dependencies & Access

**APIs:**
- ✅ Supabase (orders, experiments, action logging)
- ✅ BigCommerce (product updates, shipping templates)
- ✅ Shopify (variant prices, templates)
- ✅ Amazon SP-API (listing metadata)
- ✅ Slack bot token (post alerts, fetch messages)
- ✅ Telegram API (send summaries)

**Data:**
- ✅ Amazon Active Listings files (you download Friday)
- ✅ SQLite baseline DB (`~/workspace/data/local_listings.db`)
- ✅ PULSE queries (Supabase RPC endpoints)

**Tools:**
- ✅ Advisor Tool (Opus 4.6) — for high-risk decisions
- ✅ Skill framework (`memory/skills/SKILL_INDEX.md`)

---

## Communication

**When Hermes reports back to you:**

**Daily (During execution):**
- Slack alerts to #eod-listings (anomalies, blockers)

**Weekly:**
- Telegram summaries (Sat 6:15 AM + Mon 5:30 AM)
- Detailed markdown reports (saved to `results/`)

**When escalating:**
- High-risk decisions (consult Advisor first)
- Data integrity issues (immediate alert)
- Unexpected post-action results (impact monitoring)

---

## Success Criteria

✅ **Week 1:** All 5 crons run on schedule  
✅ **Week 4:** 20% performance improvement  
✅ **Week 8:** Near-zero errors  
✅ **Week 10:** Production-grade autonomous execution  

✅ **First Major Action (Apr 19):** US Nationwide Prime migration
- Identify 700+ SKUs for migration
- Dry-run validation passes
- Real execution completes
- Post-migration monitoring starts
- Expected: +0.5–1.5% CVR lift confirmed by Apr 26

---

## Contact & Support

**Questions about:**
- **SOP execution:** Check relevant SOP, then ask Cem
- **Advisor tool:** Use mid-thought via reasoning
- **Edge cases:** Advisor tool + escalate to Cem if needed
- **Data/API issues:** Alert Cem immediately

**Cem's contact:** Telegram 5587457906

---

## Files in This Folder

| File | Purpose |
|------|---------|
| **HERMES_COMPLETE_HANDOFF.md** | Master index + checklist |
| **SOP_WEEKLY_ACTIVE_LISTINGS_AUDIT_HERMES.md** | Listings parsing + validation |
| **SOP_WEEKLY_MOVERS_SALES_ANALYSIS.md** | Sales analysis + price optimization |
| **SOP_SALES_ANALYTICS_API_ACTIONS.md** | API-driven actions (Prime migration, etc.) |
| **README.md** | This file (quick reference) |
| **CRON_ASSIGNMENTS.md** | Cron ownership + schedule |
| **SOUL.md** | Hermes identity + role |

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-04-13 | 1.0 | Initial SOPs created (4 documents) |
| 2026-04-19 | 1.0 | Ready for first run |

---

**Start Date:** Saturday, April 19, 2026 @ 1:00 AM  
**First Deployment:** Complete (all SOPs ready)  
**Status:** 🟢 Go live

Good luck, Hermes! Make us proud. 🚀