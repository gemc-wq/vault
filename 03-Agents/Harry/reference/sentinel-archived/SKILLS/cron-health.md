# Skill: Cron Health Monitor
**Owner:** Sentinel | **Schedule:** Every 30 minutes
**Priority:** P1 — missed cron = silent data gap
**Model:** Gemma 4 for checks, Haiku for anomaly reasoning

---

## Purpose

Verify all registered cron jobs ran on schedule, succeeded, and produced valid output. Detect silent failures before they cascade into stale data or broken workflows.

---

## Registered Crons

### Mac Studio LaunchAgents (user: openclaw)

| Cron | Schedule | Expected Output | Health Check |
|------|----------|-----------------|--------------|
| ZEUS Bot | Always on | Telegram responsive | PID file exists at zeus-agent/data/zeus.pid |
| Email Triage | Every 10 min (ZEUS internal) | data/email_triage_state.json updated | last_check < 15 min ago |
| Heartbeat | Daily 7AM ET (ZEUS internal) | data/daily/ log file | Today's file exists |
| Memory Consolidation | Nightly (ZEUS internal) | data/ checkpoint files | Modified today |

### OpenClaw Agents (localhost:18789)

| Cron | Schedule | Expected Output | Health Check |
|------|----------|-----------------|--------------|
| Ava EOD Report | Daily 6PM ET | Vault daily log | **ERROR since Mar 3** — needs fix |
| Ava Nightly Mission | Daily 11PM ET | Task updates | **ERROR since Mar 3** — needs fix |
| Hermes Gateway | Always on | /health responds | **DOWN** — needs restart |

### Harry (iMac — remote)

| Cron | Schedule | Expected Output | Health Check |
|------|----------|-----------------|--------------|
| TBD | TBD | Audit needed | Ping Harry for cron inventory |

---

## Check Logic

```
Every 30 minutes:
  1. For each registered cron:
     a. Check expected output exists and is fresh
     b. Compare last_run timestamp against schedule
     c. If output missing or stale:
        → Calculate how many cycles missed
        → If 1 cycle: WARNING (log only)
        → If 2+ cycles: ALERT to Athena
        → If 6+ cycles (3 hours): P0 ALERT
  
  2. Check ZEUS process health:
     a. PID file exists and process is running
     b. Telegram bot responding (last message < 30 min)
  
  3. Check OpenClaw gateway:
     a. GET http://localhost:18789/health
     b. If non-200: ALERT immediately
  
  4. Log results to data/sentinel/cron-health.json
```

---

## Freshness Thresholds

| Cron Interval | WARNING after | ALERT after |
|---------------|---------------|-------------|
| 10 min | 15 min | 30 min |
| 30 min | 45 min | 90 min |
| Hourly | 90 min | 3 hours |
| Daily | 26 hours | 48 hours |

---

## Alert Format

```
--- SENTINEL ALERT ---
Severity: WARNING / CRITICAL
Skill: cron-health
What: {cron_name} missed {N} cycles
Detail: Last successful run: {timestamp}. Expected interval: {interval}.
Impact: {what data/process goes stale}
Action: Check logs at {log_path}. Restart if needed.
---
```

---

## Known Issues (as of 2026-04-13)

1. **Ava EOD Report** — ERROR since 2026-03-03. Needs investigation.
2. **Ava Nightly Mission** — ERROR since 2026-03-03. Needs investigation.
3. **Hermes Gateway** — DOWN. Needs restart.
4. **Harry cron inventory** — Unknown. Need to request from Harry.

---

## Changelog
- 2026-04-13 — Created. Initial cron registry from Mac Studio audit.
