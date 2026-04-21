# Ecell Global — Agent Team Configuration
> Last updated: 2026-02-17
> Approved by: Cem

---

## 👑 Cem — CEO / Human-in-the-Loop
Final decisions, vision, and direction.

---

## 🎯 AVA — Head of Sales & Marketing (Claude Sonnet 4.6 · API)
Content strategy, brand, customer-facing channels, website, Amazon ads.
Owns: ecellglobal.com redesign, GoHeadCase storefront, marketing campaigns.

### Ava's Team · Sales, Marketing & Creative

| Agent | Role | Responsibilities | Model | Cost |
|-------|------|------------------|-------|------|
| Echo | Copywriter | Web copy, Amazon listings, ad copy, campaign text, product descriptions | Claude Sonnet 4.6 | API |
| Iris | Designer | Brand visuals, mockups, creative assets, banners, logos | Gemini Nano Banana Pro | Gemini CLI OAuth |
| Loom | Researcher | Competitor teardowns, market research, landing page patterns, ad libraries | Gemini Flash | API / Gemini CLI OAuth |
| Bolt | Scout | SEO keywords, real-time lookups, quick research, trend spotting | Gemini Flash | API / Gemini CLI OAuth |
| Atlas | Analyst | Amazon ad strategy, pricing intelligence, performance reporting, market analysis | Kimi K2.5 | CHEAP |
| Forge | Web Builder | Front-end builds: ecellglobal.com, goheadcase.com (Next.js + React + Tailwind) | Codex CLI GPT-5.3 | FREE |
| Spark | Builder 2 | Deep code, complex architecture, headless Shopify POC | Codex CLI GPT-5.3 | FREE |

---

## ⚡ HARRY — Lead Automator / COO (Claude Opus 4.6 · API)
Backend ops, data pipelines, automation, infrastructure.
Owns: BigCommerce catalog, Shopify data pipeline, FBA analytics, integrations.

### Harry's Team · Backend & Ops

| Agent | Role | Responsibilities | Model | Cost |
|-------|------|------------------|-------|------|
| Pixel | Merchant | BigCommerce export, Shopify import pipeline, catalog management, SKU ops | Gemini Flash | API |
| Nexus | Integrator | Supabase, Design Hub API, Shopify metafields, N8N workflows | Codex CLI GPT-5.3 | FREE |
| Spark | Engineer | Backend automation, data scripts, APIs | Codex CLI GPT-5.3 | FREE |
| Radar | Scout | BigCommerce data pulls, catalog mapping, data recon | Gemini Flash | API |
| Prism | Analyst | Ops reporting, FBA analytics, data deep-dives | Kimi K2.5 | CHEAP |

---

## Model Stack

| Role type | Model | Provider | Cost |
|-----------|-------|----------|------|
| Ava (Lead) | Claude Sonnet 4.6 | Anthropic API | API |
| Harry (Lead) | Claude Opus 4.6 | Anthropic API | API |
| Content / Copy | Claude Sonnet 4.6 | Anthropic API | API |
| Design / Visual | Gemini Nano Banana Pro | Gemini CLI OAuth | OAuth |
| Research / Scout | Gemini Flash | API / Gemini CLI OAuth | Cheap |
| Analysis | Kimi K2.5 | Moonshot API | Very cheap |
| Coding / Building | Codex CLI GPT-5.3 | OpenAI Codex CLI | FREE |
| Merchant / Ops | Gemini Flash | API | Cheap |

---

## Active Workstreams

| Project | Lead | Support |
|---------|------|---------|
| ecellglobal.com redesign | Ava (strategy + copy) | Forge (build), Iris (visuals) |
| GoHeadCase POC / Shopify | Harry (data pipeline) | Ava (UX + content), Nexus (integrations) |
| Amazon ads | Ava + Atlas (strategy) | Echo (copy), Loom (research) |
| BigCommerce catalog export | Harry + Pixel | Radar (data) |
| ecell.app ops dashboard | Harry | Spark/Nexus (build) |

---

## Spawn Commands

### Ava's agents
```
sessions_spawn(label="echo-writer", model="anthropic/claude-sonnet-4-6", task="...")
sessions_spawn(label="iris-designer", model="google/gemini-nano-banana-pro", task="...")
sessions_spawn(label="loom-researcher", model="google/gemini-2.5-flash-preview", task="...")
sessions_spawn(label="bolt-scout", model="google/gemini-2.5-flash-preview", task="...")
sessions_spawn(label="atlas-analyst", model="moonshot/kimi-k2.5", task="...")
sessions_spawn(label="forge-builder", model="openai-codex/gpt-5.3", task="...")
sessions_spawn(label="spark-builder2", model="openai-codex/gpt-5.3", task="...")
```

### Harry's agents
```
sessions_spawn(label="pixel-merchant", model="google/gemini-2.5-flash-preview", task="...")
sessions_spawn(label="nexus-integrator", model="openai-codex/gpt-5.3", task="...")
sessions_spawn(label="spark-engineer", model="openai-codex/gpt-5.3", task="...")
sessions_spawn(label="radar-scout", model="google/gemini-2.5-flash-preview", task="...")
sessions_spawn(label="prism-analyst", model="moonshot/kimi-k2.5", task="...")
```

---

## Cost Policy
- Sub-agents: Gemini Flash or Codex CLI (free) by default
- Coding: Codex CLI GPT-5.3 (FREE) always first
- Writing: Claude Sonnet 4.6 for customer-facing copy; Kimi for drafts
- Analysis: Kimi K2.5 (cheapest capable model)
- Design: Gemini CLI OAuth (free via Google auth)
- Harry: Opus 4.6 for orchestration & decisions only
- Review spend weekly

---
*Last updated: 2026-02-17 — Approved by Cem*
