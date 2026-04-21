# Centralized Task Sheet
*All agents: check at session start, update at session end.*
*Last updated: 2026-04-11 | Updated by: Athena (Cem review session)*

---

## How To Use
- Every agent reads this file at session start (add to AGENTS.md/TOOLS.md)
- Pick up tasks assigned to you. Update status as you work.
- At session end: mark completed items, add notes, flag blockers
- Athena reviews during heartbeat rotation and escalates stale items

## Active Tasks

### Creative & Design (Pillar 1 — 30%)
| Task | Owner | Assigned | Status | Notes |
|------|-------|----------|--------|-------|
| One Piece visual direction brief | Ava | — | 🟡 In progress | Sven not active — Ava owns until Sven rebuilt |
| GoHeadCase email visual content | Ava | — | 🔴 Blocked on creative | 11K subs, zero campaigns. Needs creative assets |

### Sales & Marketplace (Pillar 2 — 25%)
| Task | Owner | Assigned | Status | Notes |
|------|-------|----------|--------|-------|
| Walmart top sellers refresh | Ava/Jay Mark | Apr 7 | 🔴 Not started | Codisto path — quickest revenue win |
| OnBuy UK API monitoring | Jay Mark | Apr 7 | 🟡 Listings started | Need order flow monitoring |
| Kaufland DE setup | Cem | Apr 7 | 🟡 NL tax DONE | EU OSS still pending |
| Amazon FBA conversion | Ava | Apr 7 | 🟡 In progress | New dashboard built, identifying high-ticket candidates |
| Target Strategy | Ava | — | 🟡 In progress | |
| Future Walmart strategy | Ava | — | 🟡 In progress | |
| SKU Staging → Shopify → Walmart | Ava | — | 🟡 In progress | Champions identified, uploading to Shopify |
| GoHeadCase Shopify store | Ava | — | 🟡 In progress | Ava owns |
| ListingForge MVP | Jay Mark + Athena | — | 🟡 In progress | Partly with Jay Mark, continuing in PH |

### Operations & Fulfillment (Pillar 3 — 20%)
| Task | Owner | Assigned | Status | Notes |
|------|-------|----------|--------|-------|
| **PH Database Access (Tailscale)** | Cem + Athena | Apr 10 | 🔴 TOP PRIORITY | Setup guide ready — Cem to execute steps 1-3 |
| Fulfillment Portal MVP | Jay Mark | Apr 7 | 🟡 Building | Evri CSV, Supabase tables |
| Label & print reconciliation | Jay Mark | — | 🟡 Priority | Falls under fulfillment/inventory tracking |
| Velocity-based reordering | Athena | — | 🟡 Priority | Depends on PH database access |
| ecell.app design code workflow | Jay Mark | Apr 7 | 🟡 Building | Supabase tables for One Piece |
| EU 3PL partner identification | Cem | Apr 7 | 🔴 Not started | Enabled by NL tax registration |
| ecellglobe.com redesign | PH Creative | — | 🟡 In progress | Waiting on PH creative team for better images |

### Marketing & Brand (Pillar 4 — 10%)
| Task | Owner | Assigned | Status | Notes |
|------|-------|----------|--------|-------|
| GoHeadCase email campaign setup | Ava | — | 🔴 Blocked on creative | Klaviyo or Shopify Email |
| Social marketing | Ava | — | 🟡 In progress | New initiative |

### Finance & Procurement (Pillar 5 — 10%)
| Task | Owner | Assigned | Status | Notes |
|------|-------|----------|--------|-------|
| Finance Ops Platform build | Cem (CLI) | Apr 8 | 🟡 CLAUDE.md ready | Vault/02-Projects/finance-ops/ — 7 phases |
| Xero OAuth setup (UK+US) | Cem | Ongoing | 🔴 Blocks Phase 1 | Needed before invoice posting works |
| PO corrections | Harry | Ongoing | 🟡 Needs Cem review | Cem flagged issues |
| DB migrations (inventory) | Harry | Apr 4 | 🔴 Not run | Needs execution |

### Intelligence & Analytics (Pillar 6 — 5%)
| Task | Owner | Assigned | Status | Notes |
|------|-------|----------|--------|-------|
| Listings KPI Dashboard | Athena | Apr 10 | 🟡 Scope complete | Phase 1: fix crons (done), Phase 2: KPI engine |
| Weekly listing intelligence | Auto (Gemma 4) | Ongoing | 🟡 Crons fixed | Switched to Gemma 4, runs Saturday |
| Amazon Prime shipping analysis | Hermes | Apr 7 | 🔴 Needs BQ data | Shipping method breakdown by SKU |
| BQ shipping method data pull | Hermes | Apr 7 | 🔴 Not started | Feeds Prime analysis |
| DelegAIt SaaS scoping | Athena | Apr 10 | 🟡 Tracking | Flag generalizable workflows |
| Vehicle integration | — | — | 🟡 In progress | |

---

## Completed (Recent — Apr 2026)
| Task | Owner | Completed | Notes |
|------|-------|-----------|-------|
| ✅ SOUL V4 deployed | Athena | Apr 10 | 9 sections, DelegAIt integrated, self-awareness engine |
| ✅ Adversary agent built | Athena | Apr 10 | Sonnet subagent, 5-question framework |
| ✅ Daily 6-pillar briefing | Athena | Apr 10 | 7:27 AM ET, Gemma 4, $0/day |
| ✅ Weekly crons switched to Gemma 4 | Athena | Apr 10 | US/UK/DE listings + PULSE, 600s timeout |
| ✅ Sales Dashboard V2 | — | Apr | Complete |
| ✅ Production Workflow SOP | — | Apr | Complete |
| ✅ Shipping Cart Optimization | — | Apr | Complete |
| ✅ Naruto Design Assets | — | Apr | Complete |
| ✅ CLC royalty breach resolved | Cem | Apr 9 | Awaiting CLC confirmation |
| ✅ Supabase RLS — all 45 tables | Cem + Athena | Apr 8 | 0 Security Advisor errors |
| ✅ EOD automation cron | Athena | Apr 8 | Daily 8AM EST → Telegram |
| ✅ Ava + Hermes comms verified | Athena | Apr 8 | OpenClaw API |
| ✅ Netherlands tax registration | Cem | Apr 7 | Enables Kaufland DE |
| ✅ 6 skill files created | Athena | Apr 7 | All pillars |
| ✅ Harry repurposed to Finance Agent | Cem | Apr 6 | Spec-only role |

## Removed (Cem directive 2026-04-11)
| Task | Reason |
|------|--------|
| Print file automation (Harry) | Replaced by IREN/DRECO unified project (GitHub) |
| Camera hole detection / all vision | Replaced by unified production project (GitHub) |
| Design file pipeline (Sven) | Sven not active — will revisit when Sven rebuilt |
| Themed micro-sites (Ava) | Abandoned — spend project, needs rethink |
| Website chatbot (Harry) | Moved to Ava, linked to GoHeadCase Shopify |
| PiPy | Replaced by PULSE |

---

## Process Rules
1. **Heartbeat check:** Every heartbeat, read this file, pick 1 unblocked task from ready queue, advance it
2. **Stale blocked items:** If blocked > 3 days, escalate to Cem with specific ask
3. **Completed items:** Move to completed section with date
4. **New tasks:** Add to appropriate pillar section
5. **Removed tasks:** Log reason in Removed section (don't delete silently)

---

*Updated 2026-04-11 by Athena after Cem's voice review of full task board.*
