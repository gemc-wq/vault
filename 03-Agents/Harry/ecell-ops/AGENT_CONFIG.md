# Ecell Global — Agent Team Configuration
> Last verified: 2026-02-08
> Org chart: projects/design-automation/org-chart-feb2026.jpg

## Model Stack
| Model | Type | Cost |
|-------|------|------|
| Claude Opus 4.6 | API | Lead Agents (Harry, Ava) |
| Claude Code 4.6 | FREE | Coding CLI (Ava's iMac) |
| GPT-5.3 Codex | FREE | Coding CLI (Ava's iMac) |
| Gemini 3 Pro | API | Research + Images |
| Gemini Flash | CHEAP | Fast Tasks (default sub-agents) |
| Kimi K2.5 | CHEAP | Budget Tasks |

## Hierarchy

### 👑 Cem — CEO / Human-in-the-Loop
Final decisions, vision, and direction.

### ⚡ Harry — Lead Automator (Claude Opus 4.6 API)
Automation, infrastructure, and technical strategy. Backend & ops.

**Sub-agents (all gemini-flash by default):**
| Agent | Label | Role | Model | Escalation |
|-------|-------|------|-------|------------|
| Spark | spark-engineer | Engineer — Code, scripts, APIs, automations | gemini-flash | — |
| Radar | radar-scout | Scout — Web research, trends & intel | gemini-flash | — |
| Prism | prism-analyst | Analyst — Data analysis, deep dives & forecasts | gemini-flash | gemini-pro |
| Pixel | pixel-merchant | Merchant — Listings, ads, Amazon revenue engine | gemini-flash | — |
| Nexus | nexus-integrator | Integrator — Systems, N8N, APIs, workflows | gemini-flash | — |

### 🛡️ Ava — Lead Strategist (Claude Opus 4.6 API)
Creative strategy and team coordination. Delegates, decides, delivers.
**Location:** iMac node (when online)

**Sub-agents (Ava manages these):**
| Agent | Role | Model |
|-------|------|-------|
| Iris | Graphics — Vision to visual. Logos, mockups & assets | Gemini Pro |
| Echo | Writer — Brand voice, amplified. Copy & content | Flash |
| Forge | Builder — Blueprints to production. Next.js & React | GPT-5.3 FREE |
| Spark Builder 2 | Deep code reasoning. Architecture & refactors | Claude Code FREE |
| Flux | DevOps — Ships & scales. Deploys infrastructure | Flash |
| Bolt | Scout — Fast answers. Research & real-time lookups | Gemini Pro |
| Atlas | Analyst — Maps the market. Strategy & deep analysis | Kimi K2.5 CHEAP |

## Spawn Commands (Harry's agents)
```
sessions_spawn(label="spark-engineer", model="gemini-flash", task="...")
sessions_spawn(label="radar-scout", model="gemini-flash", task="...")
sessions_spawn(label="prism-analyst", model="gemini-flash", task="...")
sessions_spawn(label="pixel-merchant", model="gemini-flash", task="...")
sessions_spawn(label="nexus-integrator", model="gemini-flash", task="...")
```

## Cost Policy
- Sub-agents: gemini-flash ALWAYS (unless explicitly escalated)
- Harry (me): Opus 4.6 — orchestration & decisions only
- N8N bots: gpt-4o-mini via OpenRouter
- Heavy coding: route to Ava (free CLI subscriptions)
- Review spend weekly

---
*Saved: 2026-02-08 — Approved by Cem*
