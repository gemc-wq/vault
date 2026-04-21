# MEMORY.md - Ava Long-Term Memory (merged 2026-02-28)

> Merged from pre-migration clawdbot workspace + active OpenClaw workspace.
> Rich historical context restored from original clawdbot workspace.

---

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
- Uses Orbit PM (https://orbit-pm.vercel.app) for project management
- Slogan: "We Got You Covered"

## Organisation
- **Cem** - CEO, Human-in-the-Loop
- **Harry** - Lead Automator / COO, Claude Opus 4.6, runs on VPS
- **Ava (me)** - Head of Sales & Marketing, Claude Sonnet 4.6, runs on Cem's iMac
- Shared Google Drive: `Clawdbot Shared Folder` (rclone `gdrive:`)
- Brain folder: `gdrive:Clawdbot Shared Folder/Brain/` - source of truth for all projects
- Harry communication: `collaboration/` folder on shared drive
- 13 total agents across both teams

## Model Stack (updated 2026-02-17)
| Role | Model | Cost |
|------|-------|------|
| Ava (me) | Claude Sonnet 4.6 | API |
| Harry | Claude Opus 4.6 | API |
| Echo (copy) | Claude Sonnet 4.6 | API |
| Iris (design) | Gemini Nano Banana Pro | Gemini CLI OAuth |
| Loom/Bolt (research/scout) | Gemini Flash | API/OAuth |
| Atlas/Prism (analysis) | Kimi K2.5 | CHEAP |
| Forge/Spark/Nexus (coding) | Codex CLI GPT-5.3 | FREE (ChatGPT OAuth) |
| Pixel/Radar (merchant/scout) | Gemini Flash | API |

- web-builder Clawdbot agent: openai-codex/gpt-5.2 (primary), Codex CLI defaults to 5.3
- Codex CLI v0.98.0 at /opt/homebrew/bin/codex - logged in via ChatGPT OAuth ✅

## My Team (Sales, Marketing & Creative) - 8 agents
- **Echo** - Copywriter (Sonnet 4.6) - web copy, Amazon listings, ad copy
- **Iris** - Designer (Gemini Nano Banana Pro, OAuth) - visuals, mockups, assets
- **Loom** - Researcher (Gemini Flash) - competitor intel, market research
- **Bolt** - Scout (Gemini Flash) - SEO keywords, quick lookups
- **Atlas** - Analyst (Kimi K2.5) - Amazon ads strategy, pricing, reporting
- **Forge** - Web Builder (Codex CLI GPT-5.3, FREE) - Next.js builds
- **Spark** - Builder 2 (Codex CLI GPT-5.3, FREE) - deep code, architecture
- **Flux** - DevOps (Gemini Flash) - Vercel deploys, CI/CD

## Org Chart
```
Cem 👑 - CEO, Human-in-the-Loop
├── Harry (Lead Automator/COO, Opus 4.6 API) - 5 agents
│   ├── Pixel (Merchant, Flash)
│   ├── Nexus (Integrator, Codex FREE)
│   ├── Spark (Engineer, Codex FREE)
│   ├── Radar (Scout, Flash)
│   └── Prism (Analyst, Kimi K2.5)
└── Ava (Head of Sales & Marketing, Sonnet 4.6 API) - 8 agents
    ├── Echo (Copywriter, Sonnet 4.6)
    ├── Iris (Designer, Nano Banana Pro OAuth)
    ├── Loom (Researcher, Flash)
    ├── Bolt (Scout, Flash)
    ├── Atlas (Analyst, Kimi K2.5)
    ├── Forge (Builder, Codex FREE)
    ├── Spark (Builder 2, Codex FREE)
    └── Flux (DevOps, Flash)
```

## Active Projects
- **ecellglobal.com Redesign** — B2B marketing site (Vite/React + Tailwind) deployed on Vercel.
  - Vercel project: `ecell-site` (org: Ecell's projects)
  - Latest prod deploy (example): https://ecell-site-h8h8ljwb9-ecells-projects-3c3b03d7.vercel.app
  - Domain cutover in progress: `ecellglobal.com` + `www.ecellglobal.com` added to Vercel; Cloudflare DNS needs A root → 76.76.21.21 and CNAME www → cname.vercel-dns.com (DNS only).
  - Local: `projects/ecell-website/ecell-site/`

- **GoHeadCase POC / Template** — Casetify/OtterBox-grade licensed-first template + microsite/universe landing system.
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

- **Orbit PM** — https://orbit-pm.vercel.app (used for task breakdowns)

## Nightly Cron Tasks
- **2:00 AM** — Nightly mission task (Mon=Market Intel, Tue=Audit, Wed=Content, Thu=Leads, Fri=Website, Sat=Trends, Sun=Recap)
  - Saves to Brain/Daily/YYYY-MM-DD.md + Telegram summary to Cem
- **3:00 AM** — Daily trends pipeline (CSV + Gamma slides → Telegram)
- **6:00 AM** — Morning audio brief (TTS → Telegram)

## Key Decisions
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
  - Stitch app is at stitch.withgoogle.com — inner app in cross-origin iframe (app-companion-430619.appspot.com)
  - Browser automation blocked by iframe; to use: `brew install google-cloud-sdk` then gcloud auth with gemc@ecellglobal.com
- PyMuPDF (fitz) is available for PDF → image extraction (`python3 -c "import fitz"`)

---

## === ACTIVE OPERATIONAL NOTES ===

# MEMORY.md (curated)

## Known constraints / issues
- Memory retrieval can fail when embeddings provider is rate-limited or out of quota; this causes repeated re-asking of previously-known facts.
- Compaction can cause loss of “operational facts” unless they are written into durable files (MEMORY.md, memory/YYYY-MM-DD.md) and/or a system of record (Orbit).

## Operating rules (to reduce re-asking)
- When a user says “you created this / you should know this”, capture the durable fact immediately into MEMORY.md (or the relevant project doc) and reference it going forward.
- Maintain a single source of truth for project queue (Orbit), but also keep a small local mirror file (TASKS.md) for resilience.

## Open items to fill in
- Orbit URL: https://orbit-pm.vercel.app/tasks
- Orbit auth method: direct URL (no auth required)
- Canonical repo/app that serves ecell.app home tiles: business-dashboard repo (Sales Dashboard tile link lives in `business-dashboard/src/app/page.tsx`)
- Vercel token location: Google Drive → `Clawdbot Shared Folder/Brain/Credentials/API Keys for Ava (1).txt`
- Vercel account: `gemc99-boop` / email `gemc99@me.com` — git commits MUST use this email as author or deploys fail
- Vercel team: `ecells-projects-3c3b03d7`
- To deploy: set git user.email = gemc99@me.com, then `npx vercel deploy --prod --token <token> --yes`
- Preferred cadence for Orbit check-ins (30m / 60m):
