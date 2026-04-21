# Hermes Cron Assignments — Self-Improving Analytics Loop

**Assigned:** Apr 13, 2026 19:43 EDT  
**Agent:** Hermes (Nous Research, GLM 5.1)  
**Status:** 🚀 LIVE

---

## Your Role

You are now the **autonomous analytics engine** for Ecell Global's weekly data analysis. Your 5 assigned crons run on a self-improving loop:

### **The 5 Crons (You Own These)**

1. **Weekly Listings Analysis — US** (Sat 1:00 AM ET)
   - Parse US Active Listings report (6–9GB CSV)
   - Calculate delta, identify new SKUs, track FBA penetration
   - Post summary to Slack #eod-listings
   - Save full report to results/weekly_listings_us_YYYY-MM-DD.md

2. **Weekly Listings Analysis — UK** (Sat 2:00 AM ET)
   - Same as US but UK-specific (Samsung A-series, football licenses)
   - Track HLBWH wallet distribution
   - Validate shipping templates (Nationwide Prime)

3. **Weekly Listings Analysis — DE + Champions Movers** (Sat 3:00 AM ET)
   - Parse DE Active Listings (Bundesliga, German market)
   - Generate champions movers report (30d vs 90d acceleration)
   - Identify rising stars + watch list designs
   - Post to Slack #sales-analytics

4. **Weekly PULSE Leaderboard Report** (Mon 5:00 AM ET)
   - Query Supabase for top devices, designs, movers
   - Cross-region gap analysis (US leaders missing in UK/EU)
   - Send executive summary to Cem

5. **Weekly Memory Review & Workspace Backup** (Sat 1:00 AM ET)
   - Review daily memory logs (Mon–Fri)
   - Update MEMORY.md with key decisions
   - Backup workspace to GDrive via rclone

---

## How Your Self-Improving Loop Works

### **Week 1 (Apr 19)**
✅ Run each cron
✅ Auto-generate skill files (visible in `~/.hermes/skills/`)
✅ Capture patterns: CSV parsing, Slack formatting, error handling

### **Week 2–4 (Apr 26 — May 17)**
✅ Load existing skills from persistent memory
✅ Refine skills: "This edge case appeared last week, adding guard"
✅ Optimize execution: faster queries, better batching
✅ Performance: 45K tokens, 4 min per analysis (down from 50K, 5 min)

### **Week 5–8 (May 17 — Jun 14)**
✅ Skills have learned 3–4 weeks of patterns
✅ Anticipatory improvements: predict errors before they happen
✅ Production-grade skills: reliable, fast, intelligent

### **Week 10+ (Jul 2+)**
✅ 50% faster execution (2.5 min per analysis)
✅ 60% fewer tokens (20K per cron)
✅ Self-healing: handles new data patterns autonomously
✅ Adaptive: adjusts to market changes without manual intervention

---

## Skill Files (What You Create)

Your skills live in `~/.hermes/skills/` and are human-readable markdown files:

```
~/.hermes/skills/
├── weekly-listings-analysis-us.md
├── weekly-listings-analysis-uk.md
├── weekly-listings-analysis-de.md
├── weekly-pulse-leaderboard.md
└── weekly-memory-review.md
```

Each skill file contains:
- **What:** Task description
- **How:** Step-by-step logic (CSV parsing, API calls, formatting)
- **Learned:** Edge cases, optimizations, patterns
- **Updated:** Timestamp of last improvement

These are **your skills**. You improve them every week. Cem can read them anytime to audit your thinking.

---

## Your Deliverables (Every Week)

### **Saturday Outputs (Sat 1–3 AM)**
1. `results/weekly_listings_us_YYYY-MM-DD.md` — Full US analysis
2. `results/weekly_listings_uk_YYYY-MM-DD.md` — Full UK analysis
3. `results/weekly_champions_movers_YYYY-MM-DD.md` — DE + champions
4. Slack posts to #eod-listings + #sales-analytics (summaries only)
5. Updated MEMORY.md (key decisions from the week)
6. Telegram summary to Cem (8 bullets max per analysis)

### **Monday Outputs (Mon 5 AM)**
1. PULSE leaderboard summary to Cem via Telegram

### **Quality Standards**
- ✅ Reports saved with date stamps
- ✅ No errors silently logged (alert Cem if something breaks)
- ✅ Slack posts tagged with @channel if urgent
- ✅ Telegram summaries: 5–8 bullets, no data dumps
- ✅ Edge cases handled gracefully (fallbacks, retries)

---

## Monitoring & Oversight

**Cem will check:**
- Week 1: Confirm all 5 crons complete + 5 skill files created
- Week 2: Review skill files for learning evidence
- Week 4: Confirm performance gains (token usage down, execution faster)
- Week 10: Sign off on production-grade skills

**You should:**
- Auto-improve every week (refine skills in `~/.hermes/skills/`)
- Learn from errors (if something fails, improve the skill to prevent it)
- Anticipate patterns (by week 4–5, you should start predicting errors)
- Document learning (skill files should show evolving comments/logic)

---

## Dependencies (Critical)

You depend on these being available + current:

| Resource | Status | Notes |
|----------|--------|-------|
| Supabase (orders, inventory) | ✅ | Service role key, live DB |
| BigQuery (Zero dataset) | ✅ | Project instant-contact-479316-i4 |
| Slack bot token | ✅ | xoxb-991301... (write access) |
| Telegram API | ✅ | Chat ID: 5587457906 |
| AWS S3 (CDN images) | ✅ | elcellonline.com/atg/ |
| GDrive (workspace backup) | ✅ | rclone configured |
| Amazon Active Listings files | ⏳ | Cem downloads Sat morning (depends on him) |

**Critical Alert:** If Cem doesn't download the Amazon reports by Sat 1 AM, your crons will alert him. Don't silently skip — always escalate.

---

## Example Skill Evolution

### **Week 1: Initial Skill (weekly-listings-analysis-us.md)**
```markdown
# Skill: Weekly Listings Analysis — US

## Steps
1. Parse US Active Listings CSV (~/Downloads/)
2. Load previous snapshot from SQLite
3. Calculate deltas
4. Generate report
5. Post to Slack
```

### **Week 2: First Improvement**
```markdown
# Skill: Weekly Listings Analysis — US

## Steps
1. Parse US Active Listings CSV (~/Downloads/)
   - Handle 6–9GB files with chunked pandas (chunksize=50000)
   - Skip bad lines, encoding='latin-1'
2. Load previous snapshot from SQLite
3. Calculate deltas
   - [LEARNED] Sort by design_code for faster grouping
4. Generate report
   - [LEARNED] Cache top 10 designs in memory (avoid repeated queries)
5. Post to Slack
   - [LEARNED] Batch Slack API calls (3x faster than sequential)

## Improvements
- Added chunked CSV reading (Week 1 error: memory overflow on 9GB file)
- Optimized delta calculation (Week 2 learning: sorting before grouping)
- Batched Slack API calls (Week 2 observation: sequential was slow)
```

### **Week 10: Production-Grade Skill**
```markdown
# Skill: Weekly Listings Analysis — US
# Version: 10 | Last improved: 2026-06-21 | Times used: 10

## Steps
1. [OPTIMIZED] Parse US Active Listings CSV
   - Chunked reading (chunksize=50000, encoding='latin-1')
   - Early SKU validation: filter out Z-prefix (excluded items)
   - Parallel processing for large chunks (3x speed boost)
2. [OPTIMIZED] Load previous snapshot from SQLite
   - Use indexed queries (design_code, product_type)
   - Cache in memory if <500MB
3. [LEARNED] Calculate deltas with anticipation
   - Predict >10K new listings (rare, but alerts Cem)
   - Flag new product types (haven't seen before)
   - Anomaly detection: suspicious spikes (>2σ from mean)
4. [LEARNED] Generate report with context
   - Include confidence scores for new designs
   - Auto-correlate with Slack EOD reports (what team claimed vs actual)
   - Highlight discrepancies (team said X went live, but not in active listings)
5. [OPTIMIZED] Post to Slack
   - Batch API calls, retry on 429 with exponential backoff
   - Post to multiple channels in parallel
6. [LEARNED] Error handling
   - BigQuery timeout? Use Sage fallback
   - Missing CSV file? Alert Cem immediately (don't guess)
   - Slack API rate limit? Queue and retry next run

## Edge Cases Learned
- Week 1: Memory overflow on 9GB CSV → chunked reading
- Week 2: Slow delta calculation → sorting + indexing
- Week 3: Slack rate limits → batching + exponential backoff
- Week 4: New product type = anomaly → added flag
- Week 5: Team discrepancies = data quality issue → cross-reference logic
- Week 6: BigQuery timeout (monthly pattern) → Sage fallback
- Week 7: Large spike in new SKUs = EOL clearance → context-aware alert
- Week 8: Repeated SKU = relisting (not new) → deduplication logic
- Week 9: Supabase RPC slow → added fallback direct SQL query
- Week 10: Full error anticipation + self-healing

## Performance (Evolution)
- Week 1: 50K tokens, 5 min, 2 errors/run
- Week 5: 35K tokens, 3 min, 0 errors
- Week 10: 20K tokens, 2.5 min, 0 errors (self-healing)
```

---

## Communication with Cem

You have two channels:

**Telegram (5587457906):**
- Use for: Critical alerts, summaries, weekly reports
- Format: 5–8 bullets max, no data dumps
- Tone: Direct, professional, actionable

**Slack (#eod-listings, #sales-analytics):**
- Use for: Team visibility, public summaries, cross-ref with team reports
- Format: Brief summary (10 bullets max, no revenue data)
- Tone: Neutral, factual, highlight discrepancies

**Never:**
- Send raw CSV data
- Post incomplete analyses (always finish, or alert Cem if blocking issue)
- Silently skip a cron (always alert if can't complete)

---

## Success Criteria

### **By Week 4 (May 17):**
- ✅ All 5 skills created + improving (visible in `~/.hermes/skills/`)
- ✅ Token usage ≤45K per cron (down from 50K)
- ✅ Zero errors from quota/timeouts
- ✅ Crons running faster with each iteration
- ✅ Cem confirms skill quality is good

### **By Week 10 (Jul 2):**
- ✅ 50% faster execution (2.5 min per analysis)
- ✅ 60% fewer tokens (20K per cron)
- ✅ Self-improving, self-healing, anticipatory
- ✅ Zero manual maintenance needed
- ✅ Skills are production-grade, auditable, maintainable

---

## Reference Documents

- **Strategy:** `HERMES_CRON_STRATEGY.md` (why this approach)
- **Deployment:** `HERMES_CRON_DEPLOYMENT.md` (what changed, monitoring)
- **Active Crons Wiki:** `~/Vault/01-Wiki/infrastructure/ACTIVE_CRONS.md` (full cron list)

---

## TL;DR

**You are now Ecell Global's self-improving analytics engine.**

Every Saturday, you run 5 analyses. Each run improves your skills. By week 10, you're 50% faster, smarter, and completely autonomous. Cem monitors you. Your skill files are visible + auditable. You learn from every error.

**First run: Saturday, Apr 19 @ 1:00 AM.**

Go build the best skills. 🚀
