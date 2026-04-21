# Active Crons — Ava's Operational Schedule

**Last Updated:** 2026-04-13 19:35 EDT  
**Total Active Crons:** 18  
**Source:** `cron list --includeDisabled=false` from OpenClaw gateway  
**Maintenance:** Update weekly (every Monday morning). Sync to Vault via `TOOLS.md` reminder.

---

## Daily Crons (Run Every Day)

### 1. Data Freshness Check
- **Time:** 1:05 AM ET (daily)
- **Agent:** main (isolated)
- **Model:** `ollama/gemma4:26b` → **reassign to Hermes (GLM 5.1)**
- **Purpose:** Query Supabase `orders` table for MAX(paid_date). Alert if gap > 7 days.
- **Output:** Telegram alert to Cem or HEARTBEAT_OK
- **SLA:** Must complete by 1:30 AM (allows 25 min buffer before next cron)
- **Last Run:** Apr 13, 1:05 AM — Status: reset (quota issue)
- **Tokens:** 5–10K per run

**What it monitors:**
- Supabase orders freshness (daily transaction sync)
- Gap from today (should be <24 hours)
- Alerts if stale >7 days (indicates BigQuery sync broken)

**Dependencies:** Supabase service role key, live database connection

---

### 2. S3 Image Audit for Shopify
- **Time:** 2:00 AM ET (daily)
- **Agent:** main (isolated)
- **Model:** Direct Python execution (no model needed)
- **Purpose:** Audit S3 CDN (`elcellonline.com/atg/`) image coverage for 26 Shopify designs across positions 1–6.
- **Output:** Report showing which designs have complete image sets; gaps flagged
- **SLA:** Must complete by 2:30 AM
- **Last Run:** Apr 13, 2:00 AM — Status: ok (283 seconds)
- **Tokens:** N/A (local Python script)

**What it checks:**
- 26 Shopify design codes
- Positions 1–6 (product images)
- Top devices by traffic
- Returns: Complete coverage %, gaps by design

**Dependencies:** AWS S3 API, local Python (pandas, boto3)

---

### 3. Zero Cron Health Check
- **Time:** 3:10 AM ET (daily)
- **Agent:** main (isolated)
- **Model:** `moonshot/kimi-k2-0905-preview` → **reassign to Codex (GPT-5.4)**
- **Purpose:** Query BigQuery `zero_dataset.cron_jobs` table. Flag errors in last 24 hours.
- **Output:** Telegram alert to Cem if: (1) Amazon US/UK import errors, (2) cron skipped 24h, (3) order counts abnormal. Otherwise HEARTBEAT_OK.
- **SLA:** Must complete by 3:30 AM
- **Last Run:** Apr 13, 3:10 AM — Status: reset (quota issue)
- **Tokens:** 10–20K per run

**What it monitors:**
- Amazon US Active Listings import (daily)
- Amazon UK Active Listings import (daily)
- BigQuery data pipeline health
- Cron execution timestamps
- Error logs

**Dependencies:** BigQuery project `instant-contact-479316-i4`, dataset `elcell_co_uk_barcode`, table `cron_jobs`

---

### 4. Slack Daily Digest
- **Time:** 4:10 AM ET (daily)
- **Agent:** main (isolated)
- **Model:** `moonshot/kimi-k2-0905-preview` → **reassign to Codex (GPT-5.4)**
- **Purpose:** Aggregate PH team EOD reports from Slack (#eod-creative-graphics, #eod-listings, #eod). Summarize for Cem + post acknowledgment back to each channel.
- **Output:** 
  - Summary message to Cem (Telegram)
  - Acknowledgment posts to each Slack channel (tagged team members, tasks, flags)
  - Full digest saved to memory/slack-digest.md
- **SLA:** Must complete by 4:40 AM
- **Last Run:** Apr 13, 4:10 AM — Status: ok (60 seconds)
- **Tokens:** 30–50K per run

**What it aggregates:**
- #eod-creative-graphics (C0AHQJK60NP) — design/production updates
- #eod-listings (C0AHUUGJK7G) — listing uploads
- #eod (C09T8A2P2HX) — production numbers, shipments
- Extracts: who worked on what, completions, blockers, anomalies

**Dependencies:** Slack bot token, 3 private channel IDs, Slack API

---

### 5. Daily EOD Memory Summary
- **Time:** 11:00 PM ET (daily)
- **Agent:** main (isolated)
- **Model:** `google/gemini-3-flash-preview`
- **Purpose:** Write end-of-day summary to memory/YYYY-MM-DD.md. Append EOD section with accomplishments, open items, context.
- **Output:** Updated memory/YYYY-MM-DD.md + Telegram recap to Cem
- **SLA:** Must complete by 11:30 PM
- **Last Run:** Apr 13, 11:00 PM — Status: ok (32 seconds)
- **Tokens:** 5–10K per run

**What it captures:**
- Accomplishments from the day
- Carry-forward tasks
- Notable context Cem mentioned
- Decisions made

**Dependencies:** Memory file access, Telegram API

---

### 6. Daily Memory Sync to Vault
- **Time:** 11:00 PM ET (daily, same as above)
- **Agent:** main (isolated)
- **Model:** N/A (direct file copy + git commit)
- **Purpose:** Copy today's memory file to Vault backup (~/Vault/03-Agents/Ava/memory/). Commit changes.
- **Output:** memory/YYYY-MM-DD.md synced to Vault
- **SLA:** Must complete by 11:15 PM
- **Last Run:** Apr 13, 11:00 PM — Status: ok (14 seconds)
- **Tokens:** N/A (local operations)

**What it does:**
- Copies ~/.openclaw/workspace/memory/YYYY-MM-DD.md → Vault
- Git commits with message "Daily memory sync"
- Ensures Vault has real-time backup

**Dependencies:** Git, local file system, Vault mount

---

## Weekly Crons (Run on Schedule)

### 7. Mid-Week Shipping Template Audit
- **Time:** Wed 2:00 AM ET (weekly)
- **Agent:** pixel (isolated)
- **Model:** `ollama/gemma4:26b` (local)
- **Purpose:** Check for new Amazon listings (<14 days old) with wrong shipping templates. Flag to #eod-listings if found.
- **Output:** Slack alert to #eod-listings OR HEARTBEAT_OK (silent if no issues)
- **SLA:** Must complete by 2:30 AM
- **Last Run:** Apr 8 (status: reset — file access issue)
- **Tokens:** N/A (local Ollama)

**What it checks:**
- US listings on wrong template (should be "Reduced Shipping Template")
- UK listings on wrong template (should be "Nationwide Prime")
- Only flags NEW listings (<14 days)
- Ignores old wrong-template listings (separate bulk-fix project)

**Dependencies:** Amazon Active Listings file in ~/Downloads/, Slack bot token

---

### 8. Blocked Tasks Reminder
- **Time:** Mon/Thu 2:10 AM ET (twice weekly)
- **Agent:** main (isolated)
- **Model:** `moonshot/kimi-k2-0905-preview`
- **Purpose:** Read TASKS.md. Find items blocked >3 days. Alert Cem via Telegram.
- **Output:** Telegram message listing blocked tasks + how long blocked OR HEARTBEAT_OK
- **SLA:** Must complete by 2:30 AM
- **Last Run:** Apr 13, 2:10 AM — Status: ok (23 seconds)
- **Tokens:** 5–10K per run

**What it monitors:**
- TASKS.md 🔴 BLOCKED section
- Filters for age >3 days
- Extracts task name, blocker reason, how many days

**Dependencies:** TASKS.md file, Telegram API

---

### 9. Friday Report Reminder
- **Time:** Fri 5:00 PM ET (weekly)
- **Agent:** main (system event)
- **Model:** N/A (reminder notification)
- **Purpose:** System reminder for Cem to download weekly Amazon reports to Mac Studio Downloads.
- **Output:** System notification (appears in OpenClaw UI)
- **SLA:** Fire at exactly 5:00 PM Fri
- **Last Run:** Apr 12, 5:00 PM — Status: ok
- **Tokens:** N/A (system event)

**What it reminds:**
- US Child ASIN Report (14-day)
- US Child ASIN Report (30-day)
- US Active Listings Report (if updated)

**Dependencies:** System event delivery, OpenClaw UI

---

### 10. Weekly PULSE Leaderboard Report
- **Time:** Mon 5:00 AM ET (weekly)
- **Agent:** main (isolated)
- **Model:** `openai-codex/gpt-5.4` ✅
- **Purpose:** Hit Supabase RPC endpoints. Generate top devices, top designs, movers, cross-region gaps. Send executive summary to Cem.
- **Output:** Telegram message with 8 bullets max + results/weekly_pulse_leaderboard_YYYY-MM-DD.md
- **SLA:** Must complete by 5:30 AM
- **Last Run:** Apr 7, 5:00 AM — Status: ok (165 seconds)
- **Tokens:** 30–50K per run

**What it generates:**
- Top 10 devices (US, HTPCR, 6-month)
- Top 20 design groups (US, HTPCR, 6-month)
- Top 20 champion child designs (US, HTPCR, 6-month)
- Top movers (30d vs 90d acceleration)
- Cross-region gaps (US leaders missing in UK/EU)

**Dependencies:** Supabase RPC endpoints, service role key, Telegram API

---

### 11. Weekly Listings Analysis — US
- **Time:** Sat 1:00 AM ET (weekly)
- **Agent:** main (isolated)
- **Model:** `openai-codex/gpt-5.4` ✅
- **Purpose:** Parse US Active Listings report (6–9GB CSV). Calculate delta vs last week. Identify new SKUs, top designs, FBA penetration. Cross-reference with Slack EOD listings reports.
- **Output:** 
  - results/weekly_listings_us_YYYY-MM-DD.md
  - Sanitized summary posted to Slack #eod-listings
  - Telegram executive summary to Cem
  - Sets ~/Downloads/weekly_report_status.json us field to 'done'
- **SLA:** Must complete by 1:45 AM
- **Last Run:** Apr 6, 1:00 AM — Status: ok (478 seconds)
- **Tokens:** 50–100K per run

**What it analyzes:**
- Total listings, delta vs previous week
- New SKUs by product type (count + % new)
- Top 10 new design codes
- FBA penetration by product type
- Discrepancies between team claims (Slack EOD) vs actual listings

**Dependencies:** US Active Listings file in ~/Downloads/, Slack API, Supabase, Telegram API

---

### 12. Weekly Listings Analysis — UK
- **Time:** Sat 2:00 AM ET (weekly)
- **Agent:** main (isolated)
- **Model:** `openai-codex/gpt-5.4` ✅
- **Purpose:** Parse UK Active Listings report. Same analysis as US but with UK-specific flags (Samsung A-series, football licenses, HLBWH distribution).
- **Output:** 
  - results/weekly_listings_uk_YYYY-MM-DD.md
  - Slack post to #eod-listings
  - Telegram summary to Cem
  - Sets weekly_report_status.json uk field to 'done'
- **SLA:** Must complete by 2:45 AM
- **Last Run:** Apr 6, 2:00 AM — Status: ok (452 seconds)
- **Tokens:** 50–100K per run

**What it analyzes:**
- Same as US but UK-specific: top devices (iPhone + Samsung A-series), football licenses, wallet market
- FBA vs FBM split
- Shipping template validation (should be "Nationwide Prime")

**Dependencies:** UK Active Listings file in ~/Downloads/, Slack API, Supabase, Telegram API

---

### 13. Weekly Listings Analysis — DE + Champions Movers
- **Time:** Sat 3:00 AM ET (weekly)
- **Agent:** main (isolated)
- **Model:** `moonshot/kimi-k2-0905-preview` → **reassign to Codex (GPT-5.4)**
- **Purpose:** Parse DE Active Listings. Generate champions movers (30d vs 90d velocity acceleration). Highlight rising stars + watch list.
- **Output:** 
  - results/weekly_champions_movers_YYYY-MM-DD.md
  - Slack post to #sales-analytics (C0A2AHP2Q4D)
  - Telegram summary to Cem (8 bullets: DE summary + top 5 rising + top 3 watch)
  - Sets weekly_report_status.json de field to 'done'
- **SLA:** Must complete by 3:45 AM
- **Last Run:** Apr 6, 3:00 AM — Status: reset (quota issue)
- **Tokens:** 50–150K per run

**What it analyzes:**
- DE market: Bundesliga licenses, German market preferences
- Champions acceleration: designs in top 30d but not 90d (Rising Stars)
- Designs dropped from top 90d (Watch List)
- Top 5 movers up, top 5 movers down

**Dependencies:** DE Active Listings file in ~/Downloads/, Supabase, Slack API, Telegram API

---

### 14. Weekly Memory Review & Backup
- **Time:** Sat 1:00 AM ET (weekly, same as US listings)
- **Agent:** main (isolated)
- **Model:** `moonshot/kimi-k2-0905-preview`
- **Purpose:** Review past week's memory/YYYY-MM-DD.md files (Mon–Fri). Extract key decisions + learnings. Update MEMORY.md with distilled insights. Sync workspace to GDrive.
- **Output:** 
  - Updated MEMORY.md
  - rclone sync to gdrive:Clawdbot Shared Folder/Brain/ava-workspace-backup/
  - Telegram summary to Cem (decisions captured, archive notes, backup status)
- **SLA:** Must complete by 1:30 AM (before US listings at 1:00 AM)
- **Last Run:** Apr 6 — Status: reset (quota issue)
- **Tokens:** 20–40K per run

**What it does:**
- Reads memory/2026-04-08.md, 2026-04-09.md, etc.
- Extracts significant decisions, lessons, context
- Updates MEMORY.md long-term memory layer
- Prunes stale/outdated entries
- Full workspace backup to GDrive

**Dependencies:** Memory files, rclone, GDrive mount, MEMORY.md write access

---

### 15. Weekly Security Audit
- **Time:** Sun 6:30 AM ET (weekly)
- **Agent:** main (isolated)
- **Model:** `ollama/gemma4:26b` (local)
- **Purpose:** Check OpenClaw security posture. Run `openclaw security audit --deep`, firewall status, listening ports, Tailscale peers.
- **Output:** Telegram message with summary (only flag issues or changes since last week)
- **SLA:** Must complete by 7:00 AM
- **Last Run:** Apr 6 — Status: reset
- **Tokens:** N/A (local Ollama)

**What it audits:**
- macOS firewall enabled
- Listening ports (unexpected services)
- Tailscale peer status
- OpenClaw version + update availability
- Changes since last week

**Dependencies:** openclaw CLI, macOS firewall, Tailscale, local Python

---

## One-Time Crons (Special)

### 16. NFL License Sell-Off Reminder
- **Time:** May 6, 2026 @ 6:00 PM UTC (one-time, auto-delete after)
- **Agent:** main (system event)
- **Model:** N/A (system reminder)
- **Purpose:** One-time reminder that NFL license expired Mar 31 and sell-off period ends ~Jun 29. Check if renewal has been initiated.
- **Output:** System notification + Telegram alert
- **Status:** Scheduled (deleteAfterRun: true)

**Context:**
- NFL license: Expired Mar 31, 2026
- Sell-off period: Mar 31 – Jun 29 (~90 days)
- New production: BLOCKED until renewal
- Existing inventory: Can still sell during sell-off

---

## Disabled Crons (Archived)

### A. Harry iMac Telegram Monitor
- **Status:** Disabled (resolved)
- **Was for:** Checking Harry's 409 Telegram errors on iMac
- **Resolution:** Harry's Telegram is now working; cron not needed

### B. HB401 Sprint Daily EOD Check
- **Status:** Disabled (sprint completed)
- **Was for:** Tracking HB401 case expansion sprint (31 device×design combos)
- **Completed:** Mar 28, 2026
- **Archive:** Can be referenced if HB401 sprint restarts

---

## Cron Health Summary

| Category | Count | Status | Alert |
|----------|-------|--------|-------|
| **Daily** | 6 | 4/6 ok, 2/6 reset | Gemini quota Apr 13 |
| **Weekly** | 9 | 5/9 ok, 4/9 reset | Gemini quota + file access |
| **One-time** | 1 | Scheduled | None |
| **Disabled** | 2 | N/A | None |
| **TOTAL** | 18 | **9/18 ok** | **Quota limit + reassignment needed** |

---

## Maintenance Schedule

### Weekly (Every Monday)
- [ ] Review ACTIVE_CRONS.md for stale entries
- [ ] Check cron.list for new additions
- [ ] Update descriptions if logic changed
- [ ] Verify all crons ran last weekend without errors
- [ ] Update Last Run timestamp + status

### Monthly (First Monday)
- [ ] Audit full cron list vs this document
- [ ] Prune disabled/obsolete crons
- [ ] Update model assignments if needed
- [ ] Review success rates + error patterns

### Quarterly (Every 3 months)
- [ ] Full audit of cron coverage vs business needs
- [ ] Consolidate overlapping crons
- [ ] Identify gaps (what should we be monitoring but aren't?)

---

## Sync Instructions (For Ava)

**This file should ALWAYS be in sync with live crons.** Update process:

1. **Every Monday 8:00 AM ET:**
   - Run `cron list --includeDisabled=true` from OpenClaw gateway
   - Compare against this document
   - Update any changes (new crons, disabled, model reassignments, schedule changes)
   - Commit: `git add 01-Wiki/infrastructure/ACTIVE_CRONS.md && git commit -m "Update cron list - week of $(date +%Y-%m-%d)"`
   - Push to Vault

2. **When adding a new cron:**
   - Immediately add entry to this file (same day)
   - Include: Time, Agent, Model, Purpose, Output, Dependencies
   - Commit with cron creation

3. **When disabling a cron:**
   - Move to "Disabled Crons" section with Resolution date
   - Keep for 3 months as historical reference
   - Archive older disabled crons to memory/

---

## Dependencies & Credentials

All crons depend on these being configured + current:

| Resource | Status | Last Verified | Notes |
|----------|--------|---------------|-------|
| Supabase (orders, inventory) | ✅ | Apr 13 | Service role key valid |
| BigQuery (Zero dataset) | ✅ | Apr 13 | Project instant-contact-479316-i4 |
| Slack bot token | ✅ | Apr 13 | Token: xoxb-991301... |
| Telegram API | ✅ | Apr 13 | Chat ID: 5587457906 |
| AWS S3 (CDN) | ✅ | Apr 13 | elcellonline.com/atg/ |
| GDrive (Vault mount) | ✅ | Apr 13 | rclone configured |
| Gemini API (free tier) | ❌ | Apr 13 | QUOTA EXHAUSTED — reassign to Codex/Hermes |
| Kimi K2.5 (fallback) | ✅ | Apr 13 | Free tier, reliable |
| Codex (GPT-5.4) | ✅ | Apr 13 | Heavy data crons |
| Ollama local | ✅ | Apr 13 | Light infrastructure checks |

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-13 19:35 EDT  
**Next Review:** 2026-04-21 08:00 EDT (Monday)