# SOP: Weekly Amazon Data Analysis Cron Run

**Owner:** Ava (Strategy Lead) | **Operator:** Hermes (Sales Strategist) | **Executor:** Cloud Run / Gemini Flash / Codex | **Version:** 1.0 | **Date:** 2026-04-10

---

## Overview

Every Saturday morning, we run an automated data pipeline to download Amazon reports, analyze catalog health and sales performance, and generate actionable recommendations.

**Schedule:** Saturday 1:00 AM – 8:00 AM EST (Mac Studio local time)

**Purpose:**
1. Download fresh Amazon data (Active Listings, Child ASIN, Business Reports)
2. Calculate key metrics (conversion, velocity, gaps, anomalies)
3. Generate recommendations (scale, investigate, retire, create)
4. Deliver dashboard + Slack alerts + email to Cem

---

## Cron Schedule (Current)

| Time (EST) | Task | Agent | Data Source | Output | Status |
|-----------|------|-------|-------------|--------|--------|
| **1:00 AM** | Listings US Analysis | Gemini Flash | Amazon Active Listings (US) | Delta report (new/removed) | ✅ Scheduled |
| **2:00 AM** | Listings UK Analysis | Gemini Flash | Amazon UK Active Listings | Regional comparison | ✅ Scheduled |
| **3:00 AM** | Listings DE + Movers | Gemini Flash | Amazon DE Active Listings | Top movers by product type | ✅ Scheduled |
| **5:00 AM** | PULSE Leaderboard | Gemini Flash | BigQuery (sales velocity) | Weekly sales ranking + alerts | ✅ Scheduled |
| **6:00 AM** | Amazon Reports API Download | Cloud Run | Amazon SP-API | Download Business + Child ASIN reports | ⏳ Pending Test |
| **7:00 AM** | Amazon Ads Analysis (Hermes) | Kimi K2.5 | Amazon Advertising Reports | ROAS/ACOS by campaign, negate candidates | ❌ Not Yet Automated |
| **8:00 AM** | Consolidated Report | Cem (manual review) | All above outputs | Executive summary, action items | ❌ Manual |

---

## Current Workflow (What Happens Now)

### **Friday 5:00 PM — Manual Download (Cem)**

**Action:** Download reports manually from Amazon Seller Central

**Reports Downloaded:**
1. Active Listings Report (US) — 6-7 GB
2. Child ASIN Report (14-day, US) — 5-8 MB
3. Child ASIN Report (30-day, US) — 5-8 MB
4. Business Report (14-day, US) — 7-8 MB
5. Business Report (30-day, US) — 7-8 MB
6. Campaign Report (optional, if ads exist)
7. Search Term Report (optional, if ads exist)

**Destination:** Mac Studio `~/Downloads/`

**Time:** ~15-30 minutes (Active Listings is 6-7GB, slow download)

**Checklist:**
- [ ] Login to Amazon Seller Central (gemc@ecellglobal.com)
- [ ] Navigate: Reports → Inventory → Active Listings Report
- [ ] Download US version → Save to `~/Downloads/` (rename if needed: `US Active Listings Report_YYYY-MM-DD.txt`)
- [ ] Navigate: Reports → Business Reports → Child ASIN Report
- [ ] Download 14-day version → Save (format: `US Child ASIN Report 14d_YYYY-MM-DD.csv`)
- [ ] Download 30-day version → Save (format: `US Child ASIN Report 30d_YYYY-MM-DD.csv`)
- [ ] (Optional) Download Business Reports (14d + 30d)
- [ ] (Optional) Download Campaign Report if running ads
- [ ] (Optional) Download Search Term Report if running ads
- [ ] Verify all files are in `~/Downloads/`
- [ ] Note: Don't delete files yet (analysis team picks them up Saturday morning)

**Why Manual?**
- Active Listings Report (6-7GB) is too large for cloud API
- Amazon Seller Central handles resume on failed downloads (robust)
- Faster on local Mac Studio network than Cloud Run

**Blockers:**
- ❌ If download fails during night (no retry)
- ❌ If Mac Studio network down, download won't start
- ❌ If file corrupted, no validation until morning

---

### **Saturday 1:00 AM – 8:00 AM — Automated Analysis (Cron)**

#### **1:00 AM — Listings US Analysis Cron**

**Task:** Analyze US Active Listings for delta (new SKUs, removed SKUs, price changes)

**Inputs:**
- `~/Downloads/US Active Listings Report_YYYY-MM-DD.txt` (6-7 GB)
- Previous week snapshot (SQLite: `listings_previous`)

**Process:**
1. Load new report into SQLite: `listings_current`
2. Rotate: `listings_previous` = old `listings_current`
3. Calculate delta:
   - New SKUs: (current - previous)
   - Removed SKUs: (previous - current)
   - Price changes: (|current_price - previous_price| > $0.50)
   - Status changes: (suppressed, active, inactive)
4. Output: `weekly_delta_listings_us_YYYY-MM-DD.json`

**Output Format:**
```json
{
  "date": "2026-04-12",
  "marketplace": "US",
  "previous_total_skus": 3420000,
  "current_total_skus": 3425000,
  "new_skus": 5000,
  "removed_skus": -0,
  "net_change": 5000,
  "price_changes": 1250,
  "suppression_flags": 45,
  "top_20_new_designs": [...],
  "top_20_removals": [...],
  "top_20_price_increases": [...],
  "device_coverage_gaps": [...],
  "fulfillment_mismatch_flags": [...]
}
```

**Agent:** Gemini Flash (free, fast)

**Status:** ✅ Already Scheduled

**Issues:** 
- File is 6-7GB → may time out or crash memory
- **Solution needed:** Implement chunked streaming

---

#### **2:00 AM — Listings UK Analysis Cron**

**Task:** Analyze UK Active Listings (same as US but regional)

**Inputs:**
- Amazon UK Active Listings Report (if available)
- Previous week UK snapshot (SQLite: `listings_uk_previous`)

**Process:** Same as US (delta analysis, price changes, gaps)

**Output:** `weekly_delta_listings_uk_YYYY-MM-DD.json`

**Agent:** Gemini Flash

**Status:** ✅ Already Scheduled

**Note:** Currently may not have UK data (check if downloads are enabled)

---

#### **3:00 AM — Listings DE + Movers Analysis Cron**

**Task:** Analyze Germany (DE) Active Listings + identify top movers across all regions

**Inputs:**
- Amazon DE Active Listings Report
- Delta reports from US + UK (from previous crons)

**Process:**
1. Load DE Active Listings
2. Calculate DE delta (new, removed, price changes)
3. Identify "movers" across all regions:
   - Designs with velocity >1.5x (accelerating)
   - Designs with velocity <0.7x (decelerating)
   - New designs with high initial velocity
4. Output: `weekly_movers_YYYY-MM-DD.json`

**Output Format:**
```json
{
  "date": "2026-04-12",
  "top_accelerating_designs": [
    {"design": "NARUTO-IPH17PM-HB401", "velocity": 1.8, "revenue_trend": "+45%"},
    ...
  ],
  "top_decelerating_designs": [...],
  "new_hot_designs": [...],
  "regional_comparison": {
    "us": {...},
    "uk": {...},
    "de": {...}
  }
}
```

**Agent:** Gemini Flash

**Status:** ✅ Already Scheduled

---

#### **5:00 AM — PULSE Leaderboard Cron**

**Task:** Generate weekly sales leaderboard by license, product type, device, design

**Inputs:**
- BigQuery: Sales data (nightly sync from Amazon)
- Conversion Dashboard data
- Historical baseline (90-day run rate)

**Process:**
1. Calculate velocity for each design:
   - `velocity = (14d_sales / 30d_sales) × 100`
2. Rank designs by:
   - Absolute revenue
   - Velocity (accelerating vs declining)
   - License obligation status (gap to MG)
3. Score by PULSE action type:
   - LIST IT (missing marketplace)
   - COMPLETE IT (missing device variant)
   - BUILD IT (new design justified)
   - FIX IT (high sessions, low conversion)
   - BOOST IT (low sessions, high conversion)
   - RETIRE IT (velocity <0.3x for 90+ days)
4. Output: `weekly_pulse_leaderboard_YYYY-MM-DD.md`

**Output Format:**
```markdown
# PULSE Weekly Leaderboard — Week of 2026-04-12

## Top 20 Designs by Velocity

| Rank | Design | Revenue (14d) | Velocity | Trend | Action | License Gap |
|------|--------|---------------|----------|-------|--------|------------|
| 1 | NARUTO-HB401 | $8,500 | 1.45x | 📈 Accelerating | BOOST IT | - |
| 2 | PEANUTS-HB6 | $7,200 | 1.32x | 📈 Accelerating | BOOST IT | - |
| ... | ... | ... | ... | ... | ... | ... |

## License Obligations (MG Gaps)

| License | MG | Current Revenue | Gap | Status |
|---------|----|-----------------|----|--------|
| NBA | $200K | $50K | -$150K | 🔴 CRITICAL |
| NFL | $150K | $0 | -$150K | 🔴 EXPIRED |
| ...

## Alerts

- **NBA Gap Critical:** Fast-track high-velocity NBA designs
- **NFL Renewal:** Decision needed by May 1 (expires Mar 31, 90-day sell-off ends Jun 29)
- **New Hot:** ONEPIECE-HB401 accelerating 1.6x, allocate budget
```

**Agent:** Gemini Flash

**Status:** ✅ Already Scheduled

---

#### **6:00 AM — Amazon Reports API Download (Cloud Run)**

**Task:** Download Amazon Business + Child ASIN reports via SP-API (instead of manual)

**Current Status:** ⏳ Pending Test

**Why It's Needed:**
- Automate manual Cem downloads
- Enable real-time reporting (pull fresh data)
- Reduce file size by streaming

**Reports to Pull:**
1. Child ASIN Report (14-day)
2. Child ASIN Report (30-day)
3. Business Report (14-day)
4. Business Report (30-day)
5. Campaign Report (if available)
6. Search Term Report (if available)
7. Placement Report (if available)

**Inputs:**
- Amazon SP-API credentials (stored in Cloud Run env vars)
- Request type: `GET_MERCHANT_LISTINGS_ALL_DATA` or equivalent

**Process:**
1. Check Cloud Run service for API health
2. Call Amazon `CreateReport` endpoint for each report type
3. Poll status until report ready (wait loop, max 60 min)
4. Download report document via `GetReportDocument`
5. Stream to Mac Studio or write to GCS bucket
6. Validate file format matches manual downloads
7. Delete temporary files
8. Log success/failure

**Output:** 
- `~/Downloads/US Child ASIN Report 14d_YYYY-MM-DD.csv` (auto-populated by Cloud Run)
- `~/Downloads/US Child ASIN Report 30d_YYYY-MM-DD.csv`
- (Similar for Business, Campaign, Search Term reports)

**Agent:** Cloud Run (Python/Node.js worker)

**Status:** ⏳ Pending Test (Codex to investigate Cloud Run + SP-API capability)

**Blockers:**
- ❌ SP-API scope missing (may not have report permissions)
- ❌ Cloud Run timeout (60 min SLA, reports may take >60 min)
- ❌ File size limits (large reports may fail)

**Next Step:** Codex to audit Cloud Run service + SP-API endpoints (by Apr 12)

---

#### **7:00 AM — Amazon Ads Analysis (Hermes)**

**Task:** Analyze Amazon advertising reports (Campaign, Search Term, Placement, etc.)

**Current Status:** ❌ Not Yet Automated

**Why It's Needed:**
- Identify waste terms (ACOS >50%)
- Rank campaigns by ROAS (stars vs dogs)
- Generate budget reallocation recommendations
- Validate shipping template compliance

**Inputs (When Available):**
1. Campaign Report
2. Search Term Report
3. Placement Report
4. Advertised Product Report
5. Purchased Product Report (halo effect)

**Process:**
1. Load reports from `~/Downloads/`
2. Calculate for each report (see ACTIVE-LISTINGS-CHILD-ASIN-DATA-GUIDE.md for details):
   - Campaign Report: ROAS, ACOS, portfolio quadrant (Star/Cow/Mark/Dog)
   - Search Term Report: Profitable terms, waste terms (ACOS >50%), negate candidates
   - Placement Report: Top of Search ROAS, Product Page ROAS, bid multiplier opportunities
   - Advertised Product: Per-ASIN performance, underperformers
   - Purchased Product: Halo multiplier, true ROAS validation
3. Generate recommendations:
   - Negate top 10 waste terms ($300-500/month savings)
   - Reallocate budget from Dogs (<1.5x ROAS) to Stars (>10x ROAS)
   - Adjust bid multipliers by placement
   - Identify FBA shipping template gaps
4. Output: `weekly_ads_analysis_YYYY-MM-DD.md`

**Output Format:**
```markdown
# Amazon Advertising Analysis — Week of 2026-04-12

## Campaign Portfolio

| Quadrant | Count | Total Spend | Total ROAS | Action |
|----------|-------|-------------|-----------|--------|
| Stars (>10x ROAS) | 2 | $500 | 12.5x | Scale +30% |
| Cash Cows (3-10x ROAS) | 8 | $1,500 | 5.2x | Maintain |
| Question Marks (1-3x ROAS) | 35 | $2,000 | 2.1x | Optimize |
| Dogs (<1.5x ROAS) | 26 | $1,000 | 0.8x | Pause 50% |

## Search Term Recommendations

### Top 10 Negate Candidates (ACOS >50%)
1. "cody rhodes phone case" - ACOS 78%, spend $13.52 → NEGATE
2. "roman reigns case" - ACOS 65%, spend $12.16 → NEGATE
...

Expected monthly savings: $300-500

## Placement Analysis
- Top of Search: 8.2x ROAS (premium, bid +20%)
- Product Page: 4.5x ROAS (standard, maintain)
- Rest of Page: 1.2x ROAS (low, reduce bid)

## Shipping Template Audit
- Items with Reduced Shipping Template: 85%
- Items with default template: 15% (⚠️ showing long delivery)
- Action: Investigate SP-API `PutListingsItem` capability for bulk template update
```

**Agent:** Hermes (Kimi K2.5)

**Status:** ❌ Not Yet Automated

**Blocker:** 
- Amazon advertising reports (Campaign, Search Term, etc.) currently manual downloads
- Hermes analysis rules need to be defined + tested

**Next Step:** Define analysis rules + create Hermes cron (by Apr 30)

---

#### **8:00 AM — Consolidated Report + Slack Delivery**

**Task:** Synthesize all cron outputs into one executive summary, deliver to Cem

**Current Status:** ❌ Manual (Cem reviews individual files)

**Ideal Status:** ✅ Automated dashboard + Slack alert

**Inputs (All Previous Crons):**
- `weekly_delta_listings_us_YYYY-MM-DD.json`
- `weekly_delta_listings_uk_YYYY-MM-DD.json`
- `weekly_movers_YYYY-MM-DD.json`
- `weekly_pulse_leaderboard_YYYY-MM-DD.md`
- `weekly_ads_analysis_YYYY-MM-DD.md`

**Process:**
1. Aggregate all outputs
2. Identify top 10 action items:
   - Top 5 opportunities (create, scale, fix)
   - Top 5 risks (pause, retire, investigate)
3. Calculate consolidated KPIs:
   - Conversion rate trend
   - ROAS trend
   - Shipping template compliance
   - FBA penetration
4. Generate executive summary (one page)
5. Deliver via:
   - Slack #ai-workflow (immediate alert)
   - Email to Cem (detailed tables + data)
   - Dashboard (live view, updated hourly)

**Output Format (Slack):**
```
📊 **Weekly Amazon Analysis — Week of Apr 12, 2026**

✅ **HEALTH METRICS**
├─ Conversion: 2.89% (baseline) ✅
├─ ROAS: 5.74x (target 6.5x) ⚠️
├─ ACOS: 17.42% (target <15%) ⚠️
├─ Shipping Template Compliance: 85% (target 100%) ⚠️
└─ FBA Penetration (Top 50): 42% (target 80%) ⚠️

🎯 **TOP 5 OPPORTUNITIES**
1. Create NARUTO-IPH16 variants (3 missing devices) → +$2K/mo
2. Move NFL designs to FBA (FBM 2%, FBA 6.4%) → +$3K/mo
3. Negate waste terms (ACOS >50%) → Save $400/mo
4. Scale PEANUTS-HB6 (velocity 1.6x, conversion 7.8%) → +$1K/mo
5. Increase NARUTO price point (iPhone 17PM converts +$2) → +$500/mo

🚨 **TOP 5 RISKS**
1. NFL license expired Mar 31 (decision needed by May 1)
2. NBA gap $200K behind (fast-track 5 designs)
3. 15% listings missing Reduced Shipping Template (lower conversion)
4. 26 ad campaigns with <1.5x ROAS (pause to save $500/mo)
5. PEANUTS design velocity declining (0.85x, -15% revenue)

💰 **ESTIMATED IMPACT (This Week)**
- Opportunities: +$6-7K/month potential revenue
- Risks: -$2-3K/month if not addressed
- Next week action items: 12 items assigned

👉 **Your Action:** Review full report + approve top 5 opportunities
📍 **Details:** Dashboard: https://conversion-dashboard-kohl.vercel.app (live updated Sat 8 AM)
```

**Output Format (Email Summary):**
```markdown
# WEEKLY AMAZON ANALYSIS EXECUTIVE SUMMARY
## Week of 2026-04-12 | Generated Saturday 2026-04-13 8:00 AM

### OVERVIEW
All systems green. 6 recommendations to action this week.

### METRICS AT A GLANCE
| Metric | This Week | Last Week | Change | Status |
|--------|-----------|-----------|--------|--------|
| Conversion Rate | 2.89% | 2.87% | +0.02% | ✅ |
| ROAS | 5.74x | 5.68x | +0.06x | ⚠️ (target 6.5x) |
| ACOS | 17.42% | 17.51% | -0.09% | ✅ |
| FBA Penetration | 42% | 40% | +2% | 🟡 (target 80%) |

### TOP 5 ACTION ITEMS
1. **CREATE:** NARUTO-IPH16PM/Pro/Base variants (all case types)
   - Owner: Marketplace Ops
   - Timeline: 1 week
   - Revenue impact: +$2,000/month
   - Approval: ✅ Approved

2. **MOVE TO FBA:** Top 10 NFL designs (currently FBM)
   - Owner: Harry (Inventory Planning)
   - Timeline: 2 weeks
   - Revenue impact: +$3,000/month
   - Approval: ⏳ Pending

... (continue for remaining 3)

### DETAILED ANALYSIS
[Link to dashboard / detailed tables]

### NEXT WEEK FORECAST
- NFL renewal deadline (May 1 decision needed)
- NBA gap catch-up (allocate $500/week to fast-track designs)
- Shipping template audit (determine SP-API edit capability)
```

**Agent:** Ava (main session, manual synthesis) OR Codex (automated if cron rules defined)

**Status:** ❌ Manual (Cem reviews, Ava synthesizes) → ✅ Should be automated

**Blocker:**
- Need to define synthesis rules (how to weight opportunities vs risks)
- Dashboard not yet built (currently static conversion dashboard only)

**Next Step:** Define synthesis rules + build dashboard (by Apr 30)

---

## Pre-Run Checklist (Friday 5 PM)

Before the cron runs Saturday morning, ensure:

- [ ] **Cem downloads reports** (Friday 5 PM)
  - [ ] Active Listings Report (US) → ~/Downloads/
  - [ ] Child ASIN Report 14d + 30d → ~/Downloads/
  - [ ] Business Report 14d + 30d → ~/Downloads/
  - [ ] (Optional) Campaign + Search Term reports → ~/Downloads/
  - [ ] Verify file sizes (Active Listings ~6-7GB)
  - [ ] Confirm no corruption (files not truncated)

- [ ] **Mac Studio is online** (Tailscale connected)
  - [ ] Check Tailscale status on Mac Studio
  - [ ] Verify `~/Downloads/` is accessible
  - [ ] Test network latency (should be <100ms)

- [ ] **SQLite database is healthy**
  - [ ] Previous week's listings backed up
  - [ ] Database not locked by other processes
  - [ ] Disk space available (>50GB free)

- [ ] **All cron jobs enabled**
  - [ ] Confirm all 6 crons are scheduled in cron daemon
  - [ ] Check system time is accurate (NTP sync)
  - [ ] Review any recent cron failures (Sat previous week)

- [ ] **BigQuery data is fresh** (for PULSE cron)
  - [ ] Verify nightly sync completed (3 AM ET)
  - [ ] Check BigQuery tables for latest date
  - [ ] Confirm no data latency issues

- [ ] **Notification channels ready**
  - [ ] Slack #ai-workflow is accessible
  - [ ] Email delivery working (test alert if needed)
  - [ ] Dashboard access verified

---

## During-Run Monitoring (Saturday 1 AM – 8 AM)

**What Ava Does (Hands-Off):**
- Crons run automatically, no manual intervention needed
- Logs written to: `/var/log/cron.log` (check if issues)

**What to Monitor:**
- 1:00 AM: Listings US cron starts → should finish by 1:30 AM
- 2:00 AM: Listings UK cron starts → should finish by 2:30 AM
- 3:00 AM: Listings DE cron starts → should finish by 3:30 AM
- 5:00 AM: PULSE cron starts → should finish by 5:30 AM
- 6:00 AM: Amazon Reports API (Cloud Run) → should finish by 7:00 AM
- 7:00 AM: Hermes analysis (if running) → should finish by 7:45 AM
- 8:00 AM: Report delivery (email + Slack) → completed

**If Cron Fails:**
- Check logs: `tail -100 /var/log/cron.log`
- Identify failure point (which cron, what error)
- Retry manually (if quick fix) or escalate to Codex
- Update status in Slack #ai-workflow

**Typical Success Indicators:**
- All 6 crons complete without errors
- JSON + markdown files created in `~/Documents/ecell-analysis/results/`
- Slack message posted to #ai-workflow at 8:00 AM
- Email sent to Cem by 8:15 AM
- Dashboard updated (live data reflects Saturday morning)

---

## Post-Run (Saturday 8:15 AM)

**What Cem Does (Manual Review):**

1. **Open Slack notification** (#ai-workflow)
   - Read executive summary
   - Note top 5 opportunities + 5 risks
   - Scan KPIs (conversion, ROAS, ACOS, FBA %)

2. **Open email** (detailed analysis)
   - Review action items
   - Check owners + timelines
   - Identify any surprises

3. **Open dashboard** (live metrics)
   - View conversion trends
   - Check velocity signals
   - Spot new accelerating designs

4. **Decision (30 min):**
   - Approve top 5 action items
   - Flag any concerns
   - Assign owners + due dates

5. **Update TASKS.md** (local task tracking)
   - Add new action items from cron analysis
   - Update due dates
   - Mark completed items

**Approval Process (Simple):**
- ✅ = Proceed (Marketplace Ops, Harry, Hermes execute)
- ⚠️ = Review Required (schedule call with Cem)
- ❌ = Hold (flag as risk, re-review next week)

---

## Post-Analysis (Saturday 9 AM – Sunday 5 PM)

**Marketplace Ops Actions:**
- Create missing SKU listings (e.g., NARUTO-IPH16 variants)
- Update suppressed listings (re-add, update content)
- Update ASIN linkages

**Harry (Inventory Planning):**
- Plan FBA migrations (move FBM → FBA)
- Restock high-velocity designs
- Retire low-velocity variants

**Hermes (Sales Strategist):**
- Monitor campaign performance
- Add negate terms to ad campaigns
- Reallocate budget (Stars up, Dogs down)
- Request shipping template edit capability

**Ava (Strategic):**
- Consolidate team outputs
- Update PULSE scoring model (if needed)
- Plan next week's focus areas

---

## Troubleshooting

### **Issue: Active Listings cron crashes (memory error)**

**Symptom:** Cron starts at 1:00 AM, fails by 1:05 AM with "memory exhausted" error

**Root Cause:** 6-7 GB file loaded entirely into memory

**Solution (Short-term):**
- Manually load file via chunked reader
- Skip full analysis, do delta-only
- Output smaller delta JSON (top 1,000 changes)

**Solution (Long-term):**
- Implement streaming processor (read 1GB chunks, process, write to SQLite)
- Replace with Cloud Run API call (if SP-API supported)

**Implemented By:** Codex (Phase 1 optimization)

---

### **Issue: Child ASIN cron takes >60 min**

**Symptom:** Cron starts at 6:00 AM (Cloud Run), timeout at 7:00 AM

**Root Cause:** Large CSV file, complex analysis, Google API latency

**Solution (Short-term):**
- Reduce dataset (e.g., only top 500 variants instead of all 1,800)
- Simplify analysis (skip halo effect calculation)
- Run in background task queue (not subject to 60-min timeout)

**Solution (Long-term):**
- Move analysis to BigQuery (native SQL, parallelized)
- Cache intermediate results (don't recalculate each run)

**Implemented By:** Codex + Harry (Phase 2 optimization)

---

### **Issue: Slack notification doesn't send at 8 AM**

**Symptom:** No Slack message in #ai-workflow, but cron reports success

**Root Cause:** Slack bot token expired, rate limited, or channel permissions

**Solution (Quick):**
- Check Slack bot status: https://api.slack.com/apps/A0ACDCN4SSC
- Verify bot token is valid (refresh if expired)
- Verify bot has write access to #ai-workflow
- Manually post summary if bot fails

**Implemented By:** Ava (Slack configuration)

---

### **Issue: Reports not in ~/Downloads/ by 6 AM**

**Symptom:** Cron tries to read reports, files don't exist

**Root Cause:** Cem didn't download Friday, or download failed

**Solution:**
- Check Mac Studio ~/Downloads/ directory manually
- If files missing, request Cem to download manually (immediate action)
- If files corrupted, re-download and retry cron
- Set fallback: Use previous week's reports if new ones missing (skip analysis)

**Implemented By:** Ava (file validation check at 6:00 AM)

---

## Key Contacts & Escalation

**If cron fails:**
1. **Immediate:** Check Slack #ai-workflow for error details
2. **First escalation:** Ava (via Slack) → diagnose issue
3. **Second escalation:** Codex (if technical fix needed) → fix + redeploy
4. **Third escalation:** Cem (if decision needed) → approve alternative approach

**Response SLA:**
- 8:00 AM - 9:00 AM: Ava monitors, diagnoses
- 9:00 AM - 11:00 AM: Codex implements fix (if needed)
- 11:00 AM: New results ready (if rerun), or manual summary provided

**Standby Plan:**
- If cron completely fails by 8 AM, Ava manually creates summary from available data
- Cem still receives report (may be delayed to 10 AM)

---

## Weekly Metrics to Track

**Every Saturday 8:00 AM report should include:**

| Metric | This Week | Last Week | Trend | Status |
|--------|-----------|-----------|-------|--------|
| **Conversion Rate** | 2.89% | 2.87% | +0.02% | ✅ |
| **ROAS** | 5.74x | 5.68x | +0.06x | ⚠️ |
| **ACOS** | 17.42% | 17.51% | -0.09% | ✅ |
| **CPC** | $0.18 | $0.17 | +$0.01 | ✅ |
| **Total SKUs Live** | 3,425,000 | 3,420,000 | +5,000 | ✅ |
| **New SKUs Added** | 5,000 | 4,200 | +800 | ✅ |
| **Suppressed Listings** | 45 | 38 | +7 | ⚠️ |
| **FBA Penetration** | 42% | 40% | +2% | 🟡 |
| **Shipping Template Compliance** | 85% | 83% | +2% | 🟡 |
| **License Gap (NBA)** | -$150K | -$160K | +$10K | 🟡 |
| **Ad Campaign ROAS** | 5.74x | 5.68x | +0.06x | ⚠️ |

---

## SOP Maintenance

**Who Updates This SOP:**
- Ava (strategy + process owner)
- Codex (technical implementation)
- Hermes (analysis logic)

**When to Update:**
- After Phase 1 implementation (Apr 20) — add file size solution
- After Phase 2 implementation (Apr 30) — add new metrics
- After Phase 3 implementation (May 15) — add automation details
- Quarterly (or after major changes) — full review

**Last Updated:** 2026-04-10 (Initial version)

**Next Review:** 2026-04-20 (After Phase 1 testing)

---

## Appendix A: File Size Solutions

### Current Problem
- Active Listings Report: 6-7 GB
- Cannot load entire file in memory (crashes)
- Blocks full automation on Cloud Run

### Solution 1: Chunked Streaming (Recommended)
```python
# Pseudocode
for chunk in pd.read_csv('listings.tsv', chunksize=50000, sep='\t'):
    # Process 50,000 rows at a time
    chunk_subset = chunk[['seller-sku', 'asin', 'quantity', 'price']]
    chunk_subset.to_sql('listings_current', conn, if_exists='append')
    del chunk_subset  # Free memory
```

**Pros:**
- No memory crashes
- Can automate on Cloud Run (1GB limit)
- Efficient storage (process + delete)

**Cons:**
- Slower than full load (15-30 min vs instant)
- Requires chunked reader library

**Timeline:** Implement by Apr 20 (Phase 1)

### Solution 2: Database Streaming (Alternative)
```sql
-- Load TSV directly into SQLite without Python
sqlite> .mode list
sqlite> .import listings.tsv listings_raw
```

**Pros:**
- No Python processing overhead
- Faster (native SQLite import)
- Built-in error handling

**Cons:**
- Less control over parsing
- Requires SQLite 3.32+ (IMPORT command)
- Schema mapping can be tricky

**Timeline:** Alternative if Solution 1 fails

### Solution 3: API-based Delta (Future)
Once Amazon improves SP-API, pull only changes since last sync (likely <50 MB instead of 6 GB)

**Timeline:** Not available yet, pending Amazon development

---

## Appendix B: Cron Job Definitions

### Listings US Cron
```
Schedule: 0 1 * * 6 (Saturday 1 AM ET)
Command: /opt/homebrew/bin/python3 /Users/openclaw/.openclaw/workspace/scripts/weekly_listings_analysis.py --region us --output /Users/openclaw/Documents/ecell-analysis/results/
Timeout: 30 minutes
Retry: 1 (if fails, retry once at 1:15 AM)
Log: /var/log/cron.log
```

### Listings UK Cron
```
Schedule: 0 2 * * 6 (Saturday 2 AM ET)
Command: /opt/homebrew/bin/python3 /Users/openclaw/.openclaw/workspace/scripts/weekly_listings_analysis.py --region uk --output /Users/openclaw/Documents/ecell-analysis/results/
Timeout: 30 minutes
Retry: 1
Log: /var/log/cron.log
```

### PULSE Cron
```
Schedule: 0 5 * * 6 (Saturday 5 AM ET)
Command: /opt/homebrew/bin/python3 /Users/openclaw/.openclaw/workspace/scripts/weekly_pulse_leaderboard.py --output /Users/openclaw/Documents/ecell-analysis/results/
Timeout: 30 minutes
Retry: 1
Log: /var/log/cron.log
Dependencies: BigQuery data (nightly sync must complete by 5 AM)
```

---

**Status:** Ready for execution | **Owner:** Ava | **Last Updated:** 2026-04-10

