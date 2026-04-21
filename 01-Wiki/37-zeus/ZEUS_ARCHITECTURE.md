# Athena — Infrastructure Agent Architecture (v3.0)
*(formerly Zeus)*
*Created: 2026-04-04 | Owner: Cem (CEO) | Status: 🟡 In design/build*

---

## What Zeus Is

Zeus is a slim orchestration agent built on the **Anthropic Agent SDK (Opus 4.6)**, designed to:
- Orchestrate all agents through a **single endpoint** — the OpenClaw gateway
- Route tasks intelligently to free/local models to minimise Anthropic API spend
- Coordinate Hermes, Gemma 4 (local), and all OpenClaw agents from one place

Zeus is **not** a replacement for OpenClaw. It is a **thin orchestration layer on top**.

---

## Why Zeus

Anthropic is increasing prices for third-party tool usage. Every heartbeat, cron, and sub-agent call through OpenClaw burns Anthropic API tokens. Zeus acts as the routing brain — uses Opus 4.6 only for orchestration decisions, routes everything else to free/local models.

---

## v3.0 Unified Architecture — One Endpoint

Zeus talks to **everything through OpenClaw's gateway at `localhost:18789`**.

```
Mac Studio (M4 Max, 36GB RAM) — all local, loopback only
│
├── Zeus (Anthropic Agent SDK, Opus 4.6)
│     └── Single outbound endpoint: http://127.0.0.1:18789
│
└── OpenClaw Gateway (port 18789)
      ├── OpenAI-compatible HTTP API
      ├── Bearer token auth
      ├── openclaw/main          → Ava (Sonnet 4.6)
      ├── openclaw/atlas         → Atlas (GPT-5.4 Codex, free OAuth)
      ├── openclaw/bolt          → Bolt (Gemini Pro, free OAuth)
      ├── openclaw/pixel         → Pixel (Gemini Flash, free OAuth)
      ├── openclaw/prism         → Prism → Gemma 4 26B (local, see below)
      ├── openclaw/sven          → Sven (Gemini Pro, free OAuth)
      ├── openclaw/iris          → Iris (GPT-5.4, free OAuth)
      ├── openclaw/hermes-agent  → Hermes (via ACP, already registered)
      ├── openclaw/codex         → Codex (free OAuth)
      └── openclaw/sven2         → Sven2 (Gemini Pro, free OAuth)
```

**Hermes is already registered** in OpenClaw config as an ACP-allowed agent (`acp.allowedAgents: ["hermes-agent","codex","claude-code"]`). Zeus reaches Hermes via `openclaw/hermes-agent` — no separate endpoint needed.

**Gemma 4 26B MoE** runs locally via Ollama on port 11434. OpenClaw is wired to it as a provider so Prism (and any agent) can use it as a model.

---

## Gemma 4 Integration into OpenClaw

Ollama exposes an OpenAI-compatible endpoint at `http://127.0.0.1:11434`. Wire it into OpenClaw as a provider:

```json
"models": {
  "providers": {
    "ollama": {
      "baseUrl": "http://127.0.0.1:11434",
      "api": "openai-completions",
      "models": [
        {
          "id": "gemma4:26b",
          "name": "Gemma 4 26B MoE (local)",
          "contextWindow": 131072,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```

Then Prism's model → `ollama/gemma4:26b`. Reachable via Zeus as `openclaw/prism`.

---

## Communication Pattern

```
Zeus sends task:
POST http://127.0.0.1:18789/v1/chat/completions
Authorization: Bearer <gateway_token>
{ "model": "openclaw/prism", "messages": [...] }

OpenClaw routes to Prism → Prism uses gemma4:26b via Ollama
Response returns to Zeus
```

Same pattern for every agent. One endpoint, one auth token, all 10 agents reachable.

---

## Task Routing Logic

| Task type | Model | Route |
|---|---|---|
| Orchestration / strategy | Opus 4.6 | Zeus direct (Anthropic) |
| Data analytics / SQL / pipeline | Gemma 4 26B | `openclaw/prism` |
| Research / web search | Gemini Flash | `openclaw/bolt` |
| Coding / architecture | GPT-5.4 Codex | `openclaw/atlas` |
| ETL / file processing | Gemini Flash | `openclaw/pixel` |
| Content / copy | Sonnet 4.6 | `openclaw/main` |
| Design / image QA | Gemini Pro | `openclaw/sven` |
| Hermes — Amazon ads, pricing, Karpathy analytics | Kimi K2.5 (free) | `openclaw/hermes-agent` or direct port 18791 |

---

## MCP — Scoped Role

MCP is for **tool/resource exposure only**, not agent messaging.

- Agent-to-agent messaging → `/v1/chat/completions` (already works)
- Zeus exposing tools to OpenClaw/Hermes → MCP server on Zeus
- Hermes exposing memory/resources to Zeus → MCP server on Hermes

---

## Zeus Design Principles

1. One endpoint — `localhost:18789`
2. Opus 4.6 only for orchestration — never for data/ETL tasks
3. Stateless — state lives in OpenClaw workspace, Hermes memory, vault
4. Budget gatekeeper — local/free first, Anthropic API last resort
5. Thin — routes and delegates, does not execute

---

## Phased Build Plan

### Phase 0 — Foundation *(now)*
- [x] Ollama installed on Mac Studio
- [x] gemma4:26b downloading (~17GB, ~10 min remaining)
- [ ] Wire Ollama as OpenClaw provider
- [ ] Switch Prism model to `ollama/gemma4:26b`
- [ ] Confirm `openclaw/prism` reachable and responding
- [ ] Confirm Hermes reachable as `openclaw/hermes-agent`

### Phase 1 — Zeus Basic Orchestration
- [ ] Zeus project location confirmed (Cem)
- [ ] Zeus calls `openclaw/prism` for first data analytics task
- [ ] Zeus calls `openclaw/bolt` for research
- [ ] Zeus has SOUL.md / operating instructions

### Phase 2 — MCP (tools/resources layer)
- [ ] Zeus MCP server for tools it owns
- [ ] Hermes MCP server wired into Zeus

### Phase 3 — Smart Routing + Budget Tracking
- [ ] Track Anthropic API cost vs free routing per task
- [ ] Zeus auto-selects cheapest capable model per task type

---

## Files
- This spec: `wiki/37-zeus/ZEUS_ARCHITECTURE.md`
- Zeus project: Mac Studio (location TBD from Cem)

---

## Agent Role Summary

| Agent | Model | Primary Role |
|---|---|---|
| **Zeus** | Anthropic Opus 4.6 | Orchestrator — routes tasks, budget gatekeeper |
| **Ava (main)** | Sonnet 4.6 | Strategy, project management, cross-pillar oversight |
| **Hermes** | Kimi K2.5 (free) | Sales analytics, Amazon ads optimisation, pricing adjustments, Karpathy project |
| **Prism** | Gemma 4 26B MoE (local) | Data analytics trial — pipeline, SQL, PULSE queries |
| **Atlas** | GPT-5.4 Codex (free OAuth) | Coding, architecture |
| **Bolt** | Gemini Pro (free OAuth) | Research, web search, trend spotting |
| **Pixel** | Gemini Flash (free OAuth) | ETL, file processing, data syncs |
| **Sven** | Gemini Pro (free OAuth) | Design, image QA, creative corpus |
| **Iris** | GPT-5.4 (free OAuth) | Design builds, nano-banana-pro skills |

---

## Open Questions
1. Where is the Zeus Claude Code project on Mac Studio?
2. Anthropic Agent SDK version being used?
3. Should Zeus get its own vault workspace under `vault/40-ai-workspaces/zeus/`?
4. Hermes gateway auth token for direct port 18791 access (needed for Zeus→Hermes direct channel)?
