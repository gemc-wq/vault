# MEMORY.md

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
GitHub (gemc99-boop), Vercel, OpenRouter, N8N v2.6.4, Notion, Slack (Ecell workspace), Google Drive, Asana

**Live Services:**
- CS Chat Agent: N8N webhook /webhook/headcase-chat (GPT-4o-mini via OpenRouter)
- Knowledge base trained on GoHeadCase.com policies

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

---

*Last updated: 2026-02-07*
