# Project Board
*Auto-compiled: 2026-04-21 — Vault Compiler (claude-sonnet-4-6)*
*Source: 02-Projects/*, 03-Agents/*/memory/, 04-Shared/active/*

---

## 🟢 P0 — Critical Path (Active)

| Project | Priority | Owner | Status | Last Update | Notes |
|---------|----------|-------|--------|-------------|-------|
| amazon-data-analytics | P0 | Ava / Hermes | 🟢 Active | 2026-04-15 | Shipping template analysis: 9,778 FL-stocked FBM SKUs on wrong template; Phase 0 data validation required before execution |
| listings-db | P0 | Athena (build) | 🟢 Active | 2026-04-16 | Listings Data Pipeline PRD v1.0 + SOP v1.0 complete; Athena build in progress; unblocks Layer 0, procurement, template fixes |
| procurement | P0 | Athena (build) | 🟢 Active | 2026-04-16 | Procurement Priority Overrides System; depends on listings-db Phase A |
| ecell-app | P0 | Jay Mark | 🟡 Building | 2026-04-16 | Supabase tables for One Piece; Jay Mark active |
| inventory-ordering | P0 | Hermes / Athena | 🟢 Active | 2026-04-13 | 11 docs; inventory ordering app advisory V3 in vault |

---

## 🟡 P1 — Supporting (Active)

| Project | Priority | Owner | Status | Last Update | Notes |
|---------|----------|-------|--------|-------------|-------|
| delegait | P1 | Athena | 🟢 Active | 2026-04-13 | SaaS scoping; tracking generalizable workflows |
| sentinel-agent | P1 | Athena / Harry | 🟡 In progress | 2026-04-13 | Infrastructure monitoring spec; Harry model upgrade pending |
| iren-dreco | P1 | Athena | 🟡 In progress | 2026-04-09 | Print automation / creative→replication SOP |
| listing-forge | P1 | Jay Mark + Athena | 🟡 In progress | 2026-04-09 | ListingForge MVP; partially with Jay Mark, continuing in PH |
| infrastructure | P1 | Athena | 🟡 In progress | 2026-04-10 | Vault git hardening + compiler routine setup — PAUSED pending secret remediation |
| amazon-report-middleware | P1 | Athena | 🟡 Active | 2026-04-14 | Cloud Run Amazon Reports API; PRD + handoff docs present |
| shipping-template-dashboard | P1 | Ava / Jay Mark | 🔴 Blocked | 2026-04-15 | SP-API Product Listing role not granted (Cem + Patrick action required) |
| listings-intelligence | P1 | Hermes | 🟡 In progress | 2026-04-11 | Weekly listing intelligence; crons running on Gemma 4 Saturdays |

---

## 🔴 Blocked

| Project | Priority | Owner | Status | Last Update | Notes |
|---------|----------|-------|--------|-------------|-------|
| finance-ops | P1 | Cem | 🔴 Blocked | 2026-04-07 | 7-phase build; CLAUDE.md ready. Blocked on Xero OAuth setup (UK+US) |
| fulfillment-portal | P1 | Jay Mark | 🔴 Blocked | 2026-04-07 | Evri CSV + Supabase; raw BQ key files (`jaymark-bq-key.json`) must be deleted per security incident |

---

## ⚙️ On-Hold / Low Activity

| Project | Priority | Owner | Status | Last Update | Notes |
|---------|----------|-------|--------|-------------|-------|
| one-piece | P0 | Ava + Jay Mark | ⚙️ On-hold | 2026-04-07 | First Blueprint V3 pilot; waiting on creative direction |
| sku-staging | P1 | Ava | ⚙️ On-hold | 2026-04-07 | 10 docs; SKU Staging → Shopify → Walmart in progress |
| pulse-dashboard-v2 | P1 | Athena | ⚙️ On-hold | 2026-04-07 | Needs COGS data; PULSE leaderboard cron running |
| royalty-reporting | P1 | Harry | ⚙️ On-hold | 2026-04-07 | Harry finance scope; no update since Apr 7 |
| walmart-lister | P1 | Ava / Jay Mark | ⚙️ On-hold | 2026-04-07 | Blocked on ListingForge completion |
| new-products | P1 | Ava | ⚙️ On-hold | 2026-04-07 | 8 docs; Shopify Batch 1 (1,676 products) uploaded Apr 19 ✅ |
| shopify-repush | P1 | Ava | ⚙️ On-hold | 2026-04-07 | Shopify product spec V2; credentials need scrubbing (security incident) |
| eod-automation | P1 | Athena | ⚙️ On-hold | 2026-04-07 | EOD digest cron running; operational |
| supabase-rls-fix | ✅ | Cem + Athena | ✅ Done | 2026-04-07 | 0 Security Advisor errors; complete |

---

## ⚠️ Stale (no update in 14+ days — last activity Apr 7)

| Project | Last Update | Notes |
|---------|------------|-------|
| bigcommerce-api | 2026-04-07 | 1 doc; may be superseded |
| brain-memory-layer | 2026-04-07 | Gemma 4 RAG exploration |
| command-center | 2026-04-07 | Possibly superseded by PULSE/ecell.app |
| conversion-dashboard | 2026-04-07 | 0 docs, 12 files |
| dashboard-product-entry | 2026-04-07 | Low priority |
| ecell-website | 2026-04-07 | 1 doc, 14 files; ecellglobe.com redesign |
| finance | 2026-04-07 | 1 doc; superseded by finance-ops? |
| gemma4-rag | 2026-04-07 | Local RAG exploration |
| hermes-deployment | 2026-04-07 | Hermes OPERATIONAL_PLAYBOOK_V2 (140KB) |
| image-tests | 2026-04-07 | 0 docs |
| licensing | 2026-04-07 | 6 docs; royalty/license management |
| marketing | 2026-04-07 | 1 doc |
| nemoclaw-rd | 2026-04-07 | R&D; NemoClaw project |
| openclaw-saas | 2026-04-07 | 2 docs; SaaS scoping |
| org | 2026-04-07 | Org structure |
| playbook-revision | 2026-04-07 | 1 doc |
| product-intelligence-engine | 2026-04-07 | PIE spec (6 docs) |
| prune | 2026-04-07 | 2 docs — see POSSIBLE_DUPLICATE with prune-app |
| prune-app | 2026-04-07 | 1 doc — see POSSIBLE_DUPLICATE with prune |
| pulse-dashboard | 2026-04-07 | 6 docs — see POSSIBLE_DUPLICATE with pulse-dashboard-v2, pulse-unified |
| pulse-unified | 2026-04-07 | 5 docs — see POSSIBLE_DUPLICATE |
| target-plus-migration | 2026-04-07 | 1 doc; Target+ strategy |
| vault | 2026-04-07 | Vault automation project |
| walmart | 2026-04-07 | 2 docs — see POSSIBLE_DUPLICATE with walmart-lister, walmart-listing-audit, walmart-review-strategy |
| walmart-listing-audit | 2026-04-07 | 5 docs — see POSSIBLE_DUPLICATE |
| walmart-review-strategy | 2026-04-07 | 1 doc — see POSSIBLE_DUPLICATE |
| weekly-listing-audit | 2026-04-07 | 2 docs |
| world-cup-2026 | 2026-04-07 | 1 doc; 2026 World Cup licensing opportunity |

---

## 99-On-Hold

| Project | Last Update | Notes |
|---------|------------|-------|
| 99-On-Hold | 2026-04-16 | Staging folder; 1 doc |

---

*Total project folders: 54 | No `02-Projects/_INDEX.md` found (lint flag: NEW_FOLDER_WITHOUT_REGISTRATION)*
*Stale threshold: 14 days without modification on non-on-hold/completed projects*
