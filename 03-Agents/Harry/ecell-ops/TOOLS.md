# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

## Google Drive Sync

**Folder:** Clawdbot Shared Folder
**Local path:** `/home/ubuntu/clawd/gdrive_shared`
**Sync command:** `rclone sync "gdrive:/Clawdbot Shared Folder" /home/ubuntu/clawd/gdrive_shared`

Drop files in Google Drive → I can access them locally.

---

## API Keys Stored

| Service | Config Path | Status |
|---------|-------------|--------|
| Notion | `~/.config/notion/api_key` | ✅ Active |
| Apify | `~/.config/apify/api_key` | ✅ Active |
| Firecrawl | `~/.config/firecrawl/api_key` | ✅ Active |
| Google Drive | `~/.config/rclone/rclone.conf` (gdrive) | ✅ Active |
| Slack | `~/.config/slack/bot_token` | ✅ Active |
| Asana | `~/.config/asana/token` | ✅ Active |
| Kimi K2.5 | `~/.config/kimi/credentials` | ✅ Active |
| Supabase | `~/.config/supabase/credentials` | ✅ Active |
| Airtable | `~/.config/airtable/credentials` | ✅ Active |

---

## Competitor Analysis

**Workspace:** `/home/ubuntu/clawd/competitor_analysis/`
- `ANALYSIS_REPORT_2026-01-28.md` — Main competitor report
- `NBA_MERCHANDISE_REPORT_2026-01-28.md` — NBA license research
- `nba_images/` — Reference images from high-engagement posts

---

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Orbit PM Dashboard

- **URL:** https://orbit-pm.vercel.app/tasks
- **What:** Joint task sheet for Cem / Ava / Harry — pulled from Notion
- **API:** GET `/api/tasks` (list all), PATCH `/api/tasks/{id}` (update status)
- **Task source:** `/Users/clawdbot/clawd/projects/ai-coo/TASK_LIST.md` on iMac
- **Creating tasks:** Write to TASK_LIST.md on iMac via node (no POST API yet)
- **Daily routine:** Check and update task statuses regularly

---

## Specialist Sub-Agents

See `SPECIALIST_ROSTER.md` for full roster and cost policy.
- Default model: `gemini-flash` (all sub-agents)
- Opus 4.6: complex planning only
- N8N bots: `gpt-4o-mini` via OpenRouter

---

## N8N Instance

- **URL:** http://localhost:5678
- **API Key:** `~/.config/n8n/api_key`
- **Data:** `/home/ubuntu/clawd/projects/cs-automation/n8n-data`
- **Active Workflow:** HeadCase CS Chat (webhook: `/webhook/headcase-chat`)
- **OpenRouter credentials configured** (id: 2bcCqwLbpu8dPCcj)

---

*Updated: 2026-02-06*
