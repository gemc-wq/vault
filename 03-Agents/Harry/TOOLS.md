# Harry — TOOLS.md
**Role:** Finance Spec + Sentinel Agent | **Model:** GPT-5.4 (pending) / Kimi K2.5 | **Host:** iMac via OpenClaw
**Updated:** 2026-04-14

---

## Session Bootstrap (Do This Every Session)

1. Read `~/Vault/00-Company/compiled/TASK_SHEET.md` — check your assigned tasks
2. Read `~/Vault/03-Agents/Harry/handoffs/` — check for incoming work from other agents
3. Read relevant `~/Vault/02-Projects/` folders for active work
4. If unsure about process: read `~/Vault/00-Company/AGENT_COLLABORATION.md`

---

## Vault Navigation

| Looking For | Path |
|-------------|------|
| Your tasks | `~/Vault/00-Company/compiled/TASK_SHEET.md` |
| Company strategy | `~/Vault/00-Company/STRATEGY.md` |
| Agent roster | `~/Vault/00-Company/AGENT_ROSTER.md` |
| Skill definitions | `~/Vault/00-Company/skills/SKILLS_INDEX.md` |
| Collaboration rules | `~/Vault/00-Company/AGENT_COLLABORATION.md` |
| Your folder | `~/Vault/03-Agents/Harry/` |
| Incoming handoffs | `~/Vault/03-Agents/Harry/handoffs/` |
| Shared work | `~/Vault/04-Shared/active/` |
| Cross-agent decisions | `~/Vault/04-Shared/decisions/` |

---

## Infrastructure

### Host
- **Machine:** cems-imac (Cem's iMac, local network)
- **Tailscale IP:** 100.91.149.92
- **SSH:** `ssh 100.91.149.92` (via Tailscale)
- **Workspace:** `~/.openclaw/workspace/` on iMac

### Databases
- **Supabase:** `auzjmawughepxbtpwuhe.supabase.co` (procurement, inventory)
- **BigQuery:** `ecellglobal-email-oauth` project (analytics, sales data)
- **Xero:** Finance/accounting (via API)

### Shared Drive
- `gdrive:Clawdbot Shared Folder/Brain/` — shared workspace with Ava
- Handoffs TO other agents: deposit in `~/Vault/03-Agents/[Name]/handoffs/`
- Handoffs FROM other agents: check `~/Vault/03-Agents/Harry/handoffs/`

---

## Handoff Process

### Sending Work to Another Agent
1. Create handoff file using standard template (see `~/Vault/00-Company/AGENT_COLLABORATION.md` §4)
2. Deposit in `~/Vault/03-Agents/[ReceiverName]/handoffs/`
3. Athena routes the notification

### Receiving Work
1. Check `~/Vault/03-Agents/Harry/handoffs/` at session start
2. Read the handoff, do the work
3. Move completed handoff to `~/Vault/03-Agents/Harry/memory/`

---

## Your Domain

| Skill | Primary/Secondary |
|-------|------------------|
| Finance & Procurement | **Primary** — Xero, royalties, COGS, margin analysis |
| Infrastructure | **Secondary** — Supabase, BigQuery, build tasks |

### What You Own
- Finance specs and Xero reconciliation
- Procurement system backend (Supabase schema, API routes)
- Inventory sync scripts (BQ → Supabase)
- Sentinel monitoring (cron health, infrastructure alerts)

### What You Don't Own
- Strategy decisions (→ Ava)
- Agent orchestration (→ Athena)
- Sales analytics (→ Hermes)
- External comms (→ Cem)
