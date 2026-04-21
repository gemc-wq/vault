# MEMORY.md - Ava Long-Term Memory (merged 2026-02-28)

> Merged from pre-migration clawdbot workspace + active OpenClaw workspace.
> Rich historical context restored from original clawdbot workspace.


---

## 🏗️ MASTER ARCHITECTURE - Listing Automation Engine

> **This is the North Star. Every project feeds into this. Read this section FIRST every session.**
> **Source:** Cem's Master Business Process Blueprint (Feb 8) + wiki/17-harry-workspace/projects/ai-coo/BLUEPRINT.md
> **Updated:** 2026-03-21

### The Big Idea
SKU = Content. The SKU structure (`PRODUCT_TYPE-DEVICE-DESIGN-VARIANT`) contains all the information needed to generate a complete listing. Content is assembled on-the-fly from component templates, not written per-SKU.

### Component Template Model
- HTPCR (fixed) → "Hybrid MagSafe Case - TPU bumper + PC hard back, MagSafe compatible, military grade..."
- IPH17PMAX (fixed) → "Apple iPhone 17 Pro Max"
- NARUICO (variable) → "Naruto Shippuden" + "Akatsuki" + license-specific hero copy
- **Only the design code is variable.** Product type features and device specs are reusable across ALL SKUs.

### End-to-End Pipeline (5 Phases)
1. **IDEATION** → PULSE best sellers + Social Intelligence Scout (X/Apify) → identifies what to sell/create
2. **PRODUCT DEV** → Design team creates artwork, AI generates content from SKU templates (parallel: images + copy)
3. **QA** → Sven reviews images, Echo reviews copy → approval gate
4. **GO LIVE** → Lister tool pushes to marketplaces via API (Walmart, OnBuy, Kaufland, Shopify)
5. **MONITOR** → PULSE tracks velocity, Conversion Dashboard tracks performance → feeds back to Phase 1

### Current Tools Built
- PULSE Dashboard ✅ | Conversion Dashboard ✅ | Walmart Lister ✅ | SKU Parsing Rules ✅
- SEO Content Framework ✅ | Local SQLite DB ✅ (US 3.44M + UK 5.1M rows) | EAN Assignment Engine ✅
- BigCommerce API ✅ | BQ Orders Sync ✅ (nightly cron) | ASIN→SKU Bridge ✅ (3.43M)
- **Weekly Listing Intelligence ✅** (Mar 21) - automated audit pipeline, delta tracking, HB401 gap analysis
  - Scripts: `refresh_listings.py`, `weekly_listing_audit.py`
  - Posts sanitized summaries to Slack #eod-listings (no revenue)
  - Blueprint: `wiki/17-harry-workspace/projects/ai-coo/BLUEPRINT.md`

### Marketplace Status (updated Mar 28)
- Amazon US/UK: LIVE (via Zero) | Walmart: STAGING (3,555 products, CSV ready - API item creation failing; Cem subscribed to Codisto/Shopify Marketplace Connect Mar 27)
- GoHeadCase Shopify: LIVE (orders flowing — up to #1124+ by Mar 24, includes WWE desk mats) | OnBuy UK: PLANNED (Apr) | Kaufland DE: PLANNED (May)
- Target Plus: LIVE VIA SHOPIFY (discovered Mar 23 — all Shopify orders = Target Plus, 29 orders in 4 days. Shopify = distribution hub for Target)
- TikTok Shop: ACTIVE (clean health score)
- **Walmart catalog:** 4.02M existing items (old Zero integration). New item creation blocked — Codisto may be the path forward.

### Walmart API: Keys in Harry's .env (iMac) - WALMART_API_KEY + WALMART_CLIENT_SECRET - confirmed working Mar 3
### Walmart Variant Structure: variantGroupId + Compatible Model + Case Type (up to 3 attributes)

### Image Automation = #1 bottleneck. Ecell Studio / Sven pipeline = AI mockup rendering. Once solved: <1 min per SKU.

### Champion Selection Methodology (Cem directive, Mar 19)
- **Champions = Combined Back Case Revenue** (HTPCR + HC + HB401, FBA merged)
- HTPCR is the staple product; HB401 is newer with limited range; HC is phasing out
- ALL THREE contribute to identifying which designs are top sellers
- Combined elbow (80%): **590 designs** = $352K of $440K total US back case revenue
- This is the DEFINITIVE champion list for Walmart, Shopify, and all marketplace expansion
- HTPCR listed for all champions; HB401 added only where it exists on Amazon (images available)
- HC NOT listed on new marketplaces (phasing out) but included in analysis for design demand signal
- Gap tracker: `projects/sku-staging/hb401_gap_tracker.json` - tracks which champions need HB401 images
- As PH creative team produces HB401 images, variants are auto-added to Shopify via API
- **Never use HTPCR-only data for champion selection - always combine all back case types**


### Procurement System (specced Mar 20)
- Split logic: demand-based (7-day velocity by buyer country) - US→FL, UK/ROW→UK, JP→PH
- Separate POs per destination, ~1 run/week, 12-16 POs/month
- Source of truth for cost = last PO price (NOT t_mfg_supplier_price)
- Supplier currencies confirmed: RMB (ECELLSZ, XINTAI, YIZE, SHENG, JIZHAN, QICAI), USD (SAIBORO, BAOLLY, TOKO, SANXING)
- HTPCR ¥3.50 | HB401 ¥6.50 | HB6/HB7 $1.90 | HLBWH Phone ¥7 | HDMWH 900×400 $1.76
- Spec: `projects/procurement/PROCUREMENT_SYSTEM_SPEC.md`


### Delegait — AI SaaS Spin-Off (founded Mar 24)
- **Name:** Delegait (Deleg-AI-t) — "Delegate + AI" hidden in the word
- **Tagline:** "The AI that works for you"
- **Domains to register:** delegait.ai + delegait.com (verified available Mar 24)
- **Target:** AI-confused SMBs who want rapid deployment + quick gains
- **Two revenue streams:** Delegait Platform (SaaS $299-2,499/mo) + Delegait Advisory (consultancy $5K-25K)
- **Customer #1:** Ecell Global (proven on $5M+ revenue before external launch)
- **NemoClaw:** NVIDIA NIM on OpenClaw — all inference runs locally, zero per-token cost
- **NemoClaw installed:** Mar 25 — confirmed active (~20 min setup per Cem)
- **Differentiation:** Only platform combining velocity intelligence + AI content generation + multi-marketplace automation, battle-tested on real business
- **Strategy:** Start vertical (e-commerce), brand horizontal → pivoted to SaaS + ProServ verticals
- **Trademark:** File ITU with USPTO — Class 42 (SaaS) + Class 35 (consulting)
- **Social:** Lock @delegait on X, LinkedIn, Instagram
- **Full naming session log:** memory/2026-03-24.md
- **Specs saved:** `projects/delegait/` directory:
  - `DELEGAIT_STARTER_PACK_SPEC.md` — 6-module "Business in a Box" (Storefront, Outreach, CRM, Booking, Admin/Payments, Weekly Intelligence)
  - `LAUNCH_PLAYBOOK.md` — Week 1-4 zero-employee launch strategy (dogfooding)
  - `VERTICALS.md` — SaaS + ProServ dual-vertical with 80% shared core
- **Pricing:** Launch $299/mo, Growth $799/mo, Scale $1,499/mo, Done For You $2,500/mo
- **ICP:** ProServ 2-20 employees, Orlando metro + remote, $500K-$5M revenue
- **First 3 clients target:** "AI Quick Win" — $2,500 one-time + $299/mo, delivered in 5 days
- **10 clients = $36K ARR minimum** (Launch tier), $96K ARR (Growth tier)

### Cem's Personal Mission (Mar 21 directive)
- **AI SaaS spin-off business** - productize the tools we build into a marketplace operations platform
- Everything built for Ecell Global (PULSE, Conversion Dashboard, Listings Management, Pricing Optimizer) = battle-tested SaaS candidates
- Customer #1 = Ecell Global. Product proven on $5M+ revenue business before selling externally
- Target market: licensed product sellers, multi-SKU marketplace sellers
- **Add to every project:** "Is this generalizable? Could this be a SaaS feature?"

### Key Business Data Points (Mar 21)
- **Shipping charges:** $6.99 standard, $10.99 2-day - impacts conversion (total cost $27-31 vs $19.95 product price)
- **Amazon category avg conversion:** 1.5% for phone cases (from Amazon account manager)
- **Category trend:** Down 0.85% month-over-month (site-wide)
- **Benchmark:** Our conversion above 1.5% = outperforming category despite absolute numbers looking low
- **Pricing consideration:** Test free shipping at higher product price vs current model


### Weekly Listing Intelligence (built Mar 21)
- **Weekly gap analysis pipeline:** Champions × Active Listings → gap list → Slack #listings
- **14-day attribution:** match new listings by open_date to sessions report 2 weeks later
- **Conversion baselines:** wiki/25-pulse-dashboard/CONVERSION_BASELINES.md
- **US 30d baseline:** 2.89% conversion, $178.6K revenue, 276K sessions
- **Key finding: HB401 converts 4x higher than HTPCR** (12.46% vs 2.96% on 30d US baseline)
- **Key finding: Best sellers ≠ best converters** - zero overlap top 10 by revenue vs top 10 by conversion
- **Dynamic pricing candidates:** 30 Stars (price up), 13 Q-Marks (price down), 7 Cash Cows (PPC boost)
- **Spec:** projects/LISTINGS_MANAGEMENT_SYSTEM_SPEC.md
### Key Principle: Don't store content per SKU. Generate it. 30 content blocks serve 200K+ SKUs.
### Key Reference: wiki/SKU_PARSING_RULES.md | projects/sku-staging/SEO_CONTENT_FRAMEWORK.md | projects/sku-staging/MARKETPLACE_EXPANSION_PLAN.md

## 🤖 CRON & HEARTBEAT MODEL POLICY (established 2026-03-30)

**Rule: All crons and heartbeats must run on FREE models only. Never burn Anthropic tokens on background jobs.**

### Approved cron/heartbeat models (in order of preference):
1. **`pixel` agent** (`google/gemini-3-flash-preview`) — primary cron executor, free via Gemini API
2. **`bolt` agent** (`google/gemini-3.1-pro-preview`) — for heavier cron tasks needing more reasoning
3. **`openai-codex/gpt-5.4`** — available via ChatGPT OAuth (free subscription tier)
4. **`moonshot/kimi-k2-0905-preview`** — Kimi K2.5, free tier, good for analysis crons

### Never assign crons to:
- `main` (Ava = Sonnet 4.6 = Anthropic API = $$$)
- `anthropic/claude-opus-4-6` or `anthropic/claude-sonnet-4-6` (paid)

### Why this matters:
- Cem hit Anthropic rate limits Mar 30 from cron abuse
- Switched Ava from Opus → Sonnet to reduce cost
- Background jobs (data syncs, health checks, file detections) don't need frontier models
- Zero Apache crash (Mar 29) reinforced: background infra must be independent of main session

### Heartbeat:
- Already configured: `heartbeat.model = google/gemini-3-flash-preview` ✅

### Cron audit (Mar 30):
- BQ→Supabase Orders Sync → moved to `pixel` ✅
- Data Freshness Check → moved to `pixel` ✅
- Zero Cron Health Check → moved to `pixel` ✅
- Blocked Tasks Reminder → moved to `pixel` ✅
- Daily EOD Memory Summary → already on `bolt` ✅
- Weekly Velocity Sat/Sun → on `pixel` with Flash model ✅
- Remaining on `main` (intentionally, too complex for Flash): Slack Daily Digest, Weekly PULSE Leaderboard, Friday Reminder, Weekly Memory Review, Security Audit, HB401 Sprint Check

## === HISTORICAL CONTEXT (original clawdbot workspace) ===

# MEMORY.md - Long-Term Memory

## Origin
- **Born:** 2026-02-06
- **Named by:** Cem
- **Name:** Ava
- **Role:** Head of Sales & Marketing (promoted 2026-02-17, was Lead Strategist)
- **First session:** Telegram, morning

## About Cem
- Timezone: EST (America/New_York)
- CEO & Co-Founder of Ecell Global - tech accessories manufacturer (phone cases, skins, etc.)
- B.Eng in Chemical Engineering
- Licensed brands: NFL, NBA, WWE, Harry Potter, Peanuts, Naruto, Dragon Ball Z, DC Comics, etc.
- Family business: 3 brothers - Tim (started 2000), Cem (CEO, joined 2005), Murat (Director, joined 2005)
- Private company, est. 2005 (UK), 2012 (US)
- 8M+ cases sold, 500+ devices supported
- Manufacturing: USA, UK, Philippines (Just-in-Time, cleanroom facilities)
- Offices: USA (Orlando, LA), UK, Japan, Hong Kong, Philippines
- Retail brand: Head Case Designs - top 10 global eBay seller
- Uses **Coo Blueprint** for project management (replaced Orbit PM as of 2026-03-25)
- Slogan: "We Got You Covered"

## Organisation
- **Cem** - CEO, Human-in-the-Loop
- **Harry** - Openclaw, Finance, runs on Cem's iMac (cems-imac, Tailscale 100.91.149.92)
- **Ava (me)** - Head of Strategy, Claude Haiku 4.5, runs on Cem's Mac Studio (cems-mac-studio, Tailscale 100.72.19.27)
- Shared Google Drive: `Clawdbot Shared Folder` (rclone `gdrive:`)
- Brain folder: `gdrive:Clawdbot Shared Folder/Brain/` - source of truth for all projects
- Harry communication: `collaboration/` folder on shared drive
- 13 total agents across both teams

## Model Stack (updated 2026-02-17)
| Role | Model | Cost |
|------|-------|------|
| Ava (me) | Claude Sonnet 4.6 | API |
| Harry | Claude Sonnet 4.6 | API |
| Echo (copy) | Claude Sonnet 4.6 | API |
| Iris (design) | Gemini Nano Banana Pro | Gemini CLI OAuth |
| Loom/Bolt (research/scout) | Gemini Flash | API/OAuth |
| Atlas/Prism (analysis) | Kimi K2.5 | CHEAP |
| Forge/Spark/Nexus (coding) | Codex CLI GPT-5.3 | FREE (ChatGPT OAuth) |
| Pixel/Radar (merchant/scout) | Gemini Flash | API |

- web-builder Clawdbot agent: openai-codex/gpt-5.4 (primary), Codex CLI defaults to 5.4
- Codex CLI v0.98.0 at /opt/homebrew/bin/codex - logged in via ChatGPT OAuth ✅

## My Team (Sales, Marketing & Creative) - 8+ agents
- **Echo** - Copywriter (Sonnet 4.6) - web copy, Amazon listings, ad copy
- **Iris** - Designer (Gemini Nano Banana Pro, OAuth) - visuals, mockups, assets
- **Loom** - Researcher (Gemini Flash) - competitor intel, market research
- **Bolt** - Scout (Gemini Flash) - SEO keywords, quick lookups
- **Atlas** - Analyst (Gemini 3.1 Pro) - ecommerce analytics, revenue analysis, opportunity scoring
- **Pixel** - Data Processor (Gemini 2.5 Flash) - ETL, file parsing, Supabase loads (added 2026-03-07)
- **Sven** - Creative Design & RAG Corpus (Gemini 3.1 Pro) - design corpus completion, creative design work (runs as sub-agent under Ava)
- **Forge** - Web Builder (Codex CLI GPT-5.3, FREE) - Next.js builds
- **Spark** - Builder 2 (Codex CLI GPT-5.3, FREE) - deep code, architecture
- **Flux** - DevOps (Gemini Flash) - Vercel deploys, CI/CD


## Active Projects
- **ecellglobal.com Redesign** - B2B marketing site (Vite/React + Tailwind) deployed on Vercel.
  - Vercel project: `ecell-site` (org: Ecell's projects)
  - Latest prod deploy (example): https://ecell-site-h8h8ljwb9-ecells-projects-3c3b03d7.vercel.app
  - Domain cutover in progress: `ecellglobal.com` + `www.ecellglobal.com` added to Vercel; Cloudflare DNS needs A root → 76.76.21.21 and CNAME www → cname.vercel-dns.com (DNS only).
  - Local: `projects/ecell-website/ecell-site/`

- **GoHeadCase POC / Template** - Casetify/OtterBox-grade licensed-first template + microsite/universe landing system.
  - Strategy/Mission: Brain/Projects/goheadcase/strategy/goheadcase-mission-ux-council.md
  - Asset Plan v1: Brain/Projects/goheadcase/asset-plan/GOHEADCASE_ASSET_PLAN_V1.md
  - RAG schema: Brain/Projects/goheadcase/rag/ECOM_EXPERT_RAG_SCHEMA.md
  - Benchmark captures started: Brain/Projects/goheadcase/rag/benchmarks/casetify/live/2026-02-21/
  - BigCommerce stencil code export: Brain/Projects/goheadcase/goheadcaseBigCommerceCode2025/
  - AI Studio repo clone: https://github.com/gemc-wq/goheadcase.git (local: /Users/clawdbot/clawd/projects/goheadcase-ai-studio)

- **Email Triage + Email Memory (READ ONLY)**
  - Spec: Brain/Projects/email-triage/email-triage-project.md
  - Schema: Brain/Projects/email-triage/email_memory_schema.sql
  - n8n workflow outline: Brain/Projects/email-triage/n8n_email_triage_workflow_v1.md
  - Plan: new Supabase project `email-memory` + pgvector; ingest Inbox+Sent read-only; daily digests + drafts.

- ~~**Orbit PM**~~ - **RETIRED 2026-03-25. Replaced by Coo Blueprint.**

- **New Products: Water Bottles + Wall Art** — SKU structure defined (`projects/new-products/SKU_STRUCTURE.md`). Creative briefs + Gamma deck posted to #creative Mar 23. Awaiting Cem approval on SKU codes, EAN allocation, PH team capacity. Target: Amazon live ~Apr 1.

- **Delegait** — AI SaaS spin-off. Full specs saved Mar 24-25. NemoClaw (NVIDIA NIM) confirmed active Mar 25. Execution mode — Week 1 tasks pending Cem's go-ahead.

## Nightly Cron Tasks
> ⚠️ **STATUS: Needs rethink (Cem directive 2026-03-25).** The crons below are from the original clawdbot setup and are NO LONGER RUNNING. The current live cron schedule is in the OpenClaw cron system. We need to decide what nightly automation is actually valuable before rebuilding.
- ~~**2:00 AM** - Nightly mission task (Mon=Market Intel, Tue=Audit, etc.) - DEAD, not running~~
- ~~**3:00 AM** - Daily trends pipeline (CSV + Gamma slides → Telegram) - DEAD, not running~~
- ~~**6:00 AM** - Morning audio brief (TTS → Telegram) - DEAD, not running~~

## Key Decisions Log
*(Recent first. See daily memory logs for full context.)*

### Mar 27 - HB401 Sprint Day 7 + Jay Mark Zero 2.0 Plan + Fulfillment Portal
- **HB401 creative team fully active:** Jeffrey completed HPOTDH37, Chadle listed sports designs for IPH12/IPH13, Danica re-replicated 88,176 SKUs. PNUTHAL/PNUTCHA still unconfirmed. - [memory/2026-03-27.md]
- **Jay Mark Zero 2.0 plan solidified:** FastAPI + React, Phase 1 = Evri Label Portal (standalone), Phase 2 = Order Dashboard scaffold. Amazon SP-API 75% done. Needs BQ credentials to unblock. - [memory/2026-03-27.md]
- **Cem subscribed to Shopify Marketplace Connect (Codisto)** for Walmart channel. Wants web app, not local extension. - [memory/2026-03-27.md]
- **NBCU PO acknowledged by Cem** — PO 3400799538 at 1:52 PM (was pending 3 days). - [memory/2026-03-27.md]
- **Target Plus auto-import:** Jay Mark scraped 25,866 unique SKUs from partner portal. - [memory/2026-03-27.md]
- **Carrier status clarified:** Evri CSV upload working (no API), Royal Mail = click-and-drop only (no API), USPS/FedEx via Stamps.com. - [memory/2026-03-27.md]

### Mar 25-26 - NemoClaw Active + Delegait Fully Specced + HB401 Breakthrough
- **NemoClaw installed and active** — OpenClaw on NVIDIA NIM, zero per-token cost inference. Backbone for Delegait. - [memory/2026-03-25.md]
- **Delegait full spec captured** to `projects/delegait/`: Starter Pack (6 modules), Launch Playbook, Verticals (SaaS + ProServ). - [memory/2026-03-25.md]
- **Supabase RLS security breach identified** — remediation spec at `projects/supabase-rls-fix/RLS_REMEDIATION.md`. - [memory/2026-03-25.md]
- **HB401 Day 6 breakthrough:** Patricia uploaded 16 combos after 5 days of zero progress. - [memory/2026-03-26.md]
- **NFL revenue snapshot:** $23,219 YTD / ~$97K annualized — renewal at $25K/yr is no-brainer. - [memory/2026-03-26.md]
- **Memory maintenance performed:** MEMORY.md updated with sprint status, license alerts, project refreshes. - [memory/2026-03-26.md]

### Mar 24 - Delegait Naming + Cem's Pipeline Vision + Sven Unblocked
- **Delegait (Deleg-AI-t) selected** as AI SaaS spin-off name. Domains delegait.ai + delegait.com likely available. - [memory/2026-03-24.md]
- **Cem's unified pipeline vision:** Single entry → auto-generate images + content → listings ready in minutes. Aligns with Master Architecture. - [memory/2026-03-24.md]
- **Sven image gen blocker RESOLVED:** `image_generate` tool available (Gemini 3.1 Flash Image + OpenAI GPT-Image-1). Supports editing with up to 5 reference images. - [memory/2026-03-24.md]
- **Naruto UK marketing opportunity:** Part I (220 episodes) now free on BBC iPlayer. Brief created at `projects/marketing/NARUTO_UK_IPLAYER_OPPORTUNITY.md`. - [memory/2026-03-24.md]

### Mar 23 - New Product Lines (Water Bottles + Wall Art) + Shopify→Target Plus Discovery
- **Two new product categories approved:** MagSafe Water Bottles + Aluminium Metal Wall Art. In-house printing (UV DTF, UV Flatbed, Laser). No external suppliers needed for v1. - [memory/2026-03-23.md]
- **ZERO competitors** have licensed designs on MagSafe bottles or licensed PL metal wall art on Amazon. Displate ($277M GMV) is DTC only. - [memory/2026-03-23.md]
- **Shopify orders are ALL from Target Plus** — 29 orders in 4 days (~$580). Shopify is the distribution hub for Target. Every product added auto-flows to Target. - [memory/2026-03-23.md]
- **Full creative package created:** CREATIVE_STANDARDS.md, CONTENT_RESEARCH_GUIDE.md, STYLE_GUIDE_BRIEF.md, AI_IMAGE_PROMPTS.md + Gamma deck. Posted to #creative. - [memory/2026-03-23.md]
- **Additional licenses spotted:** LFC and WWE printed bottles received (beyond initial Man City, Spurs, WB). Full license list needs confirmation. - [memory/2026-03-23.md]
- **CAA Sports intro:** Laney Steed (new day-to-day for global soccer licensing). Opportunity for World Cup prep. - [memory/2026-03-23.md]
- **Walmart API still blocked** on item creation. Excel file sent to Cem for manual Seller Center test. - [memory/2026-03-23.md]

### Mar 21 - Weekly Listing Intelligence Pipeline + HB401 Sprint
- **Built full weekly audit pipeline:** Active Listings delta DB + Child ASIN enrichment + Slack EOD cross-ref + automated Slack posting
- **Key insight: HB401 converts 4x higher than HTPCR** (12.46% vs 2.96% on 30d US baseline) - validated across all devices
- **US 30d CVR 2.89%** - above 1.5% category avg. 7d dip to 1.47% was Iran war + winter storms, not structural
- **UK 30d CVR 2.54%** - US actually outperforms UK despite UK having free SFP next-day delivery
- **HB6+HB7 underperforming** - 2.74% US, 1.35% UK. Not justifying shelf space
- **HB401 Sprint assigned from Cem:** 31 device×design combos, 20 champion designs, iPhone 13 = #1 gap. New upgraded images required.
- **Posted to Slack:** US weekly summary, US vs UK intel, HB401 gap analysis + task list, project assignment from Cem
- **Shipping analysis:** Recommended NOT cutting shipping - US CVR healthy. A/B test 20 SKUs at $4.99 first.
- **Project added to COO Blueprint:** `wiki/17-harry-workspace/projects/ai-coo/BLUEPRINT.md`
- **Follow-up cron:** Mar 28 to verify sprint completion via delta - [memory/2026-03-21.md]

### Mar 20 - Walmart API Blocked + First Shopify Order + Zero 2.0 Assessment
- **FIRST SHOPIFY ORDER (#1083):** PNUTCHA (Peanuts) $19.95 - validates store, data, checkout. PULSE's #1 design. - [memory/2026-03-20.md]
- **Walmart API item creation FAILS** on both credential sets. Inline JSON → "glitch", file upload → stuck RECEIVED. Old items uploaded via Zero integration. - [memory/2026-03-20.md]
- **Feedonomics/Target Plus officially DEAD** - cancelled Mar 20, tickets closed. Shopify-hub strategy validated. - [memory/2026-03-20.md]
- **🔴 Anthropic API out of credits** - affects Echo + agent operations. Flagged to Cem. - [memory/2026-03-20.md]
- **🔴 AWS $2,570.85 past due** - services at risk. Flagged to Cem. - [memory/2026-03-20.md]
- **Zero 2.0 staff automation map:** 38 PH staff → ~17 post-automation (55% cut, ~$102K/yr savings). 3 phases over 12 months. - [memory/2026-03-20.md]
- **QMD memory backend installed** (v2.0.1, Tobi Lütke/Shopify) - config patched, handoff to Harry. - [memory/2026-03-20.md]
- **Dragon Ball Goku pushed to Shopify** (Product ID 10074058916138, 30 variants). - [memory/2026-03-20.md]
- **Wiki section 30 created:** `wiki/30-zero-2/` with system summary, build plan, staff automation map. - [memory/2026-03-20.md]

### Mar 19 - Product Architecture Finalized + Five PULSE Tracks + Procurement Spec
- **Five PULSE analysis tracks defined (Cem directive):** Back Cases, Leather Wallets, Desk Mats, Gaming, Laptop. Each has distinct marketplace category + variant structure. - [memory/2026-03-19.md]
- **HTPCR+HB401 paired, HB6+HB7 paired, HLBWH standalone.** HC phasing out (analysis only). - [memory/2026-03-19.md]
- **Combined back case champion list = 590 designs** ($352K of $440K, 80% elbow). DEFINITIVE for all marketplaces. - [memory/2026-03-19.md]
- **HB401 gap tracker created** - 2,231 device×design combos need images. Posted to Slack #creative + #graphics. - [memory/2026-03-19.md]
- **Procurement system specced** - demand-based split (7-day velocity by buyer country), supplier costs confirmed by Cem. - [memory/2026-03-19.md]
- **BQ sync gap found + fixed:** Supabase missing ~50% orders since Mar 12 (cron ran before BQ ingestion). Backfilled 3,840 rows, cron moved to 3 AM. - [memory/2026-03-19.md]
- **Telegram group configured** for "cem & Ava, Harry" (-1003832582809). - [memory/2026-03-19.md]

### Mar 18 - Shopify API Connected + EAN Engine + Walmart Variants
- **Shopify API live:** Store yabfxs-zd, token shpat_4a41..., scope write_products+write_inventory. - [memory/2026-03-18.md]
- **Sample products pushed:** Naruto Akatsuki (iPhone 45 variants, Samsung 15 variants) - published on store. - [memory/2026-03-18.md]
- **EAN Assignment Engine:** Auto-assigned 7,353 EANs from unassigned pool. Total lookup 480K. Remaining pool 44K. - [memory/2026-03-18.md]
- **Pricing confirmed (tiered):** HTPCR $19.95, HB401 $19.95, HLBWH/HB6/HB7 $24.95. - [memory/2026-03-18.md, corrected 2026-03-25]
- **S3 CDN image rules documented:** elcellonline.com/atg/{DESIGN}/{VARIANT}/{PREFIX}-{DEVICE}-{POS}.jpg. Only position 1 on S3. - [memory/2026-03-18.md]
- **Harry switched to Sonnet 4.6** - much more productive (was GPT-5.4). - [memory/2026-03-18.md]
- **Walmart variant structure confirmed:** Parent=Design, Variants=Device+CaseType, variantGroupId=HCD-{DESIGN}. - [memory/2026-03-18.md]
- **Wiki expanded:** 5 new sections (24-28), contradiction audit completed. - [memory/2026-03-18.md]

### Mar 17 - Walmart CSVs Final + ecell.app Updated + PULSE Elbow
- **3,555 Walmart products generated:** HTPCR 2,806 + HB401 605 + Desk Mats 144. All 100% EAN. Cem approved. - [memory/2026-03-17.md]
- **PULSE elbow analysis:** 183 designs × 31 devices × ~2.7 types = 15,317 optimal variants. Cem confirmed as definitive matrix. - [memory/2026-03-17.md]
- **ecell.app updated** with PULSE + Conversion + PRUNE tiles. Deployed revision 00030 on Cloud Run. - [memory/2026-03-17.md]
- **HTPCR spec corrected in all content:** "Hybrid MagSafe Case" (TPU+PC+MagSafe ring), NOT "Soft Gel Case". - [memory/2026-03-17.md]
- **iMac SSH confirmed:** user=clawdbot, gemc99-boop token for GitHub. - [memory/2026-03-17.md]

### Mar 15 - Scope Expansion to Full GoHeadCase Catalog + SEO Framework + OnBuy UK
- **Headless Shopify = new goheadcase.com** - smart subset of 1.9M BC catalog (<200K SKUs). ALL product groups. - [memory/2026-03-15.md]
- **SEO Content Framework created:** Title/description templates per case type. Echo rewrites BC raw content before upload. - [memory/2026-03-15.md]
- **Three Intelligence Layers identified (Cem):** Daily Analytics Bot + Opportunity Finder (coverage+development) + Social Intelligence Scout. - [memory/2026-03-15.md]
- **OnBuy UK analysis complete:** 700 champions, £400K rev, 98% EAN coverage. UK = football-dominated. - [memory/2026-03-15.md]
- **Local SQLite DB built:** 8.5M rows (US 3.4M + UK 5.1M), sub-ms query speed. - [memory/2026-03-15.md]
- **Device code map expanded to 182 devices** from BigCommerce API crawl. - [memory/2026-03-15.md]
- **Amazon SP-API research dispatched** - need LWA creds + refresh token + seller ID. - [memory/2026-03-15.md]

### Mar 14 - SKU Staging Pipeline Built + Shopify CSV Generated
- **BigCommerce API connected:** Store hash `otle45p56l`, 1.87M SKUs, 950K HTPCR. Creds in TOOLS.md.
- **Target master list = EAN source:** 35,541 SKUs with EAN-13 barcodes. File: `data/ean/target_ean_lookup.json`
- **US champions: 58% have EANs (82% of revenue)** - gap is mostly US sports (IMGC, NHL, NBA)
- **Shopify product architecture decided:** Product = 1 design × 1 device, Variant = case type (HTPCR/HB401/HLBWH/HB6/HB7)
- **5 case types only (Cem directive):** HTPCR ($19.95), HB401 ($19.95), HLBWH ($24.95), HB6 ($24.95), HB7 ($24.95) - confirmed 2026-03-25
- **Shopify CSV generated:** Test (10 designs, 100 products) + Full (50 designs, 750 products). Sent to Cem for import test.
- **Casetify NOT on Shopify** - custom stack. OtterBox (Shopify Plus) is the right benchmark.
- **PULSE gap finder is correct** - compares top-200 sellers per region, not marketplace listings. Label needs update.
- **BC custom fields are gold for Shopify:** AmazonTitle, DesignName, BrandCode, DeviceModel, GenericKeywords, Price_US
- Scripts: `scripts/generate_shopify_csv.py`, output at `projects/sku-staging/output/`

### Mar 10 - PULSE Goes Live + Unified Product DB + Architecture Decisions
- **PULSE Dashboard v1 LIVE on real BQ data:** https://pulse-dashboard-inky.vercel.app - 200 velocity designs, 112 surging, $3.1M 90d rev. Top: PNUTCHA (Peanuts) $169K.
- **BQ ≠ Supabase schema lesson:** BQ `orders` has raw `Custom_Label` only; Supabase has pre-parsed `design_code`/`device_code`. Dashboard queries parse via `SPLIT(Custom_Label, '-')[SAFE_OFFSET(n)]`. CRITICAL to check target schema before writing queries.
- **Unified Product DB built in Supabase:** lineups (10,279), designs (110,634), product_types (146), devices (1,322), products (90,661), marketplace_listings (467,392). Schema: `projects/pulse-unified/UNIFIED_PRODUCT_DB_SPEC.md`
- **Key discovery:** `design_code` in orders = `LineupLabel` (99% match), NOT `DesignLabel`. Products table references lineups, not designs.
- **Supabase DB password obtained:** direct connection works, pooler doesn't.
- **Amazon conversion data loaded:** `amazon_conversion_data` table - 457K rows (US 160K, UK 153K, DE 144K) with sessions, page views, Buy Box %, conversion rates. Script: `scripts/enrich_business_reports.py`
- **ASIN→SKU bridge:** 3.4M mappings from US Active Listings. UK/DE match 80-85% using US bridge; need regional Active Listings files for 95%+.
- **Walmart gap analysis:** 750 design×product combos missing = $750K opportunity (6mo). Top missing brands: Peanuts ($73.6K), Newcastle ($45.8K), Naruto ($37.6K).
- **PULSE v4 spec finalized:** Regional filters (US/UK/EU), product group toggle (Phone Cases/Desk Mats & Skins), light theme, Supabase-backed. Target Mar 14. PULSE v2 repo: github.com/gemc-wq/pulse-dashboard-v2
- **Shopify-hub architecture confirmed:** PULSE identifies gaps → generates Shopify-ready data → connectors push to Walmart/Target+/OnBuy/Kaufland. NOT direct marketplace APIs.
- **Centralized Product DB source = BQ `headcase` dataset** (master tables: tblDesigns, tblLineups, tblDevices). Amazon/BC/Walmart are downstream.
- **License MG dropped to P1:** MG is 15% royalty on net sales, not fixed annual target. Less urgent than originally thought. Warner Bros renewed (not expired). NFL renewal still P0 ($25K/yr, expires Mar 31).
- **NFL renewal decision brief delivered:** RENEW recommended. $380K→$701K→$656K 3yr history. Rakuten Japan = 69% of NFL revenue ($517K). Break-even $250K at 10% royalty, doing 2-3x that.
- **Harry SOUL.md rewritten** to builder role. 5 tasks assigned (COGS due Mar 11, BQ sync audit, Chad file analysis, Shopify connector research, Zero PHP extraction).
- **Target+/Feedonomics DROPPED** as P0 - Shopify already set up, Veeqo handles orders. Non-issue.
- **Cem directive: "stop discussing, start building"** - fired research analyst agent (Gemini 3.1 Pro).
- **GitHub token:**  (gemc-wq, classic, repo scope)
- **Leaderboard analysis:** Top 50 lineups = 44.6% revenue. Hybrid top-50-lineup + top-300-design = 156 unique lineups covering 65%+. 106 "champion designs" from outside top 50 lineups add $390K.

### Mar 13 - BigCommerce API + SKU Staging + UPC Blocker
- **BigCommerce API connected:** Store otle45p56l, 1.87M SKUs, 950K HTPCR. Creds in TOOLS.md. - [memory/2026-03-13.md]
- **SKU Staging Pipeline launched:** 200 HTPCR champion designs from PULSE velocity data. Top: NARUICO ($57.8K), LFCLVBRD ($54K), AFCLOGOS ($42.6K). - [memory/2026-03-13.md]
- **UPC gap = #1 Walmart blocker:** Only 13.5% of champions have UPC/EAN. Need acquisition/generation plan. - [memory/2026-03-13.md]
- **Currency normalization complete:** 0 null `net_sale_usd` across 319K+ orders. Supabase backfill problem fully resolved. - [memory/2026-03-13.md]
- **RAG pattern cards 30/30 COMPLETE** (Sven sub-agent). Uploaded to Brain/Projects/goheadcase/rag/patterns/. - [memory/2026-03-13.md]
- **Zero PHP repo created:** `gemc-wq/zero-php` (private). Chad has credentials, needs repo access from Cem. - [memory/2026-03-13.md]
- **OnBuy seller onboarding:** Robert Jenkins reached out - new marketplace opportunity. - [memory/2026-03-13.md]
- **Harry: 4 tasks overdue, zero deliverables all week.** COGS (due Mar 11), Chad file + BQ audit (Mar 12), Shopify connector (Mar 13). Escalation needed Monday. - [memory/2026-03-13.md]

### Mar 12 - Orders Sync + Inventory Tracker + Infrastructure
- **BQ → Supabase orders sync built:** `scripts/sync_bq_orders.py` - delta sync, 14,661 rows backfilled (Feb 17 → Mar 12). Nightly cron 1 AM EST. - [memory/2026-03-12.md]
- **Google Workspace CLI (gws) installed:** v0.11.1, replaces `gog`. Read-only scopes (Drive, Gmail, Calendar). Drive 403 blocker resolved. - [memory/2026-03-12.md]
- **Inventory Tracker v1 built:** `blank_inventory` table + `v_inventory_alerts_v2` view. 5,193 active blank SKUs (PH 2,936, UK 2,502, FL 1,195). - [memory/2026-03-12.md]
- **77% of inventory SKUs are dead stock** (zero sales). Only 1,210 active, 513 high movers. - [memory/2026-03-12.md]
- **Sven confirmed as sub-agent under Ava** - iMac only has 8GB RAM, can't run another OpenClaw instance. - [memory/2026-03-12.md]
- **Research routing rule (Cem):** Simple research → Gemini Flash. Complex → Gemini Pro. - [memory/2026-03-12.md]
- **Harry inventory dashboard:** Builds procurement layer ON TOP of existing Supabase `blank_inventory` table. Ship target Mar 19. - [memory/2026-03-12.md]
- **Infrastructure corrected:** Harry runs on iMac (cems-imac), NOT VPS. Updated TOOLS.md. - [memory/2026-03-12.md]

### Mar 11 - PRUNE App + PULSE v2 Features + Google Stack Decision
- **PRUNE app built & deployed:** https://prune-app-xi.vercel.app - dead weight catalog analysis. 823 dead designs (252K listings, $15K fees on $0), 66 dead devices. 2 days ahead of schedule. - [memory/2026-03-11.md]
- **PULSE v2 dashboard fixed & enhanced:** RLS timeout fix (service_role key), device-first leaderboard, elbow detection auto-selector, tabbed layout (Devices | Design Groups | Champions). - [memory/2026-03-11.md]
- **Architecture decision: Google Stack for PULSE production.** BQ + Cloud Run (same network, sub-100ms). Supabase = stepping stone, not production. - [memory/2026-03-11.md]
- **Mission statement deployed** to ecellglobal.com + ecell.app (Sales Dashboard V2). - [memory/2026-03-11.md]
- **Champions insight (Cem):** Listings strategy should prioritize individual child designs, not spray all variants of a top lineup. - [memory/2026-03-11.md]
- **Miku renewal contract overdue:** Max Arguile following up. Contract sent Mar 2, Cem said "I'll review shortly" 9 days ago. - [memory/2026-03-11.md]
- **UK Amazon Active Listings available:** 9.4GB on GDrive. Unblocks UK ASIN→SKU bridge (currently 80-85% match). - [memory/2026-03-11.md]

### Mar 9 - PULSE Launch & License Discovery
- **PIE renamed to PULSE** (Product Uplift & Listing Signal Engine) - velocity-triggered opportunity identifier
- **PULSE v3.1 scope finalized** - 6 alert types (LIST/COMPLETE/BUILD/FIX/BOOST/RETIRE), license obligation layer, closed-loop tracking, device lifecycle normalization
- **License obligations discovered:** 37 licenses with MG advances. Real Madrid at 15% target pace ($612/mo vs $4,167/mo needed), NBA at 49% ($4,103/mo vs $8,333/mo). These are P0 priorities.
- **Royalty Advance file:** `data/Royalty_Advance_summary.xlsx` - all MG amounts, terms, currencies
- **Real Madrid MG:** $50K/yr started Jun 2025 (NOT in original spreadsheet, Cem provided separately)
- **NFL renewal:** Offered at $25K/yr. West Ham, Dragon Ball renewals in process.
- **First PULSE velocity run:** 154 surging + 146 accelerating designs from 2.8M BQ orders
- **Priority brief generated:** `results/PULSE_PRIORITY_BRIEF_2026-03-10.md` for PH listings team
- **PULSE Dashboard scaffolded:** `projects/pulse-dashboard/` - Next.js 16, 8 pages, 6 API routes, mock data, clean build
- **Amazon data on Mac Studio:** Active Listings 3.44M (6.4GB) + Child ASIN Report 80K - both at `data/amazon/`
- **BQ query gotchas:** Net_Sale is STRING (use SAFE_CAST), no pre-parsed design_code (parse from Custom_Label), column names are PascalCase (Custom_Label, Net_Sale, Paid_Date)
- **LLM Council review accepted:** 6-action model, closed-loop tracking Phase 1, device lifecycle normalization, licensing as first-class entity. Rejected: profit optimization (margins similar), FBA (POD), SP-API (premature)

### Mar 7 - Infrastructure Day
- **4-Pillar Strategy approved** - Sales → Production → Operations → Growth (`STRATEGY.md`) - [memory/2026-03-07.md]
- **PIE is P0** - design-first SKU selection, 8 scoring layers, target Mar 14 for v0.1 - [memory/2026-03-07.md]
- **Conversion metrics = core PIE layer** - HB401 4x HTPCR conversion (12.46% vs 2.96% on 30d US baseline, validated Mar 21), gap analysis by design coverage within addressable device set, not raw listing counts - [memory/2026-03-07.md, updated 2026-03-21]
- **ASIN→SKU bridge is critical** - Amazon session reports lack SKU; Active Listings file is the lookup table - [memory/2026-03-07.md]
- **Sven as sub-agent** under Ava, NOT separate OpenClaw instance - [memory/2026-03-07.md]
- **Pixel agent added** - Gemini 2.5 Flash, data processing/ETL specialist - [memory/2026-03-07.md]
- **Harry owns data pipelines** - BQ sync, Supabase schema, API integrations. Ava owns strategy/analytics/growth - [memory/2026-03-07.md]
- **Role clarity (Cem, Mar 8):** Ava = business strategist & planner across ALL pillars (including Ops, Finance, PH staff reduction). Harry = builder/implementer for Ops + Finance apps. Ava defines what/why, Harry builds how. Harry's output comes back to Ava for strategic review.
- **Handoff system** - SSH files at `~/.openclaw/workspace/handoffs/` + GDrive `Brain/Handoffs/` backup - [memory/2026-03-07.md]
- **Ship > Spec** - every project gets 1-week MVP target after spec approval - [memory/2026-03-07.md]
- **No staff transitions** until automation proven 4+ weeks with <5% error rate - [memory/2026-03-07.md]
- **PIE → GoHeadCase sequence** - PIE identifies SKUs first, then GoHeadCase goes live - [memory/2026-03-07.md]

### Mar 6 - Mac Studio + Benchmarks
- **Gemini for data analysis, Anthropic for strategic synthesis** - benchmark: Gemini 5.6-40s success, Sonnet/Opus timed out on data tasks - [memory/2026-03-06.md]
- **Target+ hard rule: NO US Sports** (NFL/NBA/NHL/NCAA/MLS), UK football OK - [memory/2026-03-06.md]
- **Feedonomics ends March 19** - orders already flowing via Shopify - [memory/2026-03-06.md]
- **Amazon 3.44M SKUs** - mix of FBM + FBA. FBA variants carry 'F' prefix (FHTPCR, FHB401, etc.) - same physical product, two SKUs. Snapshot was predominantly FBM at time of analysis. - [memory/2026-03-06.md, clarified 2026-03-25]
- **Blueprint Dashboard** enhanced with Supabase backend as private command center - [memory/2026-03-06.md]

### Mar 5 - Command Center + Strategy
- **Kimi K2.5 approved** as coding sub-agent (free/cheap) - [memory/2026-03-05.md]
- **Image replication bottleneck** confirmed as #1 blocker across all projects - [memory/2026-03-05.md]
- **Weekly Strategy Review cron** approved (Gemini Flash, Monday mornings) - [memory/2026-03-05.md]

### Earlier
- Light mode for ecell site (Feb 7)
- Ava promoted to Head of Sales & Marketing (Feb 17)
- Full autonomy granted on GoHeadCase POC (Feb 17)

## Lessons Learned
- Context compaction can orphan tool_result blocks → causes `unexpected tool_use_id` errors
- Fix: `session reset` (not just gateway restart, which reloads corrupt transcript)
- Changing LLM doesn't fix history corruption - it's in the transcript, not the model
- **DELEGATE all coding/programming to sub-agents** - don't burn Opus tokens on ffmpeg, builds, rendering etc.
- Claude Code `-p` mode can hang silently - use Codex CLI as fallback
- For sub-agents: try Flash first, then Codex CLI, then Claude Code CLI
- Cem's rule: I coordinate and strategise, sub-agents do the hands-on work
- **Google Stitch MCP** (stitch-mcp npm): needs `gcloud auth application-default login` + GOOGLE_CLOUD_PROJECT
  - gcloud NOT installed on Cem's iMac (as of Feb 18)
  - Stitch app is at stitch.withgoogle.com - inner app in cross-origin iframe (app-companion-430619.appspot.com)
  - Browser automation blocked by iframe; to use: `brew install google-cloud-sdk` then gcloud auth with gemc@ecellglobal.com
- PyMuPDF (fitz) is available for PDF → image extraction (`python3 -c "import fitz"`)
- **Claude Code CLI** not logged in on Mac Studio - use Codex CLI instead (authenticated via ChatGPT OAuth)
- **BQ vs Supabase schemas diverge:** BQ has raw columns (Custom_Label, Net_Sale as STRING). Supabase has parsed/typed columns (design_code, net_sale_usd as FLOAT). Always verify target schema before writing queries.
- **Vercel deployment protection:** Preview deployment URLs require SSO auth. Use the alias URL (e.g., `pulse-dashboard-inky.vercel.app`) for API testing, not the deployment-specific URL.
- **GCP service account for dashboards:** `bigquery-data-viewer@instant-contact-479316-i4.iam.gserviceaccount.com` has dataViewer + jobUser. Set key as `GOOGLE_APPLICATION_CREDENTIALS_JSON` env var on Vercel.

---

## === ACTIVE OPERATIONAL NOTES ===

# MEMORY.md (curated)

## BQ → Supabase Sync (operational 2026-03-12)
- **Script:** `scripts/sync_bq_orders.py` - delta sync (21-day lookback)
- **Nightly cron:** 3 AM ET (moved from 1 AM on 2026-03-19 to fix BQ ingestion timing), isolated session, alerts on errors
- **Result:** 305K → 319K+ orders, daily volumes restored (550-650/day)
- **Direct psql:** `postgresql://postgres:[REDACTED_DB_PASSWORD]@db.auzjmawughepxbtpwuhe.supabase.co:5432/postgres`
- Session pooler does NOT work (Tenant not found). Use direct connection only.

## PRUNE App (deployed 2026-03-11)
- **URL:** https://prune-app-xi.vercel.app
- **Purpose:** Dead weight catalog analysis - identifies zero-revenue designs/devices for delisting
- **Key stat:** 823 dead designs, 252K listings generating $0, costing ~$66K/yr in fees
- **Phases 1-5 complete.** Needs UK/DE data integration (pending Active Listings files)

## SKU Staging Pipeline (launched 2026-03-13, updated 2026-03-19)
- **Purpose:** PULSE champions → BigCommerce validation → Shopify staging → Walmart/marketplace push
- **590 combined back case champions** (HTPCR+HB401+HC, 80% elbow)
- **EAN engine built:** 480K mappings, 44K unassigned pool remaining. Auto-assigns to gap SKUs.
- **Shopify products LIVE:** First order #1083 (PNUTCHA $19.95) on Mar 20!
- **Walmart blocker:** API item creation failing. Old Zero integration was different path.
- **Image enrichment:** 636/741 products have S3 hero images. 7 US sports designs have no variants.
- **Docs:** `projects/sku-staging/SKU_STAGING_PLAN.md`, `SEO_CONTENT_FRAMEWORK.md`, `MARKETPLACE_EXPANSION_PLAN.md`

## 🔴 Active Alerts (updated Mar 28)
- **NFL renewal — 3 DAYS to Mar 31 expiry** - Flagged 4+ times (Mar 24-27). No Cem confirmation. Monday = last business day. CRITICAL.
- **CLC royalty reports overdue** past Mar 20 deadline. Breach of contract risk.
- **Supabase RLS vulnerability** — identified Mar 25, remediation spec written but not yet applied.
- **Jay Mark needs BQ credentials** — project ID, dataset, table, service account key to unblock Evri Portal build.
- **PNUTHAL/PNUTCHA** — Peanuts P1 HB401 designs still unconfirmed after sprint.
- ~~Target Plus feed DEAD~~ — RESOLVED: Shopify IS the Target Plus hub (discovered Mar 23).

## Zero 2.0 + Staff Automation (assessed 2026-03-20)
- **38 PH staff → ~17 post-automation** (55% headcount, 39% cost, ~$102K/yr savings)
- **Phase 1 (NOW-8wk):** IT dept via Veeqo + Zero 2.0 order ingest → ~₱66K/mo saved
- **Phase 2 (3-6mo):** Listings dept via Listing Engine + SKU=Content → ~₱159K/mo saved (BIGGEST)
- **Phase 3 (6-12mo):** Creative + Production + CS Tier 1 via Ecell Studio + AI → ~₱258K/mo saved
- **Zero 2.0 scope (Ava rec):** Order Ingest + Fulfillment Sync only for v1. 8 weeks for Amazon + Shopify.
- **Blockers:** Patrick knowledge transfer not started, Chad identity unknown, builder not named
- **Wiki:** `wiki/30-zero-2/` (3 docs: system summary, build plan, staff automation map)

## Known constraints / issues
- Memory retrieval can fail when embeddings provider is rate-limited or out of quota; this causes repeated re-asking of previously-known facts.
- Compaction can cause loss of "operational facts" unless they are written into durable files (MEMORY.md, memory/YYYY-MM-DD.md) and/or a system of record (Coo Blueprint).

## Operating rules (to reduce re-asking)
- When a user says "you created this / you should know this", capture the durable fact immediately into MEMORY.md (or the relevant project doc) and reference it going forward.
- Maintain a single source of truth for project queue (Coo Blueprint - replaced Orbit 2026-03-25), with TASKS.md as local Ava mirror for resilience.

## Key Session: 2026-03-07 (Major Infrastructure Day)
> Full details: `memory/2026-03-07.md` - Morning + Afternoon + Evening sessions
> Highlights: gcloud auth, BQ discovery (2.8M orders), Amazon analysis, BC catalog load, PIE v2 scope, Pixel agent added, Harry BQ sync delivered, conversion metrics as core PIE layer, execution plan created

## Data Integrity (verified 2026-03-07)
- **BigQuery (source of truth):** 2.8M rows, 2019-11-25 → 2026-03-07 (LIVE)
  - Project: `instant-contact-479316-i4`, Dataset: `zero_dataset`, Table: `orders` (VIEW)
  - 15 datasets total; `headcase` has product master (tblDesigns, tblLineups, etc.)
  - gcloud auth: ✅ `gemc@ecellglobal.com` on Mac Studio
- **Supabase orders:** 304K rows, date range 2025-01-01 → 2026-02-17 (stale partial export)
- **Source:** One-time BigQuery export, NOT live sync
- **BQ → Supabase sync: ✅ LIVE** (Harry completed 2026-03-07)
  - `net_sale_usd` column added, `fx_rates_daily` table created
  - Crons: FX refresh 1:30 AM ET, Orders sync 3:00 AM ET (moved from 2 AM on 2026-03-19, 21-day lookback)
  - Scripts on iMac: `~/.openclaw/workspace/scripts/`
- **Pre-parsed columns exist:** design_code, device_code, product_type_code, design_variant - DON'T re-parse custom_label
- **Amazon Active Listings:** 3.44M SKUs, ASIN→SKU bridge table. File at `gdrive:Brain/Projects/Amazon/`. Harry loading to Supabase/BQ.
- **Amazon session reports (standard):** Only contain ASIN, NOT SKU. Must JOIN with Active Listings for actionable data.
- **Conversion insight (Cem Mar 7, superseded Mar 21):** Early data showed HB401 2.5x HTPCR (8.34% vs 3.28%). **Validated Mar 21: 4x (12.46% vs 2.96% on 30d US baseline).** Only $16K revenue at time of Mar 7 - under-distributed. HDMWH 10% revenue from 0.47% listings. HLBWH over-distributed (29% listings, 12.9% revenue).
- **PIE Execution Plan:** 7-day sprint to v0.1 (target Mar 14). At `projects/product-intelligence-engine/EXECUTION_PLAN.md`
- **PIE PROJECT_BRIEF.md:** Updated to v2 with Layers 7 (Conversion Benchmarking) + 8 (Search Terms Phase 2)
- **SOP:** `wiki/02-sales-data/SOP_SALES_ANALYTICS.md` - lookback strategy, regional analysis, data quality rules
- **Atlas MEMORY.md + SOUL.md:** Updated with full schema, conversion rates, business context, "read MEMORY.md first" rule
- **Key insight:** Multi-lookback comparison is CRITICAL for SKU selection (new licenses like Naruto/NBA underweighted in all-time data)

## Catalog Scale (discovered 2026-03-06)
- **Amazon**: 3.44M active SKUs (FBM + FBA - FBA uses 'F' prefix, same product two SKUs), 144K out of stock
- **Walmart**: 95,640 active SKUs, 99.9% zero reviews, 90% phone cases, $10-30 sweet spot
- **Target+**: SKU count TBD - Feedonomics contract ending ~mid-March 2026

## Mac Studio (operational 2026-03-06)
- **Hardware**: M4 Max, 36GB RAM, macOS 15.7.4
- **Tailscale**: cems-mac-studio (100.72.19.27)
- **User**: openclaw (admin, passwordless sudo)
- **OpenClaw**: 2026.3.2, tools profile: full
- **Telegram**: Connected, locked to Cem (5587457906)
- **Discord**: Enabled but no bot token yet
- **iMac**: Visible on Tailscale (100.91.149.92) but SSH not configured

## Strategic Execution Framework (approved 2026-03-07)
- **4 Pillars:** Sales → Production → Operations → Growth
- **Full doc:** `STRATEGY.md`
- **Pillar 1 (Sales):** PIE, SKU selection, Target+/Walmart/Amazon FBA strategy
- **Pillar 2 (Production):** Print file automation (#1 target), camera hole AI, design pipeline
- **Pillar 3 (Operations):** Inventory migration, shipping optimization, CS email automation
- **Pillar 4 (Growth):** ListingForge, GoHeadCase, microsites, marketing
- **Key rule:** No staff transitions until automation runs in parallel 4+ weeks with <5% error rate
- **Execution:** Q1 = data pipelines + MVPs, Q2 = parallel automation + GoHeadCase, Q3 = staff transition + SaaS
- **Agent mapping:** Harry (Pillars 1-3 data/infra), Ava (strategic oversight + Pillar 4), Sven (design), Atlas/Prism (analysis), Forge/Spark (builds)

## Product Intelligence Engine (PIE) - P0 Project
- **Owner:** Harry (multi-model orchestration), **Strategic Lead:** Ava
- **Goal:** Algorithmically select ~200K SKUs from 1.89M BigCommerce catalog for GoHeadCase Shopify → Target+/Walmart/DTC
- **Core approach:** Design-first ("we sell collections") - rank designs by revenue, replicate across devices × product types
- **Architecture:** Multi-model ensemble - Atlas (Gemini 3.1 Pro) + Prism (GPT-5.4 Codex), Ava reconciles
- **Model decision (Mar 6):** Gemini for data analysis (fast/cheap), Anthropic for strategic synthesis only
- **Key data:** 304K orders ($18.9M), 704 devices, Top 50 devices = 86.5% revenue
- **Regional splits matter:** US = iPhone-heavy + desk mats; UK = Samsung A16 5G in top 10 + console skins
- **Product types by revenue:** HTPCR £8.04M > HLBWH £7.28M > HC £2.23M
- **Target+ hard rule:** NO US Sports (NFL/NBA/NHL/NCAA/MLS) - UK football OK
- **Amazon insight:** 3.44M SKUs (FBM + FBA - FBA has 'F' prefix). At time of analysis, predominantly FBM. Combining FBM+FBA = total product view.
- **Walmart:** 95K SKUs, 99.9% zero reviews - needs review velocity strategy
- **Brand tiers:** A (top 20, all designs), B (next 30, top 10), C (long tail, top 5) → ~201K estimated
- **Collection completeness:** each design → HTPCR + HC + HB401 + HLBWH minimum
- **Device families:** if iPhone 16, must include 16/Plus/Pro/Pro Max
- **PIE Phase 1.1 COMPLETED (Mar 9):** Design-level revenue rankings from full BQ (2.8M orders). Report at `results/pie-phase1.1-design-revenue-rankings.md`
  - The Big 3: HTPCR ($21.4M), HLBWH ($13.5M), HC ($9.9M) = ~90% of all revenue
  - Growth rockets (>40% of revenue in last 90d): HDMWH (WWE, 51%), HB401 (Wumples, 45%), HB6CR (West Ham, 65.5%), HB7BK (West Ham, 84%)
  - Top 90d brand: Peanuts ($184K), then Harry Potter ($154K), Liverpool FC ($128K)
  - Anime scaling fast: Naruto ($87K/90d), Dragon Ball Super ($34K/90d)
  - HLBWH over-distribution confirmed: 2.4% recent revenue vs ~29% listings → redirect to HDMWH/HB401
  - BQ direct query bypasses Supabase backfill problem - use for analytics going forward
- **PIE Phase 1.2+ COMPLETE:** ASIN→SKU bridge built (3.4M mappings), gap analysis done
- **Supabase backfill: ✅ RESOLVED** - 0 null `net_sale_usd` across 319K+ orders. BQ sync script + currency backfill fixed it all.
- **Blockers:** GA4 data (BigCommerce API ✅ connected, ASIN→SKU bridge ✅ built)
- **Brief:** `projects/product-intelligence-engine/PROJECT_BRIEF.md`
- **Dashboard:** Sales Dashboard V2 at https://app-zeta-sable.vercel.app (Vite+React+Express+BQ, repo: gemc99-boop/sales-dashboard)
- **Amazon US session data:** 80K rows (Jan-Feb 2026), ASINs + SKUs + sessions + conversion. Atlas analysis at `~/results/amazon-us-session-analysis.md`
- **BigCommerce catalog:** 50GB TSV, ~1.89M SKUs, 51 columns. At `~/Downloads/164336_622139_*`

## Operations Wiki (centralized 2026-03-07)
- **Location:** `wiki/` - 53 .md documents across 16 sections
- **Index:** `wiki/INDEX.md` with cross-reference map
- **Source:** Merged from Clawdbot Shared Folder (01-08 project folders) + Brain/Projects + Harry's migration backup
- **Key insight from cross-referencing:**
  - SCHEMA_DESIGN.md (Feb 10) already had the SKU decomposition + unified multi-marketplace schema that PIE needs - don't rebuild, extend
  - SALES_ANALYSIS_2025.md (268K orders, $5.5-6M) is PIE's baseline scoring data
  - ListingForge (10) is the productized version of Creative Pipeline (09) image + content funnels
  - Print File Pipeline (03) + Design File Management (06) share the camera hole issue - one fix solves both
  - Email Triage (15) supersedes CS Email Bot (01) - don't build both
  - Desk mats + console skins are major sellers (not just phone cases!) - discovered in 2025 sales analysis
- **Next:** Semantic search layer via pgvector or Airweave over this corpus

## PH Staff (38 total, ~₱1.27M/mo ≈ $22K USD/mo)
- **Production (10)** - Jae Vitug (Manager), Chris Yunun (Warehouse), printing + image processing
- **Listings (8)** - Jay Mark Catacutan (Lead ₱50K), mix of designers, replicators, admin
- **Creative (6)** - Bea Pineda (Manager ₱101K, oversees Creative + Graphics + Listings)
- **IT (5)** - Network/systems for image gen infra + shipping label printing (Dickel Pineda leads)
- **Customer Service (5)** - Analiza Peralta (Manager ₱140K), Cris Guintu (Asst Manager ₱84K)
- **HR (2)** + **Finance (2)**
- **Automation targets:** Listings (8 staff, replication/QA automatable), Creative asset creation (6 staff, template workflows), Print file generation (3 of Production, #1 automation target per Harry)
- **Roster saved:** `org/ph-staff-roster.md`

## Blueprint Dashboard
- **URL:** `app-zeta-sable.vercel.app` (Strategic Blueprint Dashboard - I created this)
- **Command Center:** `command-center-one-puce.vercel.app` (separate project tracker)
- **Repo:** local `~/projects/blueprint-dashboard/` (Next.js + TypeScript)
- **Data file:** `app/data/projects.ts` - static TypeScript, Cem drag-drops to reorder
- **Storage:** localStorage for user edits + initial data from projects.ts
- **Vercel team:** `ecells-projects-3c3b03d7` - 17 projects total
- **Config backed up:** `gdrive:Brain/Projects/blueprint-dashboard/`

## Veeqo Order Management (discovered 2026-03-08)
- **Two regional Veeqo instances:** US and UK (region-locked)
- Veeqo connects directly to channels - it IS the order intake point
- US channels: Amazon US, Amazon FBA, GoHeadCase Shopify, Walmart, Etsy, eBay US, Fanatics US, TikTok Shop
- Smart Order Routing: auto-allocates to nearest warehouse with stock
- Custom filtered tabs for operators (FL Premium, FL Non-Premium, etc.)
- Mark as shipped → auto-updates ALL marketplaces + sends tracking to customer
- **Pipeline:** Veeqo labels → CSV export → PO for print files → AI image generation → 1:1 reconciliation
- **Target ops model:** 3 operators (1 UK, 1 FL, 1 PH) replacing 10+ staff
- Drew's Dev Team folder (70 files) = complete evidence that Zero's manual pipeline is fully replaceable
- **Unsolved:** Shopify international routing (connecting to both Veeqo US+UK = double shipment risk)
- **Chad** to manage image tools + hardware + AI (replacing Dickel's 5-person IT team)

## Google Workspace CLI (configured 2026-03-12)
- **CLI:** `gws` v0.11.1 (`@googleworkspace/cli`) - replaces `gog`
- **Account:** gemc@ecellglobal.com (read-only: Drive, Gmail, Calendar)
- **OAuth:** Airweave client (175143437106, project instant-contact-479316-i4)
- **Credentials:** /Users/openclaw/.config/gws/credentials.enc (AES-256-GCM)
- **Drive API blocker: RESOLVED** ✅

## Inventory Tracker (built 2026-03-12)
- **Supabase:** `blank_inventory` table + `v_inventory_alerts_v2` view + `v_inventory_global` (cross-site)
- **Snapshot:** 5,193 active blank SKUs (PH 2,936, UK 2,502, FL 1,195)
- **Active:** Only 1,210 SKUs have sales (77% dead stock)
- **Alert distribution:** GREEN 4,671, YELLOW 242, RED 84, BLACK 196
- **Scripts:** `setup_inventory_schema.py`, `snapshot_inventory.py`, `deduct_inventory.py`
- **Harry building procurement dashboard on top** - ship target Mar 19

## Gmail Access (configured 2026-03-08)
- **gog CLI** with read-only OAuth (gmail, calendar, drive, contacts)
- Account: gemc@ecellglobal.com
- OAuth Client: `175143437106-funrdi7s4kh1n1sgefiln1v58fq6mkkg.apps.googleusercontent.com`
- JSON at: `/Users/openclaw/Downloads/client_secret_175143437106-funrdi7s4kh1n1sgefiln1v58fq6mkkg.apps.googleusercontent.com.json`
- Key contacts extracted: Drew Ramos (a.ramos@ecellglobal.com, IT), Bea Pineda (b.pineda@ecellglobal.com, Creative)

## Perplexity Search API (configured 2026-03-08)
- Key: 
- Set as primary web_search provider in openclaw.json

## Zero Infrastructure (discovered 2026-03-09)
- **Master DB**: 192.168.20.160 (PH local, behind firewall) - AWS Aurora is downstream sync
- **PHP codebase**: 192.168.20.57 (XAMPP, likely Windows) - `C:\xampp\htdocs\`
- **Web server creds**: elcell / yUpeMab9
- **Key PHP files**: `zero_POFiltering.php` (1300+ lines, hardcoded PO routing), `sage_generate_picking_list_split.php`, `zero_generate_purchase_order_automated_phAMG1_wh.php`
- **Manufacturing Office**: Separate ESXI + QNAP NAS + VMs (likely IREN image gen system)
- **Full map**: `wiki/23-drew-handover/ZERO_INFRASTRUCTURE_MAP.md`
- **Extraction plan**: Jay Mark Catacutan (trusted, has Claude Code, on PH LAN) to push htdocs to private GitHub

