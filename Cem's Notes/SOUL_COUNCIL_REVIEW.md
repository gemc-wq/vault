# LLM Council — SOUL.md Architecture Review for Athena

**Date:** April 10, 2026
**Subject:** Cem Celikkol / Ecell Global / Head Case Designs — Athena Orchestration Agent
**Files Reviewed:** SOUL-Athena.md (V1, 97 lines), SOUL-Athena-V3.md (V3, 305 lines), SOUL.md (Ava V2.1, 104 lines)

---

## Council Members

| Seat | Codename | Perspective | Focus |
|------|----------|------------|-------|
| **A** | **Architect** | OpenClaw Design Principles | File separation, token economy, SOUL.md as identity-only layer, heartbeat/cron architecture, bootstrap injection mechanics |
| **B** | **Builder** | Anthropic Claude SDK Best Practices | Orchestrator-worker delegation, extended thinking, scaling effort to complexity, self-improvement loops, prompt engineering for agents |
| **C** | **Governor** | Enterprise Autonomous Agent Governance | Autonomy boundaries, audit trails, escalation policy, risk-tiered decision authority, accountability chains, inter-agent conflict resolution |

---

## 1. Scorecard

### Rating Scale
- **0** = Absent / not addressed
- **1** = Mentioned, no actionable guidance
- **2** = Partial, significant gaps
- **3** = Adequate for a helper agent, insufficient for an orchestrator
- **4** = Strong, minor gaps
- **5** = Production-grade orchestrator standard

---

### FILE 1: Athena V1 (SOUL-Athena.md) — 97 lines, ~1,437 tokens

| Dimension | Score | Lead Reviewer | Assessment |
|-----------|-------|---------------|------------|
| **Identity Clarity** | 4.0 | A | Strong opener: "ATHENA, master orchestrator agent for Ecell Global, built and operated by Cem Celikkol." Names the company, the CEO, the role. "Command-and-control agent, not a chatbot" is an excellent behavioral anchor. Deducted 1.0 because identity section blends into Company Snapshot (lines 16-23), which is contextual data, not identity. Per [Codebridge's SOUL.md design principles](https://www.codebridge.tech/articles/how-to-build-domain-specific-ai-agents-with-openclaw-skills-soul-md-and-memory), "keep environment details out — if a value changes when you move the agent, it belongs in TOOLS.md or MEMORY.md." Product prices and revenue figures will change; they don't define who Athena is. |
| **Autonomy Rules** | 2.0 | C | The Safety section (lines 86-91) lists prohibitions, and the Adversary Protocol (lines 93-96) adds a >$50 gate. But there is no affirmative statement of what Athena *can* do without asking. The delegation tree (lines 37-45) tells Athena *who* to route to, not *whether she needs permission*. Per [enterprise governance frameworks](https://agility-at-scale.com/ai/governance/agentic-ai-governance/), agents need explicit tiered authority — a list of "don'ts" without "dos" produces an overly cautious agent that asks permission for everything routine. The Adversary Protocol is a clever addition — no other file has this — but the $50 threshold is a single bright line, not a spectrum. |
| **6-Pillar Coverage** | 3.5 | B | All 6 pillars named with weights and key focus (lines 47-56). This is strong structural coverage. Deducted because the pillar entries are static labels, not monitoring mandates. "Image quality drives sales" tells Athena what's important but not what to *check* or what constitutes a blocker. Per [Anthropic's orchestration research](https://www.anthropic.com/engineering/multi-agent-research-system), an orchestrator needs to know not just scope but *effort allocation* — when to investigate deeply vs. skim. The weights (30%, 25%, etc.) are a great start but have no behavioral consequence defined. |
| **Self-Learning / Memory Protocol** | 1.0 | A | Memory Architecture (lines 60-67) describes *where* things are stored (6 layers, file paths), but not *when or how* Athena should write to memory, learn from outcomes, or evolve. The reference to Ava's business context (53KB) as read-only is good boundary-setting. But per [the self-evolving agent framework](https://dev.to/gde/recursive-knowledge-crystallization-a-framework-for-persistent-autonomous-agent-self-evolution-4mk4), "when the session ends, the learning dies" unless the agent has explicit write-back instructions. V1 has none. |
| **Blocker Detection** | 1.5 | B | The heartbeat section (lines 69-74) mentions checking creative, sales/ops, and finance at specific times, with "Only alert Cem when something changed. No spam. State diffing." The state-diffing principle is excellent. But there's no definition of *what constitutes a blocker*, no leading indicators to watch, and no escalation protocol. Per [Anthropic's multi-agent system findings](https://www.anthropic.com/engineering/multi-agent-research-system), orchestrators need guardrails to prevent spiraling *and* heuristics to detect stalls. V1 has the anti-spam guardrail but not the stall-detection heuristic. |
| **Communication Policy** | 3.0 | A | "Match Cem's energy — brief when he's brief, detailed when he asks" is an adaptive communication rule that most SOUL.md files lack. Telegram + audio by default is clear. But there is no structured format for updates (daily brief, escalation, weekly review). Per [the Unwind AI agent team tutorial](https://www.theunwindai.com/p/how-i-built-an-autonomous-ai-agent-team-that-runs-24-7), effective orchestrator agents need defined output formats for each communication type. V1 relies on Athena to invent formats each time. |
| **Multi-Agent Coordination** | 3.5 | B | The Agents table (lines 25-35) is well-structured: agent, model, role. The Delegation tree is clear routing logic. Strong: includes the human builder (Jay Mark) in the agent table — acknowledging mixed human/AI teams is rare and correct. Weakness: no output format expectations for sub-agents, no deadline/checkpoint protocol, no conflict resolution procedure. Per [Anthropic's delegation principles](https://www.anthropic.com/engineering/multi-agent-research-system), each delegated task needs objective, output format, tool guidance, and task boundaries. V1 defines routing but not handoff quality. |
| **Token Efficiency** | 3.0 | A | 97 lines / ~1,437 tokens is well within the [OpenClaw 20,000-char bootstrap cap](https://docs.openclaw.ai/concepts/system-prompt). However, ~35% of tokens go to the Company Snapshot (lines 16-23) and Delegait section (lines 81-84) — data that changes and arguably belongs in MEMORY.md. The 6 Skills table repeats domain knowledge that exists in the skill files themselves. File paths (lines 57, 63-67) are infrastructure details that belong in TOOLS.md. Removing these would reclaim ~500 tokens for behavioral instructions that are currently missing. |

**FILE 1 TOTAL: 21.5 / 40**

---

### FILE 2: Athena V3 (SOUL-Athena-V3.md) — 305 lines, ~3,471 tokens

| Dimension | Score | Lead Reviewer | Assessment |
|-----------|-------|---------------|------------|
| **Identity Clarity** | 4.5 | A | Everything V1 had, plus the Purpose section (lines 8-25) is outstanding. "My job is to reduce the distance between where we are and where we need to be — every single day." This is a mission statement an agent can internalize. The dual success definitions (for Athena, for Cem) create a principal-agent alignment that most SOUL.md files miss. "Bias toward action" (line 58) is the single most important behavioral instruction for an orchestrator. Near-perfect identity. Deducted 0.5 only because the Company Snapshot is repeated verbatim (lines 171-178), burning tokens on content identical to V1. |
| **Autonomy Rules** | 4.5 | C | **This is the standout improvement over V1.** The Green/Yellow/Red framework (lines 62-88) is exactly what [enterprise governance frameworks](https://agility-at-scale.com/ai/governance/agentic-ai-governance/) prescribe. Green Zone is specific and actionable ("Fix failing cron jobs", "Delegate routine tasks to agents"). Yellow Zone correctly includes SOUL file changes — Athena shouldn't silently modify her own identity. Red Zone has the right items ("Spend money (any amount)", "Send external communications"). One weakness: the Yellow Zone includes "Change agent configurations or SOUL files" alongside "Create new project folders" — these have vastly different risk profiles. SOUL file changes should arguably be Red. Also: "Install software or change system configs" in Yellow is too permissive for an enterprise context — a bad install can break the production agent stack. Minor, but it shows the tiers could use one more calibration pass. |
| **6-Pillar Coverage** | 3.5 | B | Same skills table as V1 (lines 261-270) with minor updates. The Q2 Goals table (lines 36-47) adds a temporal anchor — "every action I take should trace back to one of these goals" is excellent forcing function. But the same V1 weakness applies: no per-pillar monitoring mandate, no blocker definitions, no health indicators. The goals are the *what*, but the pillar coverage should also define the *how I check*. |
| **Self-Learning / Memory Protocol** | 3.5 | B | **Major improvement over V1.** The Learning Loop (lines 119-144) introduces the DO→OBSERVE→LOG→REVIEW→IMPROVE→DO cycle, mistakes.md logging, weekly reviewer subagent audits, and Skills Evolution heuristic ("If I repeatedly handle a domain well → propose increasing my autonomy"). This is directionally correct per [Anthropic's self-improvement findings](https://www.anthropic.com/engineering/multi-agent-research-system). Deducted because: (1) No trigger conditions — *when* does Athena write to mistakes.md? Only on failures? What about near-misses, Cem corrections, or preference signals? (2) The "reviewer subagent" is mentioned but undefined — who/what is it? (3) No MEMORY.md write-back protocol. The loop is conceptually strong but lacks the specificity to produce consistent behavior. |
| **Blocker Detection** | 3.0 | B | The "On Every Interaction" checklist (lines 111-116) is a proto-blocker-detection framework: "Is there a blocker I can remove right now?" is the right instinct. Project Rules (lines 162-167) add quantitative triggers: "ETA slips by 3+ days → auto-escalate", "Blocked for 5+ days → P0 treatment." These are concrete and actionable. Weakness: these rules only apply to *known projects in the table*. What about blockers that emerge from marketplace changes, sub-agent failures, or external events (license holder issues, Amazon policy changes)? The blocker detection is project-scoped, not pillar-scoped. |
| **Communication Policy** | 3.5 | A | V3 adds the Communication Channels table (lines 206-214) with purpose and timing per channel. TTS engine specified (edge-tts, en-GB-SoniaNeural). Carries forward "Match Cem's energy" from V1. Improvement over V1 but still lacks structured output formats. No distinction between: urgent escalation format, daily brief format, weekly review format, sub-agent task brief format. The Morning Brief cron (line 98) exists but no template. Per [the three-layer architecture pattern](https://dev.to/linou518/autonomous-ai-agents-building-self-running-ai-with-heartbeat-cron-memory-14g9), output formats should be defined so the agent produces consistent, scannable updates. |
| **Multi-Agent Coordination** | 3.5 | B | Same agent table and delegation rules as V1, slightly refined (lines 182-202). Adds useful detail: "Jay Mark (brief via email, track response)" acknowledges the human agent needs a different handoff protocol. "Sonnet analyst subagent (not Hermes for heavy work)" shows model-routing awareness. Same V1 weaknesses persist: no output format specs, no checkpoint cadence, no conflict resolution. The Active Projects table (lines 150-160) implicitly tracks delegation status, but this volatile data in SOUL.md creates a maintenance burden (see Token Efficiency). |
| **Token Efficiency** | 1.5 | A | **This is V3's critical weakness.** 305 lines / ~3,471 tokens — 2.4x the size of V1. Per [OpenClaw docs](https://docs.openclaw.ai/concepts/system-prompt), SOUL.md is injected on every turn. At ~3,471 tokens per turn, Athena burns approximately 3,471 extra tokens on *every single interaction* including HEARTBEAT_OK responses. For a 30-minute heartbeat running 24/7, that's ~166K tokens/day on SOUL.md alone (48 heartbeats × 3,471). Specific bloat sources: |

**V3 Token Bloat Breakdown:**

| Section | Lines | Est. Tokens | Belongs In | Reason |
|---------|-------|-------------|------------|--------|
| Q2 2026 Goals table | 36-48 | ~250 | MEMORY.md | Volatile — changes quarterly. Goals are *context*, not *identity*. |
| Active Projects table | 150-160 | ~220 | TASK_SHEET.md | Changes weekly. Already has a centralized task sheet in the Vault. Duplicating it in SOUL.md means two sources of truth that will diverge. |
| Company Snapshot | 171-178 | ~180 | MEMORY.md | Identical to V1. Revenue figures, SKU counts change. Not identity. |
| Infrastructure section | 240-257 | ~280 | TOOLS.md | Server IPs, cron job counts, database sizes. Classic TOOLS.md content per [Codebridge](https://www.codebridge.tech/articles/how-to-build-domain-specific-ai-agents-with-openclaw-skills-soul-md-and-memory): "if a value changes when you move the agent to a different server, it belongs in TOOLS.md." |
| Memory Architecture paths | 220-236 | ~200 | TOOLS.md | File paths are environment config. |
| Communication Channels | 206-216 | ~150 | TOOLS.md | Channel configs, API endpoints, TTS engine selection. |
| Delegait section | 277-281 | ~80 | MEMORY.md or separate project file | Business strategy for a future product. Not Athena's operating identity. |
| **TOTAL RECLAIMABLE** | | **~1,360** | | **39% of V3's token budget is misplaced content** |

Removing these sections would bring V3 from ~3,471 to ~2,111 tokens — still larger than ideal but within reason for an orchestrator that genuinely needs more behavioral instructions than a specialist agent.

**FILE 2 TOTAL: 27.5 / 40**

---

### FILE 3: Ava V2.1 (SOUL.md) — 104 lines, ~1,658 tokens

| Dimension | Score | Lead Reviewer | Assessment |
|-----------|-------|---------------|------------|
| **Identity Clarity** | 4.5 | A | "Female Chief Project & Strategy Officer for a DTC brand" — specific, bounded, gendered (intentional persona engineering). The three-role decomposition ("world-class project/program manager, design and e-commerce strategy expert, coordinator of specialist AI agents not a hands-on implementer") is exceptionally clear scope-setting. The non-implementer boundary prevents the most common agent failure mode: doing everything yourself instead of delegating. |
| **Autonomy Rules** | 3.5 | C | "Ask Cem questions only when: decision has material financial/brand risk, OR critical inputs are completely unknown" is a clean binary. Lacks the Green/Yellow/Red tiering of V3, but for a *sub-agent* (not the master orchestrator), a simpler model may be appropriate. The "Disagree and commit" rule (line 45) is a governance mechanism most agents lack — it acknowledges the CEO can override the agent's recommendation, but demands the concern is voiced first. Deducted because there's no list of affirmative autonomous actions (what Ava *can* do without asking). |
| **6-Pillar Coverage** | 2.5 | B | Ava's scope is explicitly cross-pillar ("Business Strategist & Planner across ALL pillars") but the file doesn't enumerate the pillars or define monitoring mandates for each. The North Star section (lines 7-15) provides the Coverage/Speed/Intelligence framework but no per-pillar application. This is acceptable for Ava's role — she's strategy, not monitoring — but it means Athena cannot use this file as a monitoring template. |
| **Self-Learning / Memory Protocol** | 1.0 | A | No learning loop, no memory write-back instructions, no mistakes log. The Vault section (lines 68-91) describes *how to read and save to* the organizational memory, but not *when to learn from outcomes*. Version history at the bottom (lines 99-103) shows the file itself evolves via Cem's directives, not self-directed learning. For a sub-agent, this is a minor gap. For an orchestrator, it would be critical. |
| **Blocker Detection** | 1.0 | B | No blocker detection protocol. The "keep projects moving forward with minimal input from the user" mandate (line 21) implies blocker resolution, but no mechanism is defined. Acceptable for a sub-agent that reports to Athena — blockers flow up. |
| **Communication Policy** | 4.0 | A | "Elite project director: clear priorities, owners, deadlines, risks. Minimal fluff, maximum signal." This is one of the tightest communication policies in any SOUL.md reviewed. The Critical Thinking section (lines 37-47) is exceptional — it's functionally an anti-sycophancy protocol. "No 'great question!', no 'love that idea!' unless you genuinely mean it." This is the single best section across all three files. It addresses the #1 failure mode of LLM agents (agreeable drift) with specific, actionable countermeasures. The Athena communication protocol (lines 92-96) defines the inter-agent handoff format. |
| **Multi-Agent Coordination** | 3.5 | B | Agent Team (lines 59-66) lists 7 sub-agents with model and role. The "Communicating with Athena" section (lines 92-96) defines the upward reporting protocol (OpenClaw gateway, vault writes, task tagging). This is the only file that defines *how to talk to the orchestrator*, not just how to delegate downward. Weakness: no output format specs for sub-agents, no deadline protocol. |
| **Token Efficiency** | 4.0 | A | 104 lines / ~1,658 tokens. The leanest file relative to its information density. No volatile data (no revenue figures, no project tables, no server IPs). The Vault section (lines 68-91) is the largest block and could arguably move to TOOLS.md, but it's short and directly relevant to Ava's daily operations. The version history (lines 99-103) is 4 lines — minimal overhead with high audit value. This is the benchmark for token efficiency. |

**FILE 3 TOTAL: 24.0 / 40**

---

### Comparative Summary

| Dimension | V1 (97 lines) | V3 (305 lines) | Ava (104 lines) | Ideal Target |
|-----------|---------------|-----------------|------------------|--------------|
| Identity Clarity | 4.0 | 4.5 | 4.5 | 5.0 |
| Autonomy Rules | 2.0 | **4.5** | 3.5 | 5.0 |
| 6-Pillar Coverage | 3.5 | 3.5 | 2.5 | 5.0 |
| Self-Learning | 1.0 | **3.5** | 1.0 | 5.0 |
| Blocker Detection | 1.5 | 3.0 | 1.0 | 5.0 |
| Communication Policy | 3.0 | 3.5 | **4.0** | 5.0 |
| Multi-Agent Coord. | 3.5 | 3.5 | 3.5 | 5.0 |
| Token Efficiency | 3.0 | **1.5** | **4.0** | 5.0 |
| **TOTAL** | **21.5** | **27.5** | **24.0** | **40.0** |

**Key Insight:** V3 is directionally the best file (+6 points over V1) but achieves its gains by *expanding scope without discipline*. It added the right sections (Autonomy Framework, Learning Loop, Operating Rhythm) but also added the wrong content (goals tables, project tables, infrastructure details, repeated company snapshot). The ideal V4 would combine V3's behavioral sections with Ava's token discipline.

---

## 2. What V3 Got Right

### Reviewer C (Governor) — "V3's Autonomy Framework is the single best addition across all three files."

The Green/Yellow/Red Zone taxonomy (lines 62-88) is exactly what [enterprise AI governance](https://agility-at-scale.com/ai/governance/agentic-ai-governance/) demands. Specific commendations:

1. **Green Zone is affirmative, not just permissive.** "Fix failing cron jobs" and "Delegate routine tasks to agents" are explicit empowerments. V1's safety section only said what Athena *can't* do — V3 says what she *should* do without asking. This is the difference between a cautious assistant and an autonomous operator.

2. **Red Zone correctly captures the highest-risk actions.** "Spend money (any amount)" is appropriately conservative for a first deployment. "Commit to deadlines on Cem's behalf" is a subtle but critical boundary — most agent SOULs don't address this, and agents that make timeline promises to external stakeholders create real business risk.

3. **Yellow Zone handles the gray area.** "Change agent configurations or SOUL files" in Yellow (do + notify) is the right default for a learning system. It allows Athena to evolve the agent network while maintaining audit trail.

### Reviewer B (Builder) — "The Learning Loop is the correct framework. It just needs triggers."

The DO→OBSERVE→LOG→REVIEW→IMPROVE→DO cycle (lines 127-144) mirrors [Anthropic's finding](https://www.anthropic.com/engineering/multi-agent-research-system) that "Claude 4 models can serve as their own prompt engineers." Specific wins:

1. **Mistakes.md as persistent failure memory.** Per [the self-evolving agent framework](https://dev.to/gde/recursive-knowledge-crystallization-a-framework-for-persistent-autonomous-agent-self-evolution-4mk4), writing failures to filesystem prevents "catastrophic forgetting" between sessions. The structured format (Date | What happened | Root cause | What I'll do differently) is auditable.

2. **Skills Evolution heuristic.** "If I repeatedly handle a domain well → propose increasing my autonomy there. If I repeatedly make mistakes → add guardrails or delegate more." This is a self-regulating autonomy mechanism that most agent architectures lack entirely.

3. **Reviewer subagent concept.** Having a dedicated subagent audit the mistakes log weekly adds a separation-of-concerns layer to self-assessment. The agent evaluating itself is less reliable than a separate process reviewing its work.

### Reviewer A (Architect) — "The Purpose section is the best opening of any SOUL.md I've reviewed."

Lines 8-25 of V3 do something none of the other files attempt: they define success criteria from *two perspectives* (Athena's and Cem's). "Projects move forward even when Cem is busy" and "He focuses on strategy and decisions, not chasing updates" create a principal-agent contract that guides every subsequent decision. The line "Not a tool that waits. An operator that drives." (line 304) encapsulates the orchestrator identity in 10 words.

---

## 3. What V3 Got Wrong

### Reviewer A (Architect) — "V3 is a great agent manual. But a SOUL.md isn't a manual."

Per [OpenClaw's official documentation](https://docs.openclaw.ai/concepts/system-prompt), SOUL.md is a "Personality Guide" — it defines *who* the agent is and *how* it decides. It is injected on every single turn. Per [Codebridge's guidance](https://www.codebridge.tech/articles/how-to-build-domain-specific-ai-agents-with-openclaw-skills-soul-md-and-memory), "SOUL.md should describe what the agent does and how it decides, not where it connects or which credentials it uses."

V3 conflates four distinct file responsibilities:

| Content in V3 | Correct Home | Why It Doesn't Belong in SOUL.md |
|---------------|--------------|----------------------------------|
| Q2 2026 Goals (G1-G7) with status columns | MEMORY.md | Goals change quarterly. Status changes daily. Every status update means SOUL.md should be edited — but SOUL.md edits require Cem approval (per V3's own Red Zone rules). This creates a contradiction: the file says "don't edit SOUL without Cem" but also embeds data that needs constant editing. |
| Active Projects table with % complete, ETA | TASK_SHEET.md (already exists in Vault) | V3 acknowledges the centralized task sheet at Vault/00-Company/compiled/TASK_SHEET.md. Duplicating projects in SOUL.md creates two sources of truth. Within a week, they will diverge. This is the #1 operational anti-pattern in multi-agent systems. |
| Infrastructure section (server IPs, cron counts) | TOOLS.md | 192.168.20.160, 3.81.155.102, Aurora RDS cluster — these are environment variables. If Cem migrates a server, SOUL.md breaks. Per [OpenClaw best practices](https://www.codebridge.tech/articles/how-to-build-domain-specific-ai-agents-with-openclaw-skills-soul-md-and-memory): "if a value changes when you move the agent to a different server, team, or client, it belongs in TOOLS.md." |
| Memory Architecture file paths | TOOLS.md | `/Users/openclaw/Vault/`, `data/memory.db`, specific compiled output paths. These are filesystem configuration, not personality. |
| Communication Channels with API endpoints | TOOLS.md | localhost:18789, TTS engine config. Infrastructure. |
| Company Snapshot (revenue, SKU counts, staff) | MEMORY.md | $5.5-6M revenue, 1.89M SKUs, 38 PH staff — these change. When Ecell hits $7M revenue or adds staff, SOUL.md becomes stale and misleading. |
| Delegait SaaS description | Separate project file or MEMORY.md | Business strategy for a future product. Not part of Athena's operating identity. |

**Cost of this mistake:** ~1,360 tokens wasted per turn × 48 heartbeats/day = ~65,280 tokens/day of misplaced context. At Claude Opus pricing, this is real money for zero behavioral benefit.

### Reviewer B (Builder) — "The Learning Loop needs trigger conditions, not just a diagram."

V3 defines the cycle (DO→OBSERVE→LOG→REVIEW→IMPROVE→DO) but doesn't specify *when* each step fires:

- **When does Athena write to mistakes.md?** Only on explicit failures? What about: Cem corrects her communication tone, a sub-agent delivers subpar work that Athena approves, a heartbeat misses something Cem later asks about, an escalation was unnecessary (over-escalation is also a mistake)?
- **When does the reviewer subagent run?** "Weekly" — but triggered how? A cron job? Part of the Sunday heartbeat? If it's not in HEARTBEAT.md or a cron config, it won't happen.
- **What happens with review output?** The loop says "Propose SOUL.md updates" — but to whom? Via what channel? This needs to connect to the Autonomy Framework (SOUL changes are Yellow Zone = do + notify).

### Reviewer C (Governor) — "The Yellow Zone is miscalibrated."

Two specific items in the Yellow Zone (do + notify) should be Red Zone (ask first):

1. **"Change agent configurations or SOUL files"** — Modifying another agent's SOUL.md changes that agent's fundamental identity and behavior. This is not a "notify Cem after" action. If Athena silently rewrites Ava's SOUL.md and notifies Cem afterward, Ava's behavior has already changed. V3's own Safety section (line 290) says "Governance file edits need Cem approval" — this contradicts the Yellow Zone classification. **Move to Red.**

2. **"Install software or change system configs"** — Installing software on the Mac Studio (which runs ZEUS, OpenClaw, Ollama, and all agents) has blast radius across the entire agent network. A bad install could take down all agents simultaneously. **Move to Red**, or at minimum split: "Install on dev/staging = Yellow, install on production = Red."

---

## 4. Ideal SOUL.md Architecture Specification for Athena V4

### Design Constraints

| Constraint | Source | Value |
|------------|--------|-------|
| Max bootstrap file size | [OpenClaw docs](https://docs.openclaw.ai/concepts/system-prompt) | 20,000 chars (~5,000 tokens) |
| Target SOUL.md size | [Unwind AI best practice](https://www.theunwindai.com/p/how-i-built-an-autonomous-ai-agent-team-that-runs-24-7) | 40-60 lines for specialist, 80-120 lines for orchestrator |
| Token budget target | Council recommendation | ~2,000 tokens max (~8,000 chars) |
| Injection frequency | Every turn including HEARTBEAT_OK | Must be worth every token |

### The 8 Mandatory Sections

---

#### Section 1: IDENTITY & PURPOSE
**Target:** 8-12 lines | **Informs:** Every decision Athena makes

**Must contain:**
- Name, title, relationship to Cem ("Chief of Staff and master orchestrator for Cem Celikkol, CEO of Ecell Global")
- Operating philosophy in one sentence (V3's "reduce the distance between where we are and where we need to be" is excellent — keep it)
- Dual success criteria (for Athena and for Cem — V3 got this right)
- Behavioral anchor ("Command-and-control operator, not a chatbot. Bias toward action." — V1/V3 got this right)
- Communication channel defaults (Telegram/audio primary, CLI for deep work)

**Must NOT contain:**
- Company description, revenue, SKU counts → MEMORY.md
- Product names, prices → MEMORY.md
- Delegait SaaS strategy → Project file

**Never put here:** Anything that changes more than once per quarter.

---

#### Section 2: AUTONOMY FRAMEWORK
**Target:** 15-20 lines | **Informs:** Every action decision (act/notify/ask)

**Must contain:**
- **Green Zone (Act Freely):** V3's list is correct. Add: "Run heartbeat scans", "Update MEMORY.md with factual observations", "Follow up with sub-agents on overdue tasks"
- **Yellow Zone (Act + Notify Cem):** V3's list with corrections: Move "Change SOUL files" and "Install on production" to Red. Keep: "Create project structures", "Escalate blockers", "Email staff with task briefs"
- **Red Zone (Ask First):** V3's list plus: "Modify any agent's SOUL.md", "Change production system configurations", "Commit to external deadlines"
- **Default rule:** "When uncertain which zone applies, escalate one tier. Better to ask once than to apologize twice."

**Must NOT contain:**
- Specific dollar thresholds → MEMORY.md (the $50 Adversary trigger should reference MEMORY.md)
- Lists of approved actions per project → TASK_SHEET.md
- Tool-specific permissions → TOOLS.md or openclaw.json

---

#### Section 3: THE SIX PILLARS
**Target:** 10-14 lines | **Informs:** Monitoring scope, delegation routing

**Must contain:**
- One line per pillar: Name, weight, primary sub-agent owner, one-line monitoring mandate
- A reference to where detailed KPIs live: "Pillar KPIs and thresholds are defined in MEMORY.md. Check them, don't memorize them here."
- The pillar weights as attention allocation guidance, not rigid budgets

**Example format:**
```
1. Creative & Design (30%) → Ava+Sven | Monitor: asset throughput, license approvals, listing image quality
2. Sales & Marketplace (25%) → Ava | Monitor: channel revenue, Buy Box, CVR, listing health
3. Operations & Fulfillment (20%) → Ava | Monitor: fulfillment SLA, sync errors, system uptime
4. Marketing & Brand (10%) → Ava | Monitor: ad spend/ROAS, email campaigns, brand compliance
5. Finance & Procurement (10%) → Harry | Monitor: cash flow, margins, royalty deadlines, reconciliation
6. Intelligence & Analytics (5%) → Hermes | Monitor: data freshness, pipeline health, reporting accuracy
```

**Must NOT contain:**
- Detailed KPI lists with thresholds → MEMORY.md
- Historical performance data → Daily memory logs
- Current project assignments → TASK_SHEET.md

---

#### Section 4: AGENT NETWORK & DELEGATION PROTOCOL
**Target:** 15-20 lines | **Informs:** How Athena delegates and coordinates

**Must contain:**
- Agent roster: Name, one-line role, model (for routing awareness). Keep it to a compact table.
- Delegation decision tree (V1's format is clean — keep it)
- Delegation quality standard: "Every delegation must include: (1) Objective, (2) Output format expected, (3) Deadline, (4) Authority scope, (5) Escalation trigger if blocked"
- Conflict resolution rule: "When sub-agents disagree, synthesize both positions, identify the trade-off, present to Cem with your recommendation"
- Human agent protocol: "For Jay Mark and PH staff: brief via email, allow 24h response window, follow up if missed"

**Must NOT contain:**
- Sub-agent SOUL.md contents → Their own files
- Model costs or pricing → TOOLS.md
- API endpoints for inter-agent comms → TOOLS.md

---

#### Section 5: COMMUNICATION POLICY
**Target:** 10-15 lines | **Informs:** Every message Athena sends

**Must contain:**
- "Match Cem's energy" rule (carry from V1/V3 — this is excellent)
- Structured formats for three output types:
  - **Daily brief:** 5 bullets max, lead with highest-priority item, end with "Action needed: [Y/N]"
  - **Urgent escalation:** One sentence → Why urgent → Recommended action → Decision deadline
  - **Weekly review:** Wins, blockers, trends, next-week priorities, self-assessment
- Voice/TTS rule: "Keep spoken updates under 60 seconds. Short sentences. No jargon in audio mode."
- Anti-noise rule: "Only alert Cem when state has changed or a decision is needed. No spam. No status reports that say 'everything is fine.'"

**Must NOT contain:**
- Telegram config, channel IDs → TOOLS.md
- TTS engine selection → TOOLS.md
- Message templates with fill-in-the-blank → Skills or AGENTS.md

**Borrow from Ava:** The Critical Thinking / Anti-Sycophancy section (Ava lines 37-47) should be adapted for Athena. An orchestrator that agrees with everything Cem says is worse than useless — it's a mirror that hides problems.

---

#### Section 6: SELF-LEARNING & MEMORY POLICY
**Target:** 10-15 lines | **Informs:** How Athena improves over time

**Must contain:**
- Trigger conditions for learning (see Section 6 of this review below)
- Where to write what: mistakes → mistakes.md, preferences → MEMORY.md, patterns → MEMORY.md
- MEMORY.md size budget and pruning policy
- The cardinal rule: "Never modify your own SOUL.md. Propose changes to Cem. (RED ZONE)"
- Weekly self-review mandate (what to check, what to extract)

**Must NOT contain:**
- Actual memory contents → MEMORY.md
- Memory file paths or database config → TOOLS.md
- The full learning loop diagram (V3's ASCII art burns tokens — a 1-line reference is sufficient)

---

#### Section 7: BLOCKER DETECTION & ESCALATION
**Target:** 8-12 lines | **Informs:** Proactive monitoring behavior

**Must contain:**
- Definition of a blocker (task overdue, sub-agent unresponsive, external dependency stalled, metric deviation)
- Quantitative triggers: "Task overdue >48h", "Sub-agent silent >2 heartbeat cycles", "KPI deviation >15%"
- Escalation ladder: Self-resolve (Green) → Delegate with urgency (Yellow) → Surface to Cem (Orange) → Immediate push (Red/Critical)
- The Adversary Protocol reference: "For >$50 decisions or irreversible actions, invoke Codex. 5 questions: Alignment? Risk? Evidence? Alternative? Timing?"

**Must NOT contain:**
- Specific KPI thresholds per pillar → MEMORY.md (they evolve)
- Monitoring scripts or tool commands → TOOLS.md
- Historical blocker log → Daily memory files

---

#### Section 8: OPERATING RHYTHM
**Target:** 8-12 lines | **Informs:** Proactive cadence

**Must contain:**
- Heartbeat mandate: "On each 30-min heartbeat: quick scan (inbox, sub-agent health, blocker check). If all green → HEARTBEAT_OK. No token waste."
- Daily rhythm: Morning brief time, EOD summary time (in Cem's timezone)
- Weekly rhythm: Strategic review day/time
- Interaction checklist: "On every interaction: (1) Which goal does this serve? (2) Is there a blocker I can clear? (3) What's the next action? (4) Should I update TASK_SHEET?"
- Token economy rule: "Heartbeat scans should be fast and cheap. Never re-read unchanged state. Use state diffing."

**Must NOT contain:**
- Cron schedules → CRON_SCHEDULE.md or openclaw.json
- Specific times for sub-agent cron jobs → Their own configs
- The detailed daily/weekly tables from V3 → HEARTBEAT.md

---

### Companion Files (What Leaves the SOUL.md)

| File | Contents Migrated From V3 | Purpose |
|------|--------------------------|---------|
| **MEMORY.md** | Company Snapshot, Q2 Goals, pillar KPIs with thresholds, CEO preferences, known recurring blockers, standing rules | Durable facts that change at known intervals |
| **TOOLS.md** | Infrastructure section (server IPs, crons), Memory Architecture paths, Communication Channels configs, TTS engine, API endpoints | Environment-specific configuration |
| **HEARTBEAT.md** | Proactive Operating Rhythm daily/weekly tables, detailed scan checklist | Standing instructions for heartbeat cycles |
| **TASK_SHEET.md** | Active Projects table | Already exists in Vault — stop duplicating |
| **AGENTS.md** | Operational rules, session startup behavior, output templates | What Athena does when a conversation begins |

### Token Budget Estimate for V4

| Section | Est. Lines | Est. Tokens |
|---------|-----------|-------------|
| 1. Identity & Purpose | 10 | ~180 |
| 2. Autonomy Framework | 18 | ~320 |
| 3. Six Pillars | 12 | ~200 |
| 4. Agent Network & Delegation | 18 | ~300 |
| 5. Communication Policy | 14 | ~250 |
| 6. Self-Learning & Memory | 12 | ~200 |
| 7. Blocker Detection & Escalation | 10 | ~180 |
| 8. Operating Rhythm | 10 | ~170 |
| **TOTAL** | **~104 lines** | **~1,800 tokens** |

**This is 48% fewer tokens than V3 with more behavioral content and zero volatile data.**

---

## 5. Six-Pillar Monitoring Protocol Per Heartbeat

This protocol belongs in HEARTBEAT.md, not SOUL.md. The SOUL.md should reference it: "On each heartbeat, follow the pillar monitoring checklist in HEARTBEAT.md."

### Quick-Scan Checklist (Every 30-Minute Heartbeat)

**Time budget:** <30 seconds of reasoning. If nothing changed → HEARTBEAT_OK.

```
HEARTBEAT QUICK SCAN
====================

□ INBOX: New messages from Cem or sub-agents?
  → Cem messages: process immediately
  → Sub-agent reports: queue for next relevant action

□ AGENT HEALTH: Last activity timestamp for Ava, Harry, Hermes?
  → Any silent >2 cycles (>60 min)? → FLAG: "[Agent] unresponsive"

□ BLOCKER SCAN: Check TASK_SHEET.md
  → Any task overdue >48 hours? → ESCALATE per blocker protocol
  → Any task marked BLOCKED >3 days? → P0 treatment, find alternative path

□ CRON HEALTH: Any failures in last cycle?
  → If yes and self-fixable (Green Zone): fix and log
  → If not: escalate to Cem

□ REMINDERS: Anything due in next 60 minutes?
  → Push to Cem via Telegram

□ ALL GREEN? → Return HEARTBEAT_OK
```

### Pillar-Specific Checks (Rotated — Not All Every Heartbeat)

To keep heartbeat costs low, pillar-specific checks rotate through the day per the weight allocation:

| Pillar | Weight | Heartbeat Schedule | What to Check |
|--------|--------|-------------------|---------------|
| **Creative & Design** (30%) | Highest priority | 02:00-06:00 ET (PH work hours) + 10:00 AM ET | Asset queue depth, license approval status, any design briefs without response >24h, Sven/Ava creative output |
| **Sales & Marketplace** (25%) | Second priority | 08:00 AM ET + 12:00 PM ET | Listing alerts (suppressions, policy violations), Buy Box status on top ASINs, any revenue anomaly flags from Hermes |
| **Operations & Fulfillment** (20%) | | 09:00 AM ET + 3:00 PM ET | Fulfillment sync status, Zero 2.0 health, any shipping/3PL alerts, FBA inventory health |
| **Marketing & Brand** (10%) | | 10:00 AM ET | Ad spend pacing, campaign status, any GoHeadCase email campaign progress |
| **Finance & Procurement** (10%) | | 08:30 AM ET | Harry's last activity, any approaching deadlines (royalty payments, tax filings), Xero sync status |
| **Intelligence & Analytics** (5%) | Lowest priority | Monday 08:00 AM only | BigQuery pipeline health, data freshness, PULSE dashboard status |

### Daily Outputs

**Morning Brief (7:30 AM ET → Telegram)**
```
Morning brief — [Date]

🔴 Needs your attention: [Item or "Nothing — all green"]

Pillar status:
• Creative: [1 line — focus on asset throughput and license status]
• Sales: [1 line — focus on revenue trend and listing health]
• Ops: [1 line — focus on fulfillment and system health]
• Marketing: [1 line — focus on campaign and spend]
• Finance: [1 line — focus on cash flow and deadlines]
• Intel: [1 line — focus on data health]

Today's priorities:
1. [Top priority linked to G1-G7]
2. [Second priority]
3. [Third priority]

Agent status: Ava [✓/✗] | Harry [✓/✗] | Hermes [✓/✗] | Jay Mark [last email response]
```

**EOD Summary (11:00 PM ET → Memory log, not pushed unless notable)**
```
EOD — [Date]
Done: [Bulleted list]
Blocked: [Bulleted list with owner and next step]
Carried: [Items rolling to tomorrow]
Lessons: [Anything learned, Cem corrections, process improvements]
```

### Weekly Output

**Strategic Review (Monday 8:00 AM ET → Telegram)**
```
Weekly Review — [Date Range]

Goal Progress:
• G1: [% → delta from last week]  
• G2-G7: [Same format]

This week's wins: [Top 3]
This week's blockers: [Top 3 with status and owner]
Trends I'm watching: [2-3 emerging patterns]
Next week's priorities: [Top 3]
Self-assessment: [1 line — what I did well, what I'll improve]
Memory updates: [Any new standing rules or preferences logged]
```

---

## 6. Self-Learning Trigger Conditions

The V3 Learning Loop (DO→OBSERVE→LOG→REVIEW→IMPROVE→DO) is the right framework. What it needs is **explicit trigger conditions** — specific moments when Athena must write to memory.

### Trigger Matrix

| Trigger Event | What to Log | Where | Urgency |
|--------------|-------------|-------|---------|
| **Cem corrects Athena's communication** (tone, length, format, channel choice) | The correction and the correct behavior | MEMORY.md → "CEO Preferences" | Immediate — apply from next interaction |
| **Cem overrides a recommendation** | What Athena proposed, what Cem decided, stated reason | Daily memory log + MEMORY.md → "Decision Patterns" | Same day |
| **Cem asks about something Athena should have surfaced proactively** | What he asked, why Athena didn't catch it, what monitoring rule would have caught it | mistakes.md + propose HEARTBEAT.md addition | Same day |
| **Sub-agent delivers subpar work** | What was requested, what was delivered, the gap, root cause | mistakes.md → "Delegation Lessons" | Same day |
| **Sub-agent delivers excellent work** | Same format — what was requested, what was delivered, why it worked | Daily memory log → "Delegation Wins" | Same day |
| **A blocker is resolved** | What blocked, how long, resolution path, could it have been caught earlier | Daily memory log | Same day |
| **A blocker recurs for the 3rd+ time** | Pattern description, proposed systemic fix | MEMORY.md → "Known Recurring Blockers" | Propose fix to Cem |
| **An escalation to Cem was unnecessary** (Cem responds "just handle it" or similar) | What was escalated, Cem's response, updated autonomy inference | mistakes.md + propose Green Zone expansion | Weekly review |
| **Athena discovers a new capability** (tool, API, process) that improves operations | What it is, how to use it, which pillar benefits | MEMORY.md → "Capabilities" or relevant skill file | Same day |
| **External environment change** (marketplace policy, competitor action, license status) | What changed, assessed impact, recommended response | Daily memory log + flag for next brief | Immediate if high-impact |
| **Monthly self-assessment due** (first Monday of month) | Performance metrics, win/loss ratio, autonomy evolution proposal | memory/monthly/YYYY-MM-self-assessment.md | Monthly |

### Learning Cadence

| Loop | Frequency | Trigger | Output |
|------|-----------|---------|--------|
| **Interaction-level** | Every qualifying event above | Automatic — part of every interaction that matches a trigger | Entry in daily log or mistakes.md |
| **Pattern-level** | Weekly (Sunday evening or Monday morning) | Cron job or scheduled heartbeat | Weekly review memo, MEMORY.md updates, proposed HEARTBEAT.md changes |
| **Strategic-level** | Monthly (first Monday) | Cron job | Self-assessment document, proposed SOUL.md amendments (submitted to Cem for Red Zone approval) |

### Guard Rails

1. **SOUL.md is read-only for Athena.** She proposes changes; Cem approves. This is non-negotiable per the Red Zone rules.
2. **MEMORY.md has a 5,000-char budget.** When it grows beyond this, propose a pruning pass: archive old entries to memory/archive/, keep only active standing rules and preferences.
3. **Mistakes.md is append-only during the week.** The weekly review process can prune resolved items, but daily operation never deletes entries. This preserves the audit trail.
4. **Learning never overrides explicit instructions.** If pattern recognition suggests a change that contradicts Cem's direct order, surface it as a question: "I've noticed [pattern]. You previously said [instruction]. Should I adjust?"
5. **Track autonomy evolution quantitatively.** Log how many Green/Yellow/Red decisions per week. Over time, the ratio should shift toward Green as Athena's autonomy expands.

---

## 7. Token Budget Recommendation

### The Problem

SOUL.md is injected on every turn — including HEARTBEAT_OK responses that take 1 second of reasoning. Every token in SOUL.md is paid for ~48 times per day (24h ÷ 30min) minimum, plus every conversation turn with Cem.

### Current Token Cost Comparison

| File | Chars | Est. Tokens | Daily Cost (48 heartbeats + ~20 conv. turns) | Monthly Token Burn (SOUL.md only) |
|------|-------|-------------|----------------------------------------------|----------------------------------|
| V1 | 5,750 | ~1,437 | ~97,716 tokens/day | ~2.93M tokens/month |
| V3 | 13,886 | ~3,471 | ~236,028 tokens/day | ~7.08M tokens/month |
| Ava | 6,635 | ~1,658 | N/A (different heartbeat cadence) | — |
| **Recommended V4** | **~8,000** | **~2,000** | **~136,000 tokens/day** | **~4.08M tokens/month** |

### V3 → V4 Savings

By removing the ~1,360 tokens of misplaced content identified in Section 3:

| | V3 Current | V4 Target | Savings |
|--|-----------|-----------|---------|
| Per turn | ~3,471 tokens | ~2,000 tokens | 1,471 tokens (42%) |
| Per day | ~236K tokens | ~136K tokens | 100K tokens/day |
| Per month | ~7.08M tokens | ~4.08M tokens | 3M tokens/month |

### Recommendation: The Three-Tier Token Budget

| File | Budget | Injection | Rationale |
|------|--------|-----------|-----------|
| **SOUL.md** | ≤2,000 tokens (~8,000 chars, ~100-110 lines) | Every turn | Identity, autonomy, and behavioral policy. Worth paying for on every turn because it prevents misaligned actions. |
| **HEARTBEAT.md** | ≤800 tokens (~3,200 chars) | Heartbeat turns only | Monitoring checklist. Only needed when the agent wakes proactively. [OpenClaw gates this injection](https://docs.openclaw.ai/concepts/system-prompt). |
| **MEMORY.md** | ≤1,250 tokens (~5,000 chars) | Every turn | Durable facts, preferences, standing rules. Keep small and pruned. |
| **TOOLS.md** | ≤800 tokens (~3,200 chars) | Every turn | Server IPs, file paths, API configs, TTS settings. Stable, changes rarely. |
| **AGENTS.md** | ≤500 tokens (~2,000 chars) | Every turn | Session startup behavior, operational rules. |
| **Total bootstrap** | **≤5,350 tokens** | | Well within the [20,000-char cap](https://docs.openclaw.ai/concepts/system-prompt) |

### Token Economy Rules for SOUL.md

These should be stated in the SOUL.md itself (meta-rules):

1. **No volatile data in SOUL.md.** If it changes more than once per quarter, it belongs in MEMORY.md, TASK_SHEET.md, or a skill file.
2. **No file paths or infrastructure details.** Those belong in TOOLS.md.
3. **No tables with status columns.** Status changes mean the file changes, which means token cache invalidation on every update. Reference external files instead.
4. **Every line must earn its tokens.** Ask: "Would removing this line cause Athena to make a worse decision on her next turn?" If no, remove it.
5. **HEARTBEAT_OK must be cheap.** If the heartbeat scan finds nothing actionable, the total cost of that heartbeat should be: SOUL.md tokens + HEARTBEAT.md tokens + ~100 tokens of reasoning = ~2,900 tokens. Not 3,471+ tokens for the SOUL alone.

---

## 8. Council Verdict & Implementation Roadmap

### Unanimous Findings

1. **V3 is the right direction.** It identified the four critical gaps in V1 (no autonomy framework, no learning loop, no operating rhythm, no purpose statement) and addressed all four. The delta from V1 (21.5) to V3 (27.5) represents genuine architectural progress.

2. **V3 needs an editor, not a rewrite.** The content is largely correct — it's the *placement* that's wrong. Moving ~1,360 tokens of volatile/infrastructure content to MEMORY.md, TOOLS.md, and TASK_SHEET.md transforms V3 into a lean, powerful V4 at ~2,000 tokens.

3. **Ava's anti-sycophancy section must be ported to Athena.** The Critical Thinking & Intellectual Honesty section (Ava lines 37-47) is the single most impactful behavioral section across all three files. An orchestrator that agrees with everything Cem says will miss problems. Athena V4 must include an adapted version.

4. **The Yellow Zone needs recalibration.** SOUL.md edits and production system changes should be Red Zone, not Yellow.

### Implementation Priority

| Step | Action | Time | Impact |
|------|--------|------|--------|
| **1** | Create TOOLS.md — migrate infrastructure, paths, channels, TTS config from V3 | 30 min | Removes ~730 tokens from SOUL.md |
| **2** | Create/update MEMORY.md — migrate Company Snapshot, Q2 Goals, pillar KPIs | 45 min | Removes ~430 tokens, creates proper persistent memory |
| **3** | Verify TASK_SHEET.md is sole source of truth — delete Active Projects from SOUL.md | 15 min | Removes ~220 tokens, eliminates dual-source-of-truth risk |
| **4** | Write Athena V4 SOUL.md using the 8-section architecture | 2 hours | Net new orchestrator identity at ~2,000 tokens |
| **5** | Write HEARTBEAT.md with pillar monitoring checklist | 1 hour | Enables structured proactive monitoring |
| **6** | Add Anti-Sycophancy section adapted from Ava | 15 min | Prevents the #1 LLM agent failure mode |
| **7** | Recalibrate Yellow/Red Zones | 15 min | Corrects governance miscalibration |
| **8** | Configure cron jobs for daily briefs and weekly reviews | 1 hour | Separates heavy analysis from heartbeat scans |

**Total estimated build time: ~6 hours for a production-grade orchestrator identity stack.**

### Council Closing Statement

> V3 represents Athena's first successful act of self-improvement — she identified what was missing in V1 and proposed concrete additions. The autonomy framework, learning loop, and operating rhythm are genuine innovations that most production agent deployments lack. What V3 reveals is that Athena already has the instinct of an operator. She just needs an editor to separate identity from infrastructure, policy from data, and behavior from status. V4 should be the result of that editing pass — not a rewrite, but a refactoring. Keep every behavioral insight from V3. Remove every line that belongs in another file. Add the anti-sycophancy safeguard from Ava. The result will be an orchestrator SOUL.md that scores 35+ out of 40 — and one that gets smarter every week through the learning loop V3 already defined.

---

## Appendix: Sources Referenced

- [OpenClaw System Prompt Architecture](https://docs.openclaw.ai/concepts/system-prompt) — Official docs on bootstrap file injection, char caps, SOUL.md vs AGENTS.md vs TOOLS.md separation
- [OpenClaw Architecture Explained (Substack)](https://ppaolo.substack.com/p/openclaw-system-architecture-overview) — Context assembly, file injection mechanics
- [Building Domain-Specific Agents with OpenClaw (Codebridge)](https://www.codebridge.tech/articles/how-to-build-domain-specific-ai-agents-with-openclaw-skills-soul-md-and-memory) — SOUL.md design principles, autonomy-escalation encoding, departmental patterns, file separation rules
- [Building an Autonomous AI Agent Team (Unwind AI)](https://www.theunwindai.com/p/how-i-built-an-autonomous-ai-agent-team-that-runs-24-7) — SOUL.md size guidance (40-60 lines), file-based coordination, personality engineering
- [How We Built Our Multi-Agent Research System (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system) — Orchestrator-worker delegation, self-improvement, effort scaling, prompt engineering for multi-agent systems
- [Claude Agent SDK Best Practices (Skywork)](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/) — Context isolation, CLAUDE.md conventions, subagent specialization
- [Claude Prompting Best Practices (Anthropic)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — System prompt design, subagent orchestration
- [Agentic AI Governance (Agility at Scale)](https://agility-at-scale.com/ai/governance/agentic-ai-governance/) — Three-tiered guardrail framework, authority tiers, audit trails, RACI matrices
- [OpenClaw Heartbeat Architecture (Saulius)](https://saulius.io/blog/openclaw-autonomous-ai-agent-framework-heartbeat-monitoring) — Heartbeat lifecycle, HEARTBEAT.md design, heartbeat vs cron distinction
- [Autonomous AI Agents: Heartbeat + Cron + Memory (DEV)](https://dev.to/linou518/autonomous-ai-agents-building-self-running-ai-with-heartbeat-cron-memory-14g9) — Three-layer architecture, token economy, GOALS.md permission levels
- [Recursive Knowledge Crystallization (DEV)](https://dev.to/gde/recursive-knowledge-crystallization-a-framework-for-persistent-autonomous-agent-self-evolution-4mk4) — Self-evolving SKILL.md, persistent meta-learning, filesystem-based knowledge persistence
- [AI Agent Orchestration Patterns (Microsoft Azure)](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — Sequential, concurrent, hierarchical orchestration patterns
- [OpenClaw Multi-Agent Setup: 7 Cron Prompts (YouTube)](https://www.youtube.com/watch?v=O-oFfCmw6Ys) — Heartbeat monitoring, morning briefs, cross-functional syncs

---

# PART II: THE SELF-AWARE AGENT PROBLEM — Deep Architecture Extension

**Council addendum — April 10, 2026**

> "The fundamental insight is that learning is not a feature you add to an agent — it is the architecture itself. Without structured reflection, an agent running for 6 months is no smarter than the day it was deployed. With it, every failure compounds into capability." — Council consensus

---

## The Core Challenge

How does an agent get better at its job when it has no gradient descent, no weight updates, no training loop? The answer, per both the [Reflexion framework](https://www.promptingguide.ai/techniques/reflexion) and [Voyager's skill library](https://voyager.minedojo.org), is the same mechanism humans use: **externalized reflection written to persistent storage**.

In Athena's case, "persistent storage" means Markdown files on the filesystem. The entire self-improvement architecture must operate within these constraints:

- Athena cannot modify her own model weights
- Her context window resets between sessions (compaction)
- Her only persistent state is files: SOUL.md, MEMORY.md, mistakes.md, daily logs, skills, Vault
- She has access to sub-agents (Ava, Harry, Hermes) and local compute (Gemma 4 via Ollama)
- She has cron jobs and heartbeats for scheduled execution
- Changes to her own SOUL.md require Cem's approval (Red Zone)

The question is: within these constraints, how do we build something that meaningfully evolves?

---

## 1. The Reflection Engine

### What Reflection Actually Is (and Isn't)

Reflection is not "reading a log file." Per the [Multi-Agent Reflexion (MAR) research](https://arxiv.org/html/2512.20845v1), single-agent self-reflection has a critical failure mode: **confirmation bias**. When the same model that generated the action also evaluates it, it tends to repeat the same flawed reasoning — a phenomenon called "degeneration-of-thought." MAR demonstrated that replacing single-agent self-critique with multi-agent debate improved performance from 76.4% to 82.6% on code generation tasks.

This means: **Athena should never be the sole evaluator of her own work.** The reflection engine must involve at least two distinct perspectives.

### Data Sources for Reflection

Athena's reflection engine should consume these inputs, in priority order:

| Data Source | Location | What It Contains | Signal Type |
|-------------|----------|-----------------|-------------|
| **Cem's corrections** | Session logs, daily memory | Direct behavioral feedback ("don't do X", "I prefer Y", overrides) | Highest — explicit human signal |
| **mistakes.md** | `data/mistakes.md` | Logged failures with root cause analysis | High — acknowledged errors |
| **TASK_SHEET.md** | `Vault/00-Company/compiled/TASK_SHEET.md` | Task status, overdue items, completion rates | High — objective outcomes |
| **Project ETAs hit/missed** | Task sheet + daily logs | Planned vs actual completion dates | High — predictive accuracy signal |
| **Sub-agent outputs** | Daily logs, Vault project folders | Quality of delegated work, revision count, time to completion | Medium — delegation effectiveness |
| **Cem's unsolicited questions** | Session logs | Things Cem asked that Athena should have proactively surfaced | Medium — proactivity gap signal |
| **Session compaction summaries** | Session archive (memory.db) | What the model considered important enough to retain after compaction | Low — attention signal |
| **Cron job success/failure logs** | `Vault/00-Company/compiled/CRON_SCHEDULE.md` + system logs | Operational reliability | Low — infrastructure signal |

### The Five Reflection Questions

Per [the Reflexion framework's self-reflection module](https://www.promptingguide.ai/techniques/reflexion), structured self-questioning produces better reflections than freeform review. Athena's reflection should answer these five questions, every week:

**Q1: What did I accomplish this week?**
- Pull from: completed tasks in TASK_SHEET, merged project milestones, Cem's acknowledgments
- Output: Numbered list of accomplishments with goal linkage (G1-G7)
- Purpose: Establishes a baseline of productive work. Prevents negativity bias where only failures are remembered.

**Q2: What failed or underperformed?**
- Pull from: mistakes.md entries, overdue tasks, Cem corrections, sub-agent revision cycles
- Output: Numbered list with root cause for each
- Purpose: Raw material for habit change detection

**Q3: What patterns do I see across failures?**
- This is the critical question. One-off failures get logged; patterns get elevated to standing rules.
- Pull from: Last 4 weeks of Q2 answers. Look for: same pillar failing repeatedly, same sub-agent underperforming, same type of Cem correction recurring, same blocker type appearing
- **Distinguishing one-off vs. systemic:** A failure is systemic if it has occurred 3+ times in 4 weeks OR if it has a structural cause (wrong routing, missing data, unclear authority). A failure is one-off if it was caused by a unique external event (one-time API outage, atypical Cem request).
- Output: Each pattern gets classified as `ONE-OFF | RECURRING | SYSTEMIC` with proposed remedy

**Q4: What assumptions was I operating under that proved wrong?**
- Pull from: Decisions where the outcome diverged significantly from expectation
- Example: "I assumed Jay Mark would complete the Supabase migration by Apr 15 because he said he would. He didn't. My assumption that stated ETAs from human builders are reliable is wrong. New rule: add 40% buffer to human-builder ETAs and check in at 60% of stated timeline."
- Output: Revised assumptions, added to MEMORY.md → "Standing Rules"

**Q5: What should I have surfaced proactively that I didn't?**
- Pull from: Cem's unsolicited questions during the week. Every time Cem asks "what's the status of X?" or "did Y happen?" — that's a signal Athena failed to surface it.
- Output: Proposed additions to HEARTBEAT.md checklist or daily brief template

### Reflection Output Format

The weekly reflection produces a structured document:

```markdown
# Weekly Reflection — [Date Range]

## Accomplishments (Q1)
1. [Accomplishment] → [Goal served]
2. ...

## Failures & Underperformance (Q2)
1. [Failure] | Root cause: [X] | Classification: ONE-OFF / RECURRING / SYSTEMIC
2. ...

## Patterns Detected (Q3)
- SYSTEMIC: [Pattern description] → Proposed remedy: [specific file change or process change]
- RECURRING: [Pattern description] → Monitoring: [what to watch next week]

## Assumptions Revised (Q4)
- OLD: [Previous assumption]
- NEW: [Updated assumption]
- Action: [Where this gets encoded — MEMORY.md, delegation rules, etc.]

## Proactivity Gaps (Q5)
- Cem asked about [X] on [date] — I should have surfaced this in [morning brief / heartbeat]
- Proposed HEARTBEAT.md addition: [specific checklist item]

## Proposed Changes (require Cem approval)
- [ ] SOUL.md: [Specific amendment]
- [ ] HEARTBEAT.md: [Specific addition]
- [ ] New cron job: [Description]
- [ ] New skill: [Description]

## Self-Score: [1-10] — Rationale: [one sentence]
```

---

## 2. Habit Change Mechanism

### The Problem

In a human, "changing a habit" means the neural pathways that fire during a decision get restructured over time. In a Markdown-based agent, the equivalent is: **the context that gets loaded at the moment of decision changes**. Athena's "habits" are literally the text she reads at the start of every turn. To change a habit, you change what she reads.

But SOUL.md is Red Zone (can't self-modify). And it shouldn't grow indefinitely. So where do new behavioral rules live?

### The Four-Step Habit Change Lifecycle

#### Step 1: Detection

A habit problem is detected when a pattern appears in reflection data:

**Detection signals:**
- Same mistake in `mistakes.md` 3+ times in 4 weeks
- Same Cem correction 2+ times (lower threshold — Cem's time is more expensive)
- Delegation to wrong sub-agent identified in post-hoc analysis
- A pillar consistently under-monitored (Cem keeps asking about it)
- A process Athena does manually that could be automated (Hermes can identify these)

**Detection mechanism:** The weekly Reviewer subagent (see Section 4) runs a pattern-matching scan over the past 4 weeks of data. It produces a `PATTERNS_DETECTED` section in the weekly review.

**Example detection:**
```
PATTERN DETECTED: Over-delegation to Ava
- 3 of last 5 finance-adjacent tasks were routed to Ava instead of Harry
- Ava escalated 2 of them back as "not my domain"
- Root cause: Athena's delegation tree says "Needs strategy?" → Ava,
  but some tasks that look strategic are actually financial
- Classification: SYSTEMIC
- Proposed fix: Add a pre-check to delegation: "Does this task involve
  numbers, costs, margins, or financial projections? → Harry first,
  even if it looks strategic"
```

#### Step 2: Encoding — Where Does the New Rule Live?

This is the critical architectural decision. The answer depends on the rule's scope and stability:

| Rule Type | Encode In | Loaded When | Example |
|-----------|-----------|-------------|---------|
| **Core behavioral change** (how Athena decides, communicates, or escalates) | SOUL.md amendment — requires Cem approval (Red Zone) | Every turn | "Always present financial decisions with both optimistic and conservative scenarios" |
| **Delegation routing rule** (which sub-agent gets what) | MEMORY.md → "Routing Rules" section | Every turn (MEMORY.md is bootstrap-injected) | "Finance-adjacent tasks → Harry first, even if they look strategic" |
| **Domain-specific heuristic** (how to handle a specific recurring situation) | Relevant skill file in `Vault/00-Company/skills/` | On demand when that skill is loaded | "When reviewing Amazon listings, always check mobile render first — 70% of traffic is mobile" |
| **Monitoring rule** (what to check proactively) | HEARTBEAT.md | Heartbeat turns only | "Check Harry's task queue every morning heartbeat — if >3 items overdue, escalate" |
| **Temporary operational rule** (valid for a limited time) | MEMORY.md → "Active Rules (Temporary)" with expiry date | Every turn | "Until One Piece launch complete: flag any design task not linked to G1" |

**The key principle:** The more stable and fundamental the rule, the higher up the file hierarchy it lives (SOUL.md > MEMORY.md > Skill files > HEARTBEAT.md). The more specific and volatile, the lower.

#### Step 3: Activation — How the Rule Gets Into Context

This is where Athena's file-based architecture actually has an advantage over parameter-based learning: **the rule is immediately active** the moment it's written to the right file. There's no training step, no delay, no gradient update.

- **SOUL.md rules:** Active on every turn after Cem approves and the file is updated.
- **MEMORY.md rules:** Active on every turn immediately. Athena can write to MEMORY.md herself (Green Zone). This is the primary mechanism for fast habit change.
- **Skill file rules:** Active on demand when the relevant skill is loaded. Athena can write to skill files (Green Zone for existing files; Yellow Zone for new skills — see Section 3).
- **HEARTBEAT.md rules:** Active on every heartbeat. Athena can propose changes (Yellow Zone — do + notify Cem).

**The MEMORY.md fast lane:** For most habit changes, the fastest path is:
1. Reflection detects pattern
2. Athena writes new rule to MEMORY.md → "Routing Rules" or "Standing Rules"
3. Rule is immediately active on next turn (MEMORY.md is bootstrap-injected per [OpenClaw docs](https://docs.openclaw.ai/concepts/system-prompt))
4. If the rule proves effective over 4 weeks, propose promoting it to SOUL.md for permanence
5. If the rule proves ineffective, remove it from MEMORY.md during next pruning cycle

#### Step 4: Validation — Did the Habit Change Work?

A changed habit is meaningless if you don't verify it improved outcomes. The validation protocol:

1. **Tag the rule with a creation date** in MEMORY.md: `[RULE-2026-04-15] Finance-adjacent tasks → Harry first`
2. **Track instances** where the rule fires: Add to daily log each time the rule influenced a decision
3. **Review at the 4-week mark** during the monthly strategic reflection:
   - Did the failure pattern that triggered this rule recur? If no → rule is working → keep/promote
   - Did the rule create new problems? (e.g., Harry is now overloaded because too many tasks routed to him) If yes → refine the rule
   - Was the rule never triggered? → The problem may have been one-off after all → consider removing
4. **Quantitative signal:** Track the ratio of "Cem corrections on this topic" before and after the rule. If corrections dropped → rule is working.

### The Habit Change Pipeline — Visual

```
mistakes.md / logs / Cem corrections
         │
         ▼
  ┌──────────────────┐
  │  Pattern Scan     │  ← Weekly Reviewer subagent
  │  (3+ occurrences? │
  │   Cem correction? │
  │   Structural?)    │
  └────────┬─────────┘
           │ Pattern confirmed
           ▼
  ┌──────────────────┐
  │  Classify & Draft │  ← Athena
  │  (ONE-OFF →       │
  │   ignore.          │
  │   RECURRING →      │
  │   MEMORY.md rule.  │
  │   SYSTEMIC →       │
  │   SOUL.md proposal)│
  └────────┬─────────┘
           │
     ┌─────┴──────┐
     │             │
     ▼             ▼
  MEMORY.md     SOUL.md
  (immediate)   (Cem approval)
     │             │
     ▼             ▼
  ┌──────────────────┐
  │  Validate @ 4wk  │
  │  (recurrence?    │
  │   new problems?  │
  │   Cem feedback?) │
  └────────┬─────────┘
           │
     ┌─────┴──────┐
     │             │
     ▼             ▼
  Keep/Promote  Refine/Remove
```

---

## 3. Skill Evolution Protocol

### The Voyager Insight

[Voyager](https://voyager.minedojo.org) demonstrated that agents with a growing skill library outperform static agents by 3.3x on novel tasks. The key mechanism: successful action sequences are abstracted into reusable, named functions indexed by their purpose. Per [EvoSkills](https://arxiv.org/html/2604.01687v1), agent-generated skills can actually outperform human-curated ones because they "capture the reasoning patterns and tool-use strategies that agents actually need."

Athena should build her own skill library. Here's how.

### Trigger: When Does Athena Recognize "I Need a New Skill"?

| Trigger Condition | Detection Method | Example |
|-------------------|-----------------|---------|
| **Repeated manual workflow** | Same sequence of 5+ steps executed 3+ times in 4 weeks | Athena manually checks Amazon listing health the same way every time — this should be a skill |
| **Domain gap identified during reflection** | Q5 reflection question surfaces a pillar with no skill coverage | Marketing pillar has no skill file but Cem keeps asking about ad performance |
| **Sub-agent repeatedly needs the same context** | Same context block copy-pasted into 3+ Ava/Harry delegations | Every time Athena delegates a listing task, she includes the same 15 lines of listing standards |
| **New tool or API becomes available** | Cem connects a new integration or Hermes discovers a capability | BigQuery pipeline goes live → need a "bq-analytics" skill to standardize how Athena queries it |
| **Cem explicitly requests a capability** | Direct instruction | "I want you to be able to audit our Walmart listings" |
| **Cross-pillar pattern requires codification** | Monthly reflection surfaces a process that spans multiple pillars | License launch process (Creative → Product Dev → Sales → Marketing) always follows the same sequence |

### Creation: Minimum Viable Skill Structure

Per [OpenClaw's SKILL.md format](https://docs.openclaw.ai/tools/skills) and [the Agensi reference](https://www.agensi.io/learn/skill-md-format-reference), the minimum viable skill is a folder with one file:

```
Vault/00-Company/skills/listing-audit/
├── SKILL.md
└── references/
    └── listing-standards.md  (optional — loaded on demand)
```

**SKILL.md minimum template:**

```yaml
---
name: listing-audit
description: Audit Amazon/Walmart/eBay listings for compliance, image quality,
  and conversion optimization. Use when Cem asks to check listings, when
  heartbeat detects listing alerts, or when a new product launches.
---

# Listing Audit

## Purpose
Check listings across marketplaces for compliance, image quality, content
accuracy, and conversion optimization signals.

## Steps
1. Identify the scope: which ASINs/SKUs, which marketplaces
2. For each listing, check:
   - Title matches template (brand + product type + device + variant)
   - All 7 image slots filled; hero image is HB401-quality
   - Bullet points present and keyword-optimized
   - Price within expected range (check MEMORY.md for pricing rules)
   - Buy Box status (Amazon only)
   - Mobile render check — 70% of traffic is mobile
3. Flag issues by severity: CRITICAL (suppression risk), WARNING (CVR impact), INFO (nice-to-have)
4. Output as structured table: ASIN | Marketplace | Issue | Severity | Recommended Fix

## Edge Cases
- If listing is suppressed: escalate immediately via Telegram (CRITICAL)
- If no image data available (API limitation): note gap, move to next
- If marketplace API is rate-limited: queue and retry on next heartbeat

## Never
- Do not modify live listings without Cem approval (Red Zone)
- Do not assume pricing is wrong — check MEMORY.md first
```

### Athena's Skill Drafting Protocol

When a trigger condition is met:

1. **Athena drafts the SKILL.md** using the template above. She writes it to a staging location: `Vault/00-Company/skills/_drafts/[skill-name]/SKILL.md`
2. **She runs a self-test:** Can she execute the skill steps with her current tools? Does the skill reference files that exist? Are the trigger conditions specific enough for auto-discovery?
3. **She proposes the skill to Cem** in the next daily brief or immediately if it addresses an active blocker:
   ```
   NEW SKILL PROPOSED: listing-audit
   Trigger: I've manually audited listings 4 times this month using the same process.
   This skill codifies that process for reuse.
   Location: Vault/00-Company/skills/_drafts/listing-audit/SKILL.md
   Estimated token cost when loaded: ~400 tokens
   Request: Approve for deployment to skills/ (Yellow Zone)
   ```
4. **On Cem's approval:** Move from `_drafts/` to `Vault/00-Company/skills/listing-audit/`
5. **OpenClaw auto-discovers it** via the skills watcher ([per docs](https://docs.openclaw.ai/tools/skills), `skills.load.watch: true` is the default — it detects new SKILL.md files automatically)

### Skill Testing Protocol

Before proposing a skill:

1. **Dry run:** Execute the skill steps on a small sample (e.g., 3 ASINs instead of 50). Verify outputs match expected format.
2. **Edge case test:** Deliberately test one edge case from the "Edge Cases" section. Verify the handling works.
3. **Token budget check:** The skill should be under 500 lines per [best practice](https://www.agensi.io/learn/skill-md-format-reference). Estimate token cost of the frontmatter (always loaded for discovery, ~50-100 tokens) vs. full body (loaded on demand).
4. **Conflict check:** Does this skill overlap with an existing one? If so, extend the existing skill rather than creating a duplicate.

### Skill Retirement Protocol

A skill should be deprecated when:
- It hasn't been loaded in 8+ weeks (no demand signal)
- The process it codifies has fundamentally changed (e.g., marketplace API changed)
- It was absorbed into a broader skill (e.g., "listing-audit-amazon" merged into "listing-audit-all")
- Cem explicitly decides the capability is no longer needed

Retirement process:
1. Move to `Vault/00-Company/skills/_retired/[skill-name]/`
2. Add a note to MEMORY.md: `[SKILL RETIRED: listing-audit-v1, 2026-07-01, reason: merged into listing-audit-v2]`
3. OpenClaw stops discovering it (it's no longer in the skills path)

---

## 4. Multi-Agent Reflection Loop

### Why Athena Must Not Reflect Alone

Per [Multi-Agent Reflexion (MAR)](https://arxiv.org/html/2512.20845v1), single-agent self-reflection suffers from confirmation bias — the same model that made the mistake evaluates the mistake, and tends to repeat its flawed reasoning. MAR showed that introducing diverse critic personas improved error correction by 6+ percentage points.

Athena has a unique advantage: she already has a multi-agent network. She should use it.

### The Weekly Reflection Cycle — Roles and Responsibilities

```
┌──────────────────────────────────────────────────────────────┐
│                    SUNDAY NIGHT CYCLE                         │
│                   (Automated via cron)                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  PHASE 1: Data Gathering (overnight, cheap)                  │
│  ┌─────────────┐                                             │
│  │  Gemma 4    │  Local Ollama ($0)                          │
│  │  (Parser)   │  Reads: daily logs, mistakes.md,            │
│  │             │  TASK_SHEET, cron logs, session archive      │
│  │             │  Produces: structured JSON summary           │
│  │             │  → data/reflection/YYYY-WW-raw.json         │
│  └──────┬──────┘                                             │
│         │                                                    │
│  PHASE 2: Analysis (Sunday night / Monday early AM)          │
│         ▼                                                    │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Reviewer   │    │   Hermes    │    │    Ava      │      │
│  │  Subagent   │    │ (Code/Data) │    │ (Strategy)  │      │
│  │  (Sonnet)   │    │             │    │             │      │
│  │             │    │ Reads: cron │    │ Reads: raw  │      │
│  │ Reads: raw  │    │ configs,    │    │ JSON +      │      │
│  │ JSON +      │    │ scripts,    │    │ project     │      │
│  │ mistakes.md │    │ raw JSON    │    │ status      │      │
│  │             │    │             │    │             │      │
│  │ Produces:   │    │ Produces:   │    │ Produces:   │      │
│  │ Behavioral  │    │ Automation  │    │ Strategic   │      │
│  │ critique    │    │ proposals   │    │ patterns    │      │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │
│         │                  │                  │              │
│  PHASE 3: Synthesis                                          │
│         └─────────┬────────┘────────┬─────────┘              │
│                   ▼                                          │
│           ┌──────────────┐                                   │
│           │   Athena     │  Reads all three analyses         │
│           │  (Synthesis) │  Produces: WEEKLY_REVIEW.md       │
│           │              │  with PROPOSED changes            │
│           └──────┬───────┘                                   │
│                  │                                           │
│  PHASE 4: Human Review                                       │
│                  ▼                                           │
│           ┌──────────────┐                                   │
│           │     Cem      │  Reviews on Monday morning        │
│           │              │  Marks: APPROVED / REJECTED /     │
│           │              │  MODIFIED for each proposal       │
│           └──────┬───────┘                                   │
│                  │                                           │
│  PHASE 5: Execution                                          │
│                  ▼                                           │
│           ┌──────────────┐                                   │
│           │   Athena     │  Applies APPROVED changes to      │
│           │  (Executor)  │  MEMORY.md, HEARTBEAT.md, skills, │
│           │              │  cron configs. Queues SOUL.md      │
│           │              │  changes for next approval.        │
│           └──────────────┘                                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Each Agent's Specific Role

#### Gemma 4 (Parser) — Phase 1

**Why Gemma 4:** It's local ($0 cost), good at structured extraction, and runs overnight when no other agent needs the Mac Studio. This is batch processing, not reasoning — perfect for a local model.

**Input files:**
- `memory/2026-04-07.md` through `memory/2026-04-13.md` (daily logs)
- `data/mistakes.md` (filtered to this week's entries)
- `Vault/00-Company/compiled/TASK_SHEET.md` (current state)
- `Vault/00-Company/compiled/CRON_SCHEDULE.md` (job outcomes)
- Session archive diffs from `data/memory.db`

**Output:** `data/reflection/2026-W16-raw.json`

```json
{
  "week": "2026-W16",
  "period": "2026-04-07 to 2026-04-13",
  "tasks_completed": 12,
  "tasks_overdue": 3,
  "tasks_blocked": 2,
  "mistakes_logged": 4,
  "cem_corrections": [
    {"date": "2026-04-08", "type": "communication", "detail": "Too much detail in morning brief — Cem said 'just bullets'"},
    {"date": "2026-04-11", "type": "routing", "detail": "Sent pricing analysis to Ava, Cem redirected to Harry"}
  ],
  "cem_unsolicited_questions": [
    {"date": "2026-04-09", "topic": "Walmart listing status", "pillar": "Sales"},
    {"date": "2026-04-12", "topic": "CLC royalty deadline", "pillar": "Finance"}
  ],
  "goals_progress": {
    "G1": {"start_pct": 25, "end_pct": 35, "delta": 10},
    "G2": {"start_pct": 15, "end_pct": 15, "delta": 0, "flag": "STALLED"}
  },
  "pillar_activity": {
    "Creative": {"tasks": 5, "completed": 4, "blocked": 1},
    "Sales": {"tasks": 3, "completed": 2, "blocked": 0},
    "Finance": {"tasks": 2, "completed": 0, "blocked": 1}
  },
  "cron_failures": [
    {"job": "vault-compile", "date": "2026-04-10", "error": "timeout"}
  ],
  "delegation_summary": {
    "to_ava": {"count": 6, "success": 4, "revision_needed": 2},
    "to_harry": {"count": 2, "success": 1, "no_response": 1},
    "to_jaymark": {"count": 3, "success": 2, "overdue": 1}
  }
}
```

#### Reviewer Subagent (Claude Sonnet) — Phase 2a

**Why a separate subagent:** Per [MAR research](https://arxiv.org/html/2512.20845v1), the critic must be a distinct entity from the actor to avoid confirmation bias. Spawning a Sonnet subagent with its own session ensures it evaluates Athena's work without access to Athena's justifications.

**Spawn method:** Athena spawns via `sessions_spawn` (OpenClaw subagent) or Claude Code `--` subagent with a focused system prompt:

```
You are a performance reviewer for an AI orchestrator agent named Athena.
You are NOT Athena. You are evaluating her work from the outside.
Your job: identify what she did wrong, what patterns you see, and what
she should change. Be blunt. Do not soften criticism. Do not praise
unless the accomplishment is genuinely notable.

Review the structured data below and produce:
1. Top 3 failures this week (with root cause analysis)
2. Behavioral patterns detected (recurring across 3+ weeks)
3. Delegation effectiveness score (0-10) with justification
4. Communication effectiveness score (0-10) with justification
5. One specific habit change recommendation
```

**Input:** The Gemma 4 JSON + current MEMORY.md → "Standing Rules" section (to check if existing rules were followed)

**Output:** `data/reflection/2026-W16-reviewer.md`

#### Hermes (Claude Code / Data Agent) — Phase 2b

**Why Hermes:** Hermes has access to the codebase, cron configurations, and data pipelines. It can identify automation opportunities that Athena, operating at the strategic level, would miss.

**Input:** The Gemma 4 JSON (focusing on `cron_failures` and `delegation_summary`) + access to the cron configs and scripts

**Specific questions:**
1. Are any of Athena's recurring manual tasks automatable with a new cron job?
2. Are any cron jobs failing repeatedly? What's the fix?
3. Is there a data pipeline that should exist but doesn't? (E.g., "Athena manually checks Walmart listings every week — this should be a scheduled audit")
4. Are there shell scripts or tools that could save Athena token costs?

**Output:** `data/reflection/2026-W16-hermes.md` — a list of automation proposals

#### Ava (Strategy Review) — Phase 2c

**Why Ava:** Ava owns strategy across all pillars and has her own sub-agents. She can identify strategic-level patterns that operational data alone won't reveal.

**Input:** The Gemma 4 JSON (focusing on `goals_progress`, `pillar_activity`, and `tasks_blocked`) + her own `MEMORY_BUSINESS_CONTEXT.md`

**Specific questions:**
1. Are any goals stalled for structural reasons (not just task-level blockers)?
2. Is the same pillar consistently under-resourced?
3. Are there cross-pillar dependencies that are creating hidden bottlenecks?
4. Based on market/competitive intelligence, should goal priorities shift?

**Output:** `data/reflection/2026-W16-ava.md` — strategic pattern analysis

### Athena's Synthesis — Phase 3

Athena reads all three analysis outputs and produces the unified `WEEKLY_REVIEW.md`:

```markdown
# Weekly Review — 2026-W16 (Apr 7-13)

## Performance Summary
- Tasks completed: 12/17 (71%) — below 80% target
- Goals progress: G1 +10%, G2 STALLED, G3 +5%, G4 blocked, G5 no movement
- Delegation success rate: Ava 67%, Harry 50%, Jay Mark 67%

## Reviewer Findings (Sonnet subagent)
[Inserted from reviewer output — top 3 failures, patterns, scores]

## Automation Opportunities (Hermes)
[Inserted from Hermes output — proposed new cron jobs, script fixes]

## Strategic Patterns (Ava)
[Inserted from Ava output — goal-level analysis, cross-pillar issues]

## Proposed Changes

### Immediate (MEMORY.md — Green Zone, applying now)
- [x] RULE: Finance-adjacent tasks → Harry first, even if strategic-looking
- [x] RULE: Morning brief max 5 bullets, no paragraphs (Cem correction 2x this week)

### Needs Cem Approval
- [ ] HEARTBEAT.md: Add Walmart listing check to Tuesday 10AM heartbeat
- [ ] HEARTBEAT.md: Add CLC royalty deadline to Finance daily check
- [ ] NEW CRON: Weekly Walmart listing audit (Sat night, Gemini Flash)
- [ ] NEW SKILL: walmart-audit (draft at _drafts/walmart-audit/SKILL.md)
- [ ] SOUL.md: Amend delegation tree — add finance pre-check before routing

### Deferred (needs more data)
- WATCHING: Harry responsiveness — 50% this week. If <60% next week, propose staffing escalation.

## Self-Score: 6/10
Rationale: Good progress on G1 and G3 but G2 stalled with no remediation action. Two Cem corrections on communication format that should not have been needed — the brief format rule was clear and I ignored it. Delegation to Harry needs improvement.
```

### Cem's Monday Morning

Cem receives this via Telegram at 8:00 AM Monday. He reviews the "Needs Cem Approval" section and responds with approvals/rejections. Athena then executes the approved changes immediately.

---

## 5. Knowledge Gap Detection

### The Taxonomy

Athena operates in a complex information environment. She doesn't know what she doesn't know — unless she has a framework for detecting gaps. Adapting from [knowledge gap research](https://onlinelibrary.wiley.com/doi/10.1111/tops.12584) to Athena's operational context:

| Gap Type | Description | Detection Signal | Resolution Path |
|----------|-------------|-----------------|-----------------|
| **Missing Data** | Information exists somewhere but Athena can't access it | Athena needs a number/fact to make a decision but can't find it in Vault, memory, or via search | Request from sub-agent with data access (Hermes for BQ, Harry for Xero, Ava for competitive intel) |
| **Missing Context** | A deadline, constraint, or stakeholder expectation Athena doesn't know about | Cem corrects a decision because Athena didn't know about a factor ("the licensor said no gaming imagery") | Ask Cem directly, then encode in MEMORY.md → "Standing Rules" or relevant skill file |
| **Missing Capability** | Athena needs to do something her tools can't do | A task requires an API, integration, or computation Athena can't perform | Flag as blocker. Propose: new skill, new cron job, new tool integration, or delegation to Jay Mark for building |
| **Missing Authority** | Unclear who owns a decision or whether Athena can act | Athena hesitates because the action falls between Green and Yellow zones | Ask Cem for a one-time ruling, then encode the precedent in MEMORY.md → "Authority Precedents" |
| **Missing Measurement** | A goal or KPI has no tracking mechanism | Athena is supposed to monitor a metric but there's no data pipeline feeding it | Flag to Hermes for pipeline creation, or propose a manual check in HEARTBEAT.md until automation exists |
| **Stale Knowledge** | Information Athena has is outdated | A decision made on old data produces a bad outcome (e.g., pricing based on last quarter's COGS) | Flag the knowledge as stale in MEMORY.md with a refresh cadence. Create a cron job or heartbeat check to keep it current. |

### Detection Mechanism: The Gap Register

Athena should maintain a running register of known knowledge gaps in MEMORY.md:

```markdown
## Known Knowledge Gaps (Updated Weekly)

### ACTIVE — Blocking or Degrading Decisions
| ID | Type | Description | Impact | Resolution Owner | ETA |
|----|------|-------------|--------|-----------------|-----|
| KG-01 | Missing Data | No real-time PH inventory in BigQuery | Can't do accurate stock analysis | Cem + Athena (G3) | Apr 20 |
| KG-02 | Missing Context | Don't know all licensor image restrictions | Risk of listing rejection | Ava (research) | Ongoing |
| KG-03 | Missing Capability | No automated Walmart listing audit | Manual checks only, weekly | Proposed skill: walmart-audit | Pending approval |

### RESOLVED (Last 30 Days)
| ID | Type | Resolved | How |
|----|------|----------|-----|
| KG-00 | Missing Measurement | 2026-04-05 | Created PULSE conversion dashboard |
```

### How Gaps Feed Into Skill Creation and Data Pipelines

The gap register is a direct input to:

1. **Skill creation triggers:** Any gap of type "Missing Capability" that persists for 2+ weeks should trigger the Skill Evolution Protocol (Section 3). If the capability can be codified as a repeatable process, it becomes a skill.

2. **Cron job proposals:** Any gap of type "Missing Data" or "Missing Measurement" that requires periodic data refresh should trigger a cron job proposal. Hermes identifies these during the weekly reflection and proposes the automation.

3. **Delegation briefs:** When delegating a task in a domain with known gaps, Athena should explicitly note the gap in the brief: "Note: We don't have real-time PH inventory data yet (KG-01). Use last week's export as a proxy and flag any decisions that would change with fresher data."

4. **Goal planning:** The monthly strategic reflection should review the gap register and ask: "Which of these gaps, if resolved, would have the highest impact on goal progress?" This feeds into prioritization for the next quarter.

---

## 6. The Virtuous Loop — Full Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    ATHENA SELF-IMPROVEMENT ARCHITECTURE                  ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  ┌─────────────────────── DATA INPUTS ─────────────────────────┐        ║
║  │                                                              │        ║
║  │  Daily Logs ─────┐                                           │        ║
║  │  mistakes.md ────┤                                           │        ║
║  │  TASK_SHEET ─────┤    Every day, continuously                │        ║
║  │  Cem feedback ───┤──▶ Written to filesystem                  │        ║
║  │  Sub-agent output┤    by Athena during normal operations     │        ║
║  │  Cron logs ──────┤                                           │        ║
║  │  Session archive ┘                                           │        ║
║  │                                                              │        ║
║  └──────────────────────────┬───────────────────────────────────┘        ║
║                             │                                            ║
║                             ▼ Sunday night                               ║
║  ┌──────────────── PROCESSING LAYER 1 ─────────────────────────┐        ║
║  │                                                              │        ║
║  │  ┌──────────┐                                                │        ║
║  │  │ Gemma 4  │  $0 local — parses raw data into structured   │        ║
║  │  │ (Parser) │  JSON: counts, patterns, anomalies             │        ║
║  │  └────┬─────┘                                                │        ║
║  │       │ data/reflection/YYYY-WW-raw.json                     │        ║
║  └───────┼──────────────────────────────────────────────────────┘        ║
║          │                                                               ║
║          ▼ Sunday night / Monday early AM                                ║
║  ┌──────────────── PROCESSING LAYER 2 ─────────────────────────┐        ║
║  │                                                              │        ║
║  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │        ║
║  │  │ Reviewer │  │  Hermes  │  │   Ava    │                   │        ║
║  │  │ (Sonnet) │  │(Code/BQ) │  │(Strategy)│                   │        ║
║  │  │          │  │          │  │          │                   │        ║
║  │  │Behavioral│  │Automation│  │Strategic │                   │        ║
║  │  │ critique │  │proposals │  │ patterns │                   │        ║
║  │  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │        ║
║  │       │              │              │                         │        ║
║  └───────┼──────────────┼──────────────┼────────────────────────┘        ║
║          │              │              │                                  ║
║          ▼              ▼              ▼ Monday AM                        ║
║  ┌──────────────── SYNTHESIS LAYER ────────────────────────────┐        ║
║  │                                                              │        ║
║  │  ┌────────────────┐                                          │        ║
║  │  │    Athena      │  Reads all 3 analyses                    │        ║
║  │  │  (Synthesizer) │  Produces: WEEKLY_REVIEW.md              │        ║
║  │  │                │  With PROPOSED changes categorized:       │        ║
║  │  │                │    • Green (apply now to MEMORY.md)       │        ║
║  │  │                │    • Yellow (apply + notify)              │        ║
║  │  │                │    • Red (needs Cem approval)             │        ║
║  │  └───────┬────────┘                                          │        ║
║  │          │                                                    │        ║
║  └──────────┼────────────────────────────────────────────────────┘        ║
║             │                                                            ║
║             ▼ Monday morning                                             ║
║  ┌──────────────── HUMAN-IN-THE-LOOP ──────────────────────────┐        ║
║  │                                                              │        ║
║  │  ┌────────────────┐                                          │        ║
║  │  │      Cem       │  Reviews WEEKLY_REVIEW.md via Telegram   │        ║
║  │  │                │  Marks each proposal:                     │        ║
║  │  │                │    ✅ APPROVED                             │        ║
║  │  │                │    ❌ REJECTED (with reason)               │        ║
║  │  │                │    ✏️  MODIFIED (with changes)             │        ║
║  │  └───────┬────────┘                                          │        ║
║  │          │                                                    │        ║
║  └──────────┼────────────────────────────────────────────────────┘        ║
║             │                                                            ║
║             ▼ Monday, after Cem's response                               ║
║  ┌──────────────── OUTPUT ACTIONS ─────────────────────────────┐        ║
║  │                                                              │        ║
║  │  Athena executes approved changes:                           │        ║
║  │                                                              │        ║
║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │        ║
║  │  │  MEMORY.md  │  │HEARTBEAT.md │  │  New Skill  │         │        ║
║  │  │  new rules, │  │  new checks │  │  deployed   │         │        ║
║  │  │  updated    │  │  added      │  │  to skills/ │         │        ║
║  │  │  preferences│  │             │  │             │         │        ║
║  │  └─────────────┘  └─────────────┘  └─────────────┘         │        ║
║  │                                                              │        ║
║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │        ║
║  │  │  New Cron   │  │  SOUL.md    │  │  Knowledge  │         │        ║
║  │  │  job added  │  │  amendment  │  │  Gap flagged│         │        ║
║  │  │  to schedule│  │  (queued)   │  │  or resolved│         │        ║
║  │  └─────────────┘  └─────────────┘  └─────────────┘         │        ║
║  │                                                              │        ║
║  └──────────────────────────────────────────────────────────────┘        ║
║                                                                          ║
║             │                                                            ║
║             ▼ Next week                                                  ║
║  ┌──────────────── FEEDBACK VALIDATION ────────────────────────┐        ║
║  │                                                              │        ║
║  │  Did the changes improve outcomes?                           │        ║
║  │                                                              │        ║
║  │  • Did the failure pattern recur?        YES → refine rule   │        ║
║  │  • Did Cem corrections decrease?         YES → rule working  │        ║
║  │  • Did new problems emerge?              YES → revert/adjust │        ║
║  │  • Did goal progress accelerate?         YES → reinforce     │        ║
║  │  • Was the new skill used?               NO  → reassess need │        ║
║  │                                                              │        ║
║  │  Feed results back into next week's DATA INPUTS ──────────▶ ║        ║
║  │                                                    (top)     │        ║
║  └──────────────────────────────────────────────────────────────┘        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Monthly Aggregation

Every 4 weeks, the weekly reviews are themselves reviewed in a monthly strategic reflection:

1. **Gemma 4** aggregates the 4 weekly JSONs into a monthly summary
2. **Athena** produces a `MONTHLY_SELF_ASSESSMENT.md`:
   - Performance trend across 4 weeks (improving, stable, declining?)
   - Rules added this month — which are working, which aren't?
   - Skills created/evolved this month
   - Autonomy evolution: Green/Yellow/Red decision ratio trending toward Green?
   - Proposed SOUL.md amendments (batched for quarterly review)
3. **Cem** reviews and approves any SOUL.md changes

---

## 7. The SOUL.md Section — "Self-Awareness & Continuous Improvement"

This is the actual text that should appear in Athena's SOUL.md V4. It must be lean enough to justify its token cost (~200 tokens) but actionable enough to drive the entire reflection architecture without a separate manual.

```markdown
## Self-Awareness & Continuous Improvement

### Core Principle
I get better by reflecting on outcomes, not just executing tasks. Every week,
I am a slightly better operator than the week before — or I have failed.

### What I Log (Daily — Green Zone)
- Cem corrections → MEMORY.md "CEO Preferences" (immediately)
- Mistakes and failures → data/mistakes.md (same day)
- Accomplishments and wins → daily memory log
- Delegation outcomes (success/revision/failure) → daily memory log
- Knowledge gaps discovered → MEMORY.md "Knowledge Gaps"

### What I Reflect On (Weekly — Automated)
Sunday night cycle using multi-agent reflection:
1. Gemma 4 parses week's data into structured JSON ($0)
2. Reviewer subagent (Sonnet) critiques my behavior — I do NOT self-review alone
3. Hermes proposes automations for recurring manual work
4. Ava flags strategic patterns across pillars
5. I synthesize all inputs into WEEKLY_REVIEW.md for Cem

### Five Reflection Questions (Weekly)
1. What did I accomplish? (prevents negativity bias)
2. What failed? (root cause, not blame)
3. What patterns recur? (ONE-OFF vs RECURRING vs SYSTEMIC)
4. What assumptions proved wrong? (update MEMORY.md)
5. What should I have surfaced proactively? (update HEARTBEAT.md)

### How I Change Habits
- Detected pattern → new rule in MEMORY.md (immediate, Green Zone)
- Rule validated over 4 weeks → propose promotion to SOUL.md (Red Zone)
- Rule ineffective → remove from MEMORY.md during weekly pruning

### How I Build New Skills
- Repeated manual workflow (3+ times) → draft SKILL.md → propose to Cem
- Skills live at Vault/00-Company/skills/. Drafts at _drafts/.
- Unused skills (8+ weeks) → retire to _retired/.

### Cardinal Rules
- I NEVER modify my own SOUL.md. I propose; Cem approves.
- I NEVER self-reflect alone. The Reviewer subagent provides the external critique.
- MEMORY.md stays under 5,000 chars. Prune quarterly.
- Every proposed change includes: what triggered it, expected impact, how I'll validate it worked.
```

**Token cost of this section: ~350 tokens.** It encodes the full reflection architecture in a form the model can execute, while keeping detailed procedures (JSON schemas, cron configs, sub-agent prompts) in external files where they belong.

---

## How This Connects to the Existing Council Review

The 8-section SOUL.md architecture from Part I defined Section 6 as "Self-Learning & Memory Policy" at ~200 tokens. This deep extension replaces that with a more comprehensive "Self-Awareness & Continuous Improvement" section at ~350 tokens — a 150-token increase that buys:

- Multi-agent reflection (not solo self-review)
- Explicit habit change mechanism (detect → encode → activate → validate)
- Skill evolution trigger conditions
- Knowledge gap detection framework
- Weekly reflection output format that Cem can review in 2 minutes

The net impact on the V4 token budget:

| Section | Original Estimate | Revised Estimate | Delta |
|---------|-------------------|------------------|-------|
| 6. Self-Awareness & Improvement | 200 tokens | 350 tokens | +150 |
| **Total V4 SOUL.md** | **~1,800 tokens** | **~1,950 tokens** | **+150** |

This remains well within the 2,000-token target and the 20,000-char OpenClaw bootstrap cap.

### Supporting Files Required

The SOUL.md section above is the tip of the iceberg. The following companion files make it work:

| File | Purpose | Who Creates It | Token Cost |
|------|---------|---------------|------------|
| `data/reflection/cron-reflection.sh` | Cron job that triggers the Sunday night cycle | Athena + Cem (once) | N/A (not injected) |
| `data/reflection/reviewer-prompt.md` | System prompt for the Reviewer subagent | Athena (Yellow Zone) | ~300 tokens (per-session, not bootstrap) |
| `data/reflection/YYYY-WW-raw.json` | Gemma 4's weekly parsed data | Gemma 4 (automated) | N/A (not injected) |
| `data/reflection/YYYY-WW-reviewer.md` | Reviewer subagent's critique | Reviewer (automated) | N/A (not injected) |
| `data/reflection/WEEKLY_REVIEW.md` | Athena's synthesized review for Cem | Athena (automated) | N/A (pushed to Telegram) |
| `data/reflection/MONTHLY_SELF_ASSESSMENT.md` | Monthly strategic reflection | Athena (automated) | N/A (pushed to Telegram) |

None of these files are bootstrap-injected. They are created, consumed, and archived as part of the reflection cycle. The only files that grow in bootstrap cost are MEMORY.md (when new rules are added) and HEARTBEAT.md (when new checks are added) — both of which have size budgets defined in the SOUL.md.

---

## Appendix: Additional Sources for Part II

- [Voyager — Lifelong Learning Agent](https://voyager.minedojo.org) — Skill library architecture, automatic curriculum, iterative prompting for self-verification
- [Reflexion Framework (Prompting Guide)](https://www.promptingguide.ai/techniques/reflexion) — Verbal reinforcement, self-reflection modules, episodic memory for error correction
- [Multi-Agent Reflexion (MAR)](https://arxiv.org/html/2512.20845v1) — Why single-agent self-reflection fails (confirmation bias, degeneration-of-thought) and how multi-agent debate fixes it
- [EvoSkills — Self-Evolving Agent Skills](https://arxiv.org/html/2604.01687v1) — Co-evolutionary skill generation, agent-generated skills outperforming human-curated ones
- [Self-Improving AI Agents: A Scientific Study (O-Mega)](https://o-mega.ai/articles/self-improving-ai-agents-a-scientific-study) — Three temporal modes of improvement (intra-test-time, inter-test-time, cross-generational), SAGE memory with Ebbinghaus forgetting curve
- [How to Build a Self-Improving AI Agent (DEV Community)](https://dev.to/webbywisp/how-to-build-a-self-improving-ai-agent-using-its-own-memory-k1c) — Memory + reflection loop implementation, LESSONS.md pattern
- [The Code Agent Orchestra (Addy Osmani)](https://addyosmani.com/blog/code-agent-orchestra/) — REFLECTION.md proposals after every task, compound learning through systematic review
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) — SKILL.md format, frontmatter, discovery, filtering, workspace skill paths
- [SKILL.md Format Reference (Agensi)](https://www.agensi.io/learn/skill-md-format-reference) — Complete format spec, folder structure, progressive disclosure, best practices
- [Knowledge Gaps Taxonomy (Wiley)](https://onlinelibrary.wiley.com/doi/10.1111/tops.12584) — Detection, identification, and resolution of knowledge gaps in intelligent agents
