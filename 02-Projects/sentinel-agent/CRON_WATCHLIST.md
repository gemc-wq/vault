# Sentinel Agent — Critical Crons Watchlist
**Source:** Cem, 2026-04-13 | **Updated:** 2026-04-13 23:40 ET
**Status:** All 16 crons on stable APIs — 0 Ollama dependencies

---

## Daily Crons

| Cron | Time (ET) | Agent | Model | Purpose | Status |
|------|-----------|-------|-------|---------|--------|
| Data Freshness Check | 1:05 AM | main | GPT-5.4 | Supabase orders table freshness (>7 days = alert) | ✅ Running |
| S3 Image Audit | 2:00 AM | main | — | Shopify design image coverage (26 designs) | ✅ Running |
| Zero Cron Health Check | 3:10 AM | main | GPT-5.4 | BigQuery Zero cron_jobs table (Amazon import errors) | ✅ Running |
| Slack Daily Digest | 4:10 AM | main | — | Aggregate PH team EOD reports (#eod-creative, #eod-listings, #eod) | ✅ Running |
| Daily EOD Memory Summary | 11:00 PM | main | Kimi K2.5 | Write day's summary to memory/YYYY-MM-DD.md | ✅ Running |
| Daily Memory Sync to Vault | 11:00 PM | main | — | Copy daily notes to Vault backup | ✅ Running |

## Weekly Crons

| Cron | Day/Time (ET) | Agent | Model | Purpose | Status |
|------|---------------|-------|-------|---------|--------|
| Mid-Week Shipping Template Audit | Wed 2:00 AM | pixel | GPT-5.4 | Check new Amazon listings for wrong shipping templates (US/UK) | ✅ Running |
| Blocked Tasks Reminder | Mon/Thu 2:10 AM | main | — | Flag tasks blocked >3 days | ✅ Running |
| Friday Report Reminder | Fri 5:00 PM | main | — | Remind Cem to download weekly reports | ✅ Running |
| Weekly PULSE Leaderboard Report | Mon 5:00 AM | main | — | Top devices, designs, movers (Supabase RPC) | ✅ Running |
| Weekly Listings Analysis — US | Sat 1:00 AM | main | — | Parse US Active Listings, delta, new SKUs, FBA % | ✅ Running |
| Weekly Listings Analysis — UK | Sat 2:00 AM | main | — | Parse UK Active Listings, delta, new SKUs, FBA % | ✅ Running |
| Weekly Listings Analysis — DE | Sat 3:00 AM | main | — | Parse DE Active Listings, champions movers, cross-region gaps | ✅ Running |
| Weekly Memory Review & Backup | Sat 1:00 AM | main | GPT-5.4 | Review past week's memory, update MEMORY.md, sync to GDrive | ✅ Running |
| Weekly Security Audit | Sun 6:30 AM | main | GPT-5.4 | OpenClaw version, firewall, ports, Tailscale peers | ✅ Running |

## ZEUS Heartbeat Crons (NEW — Apr 13)

| Cron | Time (ET) | Engine | Purpose | Status |
|------|-----------|--------|---------|--------|
| Morning Skill Reminder | 9:03 AM weekdays | Gemma 4 | Top task per bucket, neglected bucket nudge | ✅ Deployed |
| Afternoon Skill Check-in | 2:07 PM weekdays | Gemma 4 | Touched/untouched buckets, quick wins | ✅ Deployed |
| Daily Brief + Board | 8:00 AM daily | Gemma 4 | Executive summary + visual task board | ✅ Running |
| Email Triage | Every 10 min | Python (no LLM) | Gmail classification, Tier 1 alerts | ✅ Running |

## One-Time Crons

| Cron | Trigger | Purpose | Status |
|------|---------|---------|--------|
| NFL License Sell-Off Reminder | May 6, 2026 | Reminder that NFL sell-off ends ~Jun 29 | ⏳ Scheduled |

## Disabled Crons

- Harry iMac Telegram Monitor (disabled) — Was checking Harry's 409 errors
- HB401 Sprint Daily EOD Check (disabled) — Sprint completed Mar 28

## Critical Databases to Monitor

| Database | Purpose | Freshness Requirement | Alert Threshold |
|----------|---------|----------------------|-----------------|
| Supabase (orders, inventory) | Daily transaction log | <24 hours | >7 days stale |

---

## Model Migration Log (Apr 13)

| Cron | Old Model | New Model | Reason |
|------|-----------|-----------|--------|
| Data Freshness | ollama/gemma4 | openai-codex/gpt-5.4 | Eliminate Ollama dependency |
| Zero Health Check | moonshot/kimi | openai-codex/gpt-5.4 | Upgrade reliability |
| Shipping Audit | ollama/gemma4 | openai-codex/gpt-5.4 | Eliminate Ollama dependency |
| EOD Memory | google/gemini-3 | moonshot/kimi-k2-0905 | Avoid Google rate limits |
| Security Audit | ollama/gemma4 | openai-codex/gpt-5.4 | Eliminate Ollama dependency |

**Result:** 0 Ollama dependencies for OpenClaw crons. Gemma 4 still used by ZEUS heartbeat (local, separate from cron pipeline).

---

## Sentinel Design Notes
- 16 OpenClaw crons + 4 ZEUS heartbeat crons = 20 total monitored
- 0 crons in Reset state (all re-enabled after model migration)
- All OpenClaw crons on GPT-5.4 or Kimi K2.5 (proven reliable)
- ZEUS heartbeat crons use Gemma 4 local (falls back to Claude SDK if Ollama down)
- Key risk: Zero Cron Health Check — if this fails, Amazon imports silently stop
- NFL one-time cron is business-critical deadline (license sell-off)
