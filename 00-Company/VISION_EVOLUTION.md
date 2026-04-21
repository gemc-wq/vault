# Ecell Global — Vision Evolution: Original → Blueprint V3
**Created:** 2026-04-12 | **Author:** Athena | **Approved by:** Cem

---

## Purpose

Track how Ecell's AI/automation vision has evolved from the original "Autonomous Enterprise" proposal (Jan 2026) to the current Operational Blueprint V3 (Apr 2026). This is a living document — updated as architecture decisions change.

---

## Timeline

| Date | Document | Core Idea |
|------|----------|-----------|
| Jan 2026 | AI Model Upgrade Request (Gemini) | 5-agent "Agentic Swarm" — fully autonomous concept-to-cash |
| Jan 2026 | Feasibility Study (LaunchOS) | Hybrid stack validation, 5 agents, 12-week rollout |
| Mar 2026 | Blueprint V2 | First staged process map |
| Apr 2026 | Blueprint V3 | 10-stage operational process, Supabase core, ecell.app frontend |
| Apr 2026 | SOUL V4 (Athena) | Master orchestrator, 6-pillar monitoring, agent-native execution |

---

## Original Vision (Jan 2026) — "The Autonomous Enterprise"

**Architecture:** 5 autonomous agents replacing 7 linear stages
- **Watcher** (Gemini 3) — trend detection, market scanning
- **Creator** (Leonardo.ai + Claude) — asset generation, design production
- **Guardian** (Claude Opus) — compliance, licensor rules enforcement
- **Merchant** (GPT-5.2) — dynamic pricing, listing optimization
- **Reaper** (GPT-5.2) — lifecycle management, SKU retirement

**Projected outcomes:**
- Concept-to-cash: 45 days → 2-3 days
- Cost per launch: $1,145 → $217
- Tech stack: ~$665/month

---

## What Survived (Validated Ideas)

1. **Multi-agent orchestration** — Now 12+ agents via OpenClaw gateway, coordinated by Athena
2. **Trend-to-design pipeline** — Watcher concept lives in market intelligence work (PULSE, Hermes)
3. **Compliance automation** — Guardian concept partially in content stage rules
4. **Dynamic pricing** — Merchant concept in Hermes analytics + FBA pricing analysis
5. **Speed as competitive moat** — Core thesis confirmed: fastest to list wins

## What Was Dropped (And Why)

| Original Concept | Why Dropped |
|-----------------|-------------|
| **AI-generated artwork** (Leonardo.ai) | **Licensed products require human designers.** NFL, Disney, One Piece — you cannot AI-generate licensed IP. Period. |
| **Fully autonomous publishing** | Licensor approval cycles (5-15 days) require human review. "AI recommends, human decides." |
| **2-3 day concept-to-cash** | Unrealistic given license compliance loops. Bottleneck is approvals, not tech. |
| **Single-vendor agent models** | Replaced with best-model-per-task: Claude (reasoning), Gemma 4 (batch), Kimi K2.5 (finance) |

## What Blueprint V3 Added

| Stage | Coverage | Original Had? |
|-------|----------|---------------|
| Inventory Management | FL/PH warehouse ops, stocking decisions | ❌ Zero coverage |
| Order Fulfillment | Zero 2.0, pick/pack/ship, fulfillment portal | ❌ Zero coverage |
| Finance | Xero, royalties, COGS tracking | ❌ Assumed revenue without cost |
| ListingForge | Bulk listing pipeline (biggest current blocker) | ❌ Assumed listings "just happen" |
| Print File Monitoring | Digital → physical handoff | ❌ Manufacturing was a black box |

---

## CRITICAL PRINCIPLE: Human Designers + AI Tools

> **AI assists human designers. AI does not replace human designers.**

This is non-negotiable for licensed products:

1. **Licensor contracts require human creative oversight.** AI-generated assets violate most license agreements.
2. **Brand quality demands human judgment.** HB401 converts 4x vs HTPCR because human designers understand brand intent.
3. **AI's role in creative:** Reference gathering, mockup generation, layout suggestions, batch resizing, background removal, style transfer previews — all as inputs TO the designer, not as final output.
4. **PH design team (38 staff)** uses AI tools to work faster, not to be replaced. Sven (AI creative director) generates briefs and direction — humans execute.

The competitive advantage is **human creativity accelerated by AI tooling**, not autonomous generation.

---

## Architecture Evolution: N8N → Agent-Native

### Current State (Mixed)
- Some workflows in N8N (webhook triggers, sequential steps)
- Some in Claude Agent SDK (Athena orchestration)
- Some in cron scripts (Gemma 4 batch tasks)

### Target State (Agent-Native)
All execution through AI agents, triggered two ways:

**1. Event-Triggered (On-Demand)**
- Telegram messages → Athena → dispatch to appropriate agent
- Email inbound → agent triage and response
- Slack triggers → agent action
- Webhook events → agent processing (new order, listing change, inventory alert)

**2. Cron-Scheduled (Automated)**
- Each agent owns its scheduled tasks
- Each cron tied to a specific agent + skill/function
- All visible in Control Centre

**Why move off N8N:**
- N8N is a workflow tool — it chains API calls. Agents reason about what to do.
- N8N fails silently on edge cases. Agents can self-heal or escalate.
- N8N requires manual workflow building for each new process. Agents learn skills.
- N8N is another system to maintain. Agent-native keeps everything in one orchestration layer.

**Migration approach:** Don't rip out N8N overnight. For each N8N workflow:
1. Identify what it does
2. Build equivalent agent skill
3. Run both in parallel for 1 week
4. Cut over when agent matches or exceeds N8N reliability

---

## Control Centre Requirements

A single dashboard showing:

### Agent Status Panel
| Agent | Status | Active Task | Last Heartbeat | Model | Cost (24h) |
|-------|--------|-------------|----------------|-------|------------|

### Cron Registry
| Cron | Agent | Skill/Function | Schedule | Last Run | Status | Next Run |
|------|-------|----------------|----------|----------|--------|----------|

### Active Tasks
| Task ID | Agent | Description | Priority | Started | ETA | Status |
|---------|-------|-------------|----------|---------|-----|--------|

### Event Log (Last 24h)
| Time | Trigger | Agent | Action | Result |
|------|---------|-------|--------|--------|

**Implementation path:** ecell.app/control-centre — Supabase backend, agents write status to `agent_heartbeats`, `agent_tasks`, `agent_crons` tables.

---

## Specialist Agent Architecture (Apr 12 — Cem Directive)

### The Problem with Multi-Tasking Agents
OpenClaw runs as one system context-switching between 10 "agents" (main, atlas, bolt, pixel, prism, sven, sven2, iris, codex, hermes). These are aliases, not specialists. Same context window, same credentials, same generalist treatment of every domain. **Accuracy degrades when one agent juggles finance, creative, operations, and analytics.**

### The Claude Integrations Model
Each agent should be:
- **Single-purpose** — one job, one system prompt, one set of tools
- **Credentialed** — its own API keys, its own data access scope
- **Persistent** — maintains its own conversation history and memory
- **Bounded** — cannot drift into another agent's domain

### Target Specialist Roster

| Agent | Pillar (Weight) | Model | Own Credentials | Key Skills |
|-------|-----------------|-------|-----------------|------------|
| **Sven** | Creative & Design (30%) | Gemini 3.1 Pro | Figma, GDrive, Adobe | Design briefs, compliance review, mockup generation |
| **Hermes** | Sales & Marketplace (25%) | Gemma 4 / Sonnet | BigQuery, SP-API, Seller Central | PULSE, pricing, listing analytics, FBA conversion |
| **Zero** | Operations & Fulfillment (20%) | Gemma 4 | Supabase, fulfillment portal | Order routing, inventory, shipping, warehouse ops |
| **Echo** | Marketing & Brand (10%) | Sonnet | Amazon Ads API, email platform | PPC, ACOS, campaigns, email marketing |
| **Harry** | Finance & Procurement (10%) | Kimi K2.5 | Xero, royalty DB | COGS, royalties, PO generation, margin tracking |
| **Iris** | Intelligence & Analytics (5%) | Gemma 4 | BigQuery, vault | Wiki maintenance, data freshness, pattern detection |
| **Athena** | Orchestrator | Claude Opus | All (read), Telegram | Dispatch, heartbeat, escalation, Cem interface |

**Athena does not do the work.** Athena reads results, routes tasks, detects conflicts, and talks to Cem.

### Credential Isolation (Each Agent Sees Only What It Needs)

| Agent | Has Access To | Does NOT Access |
|-------|--------------|-----------------|
| Sven | Figma, GDrive designs, Adobe | Financial data, pricing, inventory |
| Hermes | BigQuery, SP-API (read), listings DB | Design files, Xero, fulfillment |
| Harry | Xero, royalty tables, COGS data | Listings, creative pipeline |
| Zero | Supabase fulfillment tables, shipping APIs | Revenue data, design files |
| Echo | Amazon Ads API, email platform, campaign data | Finance, fulfillment, design |
| Iris | BigQuery (read), vault (read/write) | All operational APIs |

### Deployment Strategy (Hybrid)

| Tier | Agents | Platform | Why |
|------|--------|----------|-----|
| **Managed** | Sven, Echo, Harry | Claude Integrations | Need reasoning quality + own API creds |
| **Local** | Hermes, Zero, Iris | Gemma 4 via Ollama ($0) | Batch/data work, cost-sensitive |
| **Orchestrator** | Athena | ZEUS (Claude SDK + Telegram) | Full control, Cem interface |

### Migration Path

| Phase | Action | When |
|-------|--------|------|
| 1. Define | Write SOUL.md per specialist. Map skills, creds, boundaries. | Week of Apr 14 |
| 2. Pilot | Hermes as first true specialist (sales only, own creds, own memory) | Week of Apr 21 |
| 3. Split | Sven (creative) and Harry (finance) to own instances | Week of Apr 28 |
| 4. Retire | Decommission OpenClaw multi-hat aliases | When all specialists proven |
| 5. Control Centre | ecell.app/control-centre live with all agents reporting | Parallel with Phase 2-4 |

---

## CRITICAL PRINCIPLE: Human Designers + AI Tools

> **AI assists human designers. AI does not replace human designers.**

This is non-negotiable for licensed products:

1. **Licensor contracts require human creative oversight.** AI-generated assets violate most license agreements.
2. **Brand quality demands human judgment.** HB401 converts 4x vs HTPCR because human designers understand brand intent.
3. **AI's role in creative:** Reference gathering, mockup generation, layout suggestions, batch resizing, background removal, style transfer previews — all as inputs TO the designer, not as final output.
4. **PH design team (38 staff)** uses AI tools to work faster, not to be replaced. Sven (AI creative director) generates briefs and direction — humans execute.

The competitive advantage is **human creativity accelerated by AI tooling**, not autonomous generation.

---

## DelegAIt Product Angle

This entire evolution — from ambitious autonomous vision to grounded staged architecture — is the journey every SMB will take with AI. The playbook:

1. "Here's what you think AI will do" (autonomous everything)
2. "Here's what it actually does" (assists humans, handles batch/routine)
3. "Here's the realistic architecture" (staged process, agent-assisted, human-approved)

This is a consultancy product. Package the lessons learned.

---

## Changelog
- 2026-04-12 — Created. Comparison of original vision vs Blueprint V3. Added human designer principle, agent-native architecture direction, Control Centre requirements.
- 2026-04-12 — Added Specialist Agent Architecture section (Cem directive: move from multi-tasking generalist to single-purpose specialists). Added credential isolation, hybrid deployment strategy, migration path.
