# Ecell Global — Agent Roster
**Updated:** 2026-04-13 | **Status:** ACTIVE — reflects confirmed decisions only
*Replaces AGENT_SWARM_PROPOSAL.md (Jan vision doc, now archived)*

---

## Live Agents

| Agent | Model | Platform | Role | Skills Owned | Status |
|-------|-------|----------|------|-------------|--------|
| **Athena** | Claude Opus 4.6 | ZEUS bot (Mac Studio) | Master Orchestrator | All (dispatch) | ✅ Live |
| **Ava** | Haiku + Advisor | OpenClaw (Mac Studio) | CPO — Strategy & Product | Sales strategy, Creative briefs | ✅ Live |
| **Hermes** | GLM 5.1 (OpenRouter) | OpenClaw (Mac Studio) | Autonomous Analytics | Intelligence, Sales data | ✅ Live |
| **Harry** | Kimi K2.5 → GPT-5.4 | OpenClaw (iMac) | Finance + Sentinel | Finance, Ops monitoring | ✅ Live (model upgrade pending) |

## Confirmed Changes (Not Yet Deployed)

| Change | Decision Date | Detail | Blocker |
|--------|-------------|--------|---------|
| Harry → GPT-5.4 | Apr 13 | Upgrade from Kimi K2.5, add Sentinel monitoring role | Cem to configure model on iMac |
| Hermes 5 weekly crons | Apr 13 | Self-improving loop: US/UK/DE listings + PULSE + memory review | First run: Apr 19 |
| Skill bucket reminders | Apr 13 | 9 AM + 2 PM ET weekday Telegram nudges | ✅ Deployed in heartbeat |

## Proposed Agents (Pending Build)

| Agent | Model | Role | Estimated Cost | When |
|-------|-------|------|---------------|------|
| **Echo** | Sonnet (SDK) | Marketing & Content | ~$10-20/mo | After Anthropic Agent SDK test |
| **Iris** | Gemma 4 ($0) | Wiki maintenance | $0 | After Sentinel proves out |

**Removed from proposal:** Guardian (compliance) — good idea but lower priority. Revisit Q3.

## Human Agents

| Person | Role | Communication |
|--------|------|--------------|
| **Jay Mark** | Technical Builder (Supabase, portals, ecell.app) | Email brief from Athena |
| **PH Creative Team** (6 staff) | Design production, print files | Slack #eod-creative |
| **PH Listings Team** | SKU uploads, marketplace listings | Slack #eod-listings |

## Routing Rules

```
Cem asks about...        → Route to
─────────────────────────────────────
Strategy, prioritisation → Ava
Sales data, analytics    → Hermes
Finance, royalties, Xero → Harry
Building, infra, portal  → Jay Mark (email) or Athena (if code)
Marketing, PPC, content  → Ava (until Echo deployed)
Crons, agent health      → Harry/Sentinel (when live) or Athena
Wiki, vault maintenance  → Athena (until Iris deployed)
```

## Cost Summary

| Component | Monthly |
|-----------|---------|
| Ava (Haiku + Advisor calls) | ~$15-30 |
| Hermes (GLM 5.1) | ~$5-15 |
| Harry (GPT-5.4) | TBD |
| Gemma 4 (local) | $0 |
| Athena (Opus subscription) | Included |
| **Total** | **~$20-50/mo** |

---

*The January AGENT_SWARM_PROPOSAL.md is archived at the same path. This doc reflects what's real.*
