# Skill: Data Quality Monitor
**Owner:** Sentinel | **Schedule:** Every 4 hours
**Priority:** P1 — stale data = wrong decisions
**Model:** Gemma 4 for checks, Haiku for anomaly reasoning

---

## Purpose

Check BigQuery, Supabase, and listings databases for data freshness, row count anomalies, and integrity issues. Catch stale pipelines before they affect reporting or marketplace operations.

---

## Data Sources to Monitor

### BigQuery (Ecell datasets)

| Dataset / Table | Expected Refresh | Freshness Check | Anomaly Check |
|----------------|-----------------|-----------------|---------------|
| sales_data | Daily | max(date) < 2 days ago | Daily row count ±30% vs 7-day avg |
| listings | Daily | max(updated_at) < 2 days ago | Total rows ±5% vs yesterday |
| orders | Hourly | max(created_at) < 4 hours ago | Hourly count ±50% vs same hour last week |
| inventory | Daily | max(snapshot_date) = today | Total SKUs ±2% vs yesterday |

### Supabase

| Table | Expected Refresh | Freshness Check |
|-------|-----------------|-----------------|
| products | Continuous | Any product updated in last 24h |
| orders | Continuous | Any order in last 4h (business hours) |

### PULSE Dashboard

| Metric | Check |
|--------|-------|
| Dashboard health | HTTP 200 on dashboard URL |
| Data freshness | Latest data point < 6 hours old |

---

## Check Logic

```
Every 4 hours:
  1. BigQuery freshness:
     For each monitored table:
       a. Query max timestamp column
       b. If older than threshold → WARNING
       c. If older than 2x threshold → ALERT
  
  2. BigQuery row counts:
     For each monitored table:
       a. Get today's row count
       b. Get 7-day rolling average
       c. If deviation > threshold → WARNING with context
       d. Zero rows when expected > 0 → ALERT
  
  3. Supabase freshness:
     For each monitored table:
       a. Check latest updated_at
       b. Apply business hours filter (skip overnight for order tables)
  
  4. PULSE health:
     a. Check dashboard endpoint
     b. Check data timestamp on dashboard
  
  5. Log all results to data/sentinel/data-quality.json
  6. Alert only on WARNING or ALERT
```

---

## Anomaly Detection (Simple)

Not ML — just sensible thresholds:

| Metric | Normal | Warning | Alert |
|--------|--------|---------|-------|
| Daily sales rows | ±30% of 7-day avg | 30-50% deviation | >50% or zero |
| Listing count | ±5% of yesterday | 5-10% drop | >10% drop |
| Order count (hourly) | ±50% of same hour last week | 50-80% deviation | >80% or zero |
| Data freshness | Within threshold | 1-2x threshold | >2x threshold |

**Weekend/holiday adjustment**: Sales and order volumes naturally drop. Use day-of-week averages, not simple rolling.

---

## BigQuery Queries

```sql
-- Freshness check
SELECT MAX(date) as latest_date,
       TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(date), HOUR) as hours_stale
FROM `project.dataset.sales_data`;

-- Row count anomaly
SELECT 
  COUNT(*) as today_rows,
  (SELECT AVG(daily_count) FROM (
    SELECT COUNT(*) as daily_count 
    FROM `project.dataset.sales_data`
    WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    GROUP BY date
  )) as avg_7d
FROM `project.dataset.sales_data`
WHERE date = CURRENT_DATE();
```

---

## Alert Format

```
--- SENTINEL ALERT ---
Severity: WARNING / CRITICAL
Skill: data-quality
What: {table} data is {hours}h stale (threshold: {threshold}h)
Detail: Last update: {timestamp}. Expected refresh: {expected}.
Impact: {what reports/dashboards/processes use this data}
Action: Check {pipeline_name} for failures. Verify source is sending data.
---
```

---

## Dependencies

- BigQuery service account (via ~/.config/gcloud/)
- Supabase connection (via .env)
- PULSE dashboard URL

---

## Changelog
- 2026-04-13 — Created. Freshness checks, row count anomalies, simple threshold-based detection.
