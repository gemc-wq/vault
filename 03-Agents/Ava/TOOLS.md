# Ava — TOOLS.md
**Role:** CPO / Strategy Agent | **Model:** Haiku/Sonnet (OpenClaw) | **Host:** Mac Studio
**Updated:** 2026-04-14

---

## Session Bootstrap (Do This Every Session)

1. Read `~/Vault/00-Company/compiled/TASK_SHEET.md` — check your assigned tasks
2. Read `~/Vault/03-Agents/Ava/handoffs/` — check for incoming work from other agents
3. Read relevant `~/Vault/02-Projects/` folders for active work
4. If unsure about process: read `~/Vault/00-Company/AGENT_COLLABORATION.md`

## Vault Navigation

| Looking For | Path |
|-------------|------|
| Your tasks | `~/Vault/00-Company/compiled/TASK_SHEET.md` |
| Company strategy | `~/Vault/00-Company/STRATEGY.md` |
| Agent roster | `~/Vault/00-Company/AGENT_ROSTER.md` |
| Skill definitions | `~/Vault/00-Company/skills/SKILLS_INDEX.md` |
| Collaboration rules | `~/Vault/00-Company/AGENT_COLLABORATION.md` |
| Your folder | `~/Vault/03-Agents/Ava/` |
| Incoming handoffs | `~/Vault/03-Agents/Ava/handoffs/` |
| Shared work | `~/Vault/04-Shared/active/` |
| Cross-agent decisions | `~/Vault/04-Shared/decisions/` |

---

## Infrastructure

### Harry (COO Agent — OpenClaw on iMac)
- **Host:** cems-imac (Cem's iMac, local network)
- **Tailscale IP:** 100.91.149.92
- **Model:** Kimi K2.5 (upgrading to GPT-5.4, pending Cem config). Opus advisor NOT enabled for Harry.
- **SSH:** `ssh 100.91.149.92` (via Tailscale)
- **Handoffs:** `~/Vault/03-Agents/Harry/handoffs/` (Vault, NOT GDrive)
- **Workspace:** iMac local (~/clawd or ~/.openclaw/workspace)
- **NOT on a VPS** — runs on local iMac connected via Tailscale
- **Sentinel role:** Harry now includes Sentinel monitoring responsibilities (merged Apr 13)

### Ava (Strategy Agent — OpenClaw on Mac Studio)
- **Host:** cems-mac-studio (Mac Studio, NOT GDrive/iMac)
- **Tailscale IP:** 100.72.19.27
- **Handoffs:** `~/Vault/03-Agents/Ava/handoffs/` (Vault, NOT GDrive)
- **Cross-agent work:** `~/Vault/04-Shared/` (active tasks, completed work, decisions)
- **Handoff template:** `~/Vault/00-Company/skills/delegation/handoff-template.md`

## Agent Dispatch Rules (Added 2026-04-11)

### Data Analysis & Building
- **Codex:** Data analysis, financial modeling, CSV processing, architecture decisions
- Uses: Python, SQL, pandas, numpy for quantitative work
- Examples: 90-day sales analysis, revenue modeling, conversion analysis, database design

### Research & Crons & Heartbeats
- **Gemini (Flash/Pro):** Web research, competitive analysis, trend spotting
- **Pixel:** Cron jobs, heartbeat tasks, scheduled reports
- Uses: web_search, market research, lightweight computation
- Examples: Prime badge algorithmic impact research, competitor teardowns, weekly digests

### Strategic Planning & Architecture Review
- **Advisor Tool (Opus 4.6):** Used for major project shapes, timelines, financial recommendations
- Invoked by Ava for: Project-SHAPE docs, PROJECT-PLAN feasibility, high-stakes decisions
- Example: Unified Listings Intelligence architecture review

### Creative & Marketing
- **Sven (Creative & Marketing Director — Sub-agent under Ava)**
- **Agent ID:** sven
- **Model:** Gemini 3.1 Pro
- **Runs as:** Sub-agent (not separate instance — iMac only has 8GB RAM, can't run another OpenClaw)
- **SOUL.md:** `gdrive:Clawdbot Shared Folder/Brain/Agents/Sven/SOUL.md`
- **Role:** Marketing & Creative Director — owns creative quality bar and design corpus
- **Tasks:**
  1. **RAG Corpus** — Build and maintain the GoHeadCase design corpus at `Brain/Projects/goheadcase/rag/`
     - Pattern cards (30 total, 10 done, 20 remaining)
     - Benchmark captures (Casetify, Apple, OtterBox, Fanatics, Skinit)
     - Templates (PDP, universe landing, cart/checkout, mega menu)
     - Rubrics and seed datasets
  2. **Ecell Studio** — Image pipeline for product mockups, banners, lifestyle shots at `Brain/Projects/design-automation/`
  3. **UX/CRO Council** — Review wireframes and pages against Apple/Casetify/OtterBox benchmarks before shipping
  4. **Growth** — Influencer playbooks, content briefs, campaign concepts
- **8 Council Roles:** Design Critic, UX Architect, CRO Strategist, Merchandising Director, Creative Director, Growth Operator, Data Analyst, Asset Librarian
- **Dispatch:** `sessions_spawn` with `agentId: sven`
- **Output goes to:** `Brain/Projects/goheadcase/rag/` (corpus) and `Brain/Projects/design-automation/` (studio)
- **Keep busy:** Dispatch next task from backlog every heartbeat cycle if idle

---

### Tailscale Network
- cems-mac-studio (100.72.19.27) — Ava / Mac Studio
- cems-imac (100.91.149.92) — Harry / iMac
- hp-cem (100.120.86.40) — Windows PC

## SKU Parsing Rules
- **Reference:** `wiki/SKU_PARSING_RULES.md` — definitive guide for all dashboards/scripts
- **Key rule: F prefix = FBA** — `FHTPCR` = FBA version of `HTPCR`. Always combine for analytics.
- **Exceptions:** `FLAG` (national flags), `F1309` (Formula 1), `FRND` (Friends), `FKFLOR` (FK Floral) — NOT FBA
- **Format:** `{PRODUCT_TYPE}-{DEVICE}-{DESIGN}-{VARIANT}` (4 parts, split by `-`)
- **Canonical type:** Strip leading `F` from product type position only (not from design codes)
- **Region:** Use `Buyer_Country` not `PO_Location` for regional analysis

## Credentials & Accounts

### Shared Identity (Harry & Ava)
- **Email:** harry@ecellglobal.com
- **Password:** [REDACTED_PASSWORD]
- **Purpose:** GitHub, Vercel, OAuth (OpenAI/Gemini)
- **Stored:** 2026-02-06

## API Keys

### Firecrawl
- Key: [REDACTED_FIRECRAWL_KEY]
- Purpose: Web scraping for competitor research
- Stored: 2026-02-02

### Apify
- Key: [REDACTED_APIFY_KEY]
- Purpose: Instagram/TikTok social data
- Stored: 2026-02-02

### ElevenLabs (SAG)
- Key: [REDACTED_ELEVENLABS_KEY]
- Purpose: Text-to-speech (natural voice generation)
- Stored: 2026-02-02

### Anthropic (Claude Sonnet 4.5)
- Key: [REDACTED_ANTHROPIC_KEY]
- Purpose: Content writing (per Cem's request)
- Stored: 2026-02-02

### OpenAI Whisper
- Key: Configured in openclaw.json
- Purpose: Speech-to-text

### Notion
- Key: Stored in ~/.config/notion/api_key
- Purpose: Project management

### Google Drive (rclone)
- Remote: gdrive
- Status: Connected and working

### Gemini
- Key: [REDACTED_GEMINI_KEY]
- Purpose: Web search, content generation, analysis (shared with Harry)
- Stored: 2026-02-02

### Gemini (Image Analysis - Dedicated)
- Key: [REDACTED_GEMINI_IMAGE_KEY]
- Purpose: Image analysis (Ava exclusive)
- Stored: 2026-02-02

### Airweave
- URL: https://app.airweave.ai
- API: https://api.airweave.ai
- Key (Cem): FKgDVMh5rKabjF2eOpIPM_oNMqEoyxb2Ns5cLqxv3IM
- Key (Harry): A_lap_FuyguMzNrWTwpHm7l38EG_4ryWT5Rpxl1LM1w
- Account: gemc@ecellglobal.com (primary), harry@ecellglobal.com (secondary)
- Org: Ecell Global
- Plan: Developer (Free) — 10 sources, 500 queries/mo, 50K entities/mo
- Collection: mirror-test-collection-xsvj7d (ID: 766d2326-9520-476b-823d-d1781ecea955)
- Expires: Jun 2, 2026 (90 days)
- SDK: airweave-sdk 0.9.8 (Python)
- Purpose: MIRROR-PRODUCT context retrieval evaluation
- Stored: 2026-03-04

### Slack (Clawdbot Bot)
- Bot Token: [REDACTED_SLACK_BOT_TOKEN]
- App Token: [REDACTED_SLACK_APP_TOKEN]
- App ID: A0ACDCN4SSC
- Mode: Socket
- Workspace: Ecell Global (T09SV0EKC9G)
- Key Channels:
  - #eod-creative-graphics (C0AHQJK60NP, private) — PH creative team daily reports
  - #eod-listings (C0AHUUGJK7G, private) — PH listings team daily reports
  - #all-ecell (C09SV0EUFQA) — company announcements
  - #creative (C09SVCQS1C2) — creative work
  - #graphics (C09T8AG8AC9) — graphics team
  - #marketing (C0A2AHP2Q4D, private) — marketing
  - #ai (C09TSCR39SS) — AI discussions
  - #ai_workflow (C0AATV85ZBQ, private) — AI workflow
  - #listings (C09SZ0D5FAQ) — listings
  - #eod (C09T8A2P2HX) — general EOD
  - #social (C09SSUCDG78) — social/fun
- Scopes: channels:history, channels:read, chat:write, reactions:write, users:read, channels:join, groups:read, groups:history, app_mentions:read
- ⚠️ SECURITY: DM scopes (im:history, im:read, im:write) REMOVED (Mar 22) — prevents prompt injection via Slack DMs
- To message individuals: use @mentions in channels, NOT DMs
- Daily cron: 8 AM EST Slack digest
- Stored: 2026-03-07

### GitHub (gemc-wq)
- Token (classic): REVOKED 2026-04-14 (was exposed in git remote URL)
- Account: gemc-wq
- Scope: repo
- Purpose: Push repos from Mac Studio (PULSE, future projects)
- ⚠️ NEW TOKEN NEEDED — use `git config --global credential.helper osxkeychain` instead of embedding tokens

### Shopify (Head Case)
- Store: yabfxs-zd.myshopify.com (head-case-1499.myshopify.com)
- App: Ava Lister (Client ID: 23c4629ec8004b1b855f4e68e20111db)
- Admin API Token: [REDACTED_SHOPIFY_ADMIN_TOKEN]
- Scope: write_products, write_inventory
- Plan: Basic
- Products: 0 (empty store — ready for upload)
- Stored: 2026-03-18

### BigCommerce (GoHeadCase / Head Case Designs)
- Store Hash: otle45p56l
- API Base: https://api.bigcommerce.com/stores/otle45p56l/v3/
- Client ID: kxe45s9vob3ss8hjhmt9jnpge20z2en
- Client Secret: [REDACTED_BIGCOMMERCE_CLIENT_SECRET]
- Access Token: [REDACTED_BIGCOMMERCE_ACCESS_TOKEN]
- Catalog: 1,866,758 total SKUs / 949,808 HTPCR
- Auth Header: X-Auth-Token: <access_token>
- Stored: 2026-03-13
- Purpose: Product data for SKU staging pipeline (PULSE Champions → Shopify → Walmart)

### Amazon Reports API (Cloud Run)
- Status: RUNNING (confirmed 2026-04-04)
- Platform: Google Cloud Run
- Purpose: Automated Amazon report downloads (replaces manual Seller Central downloads)
- Next step: Test API output format matches manual download format, then wire weekly cron
- Once tested: Sat 6 AM EST cron will auto-pull US/UK/DE Active Listings + Business Reports
- SOP: `wiki/31-listings-management/SOP_WEEKLY_REPORTS.md`

### Amazon SP-API
- ⚠️ DEPRECATED — Drew's credentials below are the OLD app (does NOT have Reports scope)
- Old Client ID: amzn1.application-oa2-client.e99f04abcd2541289906c15facad1e35
- Old Merchant Token (US): A22QQRQRS0T6NJ
- DO NOT USE for reports — use the middleware instead
- **Correct app:** "Reporting for UK, US, DE" — credentials stored in GCP Secret Manager (project: instant-contact-479316-i4)
- **Middleware URL:** https://amazon-report-middleware-175143437106.europe-west1.run.app
- **API keys:** sk_live_ecell_2026 (dashboard), sk_live_claude_2026 (AI agents), sk_live_cron_2026 (crons)
- **SP-API roles status:** Listings ✅ | Analytics ❌ | Inventory ❌ | Finance ❌ (waiting on PH — Patrick)
- **Full PRD:** ~/Vault/02-Projects/amazon-data-analytics/MIDDLEWARE_PRD_CONSOLIDATED.md
- Stored: 2026-04-14

### Walmart Marketplace API
- Client ID: c7c685fa-e36e-4ca0-9f1a-5d9a505b99a2
- Client Secret: [REDACTED_WALMART_CLIENT_SECRET]
- Auth URL: https://marketplace.walmartapis.com/v3/token
- Items API: https://marketplace.walmartapis.com/v3/items
- Total items: 4,023,659 (confirmed working Mar 20)
- Token: Bearer, 900s TTL
- Stored: 2026-03-20

### NVIDIA (NemoClaw / NIM)
- Key: [REDACTED_NVIDIA_KEY]
- Account: build.nvidia.com (Cem's account)
- Default Model: nvidia/nemotron-3-super-120b-a12b
- Purpose: NemoClaw evaluation, NIM inference
- Stored: 2026-03-23

### Gamma.app
- Key: [REDACTED_GAMMA_KEY]
- Purpose: AI presentation creation
- Stored: 2026-02-02

### N8N
- URL: https://n8n.ecellglobal.com
- API Key: [REDACTED_N8N_API_KEY]
- Login: gemc@ecellglobal.com / ecell_n8n_2026!
- SSH: gcloud compute ssh n8n-server --zone=us-east1-b --project=opsecellglobal
- Purpose: Email triage, CS automation, workflow automation
- Stored: 2026-02-28

### Supabase (Orders & Inventory)
- Project ID: auzjmawughepxbtpwuhe
- URL: https://auzjmawughepxbtpwuhe.supabase.co
- Anon key: [REDACTED_SUPABASE_ANON_KEY]
- Service role key (JWT): [REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc
- DB Password: [REDACTED_DB_PASSWORD] (reset 2026-03-10, use Session Pooler — not IPv4 compatible)
- Tables: orders (304K), inventory (9.8K), walmart_listings (loading)
- Views: v_inventory_alerts, v_sales_by_device, v_sales_by_product_type, v_stock_consumption, v_unmatched_skus
- Stored: 2026-03-03

## Large File Policy
- **GDrive = source of truth** for large project files (Zero dump, print templates, BC exports, etc.)
- **Mac Studio internal = working copies only** — pull from GDrive when needed, delete after use
- **Never keep permanent large file copies locally** — 460GB internal fills fast with Ollama models + workspace
- **Amazon Active Listings** — download weekly, run delta load into SQLite, delete raw file immediately (`--delete-after` flag)
- **No external drive needed** unless fast local access to >50GB files becomes a regular requirement
- **S3 CDN covers all product images** — never store BC image files locally

## Product Image CDN (S3)
- **Base URL:** `https://elcellonline.com/atg/`
- **Pattern:** `{DESIGN}/{VARIANT}/{CASE_PREFIX}-{DEVICE}-{POSITION}.jpg`
- **Example:** `https://elcellonline.com/atg/NARUICO/AKA/TP-CR-IPH17PMAX-1.jpg`
- **Case Prefixes:** TP-CR (Soft Gel), HY-BK (Hybrid), HB-01 (Hard), LB-WH (Leather), HC-CR (Hard Classic), H6-CR (Clear MagSafe), H7-BK (Black MagSafe)
- **Coverage:** TP-CR has widest device coverage (up to iPhone 17 PM). HY-BK stops at iPhone 16.
- **Hosted on:** AWS S3 via elcellonline.com
- **Stored:** 2026-03-18

## Cron & Heartbeat Model Policy (established 2026-03-30)
- **Rule:** ALL crons and heartbeats run on FREE models only — never Anthropic API
- **Primary cron executor:** `pixel` agent → `google/gemini-3-flash-preview` (free)
- **Backup cron executor:** `bolt` agent → `google/gemini-3.1-pro-preview` (free)
- **Also free:** `openai-codex/gpt-5.4` (ChatGPT OAuth), `moonshot/kimi-k2-0905-preview` (Kimi free tier)
- **Never:** `main` (Sonnet), `opus`, or any `anthropic/*` model in crons
- **Heartbeat:** already on `google/gemini-3-flash-preview` ✅
- **Reason:** Cem hit Anthropic rate limits Mar 30. Background jobs don't need frontier models.
- **Exception:** Heavy reasoning crons (PULSE leaderboard, Slack digest) may stay on main temporarily until refactored with tighter prompts

## Active Crons Management
- **Primary Source:** `~/Vault/01-Wiki/infrastructure/ACTIVE_CRONS.md` (canonical cron documentation)
- **Sync Frequency:** Every Monday 8:00 AM ET
- **Process:** Run `cron list --includeDisabled=true`, compare against ACTIVE_CRONS.md, update changes, commit and push
- **When adding a cron:** Update ACTIVE_CRONS.md same day (Time, Agent, Model, Purpose, Output, Dependencies)
- **When disabling a cron:** Move to "Disabled Crons" section with resolution date; keep for 3 months as reference
- **Last Sync:** 2026-04-13 19:35 EDT
- **Added:** 2026-04-13

## Self-Improving Skill System
- **Location:** `memory/skills/` — auto-generated skill cards
- **Index:** `memory/skills/SKILL_INDEX.md` — master lookup table
- **Trigger:** After any task using 5+ tool calls, auto-create or improve a skill card
- **Before tasks:** Always check SKILL_INDEX.md for existing patterns
- **Inspired by:** Hermes Agent (NousResearch) self-improving loop
- **Difference from Hermes:** Hermes auto-creates skills inside its runtime. We persist them as markdown files searchable by QMD. Same concept, OpenClaw-native implementation.
- **Added:** 2026-03-28

## Gmail Send OAuth (added 2026-03-28)
- **Scope:** gmail.send added to existing OAuth app
- **⚠️ CRITICAL SAFETY RULE:** DRAFT ONLY — NEVER auto-send emails
- **Process:** Always compose the email, show to Cem for approval, then send ONLY with explicit "send it" confirmation
- **Reason:** Prompt injection risk — a compromised context could trigger unwanted emails from gemc@ecellglobal.com
- **If in doubt:** Show the draft in Telegram first, wait for approval

## GitHub — gemc99-boop (Harry's account)
- **Token:** [REDACTED_GITHUB_PAT]
- **Purpose:** Original Vercel deployments, ecell.app business dashboard
- **Surviving repos:** sales-dashboard only (everything else deleted during migration)
- **Vercel:** ecells-projects-3c3b03d7 likely connected to this account
- **Stored:** 2026-03-29

## Anthropic Advisor Tool (Ava only — enabled Apr 10 2026)
- **What:** Beta API feature — Opus 4.6 advises Haiku 4.5 mid-generation for strategic guidance
- **Beta header:** `anthropic-beta: advisor-tool-2026-03-01`
- **Tool definition in API call:**
  ```json
  {"type": "advisor_20260301", "name": "advisor", "model": "claude-opus-4-6"}
  ```
- **Valid pair:** Haiku 4.5 (executor) + Opus 4.6 (advisor) ✅
- **When to invoke:** Complex strategy, architecture decisions, multi-step reasoning, quality-critical outputs. NOT routine tasks.
- **Cost:** ~400-700 Opus tokens per advisory call — use judiciously
- **Monitoring:** Cem tracking API costs to validate ROI
- **Harry:** NOT enabled. Harry stays on Kimi K2.5.
- **Docs:** https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool

---

## 🚨 PROJECT OPERATING FRAMEWORK (Established Apr 11, 2026)

**CRITICAL RULE:** Never start building a project without first agreeing it's been shaped.

### Four Phases (In Order)

#### **Phase 1: SHAPING** ← Cem + Ava align on what we're building

**What happens:**
- Cem presents ideas, requirements, edge cases
- Ava reviews MEMORY.md + Vault for prior context + missed opportunities
- Deep discussion: What have we tried before? What didn't work? What did work?
- Advisor tool used liberally (Opus reviews architecture, tradeoffs, risks)
- **Output:** `PROJECT-SHAPE.md` document defining:
  - Problem statement (clear, concise)
  - Scope (what's in, what's out)
  - Edge cases identified (all known gotchas)
  - High-level architecture (layers, data flow, dependencies)
  - Success metrics (how we know it worked)
  - Blockers/dependencies (what do we need from others?)
  - **Most importantly: Agreement from Cem that shape is complete**

**Duration:** 1-3 hours of conversation (Cem + Ava)

**Never proceed past this phase without Cem explicitly saying: "Let's move to planning."**

---

#### **Phase 2: PLANNING** ← Translate shape into execution plan

**What happens:**
- Ava breaks shape into tasks
- Assign owners (Codex, Forge, Harry, etc.)
- Timeline + dependencies defined
- **Output:** `PROJECT-PLAN.md` document with:
  - Task breakdown (what, who, when, dependencies)
  - SOP (Standard Operating Procedure for the build)
  - Risk mitigation (for each known blocker)
  - Test criteria (how we'll validate each phase)
  - **Agreement from Cem that plan is executable**

**Duration:** 1-2 hours (mostly Ava work, brief Cem sync)

---

#### **Phase 3: BUILD** ← Execute the plan

**What happens:**
- Spawn agents (Codex, Forge, Harry, etc.)
- Build, iterate, log progress
- **Output:** Working code, scripts, dashboards, infrastructure

**Duration:** Days to weeks depending on scope

**Note:** Use crons for background work, subagents for parallel builds, never burn Anthropic tokens on background jobs (use free models)

---

#### **Phase 4: TEST & REFINE** ← Validate + iterate

**What happens:**
- Run test suite (automated)
- Manual validation by Cem
- Log issues, iterate
- Once stable: go-live

**Duration:** 1-5 days depending on complexity

---

### How Ava Operates

1. **Cem says "I want to [idea]."**
   → Ava enters SHAPING phase
   → Reads MEMORY.md + Vault for context
   → Asks clarifying questions
   → Identifies edge cases
   → Uses Advisor tool for architecture review
   → Creates `PROJECT-SHAPE.md`

2. **Ava says "Shaping complete. Ready to plan?"**
   → Cem reviews shape
   → If gaps: "Let's discuss [topic] more"
   → If ready: "Move to planning"

3. **Cem says "Move to planning"**
   → Ava creates `PROJECT-PLAN.md`
   → Breaks into tasks + timeline
   → Assigns owners (Codex, Forge, etc.)
   → Gets Cem sign-off

4. **Cem says "Let's build"**
   → Ava spawns agents
   → Monitors progress
   → Delivers working code

5. **Testing happens**
   → Cem validates
   → Issues logged + fixed
   → Go-live when stable

---

### Template: PROJECT-SHAPE.md

```markdown
# Project Shape: [Project Name]
Date: YYYY-MM-DD | Owner: Ava | Status: SHAPING IN PROGRESS

## Problem Statement
[Clear 1-2 sentence description of what we're solving]

## Scope
IN SCOPE:
- [What we're building]
- [What we're fixing]

OUT OF SCOPE:
- [What we're NOT doing]

## Edge Cases Identified
1. [Edge case 1 + how we'll handle it]
2. [Edge case 2 + how we'll handle it]

## High-Level Architecture
[Layers, data flow, dependencies]

## Success Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

## Dependencies / Blockers
- [Blocker 1]: Owner, impact
- [Blocker 2]: Owner, impact

## Notes
[Any open questions or discussion items]

---
SHAPING SIGN-OFF:
- [ ] Cem reviewed and approved
- [ ] Ready to move to planning
```

---

### Template: PROJECT-PLAN.md

```markdown
# Project Plan: [Project Name]
Date: YYYY-MM-DD | Owner: Ava | Status: PLANNING

## Reference Shape Document
`PROJECT-SHAPE.md` (linked above)

## Task Breakdown
| Task | Owner | Duration | Dependencies | Status |
|------|-------|----------|--------------|--------|
| Task 1 | Codex | 2 days | None | Ready |
| Task 2 | Forge | 3 days | Task 1 | Blocked |

## Standard Operating Procedure (SOP)
[Step-by-step guide for execution]

## Risk Mitigation
For each blocker from SHAPE:
- [Blocker]: If this fails, fallback is [X]

## Test Criteria
1. [Test 1]: [How to validate]
2. [Test 2]: [How to validate]

---
PLAN SIGN-OFF:
- [ ] Cem reviewed and approved
- [ ] Ready to build
```

---

### When to Use Advisor Tool

**During SHAPING:**
- Architecture decisions (single service vs multiple?)
- Data model design (SQLite vs API vs hybrid?)
- Risk assessment (what could go wrong?)
- Timeline estimates (realistic?)
- Dependency analysis (what could block us?)

**During PLANNING:**
- Task prioritization (what's critical path?)
- Fallback strategies (what if X fails?)

**NOT during BUILD:** Build is execution. Advisors slow it down.

---

### Red Flags (Stop and Reshape)

If any of these happen DURING BUILD, go back to SHAPING:
- Unknown edge case discovered
- Architecture doesn't fit the problem
- Major dependency shifts
- Timeline slipped >20%
- Scope creep ("while we're at it...")

**NEVER PUSH FORWARD without reshaping.** It's cheaper to reshape early than to rebuild halfway through.

---

### Memory Integration

Whenever starting a new project or revisiting one:

1. **Search MEMORY.md:** What have we tried before? What worked? What didn't?
2. **Search Vault:** Are there existing docs/SOPs we can leverage?
3. **Ask Cem:** "I found [X] in memory. Is this still relevant?"
4. **Update MEMORY.md:** After shaping is done, capture decisions + learnings

Goal: Avoid repeating mistakes. Compound on successes.

---

**Established:** 2026-04-11 | **By:** Cem (approved) | **Effect:** All projects from this date forward follow this framework
