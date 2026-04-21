# Agent Infrastructure Overview
*Owner: Athena | Last Updated: 2026-04-13 | Status: ACTIVE*

---

## Network Topology

```
┌──────────────────────────────────────────────────────────────────┐
│                     TAILSCALE MESH NETWORK                        │
│                                                                    │
│  ┌─────────────────────┐    ┌─────────────────────┐               │
│  │  Mac Studio          │    │  iMac                │               │
│  │  100.72.19.27        │    │  100.91.149.92       │               │
│  │  User: openclaw      │    │  User: clawdbot      │               │
│  │                      │    │                      │               │
│  │  ZEUS/Athena (Opus)  │    │  Harry (Kimi K2.5)   │               │
│  │  OpenClaw Gateway    │    │  OpenClaw Gateway     │               │
│  │  Sentinel            │    │  13 cron jobs         │               │
│  │  Email Triage        │    │  Procurement App      │               │
│  │  Gemma 4 (Ollama)    │    │  Inventory Sync       │               │
│  │  Vault (Obsidian)    │    │  EVRI Fulfillment     │               │
│  └──────────┬───────────┘    └──────────┬───────────┘               │
│             │                           │                           │
│             │  SSH: clawdbot@100.91.149.92 (key auth, ~320ms)      │
│             │  rsync: memory sync daily                             │
│             │                                                       │
│  ┌──────────┴───────────┐                                          │
│  │  HP PC (Windows)      │                                          │
│  │  100.120.86.40        │                                          │
│  │  User: Cem            │                                          │
│  │  (Development)        │                                          │
│  └──────────────────────┘                                          │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                        CLOUD SERVICES                             │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Google Cloud  │  │ AWS          │  │ Supabase     │            │
│  │ • BigQuery    │  │ • Zero (EC2) │  │ • Orders DB  │            │
│  │ • Datastream  │  │ • S3 (media) │  │ • Products   │            │
│  │ • Cloud Run   │  │              │  │ • Inventory   │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Anthropic    │  │ Vercel       │  │ GitHub       │            │
│  │ • Managed    │  │ • ecell.app  │  │ • All repos  │            │
│  │   Agents     │  │ • Dashboards │  │ • CI/CD      │            │
│  │   (planned)  │  │              │  │              │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Agent Roster

| Agent | Model | Host | Tailscale IP | Port | Role | Status |
|-------|-------|------|-------------|------|------|--------|
| **Athena/ZEUS** | Claude Opus 4.6 (OAuth) | Mac Studio | 100.72.19.27 | — | Master Orchestrator | 🟢 Active |
| **Ava** | Haiku 4.5 + Advisor (Opus) | Mac Studio | 100.72.19.27 | 18789 | CPO — Strategy, Listings | 🟢 Active |
| **Harry** | Kimi K2.5 | iMac | 100.91.149.92 | 18789 | Finance, Procurement | 🟢 Active |
| **Hermes** | GLM via OpenRouter | Mac Studio | 100.72.19.27 | 18789 | Data Analyst, BQ, Sales | 🟢 Active (Telegram) |
| **Sentinel** | Gemma 4 + Haiku | Mac Studio | 100.72.19.27 | — | Infrastructure Watcher | 🟢 Built (pending restart) |

### Sub-agents (ZEUS internal)

| Agent | Model | Purpose |
|-------|-------|---------|
| researcher | Sonnet | Web research, document reading |
| coder | Opus | Code writing, debugging |
| analyst | Sonnet | Data analysis, BQ queries |
| delegator | Haiku | Routes to OpenClaw agents |
| reviewer | Opus | QA, self-improvement |
| strategist | Sonnet | Strategic heartbeat |

---

## Communication Channels

```
                    ┌─────────────────┐
                    │   Cem (Human)   │
                    │   Telegram App  │
                    └───────┬─────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
     ┌──────────────┐ ┌──────────┐ ┌──────────┐
     │ ZEUS/Athena  │ │ Hermes   │ │ Harry    │
     │ @zeussbossman│ │ Telegram │ │ (no Tg)  │
     │ _bot         │ │ (direct) │ │          │
     └──────┬───────┘ └──────────┘ └──────────┘
            │
            ├──► OpenClaw Webhook ──► Ava
            │    POST /plugins/webhooks/zeus
            │
            ├──► SSH ──► Harry (iMac)
            │    clawdbot@100.91.149.92
            │
            ├──► OpenClaw Gateway API ──► Any agent
            │    POST localhost:18789/v1/chat/completions
            │
            └──► Telegram Bot API ──► Cem
                 (alerts, briefs, voice notes)
```

### Channel Matrix

| From → To | Channel | Direction | Status |
|-----------|---------|-----------|--------|
| Cem → Athena | Telegram (text/voice) | ✅ Bidirectional | 🟢 Working |
| Cem → Hermes | Telegram (direct) | ✅ Bidirectional | 🟢 Working |
| Athena → Ava | OpenClaw webhook | → One-way | 🟢 Working |
| Ava → Athena | Telegram (workaround) | → One-way | 🟡 Needs proper solution |
| Athena → Harry | SSH via Tailscale | → One-way | 🟢 Working (verified) |
| Harry → Athena | GDrive Handoffs folder | → Polling | 🟡 Manual |
| Athena → Hermes | OpenClaw ACP | → One-way | 🟢 Working |
| Ava ↔ Harry | GDrive Handoffs folder | ↔ Bidirectional | 🟡 Polling |
| Any agent → Cem | Telegram Bot API | → Push | 🟢 Working |

### Communication Gaps (to fix)

1. **Ava → Athena**: No programmatic reverse channel. Ava posts to Cem's Telegram as workaround.
2. **Harry → Athena**: No push channel. GDrive polling only. Could add: Harry writes to Supabase, Sentinel watches.
3. **No unified message bus**: Each channel is point-to-point. Future: Supabase `agent_messages` table as central bus.

---

## Data Sync Paths

### Harry Memory → Vault (NEW — automated)

```bash
# Daily rsync: iMac memory → Vault
rsync -avz clawdbot@100.91.149.92:~/.openclaw/workspace/memory/ \
  /Users/openclaw/Vault/03-Agents/Harry/memory-imac/
```

- **Source**: `clawdbot@100.91.149.92:~/.openclaw/workspace/memory/`
- **Destination**: `/Users/openclaw/Vault/03-Agents/Harry/memory-imac/`
- **Files**: 41 memory logs (Jan 2026 — present)
- **Schedule**: Daily via Sentinel cron-health skill

### Ava ↔ Harry Handoffs

- **Folder**: `gdrive:Clawdbot Shared Folder/Brain/Handoffs/`
- **Format**: `HANDOFF_FROM_{AGENT}_YYYY-MM-DD_{TOPIC}.md`
- **Also mirrored**: iMac at `~/.openclaw/workspace/handoffs/`

### Vault → All Agents

- **Vault location**: `/Users/openclaw/Vault/` (Mac Studio, Obsidian)
- **Athena**: Direct filesystem access
- **Ava**: Via OpenClaw Memory MCP (read-only)
- **Harry**: No direct access. Gets context via handoffs or SSH-delivered files.
- **Hermes**: Via OpenClaw ACP bridge

---

## Cron Registry (All Machines)

### Mac Studio — ZEUS Internal

| Cron | Schedule | Engine | Status |
|------|----------|--------|--------|
| Email Triage | Every 10 min | EmailTriageEngine | 🟢 Active |
| Heartbeat | Daily 7AM ET | HeartbeatEngine | 🟢 Active |
| Sentinel: Cron Health | Every 30 min | SentinelEngine | 🟢 Built |
| Sentinel: Security Audit | Daily 4AM ET | SentinelEngine | 🟢 Built |
| Sentinel: GitHub Activity | Daily 5AM ET | SentinelEngine | 🟢 Built |
| Memory Consolidation | Nightly | consolidation.py | 🟢 Active |

### Mac Studio — OpenClaw (Ava)

| Cron | Schedule | Agent | Status |
|------|----------|-------|--------|
| EOD Report | Daily 6PM ET | main | 🔴 ERROR since Mar 3 |
| Nightly Mission | Daily 11PM ET | main | 🔴 ERROR since Mar 3 |

### iMac — OpenClaw (Harry)

| Cron | Schedule | Agent | Status |
|------|----------|-------|--------|
| Weekly Momentum Brief | Mon 5AM ET | main | 🔴 Error |
| Cron Health Check | Daily 9AM ET | main | 🟢 OK |
| Morning Brief | Daily 8AM ET | ? | 🟢 OK |
| FX Rates Daily Sync | Daily 1:30AM ET | main | 🟢 OK |
| BQ→Supabase Orders Sync | Daily 2AM ET | main | 🔴 Error |
| Weekly Memory Review | Sat 9AM ET | main | 🟢 OK |
| Weekly Workspace Backup | Sat 9:30AM ET | main | 🟢 OK |
| BQ→Supabase Inventory Sync | Daily 3AM ET | main | 🟢 OK |
| EVRI EU Fulfillment Nightly | Daily midnight ET | main | 🟢 OK |
| Morning Audio Brief (Cem) | Daily 6AM ET | main | ⏸ Disabled |
| Daily Trends (US+UK) | Daily 3AM ET | main | ⏸ Disabled |
| Xero API Scopes Reminder | — | main | ⏸ Disabled (error) |
| Image Library Reminder | — | main | ⏸ Disabled (one-time) |

### Cloud (Future — Managed Agents)

| Cron | Schedule | Platform | Status |
|------|----------|----------|--------|
| BQ Freshness Check | Every 4h | Anthropic Managed Agents | 📋 Planned |
| Supabase Health | Every 30 min | Anthropic Managed Agents | 📋 Planned |
| GitHub Activity | Daily 5AM | Anthropic Managed Agents | 📋 Planned |

---

## OpenClaw Gateway Configuration

### Mac Studio (localhost:18789)

**Available agents**: main, atlas, bolt, pixel, prism, sven, sven2, iris, codex, hermes-agent

**Cron model policy**: ALL crons run on FREE models only
- Primary: `pixel` → `google/gemini-3-flash-preview`
- Backup: `bolt` → `google/gemini-3.1-pro-preview`
- Also free: `openai-codex/gpt-5.4`, `moonshot/kimi-k2-0905-preview`
- **Never** use `main`, `opus`, or `anthropic/*` in crons

### iMac (100.91.149.92:18789)

**Available agents**: main (Harry — Kimi K2.5)
**SSH access**: `ssh clawdbot@100.91.149.92` (key auth, passwordless)

---

## Security & Access

| Credential | Stored At | Risk Level |
|------------|-----------|------------|
| OpenClaw Gateway Token | zeus-agent/.env | HIGH — full agent access |
| Telegram Bot Token | zeus-agent/.env | HIGH — bot hijack |
| Gmail OAuth Token | zeus-agent/data/gmail_token.json | HIGH — email access |
| Google Client Secret | ~/.config/gws/client_secret.json | HIGH — OAuth impersonation |
| Supabase Service Key | ecell-app/.env.local | HIGH — full DB access |
| BigQuery Service Account | ~/.config/gcloud/ | HIGH — data warehouse |
| SSH Key (Mac Studio → iMac) | ~/.ssh/ (key auth) | HIGH — remote access |

**Sentinel** monitors all repos and vault for exposed credentials daily.

---

## Resilience & Failover

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| Mac Studio internet down | ALL monitoring stops, no alerts | Cloud tier via Managed Agents (planned) |
| Mac Studio power outage | Same as above | UPS + cloud tier |
| iMac offline | Harry crons stop, no finance sync | Sentinel detects via SSH ping failure |
| Tailscale down | No iMac access from Mac Studio | Direct LAN if same network, otherwise wait |
| OpenClaw crash | Ava/Hermes unreachable | LaunchAgent auto-restart (KeepAlive=true) |
| ZEUS crash | Athena offline, no Telegram | PID lock + LaunchAgent restart |

---

## Changelog
- 2026-04-13 — Created. Full network topology, agent roster, communication matrix, cron registry, security inventory, resilience assessment. Harry memory sync established via SSH/rsync.
