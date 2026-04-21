# Ecell Global — Agent Team Configuration
> Last verified: 2026-04-14
> Canonical roster: ~/Vault/00-Company/AGENT_ROSTER.md

## Live Agents (Apr 14, 2026)

| Agent | Model | Platform | Role | Status |
|-------|-------|----------|------|--------|
| **Athena** | Claude Opus 4.6 | ZEUS bot (Mac Studio) | Master Orchestrator | ✅ Live |
| **Ava** | Haiku + Advisor (Opus 4.6) | OpenClaw (Mac Studio) | CPO — Strategy & Product | ✅ Live |
| **Hermes** | GLM 5.1 (OpenRouter) | Hermes CLI (Mac Studio) | Autonomous Analytics | ✅ Live |
| **Harry** | Kimi K2.5 (upgrading to GPT-5.4) | OpenClaw (iMac) | Finance + Sentinel | ✅ Live |

## Harry — Finance + Sentinel (Kimi K2.5 → GPT-5.4)
**Platform:** OpenClaw (iMac, Tailscale 100.91.149.92)
- Finance specs — Xero, royalties, COGS
- Sentinel monitoring role absorbed from Sentinel agent (Apr 13)
- Sentinel SOUL.md and SKILLS archived at `reference/sentinel-archived/`
- Does NOT build — specs only. Building goes to Jay Mark or Athena.
- Model upgrade to GPT-5.4 pending Cem config on iMac

## OpenClaw Sub-agents (Mac Studio)

| Agent ID | Role | Model | Used By |
|----------|------|-------|---------|
| main | Ava (CPO) | Haiku + Advisor | Strategy, briefs |
| sven | Creative Director | Gemini 3.1 Pro | Design corpus, marketing |
| bolt | Fast research | Gemini Pro | Quick lookups |
| atlas | Market analysis | Various | Deep analysis |
| prism | Data analysis | Gemini Flash | Forecasts |
| pixel | Cron executor | Gemini Flash | Scheduled tasks |
| sven2 | Creative backup | Various | Design overflow |
| iris | Wiki maintenance | Gemma 4 ($0) | Vault upkeep |

## Cost Policy
- Crons/heartbeats: FREE models only (Gemini Flash, Gemma 4) — never Anthropic API
- Ava: Haiku (cheap) + Opus Advisor (on-demand, ~400-700 tokens per call)
- Hermes: GLM 5.1 via OpenRouter (~$5-15/mo)
- Harry: Kimi K2.5 (cheap, upgrading to GPT-5.4)
- Heavy coding: Claude Code CLI (subscription) or Hermes
- Total: ~$20-50/mo

## Routing Rules
```
Strategy, prioritisation  → Ava (OpenClaw main)
Sales data, analytics     → Hermes (Hermes CLI, not OpenClaw)
Finance, royalties, Xero  → Harry (OpenClaw iMac)
Building, infra, portal   → Jay Mark (email) or Athena (code)
Marketing, PPC, content   → Ava (until Echo deployed)
Crons, agent health       → Harry/Sentinel or Athena
Wiki, vault maintenance   → Athena (until Iris deployed)
Middleware, SP-API code   → Athena (sole owner)
```

---
*Updated: 2026-04-14 by Athena — reflects verified agent state*
