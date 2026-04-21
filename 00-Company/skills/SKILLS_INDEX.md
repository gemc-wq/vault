# Ecell Global — Skills Framework V2
*Created: 2026-04-07 | Updated: 2026-04-13 by Athena*
*V2: Added Infrastructure skill, agent assignments, V3 Blueprint alignment*

---

## The Model
Skills are focused context windows loaded on demand and rotated through the heartbeat. Each skill = one business function with its projects, metrics, agents, and relevant knowledge. Skills map to agents: each agent owns specific skills and is accountable for their delivery.

## Seven Skills (Weighted)

| # | Skill | Weight | File | Primary Agent | Supporting | Heartbeat |
|---|-------|--------|------|---------------|------------|-----------|
| 1 | **Creative & Design** | 25% | [01-CREATIVE.md](01-CREATIVE.md) | Sven (Gemini 3.1 Pro) | Ava (briefs) | 3x/cycle |
| 2 | **Sales & Marketplace** | 25% | [02-SALES.md](02-SALES.md) | Hermes (analytics), Ava | Echo (content) | 2x/cycle |
| 3 | **Operations & Fulfillment** | 15% | [03-OPERATIONS.md](03-OPERATIONS.md) | Jay Mark (builder) | Sentinel (monitoring) | 1x/cycle |
| 4 | **Marketing & Brand** | 10% | [04-MARKETING.md](04-MARKETING.md) | Echo (SDK subagent) | Ava (strategy) | 1x/cycle |
| 5 | **Finance & Procurement** | 10% | [05-FINANCE.md](05-FINANCE.md) | Harry (GPT-5.4, iMac) | Athena (PO app) | 1x/cycle |
| 6 | **Infrastructure & Platform** | 10% | [07-INFRASTRUCTURE.md](07-INFRASTRUCTURE.md) | Jay Mark + Athena | Harry/Sentinel (monitoring) | 1x/cycle |
| 7 | **Intelligence & Analytics** | 5% | [06-INTELLIGENCE.md](06-INTELLIGENCE.md) | Hermes (GLM 5.1) | Iris (wiki) | 1x/2 cycles |

## Agent → Skill Matrix

| Agent | Primary Skill | Secondary Skills | Model |
|-------|--------------|-----------------|-------|
| **Ava** | Sales strategy | Creative briefs, Marketing strategy | Haiku + Advisor |
| **Hermes** | Intelligence & Analytics | Sales data (weekly crons) | GLM 5.1 (OpenRouter) |
| **Harry** | Finance & Procurement | Infrastructure monitoring (Sentinel role) | GPT-5.4 (iMac) |
| **Echo** | Marketing & Brand | Sales content (A+, SEO) | Claude Sonnet (SDK) |
| **Sentinel** | Operations monitoring | — (merged into Harry) | Via Harry (GPT-5.4) |
| **Iris** | Intelligence (wiki) | — | Gemma 4 ($0) |
| **Jay Mark** | Infrastructure & Platform | Operations (builds) | Human (PH) |
| **Athena** | Orchestration (all) | — | Claude Opus 4.6 |

## Heartbeat Rotation Sequence
```
Creative → Sales → Operations → Creative → Marketing → Finance → Infrastructure → Sales → Intelligence
```
Creative and Sales each appear 2-3x (highest weight). Others 1x each.

## Morning + Afternoon Reminders (NEW — Apr 13)
- **9 AM ET weekdays**: Morning Focus — top unblocked task per bucket, neglected bucket nudge
- **2 PM ET weekdays**: Afternoon Check-in — touched/untouched buckets, quick wins
- Powered by Gemma 4 ($0), runs in ZEUS heartbeat engine
- Purpose: prevent single-bucket days (e.g., all-day on procurement = 6 buckets neglected)

## V3 Blueprint Alignment
Each skill maps to a Blueprint V3 process:
1. **Creative** → Design pipeline (IREN/DRECO → marketplace)
2. **Sales** → ListingForge → marketplace expansion
3. **Operations** → Fulfillment portal → Zero 2.0 replacement
4. **Marketing** → GoHeadCase + PPC optimization
5. **Finance** → Xero integration + procurement app
6. **Infrastructure** → Agent swarm, cron management, platform reliability
7. **Intelligence** → PULSE leaderboard, weekly analytics, data freshness

## How Skills Are Used

### On-Demand (Cem messages)
- Cem asks about Walmart → load Sales skill
- Cem asks about One Piece visuals → load Creative skill
- Cem asks about royalties → load Finance skill
- Cem asks about crons → load Infrastructure skill
- Cross-pillar question → load 2 relevant skills

### Heartbeat (Automated)
- Pick next skill in rotation
- Read skill file for context
- Check assigned projects for blockers or stale items
- If something changed → Telegram alert to Cem
- If nothing changed → silent, move to next skill

### Morning/Afternoon (Automated)
- Scan all 7 skills
- Cross-reference with daily logs
- Nudge toward neglected buckets

## LLM Allocation
| Agent | Model | Cost | Skills Owned |
|-------|-------|------|-------------|
| Athena | Claude Opus 4.6 | Subscription | Orchestration |
| Ava | Haiku + Advisor | ~$15-30/mo | Sales strategy, Creative briefs |
| Harry | GPT-5.4 | TBD | Finance, Sentinel monitoring |
| Hermes | GLM 5.1 | ~$5-15/mo | Intelligence, Sales analytics |
| Echo | Claude Sonnet | ~$10-20/mo | Marketing, Sales content |
| Iris | Gemma 4 | $0 | Wiki maintenance |
| Gemma 4 | Ollama local | $0 | Batch tasks, heartbeat, reminders |
