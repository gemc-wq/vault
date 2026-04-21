# Skill: Infrastructure & Platform
**Weight: 10% | Heartbeat: 1x per cycle | Agents: Jay Mark (builder), Athena (orchestration), Harry/Sentinel (monitoring)**

---

## Why 10%
Infrastructure is the foundation everything else runs on. Agent health, cron reliability, database freshness, and platform stability directly gate every other pillar. If infrastructure breaks, Creative can't produce, Sales can't list, Operations can't ship.

## Scope
- Agent swarm health and configuration
- Cron job management (18 active + monitoring)
- Database health (Supabase, BigQuery, SQLite)
- ZEUS bot reliability and uptime
- OpenClaw gateway management
- Ollama / local LLM health
- Platform builds (ecell.app, procurement portal, fulfillment portal)
- Network infrastructure (Tailscale mesh, iMac connectivity)

## Active Projects
| Project | Status | Priority | Owner |
|---------|--------|----------|-------|
| Procurement Portal | 🟡 Phase 3 UI live, Phase 4 pending | P1 | Athena + Cem |
| Cron Command Centre | 🟡 Scope defined, build pending | P1 | Athena |
| Sentinel monitoring (via Harry) | 🟡 Agreed, not yet configured | P1 | Harry (GPT-5.4) |
| Fulfillment Portal | 🟡 Jay Mark building | P2 | Jay Mark |
| ecell.app | 🟡 Jay Mark building | P2 | Jay Mark |
| Anthropic Agent SDK test | ⏳ Task to be selected | P2 | Athena |
| Zero 2.0 replacement | 🟡 Scoping | P3 | Jay Mark |

## Agent Swarm — Current State (Apr 13)
| Agent | Model | Platform | Status |
|-------|-------|----------|--------|
| Athena | Opus 4.6 | ZEUS (Mac Studio) | ✅ Live |
| Ava | Haiku + Advisor | OpenClaw (Mac Studio) | ✅ Live |
| Hermes | GLM 5.1 | OpenClaw (Mac Studio) | ✅ Live |
| Harry | Kimi K2.5 → GPT-5.4 | OpenClaw (iMac) | 🟡 Model upgrade pending |
| Echo | Sonnet (SDK) | ZEUS subagent | ⏳ Proposed |
| Guardian | Sonnet (SDK) | ZEUS subagent | ⏳ Proposed |
| Iris | Gemma 4 | Ollama | ⏳ Proposed |

## Cron Infrastructure (18 Active)
See: `Vault/02-Projects/sentinel-agent/CRON_WATCHLIST.md` for full list.

| Category | Count | Owner |
|----------|-------|-------|
| Daily crons | 6 | main (migrating to owning agents) |
| Weekly crons | 9 | Hermes (5), main (3), pixel (1) |
| One-time | 1 | main (NFL sell-off May 6) |
| Reset/needs re-enabling | 2 | Weekly Memory Review, Weekly Security Audit |

**Critical cron:** Zero Cron Health Check (3:10 AM) — if this fails, Amazon imports silently stop.

## Key Metrics
- Agent uptime (target: >99% during business hours)
- Cron success rate (target: >95%)
- Data freshness: Supabase <24h, BigQuery <6h
- ZEUS response time (target: <30s for Telegram replies)
- Ollama availability (target: >95%)

## Databases Monitored
| Database | Purpose | Freshness | Alert |
|----------|---------|-----------|-------|
| Supabase (procurement) | Inventory, transfers, POs | <24h | >7 days stale |
| Supabase (catalog) | SKU catalog, designs | <24h | >7 days stale |
| BigQuery (Zero) | Amazon imports, analytics | <6h | >12h stale |
| SQLite (ZEUS) | Session memory | Real-time | — |

## Infrastructure Decisions Log
- **Apr 6**: Harry repurposed from COO/builder to finance-only
- **Apr 10**: ZEUS bot launched with Claude Agent SDK
- **Apr 12**: Agent swarm proposal drafted (8 specialist agents)
- **Apr 13**: Harry agreed as Sentinel (GPT-5.4), Hermes assigned 5 self-improving crons
- **Apr 13**: Skill bucket reminders added to heartbeat (9 AM + 2 PM ET)
