# CRON CALENDAR — Scheduled Jobs Registry

> Single source of truth for all automated jobs. Ava + Harry reference this to ensure jobs execute on time.
> Last updated: 2026-03-03

## Active Jobs

| ID | Name | Schedule | Time (EST) | Owner | Agent | Status | Description |
|----|------|----------|------------|-------|-------|--------|-------------|
| `fe10c64e` | Daily EOD Report | `0 19 * * *` | 7:00 PM daily | Ava | main | ⚠️ error | Gamma slides summary → Telegram |
| `ea6cb82e` | Nightly Mission | `0 2 * * *` | 2:00 AM daily | Ava | main | ⚠️ error | Mon=Intel, Tue=Audit, Wed=Content, Thu=Leads, Fri=Website, Sat=Trends, Sun=Recap |
| `0af7da5b` | Weekly Amazon | `0 8 * * 6` | Sat 8:00 AM | Ava | main | ✅ ok | Amazon sales session review |
| `c2921f82` | Weekly Momentum Brief | `0 8 * * 1` | Mon 8:00 AM | Ava | main | ✅ idle | BigQuery momentum analysis → AI narrative → Telegram + Drive |
| `8ad00cac` | Cron Health Check | `0 9 * * *` | 9:00 AM daily | Ava | main | ✅ idle | Verify all crons ran, alert on drift/error |

## Job Rotation (Nightly Mission)

| Day | Mission | Output |
|-----|---------|--------|
| Mon | Market Intelligence | Competitor/trend scan |
| Tue | Audit | Site/listing quality check |
| Wed | Content | Copy/asset review |
| Thu | Lead Generation | Opportunity identification |
| Fri | Website | Site performance/UX check |
| Sat | Trends | Weekly trend roundup |
| Sun | Recap | Week summary + next week plan |

## Error Log

| Date | Job | Error | Resolution |
|------|-----|-------|------------|
| 2026-03-03 | Daily EOD Report | error | TBD — needs investigation |
| 2026-03-03 | Nightly Mission | error | TBD — needs investigation |

## Rules
1. All cron jobs must be registered here
2. Harry + Ava check this calendar during heartbeats
3. Any job in error state for >24h gets escalated to Cem
4. New jobs require an entry here BEFORE creation
5. Job drift (>15 min late) gets flagged in next heartbeat

## How to Add/Modify
- OpenClaw CLI: `openclaw cron add/edit/remove`
- Always update this file to match
- Sync to Orbit PM as a recurring task card
