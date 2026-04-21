# Ecell Global Vault — Master Index
*Last compiled: 2026-04-12 | Compiler: Athena*

---

## How This Vault Works

Three-layer knowledge system (Karpathy wiki pattern + Cole Medin compiler):

```
Raw (agent logs)  →  Wiki (curated knowledge)  →  Compiled (auto-generated outputs)
03-Agents/           01-Wiki/                      00-Company/compiled/
```

**Raw**: Agents write daily memory logs. Unfiltered, append-only.  
**Wiki**: Relevance filter promotes knowledge from raw → wiki nightly. Human-curated topic pages.  
**Compiled**: Nightly compile builds indexes, project boards, blockers, and digests from wiki + raw.  

**Update cycle**: Gemma 4 26B runs at 02:00 ET nightly. Claude Sonnet runs monthly deep compile.

---

## 🏢 00-Company — Canonical Docs (5 files)

Company-level truth. Rarely changes. Cem approves updates.

| Document | Description | Last Updated |
|----------|-------------|-------------|
| [STRATEGY.md](00-Company/STRATEGY.md) | 4-Pillar framework (Sales, Production, Operations, Growth) | Mar 7 |
| [OPERATIONAL_BLUEPRINT_V3.md](00-Company/OPERATIONAL_BLUEPRINT_V3.md) | 10-stage pipeline: License → Intelligence | Apr 6 |
| [SKU_PARSING_RULES.md](00-Company/SKU_PARSING_RULES.md) | SKU anatomy and decomposition rules | Mar 20 |
| [VISION_EVOLUTION.md](00-Company/VISION_EVOLUTION.md) | Original vision → Blueprint V3 comparison, specialist agent architecture, human+AI design principle | Apr 12 |
| [PROCESS_MAP_V4.md](00-Company/PROCESS_MAP_V4.md) | Process map v4 | Apr 7 |
| [AGENT_CRON_ARCHITECTURE.md](00-Company/AGENT_CRON_ARCHITECTURE.md) | Agent-cron pattern replacing N8N — polling via MCP connectors, specialist agents on cron | Apr 12 |

### compiled/ — Auto-Generated Outputs
| Document | Description | Updated By |
|----------|-------------|-----------|
| [PROJECT_BOARD.md](00-Company/compiled/PROJECT_BOARD.md) | All active projects, status, owners, blockers | Nightly |
| [BLOCKERS.md](00-Company/compiled/BLOCKERS.md) | Active blockers awaiting action | Nightly |
| [WEEKLY_DIGEST.md](00-Company/compiled/WEEKLY_DIGEST.md) | Week's decisions, deliverables, knowledge gained | Weekly |
| [VAULT_HEALTH.md](00-Company/compiled/VAULT_HEALTH.md) | File counts, stale docs, lint issues | Nightly |
| [CHANGE_LOG.md](00-Company/compiled/CHANGE_LOG.md) | Append-only record of vault changes | Nightly |

---

## 📚 01-Wiki — Curated Knowledge (314 pages)

Single source of truth for business knowledge. Organized by topic.  
Full index: [01-Wiki/INDEX.md](01-Wiki/INDEX.md) | Map of content: [01-Wiki/MOC.md](01-Wiki/MOC.md)

### Key Sections
| # | Section | Pages | Covers |
|---|---------|-------|--------|
| 01 | Customer Service | 4 | CS architecture, marketplace rules, email SOPs |
| 02 | Sales Data | 3 | Schema, 2025 analysis, analytics SOPs |
| 03 | Production | 3 | Daily print workflow, TIFF/EPS pipeline |
| 04 | Shipping | 2 | Carrier rules, label SOPs |
| 05 | Inventory | 1 | Stock tracking, velocity reordering |
| 08 | Infrastructure | 8 | Systems overview, BigQuery, Supabase, AWS |
| 11 | Product Intelligence | 2 | PIE — algorithmic SKU selection |
| 14 | GoHeadCase | 13 | DTC brand, product matrix, Shopify |
| 17 | Harry Workspace | 12 | Finance agent archive, ecell-ops |
| 23 | Drew Handover | 27 | Zero infrastructure, credentials, processes |
| 32 | Fulfillment Portal | 6 | Spec, architecture, Evri CSV MVP |
| 35 | IREN/DRECO | 3 | Print automation, creative→replication SOP |
| 36 | Royalty Reporting | 5 | Legacy system analysis, schema proposal |
| 38 | Athena | 3 | Onboarding briefs, Monday brief |

---

## 🔨 02-Projects — Active Work (261 docs + code)

Project specs, build logs, and code. Each folder = one project.

### P0 — Critical Path (One Piece Launch)
| Project | Folder | Docs | Status |
|---------|--------|------|--------|
| One Piece Launch | [one-piece/](02-Projects/one-piece/) | 7 + 7 images | 🟢 Active — first Blueprint V3 pilot |
| ecell.app | [ecell-app/](02-Projects/ecell-app/) | 8 | 🟡 Jay Mark building |
| ListingForge | [listing-forge/](02-Projects/listing-forge/) | ~20 | 🟡 Gates marketplace expansion |
| Fulfillment Portal | [fulfillment-portal/](02-Projects/fulfillment-portal/) | 7 | 🟡 Jay Mark taking over from Harry |

### P1 — Supporting
| Project | Folder | Docs | Status |
|---------|--------|------|--------|
| SKU Staging | [sku-staging/](02-Projects/sku-staging/) | ~40 | 🟢 Active |
| PULSE Dashboard | [pulse-dashboard-v2/](02-Projects/pulse-dashboard-v2/) | ~10 | 🟡 Needs COGS data |
| Procurement | [procurement/](02-Projects/procurement/) | 3 | 🟡 Harry finance scope |
| Royalty Reporting | [royalty-reporting/](02-Projects/royalty-reporting/) | 3 | 🟡 Harry finance scope |
| Walmart Lister | [walmart-lister/](02-Projects/walmart-lister/) | ~13 | 🟡 Blocked on ListingForge |
| IREN/DRECO | [iren-dreco/](02-Projects/iren-dreco/) | 2 | 🟡 Lane 2 first |

### Archive / Reference
| Project | Folder | Note |
|---------|--------|------|
| Zero Codebase | [zero-codebase/](02-Projects/zero-codebase/) | 36.7K files — legacy PHP reference |
| PPC AutoResearch | [ppc-autoresearch/](02-Projects/ppc-autoresearch/) | 5.6K files — Amazon ads research |

---

## 🤖 03-Agents — Agent Workspaces (197 docs)

Each agent has: identity files, memory logs, and project-specific outputs.

### Ava (CPSO — Mac Studio / OpenClaw)
| Item | Path | Description |
|------|------|-------------|
| Daily logs | [memory/](03-Agents/Ava/memory/) | 39 daily logs (Mar 1 → Apr 7) |
| Archive | [memory-archive/](03-Agents/Ava/memory-archive/) | Older logs |
| Cross-session | memory/cross-session-state.md | Persistent state across compactions |
| Slack digest | memory/slack-digest.md | Slack channel summaries |

### Harry (Finance Agent — iMac)
| Item | Path | Description |
|------|------|-------------|
| Identity | [SOUL.md](03-Agents/Harry/SOUL.md), [AGENTS.md](03-Agents/Harry/AGENTS.md) | Agent config |
| Memory | [MEMORY.md](03-Agents/Harry/MEMORY.md) | 17KB curated long-term memory |
| Daily logs | [daily/](03-Agents/Harry/daily/) | 23 daily logs |
| Projects | [projects/](03-Agents/Harry/projects/) | Finance project specs |
| ecell-ops | [ecell-ops/](03-Agents/Harry/ecell-ops/) | Operational outputs |

### Athena (Orchestrator — Mac Studio / ZEUS)
| Item | Path | Description |
|------|------|-------------|
| Onboarding V2 | [ATHENA_ONBOARDING_BRIEF_V2.md](03-Agents/Athena/ATHENA_ONBOARDING_BRIEF_V2.md) | Current brief |
| Harry Monday Brief | [HARRY_MONDAY_BRIEF.md](03-Agents/Athena/HARRY_MONDAY_BRIEF.md) | Weekly check template |

### Hermes (Sales Analytics — Server)
| Item | Path | Description |
|------|------|-------------|
| Setup | [HERMES_SALES_STRATEGIST_SETUP.md](03-Agents/Hermes/HERMES_SALES_STRATEGIST_SETUP.md) | Deployment config |

---

## Compile Rules

### Nightly (02:00 ET — Gemma 4 26B, $0.00)
1. **Filter**: Scan new raw logs in `03-Agents/*/memory/` → relevance filter → save cleaned versions
2. **Promote**: Extract decisions, process knowledge, corrections → append to relevant `01-Wiki/` pages
3. **Compile**: Rebuild `00-Company/compiled/` outputs (PROJECT_BOARD, BLOCKERS, VAULT_HEALTH)
4. **Lint**: 15-point vault health check (stale docs, broken links, duplicates, oversized files)
5. **Log**: Append to CHANGE_LOG.md

### Weekly (Monday 08:00 ET — Gemma 4)
- Build WEEKLY_DIGEST.md from the week's filtered logs
- Flag stale wiki pages (no updates in 30+ days)

### Monthly (1st of month — Claude Sonnet)
- Deep compile: re-index entire wiki, rebuild MOC.md, audit cross-references
- Reconcile PROJECT_BOARD against actual project folder contents

### What triggers an INDEX.md update
- New folder created in any section
- Compiled output changes materially
- Agent added or removed from 03-Agents/
- Cem or Ava makes structural vault change

---

## Key References
- **North Star**: "#1 licensed tech accessories — any fan, any device, everywhere, fastest"
- **3 Metrics**: Coverage, Speed, Intelligence
- **Blueprint V3**: [OPERATIONAL_BLUEPRINT_V3.md](00-Company/OPERATIONAL_BLUEPRINT_V3.md)
- **Strategy**: [STRATEGY.md](00-Company/STRATEGY.md)
- **Vault SOP**: [01-Wiki/VAULT_ARCHITECTURE.md](01-Wiki/VAULT_ARCHITECTURE.md)


## Auto-promoted Wiki Pages (2026-04-17)
| Page | Description | Date |
|------|-------------|------|
| [master_project_map.md](01-Wiki/14-goheadcase/master_project_map.md) | Auto-promoted from agent logs | 2026-04-17 |
| [microsite_strategy.md](01-Wiki/14-goheadcase/microsite_strategy.md) | Auto-promoted from agent logs | 2026-04-17 |
| [fulfillment_orchestrator.md](01-Wiki/03-production/fulfillment_orchestrator.md) | Auto-promoted from agent logs | 2026-04-17 |


## Auto-promoted Wiki Pages (2026-04-18)
| Page | Description | Date |
|------|-------------|------|
| [pulse-dashboard-architecture.md](01-Wiki/08-infrastructure/pulse-dashboard-architecture.md) | Auto-promoted from agent logs | 2026-04-18 |
| [amazon-reporting-process.md](01-Wiki/11-product-intelligence/amazon-reporting-process.md) | Auto-promoted from agent logs | 2026-04-18 |


## Auto-promoted Wiki Pages (2026-04-19)
| Page | Description | Date |
|------|-------------|------|
| [reporting-architecture.md](01-Wiki/08-infrastructure/reporting-architecture.md) | Auto-promoted from agent logs | 2026-04-19 |
| [listing-snapshot-logic.md](01-Wiki/10-listingforge/listing-snapshot-logic.md) | Auto-promoted from agent logs | 2026-04-19 |
| [openclaw-ops.md](01-Wiki/08-infrastructure/openclaw-ops.md) | Auto-promoted from agent logs | 2026-04-19 |
