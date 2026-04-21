# Agent Roster — Ecell Global

## 🎯 Ava (Lead)
- **Model:** Claude Opus 4.6
- **Role:** Strategy, creative direction, coordination, direct comms with Cem
- **Handles:** Planning, delegation, brand decisions, memory management

## 🎨 Graphics Agent
- **Label:** `ecell-graphics`
- **Model:** Gemini Pro (image generation via REST API)
- **API Key:** Configured in ~/.gemini/settings.json
- **Role:** Logo design, mockups, hero images, social media assets, visual concepts
- **Endpoint:** `gemini-2.0-flash-exp-image-generation` via REST

## 💻 Builder Agent (Forge)
- **Label:** `builder`
- **Model:** GPT-5.3 via Codex CLI (`codex exec`)
- **Role:** Frontend/fullstack coding — Next.js, React, Tailwind, TypeScript
- **How to invoke:** `codex exec --approval-mode full-auto "task description"`
- **Workspace:** Project-specific directory (e.g., /Users/clawdbot/.openclaw/workspace/projects/)
- **Notes:** Authenticated via ChatGPT subscription (OAuth). Default model: gpt-5.3-codex

## 💻 Builder Agent 2 (Spark)
- **Label:** `spark`
- **Model:** Claude Opus 4.6 via Claude Code CLI (`claude -p`)
- **Role:** Second coding agent — complex architecture, multi-file refactors, deep code reasoning
- **How to invoke:** `claude -p "task" --max-turns 1 --output-format text` (requires PTY)
- **Notes:** Authenticated via Claude subscription (OAuth). Needs PTY to run non-interactively.

## ⚡ Scout Agent (Fast Research)
- **Label:** `scout`
- **Model:** google/gemini-3-pro-preview (or Flash when available)
- **Role:** Quick lookups, competitor checks, market data, news, fact-checking
- **Optimized for:** Speed over depth, 1-2 minute tasks

## 🔬 Analyst Agent (Deep Research)
- **Label:** `analyst`
- **Model:** google/gemini-3-pro-preview
- **Role:** In-depth market analysis, strategy reports, competitor deep-dives, data synthesis
- **Optimized for:** Thoroughness, multi-source analysis, 5-10 minute tasks

## ✍️ Writer Agent (Echo)
- **Label:** `writer`
- **Model:** google/gemini-3-pro-preview (Flash for drafts, Pro for polish)
- **Role:** Website copy, marketing content, social media posts, email campaigns, SEO
- **Tone:** Matches Ecell brand voice — professional, trustworthy, globally-minded
- **Note:** First drafts on Flash, Ava reviews/polishes. No need for Opus rates on copy.

## 🚀 DevOps Agent (Flux)
- **Label:** `devops`
- **Model:** google/gemini-3-pro-preview (Flash default)
- **Role:** Deployments, Vercel, GitHub, CI/CD, infrastructure, server config
- **Has access to:** Vercel token, GitHub (pending PAT)
- **Note:** Deploy scripts and infra don't need heavy models.

---

## How It Works
- Ava (me) coordinates and delegates to specialists
- Agents run as sub-sessions via `sessions_spawn`
- Builder agent uses Codex CLI (`codex exec`) for code tasks
- Graphics agent uses Gemini REST API for image generation
- All others use their respective LLM models via Clawdbot's model routing

## API Keys & Auth
- **Anthropic:** API key configured ✅
- **Google/Gemini:** API key configured ✅
- **OpenAI/Codex:** ChatGPT OAuth (signed in) ✅
- **Vercel:** Token (session-stored)
- **GitHub:** PAT needed ❌
