# MEMORY.md

## Standing Rules

## Cem's Dog Walking Windows (audio-only preference)
- **Morning:** 6:30–7:30 AM daily
- **Afternoon:** 3:00–4:30 PM daily
- During these times: respond in audio (TTS) only — no long text walls
- Cem walks Bart and Yuki; prefers hands-free during walks


## Gateway Always-On Setup (Feb 20)
- **Registry Run Key:** `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run` → `ClawdbotGateway` → watchdog on login
- **Watchdog:** `C:\Users\gemc\clawd\scripts\gateway-watchdog.ps1` — checks every 30s, auto-restarts
- **NSSM:** installed, but service creation needs admin PowerShell (Cem to run when convenient)
- **Elevated exec:** enabled for Cem (telegram:5587457906) — Cem types `/elevated full` to activate

## Shared Telegram Group (Feb 20)
- **Supergroup ID:** -1003832582809 (Harry + Ava + Cem)
- Old group ID: -5273192890 (migrated to supergroup)
- Config: whitelisted, `requireMention: false`

## Mission Control v2 — Listing Generator (Feb 20)
- Route `/listing-generator` added to mission-control-v2 (Vercel)
- 4 API routes: generate/chat/brands/devices
- Pending: Supabase `listings` table SQL migration (Cem action), Vercel redeploy
- Supabase project: nuvspkgplkdqochokhhi

## Sales Dashboard Data Source (Feb 20)
- Live orders in Supabase project2: auzjmawughepxbtpwuhe (304K orders, 2025+)
- Schema: paid_date, marketplace, buyer_country, currency, gbp_price, quantity, custom_label, product_type_code, device_code, design_code, brand
- Decision pending: integrate into Mission Control (A) vs. fix standalone (B)

## BigQuery Access — Full ZERO Mirror (Feb 22)
- Project: `instant-contact-479316-i4` (current gcloud default)
- Key datasets: `zero_dataset` (orders_clean, inventory), `headcase` (design catalog), `production_tracker` (fl/uk stocks, print output)
- This is the data source for Fulfillment Orchestrator — no direct MySQL needed
- Auth: gcloud `gemc@ecellglobal.com`, token via `gcloud auth print-access-token`

## Fulfillment Orchestrator — Phase 1 MVP Built (Feb 22) ✅
- Project: `C:\Users\gemc\clawd\projects\fulfillment-orchestrator\`
- Stack: Next.js 14 App Router, BigQuery, rclone → GDrive, pdf-lib
- Dashboard: `http://localhost:3000/fulfillment`
- Features: order queue, routing engine, label + print stubs, reconciliation, dispatch_log
- Phase 1 stubs remaining: real EasyPost labels, real TIFF/EPS rendering
- Build log: `memory/fulfillment-orchestrator-build-log.md`

## Fulfillment Orchestrator — Hard Routing Rules (Feb 22)
- Saturday → Philippines handles ALL orders
- H89 (skins) + HST (stickers) + HDM (desk mats) → UK + US (FL) ONLY — never Philippines
- Other products → FL if FL stock available (BigQuery inventory table)
- Veeqo MUST remain for Amazon USA (A-to-z protection + tracking validity)
- Print files → Google Drive (local offices pull from there)
- EU carriers → Evri + Royal Mail (Deutsche Post phased out)
- PH freight: PH→UK = DHL/FedEx; PH→US = FedEx
- Label + print file delivery: Orchestrator generates sorted SKU-ordered combined PDF → upload to GDrive → local site downloads + prints. No print server.
- Overflow triggers: Saturday, Monday, over capacity, holiday, HLBWH from FL (longer print = often sent to PHL)
- Still needed: Evri API key

## GoHeadCase Master Plan — APPROVED (Feb 21)
- Cem approved 26-week, 4-phase Headless Shopify Microsite Strategy
- File: `gdrive_shared/Brain/Projects/goheadcase/MASTER_PROJECT_MAP.md`
- Phase 0 (Foundation) now active — Ava leads microsite build, Harry owns data/infra
- Goal: 2,609 → 26,000+ own-site units in 12 months; Amazon dependency 76% → <60%

## MISSION.md — Pending
- Draft ready in chat (Feb 19 session)
- Waiting: Cem brain dump + mission statement sign-off
- Items: goals, mission statement, Cem Operating Prompt


- **Always save project conversations** — whenever Cem discusses projects, decisions, direction, or strategy, write it to `memory/YYYY-MM-DD.md` immediately. Don't rely on session memory alone.

## Critical: IT Manager Leaving Feb 14
- Three Philippines understudies handle day-to-day (picking lists)
- Technical risk: cron jobs, API integrations, internal app
- Handover questionnaire sent: `gdrive_shared/08_Infrastructure/IT_HANDOVER_QUESTIONNAIRE.md`
- Harry + Cem absorbing all technical responsibilities

## Agent Architecture (Feb 11)
- VPS = Harry's brain (always on, gateway, N8N, orchestration)
- Windows PC (gemc) = Harry's hands (coding, builds, Photoshop scripting)
- iMac = Ava's machine (websites, design, marketing)
- Google Drive for file sharing between all
- Sub-agents default to Gemini Flash (cheap)

## Business Process Docs Location
- Master status: `projects/MASTER_PROJECT_STATUS.md`
- All SOPs: `gdrive_shared/01-08_*/SOP_*.md`
- Production deep-dive: `projects/production-workflow/`
- Sales schema: `projects/sales-schema/`
- CS automation: `projects/cs-automation/`

## TTS Working Config
- Provider: ElevenLabs (OpenAI quota exhausted)
- Voice ID: 8Ln42OXYupYsag45MAUy
- Pipeline: ElevenLabs API → mp3 → ffmpeg ogg/opus → message tool asVoice
- Built-in tts tool unreliable for delivery; manual pipeline works - Long-Term Memory

## About Cem

- **Full Context:** 52-year-old British national in Orlando, FL
- **Family:** Wife Alma, son James (10)
- **Work:** ECELL Global / Head Case Designs
- **Email:** gemc@ecellglobal.com
- **Style:** Relaxed, no corporate stiffness

## Head Case Designs (goheadcase.com)

- **Founded:** 2011
- **Product:** Phone cases, tablet cases, gaming skins, laptop skins, audio cases
- **USP:** 12,000+ licensed designs (sports, entertainment, music, gaming, lifestyle)
- **Recognition:** One of License Global's leading licensees
- **Market coverage:** 95% of devices

**Global Offices:**
- Orlando, FL (HQ)
- United Kingdom
- China
- Philippines (operations — currently 42 staff)
- Japan

**Current Strategic Focus:**
- AI automation to reduce Philippines headcount: 42 → 25 staff (40% reduction)
- Departments: Creative/Marketing, Content/Listing, Graphics, CS, Inventory
- Using Claude, Gemini, Perplexity for AI solutions

## Key Integrations

- **Notion:** Second brain — Professional Dashboard, projects, to-dos
- **Brave Search:** Web search enabled

## Active Projects (from Notion)

- **FBA Conversions** — Amazon fulfillment optimization
- **ECELL Business Process** — PD → go-live → marketing (includes influencer strategy)
- **Inventory Reorder systems** — automation
- **NFL Royalty Reports** — licensed sports merchandise tracking
- **Competition Analysis**
- **AI Automation** — reducing headcount through workflow automation

## Hobbies & Life

- **BJJ:** Blue belt — transitioned from soccer ("too old now")
- **Fitness:** Enjoys working out and running but struggles to find time
- **Soccer:** Played most of his life
- **Dogs:** 3 large dogs
  - Bart (Japanese Akita)
  - Yuki (Japanese Akita)
  - Siberian Husky (name?)

## Key Infrastructure (Feb 2026)

**Tools Connected:**
GitHub (gemc99-boop), Vercel, OpenRouter, N8N v2.6.4, Notion, Slack (Ecell workspace), Google Drive, Asana, Google Cloud SDK (gcloud), rclone

**GCP Projects:**
- `opsecellglobal` — main ops project (ecell-dashboard on Cloud Run)
- `instant-contact-479316-i4` — BigQuery, FBA Planner, Royalty Reporting, Sales Dashboard

**Cloud Run (ecell.app):**
- Service: ecell-dashboard (us-east1) on opsecellglobal
- URL: https://ecell-dashboard-786712421741.us-east1.run.app
- Stack: Next.js 16 + Auth.js v5 + Tailwind 4 + framer-motion
- Design: Antigravity style (Space Grotesk, antigravity shadows, technical dot grid, Material Symbols)
- ecell.app LIVE ✅ — Cloud Run, Google SSO (@ecellglobal.com only), AUTH_TRUST_HOST=true
- OAuth credentials: ~/.config/google-oauth/ecell-app.json
- Apps: Sales Dashboard, FBA Planner, Royalty Reporting, Mission Control, Orbit PM, Business Processes (placeholder), Product Entry (placeholder), Image Maker (placeholder)
- Sales Dashboard link: gemc-wq.github.io/sales-dashboard/ (GitHub Pages)

**Agent Cost Model (Updated Feb 17):**
- Harry = **Sonnet 4.6** via Anthropic API KEY (switched from Opus 4.6 — 5x cheaper, $3/$15 per 1M tokens)
- NOT on Max subscription OAuth — Anthropic blocked OAuth
- Sub-agents = GPT-5.2 via ChatGPT subscription OAuth (openai-codex/gpt-5.2) — zero cost
- Graphics = Nano Banana Pro / Gemini 3
- Delegate aggressively to sub-agents; Sonnet 4.6 for strategy/judgment

**Discord (Ecell Ops):**
- Guild: 1472782527331569789
- Harry groupPolicy: open
- Ava gateway token: in gdrive ava-setup folder
- Ava chat completions API not enabled — can't direct message yet

**Live Services:**
- CS Chat Agent: N8N webhook /webhook/headcase-chat (GPT-4o-mini via OpenRouter)
- Knowledge base trained on GoHeadCase.com policies
- ecell.app: LIVE ✅ (Cloud Run, org policy override applied)

**BigCommerce API:**
- Store: otle45p56l, app: ecell.app, credentials at ~/.config/bigcommerce/credentials.json
- Catalog: 1.89M products, images on BigCommerce CDN

**Supabase (2 projects):**
- nuvspkgplkdqochokhhi (gemc99-boop): Product catalog — devices, brands, product_types
- auzjmawughepxbtpwuhe (gemc-wq): Orders & Inventory — synced from BigQuery
  - mgmt token: [REDACTED_MGMT_TOKEN]
  - 304K orders (2025+), 9,805 inventory rows (active only)
  - SKU auto-parse trigger, HC prefix standardized on inventory
  - Excluded: Z% (legacy), H8% (PS5 skins)
  - Active inventory = PO date 2024+ OR has 2025 sales

**SKU Format:** ProductType-Device-DesignParent-DesignChild
- HC prefix standardized: inventory uses HC-IPH16 (not bare IPH16)
- Direct match: product_type || '-' || device = inventory item_code

**AI Sales Bot:** ON HOLD — architecture docs in projects/sales-bot/
- Vertex AI ($1,670/mo) vs AWS S3 Vectors + Nova ($240-600/mo)
- Needs further discussion on image source (AWS vs BigCommerce CDN)

**Microsites / Shopify Factory Strategy (NEW — Feb 17):**
- GoHeadCase.com with 2M products only sold 2,609 units in 2025 (<1% of orders)
- Problem: too broad, no identity, no SEO, no targeted marketing
- Solution: niche microsite factory on Shopify
- Four microsites based on 2025 sales data:
  1. ⚽ The Kit Room (football/sports) — UK dominant
  2. 🧙 The Wizarding Store (Harry Potter/LotR/fantasy) — US dominant
  3. 🐾 Soft & Sweet (Peanuts/patterns/female-skewing)
  4. 🎮 Otaku Zone (anime/gaming — Naruto, desk mats)
- Phase 1: Mini GoHeadCase clone on Shopify (POC, ~500 products)
- Phase 2: Website factory — Ava builds Shopify theme template, Harry automates pipeline
- Harry role: BigCommerce → Supabase → Shopify CSV pipeline
- Ava role: Shopify frontend, content, social, email per niche
- Next step: Microsites Architecture doc + loop Ava in
- Stitch/Antigravity = Google's design tool Ava uses on iMac for frontend work

**Ecell Apps (all on Google Cloud Run):**
- Sales Dashboard (React/Firestore) — repo: gemc-wq/sales-dashboard
- FBA Planner (Streamlit) — inventory analysis, restock planning
- Royalty Converter (Flask) — per-licensor formatting (NFL, Arsenal, Chelsea, etc.)
- All need Amazon SP-API to replace manual CSV uploads
- Cem says they already have Amazon API key

**App Dashboard planned:** "Ecell Command Centre" on Vercel, Google SSO, match brand design

## Agent Team Structure (Feb 2026)

Cem (CEO) → Harry (Automation) + Ava (Creative/Strategy)
- Harry's sub-agents: Spark, Radar, Prism, Pixel, Nexus (all Gemini Flash)
- Ava's sub-agents: Iris, Echo, Forge, Spark2, Flux, Bolt, Atlas
- **Cost policy:** Default gemini-flash, Opus only for complex planning
- **Heavy coding → Ava** (iMac has Claude Code + Codex on FREE subscriptions)
- Documented in SPECIALIST_ROSTER.md

## Slack Team Notes

- **Jeff (Jeffrey Mangilit)** — Creative team, building Samsung S24/S25 templates in Figma, using Gemini Gem for image creation
- Creative channel: C09SVCQS1C2

## Notes

- Cem is deeply focused on AI automation for business efficiency ("The Autonomous Enterprise")
- Licensed products: NFL, WWE, Peanuts, Harry Potter, Brighton & Hove Albion FC, Arsenal, Chelsea, Man City, Liverpool, Juventus, Barcelona, Real Madrid, Tottenham
- Top sellers: Naruto (US #1), Peanuts, LFC (UK #1), Harry Potter
- GoHeadCase.com = D2C site, but most sales via Amazon
- Dogs: Bart, Yuki (new 2025), Kaito (husky). Atom & Yumi (Akitas) passed 2025.
- Morning audio briefings requested — Cem listens while walking dogs at 6:30 AM EST

## Role Boundaries — CONFIRMED Feb 20
- **Harry** = COO, operational: data, automation, pipelines, infrastructure, CS, inventory, analytics, N8N
- **Ava** = Head Case Designs: websites, frontend, creative, GoHeadCase microsite factory
- Do NOT drift into website/frontend work — that's Ava's lane

## Mission Control v2 — Calendar (Feb 20)
- URL: https://mission-control-v2-three.vercel.app
- Calendar view live at /calendar — monthly grid, colour-coded by assignee
- Cem wants: daily task cadence where Harry + Ava each have clear daily tasks moving toward goals

## Supabase Project2 Service Role Key (Feb 20)
- project2: auzjmawughepxbtpwuhe (orders + inventory)
- service_role key: [REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc
- Save to credentials file; use this for inventory/orders queries

## N8N Server — Live (2026-02-20)
- **URL:** https://n8n.ecellglobal.com (GCP e2-small, us-east1-b, opsecellglobal)
- **IP:** 104.196.12.151 | Login: admin / ecell_n8n_2026!
- **Stack:** Docker Compose (n8n + Postgres + Caddy auto-TLS)
- **DNS:** Cloudflare — ecellglobal.com (token saved at ~/.config/cloudflare/api_token)
- **SSH:** `gcloud compute ssh n8n-server --zone=us-east1-b --project=opsecellglobal`
- **Purpose:** Email Triage MVP — gemc@ecellglobal.com Gmail OAuth (Ava building workflows)
- **Org policy fix:** vmExternalIpAccess allowedValues set at project level

## CS AI System — New Project (2026-02-18)
Three-channel AI system for new B2B business on esaleglobal.com:
1. **Chat Widget** — Claude Sonnet + N8N + Supabase (Ava provisioning space in ESale redesign)
2. **Outreach Assistant** — N8N + GPT-5.2 + Resend (email sequences for new business; LinkedIn TBC)
3. **Voice Agent** — Twilio + Google STT + ElevenLabs + Claude (CS phone line)
All → one Supabase DB. GoHeadCase existing customers = separate Vertex AI track (Phase 2).
Amazon SP-API parked — using BigCommerce as data source instead.
Spec: `projects/cs-ai-system/CS_AI_ARCHITECTURE_SPEC.md`

## Trend Intelligence — 2026-02-18

**Top design opportunities identified (nightly mission):**
1. **GTA VI Vice City Aesthetic** — Pre-hype NOW, game launches Nov 2026. Neon Miami/Vice City palette already viral on TikTok. Strike before summer marketing ramp.
2. **Winter Olympics 2026 (Milan-Cortina)** — Live this week, multiple viral moments. Alpine/sport/national pride art — fast-turn 2-week window.
3. **Pixel/Y2K Nostalgia ("Pixel Heart")** — High volume potential, wide demo, no licensing cost. Mint/peach/teal palettes, 8-bit charm.
4. **Soft Earth & Stone** — Sage green, clay, soft marble — premium minimalism niche, underserved vs. maximalism wave.
5. **Jewel Drop / Rhinestone-Core** — TikTok-viral luxury jewelry-inspired cases (OSSA brand). Flat print equivalent at mass-market price.

**Supabase approvals:** Clear (0 pending) as of 2026-02-18.  
**Full brief:** `memory/nightly-output-2026-02-18.md`

---

*Last updated: 2026-02-18*
