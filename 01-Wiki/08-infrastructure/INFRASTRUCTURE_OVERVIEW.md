# Infrastructure Overview
*Version: 2.0 | Updated: 2026-04-13 | Author: Athena*
*Supersedes V1.0 (Feb 11). Reflects ZEUS launch, agent swarm architecture, role changes.*

---

## Compute Nodes

| Node | Type | Location | OS | Status | Purpose |
|------|------|----------|----|--------|---------|
| **Mac Studio** | Desktop | Windermere, FL | macOS | ✅ Running | ZEUS bot, OpenClaw gateway, Ollama (Gemma 4), primary compute |
| **iMac** | Desktop | Windermere, FL | macOS | ✅ Running | Harry (finance-only), Kimi K2.5 via Tailscale |
| **Cem's MacBook Pro** | Laptop | Mobile | macOS | Available | 96GB — dev node, Claude Code CLI |
| ~~AWS Server (Ubuntu)~~ | ~~Cloud VM~~ | ~~us-east-2~~ | — | ❌ Deprecated | Replaced by Mac Studio local stack |

**Network:** All nodes connected via Tailscale mesh. iMac reachable at 100.91.149.92.

---

## Agent Swarm Architecture

```
                        Cem (Telegram / CLI)
                              |
                         +----+----+
                         | ATHENA  |  Claude Opus 4.6 -- ZEUS bot
                         |  Master |  Email triage, heartbeat, dispatch
                         +----+----+
                              |
         +----------+---------+----------+----------+
         |          |         |          |          |
    +----+---+ +---+----+ +--+---+ +---+----+ +--+---+
    |  AVA   | | HERMES | |HARRY | |  ECHO  | |GUARD.|
    |Strategy| |Analyt. | |Finan.| |Content | |Compli|
    |Haiku+  | |GLM 5.1 | |Kimi  | |Sonnet  | |Sonnet|
    |Advisor | |        | |K2.5  | |SDK     | |SDK   |
    +--------+ +--------+ +------+ +--------+ +------+
    OpenClaw    OpenClaw    iMac    ZEUS sub   ZEUS sub
    Mac Studio  Mac Studio  local   on-demand  on-demand

         +----------+----------+
         |          |          |
    +----+---+ +---+----+ +--+-------+
    |SENTNEL | |  IRIS  | |JAY MARK  |
    |  Ops   | | Intel  | | Builder  |
    |Gemma 4 | |Gemma 4 | | (Human)  |
    |+Haiku  | |  $0    | |   PH     |
    +--------+ +--------+ +---------+
    ZEUS sub   ZEUS sub    Email brief
    + Ollama   + Ollama    from Athena
```

---

## Agent Roster

| Agent | Model | Platform | Pillar | Status | Monthly Cost |
|-------|-------|----------|--------|--------|-------------|
| **Athena** | Claude Opus 4.6 (SDK) | ZEUS bot (always-on) | Orchestration | ✅ Live | Subscription |
| **Ava** | Haiku + Anthropic Advisor | OpenClaw, Mac Studio | Strategy & Product | ✅ Live | ~$15-30 |
| **Hermes** | GLM 5.1 via OpenRouter | OpenClaw, Mac Studio | Sales & Intelligence | ✅ Live | ~$5-15 |
| **Harry** | Kimi K2.5 | OpenClaw, iMac | Finance & Procurement | ✅ Live | ~$0-5 |
| **Echo** | Claude Sonnet (SDK) | ZEUS subagent | Marketing & Brand | ⏳ Proposed | ~$10-20 |
| **Guardian** | Claude Sonnet (SDK) | ZEUS subagent | Compliance & QA | ⏳ Proposed | ~$5-10 |
| **Sentinel** | Gemma 4 + Haiku | ZEUS + Ollama | Operations & Monitoring | ⏳ Proposed | ~$2-5 |
| **Iris** | Gemma 4 | Ollama | Intelligence & Wiki | ⏳ Proposed | $0 |
| **Jay Mark** | Human (PH) | Email brief | Technical Builder | ✅ Active | Salary |
| | | | | **Total agents:** | **~$37-85/mo** |

### Key Role Changes (Apr 2026)

| Agent | Before | After | Reason |
|-------|--------|-------|--------|
| **Harry** | COO/Builder (Opus on AWS) | Finance-only (Kimi K2.5 on iMac) | Builder work deprecated; Jay Mark handles infra. Finance is Harry's strength. |
| **Hermes** | Data analyst (ad-hoc queries) | Autonomous analytics engine (5 self-improving weekly crons) | Needs consistent weekly output, not ad-hoc. GLM 5.1 is cost-effective for batch analytics. |
| **main agent** | Multi-hat generalist | Ava (strategy) + cron host | Specialist model replaces generalist. Crons migrating to owning agents. |

---

## Services

| Service | Host | Port | Status | Purpose |
|---------|------|------|--------|---------|
| **ZEUS Bot** | Mac Studio | — | ✅ Running | Telegram bot + Claude Agent SDK orchestrator |
| **OpenClaw Gateway** | Mac Studio | 18789 | ✅ Running | Agent routing (main, hermes-agent, codex, etc.) |
| **Ollama (Gemma 4)** | Mac Studio | 11434 | ✅ Running | Local LLM for batch tasks ($0/run) |
| **Supabase** | Cloud (supabase.co) | — | ✅ Active | Product catalog, procurement, orders, inventory |
| **BigQuery** | Google Cloud | — | ✅ Active | Zero dataset, analytics warehouse |
| **N8N** | Mac Studio | 5678 | ✅ Running | Workflow automation |
| **Slack Bot** | Cloud | — | ✅ Active | Team notifications, EOD digests |

---

## Databases

| Database | Type | Project/Instance | Purpose | Freshness Req | Status |
|----------|------|-----------------|---------|---------------|--------|
| **Supabase (procurement)** | Postgres | auzjmawughepxbtpwuhe | Procurement system (blank_inventory, transfers, POs) | <24h | ✅ Active |
| **Supabase (product catalog)** | Postgres | nuvspkgplkdqochokhhi | SKU catalog, design metadata | <24h | ✅ Active |
| **BigQuery** | Warehouse | instant-contact-479316-i4 | Zero dataset, Amazon imports, analytics | <6h | ✅ Active |
| **SQLite (ZEUS)** | Local | ~/zeus-agent/data/memory.db | Session archive, L4 memory | Real-time | ✅ Active |
| **SQLite (listings)** | Local | Downloads/listings.db | Hermes listing snapshots | Weekly | ✅ Active |
| ~~AWS Production DB~~ | ~~SQL Server~~ | — | Legacy production orders | — | ❌ Deprecated |

---

## AI Models & Cost Stack

| Use Case | Model | Provider | Cost | Agent |
|----------|-------|----------|------|-------|
| Athena (orchestration) | Claude Opus 4.6 | Anthropic SDK (OAuth) | Subscription | Athena |
| Ava (strategy) | Haiku + Advisor | Anthropic via OpenClaw | ~$0.01/task, Advisor ~$0.10/call | Ava |
| Hermes (analytics) | GLM 5.1 | OpenRouter via OpenClaw | ~$0.005/task | Hermes |
| Harry (finance) | Kimi K2.5 | Moonshot via OpenClaw | ~$0.001/task | Harry |
| Batch/cron tasks | Gemma 4 26B | Ollama (local) | $0 | Sentinel, Iris, Athena fallback |
| New subagents | Claude Sonnet | Anthropic SDK | ~$0.03/task | Echo, Guardian |
| CS Bot | GPT-4o-mini | OpenRouter | ~$0.01/interaction | N8N workflow |
| Voice (TTS) | edge-tts (SoniaNeural) | Free | $0 | ZEUS |
| Voice (STT) | faster-whisper | Local | $0 | ZEUS |
| UI generation | Gemini 3.1 Pro Preview | Google AI | API key | Ad-hoc |

---

## Cron Infrastructure

### Ownership Map (18 Active + 2 Reset)

| Owner | Daily | Weekly | One-Time | Total |
|-------|-------|--------|----------|-------|
| **main (→ migrating)** | 5 | 2 | 1 | 8 |
| **Hermes** | 0 | 5 | 0 | 5 |
| **pixel** | 0 | 1 | 0 | 1 |
| **Sentinel (proposed)** | 4+ | 1 | 0 | 5+ |
| **Iris (proposed)** | 2 | 1 | 0 | 3 |
| **Echo (proposed)** | 2 | 0 | 0 | 2 |
| **Guardian (proposed)** | 1 | 1 | 0 | 2 |

### Critical Crons (Monitored by Sentinel)

| Cron | Time (ET) | Current Owner | Purpose |
|------|-----------|---------------|---------|
| Data Freshness Check | Daily 1:05 AM | main | Supabase orders staleness (>7d = alert) |
| S3 Image Audit | Daily 2:00 AM | main | Shopify design image coverage |
| Zero Cron Health Check | Daily 3:10 AM | main | BigQuery Zero import errors |
| Slack Daily Digest | Daily 4:10 AM | main | PH team EOD aggregation |
| Weekly PULSE Leaderboard | Mon 5:00 AM | Hermes | Top devices, designs, movers |
| Weekly Listings US/UK/DE | Sat 1-3 AM | Hermes | Marketplace listing analysis |
| Mid-Week Shipping Audit | Wed 2:00 AM | pixel | Amazon shipping template check |
| NFL Sell-Off Reminder | May 6 (one-time) | main | License sell-off deadline ~Jun 29 |

See: `Vault/02-Projects/sentinel-agent/CRON_WATCHLIST.md` for full 18-cron list.
See: `Vault/01-Wiki/Infrastructure/ACTIVE_CRONS.md` for detailed cron registry.
See: `Vault/03-Agents/Hermes/CRON_ASSIGNMENTS.md` for Hermes' 5-cron self-improving loop.

---

## ZEUS Bot Architecture

```
     Cem's Phone          Mac Studio
     +----------+         +----------------------------------+
     | Telegram |<------->|  zeus.py                         |
     +----------+         |    +-> telegram_gateway.py       |
                          |         +-> orchestrator.py      |
                          |              | Claude Agent SDK   |
                          |              | (OAuth via CLI)    |
                          |              |                    |
                          |    +---------+----------+        |
                          |    |   MCP Servers       |        |
                          |    |                     |        |
                          |    |  openclaw_mcp.py ---+--> OpenClaw Gateway (:18789)
                          |    |    +-> Any agent    |    +-- main (Ava), hermes-agent
                          |    |    +-> Hermes (ACP) |    +-- harry (iMac via Tailscale)
                          |    |                     |    +-- codex (future adversary)
                          |    |  memory_mcp.py -----+--> Obsidian Vault (READ-ONLY)
                          |    |    +-> Local writes  |    + data/ directory
                          |    |                     |        |
                          |    |  codex_mcp.py ------+--> ChatGPT 5.4 (DISABLED)
                          |    |    (no OpenAI key)  |        |
                          |    +---------------------+        |
                          +----------------------------------+
```

**Key files:** `~/zeus-agent/` — see `~/zeus-agent/CLAUDE.md` for full developer context.

**6 Subagents (defined in orchestrator.py):**

| Name | Model | Role |
|------|-------|------|
| researcher | Sonnet | Web research, document reading |
| coder | Opus | Code writing, debugging, execution |
| analyst | Sonnet | Data analysis, BigQuery, reports |
| delegator | Haiku | Routes to OpenClaw agents + Hermes |
| reviewer | Opus | QA, self-improvement, skill evolution |
| strategist | Sonnet | Strategic heartbeat, project reviews |

---

## Communication Channels

| Channel | Platform | Purpose | Status |
|---------|----------|---------|--------|
| **Telegram** | @zeussbossman_bot | Cem <-> Athena (primary) | ✅ Active |
| **Slack** | Ecell workspace | Team channels (#eod-creative, #eod-listings, #sales-analytics) | ✅ Active |
| **Email** | gemc@ecellglobal.com | Triage by Athena (read-only), drafts need approval | ✅ Active |
| **OpenClaw ACP** | localhost:18789 | Agent-to-agent dispatch | ✅ Active |

---

## Tool Allocation Matrix

Each agent sees ONLY its tools. No shared pool.

| Tool / API | Ava | Hermes | Harry | Echo | Guardian | Sentinel | Iris | Athena |
|------------|-----|--------|-------|------|----------|----------|------|--------|
| **Vault read** | all | sales/intel | finance | content | licenses | ops | all | all |
| **Vault write** | own | own | own | own | own | own | wiki | compiled |
| **BigQuery** | - | ✅ | - | - | - | - | - | read |
| **Supabase** | read | r/w | - | - | read | r/w | - | read |
| **Xero** | - | - | ✅ | - | - | - | - | - |
| **Amazon SP-API** | - | read | - | read | read | - | - | - |
| **Amazon Ads** | - | read | - | r/w | - | - | - | - |
| **Gmail MCP** | - | - | - | - | - | - | - | read |
| **Shopify API** | - | read | - | - | - | - | - | - |
| **Zero API** | - | - | - | - | - | ✅ | - | - |
| **Ollama** | - | - | - | - | - | ✅ | ✅ | ✅ |
| **Web search** | ✅ | ✅ | - | ✅ | - | - | - | ✅ |
| **Agent dispatch** | ✅ | - | - | - | - | - | - | ✅ |
| **Telegram send** | - | - | - | - | - | - | - | ✅ |

---

## API Keys & Credentials

| Service | Location | Status |
|---------|----------|--------|
| Anthropic (SDK OAuth) | Claude CLI auto-manages | ✅ |
| OpenClaw Gateway | .env (OPENCLAW_GATEWAY_TOKEN) | ✅ |
| Supabase (procurement) | .env.local (service role key) | ✅ |
| Supabase (catalog) | gateway config | ✅ |
| Google (Gemini) | .env.local (GEMINI_API_KEY) | ✅ |
| BigQuery | GCloud service account | ✅ |
| Moonshot (Kimi K2.5) | gateway config | ✅ |
| OpenRouter (GLM) | gateway config | ✅ |
| Slack bot | gateway config (xoxb-*) | ✅ |
| Telegram bot | .env (BOT_TOKEN) | ✅ |
| Brave Search | gateway config | ✅ |
| Amazon SP-API | Available (from Feb 8) | ✅ |
| Xero | Harry config (iMac) | ✅ |
| eBay API | TBD | ⏳ Pending |

---

## Rollout Schedule (Agent Swarm)

| Week | Action | Status |
|------|--------|--------|
| Apr 14 | Write SOUL.md + SKILLS for Echo, Guardian | ⏳ Next |
| Apr 14 | Update Hermes SOUL for GLM 5.1 + self-improving loop | ✅ Done |
| Apr 19 | Hermes first autonomous cron run (Sat 1AM) | ⏳ Scheduled |
| Apr 21 | Deploy Echo (PPC monitoring, shadow mode) | ⏳ Planned |
| Apr 21 | Deploy Sentinel (Zero health + inventory) | ⏳ Planned |
| Apr 28 | Deploy Guardian (compliance, shadow mode) | ⏳ Planned |
| Apr 28 | Deploy Iris (wiki maintenance) | ⏳ Planned |
| May 5 | Retire unused OpenClaw aliases (atlas, bolt, pixel, prism, sven2) | ⏳ Planned |
| May 5 | Control Centre MVP at ecell.app/control-centre | ⏳ Planned |

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Agent Swarm Proposal | `00-Company/AGENT_SWARM_PROPOSAL.md` | Full roster, tool matrix, cost model |
| Hermes Cron Assignments | `03-Agents/Hermes/CRON_ASSIGNMENTS.md` | 5-cron self-improving loop spec |
| Sentinel Cron Watchlist | `02-Projects/sentinel-agent/CRON_WATCHLIST.md` | 18 crons to monitor |
| Active Crons Registry | `01-Wiki/Infrastructure/ACTIVE_CRONS.md` | Detailed cron registry (440 lines) |
| Harry SOUL V2 | `03-Agents/Harry/SOUL_V2_CONFIRMED.md` | Finance-only role confirmation |
| Hermes SOUL | `03-Agents/Hermes/SOUL.md` | Intelligence Agent identity |
| ZEUS CLAUDE.md | `~/zeus-agent/CLAUDE.md` | ZEUS developer context |
| Athena SOUL V4 | `~/zeus-agent/workspace/SOUL.md` | Master orchestrator rules |

---

## Changelog
- V2.0 (2026-04-13) — Full rewrite. Added agent swarm architecture, ZEUS bot, role changes (Harry finance-only, Hermes autonomous analytics), cron ownership map, tool allocation matrix, updated compute nodes, databases, and cost stack. Deprecated AWS server.
- V1.0 (2026-02-11) — Initial infrastructure overview (Harry-era, AWS-centric).
