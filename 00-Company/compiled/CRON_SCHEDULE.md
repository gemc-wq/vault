# Cron Schedule — Mac Studio
**Last updated:** 2026-04-10 | **Updated by:** Athena (from Cem)
**Window:** Midnight–7AM ET | Daytime free for work

---

## Gemma 4 (Local — Ollama, $0.00)

| Cron | Time (ET) | Purpose |
|------|-----------|---------|
| Data Freshness Check | 1:00 AM daily | Verify data pipelines are current |
| EOD Memory Summary | 11:00 PM daily | Consolidate daily agent memory |
| Weekly Memory Review | 1:00 AM Saturday | Deep memory consolidation + pruning |
| Blocked Tasks Reminder | 2:00 AM Mon/Thu | Flag stale/blocked tasks for escalation |
| Shipping Template Audit | 2:00 AM Wednesday | Verify shipping templates are correct |

## Gemini Flash (External — Google API)

| Cron | Time (ET) | Purpose |
|------|-----------|---------|
| Zero Health Check | 3:00 AM daily | System health ping (status: ok, ~73s) ✅ |
| Slack Daily Digest | 4:00 AM daily | Parse Slack → digest for Telegram |
| Security Audit | 6:00 AM Sunday | Security scan across systems |

## Gemma 4 — Weekly Data Crons (Local, $0 — switched from Gemini Flash 2026-04-10)

| Cron | Time (ET) | Purpose | Timeout |
|------|-----------|---------|---------|
| Listings US | 1:00 AM Saturday | US marketplace listing analysis | 600s |
| Listings UK | 2:00 AM Saturday | UK marketplace listing analysis | 600s |
| Listings DE + Movers | 3:00 AM Saturday | DE listings + cross-region movers | 600s |
| PULSE Leaderboard | 5:00 AM Monday | Weekly sales leaderboard + alerts | 600s |

## Athena-Managed (LaunchAgents + Crontab)

| Cron | Time (ET) | Engine | Status |
|------|-----------|--------|--------|
| EOD Digest → Telegram | 8:00 AM daily | Node.js + curl | ✅ Running (needs SSL cleanup) |
| Vault Compiler | 2:00 AM daily | Gemma 4 / Ollama | ✅ Fixed (UTF-8 error resolved) |

## Always-On Services

| Service | LaunchAgent | Status |
|---------|-------------|--------|
| ZEUS Bot (Athena) | ai.athena.bot | ✅ Running |
| OpenClaw Gateway | ai.openclaw.gateway | ✅ Running |
| Ollama (Gemma 4) | homebrew.mxcl.ollama | ✅ Running |
| Hermes Gateway | ai.hermes.gateway | ⚠️ Not running — needs restart |

---

*All times are Eastern Time (ET). Mac Studio handles all cron jobs overnight to keep daytime compute free.*
