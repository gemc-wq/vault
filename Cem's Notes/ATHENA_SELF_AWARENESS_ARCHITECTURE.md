# Athena — Deep Self-Awareness & Continuous Improvement Architecture

**Version:** 1.0  
**Author:** Architecture Design Agent  
**Date:** 2026-07-18  
**System:** Ecell Global / Head Case Designs — Athena Master Orchestrator  
**Stack:** Claude SDK (claude-opus-4-6), OpenClaw, Telegram (STT/TTS), Gemma 4 (Ollama), Hermes (Claude Code)

---

## Table of Contents

1. [Part 1: The Reflection Engine](#part-1-the-reflection-engine)
2. [Part 2: Habit Change Mechanics](#part-2-habit-change-mechanics)
3. [Part 3: Skill Evolution Protocol](#part-3-skill-evolution-protocol)
4. [Part 4: Multi-Agent Self-Reflection Loop](#part-4-multi-agent-self-reflection-loop)
5. [Part 5: Knowledge Gap Detection & Handling](#part-5-knowledge-gap-detection--handling)
6. [Part 6: The Virtuous Loop — Full Architecture Diagram](#part-6-the-virtuous-loop--full-architecture-diagram)
7. [Part 7: The SOUL.md Section](#part-7-the-soulmd-section)
8. [Part 8: Implementation Roadmap](#part-8-implementation-roadmap)

---

## Part 1: The Reflection Engine

### 1.1 Data Sources to Scan

Athena's weekly reflection must be evidence-based, not vibes-based. Every reflection question is grounded in specific file reads. Here are the six canonical data sources and exactly what to extract from each:

#### Source 1: `mistakes.md`

**Location:** `/workspace/mistakes.md`  
**What to extract:**
- Total new entries this week (count)
- Categorise each by pillar: Creative / Sales / Operations / Marketing / Finance / Intelligence
- Categorise each by failure type: Wrong delegation, Bad assumption, Missed deadline, Wrong priority, Tool failure, Knowledge gap
- Flag any entry that mentions Cem correcting Athena (tag: `cem-correction`)
- Flag any entry that repeats a pattern from a prior week (tag: `recurring`)

**Extraction format (per entry):**
```json
{
  "date": "2026-07-14",
  "description": "Sent Ava a BQ query task — she doesn't have BQ access",
  "pillar": "Operations",
  "failure_type": "wrong_delegation",
  "cem_correction": false,
  "recurring": true,
  "recurring_ref": "2026-W27 — same issue with Harry"
}
```

#### Source 2: `TASK_SHEET.md`

**Location:** `/workspace/TASK_SHEET.md`  
**What to extract:**
- Tasks completed this week: count, on-time vs. late, average lateness (in hours)
- Tasks still open past their ETA: list with days overdue
- Tasks deferred (moved forward without completion): count and reasons
- Tasks added mid-week (unplanned work): count and source (Cem request, agent escalation, self-initiated)
- Pillar distribution of completed work vs. target allocation (Creative 30%, Sales 25%, etc.)

**Extraction format:**
```json
{
  "week": "2026-W29",
  "completed": 23,
  "on_time": 18,
  "late": 5,
  "avg_lateness_hours": 6.2,
  "overdue_open": [
    {"task": "Update PH catalogue metadata", "days_overdue": 3, "pillar": "Sales", "blocker": "waiting on licensor approval"}
  ],
  "deferred": 4,
  "unplanned": 7,
  "pillar_actual": {"Creative": 0.35, "Sales": 0.20, "Operations": 0.25, "Marketing": 0.05, "Finance": 0.10, "Intelligence": 0.05},
  "pillar_target": {"Creative": 0.30, "Sales": 0.25, "Operations": 0.20, "Marketing": 0.10, "Finance": 0.10, "Intelligence": 0.05}
}
```

#### Source 3: Session Logs (Daily Memory Files)

**Location:** `/workspace/memory/YYYY-MM-DD.md` (7 files per week)  
**What to extract:**
- Decisions made: what was decided, who was delegated to, outcome if known
- Repeated actions: same type of task appearing 3+ times across the week
- Deferred items: things Athena noted but didn't act on (search for phrases like "will handle later", "deferred", "low priority for now")
- Cem interactions: every message from Cem, especially corrections/redirections
- Time-of-day patterns: when was Athena most/least effective (based on task density and completion)
- Stuck loops: any evidence of Athena attempting the same action multiple times without resolution

#### Source 4: Cem Corrections

**Location:** Extracted from session logs and Telegram message history  
**What to extract:**
- Every instance where Cem said variations of: "no", "that's wrong", "not what I meant", "actually...", "don't do that", "I already told you", "why did you..."
- Context around the correction: what Athena proposed/did, what Cem wanted instead
- Whether the same correction has been given before

**Extraction format (per correction):**
```json
{
  "date": "2026-07-15",
  "athena_action": "Proposed sending creative brief to Harry",
  "cem_correction": "That's Sven's domain — Harry is finance only",
  "root_cause": "authority_confusion",
  "prior_occurrence": "2026-W27 — similar confusion on who handles packaging design",
  "suggested_fix": "Update DELEGATION_NOTES.md for Sven: all creative briefs, including packaging"
}
```

#### Source 5: Project Milestone Data

**Location:** `/workspace/SOUL-Athena-V3.md` or equivalent project tables  
**What to extract:**
- Projects with ETA slippage this week (% complete didn't advance as expected)
- Projects that hit milestones on time
- Projects blocked (and what's blocking them — agent, external dependency, tool, knowledge)
- Portfolio health: what percentage of active projects are green/yellow/red
- Cross-pillar dependencies that are creating bottlenecks

#### Source 6: Agent Output Quality

**Location:** Derived from session logs + TASK_SHEET.md outcomes  
**What to extract per agent (Ava, Harry, Sven, Hermes, Gemma 4):**
- Tasks delegated this week: count
- Tasks completed satisfactorily on first attempt: count
- Tasks requiring revision: count and nature of revision
- Tasks that failed/bounced back: count and reason
- Average turnaround time
- Accept rate: `(first-attempt accepted) / (total delegated)` — this is the key quality metric

**Extraction format:**
```json
{
  "agent": "Ava",
  "week": "2026-W29",
  "delegated": 8,
  "accepted_first_try": 5,
  "revised": 2,
  "failed": 1,
  "accept_rate": 0.625,
  "avg_turnaround_hours": 2.3,
  "revision_reasons": ["missing market context", "wrong format for Shopify listing"],
  "failure_reason": "task outside Ava's capability — needed BQ query"
}
```

---

### 1.2 Structured Reflection Questions

Athena runs these questions every week, answering each with specific evidence from the data sources above. No question gets a vague answer — every claim must cite a specific log entry, task, or metric.

```markdown
## Weekly Reflection Template — Week [YYYY-Wxx]

### Q1: North Star Progress
What did I accomplish this week that moved the needle on the 3 North Star metrics?
- **Coverage** (% of Cem's operational load handled autonomously):
  [Evidence: X tasks completed without Cem input, Y tasks required Cem intervention]
- **Speed** (time from task creation to completion):
  [Evidence: Average completion time this week vs. last week]
- **Intelligence** (quality of autonomous decisions — accept rate, mistake rate):
  [Evidence: X/Y delegations accepted first try, Z mistakes logged]

### Q2: Failure Audit
What failed this week, and what was my role in each failure?
- [List each failure from mistakes.md with root cause analysis]
- My contribution to each failure: [wrong assumption / wrong delegation / missed context / tool limitation]
- Which failures were preventable with information I already had?

### Q3: Delegation Calibration
Which delegation decisions were wrong this week? Which agents did I over-use or under-use?
- Agent accept rates this week: Ava [X%], Harry [X%], Sven [X%], Hermes [X%], Gemma 4 [X%]
- Delegation volume vs. target: [actual vs. expected based on pillar allocation]
- Misrouted tasks: [list tasks sent to wrong agent, with correct agent identified]
- Agents sitting idle while others are overloaded: [evidence]

### Q4: Cem Correction Analysis
What did Cem correct me on? What assumptions was I making that were wrong?
- Total corrections this week: [count]
- Correction categories: [list]
- Underlying assumption behind each correction: [what I believed that was wrong]
- Which corrections repeat patterns from prior weeks: [list with week references]
- Proposed permanent fix for each recurring correction: [specific file edit]

### Q5: Multi-Week Patterns (3+ week lookback)
What patterns am I seeing across multiple weeks?
- Recurring failures: [patterns appearing 3+ times]
- Improving trends: [metrics getting better]
- Degrading trends: [metrics getting worse]
- Seasonal or cyclical patterns: [e.g., end-of-month finance load]
- Agent capability shifts: [agents improving or degrading at specific task types]

### Q6: Knowledge Gaps
What do I not know that I need to know?
- Decisions I deferred because I lacked information: [list]
- Assumptions I made that I couldn't verify: [list]
- Data I needed but couldn't access: [list with specific system/API]
- Context I'm missing about the business: [list]
- Tools or integrations I need but don't have: [list]

### Q7: Automation Opportunities
What recurring manual work could be automated?
- Tasks I performed manually 3+ times this week: [list with frequency]
- Tasks that follow a predictable pattern: [list]
- Tasks that Hermes could script: [list with estimated effort]
- Data pipelines that should exist but don't: [list]
```

---

### 1.3 `WEEKLY_REVIEW.md` — Output Format

**Location:** `/workspace/reviews/YYYY-Wxx_REVIEW.md`  
**Retention:** All reviews kept permanently (they're the learning corpus)

```markdown
# Weekly Review — [YYYY-Wxx]
**Generated:** [timestamp]
**Review Period:** [Monday date] to [Sunday date]

---

## Executive Summary (for Cem's Telegram brief)
[3-5 bullet points. What went well, what went wrong, what's changing. Max 200 words.
This is what Cem actually reads. Everything below is the evidence.]

---

## Scorecard

| Metric | This Week | Last Week | Δ | 4-Week Avg | Target |
|--------|-----------|-----------|---|------------|--------|
| Tasks completed | | | | | |
| On-time rate | | | | | |
| Mistake count | | | | | |
| Cem corrections | | | | | |
| Delegation accept rate | | | | | |
| Autonomous decisions | | | | | |
| Coverage % | | | | | |

---

## North Star Progress
[Detailed answer to Q1 with evidence]

## Failure Audit
[Detailed answer to Q2 with evidence]

## Delegation Calibration
[Detailed answer to Q3 with evidence]

## Cem Correction Analysis
[Detailed answer to Q4 with evidence]

## Multi-Week Patterns
[Detailed answer to Q5 with evidence]

## Knowledge Gaps Identified
[Detailed answer to Q6 — each gap gets a type tag from Part 5 taxonomy]

## Automation Opportunities
[Detailed answer to Q7]

---

## Proposed Changes

### Change 1: [Short title]
- **Type:** routing_rule | escalation_threshold | delegation_note | skill_creation | soul_amendment | automation
- **Status:** PROPOSED
- **Evidence:** [Which data points drove this proposal]
- **Specific change:** [Exact file and exact edit — not vague]
- **Expected impact:** [What metric should improve and by how much]
- **Risk if wrong:** [What happens if this change makes things worse]
- **Trial period:** 2 weeks
- **Validation metric:** [How to measure if it worked]
- **Requires Cem approval:** yes | no
  - yes if: SOUL.md amendment, new escalation threshold, authority boundary change
  - no if: routing optimisation, delegation note update, skill creation

### Change 2: [...]
[repeat structure]

---

## Inputs (for audit trail)
- Gemma 4 pattern scan: /compiled/WEEKLY_PATTERNS.json
- Reviewer critique: /compiled/REVIEWER_CRITIQUE.md
- Hermes automation scan: /compiled/AUTOMATION_CANDIDATES.md
- Ava strategic scan: /compiled/STRATEGIC_GAPS.md

---

## Previous Review Follow-Up
[For each PROPOSED change from last week:]
- Change: [title]
- Status: APPROVED → ACTIVE | REJECTED (reason) | VALIDATED (result) | FAILED (what happened)
- Metric change since activation: [data]
```

---

## Part 2: Habit Change Mechanics

### 2.1 Pattern Detection via Gemma 4

Gemma 4 runs locally on Ollama at $0 cost. It's the workhorse for nightly log parsing — high volume, low stakes, cheap.

#### Nightly Cron Job: `log_parser.sh`

**Schedule:** Every night at 23:30 ET  
**Runtime:** ~5-10 minutes on local Mac Studio

```bash
#!/bin/bash
# /workspace/crons/log_parser.sh
# Runs Gemma 4 via Ollama to parse today's session log

DATE=$(date +%Y-%m-%d)
WEEK=$(date +%Y-W%V)
LOG_FILE="/workspace/memory/${DATE}.md"
MISTAKES_FILE="/workspace/mistakes.md"
TASK_SHEET="/workspace/TASK_SHEET.md"
OUTPUT_DIR="/workspace/compiled/daily"
OUTPUT_FILE="${OUTPUT_DIR}/${DATE}_patterns.json"

mkdir -p "$OUTPUT_DIR"

# Build the prompt with today's data
PROMPT=$(cat <<'EOF'
You are a pattern extraction engine. Read the following daily session log, mistakes file, and task sheet.
Extract structured patterns in JSON format.

For each pattern you find, output:
{
  "patterns": [
    {
      "id": "[DATE]-[sequential number]",
      "pattern": "[plain English description of what happened]",
      "category": "delegation_error | repeated_task | cem_correction | missed_deadline | tool_failure | knowledge_gap | agent_quality | priority_misalignment | process_inefficiency",
      "pillar": "Creative | Sales | Operations | Marketing | Finance | Intelligence",
      "severity": "low | medium | high | critical",
      "agents_involved": ["agent names"],
      "frequency_today": [number of times this pattern appeared today],
      "evidence": "[exact quote or reference from the log]",
      "suggested_action": "[one-line suggestion]"
    }
  ],
  "metrics": {
    "tasks_completed": [number],
    "tasks_delegated": [number],
    "cem_interactions": [number],
    "cem_corrections": [number],
    "decisions_made": [number],
    "deferrals": [number]
  },
  "cem_corrections_detail": [
    {
      "context": "[what Athena did]",
      "correction": "[what Cem said]",
      "implied_rule": "[what Athena should learn from this]"
    }
  ]
}

Rules:
- Only extract patterns you can directly evidence from the logs. No speculation.
- A "repeated_task" is something that looks structurally similar to something done in the past 7 days.
- severity: critical = Cem correction or missed deadline on high-priority item. high = wrong delegation or agent failure. medium = process inefficiency. low = minor observation.
- If you see NO patterns, output {"patterns": [], "metrics": {...}, "cem_corrections_detail": []}

EOF
)

# Combine the data files and send to Gemma 4
{
  echo "=== SESSION LOG (${DATE}) ==="
  cat "$LOG_FILE" 2>/dev/null || echo "[no session log for today]"
  echo ""
  echo "=== MISTAKES.MD (last 20 entries) ==="
  tail -100 "$MISTAKES_FILE" 2>/dev/null || echo "[no mistakes file]"
  echo ""
  echo "=== TASK_SHEET.MD (active tasks) ==="
  grep -A2 "status: active\|status: overdue\|status: completed" "$TASK_SHEET" 2>/dev/null | head -100 || echo "[no task sheet]"
} | ollama run gemma3:latest "$PROMPT" > "$OUTPUT_FILE"

echo "[$(date)] Pattern extraction complete: $OUTPUT_FILE"
```

#### Weekly Aggregation: `weekly_aggregator.sh`

**Schedule:** Saturday 23:00 ET  
**Purpose:** Combines 7 daily pattern files into `WEEKLY_PATTERNS.json`

```bash
#!/bin/bash
# /workspace/crons/weekly_aggregator.sh

WEEK=$(date +%Y-W%V)
OUTPUT="/workspace/compiled/WEEKLY_PATTERNS.json"
DAILY_DIR="/workspace/compiled/daily"

# Collect all daily patterns from this week
PROMPT=$(cat <<'EOF'
You are a pattern aggregation engine. You will receive 7 daily pattern extraction files.

Your job:
1. MERGE patterns that describe the same underlying issue across multiple days
2. COUNT how many days each pattern appeared (frequency)
3. ESCALATE any pattern with frequency >= 3
4. IDENTIFY trends: patterns that are new this week vs. recurring from prior weeks
5. RANK by severity × frequency

Output format:
{
  "week": "[WEEK]",
  "generated": "[timestamp]",
  "escalated_patterns": [
    {
      "pattern": "[description]",
      "frequency": [number of days it appeared],
      "category": "[category]",
      "pillar": "[pillar]",
      "severity": "[severity]",
      "first_seen": "[date]",
      "evidence_summary": "[combined evidence across days]",
      "suggested_action": "[refined suggestion based on full week's context]",
      "escalation_reason": "frequency >= 3 | severity critical | cem_correction_repeated"
    }
  ],
  "all_patterns": [...all patterns, including non-escalated],
  "weekly_metrics": {
    "total_tasks_completed": [sum],
    "total_cem_corrections": [sum],
    "total_delegation_errors": [sum],
    "busiest_day": "[day]",
    "quietest_day": "[day]",
    "pillar_distribution": {"Creative": X, "Sales": Y, ...}
  },
  "cem_corrections_all": [...all corrections from the week],
  "cross_week_recurrences": [
    {
      "pattern": "[description]",
      "weeks_seen": ["2026-W27", "2026-W28", "2026-W29"],
      "total_frequency": [sum across weeks],
      "escalation": "URGENT — this has persisted 3+ weeks"
    }
  ]
}

For cross_week_recurrences, also read the previous 3 weekly pattern files if they exist.
EOF
)

# Feed all daily files plus prior weekly files
{
  for f in "$DAILY_DIR"/*.json; do
    echo "=== $(basename "$f") ==="
    cat "$f"
    echo ""
  done
  echo "=== PRIOR WEEKS ==="
  for f in /workspace/compiled/archive/WEEKLY_PATTERNS_*.json; do
    echo "=== $(basename "$f") ==="
    cat "$f" 2>/dev/null
    echo ""
  done | tail -3000  # limit context window for Gemma 4
} | ollama run gemma3:latest "$PROMPT" > "$OUTPUT"

# Archive this week's daily files
mkdir -p "$DAILY_DIR/archive"
mv "$DAILY_DIR"/*_patterns.json "$DAILY_DIR/archive/" 2>/dev/null

# Archive this week's aggregated file
cp "$OUTPUT" "/workspace/compiled/archive/WEEKLY_PATTERNS_${WEEK}.json"

echo "[$(date)] Weekly aggregation complete: $OUTPUT"
```

#### `PATTERN_SUMMARY.json` Format (canonical)

```json
{
  "week": "2026-W29",
  "generated": "2026-07-18T23:15:00-04:00",
  "escalated_patterns": [
    {
      "pattern": "Ava re-queued 3x on listing tasks due to missing product specs",
      "frequency": 4,
      "category": "agent_quality",
      "pillar": "Sales",
      "severity": "medium",
      "first_seen": "2026-07-14",
      "evidence_summary": "July 14: Ava asked for specs twice on SKU-4421. July 15: same on SKU-4455. July 16: Athena pre-fetched specs, task completed first try. July 17: forgot to pre-fetch, loop repeated.",
      "suggested_action": "Add pre-flight check to all listing tasks: verify product specs exist in BQ before delegating to Ava",
      "escalation_reason": "frequency >= 3"
    }
  ],
  "all_patterns": [],
  "weekly_metrics": {
    "total_tasks_completed": 23,
    "total_cem_corrections": 2,
    "total_delegation_errors": 3,
    "busiest_day": "Tuesday",
    "quietest_day": "Sunday",
    "pillar_distribution": {
      "Creative": 8,
      "Sales": 5,
      "Operations": 5,
      "Marketing": 2,
      "Finance": 2,
      "Intelligence": 1
    }
  },
  "cem_corrections_all": [
    {
      "date": "2026-07-15",
      "context": "Athena proposed bulk-updating all Amazon listings",
      "correction": "Don't touch Amazon listings without checking suppression risk first",
      "implied_rule": "Amazon listing changes require suppression risk check before execution"
    }
  ],
  "cross_week_recurrences": []
}
```

### 2.2 Escalation Threshold

A pattern escalates from Gemma 4's nightly parsing to Athena's Weekly Reviewer when ANY of these conditions are met:

| Condition | Threshold | Rationale |
|-----------|-----------|-----------|
| Frequency | Same pattern 3+ times in 2 weeks | Not a one-off — it's structural |
| Severity | Any `critical` pattern once | Cem correction or missed deadline = immediate attention |
| Recurrence | Pattern appeared in 3+ weekly reviews | Persistent issue not being fixed |
| Agent failure | Same agent fails at same task type 2+ times | Delegation rule needs updating |
| Cem correction repeat | Same correction given twice | Athena isn't learning from feedback |

### 2.3 Rule Encoding — Where Habit Changes Live

Each type of habit change maps to a specific file. This prevents one mega-file from becoming unmanageable and ensures each file has a clear owner and update cadence.

#### File 1: `ROUTING_RULES.md`

**Location:** `/workspace/config/ROUTING_RULES.md`  
**Purpose:** Overrides and refinements to default agent-task routing  
**Loaded by:** Athena on every heartbeat (30-min cycle) via reference in AGENTS.md  
**Update authority:** Athena (auto) for routing optimisations; Cem for authority boundary changes

```markdown
# Routing Rules
Last updated: [timestamp]

## Active Rules

### RULE-001 [STABLE since 2026-W25]
- **Trigger:** Task involves Amazon listing edits
- **Pre-flight:** Run suppression risk check via BQ query before any edit
- **Route to:** Ava (if low risk) | Escalate to Cem (if medium/high risk)
- **Origin:** Cem correction 2026-07-15
- **Validation:** 0 suppression incidents since activation

### RULE-002 [TRIAL since 2026-W29, expires 2026-W31]
- **Trigger:** Listing task delegated to Ava
- **Pre-flight:** Verify product specs exist in catalogue before delegation
- **Route to:** If specs missing → fetch specs first, then delegate
- **Origin:** Pattern escalation — Ava re-queued 4x in W29
- **Validation metric:** Ava listing task accept rate (target: >80%, was 62.5%)

## Expired/Retired Rules
### RULE-000 [RETIRED 2026-W24]
- **Was:** Route all finance queries to Harry via email
- **Retired because:** Harry now accepts direct OpenClaw messages
```

#### File 2: `ESCALATION_CALIBRATION.md`

**Location:** `/workspace/config/ESCALATION_CALIBRATION.md`  
**Purpose:** Defines when Athena should escalate to Cem vs. handle autonomously  
**Update cadence:** After each Cem validation (Cem says "you should/shouldn't have asked me")

```markdown
# Escalation Calibration
Last updated: [timestamp]

## Escalate to Cem (ALWAYS)
- Spend over $500 in a single action
- New licensor relationship decisions
- Hiring/firing/contractor decisions
- Changes to SOUL.md
- Public-facing communications (press, social media official accounts)
- Legal/compliance decisions

## Handle Autonomously (Cem trusts Athena)
- Routine listing updates (< 50 SKUs)
- Creative brief routing to Sven
- Standard financial reports from Harry
- Inventory reorder within pre-approved parameters
- Daily operational decisions within established SOPs

## Grey Zone (use judgement, log decision, review weekly)
- [Items move here when Cem gives mixed signals]
- New marketplace listings (escalated until W30, then review)

## Calibration Log
| Date | Decision | Athena's Call | Cem's Feedback | Adjustment |
|------|----------|---------------|----------------|------------|
| 2026-07-15 | Bulk Amazon update | Proceeded autonomously | "Should have checked with me" | Moved to ESCALATE |
```

#### File 3: `DELEGATION_NOTES.md` (Per Agent)

**Location:** `/workspace/03-Agents/[AgentName]/DELEGATION_NOTES.md`  
**Purpose:** Agent-specific routing intelligence, accumulated over time  
**Update authority:** Athena (auto) after each delegation outcome

```markdown
# Delegation Notes — Ava (CPO/Strategy)

## Strengths (validated by accept rate > 80%)
- Product listing creation and optimisation
- Market research and competitor analysis
- Shopify catalogue management
- Strategic planning documents

## Weaknesses (validated by accept rate < 60%)
- Direct BQ/SQL queries (no access) — route to Harry or Hermes
- Creative asset generation — route to Sven
- Financial modelling — route to Harry

## Preferences
- Performs best with: clear brief, product specs pre-attached, target marketplace specified
- Struggles when: given vague "figure it out" tasks without context
- Turnaround: typically 1-3 hours for standard tasks

## Recent Observations
- [2026-W29] Accept rate dropped to 62.5% — traced to missing product specs on delegation
- [2026-W28] Excellent on Shopify migration tasks — 100% first-attempt accept rate

## Standing Rules
- ALWAYS attach product specs when delegating listing tasks
- NEVER delegate BQ queries — Ava will attempt and fail
- For mixed creative/strategy tasks: Ava leads strategy, Sven handles creative assets
```

#### File 4: `SOUL.md` Amendments

**Purpose:** Permanent behavioural changes that define who Athena *is*  
**Update authority:** Cem approval REQUIRED — no exceptions  
**Process:**

1. Athena proposes amendment in WEEKLY_REVIEW.md with status `PROPOSED`
2. Amendment includes: exact text to add/change, rationale, evidence
3. Cem reviews in Monday morning brief
4. If approved: Athena applies the edit, logs in SOUL.md changelog
5. If rejected: Athena logs rejection reason, does not re-propose for 4 weeks unless new evidence

```markdown
## Proposed SOUL.md Amendment — 2026-W29

### Current text (lines 45-47):
> Athena delegates creative tasks to the most available agent.

### Proposed text:
> Athena delegates creative tasks exclusively to Sven. Mixed creative/strategy 
> tasks are split: Ava handles strategy components, Sven handles all visual/design 
> components. No creative asset generation is delegated to Ava or Harry.

### Evidence:
- 3 instances in W27-W29 of creative tasks misrouted to Ava (mistakes.md entries #44, #47, #52)
- Cem correction on 2026-07-08: "Sven does all creative, period"
- Sven accept rate on creative: 94%. Ava accept rate on creative: 31%.

### Status: PROPOSED → [awaiting Cem approval]
```

### 2.4 The Complete Habit Change Flow

```
Step 1: DETECT
├── Gemma 4 nightly log parser → daily pattern JSON
├── Gemma 4 Saturday aggregator → WEEKLY_PATTERNS.json
└── Escalation check: frequency ≥ 3 OR severity = critical OR cross-week recurrence

Step 2: ANALYSE
├── Reviewer subagent (Sunday 00:00) reads patterns + mistakes + tasks
├── Produces structured critique with specific rule change proposals
└── Each proposal identifies: target file, exact edit, expected metric improvement

Step 3: EVALUATE
├── Athena reads Reviewer's proposals
├── For each proposal, Athena checks:
│   ├── Is this within my authority? (no SOUL.md changes without Cem)
│   ├── Does the evidence support this change? (minimum 3 data points)
│   ├── What's the risk if this change is wrong? (reversibility assessment)
│   └── Is there a simpler fix? (avoid over-engineering)
├── Auto-approve: routing rules, delegation notes, skill creation
└── Escalate to Cem: SOUL.md amendments, escalation threshold changes, authority boundaries

Step 4: ACTIVATE
├── Apply approved changes to target files
├── Tag each change with:
│   ├── status: TRIAL
│   ├── activated: [date]
│   ├── trial_expires: [date + 2 weeks]
│   └── validation_metric: [specific measurable outcome]
└── Notify Cem of activated changes in Monday brief

Step 5: VALIDATE (runs automatically during 2-week trial)
├── Gemma 4 tracks whether the target pattern recurs
├── Athena checks validation metric at trial midpoint (1 week) and endpoint (2 weeks)
├── Outcomes:
│   ├── IMPROVED (metric improved ≥ 20%): change becomes STABLE, trial tag removed
│   ├── NO CHANGE (metric within ±10%): extend trial 2 more weeks with modified approach
│   ├── DEGRADED (metric worsened ≥ 10%): REVERT change, log failure, try different approach
│   └── INCONCLUSIVE (insufficient data): extend trial 2 weeks
└── All outcomes logged in the change's file entry

Step 6: STABILISE or ITERATE
├── STABLE changes: remove trial metadata, add validation evidence
├── FAILED changes: revert file edit, add to "approaches_tried" list for that pattern
├── After 3 failed approaches: escalate to Cem as "I can't solve this — need your input"
└── Successfully stabilised changes feed into Athena's "proven playbook"
```

---

## Part 3: Skill Evolution Protocol

### 3.1 Skill Creation Triggers

Athena monitors for these four trigger conditions continuously. Gemma 4 assists with frequency counting on triggers 1 and 2.

#### Trigger 1: Repeated Manual Process

**Detection:** Gemma 4 flags any multi-step process that appears 3+ times in a 7-day window in session logs.

**Signal pattern in logs:**
```
[session log contains 3+ entries matching]:
- Same sequence of 2+ actions (e.g., "query BQ → format result → send to Ava")
- Same task type with same pre-conditions
- Athena performing steps that could be codified as a checklist
```

**Example:** Athena manually checks inventory levels in BQ, compares to reorder threshold, drafts reorder request, sends to operations. Done 4 times this week. → Skill candidate: `inventory-reorder-check`

#### Trigger 2: Sub-Agent Consistent Failure

**Detection:** Agent accept rate < 50% on a specific task category over 2+ weeks.

**Signal:** DELEGATION_NOTES.md shows a task type in an agent's "Weaknesses" section AND that task type keeps being delegated to them.

**Response:** Either route task to correct agent (routing rule) OR create a skill that includes the correct pre-processing Athena needs to do before delegating.

**Example:** Ava fails at listing tasks when specs are missing → New skill: `listing-prep` that codifies the spec-gathering pre-flight.

#### Trigger 3: New Tool/API Connected

**Detection:** Hermes reports a new integration, or Cem mentions a new tool in session.

**Response:** Create a skill that documents: what the tool does, how to call it, when to use it, common patterns, error handling.

**Example:** New TikTok Shop API connected → Skill: `tiktok-shop-management` with listing creation, order sync, and analytics workflows.

#### Trigger 4: Knowledge Gap → Reference Skill

**Detection:** Athena identifies a recurring knowledge gap (same type of question she can't answer, or same context she lacks).

**Response:** Create a reference skill — a structured knowledge document that Athena loads when she's in that domain.

**Example:** Athena repeatedly unsure about licensor approval timelines → Skill: `licensor-reference` with approval SLAs, contact info, escalation paths per licensor.

### 3.2 Skill Template

Every skill Athena creates follows this exact template. No exceptions — consistency enables automated lifecycle management.

```markdown
---
name: [kebab-case-name]
description: [One line — what it does and when Athena should load it]
version: 1.0
created: [YYYY-MM-DD]
created_by: athena-self
origin: repeated_manual | agent_failure | new_tool | knowledge_gap
origin_evidence: [Reference to the trigger — e.g., "W29 review, pattern P-029-003"]
status: experimental
uses: 0
successes: 0
failures: 0
last_used: null
triggers:
  - "[condition 1 that should cause Athena to auto-load this skill]"
  - "[condition 2]"
retirement_condition: "[When this skill should be reviewed for deprecation]"
---

# [Skill Name]

## Purpose
[2-3 sentences: What problem does this skill solve? What was happening before 
this skill existed that was suboptimal?]

## When to Use
[Bullet list of specific conditions/triggers. Be precise enough that Athena 
can pattern-match against incoming tasks.]
- When [specific condition 1]
- When [specific condition 2]
- NOT when [exclusion condition — prevent misuse]

## Pre-Conditions
[What must be true before this skill can execute?]
- [ ] [Condition 1 — e.g., "BQ access is available"]
- [ ] [Condition 2 — e.g., "Product SKU is known"]

## Step-by-Step

### Step 1: [Action name]
**Action:** [Exactly what to do]
**Tool/Agent:** [Which tool or agent to use]
**Expected output:** [What good looks like]
**If failed:** [What to do if this step fails]

### Step 2: [Action name]
[...]

### Step N: [Final action]
[...]

## Verification
[How to confirm the skill executed correctly]
- [ ] [Check 1 — e.g., "Listing appears on Shopify within 2 hours"]
- [ ] [Check 2 — e.g., "No error in agent response"]
- [ ] [Check 3 — e.g., "Cem not notified of issue (autonomous success)"]

## Known Limitations
- [Limitation 1 — e.g., "Does not handle bundles, only single SKUs"]
- [Limitation 2 — e.g., "Requires BQ to be responsive; during outages, defer task"]

## Changelog
| Version | Date | Change | Reason |
|---------|------|--------|--------|
| 1.0 | [date] | Initial creation | [origin_evidence] |

## Retirement Condition
[Specific, measurable condition that triggers deprecation review:]
- Not used in 60 days
- Underlying tool/API deprecated
- Accept rate < 50% after 10+ uses
- Better approach identified and validated
```

### 3.3 Skill Testing Protocol

```
LIFECYCLE: creation → experimental → stable → (deprecated → archived)

EXPERIMENTAL PHASE (first 5 uses):
├── Every use is logged:
│   ├── Date and context
│   ├── Outcome: success | partial_success | failure
│   ├── Time taken vs. estimated time
│   ├── Quality: accepted_first_try | revised | rejected
│   └── Notes: what went wrong, what could improve
├── After each use, update YAML frontmatter:
│   ├── uses: [increment]
│   ├── successes: [increment if success]
│   ├── failures: [increment if failure]
│   └── last_used: [date]
├── PROMOTION to stable requires:
│   ├── uses >= 3
│   ├── success_rate >= 80% (i.e., at least 3 of first 5 succeed)
│   └── No critical failures (defined as: Cem had to intervene)
├── DEMOTION to deprecated triggers:
│   ├── 2 failures in first 5 uses
│   ├── OR any critical failure
│   └── OR Cem says "stop using this approach"
└── During experimental: Athena adds a mental note to pay extra attention 
    to outcomes and logs more detail than usual

STABLE PHASE (ongoing):
├── Normal use, normal logging (less verbose)
├── Quarterly review: is this skill still relevant?
├── Continuous metrics: uses, success_rate, avg_time
├── Degradation detection:
│   ├── If success_rate drops below 60% over any 10-use window → flag for review
│   └── If not used in 60 days → flag for retirement review
└── Version updates: Athena can update steps, add known limitations, refine triggers

DEPRECATED PHASE:
├── Triggered by: retirement condition met, or manual deprecation
├── Skill is NOT deleted — moved to /skills/archive/
├── Deprecation notice added to frontmatter: status: deprecated, deprecated_date, deprecated_reason
├── Athena stops auto-loading this skill
├── Fallback: revert to manual process for the task type
└── Review: was this skill's purpose absorbed by a better skill? Log the replacement.
```

### 3.4 Skill Index File

Athena maintains `/workspace/skills/SKILL_INDEX.md` — a registry of all skills with current status, enabling fast lookup without reading every skill file.

```markdown
# Skill Index
Last updated: [timestamp]
Auto-generated by Athena after each skill lifecycle event.

## Active Skills

| Name | Status | Uses | Success Rate | Last Used | Pillar | Origin |
|------|--------|------|-------------|-----------|--------|--------|
| inventory-reorder-check | stable | 14 | 92.8% | 2026-07-17 | Operations | repeated_manual |
| listing-prep | experimental | 2 | 100% | 2026-07-16 | Sales | agent_failure |
| licensor-reference | stable | 8 | 87.5% | 2026-07-18 | Intelligence | knowledge_gap |

## Deprecated Skills

| Name | Deprecated | Reason | Replacement |
|------|-----------|--------|-------------|
| old-inventory-check | 2026-W24 | Replaced by inventory-reorder-check | inventory-reorder-check |

## Pending Creation (from latest review)

| Proposed Name | Trigger | Evidence | Priority |
|--------------|---------|----------|----------|
| tiktok-shop-management | new_tool | TikTok API connected W28 | high |
```

---

## Part 4: Multi-Agent Self-Reflection Loop

### 4.1 The Cast and Their Roles

| Agent | Model | Cost | Role in Reflection | Why This Agent |
|-------|-------|------|-------------------|----------------|
| **Gemma 4** | Ollama local | $0 | Log parsing, pattern extraction, frequency counting | High-volume grunt work, runs nightly, no API cost |
| **Reviewer** | Claude Sonnet (subagent) | ~$0.02/week | Structured critique, identifies root causes, proposes rule changes | Needs reasoning ability but not full Opus, disposable subagent |
| **Hermes** | Claude Code | ~$0.05/week | Scans codebase/crons for automation opportunities | Has code context, understands what's scriptable |
| **Ava** | OpenClaw (Mac Studio) | ~$0.03/week | Strategic pattern review, portfolio health, pillar balance | Has business strategy context, sees cross-project patterns |
| **Athena** | Claude Opus 4 | ~$0.10/week | Synthesises all inputs, produces WEEKLY_REVIEW.md, proposes changes to Cem | Full reasoning power for synthesis and judgement calls |

**Total weekly cost of self-improvement cycle: ~$0.20**

### 4.2 The Weekly Cycle — Precise Timing

```
SATURDAY
├── 23:00 ET — Gemma 4: Weekly pattern aggregation
│   ├── Input: 7 daily pattern JSONs + 3 prior weekly patterns
│   ├── Output: /compiled/WEEKLY_PATTERNS.json
│   └── Duration: ~10 minutes
│
SUNDAY
├── 00:00 ET — Reviewer subagent: Structured critique
│   ├── Input: WEEKLY_PATTERNS.json + mistakes.md + TASK_SHEET.md + last 3 WEEKLY_REVIEW.md files
│   ├── Output: /compiled/REVIEWER_CRITIQUE.md
│   └── Duration: ~3 minutes (single Claude Sonnet call)
│
├── 01:00 ET — Hermes: Automation scan
│   ├── Input: Session logs (week) + cron job list + recent CLI history
│   ├── Output: /compiled/AUTOMATION_CANDIDATES.md
│   └── Duration: ~5 minutes
│
├── 02:00 ET — Ava: Strategic scan
│   ├── Input: SOUL-Athena-V3 project tables + TASK_SHEET.md + pillar metrics
│   ├── Output: /compiled/STRATEGIC_GAPS.md
│   └── Duration: ~5 minutes
│
├── 06:00 ET — Athena: Synthesis
│   ├── Input: All four compiled files + raw data sources
│   ├── Output: /reviews/YYYY-Wxx_REVIEW.md
│   ├── Action: Sends executive summary to Cem via Telegram
│   └── Duration: ~10 minutes
│
MONDAY
├── 09:00 ET (or whenever Cem reviews)
│   ├── Cem approves/rejects proposed changes
│   ├── Athena applies approved changes
│   ├── New rules activated with TRIAL status
│   └── New skills deployed with EXPERIMENTAL status
│
MONDAY-FRIDAY
├── Ongoing: Gemma 4 nightly parsing continues
├── Ongoing: Trial rules are monitored
├── Ongoing: Experimental skills are tracked
└── Ongoing: Data accumulates for next cycle
```

### 4.3 Exact Prompts

#### Prompt 1: Gemma 4 Log Parser (Nightly)

```
SYSTEM: You are a log analysis engine for Athena, an AI orchestration agent. 
Your job is precise pattern extraction — nothing creative, nothing speculative. 
Extract only what the data shows.

INPUT: You will receive:
1. Today's session log (Athena's daily activity)
2. Recent entries from mistakes.md
3. Current TASK_SHEET.md snapshot

TASK: Extract structured patterns in the following JSON format:

{
  "date": "[today's date]",
  "patterns": [
    {
      "id": "[date]-[seq]",
      "pattern": "[factual description of what happened]",
      "category": "[one of: delegation_error, repeated_task, cem_correction, 
                   missed_deadline, tool_failure, knowledge_gap, agent_quality, 
                   priority_misalignment, process_inefficiency]",
      "pillar": "[Creative|Sales|Operations|Marketing|Finance|Intelligence]",
      "severity": "[low|medium|high|critical]",
      "agents_involved": ["list"],
      "frequency_today": [count],
      "evidence": "[exact quote from log]",
      "suggested_action": "[one concrete action]"
    }
  ],
  "metrics": {
    "tasks_completed": [int],
    "tasks_delegated": [int],  
    "cem_interactions": [int],
    "cem_corrections": [int],
    "decisions_made_autonomously": [int],
    "deferrals": [int]
  },
  "cem_corrections_detail": [
    {
      "timestamp": "[time]",
      "context": "[what Athena did or proposed]",
      "correction": "[Cem's exact words or close paraphrase]",
      "implied_rule": "[what behaviour should change]"
    }
  ],
  "repeated_sequences": [
    {
      "sequence": "[description of the multi-step process]",
      "times_today": [count],
      "candidate_for_skill": [true|false]
    }
  ]
}

RULES:
- Only output patterns you can directly evidence from the logs
- severity: critical = Cem had to fix something or a deadline was missed on a 
  high-priority item. high = wrong delegation or output rejected. medium = 
  inefficiency. low = observation.
- For repeated_sequences: flag any 2+ step process that appeared 2+ times TODAY
- If the log is empty or minimal, output minimal JSON with zero counts
- Do NOT hallucinate patterns. If nothing noteworthy happened, say so.
```

#### Prompt 2: Reviewer Subagent System Prompt

```
SYSTEM: You are Athena's Weekly Reviewer — a critical analysis subagent. Your job 
is to provide honest, structured critique of Athena's performance this week. You 
are NOT Athena. You are an independent reviewer who sees Athena's blind spots.

You will receive:
1. WEEKLY_PATTERNS.json — aggregated patterns from Gemma 4's nightly scans
2. mistakes.md — Athena's logged failures
3. TASK_SHEET.md — task completion data
4. Last 3 WEEKLY_REVIEW.md files — to check if past proposed changes were effective

YOUR MANDATE:
- Be specific. Cite exact dates, tasks, and metrics. No vague observations.
- Be honest. If Athena is making the same mistake repeatedly, say so directly.
- Be constructive. Every criticism must come with a specific, implementable fix.
- Be calibrated. Distinguish between one-off errors and systemic issues.
- Challenge Athena's assumptions. If she's been doing something a certain way and 
  it's not working, propose an alternative.

OUTPUT FORMAT — /compiled/REVIEWER_CRITIQUE.md:

# Weekly Reviewer Critique — [Week]

## Performance Grade: [A/B/C/D/F]
[One paragraph justification. Grade is relative to last week. Include both 
objective metrics and qualitative assessment.]

## Critical Issues (must address this week)
[Issues where inaction will cause harm]

### Issue 1: [title]
- **What happened:** [specific events with dates]
- **Root cause:** [Athena's analysis may be wrong — provide YOUR root cause analysis]
- **Impact:** [what was the cost — time, quality, Cem trust]
- **Proposed fix:** [specific file + specific edit + expected outcome]
- **Applies to file:** [exact file path]

## Delegation Audit

### Agent Performance Summary
| Agent | Tasks | Accept Rate | Trend (4wk) | Assessment |
|-------|-------|-------------|-------------|------------|
| Ava   |       |             |             |            |
| Harry |       |             |             |            |
| Sven  |       |             |             |            |
| Hermes|       |             |             |            |
| Gemma |       |             |             |            |

### Misrouted Tasks
[List every task that went to the wrong agent, with correct routing]

### Underutilised Agents
[Agents who could have taken more work but weren't asked]

## Pattern Analysis

### Recurring Patterns (3+ weeks)
[These are the most important — they indicate structural issues]

### New Patterns This Week
[First-time patterns to watch]

### Resolved Patterns
[Patterns from prior weeks that no longer appear — what fixed them?]

## Cem Correction Analysis
[Every correction from Cem this week, with deeper analysis than Athena's own 
assessment. What is Cem's unspoken expectation?]

## Proposed Rule Changes (prioritised)

### Priority 1: [change title]
- **Target file:** [exact path]
- **Current state:** [what the file says now]
- **Proposed state:** [exact text to replace it with]
- **Evidence strength:** [strong/medium/weak — based on data points]
- **Requires Cem approval:** [yes/no]

### Priority 2: [...]

## Questions for Athena
[Things the Reviewer noticed but can't resolve alone — needs Athena's context]

## Grade Trend
| Week | Grade | Key Factor |
|------|-------|------------|
| W27  |       |            |
| W28  |       |            |
| W29  |       |            |
```

#### Prompt 3: Hermes Automation Scan

```
SYSTEM: You are Hermes, Athena's coding agent. You're being asked to scan for 
automation opportunities. Your expertise is: what manual processes could be 
replaced by scripts, cron jobs, or API integrations?

You will receive:
1. This week's session logs (daily memory files)
2. Current cron job list (/workspace/crons/)
3. Recent CLI history (what commands Athena/agents ran manually)
4. TASK_SHEET.md (to see recurring task types)

YOUR TASK: Identify manual work that should be automated. For each candidate:

OUTPUT FORMAT — /compiled/AUTOMATION_CANDIDATES.md:

# Automation Candidates — [Week]

## High Priority (would save 2+ hours/week)

### AUTO-001: [descriptive name]
- **Current manual process:** [step-by-step of what happens now]
- **Frequency:** [X times per week/day]
- **Time per occurrence:** [estimated minutes]
- **Total weekly time:** [frequency × time]
- **Proposed automation:**
  - **Type:** cron_job | script | api_integration | webhook | skill
  - **Implementation:** [technical description — what language, what API calls, 
    what schedule]
  - **Estimated build time:** [hours for Hermes to implement]
  - **Dependencies:** [what tools/APIs/access needed]
  - **Risk:** [what could go wrong]
- **Files to create/modify:** [list]
- **Expected time savings:** [hours/week after automation]

## Medium Priority (would save 30min-2hr/week)

### AUTO-002: [...]

## Low Priority (nice to have, < 30min/week savings)

### AUTO-003: [...]

## Already Automated (validation check)
[List current crons/automations and confirm they're still running correctly.
Flag any that are broken, outdated, or redundant.]

## NOT Worth Automating (and why)
[Tasks that look repetitive but shouldn't be automated — e.g., tasks requiring 
Cem's judgement, one-off spikes, tasks that are already fast enough manually]
```

#### Prompt 4: Ava Strategic Scan

```
SYSTEM: You are Ava, Athena's CPO/Strategy agent. You're being asked to provide 
a weekly strategic assessment. Your perspective is: are we working on the right 
things? Are the 6 pillars balanced? Are projects healthy?

You will receive:
1. SOUL-Athena-V3 project tables (all active projects with % complete, ETA, status)
2. TASK_SHEET.md (this week's task distribution)
3. WEEKLY_PATTERNS.json (this week's operational patterns)

YOUR TASK: Provide strategic analysis that Athena may not see from inside the 
day-to-day operations.

OUTPUT FORMAT — /compiled/STRATEGIC_GAPS.md:

# Strategic Gaps Analysis — [Week]

## Portfolio Health

### By Pillar
| Pillar | Target % | Actual % | Active Projects | On Track | At Risk | Blocked |
|--------|----------|----------|-----------------|----------|---------|---------|
| Creative (30%) | | | | | | |
| Sales (25%) | | | | | | |
| Operations (20%) | | | | | | |
| Marketing (10%) | | | | | | |
| Finance (10%) | | | | | | |
| Intelligence (5%) | | | | | | |

### Pillar Imbalance Alert
[Flag any pillar where actual allocation deviates >10% from target. 
Is this intentional (seasonal) or drift?]

## Project Status

### At Risk Projects (need attention)
| Project | Pillar | % Complete | ETA | Days Slipped | Blocker |
|---------|--------|------------|-----|-------------|---------|
| | | | | | |

### Blocked Projects (need unblocking)
[For each: what's blocking it, who can unblock it, proposed action]

### Consistently Slipping (3+ weeks of missed milestones)
[These are the most important — they indicate systemic issues, not one-off delays]

## Cross-Pillar Dependencies
[Projects that depend on deliverables from another pillar. 
Are these dependencies creating bottlenecks?]

## Strategic Blind Spots
[What SHOULD we be working on that we're NOT? Based on:
- Market trends (from recent research)
- Licensor deadlines
- Seasonal planning (Q4 prep, etc.)
- Competitive moves]

## Resource Allocation Recommendations
[Should any agent get more/fewer tasks? Should any pillar get more/less attention?
Back with data.]

## 30-Day Outlook
[Based on current trajectory, what will the portfolio look like in 30 days?
Which projects will complete? Which will still be blocked? What new work is coming?]
```

#### Prompt 5: Athena Synthesis

```
SYSTEM: You are Athena, synthesising your weekly self-improvement cycle. You have 
received inputs from 4 sources. Your job is to produce WEEKLY_REVIEW.md — the 
single document that captures your self-assessment, proposes changes, and goes 
to Cem.

INPUTS:
1. /compiled/WEEKLY_PATTERNS.json — Gemma 4's pattern aggregation
2. /compiled/REVIEWER_CRITIQUE.md — Your Reviewer's independent assessment
3. /compiled/AUTOMATION_CANDIDATES.md — Hermes' automation opportunities
4. /compiled/STRATEGIC_GAPS.md — Ava's strategic analysis

ALSO READ (directly, for verification):
- /workspace/mistakes.md
- /workspace/TASK_SHEET.md
- /workspace/memory/ (this week's daily logs)
- Last 3 /reviews/YYYY-Wxx_REVIEW.md files (for trend tracking)

SYNTHESIS RULES:

1. EXECUTIVE SUMMARY FIRST: Cem reads this on Telegram Sunday morning. 
   Max 5 bullets, max 200 words. Lead with the most important thing.
   Format: "[metric change] because [root cause] → [proposed action]"

2. SCORECARD: Fill every cell with real numbers. If a metric can't be calculated, 
   write "N/A — [reason]" not a guess.

3. DISAGREEMENTS: If the Reviewer's assessment differs from your own, include BOTH 
   perspectives. Don't suppress disagreement — it's valuable signal.

4. PROPOSED CHANGES: For each proposed change, you MUST include:
   - The specific file to edit
   - The exact text to add/change (not "update the routing rules" but the actual rule)
   - Which of the 4 inputs provided the evidence
   - Whether it requires Cem approval
   - The validation metric and trial period
   - Limit to 5 proposed changes max. Prioritise ruthlessly.

5. FOLLOW-UP: Check every proposed change from last week's review.
   Did it get approved? Applied? Did it work? Be honest.

6. CEM'S TIME IS SACRED: Cem should be able to review and approve/reject all 
   changes in under 10 minutes. If you're proposing too much, you're not 
   prioritising well enough.

7. TONE: Direct, evidence-based, self-critical but not self-flagellating. 
   You're a chief of staff reporting to the CEO, not a student apologising 
   to a teacher.

OUTPUT: Save to /reviews/[YYYY]-W[xx]_REVIEW.md following the template in Part 1.3.

TELEGRAM BRIEF FORMAT (sent via bot):
---
📊 Weekly Review — W[xx]

[Bullet 1: Top win]
[Bullet 2: Top failure + fix]  
[Bullet 3: Key metric change]
[Bullet 4: What's changing next week]
[Bullet 5: What needs your approval (if anything)]

Full review: [link to file or "in workspace"]
---
```

---

## Part 5: Knowledge Gap Detection & Handling

### 5.1 Complete Gap Taxonomy

#### Gap Type 1: DATA GAP

**Definition:** Athena needs a metric, number, or dataset she can't access.

**Detection signals:**
- Athena attempts a BQ query and gets an error or empty result
- Athena needs to make a decision but lacks a specific number (e.g., current inventory level, conversion rate, revenue for a period)
- A task requires data from a system Athena isn't connected to
- Athena makes an assumption and explicitly notes "assuming X because I can't verify"

**Examples:**
- Need live PrintHouse inventory count but BQ table hasn't been updated since last sync
- Need Amazon seller metrics but no API connection
- Need cost-per-unit for a new product but supplier quote not in system

**Immediate action:**
1. Check if data exists elsewhere (alternative table, cached report, Harry's financial records)
2. If available via another agent: delegate query (Harry for financial data, Hermes for BQ/API)
3. If truly unavailable: log gap in `KNOWLEDGE_GAPS.md` with urgency and workaround used
4. Use best available proxy with explicit uncertainty: "Using last month's data as proxy — [X]% confidence"

**Systemic fix:**
- Hermes creates data pipeline (cron job pulling from source API → BQ/SQLite)
- New skill documenting where each data type lives and how to access it
- Dashboard or automated report that surfaces the metric regularly

**Feed into improvement loop:**
```json
{
  "gap_type": "data",
  "description": "Live PH inventory not available in BQ",
  "first_detected": "2026-07-14",
  "occurrences": 3,
  "workaround": "Using last sync data (up to 24h stale)",
  "systemic_fix": "Hermes to create hourly PH→BQ sync cron",
  "status": "open",
  "assigned_to": "Hermes",
  "eta": "2026-W31"
}
```

#### Gap Type 2: CONTEXT GAP

**Definition:** Athena is missing background, history, or situational knowledge needed to make a good decision.

**Detection signals:**
- Athena asks Cem a question that she "should" know the answer to (Cem's response: "I told you this before" or "check your notes")
- Athena makes a decision and Cem corrects it with context Athena didn't have
- A task involves a relationship, history, or nuance not captured in any file
- Athena needs to understand *why* a process exists, not just *what* it is

**Examples:**
- Don't know why Disney has a different approval process than other licensors
- Unaware that a specific supplier has been unreliable in the past
- Missing context on why Cem prefers one marketplace over another for certain products

**Immediate action:**
1. Search MEMORY.md and session logs for prior mentions
2. If found: update current context and proceed
3. If not found: ask Cem with a specific question (not vague "what should I know?")
4. Log the gap so it gets captured permanently

**Systemic fix:**
- Create or update reference skill (e.g., `licensor-reference`) with the missing context
- Update MEMORY.md with permanent business context entries
- Create `/workspace/context/[topic].md` reference files for complex topics

**Feed into improvement loop:** Context gaps that recur → reference skill creation trigger

#### Gap Type 3: CAPABILITY GAP

**Definition:** Athena lacks a tool, API integration, or technical skill to accomplish a task.

**Detection signals:**
- A task requires interaction with a system Athena has no API access to
- Athena needs to perform an action that no agent in the team can do
- A manual process exists because no automation has been built
- Athena knows *what* to do but can't execute because the tooling doesn't exist

**Examples:**
- No API integration with TikTok Shop (new marketplace)
- Can't generate product mockups (need to integrate with design tool API)
- No automated way to check trademark status

**Immediate action:**
1. Check if an existing agent can handle it (Hermes for code, Sven for creative, etc.)
2. If no agent can: perform manually and document the manual process
3. Flag as automation candidate for Hermes

**Systemic fix:**
- Hermes builds the integration/tool
- New skill created documenting how to use the new capability
- Add to AGENTS.md if it changes an agent's capability profile

**Feed into improvement loop:** Capability gaps → AUTOMATION_CANDIDATES.md → Hermes sprint

#### Gap Type 4: AUTHORITY GAP

**Definition:** Unclear who owns a decision, task, or domain — leading to either inaction or stepping on toes.

**Detection signals:**
- Athena hesitates on a task because she's unsure if it's her call or Cem's
- Two agents get assigned overlapping work
- A task sits in limbo because nobody claims ownership
- Cem says "why did you ask me this? Just handle it" or conversely "why didn't you check with me?"

**Examples:**
- Mixed creative/strategy task: does Sven or Ava lead?
- New product launch pricing: Harry's domain or Cem's?
- Customer complaint on social media: Marketing or Operations?

**Immediate action:**
1. Check ESCALATION_CALIBRATION.md for existing guidance
2. Check DELEGATION_NOTES.md for the relevant agents
3. If still unclear: default to escalating to Cem (safer than overstepping)
4. Log the ambiguity explicitly

**Systemic fix:**
- Update ESCALATION_CALIBRATION.md with the clarified boundary
- Update relevant DELEGATION_NOTES.md files
- If it's a fundamental authority question: propose SOUL.md amendment
- Create a RACI note for the ambiguous domain

**Feed into improvement loop:** Authority gaps that recur → SOUL.md amendment proposal

#### Gap Type 5: TEMPORAL GAP

**Definition:** Information exists but may be stale, outdated, or no longer accurate.

**Detection signals:**
- Athena references a MEMORY.md entry or context file older than 90 days
- A process that was documented has likely changed (e.g., marketplace policy updates)
- Athena's knowledge about a tool/vendor is from months ago
- An agent's capabilities have changed but DELEGATION_NOTES.md hasn't been updated

**Examples:**
- MEMORY.md says "PrintHouse turnaround is 5 business days" — that may have changed
- Supplier pricing from Q1 being used for Q3 cost calculations
- Agent DELEGATION_NOTES.md written 3 months ago doesn't reflect recent improvements

**Immediate action:**
1. Check if fresher information is available (recent session logs, agent reports)
2. If the stale information is being used for a decision: flag the uncertainty explicitly
3. Trigger a verification task: "Confirm [X] is still current"

**Systemic fix:**
- Add `last_verified` dates to all reference files and context entries
- Create a quarterly "staleness audit" skill that checks all reference data
- Gemma 4 nightly job: flag any MEMORY.md entry referenced today that's >90 days old

**Feed into improvement loop:** Temporal gaps → staleness audit → reference refresh cycle

### 5.2 Knowledge Gap Registry

**Location:** `/workspace/compiled/KNOWLEDGE_GAPS.md`  
**Updated by:** Athena (continuously) + Weekly Review (formal reconciliation)

```markdown
# Knowledge Gap Registry
Last updated: [timestamp]

## Open Gaps

### GAP-001 [DATA] Live PH inventory sync
- **Detected:** 2026-07-14
- **Occurrences:** 3
- **Impact:** Delays in reorder decisions by ~24 hours
- **Workaround:** Using last-sync data with uncertainty flag
- **Fix:** Hermes building hourly sync cron
- **Assigned:** Hermes
- **ETA:** 2026-W31
- **Priority:** HIGH

### GAP-002 [CONTEXT] Disney approval process nuances
- **Detected:** 2026-07-10
- **Occurrences:** 2
- **Impact:** Two briefs sent without required pre-approval step
- **Workaround:** Always escalate Disney tasks to Cem
- **Fix:** Create licensor-reference skill with per-licensor SOPs
- **Assigned:** Athena (skill creation)
- **ETA:** 2026-W30
- **Priority:** MEDIUM

## Resolved Gaps

### GAP-000 [CAPABILITY] Amazon Seller API access
- **Detected:** 2026-06-15
- **Resolved:** 2026-06-28
- **Resolution:** Hermes built API integration, documented in skill amazon-seller-ops
```

---

## Part 6: The Virtuous Loop — Full Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    ATHENA SELF-AWARENESS & CONTINUOUS IMPROVEMENT               ║
║                              FULL ARCHITECTURE                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝

                              ┌─────────────────┐
                              │   CEM (CEO)      │
                              │  Reviews weekly  │
                              │  Approves/Rejects│
                              └────────┬────────┘
                                       │ Monday 09:00
                                       │ Telegram
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          ATHENA (Master Orchestrator)                        │
│                     Claude Opus 4 — 30-min heartbeat                        │
│                                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐   │
│  │  SOUL.md    │  │ MEMORY.md    │  │ TASK_SHEET   │  │ mistakes.md    │   │
│  │  (identity) │  │ (long-term)  │  │ (active work)│  │ (failure log)  │   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘  └───────┬────────┘   │
│         │                │                  │                   │            │
│         └────────────────┴──────────────────┴───────────────────┘            │
│                                     │                                        │
│                          [Daily Operations]                                  │
│                                     │                                        │
│              ┌──────────────────────┼──────────────────────┐                │
│              ▼                      ▼                      ▼                │
│     ┌────────────┐        ┌────────────┐         ┌────────────┐            │
│     │ Delegate   │        │ Execute    │         │ Escalate   │            │
│     │ to agents  │        │ autonomously│        │ to Cem     │            │
│     └─────┬──────┘        └─────┬──────┘         └─────┬──────┘            │
│           │                     │                       │                   │
│           ▼                     ▼                       ▼                   │
│    ┌──────────────────────────────────────────────────────────┐             │
│    │              SESSION LOGS (daily memory/)                │             │
│    │   Every decision, delegation, outcome, Cem interaction   │             │
│    └──────────────────────────┬───────────────────────────────┘             │
│                               │                                             │
└───────────────────────────────┼─────────────────────────────────────────────┘
                                │
        ════════════════════════╪═══════════════════════════════
               NIGHTLY CYCLE   │   (23:30 ET daily)
        ════════════════════════╪═══════════════════════════════
                                ▼
                    ┌───────────────────────┐
                    │   GEMMA 4 (Ollama)    │
                    │   Local, $0 cost      │
                    │                       │
                    │  Reads:               │
                    │  • session log        │
                    │  • mistakes.md        │
                    │  • TASK_SHEET.md      │
                    │                       │
                    │  Produces:            │
                    │  • daily pattern JSON │
                    │  • metrics extraction │
                    │  • correction tagging │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  /compiled/daily/     │
                    │  YYYY-MM-DD_          │
                    │  patterns.json        │
                    │  (7 files per week)   │
                    └───────────┬───────────┘
                                │
        ════════════════════════╪═══════════════════════════════
              WEEKLY CYCLE     │   (Saturday-Monday)
        ════════════════════════╪═══════════════════════════════
                                │
          Saturday 23:00 ET     │
                                ▼
                    ┌───────────────────────┐
                    │   GEMMA 4 (Ollama)    │
                    │   Weekly Aggregation  │
                    │                       │
                    │  Reads:               │
                    │  • 7 daily JSONs      │
                    │  • 3 prior weekly     │
                    │    pattern files      │
                    │                       │
                    │  Produces:            │
                    │  WEEKLY_PATTERNS.json │
                    │  • Merged patterns    │
                    │  • Frequency counts   │
                    │  • Escalated items    │
                    │  • Cross-week trends  │
                    └───────────┬───────────┘
                                │
          Sunday 00:00 ET       ▼
          ┌─────────────────────────────────────────────────────┐
          │                                                     │
          ▼                                                     │
┌─────────────────────┐                                         │
│  REVIEWER (Sonnet)  │                                         │
│  Spun up weekly     │                                         │
│  ~$0.02             │                                         │
│                     │                                         │
│  Reads:             │                                         │
│  • WEEKLY_PATTERNS  │                                         │
│  • mistakes.md      │                                         │
│  • TASK_SHEET.md    │                                         │
│  • Last 3 reviews   │                                         │
│                     │                                         │
│  Produces:          │                                         │
│  REVIEWER_CRITIQUE  │                                         │
│  .md                │                                         │
│  • Performance grade│                                         │
│  • Critical issues  │                                         │
│  • Delegation audit │                                         │
│  • Rule change      │                                         │
│    proposals        │                                         │
└─────────┬───────────┘                                         │
          │                                                     │
          │  Sunday 01:00 ET                                    │
          │                     ┌───────────────────────┐       │
          │                     │   HERMES (Claude Code)│       │
          │                     │   ~$0.05              │       │
          │                     │                       │       │
          │                     │  Reads:               │       │
          │                     │  • Session logs       │       │
          │                     │  • /crons/ directory  │       │
          │                     │  • CLI history        │       │
          │                     │  • TASK_SHEET.md      │       │
          │                     │                       │       │
          │                     │  Produces:            │       │
          │                     │  AUTOMATION_          │       │
          │                     │  CANDIDATES.md        │       │
          │                     │  • Manual processes   │       │
          │                     │  • Script proposals   │       │
          │                     │  • Cron health check  │       │
          │                     └───────────┬───────────┘       │
          │                                 │                   │
          │  Sunday 02:00 ET                │                   │
          │                     ┌───────────────────────┐       │
          │                     │   AVA (OpenClaw)      │       │
          │                     │   CPO/Strategy        │       │
          │                     │   ~$0.03              │       │
          │                     │                       │       │
          │                     │  Reads:               │       │
          │                     │  • Project tables     │       │
          │                     │  • TASK_SHEET.md      │       │
          │                     │  • WEEKLY_PATTERNS    │       │
          │                     │                       │       │
          │                     │  Produces:            │       │
          │                     │  STRATEGIC_GAPS.md    │       │
          │                     │  • Portfolio health   │       │
          │                     │  • Pillar balance     │       │
          │                     │  • Blocked projects   │       │
          │                     │  • 30-day outlook     │       │
          │                     └───────────┬───────────┘       │
          │                                 │                   │
          ▼                                 ▼                   │
┌─────────────────────────────────────────────────────────────┐ │
│                    COMPILED INPUTS                           │ │
│                    /compiled/                                │ │
│                                                             │ │
│  ┌────────────────┐ ┌──────────────┐ ┌──────────────┐      │ │
│  │REVIEWER_       │ │AUTOMATION_   │ │STRATEGIC_    │      │ │
│  │CRITIQUE.md     │ │CANDIDATES.md │ │GAPS.md       │      │ │
│  └───────┬────────┘ └──────┬───────┘ └──────┬───────┘      │ │
│          └─────────────────┼────────────────┘               │ │
│                            │                                │ │
└────────────────────────────┼────────────────────────────────┘ │
                             │                                  │
          Sunday 06:00 ET    │    ┌─────────────────────────────┘
                             ▼    ▼
                    ┌───────────────────────┐
                    │   ATHENA (Synthesis)  │
                    │   Claude Opus 4       │
                    │   ~$0.10              │
                    │                       │
                    │  Reads ALL:           │
                    │  • 4 compiled files   │
                    │  • Raw data sources   │
                    │  • Prior 3 reviews    │
                    │                       │
                    │  Produces:            │
                    │  WEEKLY_REVIEW.md     │
                    │  + Telegram brief     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   /reviews/           │
                    │   YYYY-Wxx_REVIEW.md  │
                    │                       │
                    │  Contains:            │
                    │  • Executive summary  │
                    │  • Scorecard          │
                    │  • Full analysis      │
                    │  • Proposed changes   │
                    │  │  (PROPOSED status) │
                    │  • Prior change       │
                    │    follow-up          │
                    └───────────┬───────────┘
                                │
                     ┌──────────┴──────────┐
                     ▼                     ▼
          ┌──────────────────┐  ┌──────────────────┐
          │ Telegram Brief   │  │ Full Review File │
          │ to Cem (Sunday)  │  │ in workspace     │
          └──────────────────┘  └──────────────────┘
                     │
                     ▼ (Monday — Cem reviews)
          ┌──────────────────────────────────────────┐
          │           CEM DECISION GATE              │
          │                                          │
          │  For each proposed change:               │
          │  ✅ APPROVED → Apply immediately          │
          │  ❌ REJECTED → Log reason, don't retry    │
          │     for 4 weeks without new evidence     │
          │  🔄 MODIFY → Apply modified version       │
          └──────────────────┬───────────────────────┘
                             │
                             ▼
          ┌──────────────────────────────────────────┐
          │         CHANGE APPLICATION               │
          │                                          │
          │  Routing change → ROUTING_RULES.md       │
          │  Escalation change → ESCALATION_         │
          │                      CALIBRATION.md      │
          │  Delegation change → DELEGATION_NOTES/   │
          │  New skill → /skills/[name]/SKILL.md     │
          │  SOUL change → SOUL.md (with changelog)  │
          │  New automation → Hermes builds it        │
          │                                          │
          │  All changes tagged: TRIAL (2 weeks)     │
          └──────────────────┬───────────────────────┘
                             │
        ═════════════════════╪═══════════════════════
             VALIDATION      │  (2-week trial)
        ═════════════════════╪═══════════════════════
                             │
                             ▼
          ┌──────────────────────────────────────────┐
          │         VALIDATION LOOP                  │
          │                                          │
          │  Gemma 4 nightly: does the pattern       │
          │  still appear?                           │
          │                                          │
          │  Athena weekly: check validation metric  │
          │                                          │
          │  After 2 weeks:                          │
          │  ├── IMPROVED (≥20%) → STABLE            │
          │  ├── NO CHANGE (±10%) → extend trial     │
          │  ├── DEGRADED (≥10%) → REVERT            │
          │  └── INCONCLUSIVE → extend trial         │
          └──────────────────┬───────────────────────┘
                             │
                             ▼
          ┌──────────────────────────────────────────┐
          │         FEEDBACK INTO SYSTEM             │
          │                                          │
          │  Stable rules → permanent in config      │
          │  Stable skills → SKILL_INDEX updated     │
          │  Failed approaches → logged, avoided     │
          │  Learnings → feed next week's reflection │
          │                                          │
          │  THE LOOP CONTINUES ─────────────────────┼──→ (back to top)
          └──────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════
                    FILE SYSTEM MAP
═══════════════════════════════════════════════════════════════

/workspace/
├── SOUL.md                          ← Identity + improvement protocol
├── MEMORY.md                        ← Long-term business context
├── TASK_SHEET.md                    ← Active work tracking
├── mistakes.md                      ← Failure log
│
├── memory/                          ← Daily session logs
│   ├── 2026-07-14.md
│   ├── 2026-07-15.md
│   └── ...
│
├── config/                          ← Habit change files
│   ├── ROUTING_RULES.md
│   ├── ESCALATION_CALIBRATION.md
│   └── KNOWLEDGE_GAPS.md
│
├── 03-Agents/                       ← Per-agent intelligence
│   ├── Ava/
│   │   └── DELEGATION_NOTES.md
│   ├── Harry/
│   │   └── DELEGATION_NOTES.md
│   ├── Sven/
│   │   └── DELEGATION_NOTES.md
│   ├── Hermes/
│   │   └── DELEGATION_NOTES.md
│   └── Gemma/
│       └── DELEGATION_NOTES.md
│
├── skills/                          ← Athena's skill library
│   ├── SKILL_INDEX.md
│   ├── inventory-reorder-check/
│   │   └── SKILL.md
│   ├── listing-prep/
│   │   └── SKILL.md
│   └── archive/                     ← Deprecated skills
│       └── old-inventory-check/
│           └── SKILL.md
│
├── compiled/                        ← Weekly cycle outputs
│   ├── daily/                       ← Gemma 4 nightly outputs
│   │   ├── 2026-07-14_patterns.json
│   │   └── ...
│   ├── archive/                     ← Historical weekly patterns
│   │   └── WEEKLY_PATTERNS_2026-W28.json
│   ├── WEEKLY_PATTERNS.json         ← Latest weekly aggregation
│   ├── REVIEWER_CRITIQUE.md         ← Latest reviewer output
│   ├── AUTOMATION_CANDIDATES.md     ← Latest Hermes scan
│   └── STRATEGIC_GAPS.md            ← Latest Ava analysis
│
├── reviews/                         ← Permanent review archive
│   ├── 2026-W27_REVIEW.md
│   ├── 2026-W28_REVIEW.md
│   └── 2026-W29_REVIEW.md
│
└── crons/                           ← Automation scripts
    ├── log_parser.sh                ← Gemma 4 nightly
    ├── weekly_aggregator.sh         ← Gemma 4 Saturday
    ├── weekly_review_orchestrator.sh ← Sunday cycle runner
    └── [automation scripts built by Hermes]
```

---

## Part 7: The SOUL.md Section

This is the exact text to add to Athena's SOUL.md. Under 30 lines, reference-dense, executable.

```markdown
## Self-Awareness & Continuous Improvement Protocol

I reflect, adapt, and improve weekly without Cem telling me what to change.

**Nightly (23:30 ET):** Gemma 4 parses my session log → /compiled/daily/[date]_patterns.json.
**Weekly (Sat-Sun):** Four-agent cycle produces WEEKLY_REVIEW.md:
  Gemma 4 (23:00) → patterns | Reviewer (00:00) → critique | Hermes (01:00) → automation | Ava (02:00) → strategy
  I synthesise all four at 06:00 → Telegram brief to Cem → he approves changes Monday.

**Habit changes live in files:** ROUTING_RULES.md, ESCALATION_CALIBRATION.md, DELEGATION_NOTES.md (per agent).
Changes I can auto-apply: routing rules, delegation notes, new skills.
Changes requiring Cem: SOUL.md edits, escalation threshold changes, authority boundaries.
All changes start as 2-week TRIAL → validated by metric → STABLE or REVERT.

**Skills:** I create skills when I do the same multi-step process 3+ times, or an agent consistently fails at a task type. Skills start EXPERIMENTAL (3+ uses to promote), tracked in SKILL_INDEX.md, retired after 60 days unused.

**Knowledge gaps:** I categorise what I don't know (Data/Context/Capability/Authority/Temporal), log in KNOWLEDGE_GAPS.md, and route each to the right fix: Hermes for data pipelines, reference skills for context, Cem for authority.

**Five questions I ask myself weekly:**
1. What did Cem have to correct, and have I encoded the lesson permanently?
2. Which delegations failed, and do I need to update routing or agent notes?
3. What patterns persist 3+ weeks that I haven't fixed?
4. What manual work should I automate?
5. What don't I know that I need to know?

**The bar:** Each week, my Coverage, Speed, and Intelligence metrics should improve. If any metric degrades for 2 consecutive weeks, I escalate to Cem with a diagnosis and proposed fix.
```

---

## Part 8: Implementation Roadmap

### Phase 1: Minimum Viable Self-Improvement Loop (Week 1)

**Goal:** Get the basic reflection cycle running. Athena can reflect weekly and propose changes, even if the multi-agent cycle isn't ready yet.

#### What Cem Does (30 minutes total):
1. **Approve the SOUL.md addition** (5 min) — Review and approve the Section 7 text above
2. **Create directory structure** (5 min) — Or tell Athena/Hermes to do it:
   ```bash
   mkdir -p /workspace/{config,compiled/daily,compiled/archive,reviews,crons,skills/archive}
   mkdir -p /workspace/03-Agents/{Ava,Harry,Sven,Hermes,Gemma}
   ```
3. **Review first manual weekly review** (20 min) — Athena will produce the first WEEKLY_REVIEW.md manually (no agents), and Cem reviews to calibrate expectations

#### What Athena Sets Up Herself:
1. **Create config files:**
   - `/workspace/config/ROUTING_RULES.md` — Start empty, populated from first review
   - `/workspace/config/ESCALATION_CALIBRATION.md` — Seed with known escalation rules from SOUL.md
   - `/workspace/config/KNOWLEDGE_GAPS.md` — Start empty
2. **Create DELEGATION_NOTES.md per agent** — Seed with what Athena already knows about each agent's strengths/weaknesses from MEMORY.md and experience
3. **Create SKILL_INDEX.md** — Audit existing skills/, document current state
4. **Run first weekly reflection manually** — Athena reads her own logs, mistakes.md, and TASK_SHEET.md, and writes the first WEEKLY_REVIEW.md using the template. No other agents involved. This calibrates the format.
5. **Identify the top 3 patterns** from the first manual review — these become the first proposed changes

#### What Hermes Builds:
1. **`log_parser.sh`** — The Gemma 4 nightly cron job (from Part 2). Test it with 3 days of existing logs.
2. **Cron scheduling** — Set up the 23:30 nightly cron for Gemma 4 log parsing
3. **JSON validation** — Simple script that checks Gemma 4's output is valid JSON (Gemma sometimes outputs malformed JSON)

#### Week 1 Deliverables:
- [ ] SOUL.md updated with improvement protocol
- [ ] Directory structure created
- [ ] All config files seeded
- [ ] DELEGATION_NOTES.md for all 5 agents
- [ ] SKILL_INDEX.md with current skill audit
- [ ] First manual WEEKLY_REVIEW.md produced and reviewed by Cem
- [ ] Gemma 4 nightly log parser running and producing valid JSON
- [ ] First 3 proposed changes from manual review (at least 1 approved by Cem)

---

### Phase 2: Multi-Agent Review Cycle (Weeks 2-3)

**Goal:** The full Saturday-Sunday cycle runs with all 4 agents. Athena synthesises and sends Cem a Telegram brief.

#### What Cem Does (15 minutes/week):
1. **Monday morning:** Review Telegram brief + WEEKLY_REVIEW.md, approve/reject proposed changes
2. **Calibrate:** After 2 weeks, tell Athena what's useful and what's noise in the reviews

#### What Athena Sets Up:
1. **Weekly aggregation prompt** — Test Gemma 4's Saturday aggregation with 2 weeks of daily JSONs
2. **Reviewer subagent** — Write the system prompt (from Part 4), test with one week of data
3. **Ava strategic scan** — Send Ava the strategic scan prompt, calibrate output format
4. **Telegram brief format** — Configure the Telegram bot to send the formatted executive summary
5. **Follow-up tracking** — Start tracking proposed changes across weeks (PROPOSED → APPROVED → TRIAL → STABLE/REVERTED)

#### What Hermes Builds:
1. **`weekly_aggregator.sh`** — Gemma 4 Saturday aggregation cron
2. **`weekly_review_orchestrator.sh`** — Master script that runs the Sunday cycle:
   ```bash
   # Saturday 23:00 — Gemma 4 aggregation (already scheduled)
   # Sunday 00:00 — Spin up Reviewer subagent
   # Sunday 01:00 — Trigger Hermes automation scan
   # Sunday 02:00 — Trigger Ava strategic scan
   # Sunday 06:00 — Trigger Athena synthesis
   ```
3. **Reviewer subagent runner** — Script that creates a Claude Sonnet subagent, feeds it the inputs, captures the output
4. **Hermes self-scan script** — Hermes's automation scanning capability (it's analysing its own codebase)
5. **Archival automation** — Script that archives compiled files after each weekly cycle

#### Weeks 2-3 Deliverables:
- [ ] Gemma 4 weekly aggregation tested and producing valid WEEKLY_PATTERNS.json
- [ ] Reviewer subagent running and producing REVIEWER_CRITIQUE.md
- [ ] Hermes automation scan producing AUTOMATION_CANDIDATES.md
- [ ] Ava strategic scan producing STRATEGIC_GAPS.md
- [ ] Full Athena synthesis producing WEEKLY_REVIEW.md from all 4 inputs
- [ ] Telegram brief sent to Cem Sunday morning (2 successful weeks)
- [ ] At least 5 proposed changes across 2 weeks, with at least 3 approved
- [ ] Change follow-up tracking working (previous weeks' changes have status updates)
- [ ] orchestrator.sh running end-to-end without manual intervention

---

### Phase 3: Skill Creation/Retirement Lifecycle (Month 2)

**Goal:** Athena autonomously creates, tests, promotes, and retires skills based on observed patterns.

#### What Cem Does (10 minutes/week):
1. **Review new skill proposals** in WEEKLY_REVIEW.md (most won't need approval)
2. **Validate 1-2 promoted skills** — Confirm that "experimental → stable" transitions make sense
3. **Flag skills to deprecate** — If Cem knows a process has changed

#### What Athena Sets Up:
1. **Skill creation triggers** — Integrate Gemma 4's `repeated_sequences` detection with skill creation workflow
2. **Skill template** — Create the template (from Part 3) as a reference in `/skills/SKILL_TEMPLATE.md`
3. **Skill lifecycle management** — After each skill use, update YAML frontmatter (uses, successes, failures, last_used)
4. **SKILL_INDEX.md auto-update** — After each skill lifecycle event, regenerate the index
5. **Quarterly staleness audit** — Run monthly (not quarterly at first) to catch stale skills early
6. **Knowledge gap → skill pipeline** — When a CONTEXT gap recurs 3+ times, automatically propose a reference skill

#### What Hermes Builds:
1. **Skill frontmatter updater** — Script that reads a skill's YAML, increments counters, updates dates
2. **Skill index generator** — Script that reads all `/skills/*/SKILL.md` files, generates SKILL_INDEX.md
3. **Staleness checker** — Script that flags skills not used in 60 days, reference files not verified in 90 days
4. **First automation from AUTOMATION_CANDIDATES.md** — Build the highest-priority automation identified in Phase 2

#### Month 2 Deliverables:
- [ ] At least 3 skills created by Athena autonomously
- [ ] At least 1 skill promoted from experimental → stable
- [ ] Skill lifecycle tracking working (YAML frontmatter updating automatically)
- [ ] SKILL_INDEX.md auto-generating after each lifecycle event
- [ ] Knowledge gap → skill pipeline producing at least 1 reference skill
- [ ] First Hermes-built automation live and validated
- [ ] Staleness checker running monthly
- [ ] Cem spending ≤10 min/week on improvement cycle review

---

### Phase 4: Genuine Self-Calibration (Month 3+)

**Goal:** The system runs itself. Athena is genuinely getting better week over week, measurably. Cem's role shifts from reviewing changes to steering strategy.

#### What Cem Does (5 minutes/week):
1. **Glance at Telegram brief** — Confirm nothing unexpected
2. **Approve only SOUL.md changes and authority boundary shifts** — Everything else is on autopilot
3. **Monthly deep review** — Look at 4-week trend in the scorecard, validate direction

#### What Athena Achieves:
1. **Self-calibrating delegation** — Accept rates across all agents > 80% (up from wherever they started)
2. **Pattern resolution** — No pattern persists more than 4 weeks without a fix or escalation
3. **Proactive automation** — Athena proposes automations before Cem notices the manual work
4. **Skill maturity** — 80%+ of active skills are stable, creation and retirement flowing naturally
5. **Knowledge gap closure** — Average gap resolution time < 2 weeks
6. **Coverage growth** — Measurable increase in % of Cem's operational load handled autonomously
7. **Meta-improvement** — The improvement loop itself gets better: faster pattern detection, better proposals, higher approval rate

#### Validation Metrics (Month 3 Targets):

| Metric | Phase 1 Baseline | Month 3 Target | How Measured |
|--------|-----------------|----------------|--------------|
| Delegation accept rate (all agents) | Establish baseline | > 80% | DELEGATION_NOTES.md data |
| Cem corrections per week | Establish baseline | < 2 | mistakes.md tagging |
| On-time task completion | Establish baseline | > 85% | TASK_SHEET.md |
| Pattern resolution time | N/A | < 4 weeks | WEEKLY_PATTERNS.json tracking |
| Skill creation rate | 0 | 1-2 per month | SKILL_INDEX.md |
| Automation proposals accepted | 0 | > 60% | AUTOMATION_CANDIDATES.md tracking |
| Cem review time per week | 30 min (Phase 1) | < 10 min | Self-reported |
| Recurring mistakes | Establish baseline | 50% reduction | mistakes.md cross-week analysis |

#### What Hermes Builds (Ongoing):
1. **Metrics dashboard** — SQLite database + simple web dashboard showing scorecard trends over time
2. **Automated validation** — Script that checks trial rules at midpoint and endpoint, produces validation reports
3. **Cross-week trend analysis** — Script that reads all WEEKLY_PATTERNS.json files, produces trend visualization
4. **Improvement velocity metric** — How fast is Athena getting better? (Week-over-week metric improvement rate)

#### Long-Term Evolution (Month 6+):
- **Self-modifying prompts:** Athena adjusts the Gemma 4 log parser prompt based on what it's missing
- **Agent capability evolution:** As agents improve, DELEGATION_NOTES.md automatically expands their trusted task types
- **Predictive mode:** Athena starts anticipating problems before they manifest (based on pattern trends)
- **Cross-business learning:** Patterns from one pillar inform improvements in another
- **Cem trust score:** Implicit metric — how many decisions does Cem override? Trending toward zero = maximum trust

---

## Appendix: Weekly Orchestrator Script

```bash
#!/bin/bash
# /workspace/crons/weekly_review_orchestrator.sh
# Master script for the Sunday reflection cycle
# Scheduled: Saturday 23:00 ET (kicks off the cascade)

set -e
WEEK=$(date +%Y-W%V)
LOG="/workspace/compiled/orchestrator_${WEEK}.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

# Step 1: Gemma 4 Weekly Aggregation (runs immediately at Sat 23:00)
log "Step 1: Starting Gemma 4 weekly aggregation"
bash /workspace/crons/weekly_aggregator.sh >> "$LOG" 2>&1
log "Step 1: Complete — WEEKLY_PATTERNS.json generated"

# Validate JSON output
if ! python3 -c "import json; json.load(open('/workspace/compiled/WEEKLY_PATTERNS.json'))" 2>/dev/null; then
  log "ERROR: WEEKLY_PATTERNS.json is invalid JSON. Attempting repair..."
  # Fallback: have Gemma 4 retry with stricter prompt
  bash /workspace/crons/weekly_aggregator.sh --strict >> "$LOG" 2>&1
fi

# Step 2: Reviewer Subagent (Sunday 00:00 — wait 1 hour)
log "Step 2: Waiting until 00:00 for Reviewer..."
sleep_until_hour 0  # utility function that sleeps until target hour

log "Step 2: Starting Reviewer subagent"
# Spin up Claude Sonnet subagent via Claude SDK
python3 /workspace/crons/run_reviewer.py \
  --patterns /workspace/compiled/WEEKLY_PATTERNS.json \
  --mistakes /workspace/mistakes.md \
  --tasks /workspace/TASK_SHEET.md \
  --prior-reviews /workspace/reviews/ \
  --output /workspace/compiled/REVIEWER_CRITIQUE.md \
  >> "$LOG" 2>&1
log "Step 2: Complete — REVIEWER_CRITIQUE.md generated"

# Step 3: Hermes Automation Scan (Sunday 01:00)
log "Step 3: Waiting until 01:00 for Hermes..."
sleep_until_hour 1

log "Step 3: Starting Hermes automation scan"
# Trigger Hermes via OpenClaw agent-to-agent message
python3 /workspace/crons/trigger_hermes_scan.py \
  --session-logs /workspace/memory/ \
  --crons /workspace/crons/ \
  --output /workspace/compiled/AUTOMATION_CANDIDATES.md \
  >> "$LOG" 2>&1
log "Step 3: Complete — AUTOMATION_CANDIDATES.md generated"

# Step 4: Ava Strategic Scan (Sunday 02:00)
log "Step 4: Waiting until 02:00 for Ava..."
sleep_until_hour 2

log "Step 4: Starting Ava strategic scan"
python3 /workspace/crons/trigger_ava_scan.py \
  --projects /workspace/SOUL-Athena-V3.md \
  --tasks /workspace/TASK_SHEET.md \
  --patterns /workspace/compiled/WEEKLY_PATTERNS.json \
  --output /workspace/compiled/STRATEGIC_GAPS.md \
  >> "$LOG" 2>&1
log "Step 4: Complete — STRATEGIC_GAPS.md generated"

# Step 5: Athena Synthesis (Sunday 06:00)
log "Step 5: Waiting until 06:00 for Athena synthesis..."
sleep_until_hour 6

log "Step 5: Starting Athena synthesis"
python3 /workspace/crons/run_synthesis.py \
  --patterns /workspace/compiled/WEEKLY_PATTERNS.json \
  --critique /workspace/compiled/REVIEWER_CRITIQUE.md \
  --automation /workspace/compiled/AUTOMATION_CANDIDATES.md \
  --strategy /workspace/compiled/STRATEGIC_GAPS.md \
  --output /workspace/reviews/${WEEK}_REVIEW.md \
  >> "$LOG" 2>&1
log "Step 5: Complete — ${WEEK}_REVIEW.md generated"

# Step 6: Send Telegram brief to Cem
log "Step 6: Sending Telegram brief"
python3 /workspace/crons/send_telegram_brief.py \
  --review /workspace/reviews/${WEEK}_REVIEW.md \
  >> "$LOG" 2>&1
log "Step 6: Complete — Telegram brief sent"

# Cleanup and archive
cp /workspace/compiled/WEEKLY_PATTERNS.json \
   "/workspace/compiled/archive/WEEKLY_PATTERNS_${WEEK}.json"

log "Weekly review cycle complete for ${WEEK}"
```

---

## Appendix: Quick Reference — What Goes Where

| Signal | Detection | File Updated | Agent | Requires Cem |
|--------|-----------|-------------|-------|-------------|
| Wrong delegation | accept_rate < 60% | DELEGATION_NOTES.md | Athena | No |
| Routing error | pattern 3+ times | ROUTING_RULES.md | Athena | No |
| Escalation miscalibration | Cem override | ESCALATION_CALIBRATION.md | Athena | Yes |
| Repeated manual process | 3+ times/week | New skill in /skills/ | Athena | No |
| Agent capability change | accept_rate shift | DELEGATION_NOTES.md | Athena | No |
| Cem correction (recurring) | 2+ occurrences | SOUL.md amendment proposed | Athena | Yes |
| Automation opportunity | Hermes scan | Hermes builds it | Hermes | No (unless >2hr build) |
| Strategic gap | Ava scan | TASK_SHEET.md priority shift | Athena + Ava | If major |
| Knowledge gap (data) | Query failure | KNOWLEDGE_GAPS.md → Hermes pipeline | Hermes | No |
| Knowledge gap (context) | Missing info | Reference skill or MEMORY.md update | Athena | No |
| Knowledge gap (capability) | No tool available | KNOWLEDGE_GAPS.md → Hermes build | Hermes | If >4hr build |
| Knowledge gap (authority) | Ambiguous ownership | ESCALATION_CALIBRATION.md or SOUL.md | Athena | Yes |
| Knowledge gap (temporal) | Stale data (>90d) | Verification task triggered | Athena/Gemma | No |
| Skill degradation | success_rate < 60% | Skill deprecated → archive | Athena | No |
| Pattern persists 4+ weeks | Cross-week recurrence | Escalate to Cem | Athena | Yes |

---

*End of document. This architecture is designed to be implemented incrementally — start with Phase 1, validate the basic loop works, and build from there. The system should be fully self-calibrating by Month 3.*
