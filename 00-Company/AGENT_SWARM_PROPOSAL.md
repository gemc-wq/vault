# Ecell Global — Specialist Agent Swarm Proposal
**Created:** 2026-04-12 | **Author:** Athena | **Status:** DRAFT — awaiting Cem approval
**Supersedes:** OpenClaw multi-hat aliases

---

## Design Principles

1. **One agent, one job.** No multi-tasking generalists. Each agent owns a pillar.
2. **Right model for the task.** Don't pay Opus prices for data crunching. Don't use Haiku for strategy.
3. **Each agent owns its tools.** No shared tool pool. Tools are scoped to the agent's domain.
4. **Each agent owns its memory.** Vault folder per agent. Daily logs. Cross-session state.
5. **Athena dispatches, doesn't do.** The orchestrator routes tasks and monitors health — never does domain work.

---

## The Roster

### RETAIN AS-IS (Already Proven)

#### Ava — Chief Product & Strategy Officer
| Attribute | Value |
|-----------|-------|
| **Model** | Haiku + Anthropic Advisor tool (escalates to Opus/Sonnet for strategic calls) |
| **Platform** | OpenClaw on Mac Studio |
| **Pillar** | Strategy & Product (cross-pillar) |
| **Memory** | 39+ daily logs, MEMORY_BUSINESS_CONTEXT.md, cross-session-state.md — **retain all** |
| **Status** | ✅ Running. Valuable memory. Do not rebuild. |

**Skills:**
- Project prioritisation and roadmap ownership
- Blueprint V3 process stewardship
- Design brief creation and approval workflow
- Cross-pillar conflict resolution
- Cem's strategic right hand

**Tools:**
- Vault read/write (full access)
- Anthropic Advisor (Opus reasoning on demand)
- Slack digest reader
- OpenClaw agent dispatch (can assign work to other agents)

**Crons:**
- None — Ava is on-demand, triggered by Athena dispatch or Cem direct

---

#### Hermes — Data Analyst & Builder
| Attribute | Value |
|-----------|-------|
| **Model** | GLM via OpenRouter |
| **Platform** | OpenClaw on Mac Studio |
| **Pillar** | Sales & Intelligence (25% + 5%) |
| **Memory** | HERMES_SALES_STRATEGIST_SETUP.md, SKILL.md, dashboard outputs |
| **Status** | ✅ Running. Model recently switched to GLM. |

**Skills:**
- BigQuery analysis and dashboard generation
- Amazon Business Report processing (weekly)
- PULSE leaderboard generation
- Listing intelligence audits (weekly)
- FBA conversion analysis
- Sales trend detection and reporting
- Dashboard building (HTML reports)

**Tools:**
- BigQuery API (direct)
- Supabase API (read/write)
- Shopify Admin API (read)
- Local file access (downloads, CSVs, listings.db)
- Python execution (data processing, pandas)
- Vault read/write (03-Agents/Hermes/)

**Crons:**
| Cron | Schedule | Purpose |
|------|----------|---------|
| PULSE Leaderboard | Mon 5AM ET | Weekly sales leaderboard + alerts |
| Listings US/UK/DE | Sat 1-3AM ET | Marketplace listing analysis |
| Data Freshness | Daily 1AM ET | Verify BQ/Supabase pipelines current |

---

#### Harry — Finance Specialist
| Attribute | Value |
|-----------|-------|
| **Model** | Kimi K2.5 |
| **Platform** | OpenClaw on iMac (Tailscale: 100.91.149.92) |
| **Pillar** | Finance & Procurement (10%) |
| **Memory** | MEMORY.md (17KB curated), 23 daily logs, project specs |
| **Status** | ✅ Running on iMac. Finance only — builder role deprecated. |

**Skills:**
- Xero reconciliation and reporting
- Royalty calculation and tracking
- COGS analysis and margin monitoring
- Purchase order generation
- Supplier payment tracking
- Invoice processing

**Tools:**
- Xero API
- Vault read/write (03-Agents/Harry/)
- Local file access (iMac)
- Python/SQL execution

**Crons:**
| Cron | Schedule | Purpose |
|------|----------|---------|
| Margin Check | Daily 2AM ET | Flag margin drops >3pp any channel |
| Royalty Tracker | Weekly Mon | Track upcoming royalty payments due <7 days |

**Does NOT own:** Infrastructure, N8N, Supabase schema, fulfillment portal builds → that's now Jay Mark (human) or Claude SDK agents.

---

### NEW AGENTS (Claude SDK via ZEUS)

These run as Claude Agent SDK subagents, dispatched by Athena. Each has its own SOUL.md, tools, and memory space. Cost: per-invocation (no always-on process).

#### Echo — Content & Marketing
| Attribute | Value |
|-----------|-------|
| **Model** | Claude Sonnet (via SDK) |
| **Platform** | ZEUS subagent |
| **Pillar** | Marketing & Brand (10%) |
| **Why new:** | No agent currently owns marketing. Ava does it ad-hoc. Needs a specialist for PPC, content, and email marketing. |

**Skills:**
- Amazon PPC campaign analysis (ACOS monitoring, bid optimization)
- SEO content generation from SKU templates (the "SKU = Content" model)
- A+ Content and listing copy optimization
- Email marketing campaigns (when platform connected)
- Competitor listing analysis

**Tools:**
- Amazon Ads API (read — when connected)
- Vault read (01-Wiki/09-creative-pipeline/, 02-Projects/listing-forge/)
- SKU template engine (the content block system)
- Web search (competitor research)

**Crons:**
| Cron | Schedule | Purpose |
|------|----------|---------|
| PPC Health | Daily 6AM ET | Flag campaigns with ACOS >35% and spend >$500 |
| Content Queue | Daily 7AM ET | Check for SKUs needing content, generate from templates |

**SOUL.md key rules:**
- Never publish content without approval gate
- Licensed content must follow licensor guidelines (load from Vault)
- A+ Content follows the HB401 quality bar (4x conversion benchmark)

---

#### Guardian — Compliance & QA
| Attribute | Value |
|-----------|-------|
| **Model** | Claude Sonnet (via SDK) |
| **Platform** | ZEUS subagent |
| **Pillar** | Cross-pillar (compliance layer) |
| **Why new:** | Licensor compliance is currently manual. Guardian catches violations before they reach marketplace. |

**Skills:**
- License agreement rule enforcement (territory, product type, expiry)
- Image compliance checking (logo placement, trademark rules)
- Listing content compliance (no prohibited claims, correct attribution)
- Marketplace policy compliance (Amazon, Walmart, TikTok)
- Expiry date monitoring and renewal alerts

**Tools:**
- Vault read (01-Wiki/ for license rules, 02-Projects/listing-forge/)
- Supabase read (licenses table — when built)
- Image analysis (multimodal — check design files against rules)

**Crons:**
| Cron | Schedule | Purpose |
|------|----------|---------|
| License Expiry | Weekly Mon 3AM | Flag licenses expiring <30 days |
| Listing Compliance | Daily 4AM ET | Spot-check 50 random active listings |

**SOUL.md key rules:**
- NEVER approve content autonomously — flag issues, recommend fixes, human decides
- Red Zone: any licensor communication must go through Cem
- Maintain compliance rulebook per license in Vault

---

#### Sentinel — Operations & Monitoring
| Attribute | Value |
|-----------|-------|
| **Model** | Gemma 4 (local, $0) for routine checks; Claude Haiku for escalation reasoning |
| **Platform** | ZEUS subagent + local Ollama |
| **Pillar** | Operations & Fulfillment (20%) |
| **Why new:** | Zero system monitoring, inventory, and fulfillment are currently unowned by any agent. |

**Skills:**
- Zero system health monitoring
- Inventory level tracking (FL, PH, UK warehouses)
- Order routing verification (right warehouse, right carrier)
- Shipping template audits
- Fulfillment SLA monitoring

**Tools:**
- Zero API (health checks)
- Supabase read/write (fulfillment tables — when built)
- Vault read (01-Wiki/04-shipping/, 01-Wiki/05-inventory/)
- Email monitoring (Zero system emails — fed by email triage engine)

**Crons:**
| Cron | Schedule | Purpose |
|------|----------|---------|
| Zero Health | Every 30 min | Ping Zero portal, flag if down |
| Inventory Alert | Every 4 hours | Check critical stock levels |
| Shipping Audit | Wed 2AM ET | Verify shipping templates correct |
| Order SLA | Every 2 hours | Flag orders approaching SLA breach |

**SOUL.md key rules:**
- Gemma 4 handles all routine checks ($0)
- Only escalate to Claude when anomaly detected (saves cost)
- Alert Athena if any system down >2 consecutive checks

---

#### Iris — Intelligence & Wiki Maintenance
| Attribute | Value |
|-----------|-------|
| **Model** | Gemma 4 (local, $0) |
| **Platform** | ZEUS background task + Ollama |
| **Pillar** | Intelligence & Analytics (5%) + Vault maintenance |
| **Why new:** | The Vault wiki layer stopped compounding (frozen since Mar 20). Iris owns wiki health. |

**Skills:**
- Vault wiki maintenance (the LLM Wiki pattern)
- Knowledge promotion: raw agent logs → wiki pages
- Index and MOC rebuilding
- Contradiction detection and staleness flagging
- Daily digest compilation
- Slack channel monitoring and summarisation

**Tools:**
- Vault read/write (01-Wiki/, INDEX.md, MOC.md)
- Local file access (agent daily logs)
- Ollama (Gemma 4 for batch processing)

**Crons:**
| Cron | Schedule | Purpose |
|------|----------|---------|
| Vault Compile | Daily 2AM ET | Nightly compile: filter logs → promote to wiki → rebuild indexes |
| Wiki Lint | Weekly Sat 1AM | Health check: stale pages, orphans, contradictions |
| Slack Digest | Every 30 min | Parse Slack → compile for daily digest |
| Memory Consolidation | Daily 11PM ET | Consolidate all agent daily logs |

---

### Athena — Master Orchestrator (UNCHANGED)
| Attribute | Value |
|-----------|-------|
| **Model** | Claude Opus (via SDK) |
| **Platform** | ZEUS bot (always-on, LaunchAgent) |
| **Pillar** | Orchestration (all pillars) |
| **Status** | ✅ Running |

**Does:**
- Dispatches tasks to specialist agents
- Monitors 6-pillar heartbeat
- Runs email triage (10-min cron)
- Morning briefing to Cem
- Escalation management
- Cem's direct interface (Telegram + CLI)

**Does NOT do:**
- Data analysis (→ Hermes)
- Content creation (→ Echo)
- Finance (→ Harry)
- Infrastructure building (→ Jay Mark human)
- Strategy decisions (→ Ava)

---

## Architecture Diagram

```
                        Cem (Telegram / CLI)
                              │
                         ┌────┴────┐
                         │ ATHENA  │  Claude Opus — ZEUS bot
                         │Orchestr.│  Email triage, heartbeat, dispatch
                         └────┬────┘
                              │
         ┌──────────┬─────────┼──────────┬──────────┐
         │          │         │          │          │
    ┌────┴───┐ ┌───┴────┐ ┌──┴───┐ ┌───┴────┐ ┌──┴───┐
    │  AVA   │ │ HERMES │ │HARRY │ │  ECHO  │ │GUARD.│
    │Strategy│ │  Data  │ │Finan.│ │Content │ │Compli│
    │Haiku+  │ │GLM/OR  │ │Kimi  │ │Sonnet  │ │Sonnet│
    │Advisor │ │        │ │K2.5  │ │SDK     │ │SDK   │
    └────────┘ └────────┘ └──────┘ └────────┘ └──────┘
    OpenClaw    OpenClaw    iMac    ZEUS sub   ZEUS sub
    Mac Studio  Mac Studio  local   on-demand  on-demand

         ┌──────────┬──────────┐
         │          │          │
    ┌────┴───┐ ┌───┴────┐ ┌──┴──────┐
    │SENTNEL │ │  IRIS  │ │JAY MARK │
    │  Ops   │ │ Intel  │ │ Builder │
    │Gemma 4 │ │Gemma 4 │ │ (Human) │
    │+Haiku  │ │  $0    │ │   PH    │
    └────────┘ └────────┘ └─────────┘
    ZEUS sub   ZEUS sub    Email brief
    + Ollama   + Ollama    from Athena
```

---

## Tool Allocation Matrix

Each agent sees ONLY its tools. No shared pool.

| Tool / API | Ava | Hermes | Harry | Echo | Guardian | Sentinel | Iris | Athena |
|------------|-----|--------|-------|------|----------|----------|------|--------|
| **Vault read** | ✅ all | ✅ sales/intel | ✅ finance | ✅ content | ✅ licenses | ✅ ops | ✅ all | ✅ all |
| **Vault write** | ✅ own folder | ✅ own folder | ✅ own folder | ✅ own folder | ✅ own folder | ✅ own folder | ✅ wiki layer | ✅ compiled |
| **BigQuery** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ read |
| **Supabase** | ✅ read | ✅ r/w | ❌ | ❌ | ✅ read | ✅ r/w | ❌ | ❌ read |
| **Xero** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Amazon SP-API** | ❌ | ✅ read | ❌ | ✅ read | ✅ read | ❌ | ❌ | ❌ |
| **Amazon Ads API** | ❌ | ✅ read | ❌ | ✅ r/w | ❌ | ❌ | ❌ | ❌ |
| **Gmail MCP** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ read |
| **Figma MCP** | ❌ | ❌ | ❌ | ❌ | ✅ read | ❌ | ❌ | ❌ |
| **Shopify API** | ❌ | ✅ read | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Zero API** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Ollama (Gemma 4)** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Web search** | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Agent dispatch** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Telegram send** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Cost Model

| Agent | Model | Hosting | Est. Monthly Cost |
|-------|-------|---------|-------------------|
| **Ava** | Haiku + Advisor | OpenClaw (existing) | ~$15-30 (Haiku cheap, Advisor calls ~$0.10 each) |
| **Hermes** | GLM via OpenRouter | OpenClaw (existing) | ~$5-15 (GLM is cheap) |
| **Harry** | Kimi K2.5 | iMac (existing) | ~$0-5 (near-zero) |
| **Echo** | Sonnet (SDK) | ZEUS on-demand | ~$10-20 (invoked daily for PPC + content) |
| **Guardian** | Sonnet (SDK) | ZEUS on-demand | ~$5-10 (invoked daily for compliance checks) |
| **Sentinel** | Gemma 4 + Haiku | ZEUS + Ollama | ~$2-5 (Gemma $0, Haiku for escalations only) |
| **Iris** | Gemma 4 | Ollama | $0 (all local) |
| **Athena** | Opus (SDK) | ZEUS always-on | Subscription (existing) |
| | | | **Total: ~$37-85/month** |

vs. original vision's $665/month estimate. 90% cheaper because of Gemma 4 local + right-sizing models.

---

## Implementation — How to Make Sure Each Agent Has Correct Skills & Tools

### Step 1: SOUL.md Per Agent (Week of Apr 14)
Each agent gets:

```
/Vault/03-Agents/{AgentName}/
├── SOUL.md          ← Identity, rules, boundaries (what it does AND doesn't do)
├── TOOLS.md         ← Exact tools available, with credentials scope
├── SKILLS/          ← Skill files (one .md per skill)
│   ├── skill-1.md
│   └── skill-2.md
├── MEMORY.md        ← Curated long-term memory
├── memory/          ← Daily logs
└── crons/           ← Cron definitions
    └── cron-1.md
```

### Step 2: Tool Binding via ZEUS Orchestrator
For Claude SDK agents (Echo, Guardian, Sentinel), tools are bound at invocation:

```python
# In orchestrator.py — agent definitions
agents = {
    "echo": AgentDefinition(
        description="Content & Marketing specialist",
        prompt=load_soul("Echo"),  # Loads SOUL.md + SKILLS/
        model="claude-sonnet-4-5",
        tools=["mcp__amazon_ads__*", "vault_read_file", "vault_search"],
    ),
    "guardian": AgentDefinition(
        description="Compliance & QA specialist", 
        prompt=load_soul("Guardian"),
        model="claude-sonnet-4-5",
        tools=["vault_read_file", "vault_search", "mcp__figma__get_design_context"],
    ),
    "sentinel": AgentDefinition(
        description="Operations & Monitoring specialist",
        prompt=load_soul("Sentinel"),
        model="claude-haiku-4-5",
        tools=["vault_read_file", "mcp__supabase__*"],
    ),
}
```

The `tools` list **enforces boundaries** — an agent literally cannot call tools not in its list.

### Step 3: Skill Verification Protocol
Before an agent goes live:

1. **Write SOUL.md** — identity, rules, boundaries
2. **Define skills** — one .md file per skill with trigger, steps, success criteria
3. **Bind tools** — explicit list in orchestrator config
4. **Dry run** — invoke agent with 5 test tasks, verify it stays in lane
5. **Shadow mode** — run alongside current process for 1 week, compare outputs
6. **Go live** — cut over, register in Control Centre

### Step 4: Guardrail Enforcement

| Guardrail | How Enforced |
|-----------|-------------|
| Agent can't use wrong tools | `tools=` list in AgentDefinition — hard boundary |
| Agent can't access wrong data | MCP servers scoped per agent — only exposed APIs are available |
| Agent can't send external comms | No Telegram/email send tools given to domain agents — only Athena |
| Agent can't approve its own work | Approval gates in skill definitions — outputs go to Athena or Cem |
| Agent drift detection | Weekly review: did the agent invoke tools outside its skill set? Log analysis. |

---

## Rollout Schedule

| Week | Action | Agents Affected |
|------|--------|----------------|
| **Apr 14** | Write SOUL.md + SKILLS for Echo and Guardian | New agents |
| **Apr 14** | Update Hermes SOUL.md for GLM model change | Hermes |
| **Apr 21** | Deploy Echo as ZEUS subagent. Shadow mode for PPC monitoring. | Echo |
| **Apr 21** | Deploy Sentinel for Zero health + inventory monitoring | Sentinel |
| **Apr 28** | Deploy Guardian for compliance checks. Shadow mode. | Guardian |
| **Apr 28** | Deploy Iris for wiki maintenance. Fix the frozen wiki. | Iris |
| **May 5** | Cut over: retire OpenClaw multi-hat aliases (bolt, atlas, pixel, prism, sven2) | OpenClaw cleanup |
| **May 5** | Control Centre MVP live at ecell.app/control-centre | All agents |

**Ava, Hermes, Harry: no changes.** They keep running as-is. We build around them.

---

## OpenClaw Cleanup

After specialist agents are proven, retire unused aliases:

| Current Alias | Disposition |
|---------------|-------------|
| main | → Ava (already is) |
| sven | → Keep for Sven creative sub-agent under Ava |
| atlas | → Retire (replaced by Hermes for data) |
| bolt | → Retire (replaced by Jay Mark human + Claude SDK) |
| pixel | → Retire (no dedicated use case) |
| prism | → Retire (no dedicated use case) |
| sven2 | → Retire (duplicate) |
| iris | → Redirect to new Iris agent (ZEUS subagent) |
| codex | → Future: Codex adversary when OpenAI key provided |

---

## Changelog
- 2026-04-12 — Created. Full specialist agent roster, tool allocation matrix, cost model, implementation plan, rollout schedule.
