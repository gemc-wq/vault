# Athena/Zeus ↔ Ava Integration
*Owner: Cem | Documented: 2026-04-10 | Status: Partial — bidirectional comms needed*

---

## What Zeus/Athena Is

**Zeus** is a Python orchestrator running permanently on Mac Studio at `/Users/openclaw/zeus-agent/`. It runs on Anthropic's Claude Code CLI using **ChatGPT-style OAuth** (not API key billing), giving access to **Claude Opus 4.6 for free** via subscription.

**Athena** is the AI brain inside Zeus — she's the high-reasoning planner and strategist. Because she runs on Opus 4.6 via OAuth, she should be used for complex tasks, architecture decisions, and multi-agent planning.

**Why this matters:** Opus 4.6 via API costs $5/$25 per MTok. Via OAuth subscription, it's effectively free. Zeus/Athena is our access to frontier-level reasoning without API cost.

---

## Current Architecture

```
Cem (Telegram)
     │
     ▼
Zeus (Python) ──── Athena (Claude Code OAuth / Opus 4.6)
     │                      │
     │  webhook              │  webhook
     ▼                      ▼
OpenClaw (:18789) ──── Ava (Haiku 4.5 + sub-agents)
```

---

## Communication Status

### Athena → Ava ✅ (works)
- Athena calls OpenClaw webhook: `POST /plugins/webhooks/zeus`
- Header: `X-OpenClaw-Webhook-Secret: f681fbf4e3ce7a35dae91ee14e12fd997b229008f5969a9f`
- Lands in session: `agent:main:main`
- Secret stored in OpenClaw env as `OPENCLAW_WEBHOOK_SECRET`

### Ava → Athena ⏳ (workaround only, needs proper solution)
- **Current workaround:** Ava posts to Zeus's Telegram bot (`8741359019:AAGCHs1JTckbf5XqsSTG3CII-8hH_90nMz0`) to Cem's chat ID — Athena picks it up via Telegram
- **Problem:** Not programmatic. Goes through Cem's chat. No structured payload.
- **Proper solution needed** (see options below)

---

## Intended Usage Pattern

**Ava → Athena (for planning/strategy):**
1. Ava identifies a task requiring deep reasoning (architecture, complex strategy, multi-step orchestration)
2. Ava sends task to Athena with context
3. Athena (Opus 4.6) produces a structured plan
4. Plan is handed back to Ava for execution

**Athena → Ava (for execution):**
1. Athena plans work and breaks it into executable tasks
2. Athena calls OpenClaw webhook to inject tasks into Ava's session
3. Ava executes (listings, Shopify, data pipelines, etc.)
4. Ava reports results back

---

## Data Handoff Options (to be decided)

| Option | Pros | Cons |
|---|---|---|
| **GDrive Handoffs folder** | Already exists (`Brain/Handoffs/`), both agents can read/write | Polling required, no push |
| **Supabase shared table** | Real-time, structured, both agents have access | Needs schema design |
| **Zeus HTTP endpoint** | Clean, push-based | Zeus needs code change to add server |
| **OpenClaw webhook payload** | Already works Athena→Ava | No reverse channel yet |

*Recommended: Start with GDrive Handoffs folder for MVP. Add Supabase table when volume requires it.*

---

## Key Credentials

| Item | Value |
|---|---|
| Zeus location | `/Users/openclaw/zeus-agent/` |
| Zeus Telegram bot | `@zeussbossman_bot` |
| Zeus bot token | `8741359019:AAGCHs1JTckbf5XqsSTG3CII-8hH_90nMz0` |
| OpenClaw webhook | `http://localhost:18789/plugins/webhooks/zeus` |
| Webhook secret | `f681fbf4e3ce7a35dae91ee14e12fd997b229008f5969a9f` |
| Athena model | Claude Opus 4.6 (via Claude Code OAuth) |
| Ava model | Claude Haiku 4.5 (Anthropic API) |

---

## Next Steps

- [ ] Design bidirectional Ava↔Athena protocol
- [ ] Decide on data handoff mechanism (GDrive vs Supabase)
- [ ] Add simple HTTP endpoint to Zeus OR write Supabase queue
- [ ] Test: Ava triggers Athena task → Athena plans → Athena calls back to Ava → Ava executes
- [ ] Document the full end-to-end flow once working

---

*Note: OpenClaw's recent update includes ACP/webhook access to Claude CLI — this may be the mechanism for Ava→Athena triggering. Needs investigation.*
