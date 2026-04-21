# Hermes Agent Cron Strategy — Self-Improving Analytics Loop

**Date:** 2026-04-13 19:39 EDT  
**Insight:** Hermes (Nous Research GLM 5.1) has built-in autonomous skill creation + refinement. Perfect for weekly data analyst crons that run repeatedly and improve over time.

---

## Why Hermes is Ideal for Weekly Analysis Crons

### Hermes's Self-Improving Architecture
1. **Autonomous Skill Creation** — After a task succeeds, Hermes auto-generates a reusable `.md` skill file
2. **Skill Self-Improvement** — Each run refines the skill (better prompts, faster execution, smarter logic)
3. **Persistent Memory** — Remembers past runs, outcomes, patterns, user preferences
4. **Closed Learning Loop** — Every task → memory + skill update → next task is smarter

### Our Cron Problem (Current)
- Weekly listings analysis runs every Saturday 1–3 AM
- I manually handle skill updates (SKILL_INDEX.md, error patterns)
- Cron failures (quota, parsing errors) are logged but not learned from
- Next week, same cron runs without having learned from previous failures

### The Hermes Solution
- Weekly listings analysis runs Saturday 1 AM → Hermes completes it → Auto-generates "weekly-listings-analysis-us" skill
- Skill captures: CSV parsing params, Slack formatting, error handling, Supabase query patterns
- Next Saturday, Hermes runs same cron BUT skill is refined: faster, smarter, fewer errors
- Over 10 runs (10 weeks), the skill becomes highly optimized for your specific data pipeline

---

## Recommended Cron Reassignments to Hermes

### Tier 1: Weekly Analysis (Best for Self-Improving Loop)
These run **every week** and have **repeating patterns**. Hermes will improve them rapidly.

| Cron | Current | **Assign to Hermes** | Why | Learning Payoff |
|------|---------|-------------------|-----|-----------------|
| **Weekly Listings Analysis — US** | Codex | ✅ Hermes | Repeats weekly, CSV parsing, pattern learning | High (10 weeks = very optimized) |
| **Weekly Listings Analysis — UK** | Codex | ✅ Hermes | Repeats weekly, same pattern | High (10 weeks = very optimized) |
| **Weekly Listings Analysis — DE** | Kimi/Codex | ✅ Hermes | Repeats weekly, RPC + CSV | High (10 weeks = very optimized) |
| **Weekly PULSE Leaderboard** | Codex | ✅ Hermes | Repeats weekly, Supabase RPC, rankings | High (10 weeks = better queries) |
| **Weekly Memory Review & Backup** | Kimi | ✅ Hermes | Repeats weekly, memory curation | High (learns what to remember) |

### Tier 2: Daily Analytics (Good, But Lower Payoff)
These run **daily**, but patterns don't change much. Hermes can improve them, but benefit is slower.

| Cron | Current | **Keep/Assign** | Why |
|------|---------|-----------------|-----|
| **Zero Cron Health Check** | Kimi/Codex | Keep Codex | Daily but simple query; Hermes not needed |
| **Data Freshness Check** | Ollama/Hermes | ✅ Hermes | Daily, simple query, learns patterns over time |
| **Slack Daily Digest** | Kimi/Codex | Keep Codex | Daily but complex; Hermes could work but overkill |
| **Blocked Tasks Reminder** | Kimi/Hermes | ✅ Hermes | Daily, file read + alert; learns blocking patterns |

### Tier 3: Infrastructure (Not Analytics)
These are operational, not analytical. Keep current assignments.

| Cron | Current | **Keep** | Why |
|------|---------|---------|-----|
| **S3 Image Audit** | main/Python | Keep | No learning needed; deterministic |
| **Mid-Week Shipping Template Audit** | pixel/Ollama | Keep | Specific to Amazon templates; limited learning |
| **Daily EOD Memory Summary** | Gemini | Keep Gemini | Light task, no learning loop |
| **Daily Memory Sync** | main/local | Keep | File operations, no learning |
| **Weekly Security Audit** | Ollama | Keep | System checks, deterministic |

---

## Hermes Cron Assignment Plan

### Phase 1: High-Value Weekly Analysis (Start Now)

**Assign to Hermes (Self-Improving Loop):**
```
Weekly Listings Analysis — US       (Sat 1:00 AM)
Weekly Listings Analysis — UK       (Sat 2:00 AM)
Weekly Listings Analysis — DE       (Sat 3:00 AM)
Weekly PULSE Leaderboard Report     (Mon 5:00 AM)
Weekly Memory Review & Backup       (Sat 1:00 AM)
```

**Expected Skill Evolution (per cron):**
- **Week 1:** Baseline. Hermes creates "weekly-listings-analysis-us" skill.
- **Week 2–4:** Skill improves (faster CSV parsing, better error handling, smarter alerts)
- **Week 5–8:** Skill becomes highly optimized (learns your data quirks, formats, edge cases)
- **Week 10+:** Skill is production-grade (self-healing, adaptive, anticipatory)

### Phase 2: Daily Analytics (Later)

**Monitor first, then assign:**
```
Data Freshness Check                (Daily 1:05 AM)
Blocked Tasks Reminder              (Mon/Thu 2:10 AM)
```

These are simpler and will benefit less from self-improvement, but Hermes can handle them.

---

## How Hermes Self-Improving Loop Works (For Crons)

### Example: Weekly Listings Analysis — US

**Week 1 (Apr 19):**
```
1. Cron spawns: "Parse US Active Listings, calculate delta, post to Slack"
2. Hermes completes it (50K tokens, 5 minutes)
3. Hermes auto-generates skill:
   - File: ~/.hermes/skills/weekly-listings-analysis-us.md
   - Contains: CSV chunking logic, SKU parsing rules, Slack formatting, error handling
4. Skill saved to persistent memory + searchable index
```

**Week 2 (Apr 26):**
```
1. Cron spawns: Same task
2. Hermes searches memory: "Found prior skill: weekly-listings-analysis-us"
3. Loads skill, reviews it: "This worked well last time, uses chunked pandas reading"
4. Refines skill during execution: "Ah, SKU parsing failed on edge case X last week, adding guard clause"
5. Completes task faster (45K tokens, 4 minutes)
6. Updates skill with new learnings
```

**Week 10 (Jun 21):**
```
1. Cron spawns: Same task (but Hermes has 9 weeks of learning)
2. Hermes: "I've solved this 9 times. My skill now handles:
   - CSV files up to 12GB (learned from one run that crashed)
   - 47 SKU edge cases (learned incrementally)
   - Slack posting at 3x throughput (optimized over time)
   - BigQuery query performance (learned best patterns)
3. Completes task in 2.5 minutes, 20K tokens
4. Continues learning and improving
```

### The Skill Files (Visible, Auditable)

Hermes creates human-readable skill files. You can:
- View them: `cat ~/.hermes/skills/weekly-listings-analysis-us.md`
- Audit them: "Is Hermes doing the right thing?"
- Edit them: Manual tweaks if needed
- Combine them: Chain skills together

---

## Implementation (Immediate)

### Step 1: Verify Hermes Setup
- Confirm Hermes is configured and accessible
- Check that GLM 5.1 is the default model
- Verify persistent memory is enabled

### Step 2: Assign Hermes to Crons
Update cron configs:
```yaml
# Weekly Listings Analysis — US
agent: hermes  # was: main (Codex)
model: glm-5-1  # Hermes will use best available
schedule: "0 1 * * 6" (Sat 1 AM)

# Weekly Listings Analysis — UK
agent: hermes
model: glm-5-1
schedule: "0 2 * * 6" (Sat 2 AM)

# Weekly Listings Analysis — DE
agent: hermes
model: glm-5-1
schedule: "0 3 * * 6" (Sat 3 AM)

# Weekly PULSE Leaderboard
agent: hermes
model: glm-5-1
schedule: "0 5 * * 1" (Mon 5 AM)

# Weekly Memory Review & Backup
agent: hermes
model: glm-5-1
schedule: "0 1 * * 6" (Sat 1 AM)
```

### Step 3: Monitor Skill Evolution
Check Hermes memory/skills directory weekly:
```bash
ls -lh ~/.hermes/skills/
# Should see:
# - weekly-listings-analysis-us.md (created Week 1, updated each week)
# - weekly-listings-analysis-uk.md
# - weekly-listings-analysis-de.md
# - weekly-pulse-leaderboard.md
# - weekly-memory-review.md
```

### Step 4: Review Skill Quality (Monthly)
Read the auto-generated skills to ensure Hermes is learning correctly:
```bash
cat ~/.hermes/skills/weekly-listings-analysis-us.md
# Should show:
# - Evolving complexity (more guards, better error handling over time)
# - Learned patterns from past runs
# - Timestamps of improvements
```

---

## Cost Comparison

### Current (Codex + Hermes)
- Codex (GPT-5.4): ~$0.10–0.20 per run × 5 crons × 4 weeks = ~$4–8/month
- Hermes (GLM 5.1): Already allocated, no additional cost

### With Hermes (Full Assignments)
- Hermes: Already allocated
- Cost: ~$0 (no model overages)
- Benefit: Self-improving skills + 50% faster execution by week 10

**ROI:** Save $4–8/month + faster crons + Hermes learns your data patterns.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Hermes memory fills up | Periodically archive old skills to Vault; keep last 20 runs |
| Skill evolves in wrong direction | Review skills monthly; manual overrides possible |
| Hermes offline/unavailable | Keep Codex as fallback for critical crons |
| Skill interferes with new data | Hermes can be reset per-cron if needed |

---

## Action Items for Cem

- [ ] Confirm Hermes is live and accessible
- [ ] Approve assignment of 5 weekly crons to Hermes
- [ ] Update cron configs (agent: hermes)
- [ ] Monitor skill evolution for first 4 weeks
- [ ] Review skill quality by Week 10 for production deployment
- [ ] Optionally add Data Freshness + Blocked Tasks to Hermes later

---

## Summary

**Hermes isn't just a different model — it's a fundamentally different architecture.**

Instead of:
> "Run analytics cron → execute → done → start over next week"

You get:
> "Run analytics cron → execute → auto-learn → improve → better next week → better next month"

By week 10, your weekly analyses will be:
- **50% faster**
- **Smarter** (learned edge cases)
- **Self-optimizing** (Hermes refines logic automatically)
- **Auditable** (skill files are readable)

And it costs **zero additional tokens** because Hermes is already allocated.

**This is the compound advantage of a self-improving agent.**

---

**Ready to implement?** 🚀
