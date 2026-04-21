# ATHENA ONBOARDING BRIEF
**Prepared by:** Ava (CPO/Strategy)
**Date:** 2026-04-05
**Purpose:** Get Athena up to speed and ready to plan, delegate, and unblock

---

## 🏢 WHO WE ARE

**Ecell Global** — licensed tech accessories manufacturer. $5M+ annual revenue.
- **Offices:** Orlando FL (US), UK, Philippines (PH), Japan, Hong Kong
- **Retail brand:** Head Case Designs (top 10 global eBay seller)
- **Products:** Phone cases (HTPCR, HB401, HLBWH, HB6CR, HB7BK, HC), desk mats (HDMWH), gaming skins (H8939)
- **Licensed brands:** NFL, NBA, WWE, Harry Potter, Naruto, Dragon Ball, DC, Peanuts, Premier League clubs, F1, and 30+ others
- **Marketplaces:** Amazon (US/UK/DE), Shopify (→Target Plus), TikTok Shop, Walmart (staging), GoHeadCase DTC

**North Star:** World's #1 licensed tech accessories company. Three pillars:
1. **Coverage** — every top design on every marketplace
2. **Speed** — order to doorstep < 48 hours
3. **Intelligence** — data-driven decisions

---

## 👥 YOUR TEAM

| Agent | Role | Model | Key Domain |
|-------|------|-------|------------|
| **Ava** | CPO / Strategy | Sonnet 4.6 | Sales, marketing, content, listings strategy |
| **Harry** | COO / Builder | Sonnet 4.6 (iMac) | Finance, ops, procurement, fulfillment builds |
| **Hermes** | Analyst | Kimi K2.5 | Amazon ads, pricing, Karpathy analytics, self-healing |
| **Jay Mark** | PH AI Guy | Human (back Mon Apr 7) | On-the-ground execution in PH — fulfillment, printing, Zero |
| **Echo** | Copy | Sonnet 4.6 | Listing copy, web copy |
| **Iris** | Design | Gemini Pro | Mockups, banners |
| **Bolt** | Scout | Gemini Flash | SEO, research |
| **Forge/Spark** | Builders | Codex GPT-5.4 | Next.js/React builds |

**Communication channels:**
- Ava ↔ Cem: Telegram
- Harry: SSH to iMac (100.91.149.92) or via GDrive handoff folder
- PH team: Slack (#eod-listings, #eod-creative-graphics, #graphics)
- Shared brain: `gdrive:Clawdbot Shared Folder/Brain/`

---

## 💰 COST CONSTRAINT (critical)

**Anthropic OAuth removed** — ALL Anthropic model calls are now billed API.
- Athena (Opus 4.6) = expensive. Use only for planning/orchestration, not execution.
- Crons and heartbeats: **FREE models only** (Gemini Flash, Gemini Pro OAuth, Codex OAuth, Kimi)
- Never assign background jobs to Athena, Ava, or Harry's Sonnet sessions.
- Rule: if a task is mechanical/repetitive → delegate to free model agent.

---

## 🔴 ACTIVE PROJECTS — STATUS

### 1. FULFILLMENT PORTAL (P0 — Jay Mark's Monday task)
**What:** Web portal for UK/PH/FL teams to manage shipping dispatch.
**Status:** Spec COMPLETE by Harry (`Brain/Harry/vault_export_2026-04-04/FULFILLMENT_PORTAL_SPEC.md`)
**Architecture:**
- BQ → Supabase order sync
- Next.js portal (Vercel)
- Evri CSV generation (MVP), Royal Mail + Amazon Buy Shipping (Phase 2)
- Write-back to Aurora `order_tracking` table (new table only, never touch ZERO's core tables)
**Blockers:**
- Jay Mark starts Monday — needs task briefed with spec
- Supabase schema migrations need running
- BQ service account credentials needed for portal
**Owner:** Harry builds, Jay Mark tests/operates
**Athena action:** Brief Harry with spec on Monday, assign Jay Mark testing role

### 2. XERO FINANCE APP (P0 — Harry's primary)
**What:** Internal finance ops app for AP automation + journal posting + reporting.
**Status:** Scope COMPLETE (`Brain/Harry/vault_export_2026-04-04/XERO_FINANCE_APP_SCOPE.md`)
**Built so far:**
- DB schema (11 new tables: POs, packing lists, supplier invoices, GRNs, stock alerts, inventory snapshots)
- Stock-out monitor (Airweave multi-lingual: EN/ZH/ES/TL)
- Procurement system Next.js app (built, deployed to `.next/`)
- PH order gap analysis (complete — see below)
**Blockers:**
- Xero auth (UK + US) pending — Harry needs OAuth tokens
- gog Gmail auth needs setup on Harry's iMac for email intake
- DB migrations need running
**Owner:** Harry
**Athena action:** Unblock Xero auth — get Cem to provide Xero OAuth credentials for UK + US orgs

### 3. PROCUREMENT SYSTEM (P1 — Harry)
**What:** Replace manual PH procurement with velocity-based PO generation.
**Status:** Gap analysis COMPLETE (Apr 1). Critical findings:
- 11 EOL items still in PH order (¥1,000 wasted)
- Negative qty data error (HTPCR-IPH17PRO: -163 units)
- All stock shipped to PH, should split: 70% PH / 15% UK / 15% FL
- Estimated shipping savings if split: **$1,014 per PO cycle** (64% reduction)
**Blockers:** Cem needs to approve split % and correct the negative qty error
**Athena action:** Get Cem decision on PO split and EOL exclusion this week

### 4. LISTING IMAGE AUTOMATION / LISTINGFORGE (P0 — Jay Mark + Forge)
**What:** Auto-generate product listing images from jig templates.
**Status:**
- Full IREN/DRECO reverse-engineering complete
- Lane 1 POC built and tested (Pillow-based composite image generation)
- Jig data loaded from PH MySQL (4,580 rows, iPhone 17 included)
- Rotation and corner radius logic written
**Next:** Jay Mark to run the PH print automation (IREN/DRECO) and provide modern jig rows
**Owner:** Ava/Forge build, Jay Mark operates in PH
**Athena action:** On Monday, brief Jay Mark: (1) access PH MySQL, (2) export current jig measurements for iPhone 13–17 series, (3) provide to Forge for Lane 1 completion

### 5. SHOPIFY → MARKETPLACE EXPANSION (P0 — Ava)
**What:** 1,803 HB401 gap designs ready for Shopify bulk upload.
**Status:** EANs confirmed, images from S3 CDN, CSV ready.
**Blocker:** Cem go-ahead to bulk upload 1,803 products.
**Athena action:** Get Cem's go-ahead this week.

### 6. AMAZON REPORTS AUTOMATION (P1 — cron)
**What:** Auto-download weekly Amazon Active Listings (US/UK/DE).
**Status:** Cloud Run API confirmed running. SOP written.
**Blocker:** One test run to confirm API output format matches manual download.
**Athena action:** Assign to Pixel (Flash, free) to run test this week.

### 7. NFL LICENSE RENEWAL (P0 — OVERDUE)
**Status:** Expired Mar 31. 90-day sell-off window. Can sell existing inventory through ~Jun 29.
**New production blocked.** $25K/yr renewal fee, ~$97K annualized revenue.
**Thread:** Cem replied to Archie (IMG) on Mar 16 re: channel plans.
**Athena action:** Follow up with Cem — is this being renewed or are we exiting NFL?

---

## 📊 KEY DATA SOURCES

| Source | What's in it | Access |
|--------|-------------|--------|
| BigQuery (`instant-contact-479316-i4`) | 2.8M orders, product master, order tracking | gcloud auth on Mac Studio |
| Supabase (`auzjmawughepxbtpwuhe`) | 305K orders, inventory, listings | Service role key in TOOLS.md |
| SQLite (`data/local_listings.db`) | US 3.6M + UK 5.2M Amazon listings | Local on Mac Studio |
| Amazon SP-API | Reports, sessions, inventory | Creds in TOOLS.md |
| BigCommerce (`otle45p56l`) | 1.87M SKUs, source catalog | Creds in TOOLS.md |
| Shopify (`yabfxs-zd`) | GoHeadCase store, orders | Admin token in TOOLS.md |

---

## 🔑 THIS WEEK'S PRIORITIES (Athena's action list)

### Monday (Jay Mark starts):
1. **Brief Jay Mark** — Send him: Fulfillment Portal spec + his role (tester/operator), jig export task for ListingForge
2. **Assign Harry** — Xero auth unblock: get UK + US OAuth tokens from Cem, run DB migrations

### This week:
3. **Shopify upload go-ahead** — Get Cem's approval for 1,803 HB401 bulk upload
4. **NFL decision** — Pin Cem: renew at $25K or exit? Affects creative planning.
5. **PO corrections** — Route Harry's gap analysis to Cem/PH: remove EOL items, fix negative qty, approve split %
6. **Amazon API test** — Delegate to Pixel (Gemini Flash): test Cloud Run API output vs manual download

### Ongoing delegation:
- Harry: Xero app + Procurement system + Fulfillment Portal build
- Ava: Listings content, design briefing, creative direction
- Hermes: Amazon ad analysis, pricing
- Forge: ListingForge Lane 1 completion once jig data arrives

---

## 🧠 RULES OF ENGAGEMENT

1. **Delegate everything executable.** Athena plans and unblocks — doesn't run SQL or write code.
2. **One question per blocker.** When escalating to Cem, bundle all questions in one message.
3. **Cost-aware routing.** Data/mechanical tasks → Gemini Flash (free). Strategic synthesis → Sonnet. Planning → Athena/Opus.
4. **GDrive = source of truth.** All deliverables go to `Brain/` on GDrive. Workspace = working copy.
5. **NFL is P0** until resolved — mention in every Cem touchpoint.

---

## 📁 KEY FILE PATHS

| File | Purpose |
|------|---------|
| `MEMORY.md` | Ava's long-term memory (full context) |
| `TASKS.md` | Active task queue |
| `wiki/` | Operations knowledge base (53 docs) |
| `projects/sku-staging/` | Shopify/Walmart pipeline |
| `projects/listing-forge/` | Image automation POC |
| `projects/licensing/` | NFL, NBA, etc. renewal drafts |
| `Brain/Harry/vault_export_2026-04-04/` | Harry's latest deliverables (on GDrive) |
| `data/local_listings.db` | SQLite listings database |
| `scripts/` | Analysis and sync scripts |

---

*Brief prepared by Ava | Updated 2026-04-05*
