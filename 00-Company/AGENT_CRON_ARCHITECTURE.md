# Agent-Cron Architecture — Replacing N8N with Agent Polling
**Created:** 2026-04-12 | **Author:** Athena | **Directive from:** Cem
**Status:** APPROVED PATTERN — apply to all new automations

---

## Core Principle

> **No middleware. Agents check sources directly on a cron, reason about what they find, and act.**

Instead of N8N sitting between an event source (email, Slack, webhook) and the action, the specialist agent runs on a schedule, connects to the source via MCP/API connector, reads what's new, and decides what to do.

```
OLD:  Event → N8N webhook → fixed workflow steps → output
NEW:  Agent cron (Xmin) → check source via MCP → reason → act
```

---

## Why This Is Better

| Factor | N8N Workflow | Agent Cron |
|--------|-------------|------------|
| **Edge cases** | Fails silently — fixed paths can't handle unexpected input | Agent reasons about unexpected input, escalates if unsure |
| **Maintenance** | Each workflow is manual JSON to build and debug | Agent skill is a prompt + tools — easier to modify |
| **Context** | Stateless — each run starts from zero | Agent has memory — knows what it handled last run |
| **Credential management** | N8N stores creds in its own DB | MCP connectors scope creds per agent |
| **Observability** | N8N execution logs (separate UI) | Control Centre shows all agent activity in one view |
| **Cost** | N8N hosting + maintenance | Gemma 4 ($0) for most polling; Sonnet/Haiku for reasoning |
| **Single point of failure** | N8N goes down = all automations stop | Each agent runs independently |

---

## The Pattern

### 1. Email Monitoring (Replaces N8N Email Triage)

```
Agent:     Hermes (or dedicated CS agent)
Cron:      Every 10 minutes
Connector: Gmail MCP (gmail_search_messages, gmail_read_message)
Logic:
  1. Search for unread messages since last check
  2. For each email:
     - Classify: customer complaint / order query / licensor / supplier / spam
     - Customer → draft reply (gmail_create_draft) + log to Supabase
     - Licensor → flag to Athena → escalate to Cem (Red Zone)
     - Supplier → route to Harry (finance)
     - Spam → archive
  3. Update last-checked timestamp in agent memory
```

### 2. Slack Digest (Replaces N8N Slack Daily Digest)

```
Agent:     Iris (intelligence)
Cron:      Every 30 minutes (digest compiled at 4AM ET)
Connector: Slack MCP (future) or Slack API via Bash
Logic:
  1. Pull messages from monitored channels since last check
  2. Classify by relevance (design updates, order issues, PH team questions)
  3. Append to daily digest in memory
  4. At 4AM: compile full digest → Telegram to Cem
```

### 3. Order Monitoring (Replaces N8N Order Webhooks)

```
Agent:     Zero (operations)
Cron:      Every 15 minutes
Connector: SP-API MCP or direct API call
Logic:
  1. Check for new orders since last poll
  2. For each order:
     - Match SKU → fulfillment location (FL, PH, UK)
     - Check inventory availability
     - Route to correct warehouse queue
     - Flag if out-of-stock → escalate to Athena
  3. Update order counts in Supabase
```

### 4. Listing Health Check (Replaces N8N Listing Monitor)

```
Agent:     Hermes (sales)
Cron:      Every 2 hours
Connector: SP-API (Catalog Items API)
Logic:
  1. Check top-100 ASINs for suppression/Buy Box loss
  2. Compare current price vs target price
  3. Flag deviations > 5% → alert Athena
  4. Log health metrics to BigQuery
```

### 5. System Health (Replaces N8N Zero Health Check)

```
Agent:     Athena (orchestrator)
Cron:      Every 30 minutes
Connector: HTTP requests to service endpoints
Logic:
  1. Ping: Zero portal, Supabase, BigQuery, Ollama, OpenClaw gateway
  2. Check response times and error rates
  3. If service down > 2 checks → alert Cem
  4. Log to agent_heartbeats table
```

### 6. Data Freshness (Replaces N8N Data Pipeline Checks)

```
Agent:     Iris (intelligence)
Cron:      Daily 1:00 AM
Connector: BigQuery MCP, Supabase API
Logic:
  1. Check last-updated timestamp on key tables
  2. Flag if any table > 24h stale
  3. Attempt re-sync if possible
  4. Report to Athena if manual intervention needed
```

---

## MCP Connectors Available Now

These are already loaded and can be used by agents immediately:

| Connector | Tools | Use For |
|-----------|-------|---------|
| **Gmail MCP** | search, read, create_draft, list_labels | Email triage, CS, supplier comms |
| **Google Calendar MCP** | list_events, create_event, find_free_time | Scheduling, deadline tracking |
| **Notion MCP** | search, create_pages, update_page | Project tracking (if used) |
| **Figma MCP** | get_design_context, get_screenshot | Design review, asset checking |

### Connectors Needed

| Connector | Priority | Use For |
|-----------|----------|---------|
| **Slack MCP** | P1 | Replace N8N Slack digest |
| **Xero MCP** | P1 | Harry finance agent direct access |
| **SP-API MCP** | P1 | Order monitoring, listing health |
| **Supabase MCP** | P2 | Direct table reads/writes from agents |

---

## Cron Registry Format

Every agent cron registered in the Control Centre:

```
cron_id:       email-triage-hermes
agent:         Hermes
skill:         customer-service/email-triage
schedule:      */10 * * * *  (every 10 min)
connector:     Gmail MCP
last_run:      2026-04-12T15:30:00Z
status:        OK
next_run:      2026-04-12T15:40:00Z
avg_duration:  45s
avg_cost:      $0.00 (Gemma 4)
```

---

## Migration Checklist

For each N8N workflow being replaced:

- [ ] Document what the N8N workflow does (input → logic → output)
- [ ] Identify which specialist agent owns this function
- [ ] Identify which MCP connector provides access
- [ ] Write the agent skill (prompt + tools)
- [ ] Set up the cron schedule
- [ ] Run both N8N and agent cron in parallel for 1 week
- [ ] Compare outputs — agent must match or exceed N8N accuracy
- [ ] Cut over: disable N8N workflow, agent cron goes live
- [ ] Register in Control Centre

---

## Implementation Priority

| # | N8N Workflow to Replace | Agent | Cron | Effort | Impact |
|---|------------------------|-------|------|--------|--------|
| 1 | Email triage | Hermes/CS | 10 min | Medium | High — CS response time |
| 2 | Slack daily digest | Iris | 30 min | Low | Medium — Cem visibility |
| 3 | Zero health check | Athena | 30 min | Low | High — uptime monitoring |
| 4 | Data freshness | Iris | Daily | Low | Medium — data quality |
| 5 | Order monitoring | Zero | 15 min | High | High — fulfillment speed |
| 6 | Listing health | Hermes | 2 hours | Medium | High — revenue protection |

---

## DelegAIt Product Angle

This "N8N → Agent Cron" migration pattern is directly productizable:
- SMBs using Zapier/N8N/Make hit the same wall — brittle workflows that fail on edge cases
- "Replace your automation tool with an AI agent that checks and reasons" is a compelling pitch
- Package: audit existing workflows → design agent crons → migrate → monitor via Control Centre
- Price point: $500-1,500 per workflow migration

---

## Changelog
- 2026-04-12 — Created. Documented agent-cron pattern, 6 migration targets, MCP connector inventory, Control Centre cron registry format.
