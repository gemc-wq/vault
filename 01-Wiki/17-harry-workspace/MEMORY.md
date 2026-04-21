# MEMORY.md — Long‑Term Memory (curated)

> This file is intentionally *curated*, not a raw log.
> Add stable facts, preferences, ongoing projects, and high-signal decisions.
> Keep sensitive/private details out unless the user explicitly asks.

## Identity & Preferences

- **User:** Cem Celikkol (he/him). Prefer calling him **Cem**.
- **Timezone:** America/New_York.
- **Assistant identity:** **Harry** (COO at Ecell Global). Signature: ⚡.
- **Tone / vibe preferences:** direct, technical, proactive; low fluff; ask before external actions.

## Setup Notes

- This OpenClaw instance is an upgrade from an existing clawdbot.
- Prior “memory” moved over so far is a SQLite file (`memory/main.sqlite`) that appears to be an embedding/vector store (not markdown memory).

### Shared Drive / rclone (canonical project store)

- **rclone remote:** `gdrive:`
- **Root:** `gdrive:Clawdbot Shared Folder/`
- **Preferred projects root:** `gdrive:Clawdbot Shared Folder/Brain/Projects/`
- **Windows local mirror:** `C:\Users\gemc\clawd\gdrive_shared\` (e.g., `...\Brain\Projects\...`)
- Use `rclone sync` to refresh local mirror; use `rclone copy/copyto` to push artefacts to the Shared Drive.

## Ongoing Projects / TODO

- [ ] If desired: parse old `C:\Users\gemc\.clawdbot\agents\main\sessions\*.jsonl` and distill key preferences + projects here.

## Ops Learnings / Tooling

- **2026-03-03 nightly (Tue):** Supabase approvals check = **0 pending**. BigCommerce catalog health audit completed (1.9M products, $800K inventory value). Key findings: (1) 8 SKUs with NEGATIVE total_sold — possible return fraud or data issue, investigate urgently; (2) ~200 wallet cases mis-priced at $17.95 vs standard $21.95 — easy P0 margin fix; (3) 2,000-5,000 Huawei/OPPO/Nokia device SKUs are dead weight (0 sales, regional devices); (4) University tablet case segment (HTPCR-TABLET-IMGC*) has 0 sales across all designs — review/hide; (5) Placeholder SKUs at $2.25-$3.00 (screen protectors + blank shells) need audit. Full report: C:\Users\gemc\clawd\memory\nightly-output-2026-03-03.md
- **2026-03-04 nightly (Wed):** Supabase approvals check = **0 pending**. Trend Intelligence completed. Key signals: (1) GTA 6 confirmed Nov 19 2026 — P0 brief "Vice & Neon" (Miami aesthetic, no license needed, 8-month window); (2) Mob Wife dark luxury still surging Feb/Mar 2026 — "Dark Empire" brief, WWE Women's Division natural fit (Rhea Ripley); (3) Pearl/Rhinestone phone-cases-as-jewellery viral on TikTok (OSSA brand) — "Pearl Baroque" brief, Peanuts "Snoopy in Pearls" concept is high-viral-potential; (4) Chaos Culture / Gen Alpha aesthetic = skeleton/maximum-noise/anti-design — "Chaos Kids" brief fits WWE Judgment Day; (5) Quiet Luxe Botanical VALIDATED by Spring 2026 Vogue + r/fashion — HP Herbology + Brighton Spring briefs confirmed P0. Full report: C:\Users\gemc\clawd\memory\nightly-output-2026-03-04.md
- **2026-03-04 design brief status:** Brief 05 (Quiet Luxe Botanical / HP Herbology / Brighton Spring) = should already be in Ava/Iris queue from Mon intel — chase status. Brief 01 (Vice & Neon) = new P0, delegate today.
- **2026-02-27 nightly:** Supabase approvals check returned **0 pending**.
- **2026-02-27 trend intel:** Strong signals around **liminal/backrooms industrial aesthetics**, **millennial retro gaming nostalgia**, and **AI/deepfake glitch discourse** as graphic language.

- **2026-03-02 trend intel (Monday nightly):**
  - 🔥 **Pokémon 30th Anniversary** = #1 viral nostalgia moment March 2026. HCD has NO Pokémon license — Peanuts Nostalgia Archive brief is the mitigation. Flag Pokémon/Nintendo for BD pipeline.
  - 🔥 **Hockey jersey aesthetic** surging in streetwear (Complex Jan 2026). NFL × jersey-style graphics = P0 brief "Gridiron Jersey" — 128 SKUs potential across 32 teams.
  - 🔥 **Spring 2026 Vogue trend** = Morandi pastels (chalky, low-sat), botanicals, fringe, expressive individuality. Directly feeds Harry Potter Herbology and Brighton Spring Edit briefs.
  - 📱 **Y2K sticker collage format** = high commercial performer on clear cases. Peanuts archive collage = low effort, high revenue.
  - 🎬 **Studio Ghibli / Kiki's IMAX remaster** = anime nostalgia signal. HCD has no Ghibli license — BD gap to note.
  - 5 design briefs generated: Gridiron Jersey (NFL), Peanuts Nostalgia Archive, HP Herbology Spring, WWE Chaos King, Brighton FC × Spring Morandi.
  - P0 actions: delegate briefs 01+02 to Ava's Creator agents (Echo/Iris) immediately.
  - Brighton FC eco-pilot SKU (compostable material) = whitespace vs Pela — include in next CEO briefing.

- **2026-03-01 competitor intel (updated):**
  - **Casely** = #1 ranked in ALL Feb/Mar 2026 brand roundups. "Casely Club" subscription (monthly/quarterly) = their key differentiator. ~$30-45 price point. Design-led DTC. ZERO licensed IP. **Urgent gap: HCD must pilot "HCD Club" subscription with rotating licensed IP drops before Casely gains more ground.**
  - **Pela** = #2 eco/sustainable (compostable). Gen Z appeal. No licensed IP. HCD whitespace: eco + licensed pilot (Brighton FC compostable, Peanuts Earth Day).
  - **Mous** = Premium engineering ($40-80). Aramid fiber, no licensed IP, no subscription. Low direct threat.
  - **Amazon March 2026:** Tortoise Shell/Leopard #1 new release (iPhone 17). iPhone 17 = dominant device in all bestseller snippets. MagSafe = table stakes. Glitter + floral strong.
  - **Strategic synthesis:** HCD moat (licensed IP + JIT) = intact but underexploited. No competitor can do licensed + subscription + eco. That combo = Category of One.
  - **Top 3 P1 actions:** (1) HCD Club subscription pilot, (2) iPhone 17 catalog audit, (3) MagSafe listing sweep.

- **2026-02-28 competitor intel:**
  - **Casetify** = #1 ranked competitor / market leader. Design-first, artist marketplace model, celebrity + selective licensed collabs (Pokémon, Hello Kitty, major sports — not broad). Est. $300M+ revenue. Premium price point $50-80+. Impact Series (eco/compostable). **No subscription model** — gap HCD could exploit. ZERO broad licensed IP portfolio — HCD's core moat.
  - **Pela** = Eco/sustainable cases (compostable). No licensed IP. Unique segment, uncontested by HCD.
  - **Mous** = Premium engineering/protection. High price point. Not directly competing with HCD's design library.
  - **Amazon Feb 2026 top trends:** Tortoise shell/leopard animal prints surging, floral patterns strong, MagSafe now table stakes, silicone 56.64% market share.
  - **Priority actions identified:** (1) Pilot "HCD Club" subscription, (2) MagSafe listing audit across all marketplaces, (3) Eco-licensed pilot (Brighton FC / Peanuts in compostable material), (4) Animal print quick-launch via Creator pipeline.
  - **Pricing gap:** HCD at ~$10-20 on Amazon vs Casetify $50-80+ — test price elasticity on premium licensed designs.

- **web_search** working — Brave API key set in `.env`; rate-limits (429) during bursts, use spacing.
- **Apify** — `APIFY_API_KEY` + `APIFY_TOKEN` in `.env` (wired 2026-03-02)
- **Firecrawl** — `FIRECRAWL_API_KEY` in `.env` (confirmed present 2026-03-02)
- **X/Twitter** — `X_BEARER_TOKEN` in `.env` (wired 2026-03-02); ready for trend scraping
- **Walmart API** — `WALMART_API_KEY` + `WALMART_CLIENT_SECRET` in `.env` (added 2026-03-02). Auth confirmed ✅ (Bearer token, 900s TTL). Use for listings, catalog, orders, or reporting.
- **Gamma API** — `GAMMA_API_KEY` in `.env` (added 2026-03-02). Endpoint: `POST https://public-api.gamma.app/v1.0/generations`, poll: `GET /generations/{id}`. 4,964 credits remaining. First deck generated: https://gamma.app/docs/9xe27j65rnvopfy (HCD 2026 Creative Direction — 3 briefs)
- **browser** tool unavailable (timeout). Fallback: `web_fetch` + Reddit JSON feeds directly.
- **PowerShell gotcha:** avoid inline `&` querystrings inside `powershell -Command "..."` (quoting can break); write a `.ps1` script and execute it for reliable API calls.
- **Catalog health:** device-model gap detection depends heavily on SKU parsing; current heuristic (only `IPH*`/`SAM*`) is too narrow for OPPO/Xiaomi/Tablet SKUs.

## TTS / Voice
- **Harry TTS:** ElevenLabs provider, voice `2UMI2FME0FFUFMlUoRER` (Cem-specified, 2026-03-02). Correct API key `sk_13b47d30058...` confirmed. **Root cause of wrong voice (fixed 2026-03-03):** `C:\Users\gemc\.openclaw\tts-voice.json` was a hidden override file hardcoded to Daniel voice (`onwK4e9ZLuTAKqWW03F9`) — bypassing `openclaw.json` entirely. Now updated to `2UMI2FME0FFUFMlUoRER`. OpenAI `onyx` configured as secondary but needs billing credit at platform.openai.com before it'll work.
- **Ava ElevenLabs voiceId:** `OgJx1vCzNCD1EQHT212Ls`
- **Ava ElevenLabs voiceId:** `OgJx1vCzNCD1EQHT212Ls`

---

## Infrastructure (stable refs)

### Machines
| Agent | Host | Tailscale IP | OS | OpenClaw ver |
|-------|------|-------------|-----|--------------|
| Harry | HP_Cem | `100.120.86.40` | Windows 10 x64 | v2026.3.2 ✅ |
| Ava | Cems-iMac-3 | `100.91.149.92` | macOS | v2026.2.26 |

### SSH (Harry → Ava)
- `ssh clawdbot@100.91.149.92` (passwordless key auth; password fallback = "Harry")
- Must prefix PATH on iMac: `env PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin`
- Ava workspace: `/Users/clawdbot/.openclaw/workspace`
- openclaw binary: `/opt/homebrew/bin/openclaw`

### OpenClaw Config Paths
- Harry: `C:\Users\gemc\.openclaw\openclaw.json`, `C:\Users\gemc\.openclaw\.env`
- `.env` contains: `ELEVENLABS_API_KEY`, `ANTHROPIC_API_KEY`, `BRAVE_API_KEY`
- Credentials source: `C:\Users\gemc\clawd\gdrive_shared\Brain\Credentials\API Keys for Ava (1).txt`

### Supabase
- **Project 1 (catalog):** `nuvspkgplkdqochokhhi`
- **Project 2 (orders/inventory):** `auzjmawughepxbtpwuhe`
- Seed migration committed to `ecell-ops` repo (`37b7acb`): SQL, CSVs, seed script, README
- Security Advisor: `SECURITY DEFINER` view warnings pending remediation

### Cloud Run
- Service: `ecell-dashboard` | Project: `opsecellglobal` | Region: `us-east1`
- URL: `https://ecell-dashboard-786712421741.us-east1.run.app`
- Latest revision: `ecell-dashboard-00027-k6w`
- BigQuery cross-project IAM Option A configured (queries `instant-contact-479316-i4`)
- Service: `sales-dashboard` | Project: `opsecellglobal` | Region: `us-east1`
- URL: `https://sales-dashboard-786712421741.us-east1.run.app`
- Repo: `https://github.com/gemc99-boop/sales-dashboard` — 8 tabs, FX→USD, 2.8M orders
- Revenue field: `Net_Sale` (GBP_Price always empty); FX via `USD_CONVERSION` CASE in server.js
- Service: `sales-dashboard-v2` (old, can retire) | same project/region

### Shared Drive Structure
```
gdrive:Clawdbot Shared Folder/
  Brain/
    Org/START_HERE.md          ← boot orientation for both agents
    Handoffs/{inbox,doing,done}.md
    SOPs/AGENT_MEMORY_SOP.md
    MEMORY_ARCHITECTURE.md     ← Supabase pgvector full design
    BRAIN_INDEX.md
    Credentials/API Keys for Ava (1).txt
    Projects/goheadcase/goheadcaseBigCommerceCode2025/node_modules/  ⚠️ HUGE
```
- ⚠️ Always use `--exclude "node_modules/**"` in ALL rclone sync commands

### Handoff System (Ava ↔ Harry)
- **Harry → Ava:** SSH-write `HANDOFF_FROM_HARRY.md` to `/Users/clawdbot/.openclaw/workspace/`
- **Ava → Harry:** `handoff_to_harry.sh` at `/Users/clawdbot/.openclaw/workspace/handoff_to_harry.sh` (rclone-based, appends to `Brain/Handoffs/inbox.md`)
- Ava → Harry direct SSH blocked (Windows `sshd` not installed; needs admin elevation to enable)
- Rollback bundle: `C:\Users\gemc\Desktop\clawdbot_workspace_backup_20260223_223153.bundle`

---

## Agent Roles & Model Routing

| Role | Agent | Model | Cost |
|------|-------|-------|------|
| COO (main) | Harry | Sonnet 4.6 (Anthropic API) | $$ |
| CPSO (main) | Ava | Sonnet 4.6 (ChatGPT OAuth) | ~free |
| CEO sub-agent | (spawn on demand) | Opus 4.6 | $$$ max 2-3/day |
| Coding sub-agents | Forge, Spark | Codex 5.3 (ChatGPT OAuth) | ~free |
| Research | Loom, Bolt | Gemini Flash | near-free |
| Analytics | Atlas | Kimi K2.5 | free |

**Ava's team:** Echo (Copy/Sonnet), Iris (Design/Gemini Nano), Loom (Research/Flash), Bolt (Scout/Flash), Atlas (Analyst/Kimi), Forge (Builder/Codex), Spark (Builder2/Codex)

---

## Google Gemini CLI OAuth (2026-03-03)
- OpenClaw supports `google-gemini-cli` OAuth provider natively
- Default model: `google/gemini-3-pro-preview`
- Uses existing gcloud OAuth (`gemc@ecellglobal.com`) — no API key needed
- Cem interested in switching main LLM from Sonnet → Gemini 3 Pro via OAuth
- **Recommendation:** Test in sub-agent first, then cut over if stable
- Config: add `google:default` auth profile + set primary model to `google/gemini-3-pro-preview`

## Supabase Account Note (2026-03-03, corrected)
- Both projects (`nuvspkgplkdqochokhhi` + `auzjmawughepxbtpwuhe`) are under **gemc-wq's Org** (personal), NOT a separate ecellglobal org
- New Supabase key format (`sb_secret_*` / `sb_publishable_*`) returns 401 on REST API — use old JWT service_role key instead
- `walmart_listings` table is in Project 2 (`auzjmawughepxbtpwuhe`) — JWT key works ✅
- Walmart API field mapping: `productName` and `productType` are at TOP LEVEL of item object (not under `itemDetails`)

## Open Projects (as of 2026-03-03)

- [ ] **Ecell Spin-offs Portfolio** (`projects/ecell-spinoffs/`): Parent project for all ventures outside core Ecell/HCD ops. Trigger for own OpenClaw instance = recurring ops or separate customers. Currently managed by Harry.
  - [ ] **AI for Small Business** (`projects/ecell-spinoffs/ai-for-small-business/`): Spin-off website/platform for SMBs adopting AI. Format TBD (content site / SaaS / audit tool). Needs Cem input on value prop + monetisation before scoping.
  - [ ] **MIRROR-PRODUCT** (`projects/ecell-spinoffs/memory-virtual-assistant/`): Productised version of Project MIRROR — Obsidian-style persistent memory + validation loop for personal AI assistants, sold to consumers. Core moat: user validation loop (nonsense / valid idea / valid statement) shapes assistant behaviour = personal RLHF. Architecture: MD files (storage) + pgvector (computation) + Obsidian graph (presentation) + Telegram bot (MVP validation UI). Build for us first → prove loop → package as product. Key open questions: Obsidian plugin vs standalone app, primary voice capture channel for Cem, business model.
- [ ] **Project MIRROR** (Digital Replica / Personal AI Model): Build a digital replica of Cem — capture voice, email, calendar, social, docs → process → Supabase pgvector → dynamic persona model. Spec: `projects/user-replica/README.md`. Gamma deck: https://gamma.app/docs/wonz00epc4evfso. Phase 1 ready to start — awaiting Cem confirmation of primary voice capture channel.
- [ ] **Walmart × Amazon Gap Analysis** (`projects/walmart-amazon-gap/README.md`): Sync Walmart 95k listings + Amazon CSVs → Supabase matrix → momentum scoring → upload gaps to Walmart. Blocked on: (1) Cem runs CREATE TABLE SQL in Supabase P2, (2) Cem exports 2 Amazon CSVs (All Listings + Business Report 30d).


- [ ] **PO Upload Workflow** (ecell.app, part of NBCU project): Phase 1 = UI upload POs → FedEx CSV; Phase 2 = FedEx label API; Phase 3 = Xero CSV/API import. Spec: `projects/po-workflow/README.md`. Delegate to Forge/Spark.
- [ ] **Xero integration**: Import POs/SOs into Xero (ECOM software). CSV primary path; research API key availability. Part of PO Workflow Phase 3.
- [x] **TTS → OpenAI**: Switched to OpenAI TTS, voice "onyx" (deep male). `OPENAI_API_KEY` in `.env`. ElevenLabs kept as fallback config.
- [x] OpenClaw updated on Harry Windows: v2026.3.2 ✅ (2026-03-03). Fix: stop gateway → `npm i -g openclaw@latest` → restart (EBUSY if gateway running during install)
- [ ] Supabase pgvector Phase 1: run SQL from `MEMORY_ARCHITECTURE.md`, set env vars, test `memory_ops.ps1`
- [ ] Add `.rcloneignore` to exclude `node_modules/**` from Brain Drive syncs
- [ ] Create `WORKFLOW_AUTO.md` — draft standard workflow doc
- [ ] Supabase Project 2: apply seed SQL + CSV imports; integrate into `parse_sku()`
- [ ] NBCU `recipientLine2`: tighten parsing (strip "Invoice Terms Net 30 Days" suffix); regen batch CSV
- [ ] Fix Sales Dashboard tile URL (still pointing to old GitHub Pages URL)
- [ ] Enable Windows OpenSSH Server (admin required) for direct Ava → Harry SSH
- [ ] Supabase Security Advisor: remediate `SECURITY DEFINER` view warnings
- [ ] ecell.app Sales Dashboard v1: wire BigQuery views + Amazon CSV ingestion

## Key Decisions (durable)

- Harry = autonomous COO: orchestrates, delegates, minimal CEO interrupts, metrics-grounded
- Ava = CPSO: owns design/UX/content/e-commerce strategy
- Memory: Supabase pgvector (primary) + Qdrant (backup); `text-embedding-004`; 3-tier (stable/active/episodic); namespace `harry|ava|shared`
- Ava → Harry handoff = rclone (not reverse SSH)
- START_HERE.md = required boot read for both agents after restart/compaction
- FedEx workflow: CSV only; 0.5 LBS, 11×7×1, FedEx Ground, ref = PO, bill 3rd-party
- BigQuery: Option A cross-project IAM; sales safe mode = Amazon CSV first, SP-API as R&D
- Vercel account: `gemc99-boop` / `gemc99@me.com`; team `ecells-projects-3c3b0d7`
- Orbit PM: `https://orbit-pm.vercel.app/tasks` (no auth)

## Ecell Global / HCD Quick Facts

- Revenue: $64M/yr (2025); 50+ employees; offices UK/USA/DE/PH/CN/AU
- 4M cases/yr capacity; 8M+ sold historically; 8,000+ designs; 300+ device models
- Licensing: NFL, WWE, Peanuts, Harry Potter, Brighton & Hove Albion FC (2025-27)
- Casetify = #1 competitor (~$300M+, design-first, selective licensed, NO subscription)
- HCD moat: broad licensed IP + Just-In-Time manufacturing
- 2026 vision: "Sovereign Swarm" 5-agent autonomous enterprise (Watcher/Creator/Guardian/Merchant/Reaper)
