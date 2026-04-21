# Ecell Global Operations Wiki — Master Index
*Created: 2026-03-07 | Updated: 2026-03-20 | 270+ documents | Source: Clawdbot Shared Folder + Brain + Harry iMac Transfer + Ava Archive*

---

## How to Use This Wiki
- **Single source of truth** for all operational knowledge
- **Semantic search layer** planned (Airweave/pgvector over these .md files)
- **Cross-references** noted where older docs inform newer projects
- Documents prefixed with section numbers for navigation
- Sections 17-22 added 2026-03-08: Harry's full workspace, competitor research, collaboration docs, ecell website project, Ava archive, presentations

---

## 01 — Customer Service (4 files)
| Document | Description | Status |
|----------|-------------|--------|
| [CS_ARCHITECTURE.md](01-customer-service/CS_ARCHITECTURE.md) | CS automation architecture — website-only scope (Feb 11) | ✅ Current |
| [CS_ARCHITECTURE_V2.md](01-customer-service/CS_ARCHITECTURE_V2.md) | Full N8N + Chatwoot + Vapi architecture (multi-channel) | ✅ Reference |
| [MARKETPLACE_RULES.md](01-customer-service/MARKETPLACE_RULES.md) | Amazon/eBay communication compliance rules | ✅ Critical |
| [SOP_EMAIL_HANDLING.md](01-customer-service/SOP_EMAIL_HANDLING.md) | Email handling SOP (draft) | ⚠️ Draft |

**Cross-refs:** → `15-email-triage/` (N8N email triage workflow supersedes parts of this)

---

## 02 — Sales Data & Analytics (3 files)
| Document | Description | Status |
|----------|-------------|--------|
| [SCHEMA_DESIGN.md](02-sales-data/SCHEMA_DESIGN.md) | Unified sales schema (multi-marketplace, SKU decomposition) | ✅ Core |
| [SALES_ANALYSIS_2025.md](02-sales-data/SALES_ANALYSIS_2025.md) | 268K orders, $5.5-6M, geo brand rankings | ✅ Baseline |
| [SOP_SALES_ANALYTICS.md](02-sales-data/SOP_SALES_ANALYTICS.md) | Lookback strategy, regional analysis, data quality | ✅ Current |

**Cross-refs:** → `11-product-intelligence/PROJECT_BRIEF.md` (PIE uses this data), → `14-goheadcase/` (sales summaries)

---

## 03 — Production Workflow (3 files)
| Document | Description | Status |
|----------|-------------|--------|
| [DAILY_PRINT_PRODUCTION.md](03-production/DAILY_PRINT_PRODUCTION.md) | Full daily production workflow deep-dive | ✅ Detailed |
| [PRINT_FILE_PIPELINE.md](03-production/PRINT_FILE_PIPELINE.md) | TIFF + EPS pipelines, automation target (#1) | ✅ Key |
| [SOP_DAILY_PRINT_PRODUCTION.md](03-production/SOP_DAILY_PRINT_PRODUCTION.md) | Production SOP (draft) | ⚠️ Draft |

---

## 04 — Shipping & Fulfillment (2 files)
| Document | Description | Status |
|----------|-------------|--------|
| [SHIPPING_CARRIER_RULES.md](04-shipping/SHIPPING_CARRIER_RULES.md) | UK/US/PH carrier matrix, 3-layer routing logic | ✅ Detailed |
| [SOP_SHIPPING_LABELS.md](04-shipping/SOP_SHIPPING_LABELS.md) | Label processing SOP | ⚠️ Draft |

---

## 05 — Inventory Management (1 file)
| Document | Description | Status |
|----------|-------------|--------|
| [SOP_INVENTORY_TRACKING.md](05-inventory/SOP_INVENTORY_TRACKING.md) | Blank stock tracking, velocity-based reordering | ⚠️ Draft |

---

## 06 — Design Automation (2 files)
| Document | Description | Status |
|----------|-------------|--------|
| [SOP_DESIGN_FILE_MANAGEMENT.md](06-design-automation/SOP_DESIGN_FILE_MANAGEMENT.md) | PSD/EPS/TIFF management, SKU-to-design mapping | ⚠️ Draft |
| [DESIGN_SYSTEM.md](06-design-automation/DESIGN_SYSTEM.md) | Brand design system guidelines | ✅ Reference |

---

## 07 — Chatbot & RAG (1 file)
| Document | Description | Status |
|----------|-------------|--------|
| [VERTEX_AI_RAG_PLAN.md](07-chatbot-rag/VERTEX_AI_RAG_PLAN.md) | Vertex AI chatbot + packing verification, ~$100/mo | ✅ Spec |

---

## 08 — Infrastructure (8 files)
| Document | Description | Status |
|----------|-------------|--------|
| [INFRASTRUCTURE_OVERVIEW.md](08-infrastructure/INFRASTRUCTURE_OVERVIEW.md) | Compute nodes, services, databases, API keys | ⚠️ Outdated (Feb 11) |
| [MASTER_PROJECT_STATUS_FEB11.md](08-infrastructure/MASTER_PROJECT_STATUS_FEB11.md) | Harry's last project status (Feb 11) | 📁 Archive |
| [HARRY_PROJECT_BOARD.md](08-infrastructure/HARRY_PROJECT_BOARD.md) | Harry's full project board (Jan 30) | 📁 Archive |
| [HARRY_CONTEXT_SUMMARY.md](08-infrastructure/HARRY_CONTEXT_SUMMARY.md) | Ava's summary of Harry's work | ✅ Current |
| [HARRY_MEMORY_BACKUP.md](08-infrastructure/HARRY_MEMORY_BACKUP.md) | Harry's full memory from VPS | 📁 Archive |
| [IT_HANDOVER_QUESTIONNAIRE.md](08-infrastructure/IT_HANDOVER_QUESTIONNAIRE.md) | IT infra questionnaire for PH team | ✅ Reference |
| [BRAIN_INDEX.md](08-infrastructure/BRAIN_INDEX.md) | Brain folder index | ✅ Reference |
| [AGENT_MEMORY_SOP.md](08-infrastructure/AGENT_MEMORY_SOP.md) | Agent memory management SOP | ✅ Reference |

---

## 09 — Creative Pipeline (2 files)
| Document | Description | Status |
|----------|-------------|--------|
| [AI_COO_BLUEPRINT.md](09-creative-pipeline/AI_COO_BLUEPRINT.md) | Master business process (Ideation → QA → Go Live → Marketing) | ✅ Core |
| [CREATIVE_PIPELINE_ARCHITECTURE.md](09-creative-pipeline/CREATIVE_PIPELINE_ARCHITECTURE.md) | "Concept to Cash" architecture, N8N workflows, Supabase schema | ✅ Spec |

---

## 10 — ListingForge (1 file)
| Document | Description | Status |
|----------|-------------|--------|
| [PRODUCT_SPEC.md](10-listingforge/PRODUCT_SPEC.md) | Full SaaS product spec — AI listing image + content generator | ✅ Detailed |

---

## 11 — Product Intelligence Engine (1 file)
| Document | Description | Status |
|----------|-------------|--------|
| [PROJECT_BRIEF.md](11-product-intelligence/PROJECT_BRIEF.md) | PIE — algorithmic SKU selection for GoHeadCase (~200K from 1.89M) | ✅ Current (Mar 7) |

---

## 12 — Organization (1 file)
| Document | Description | Status |
|----------|-------------|--------|
| [PH_STAFF_ROSTER.md](12-org/PH_STAFF_ROSTER.md) | 38 PH staff — departments, roles, salaries | ✅ Current |

---

## 13 — SaaS Spin-off (2 files)
| Document | Description | Status |
|----------|-------------|--------|
| [STRATEGY.md](13-saas-spinoff/STRATEGY.md) | AI automation agency concept | ⚠️ Early concept |
| [STRATEGIC_PRESENTATION.md](13-saas-spinoff/STRATEGIC_PRESENTATION.md) | Strategic presentation | ✅ Reference |

---

## 14 — GoHeadCase (14 files)
| Document | Description | Status |
|----------|-------------|--------|
| [MASTER_PROJECT_MAP.md](14-goheadcase/MASTER_PROJECT_MAP.md) | Full project map (phases, tracks) | ✅ Current |
| [GOHEADCASE_PRODUCT_MATRIX.md](14-goheadcase/GOHEADCASE_PRODUCT_MATRIX.md) | Product type × device matrix | ✅ Key |
| [MOMENTUM_ANALYSIS.md](14-goheadcase/MOMENTUM_ANALYSIS.md) | Project momentum/velocity analysis | ✅ Reference |
| [PHASE0_MICRO_CATALOGUE.md](14-goheadcase/PHASE0_MICRO_CATALOGUE.md) | Phase 0 micro catalogue spec | ✅ Reference |
| [DESIGN_HUB_SPEC.md](14-goheadcase/DESIGN_HUB_SPEC.md) | Design hub specification | ✅ Reference |
| [STORE_NAV_RULES.md](14-goheadcase/STORE_NAV_RULES.md) | Store navigation rules | ✅ Reference |
| [WAREHOUSE_POC_SPEC.md](14-goheadcase/WAREHOUSE_POC_SPEC.md) | Warehouse POC spec | ✅ Reference |
| [POC_WAREHOUSE_BRIEF.md](14-goheadcase/POC_WAREHOUSE_BRIEF.md) | POC warehouse brief | ✅ Reference |
| [MISSION_UX_COUNCIL.md](14-goheadcase/MISSION_UX_COUNCIL.md) | Mission + UX council strategy | ✅ Reference |
| [TEAM_MISSION_STRATEGY.md](14-goheadcase/TEAM_MISSION_STRATEGY.md) | Team mission strategy | ✅ Reference |
| [amazon-us summary](14-goheadcase/amazon-us-2026-01-01_to_2026-02-15-summary.md) | Amazon US sales summary | ✅ Data |
| [uk-vs-us summary](14-goheadcase/uk-vs-us-sales-summary-2026-01-01_to_2026-02-15.md) | UK vs US sales comparison | ✅ Data |
| [rag/ECOM_EXPERT_RAG_SCHEMA.md](14-goheadcase/rag/ECOM_EXPERT_RAG_SCHEMA.md) | RAG schema for ecommerce expert | ✅ Spec |
| [rag/RAG_SEED_TODO.md](14-goheadcase/rag/RAG_SEED_TODO.md) | RAG corpus seed checklist | ⚠️ Mostly incomplete |

---

## 15 — Email Triage (2 files)
| Document | Description | Status |
|----------|-------------|--------|
| [EMAIL_TRIAGE_PROJECT.md](15-email-triage/EMAIL_TRIAGE_PROJECT.md) | Email memory + triage project spec | ✅ Spec |
| [N8N_WORKFLOW_V1.md](15-email-triage/N8N_WORKFLOW_V1.md) | N8N workflow for email triage v1 | ✅ Spec |

---

## 16 — Other Projects (7 files)
| Document | Description |
|----------|-------------|
| [brain-memory-layer/BRAIN_MEMORY_LAYER_SPEC.md](16-other-projects/brain-memory-layer/BRAIN_MEMORY_LAYER_SPEC.md) | Brain memory layer spec (semantic search) |
| [data-sync/SKU_PARSING_AND_SYNC.md](16-other-projects/data-sync/SKU_PARSING_AND_SYNC.md) | SKU parsing and data sync spec |
| [sales-bot/ARCHITECTURE.md](16-other-projects/sales-bot/ARCHITECTURE.md) | Sales bot architecture |
| [sales-bot/AWS_INTEGRATION_RESEARCH.md](16-other-projects/sales-bot/AWS_INTEGRATION_RESEARCH.md) | AWS integration research |
| [ecell-spinoffs/README.md](16-other-projects/ecell-spinoffs/README.md) | Ecell spin-off products index |

---

## 17 — Harry's Workspace (137 files) ⭐ NEW
*Source: `gdrive:Clawdbot Shared Folder/Harry folder for iMac transfer/`*
*Harry's complete OpenClaw workspace — memory, daily logs, project specs, ecell-ops workspace*

### Root Workspace Files
| Document | Description |
|----------|-------------|
| [MEMORY.md](17-harry-workspace/MEMORY.md) | Harry's long-term memory (current) |
| [MEMORY (1).md](17-harry-workspace/MEMORY%20(1).md) | Harry's memory (earlier version) |
| [SOUL.md](17-harry-workspace/SOUL.md) | Harry's identity/persona definition |
| [AGENTS.md](17-harry-workspace/AGENTS.md) | Harry's agent team config |
| [AGENT_CONFIG.md](17-harry-workspace/AGENT_CONFIG.md) | Agent configuration |
| [TOOLS.md](17-harry-workspace/TOOLS.md) | Harry's tools notes |
| [USER.md](17-harry-workspace/USER.md) | Harry's notes about Cem |
| [fulfillment-orchestrator-build-log.md](17-harry-workspace/fulfillment-orchestrator-build-log.md) | Build log |

### Daily Logs (22 files)
`daily/2026-01-27.md` through `daily/2026-03-03.md` — Harry's daily operational logs

### Project Specs (47 files across 14 project folders)
| Folder | Key Documents |
|--------|--------------|
| `projects/ai-coo/` | AVA_DASHBOARD_BRIEF, AVA_FRONTEND_BRIEF, AVA_IMAGE_MAKER_BRIEF, BLUEPRINT, LOCAL_LLM_SETUP |
| `projects/amazon-sp-api/` | APPLICATION-CHECKLIST, SP-API-GUIDE |
| `projects/cs-automation/` | CS_ARCHITECTURE, ARCHITECTURE, IMPLEMENTATION, MARKETPLACE_RULES, TICKETING_SCHEMA, knowledge-base/* |
| `projects/cs-ai-system/` | CS_AI_ARCHITECTURE_SPEC |
| `projects/design-automation/` | CREATIVE_PIPELINE, PHONE_CASE_IMAGE_GEN_PROMPTS, LISTINGFORGE_SPEC, console-skins/*, print-images/*, product-images/*, track1-speed-to-market/* |
| `projects/fulfillment-orchestrator/` | README, PROGRESS |
| `projects/hcd-listing-generator/` | README, DEPLOYMENT, QUICKSTART-RAILWAY |
| `projects/local-llm-research/` | LOCAL_LLM_REPORT |
| `projects/business-dashboard/` | README |
| `projects/fba-analyzer/` | README |
| `projects/goheadcase-d2c/` | README |
| `projects/ava-setup/` | IDENTITY, INSTALL, SOUL |

### ecell-ops Workspace (68 files)
Harry's original ecell-ops OpenClaw workspace — includes his workspace files, memory logs (Jan 27 – Feb 14), and full project folder mirror with specs for ai-coo, amazon-sp-api, cs-automation, design-automation, local-llm-research, production-workflow, saas-spin-off, sales-analysis, sales-schema, vertex-ai-rag.

---

## 18 — Competitor Research (11 files) ⭐ NEW
*Source: `Competitor_Analysis_2026-01-28/` + `Research/` + `Sales Data Amazon US/`*

| Document | Description |
|----------|-------------|
| [FULL_COMPETITOR_REPORT_2026-01-28.md](18-competitor-research/FULL_COMPETITOR_REPORT_2026-01-28.md) | Comprehensive competitor report |
| [ANALYSIS_REPORT_2026-01-28.md](18-competitor-research/ANALYSIS_REPORT_2026-01-28.md) | Competitor analysis report |
| [EXTENDED_PRODUCT_CATEGORIES_2026-01-28.md](18-competitor-research/EXTENDED_PRODUCT_CATEGORIES_2026-01-28.md) | Extended product category mapping |
| [NBA_MERCHANDISE_REPORT_2026-01-28.md](18-competitor-research/NBA_MERCHANDISE_REPORT_2026-01-28.md) | NBA merchandise landscape |
| [Perplexity competitor analysis.md](18-competitor-research/Perplexity%20competitor%20analysis.md) | Amazon US competitor deep-dive |
| [5_Rebrand_Options_SWOT_Analysis.md](18-competitor-research/5_Rebrand_Options_SWOT_Analysis.md) | 5 rebrand options SWOT |
| [Refined_Rebrand_Names_Tech_Accessories.md](18-competitor-research/Refined_Rebrand_Names_Tech_Accessories.md) | Refined rebrand name options |
| [Spinoff_Rebrand_Strategic_Study.md](18-competitor-research/Spinoff_Rebrand_Strategic_Study.md) | SaaS spin-off rebrand strategy |
| [SaaS_Spinoff_Research_AI_Automation_Agency.md](18-competitor-research/SaaS_Spinoff_Research_AI_Automation_Agency.md) | AI automation agency research |
| [competitor_style_analysis.md](18-competitor-research/competitor_style_analysis.md) | Visual/style competitor analysis |
| [design_inspiration_research.md](18-competitor-research/design_inspiration_research.md) | Design inspiration research |

---

## 19 — Collaboration (7 files) ⭐ NEW
*Source: `collaboration/` — Harry ↔ Ava handoffs and joint work*

| Document | Description |
|----------|-------------|
| [HANDOFF_HARRY.md](19-collaboration/HANDOFF_HARRY.md) | Harry's main handoff document |
| [HANDOFF_HARRY_ECELL_HERO_LAYOUT.md](19-collaboration/HANDOFF_HARRY_ECELL_HERO_LAYOUT.md) | Hero section layout handoff |
| [IMPLEMENTATION_SPECS.md](19-collaboration/IMPLEMENTATION_SPECS.md) | Joint implementation specifications |
| [OVERNIGHT_SUMMARY.md](19-collaboration/OVERNIGHT_SUMMARY.md) | Overnight work summary |
| [brand_refinement_proposals.md](19-collaboration/brand_refinement_proposals.md) | Brand refinement proposals |
| [content_website_suite.md](19-collaboration/content_website_suite.md) | Website content suite |
| [research_competitor_summary.md](19-collaboration/research_competitor_summary.md) | Competitor research summary |

---

## 20 — Ecell Website Redesign (15 files) ⭐ NEW
*Source: `Projects/2_Ecell_Website_Redesign/` + `Projects/` root*

### Research
| Document | Description |
|----------|-------------|
| [research/B2B_Research_Brief_EcellGlobal.md](20-ecell-website/research/B2B_Research_Brief_EcellGlobal.md) | B2B research brief |
| [research/Competitive_Research_Report_EcellGlobal_B2B.md](20-ecell-website/research/Competitive_Research_Report_EcellGlobal_B2B.md) | B2B competitive research |
| [research/Competitor_Analysis_B2B_Tech_Accessories.md](20-ecell-website/research/Competitor_Analysis_B2B_Tech_Accessories.md) | B2B tech accessories competitor analysis |
| [research/phase1_content_audit_report.md](20-ecell-website/research/phase1_content_audit_report.md) | Phase 1 content audit |

### Content
| Document | Description |
|----------|-------------|
| [content/Ecell_Tech_Website_Content_Complete.md](20-ecell-website/content/Ecell_Tech_Website_Content_Complete.md) | Complete website content |
| [content/Content_Inventory_Rewrite_Strategy.md](20-ecell-website/content/Content_Inventory_Rewrite_Strategy.md) | Content rewrite strategy |
| [content/ecell-website-content-v3-international.md](20-ecell-website/content/ecell-website-content-v3-international.md) | V3 international content |

### Project Management
| Document | Description |
|----------|-------------|
| [project-management/PROJECT_STATUS.md](20-ecell-website/project-management/PROJECT_STATUS.md) | Project status tracker |
| [project-management/synapseai_website_roadmap.md](20-ecell-website/project-management/synapseai_website_roadmap.md) | Original SynapseAI roadmap |
| [project-management/synapseai_website_roadmap_REVISED.md](20-ecell-website/project-management/synapseai_website_roadmap_REVISED.md) | Revised roadmap |

### Other
| Document | Description |
|----------|-------------|
| [design-assets/antigravity_design_brief.md](20-ecell-website/design-assets/antigravity_design_brief.md) | Antigravity design brief |
| [SPECIALIST_ROSTER.md](20-ecell-website/SPECIALIST_ROSTER.md) | Project specialist roster |
| [PROJECTS.md](20-ecell-website/PROJECTS.md) | Projects overview |
| [PRODUCT_SPEC_LISTINGFORGE.md](20-ecell-website/PRODUCT_SPEC_LISTINGFORGE.md) | ListingForge spec (copy from Projects/) |
| [README.md](20-ecell-website/README.md) | Design automation README |

---

## 21 — Ava Archive (31 files) ⭐ NEW
*Source: `ava-backup-2026-03-05/workspace/` — Ava's pre-Mac Studio workspace*

### Workspace Core
| Document | Description |
|----------|-------------|
| [MEMORY.md](21-ava-archive/MEMORY.md) | Ava's memory (pre-migration) |
| [MEMORY.ecell-ops.md](21-ava-archive/MEMORY.ecell-ops.md) | Harry's ecell-ops memory copy |
| [SOUL.md](21-ava-archive/SOUL.md) | Ava's identity (old version) |
| [AGENTS.md](21-ava-archive/AGENTS.md) | Ava's agent config (old) |
| [AGENTS_ROSTER.md](21-ava-archive/AGENTS_ROSTER.md) | Agent roster |
| [AGENT_CONFIG.md](21-ava-archive/AGENT_CONFIG.md) | Agent config |
| [TOOLS.md](21-ava-archive/TOOLS.md) | Tools notes |
| [TASKS.md](21-ava-archive/TASKS.md) | Task list (pre-migration) |
| [CRON_CALENDAR.md](21-ava-archive/CRON_CALENDAR.md) | Cron schedule |
| [HEARTBEAT.md](21-ava-archive/HEARTBEAT.md) | Heartbeat config |
| [HANDOFF_FROM_HARRY.md](21-ava-archive/HANDOFF_FROM_HARRY.md) | Harry's handoff to Ava |
| [IDENTITY.md](21-ava-archive/IDENTITY.md) | Identity file |
| [USER.md](21-ava-archive/USER.md) | User notes |

### Daily Logs
`2026-02-23` through `2026-03-05` — 10 daily operational logs + weekly recap

### Subfolders
`content/`, `presentations/`, `orbit-pm/`, `ops/`, `MicroAnime/`, `_tmp/`

---

## 22 — Presentations (4 files) ⭐ NEW
*Source: `Presentations/` + `Cem Review/` + `design-automation/`*

| Document | Description |
|----------|-------------|
| [EcellGlobal_B2B_Redesign_Strategy.md](22-presentations/EcellGlobal_B2B_Redesign_Strategy.md) | B2B redesign strategy presentation |
| [content_website_suite.md](22-presentations/content_website_suite.md) | Website content suite (Cem review) |
| [hero-variations-prompts.md](22-presentations/hero-variations-prompts.md) | Hero section design prompts |
| [design-auto-reference-README.md](22-presentations/design-auto-reference-README.md) | Design automation reference images |

---

## Key Cross-Reference Map

```
SCHEMA_DESIGN (02) ──────────► PIE PROJECT_BRIEF (11)
                               ├── uses SKU decomposition logic
                               └── unified schema = PIE's data backbone

SALES_ANALYSIS_2025 (02) ────► PIE PROJECT_BRIEF (11)
                               ├── 268K orders = scoring data
                               └── geo brand rankings = regional splits

DESIGN_FILE_MGMT (06) ───────► CREATIVE_PIPELINE (09)
                               └── design files = input to image funnel

CREATIVE_PIPELINE (09) ──────► LISTINGFORGE (10)
                               └── ListingForge = productized version

PRINT_FILE_PIPELINE (03) ────► DESIGN_FILE_MGMT (06)
                               └── camera hole issue spans both

CS_ARCHITECTURE (01) ────────► EMAIL_TRIAGE (15)
                               └── email triage supersedes CS email bot

GOHEADCASE (14) ──────────────► PIE (11)
                               └── PIE determines what ships to GoHeadCase

INVENTORY (05) ───────────────► SHIPPING (04)
                               └── stock-out = rerouting trigger

HARRY WORKSPACE (17) ────────► all sections
                               └── Harry's project specs = origin docs
                                   for sections 01-10

COMPETITOR RESEARCH (18) ────► GOHEADCASE (14) + SAAS SPINOFF (13)
                               └── market positioning data

COLLABORATION (19) ──────────► ECELL WEBSITE (20)
                               └── handoffs drove website redesign

ECELL WEBSITE (20) ──────────► ecellglobal.com live site
                               └── content, research, roadmap archive
```

---

## 30 — Zero 2.0 & Staff Automation (3 files) — NEW
| Document | Description | Status |
|----------|-------------|--------|
| [ZERO_SYSTEM_SUMMARY.md](30-zero-2/ZERO_SYSTEM_SUMMARY.md) | Legacy Zero ERP system — infrastructure, databases, technical debt | ✅ Current |
| [ZERO_2_BUILD_PLAN.md](30-zero-2/ZERO_2_BUILD_PLAN.md) | Zero 2.0 agentic replacement — plan + Ava's scope assessment | ✅ Under Review |
| [STAFF_AUTOMATION_MAP.md](30-zero-2/STAFF_AUTOMATION_MAP.md) | Full PH staff × automation mapping — who stays, who's replaced, timeline | ✅ Current |

**Cross-refs:** → `12-org/PH_STAFF_ROSTER` (staff details), → `23-drew-handover/` (Patrick profile, Zero infra), → `projects/procurement/` (procurement spec)

---

## Recent Projects Not Yet In Wiki (as of 2026-03-20)

| Project | Location | Description | Status |
|---------|----------|-------------|--------|
| **Procurement System** | `projects/procurement/` | Demand-based PO generation with supplier splits | ✅ Spec complete (Mar 20) |
| **Walmart Lister** | `projects/walmart-lister/` + `projects/walmart/` | Walmart Marketplace API integration, item feeds | 🟡 API auth works, feed ingestion blocked |
| **SKU Staging** | `projects/sku-staging/` | Champion selection, Shopify CSV, marketplace expansion pipeline | ✅ Active — first Shopify order Mar 20 |
| **PULSE v2** | `projects/pulse-dashboard-v2/` | Regional filters, product groups, Supabase-backed velocity dashboard | ✅ Live at pulse-dashboard-inky.vercel.app |
| **Shopify Store** | TOOLS.md (creds) | Head Case Shopify store — 200K SKU target, first sale Mar 20 | 🟡 Live, importing champions |
| **QMD Memory** | OpenClaw config | Tobi Lütke's hybrid memory search backend — installed Mar 20 | ✅ Live |

---

*Wiki last updated: 2026-03-20 by Ava*
*Total documents: 270+ | Sections: 30*
*Source coverage: All .md files from Clawdbot Shared Folder + recent project docs*
*QMD now indexes all wiki/ files for memory search*

## 36 — Royalty Reporting (4 files) ⭐ NEW
| Document | Description | Status |
|----------|-------------|--------|
| [README.md](36-royalty-reporting/README.md) | Project overview and scope | ✅ Current |
| [ROYALTY_CALCULATION.md](36-royalty-reporting/ROYALTY_CALCULATION.md) | Contract/rate logic + royalty automation SOP | ✅ Current |
| [LEGACY_LOGIC_EXTRACTION.md](36-royalty-reporting/LEGACY_LOGIC_EXTRACTION.md) | Legacy PHP royalty engine extraction | ✅ Current |
| [IMPLEMENTATION_MAP.md](36-royalty-reporting/IMPLEMENTATION_MAP.md) | Target architecture and rollout plan | ✅ Current |
