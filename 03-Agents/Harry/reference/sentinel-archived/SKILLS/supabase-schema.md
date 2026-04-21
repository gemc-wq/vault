# Skill: Supabase Schema Watcher
**Owner:** Sentinel | **Schedule:** Nightly 3AM ET
**Priority:** P1 — schema change can silently break downstream apps
**Model:** Gemma 4 for diff, Haiku for impact assessment

---

## Purpose

Detect schema changes in Supabase projects. Cross-reference changes against dependent apps and crons. Alert when a change could break something downstream.

---

## What to Watch

### Tables of Interest

| Table / Schema | Used By | Impact if Changed |
|---------------|---------|-------------------|
| listings / products | ListingForge, PIE, PULSE | Marketplace feeds break |
| orders | Zero 2.0, fulfillment portal | Order processing fails |
| designs / assets | Design pipeline, Ava briefs | Creative workflow breaks |
| agent_status (future) | Control Centre | Monitoring blind spot |
| cron_registry (future) | Control Centre, Sentinel | Cron monitoring breaks |

### Schema Snapshot

```sql
-- Take nightly snapshot of all public tables
SELECT 
  table_name,
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

Store snapshot at: `data/sentinel/schema-snapshot.json`

---

## Check Logic

```
Nightly 3AM ET:
  1. Pull current schema from information_schema
  2. Compare against last night's snapshot
  3. For each change detected:
     a. Classify: ADD_COLUMN, DROP_COLUMN, ALTER_TYPE, NEW_TABLE, DROP_TABLE
     b. Look up affected downstream apps (from table above)
     c. If DROP_COLUMN or ALTER_TYPE on used column:
        → P0 ALERT — breaking change
     d. If ADD_COLUMN or NEW_TABLE:
        → INFO log (non-breaking)
     e. If DROP_TABLE:
        → P0 ALERT — data loss risk
  4. Save new snapshot
  5. Log diff to data/sentinel/schema-changes.log
```

---

## RLS Audit (weekly, bundled with schema check on Sundays)

```sql
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND rowsecurity = false;
```

Any table with `rowsecurity = false` that contains business data → WARNING.

Tables expected to have RLS disabled (acceptable):
- `_migrations`
- `schema_version`
- Public lookup tables with no sensitive data

---

## Alert Format

```
--- SENTINEL ALERT ---
Severity: CRITICAL / WARNING / INFO
Skill: supabase-schema
What: Schema change detected — {change_type} on {table}.{column}
Detail: {old_definition} → {new_definition}
Impact: Used by {app_list}. {breaking_or_not}.
Action: Verify {app_list} still work. Update queries if needed.
---
```

---

## Dependencies

- Supabase connection string (from .env or Supabase Management API)
- `psycopg2` or `supabase-py` for direct SQL
- Alternative: Supabase Management API for schema inspection

---

## Changelog
- 2026-04-13 — Created. Schema snapshot approach, RLS audit, downstream dependency map.
