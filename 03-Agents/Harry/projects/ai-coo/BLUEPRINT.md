# Ecell Global — Master Business Process Blueprint
> Source: Cem's business process docs (Feb 8, 2026)
> **Updated:** 2026-03-25 by Ava — removed completed projects from active, added new strategic initiatives
> Cross-ref: MEMORY.md Master Architecture, AI Impact Analysis, Listings Management Spec

---

## Project Status Dashboard

| # | Project | Status | Owner | Impact | Notes |
|---|---------|--------|-------|--------|-------|
| 1 | **PULSE Dashboard** | ✅ LIVE | Ava | 🔴 HIGH | v2 live, champions, gap analysis, elbow detection |
| 2 | **Conversion Dashboard** | ✅ LIVE | Ava | 🔴 HIGH | Sessions/conversion analysis, quadrant view |
| 3 | **BQ→Supabase Sync** | ✅ LIVE | Ava | 🔴 HIGH | Nightly 3 AM cron, 2-day lookback |
| 4 | **Local SQLite Database** | ✅ LIVE | Ava | 🔴 HIGH | 8.5M listings (US+UK), EAN 480K, instant queries |
| 5 | **Slack Daily Digest** | ✅ LIVE | Ava | 🟡 MED | 8 AM cron, posts review back to channels |
| 6 | **ecell.app Dashboard** | ✅ LIVE | Ava | 🟡 MED | PULSE + all apps on Cloud Run |
| 7 | **HB401 Gap Tracker** | ✅ LIVE | Ava | 🟠 HIGH | 3,782 gaps posted to Slack |
| 8 | **Shopify Integration** | ✅ LIVE | Ava | 🟠 HIGH | API connected, products pushing, Target Plus flowing |
| 9 | **Walmart Lister Tool** | ✅ BUILT | Ava | 🔴 HIGH | CLI generates Shopify CSV + Walmart multi-variant |
| 10 | **Walmart API Uploader** | 🟡 BLOCKED | Ava | 🔴 HIGH | Feed format issue — Seller Center spreadsheet path |
| 11 | **Weekly Listing Intelligence** | 📋 SPECCED | Ava | 🔴 HIGH | 3 loops: targets, license monitor, attribution |
| 12 | **AutoPricer** | 📋 SPECCED | Ava | 🔴 HIGH | **BLOCKED: Amazon SP-API roles needed** |
| 13 | **Image Pipeline (Ecell Studio)** | 📋 SPECCED | Sven2 | 🔴 HIGH | AI mockup pipeline — critical post staff reduction |
| 14 | **Amazon SP-API Automation** | 🔴 BLOCKED | Ava | 🔴 HIGH | Needs Reporting + Pricing roles in Seller Central |
| 15 | **OnBuy UK Expansion** | 🟢 IN PROGRESS | Jay Mark | 🟠 HIGH | API lister built, test listings submitted |
| 16 | **Procurement/PO System** | 📋 SPECCED | Harry | 🟡 MED | PO→GR→Invoice matching |
| 17 | **Zero 2.0 Replacement** | 📋 PLANNED | Harry | 🟠 HIGH | Replace PH legacy system |
| 18 | **Email Triage** | 📋 SPECCED | Harry | 🟡 MED | N8N + Supabase email-memory |

### NEW — Strategic Initiatives

| # | Project | Status | Owner | Impact | Notes |
|---|---------|--------|-------|--------|-------|
| 19 | **OpenClaw SaaS Spin-off** | 🔬 DISCOVERY | Ava | 🔴 HIGH | NemoClaw starter kits for business verticals |
| 20 | **Flash Router / Memory Layer** | 🔬 DISCOVERY | Ava | 🟠 HIGH | Per-topic agent routing, semantic memory coordination |
| 21 | **PH Staff Restructuring** | 🟢 IN PROGRESS | Cem/Ava | 🔴 HIGH | 30% reduction (10 staff), handover plans needed |
| 22 | **New Product Launch** | 🟢 IN PROGRESS | Bea/Ava | 🟠 HIGH | MagSafe water bottles + metal wall art, lifestyle images |
| 23 | **Telegram Topic Agents** | 📋 READY | Ava | 🟡 MED | Per-topic agentId config, specialist agents per channel |

---

## Priority Stack (March 25 reprioritization)

### P0 — THIS WEEK
1. **PH Staff Restructuring** — 10 positions, handover plans, knowledge extraction before exits
2. **Walmart product upload** — Seller Center spreadsheet for champion designs
3. **New Product Lifestyle Images** — Water bottle + wall art AI images for listings
4. **Telegram Topic Agents** — Configure per-topic agent routing (approved by Cem)

### P1 — NEXT 2 WEEKS
5. **Image Pipeline production** — Critical now that graphics team is being reduced
6. **OnBuy UK go-live** — Jay Mark's API lister ready, awaiting OnBuy feedback
7. **Amazon SP-API roles** — Cem to add Reporting + Pricing roles in Seller Central
8. **Flash Router prototype** — Test GPT-5.4 nano vs Gemini Flash Lite for triage

### P2 — THIS MONTH
9. **AutoPricer prototype** — build agent + Supabase schema, test on Walmart first
10. **OpenClaw SaaS Discovery** — NemoClaw policy engine research, starter kit spec
11. **Weekly Listing Intelligence** — automated audit pipeline Phase 1

### P3 — NEXT QUARTER
12. **OpenClaw Starter Kits** — Package e-commerce kit, test on second business
13. **Kaufland DE** — German marketplace expansion
14. **Zero 2.0** — Legacy system replacement
15. **Procurement System** — PO management on Supabase

---

## Completed Projects (Archive)

| Date | Project | Outcome |
|------|---------|---------|
| Mar 21 | Listings Management Spec | 3 loops for PH team direction |
| Mar 21 | Conversion Baselines | US 2.89%, quadrant analysis, pricing candidates |
| Mar 21 | AutoPricer Spec | Full AutoResearch pricing loop documented |
| Mar 21 | COGS Handoff | Harry→Ava, Excel models complete |
| Mar 20 | Walmart Seller Center Template | Downloaded, field mapping complete |
| Mar 20 | First Shopify Order | #1083 PNUTCHA $19.95 |
| Mar 19 | HB401 Gap Analysis | 3,782 gaps, posted to Slack |
| Mar 19 | Walmart API Auth | Connected (read), item creation format WIP |
| Mar 18 | ecell.app Update | PULSE tile added, Cloud Run deployed |
| Mar 18 | Shopify API Connected | Products pushing, images mapped |
| Mar 15 | EAN Assignment Engine | 7,353 auto-assigned, 480K total mappings |
| Mar 15 | SEO Content Framework | Title templates, feature bullets per case type |
| Mar 15 | Conversion Dashboard | Sessions/conversion analysis, velocity comparison |
| Mar 15 | Local SQLite DB | 8.5M listings, instant queries, delta refresh |
| Mar 14 | SKU Staging Pipeline | Champions identified, Shopify CSV generator built |
| Mar 13 | BigCommerce API | 1.87M SKUs accessible, custom fields mapped |
| Mar 12 | gws CLI setup | Gmail/Calendar/Drive read-only access |
| Mar 12 | Inventory Tracker | 5,193 SKUs, 77% dead stock identified |
| Mar 12 | BQ→Supabase Sync | Nightly cron, 2-day lookback |
| Mar 11 | PRUNE | 823 dead designs identified, $66K/yr fee savings |
| Mar 10 | PULSE v1 → v2 | Live dashboard with champions, gaps, elbow detection |
| Mar 8 | SKU Parsing Rules | wiki/SKU_PARSING_RULES.md — F prefix, brand codes |
| — | Target Plus Migration | ✅ COMPLETE — Shopify→Target Plus flow live, 29+ orders |
| — | Memory/Embedding Layer v1 | ✅ COMPLETE — QMD + Gemini Embedding 2.0 + hybrid search configured |

---

## Blockers (Cem action required)

| Blocker | Impact | Action |
|---------|--------|--------|
| **Amazon SP-API roles** | Blocks: AutoPricer, Business Report automation, listing sync | Add Reporting + Pricing roles in Seller Central |
| **Royalty rates per license** | Blocks: COGS completion, pricing floor enforcement | Provide per-license royalty % |
| **PH Staff handover plans** | Blocks: clean transition | Approve handover task lists per person |

---

## Agent Assignments

| Agent | Current Focus | Next |
|-------|--------------|------|
| **Ava** | Blueprint update + Staff restructuring + Topic agent config | Flash Router prototype |
| **Harry** | Morning brief cleanup ✅ | PO Management system, Blueprint as project tracker |
| **Sven2** | Image gen (Gemini Pro + nano-banana) | Water bottle + wall art lifestyle images |
| **Atlas** | Analytics on-demand | Sales drop investigation (Mar 19 dip) |
| **Bolt** | Research on-demand | NemoClaw policy engine docs |
| **Pixel** | Data processing on-demand | UK listings analysis |

---

*This blueprint is the single source of truth for project status. Updated by Ava + Harry.*
*Harry: Wire your morning brief to read from this file on GDrive.*
*Location: `wiki/17-harry-workspace/projects/ai-coo/BLUEPRINT.md`*
*GDrive: `gdrive:Clawdbot Shared Folder/Brain/Projects/ai-coo/BLUEPRINT.md`*
