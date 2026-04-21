# Specialist Agent Roster

## Cost Policy
- **Default model for all sub-agents: `gemini-flash`**
- Only escalate when the task genuinely needs it
- Opus 4.6 + thinking: ONLY for complex planning & architecture tasks
- **Heavy coding → Ava** (iMac has Claude Code + OpenAI Codex on subscriptions = FREE)
- Harry handles: orchestration, N8N, research, small scripts
- Review spend weekly

## Agent Roster

### ⚡ The Scout — `gemini-flash`
- Fast web research, market scans, trend monitoring
- Competitor price checks, news monitoring
- Quick summaries, data extraction
- **Cost:** ~$0.075/M in — basically free

### 🎨 The Creator — `gemini-pro`
- Image generation & editing (nano-banana-pro)
- Product mockups, design variations
- Marketing visuals, social media assets
- **Cost:** ~$1.25/M in — escalate only for image tasks

### 🔬 The Analyst — `gemini-flash` (default) → `gemini-pro` (deep dives)
- Financial modeling, data analysis
- Competitor deep-dives, SWOT analysis
- Start on Flash, escalate to Pro if insufficient
- **Cost:** Free to moderate

### 💻 The Engineer — `gemini-flash` (default) → `claude-code-wingman` (complex builds)
- Building apps, dashboards, automations
- N8N workflow development, API integrations
- Use Flash for scripts, escalate for architecture
- **Cost:** Free to moderate

### ✍️ The Writer — `gemini-flash`
- Product descriptions, marketing copy
- Email campaigns, listing optimization
- Flash handles 90% of writing tasks fine
- **Cost:** ~$0.075/M in

### 📊 The Merchant — `gemini-flash`
- Amazon listing optimization, SEO keywords
- Pricing analysis, ad copy
- Sales data analysis
- **Cost:** ~$0.075/M in

### 🎬 The Producer — `gemini-pro`
- Presentation decks (Gamma skill)
- Pitch materials, investor decks
- Only needs Pro for visual/complex outputs
- **Cost:** Moderate, use sparingly

## Escalation Rules
1. Start EVERY task on `gemini-flash`
2. If Flash output is insufficient → retry on `gemini-pro`
3. `opus` + thinking → ONLY for:
   - Complex multi-step automation architecture
   - Critical business decisions requiring deep reasoning
   - Tasks explicitly requested by Cem on Opus
4. N8N/chat bots → `gpt-4o-mini` via OpenRouter (cheapest for chat)

## Model Quick Reference
| Model | Cost (per 1M tokens) | Use Case |
|---|---|---|
| gemini-flash | $0.075 in / $0.30 out | Default everything |
| gemini-pro | $1.25 in / $10 out | Images, deep analysis |
| gpt-4o-mini | $0.15 in / $0.60 out | N8N chat/email bots |
| opus 4.6 | $15 in / $75 out | Complex planning ONLY |

---
*Created: 2026-02-06 — Approved by Cem*
