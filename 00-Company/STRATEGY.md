# Ecell Global — Strategic Execution Framework
*Created: 2026-03-07 | Owner: Ava (CPSO) | Approved: Cem (CEO)*

---

## The Four Pillars

### Pillar 1: SALES — Revenue Engine
*Goal: Algorithmically select the right products, on the right channels, at the right price.*

| Project | Owner | Agent(s) | Status | Wiki Docs |
|---------|-------|----------|--------|-----------|
| **PIE — Product Intelligence Engine** | Harry | Atlas (Gemini 3.1 Pro), Prism (GPT-5.4) | 🟡 Brief complete, awaiting execution | `11-product-intelligence/` |
| **SKU Selection (~200K from 1.89M)** | Harry | Atlas + Prism ensemble | 🔴 Blocked on design-level revenue query | `02-sales-data/SCHEMA_DESIGN.md` |
| **Target+ Strategy** | Ava | Bolt (research) | 🟡 Deep dive done Mar 6 | `wiki/14-goheadcase/` |
| **Walmart Strategy** | Ava | Bolt | 🔴 Not started (95K SKUs, 99.9% zero reviews) | `11-product-intelligence/PROJECT_BRIEF.md` |
| **Amazon FBA Conversion** | Ava | Atlas | 🔴 Not started (3.44M SKUs ALL FBM!) | — |
| **Sales Dashboard V2** | Harry | Forge/Spark (Codex) | 🟡 Frontend exists, needs Supabase backend | `02-sales-data/` |

**Key Data:**
- 304K orders, $18.9M revenue (Supabase)
- Top 50 devices = 86.5% of revenue
- Regional splits: US = iPhone + desk mats, UK = Samsung A16 5G + console skins
- Target+ hard rule: NO US Sports

**PH Staff Impact:** None directly — this is strategic, not operational.

**Milestone:** First scored PIE output (design-level rankings) → 1 week from data pipeline completion.

---

### Pillar 2: PRODUCTION — Build & Ship Engine
*Goal: Automate the path from order → printed product → shipped package. Spec thoroughly, automate incrementally, prove before transitioning staff.*

| Project | Owner | Agent(s) | Status | Wiki Docs |
|---------|-------|----------|--------|-----------|
| **Print File Automation** | Harry | Forge (Codex) | 🔴 Specced, not built | `03-production/PRINT_FILE_PIPELINE.md` |
| **Camera Hole Detection (AI Vision)** | Harry | Gemini Vision | 🔴 Concept only — needs examples from Cem | `06-design-automation/SOP_DESIGN_FILE_MANAGEMENT.md` |
| **Design File Pipeline** | Sven | Sven (Gemini 3.1 Pro) | ⏸️ ON HOLD — Sven inactive, parked in `02-Projects/99-On-Hold/` | `06-design-automation/` |
| **Label ↔ Print File Reconciliation** | Harry | N8N workflow | 🔴 Specced | `03-production/DAILY_PRINT_PRODUCTION.md` |
| **Veco Integration (EU/Intl)** | Cem/Tim | — | 🟡 US+UK done, EU/Intl remaining | `04-shipping/SHIPPING_CARRIER_RULES.md` |
| **Production Workflow SOP** | Ava | — | 🟡 Documented but needs validation with PH team | `03-production/` |

**Key Data:**
- 5-7 PH staff daily on print file generation (#1 automation target)
- 80% of orders = standard (automatable), 15% = AI-assisted, 5% = manual
- TIFF files (flatbed/jig) + EPS files (vinyl skins) = two separate pipelines
- Camera hole placement = the hard problem

**PH Staff Impact:**
- **Production team (10):** 3-5 staff on print files could be redeployed once automation proven
- **Approach:** Run automation IN PARALLEL with manual for 4-8 weeks. Compare output quality. Only transition when error rate < manual error rate.

**Blockers:** Camera hole obstruction examples from Cem, EPS workflow documentation.

**Milestone:** Automated print file generation for top 10 devices (TIFF pipeline) with <5% error rate.

---

### Pillar 3: OPERATIONS — Run the Machine
*Goal: Inventory accuracy, shipping reliability, CS efficiency. The foundation everything else depends on.*

| Project | Owner | Agent(s) | Status | Wiki Docs |
|---------|-------|----------|--------|-----------|
| **Inventory Tracking (Supabase)** | Harry | — | 🔴 Legacy MySQL, needs migration | `05-inventory/SOP_INVENTORY_TRACKING.md` |
| **Velocity-Based Reordering** | Harry | Atlas | 🔴 Needs inventory + sales data connected | `05-inventory/` |
| **Shipping Carrier Optimization** | Ava | Bolt | 🟡 Rules documented, Veco partially configured | `04-shipping/SHIPPING_CARRIER_RULES.md` |
| **CS Email Automation** | Harry | N8N + GPT-4o-mini | 🟡 Chat bot live, email draft inactive | `01-customer-service/` |
| **Email Triage (N8N)** | Harry | N8N workflow | 🟡 Spec complete | `15-email-triage/` |
| **Slack EOD Monitoring** | Ava | Daily cron | ✅ Live (8 AM EST) | — |
| **Marketplace Compliance Rules** | Ava | — | ✅ Documented | `01-customer-service/MARKETPLACE_RULES.md` |

**Key Data:**
- 3-layer shipping routing: Equipment capability → Stock availability → Manual overrides
- Amazon 24hr SLA (including weekends) — highest compliance risk
- Inventory currently on 15-year-old MySQL — needs migration to Supabase
- CS team (5 PH staff) handles multi-marketplace support

**PH Staff Impact:**
- **CS team (5):** Email triage AI reduces ticket volume — potential to handle 2x volume with same headcount (growth enabler, not headcount cut)
- **Label management (2):** Veco already automating — staff transitioning once EU/Intl configured

**Blockers:** Legacy MySQL access, Gmail App Password, Cloud SQL connection details.

**Milestone:** Inventory data in Supabase + automated stock alerts for top 50 devices.

---

### Pillar 4: GROWTH — Scale the Business
*Goal: New channels, better storefronts, marketing automation. Only once Pillars 1-3 are solid.*

| Project | Owner | Agent(s) | Status | Wiki Docs |
|---------|-------|----------|--------|-----------|
| **ListingForge MVP** | Ava | Forge/Spark (Codex) | 🔴 Full spec exists, not built | `10-listingforge/PRODUCT_SPEC.md` |
| **GoHeadCase Shopify Store** | Harry | Forge (Codex) | 🔴 Blocked on PIE output (Pillar 1) | `14-goheadcase/` |
| **Themed Microsites** | Ava | Sven (design), Forge (build) | 🔴 Folders exist, no builds | `wiki/16-other-projects/microsites/` |
| **RAG Corpus (Ecom Expert)** | Sven | Sven (Gemini 3.1 Pro) | 🔴 1/30 pattern cards, 2/18 benchmarks | `14-goheadcase/rag/` |
| **Website Chatbot** | Harry | Vertex AI / Gemini Flash | 🔴 Specced, not built | `07-chatbot-rag/VERTEX_AI_RAG_PLAN.md` |
| **Naruto Design Assets** | Sven | Sven | 🟡 20 PSDs uploaded, no output yet | — |
| **Social Marketing** | Ava | Echo (copy), Iris (design) | 🔴 Not started | — |
| **SaaS Spin-off (ListingForge public)** | Cem | — | ⏸️ Phase 3 — after internal tool proven | `13-saas-spinoff/` |
| **Ecellglobal.com Redesign** | Ava | Forge (Codex) | 🟡 Deployed on Vercel, DNS pending | — |

**PH Staff Impact:**
- **Listings team (8):** ListingForge reduces manual listing creation from hours to minutes per product
- **Creative team (6):** AI-generated mockups + content = 10x output with same team
- **Net effect:** Same headcount, dramatically more products listed across more channels

**Milestone:** ListingForge MVP generating images + content for 1 brand × 10 devices.

---

## Execution Sequence

```
QUARTER 1 (NOW → Apr 2026)
├── Pillar 1: PIE data pipeline + first scored output
├── Pillar 2: Print file pipeline — spec validation with PH team
├── Pillar 3: Inventory → Supabase migration started
└── Pillar 4: ListingForge MVP (internal, 1 brand)

QUARTER 2 (Apr → Jun 2026)
├── Pillar 1: 200K SKUs selected, GoHeadCase Shopify loaded
├── Pillar 2: Automated TIFF pipeline running in parallel with manual
├── Pillar 3: CS email triage live, Veco EU/Intl configured
└── Pillar 4: GoHeadCase live on Shopify, first microsites

QUARTER 3 (Jul → Sep 2026)
├── Pillar 1: Amazon FBA conversion strategy for top 1000 SKUs
├── Pillar 2: Staff transition — validated automation replaces manual
├── Pillar 3: Velocity-based reordering live
└── Pillar 4: ListingForge public beta (SaaS), marketing ramp
```

---

## Agent Assignment Matrix

| Agent | Pillar | Primary Work |
|-------|--------|-------------|
| **Ava (me)** | ALL | Strategic oversight, project management, delegation, quality gate |
| **Harry** | 1, 2, 3 | PIE orchestration, N8N workflows, Supabase, data pipelines |
| **Atlas** | 1 | Data analysis (Gemini 3.1 Pro) — revenue scoring, device rankings |
| **Prism** | 1 | Behavioral analysis (GPT-5.4) — probabilistic SKU scoring |
| **Sven** | 2, 4 | Design work (Gemini 3.1 Pro) — Naruto assets, RAG corpus, mockups |
| **Bolt** | 1, 3 | Research/scout (Gemini Flash) — marketplace intel, SEO, trends |
| **Forge** | 2, 4 | Web builds (Codex GPT-5.3) — ListingForge, GoHeadCase, dashboards |
| **Spark** | 2, 4 | Complex code (Codex GPT-5.3) — architecture, multi-file refactors |
| **Echo** | 4 | Copywriting (Sonnet 4.6) — listings, ad copy, marketing content |

---

## Dependencies Map

```
Pillar 1 (Sales) ──── outputs ────► Pillar 4 (Growth)
    │                                    │
    │ PIE selects SKUs                   │ GoHeadCase needs SKU list
    │ Revenue data informs pricing       │ ListingForge needs product catalog
    │                                    │
Pillar 2 (Production) ◄── feeds ──── Pillar 3 (Operations)
    │                                    │
    │ Print files need order data        │ Inventory feeds production routing
    │ Design files need catalog          │ Shipping needs label-print match
    │                                    │
    └──────────► BOTH need Supabase as backbone ◄──────────┘
```

---

## Governance Rules

1. **No staff transitions until automation runs in parallel for 4+ weeks with <5% error rate**
2. **Cem approves any headcount changes** — AI recommends, human decides
3. **Weekly status updates** — Ava reports to Cem every Monday (or on-demand)
4. **Blockers escalated within 24 hours** — if an agent is stuck, Ava escalates to Cem
5. **Ship > Spec** — every project gets a 1-week MVP target after spec approval

---

*This is a living document. Updated as pillars progress.*
*Saved to: workspace/STRATEGY.md | Wiki: to be added*
*Committed to: MEMORY.md (summary)*
