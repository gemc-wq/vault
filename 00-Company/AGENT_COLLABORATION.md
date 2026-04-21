# Agent Collaboration Framework
**Version:** 2.0 | **Updated:** 2026-04-19 | **Owner:** Athena

**Changelog:**
- v2.0 (2026-04-19): Added §10 Project Intake Rule and §11 Pending Validation Workflow. Reason: projects were splintering (61 folders with duplicates) and unvalidated wiki promotions were creating contradictory source-of-truth.
- v1.0 (2026-04-14): Initial framework.

---

## 1. The Problem

Agents work in isolation. Each has its own SOUL.md, TOOLS.md, and memory — but no standard way to:
- Hand off work to another agent
- See what other agents are working on
- Find shared company knowledge
- Know WHERE to look for what
- Avoid creating duplicate projects
- Validate knowledge before it becomes canonical

This document codifies how agents collaborate.

---

## 2. Vault Navigation Map

Every agent MUST have this reference in their TOOLS.md or session bootstrap. This is the "you are here" map.

```
/Users/openclaw/Vault/
│
├── 00-Company/                    ← COMPANY-WIDE (all agents read)
│   ├── AGENT_COLLABORATION.md     ← THIS FILE — how agents work together
│   ├── AGENT_ROSTER.md            ← Who does what, models, costs
│   ├── STRATEGY.md                ← North star, 3 metrics, 4 pillars
│   ├── compiled/                  ← Auto-generated reports (read-only)
│   │   ├── TASK_SHEET.md          ← Master task tracker
│   │   └── CRON_SCHEDULE.md       ← All cron jobs
│   └── skills/                    ← 7 skill buckets + index
│       └── SKILLS_INDEX.md        ← Which agent owns which skill
│
├── 01-Wiki/                       ← KNOWLEDGE BASE (reference docs)
│   ├── _pending/                  ← NEW: unvalidated promotions awaiting Cem approval
│   └── [topic folders]            ← Canonical, validated knowledge only
│
├── 02-Projects/                   ← ACTIVE PROJECTS (one folder each)
│   ├── _INDEX.md                  ← NEW: canonical project list — source of truth
│   └── [project-name]/            ← README, status, handoffs, specs
│
├── 03-Agents/                     ← AGENT-SPECIFIC (your folder)
│   ├── [YourName]/                ← Your memory, daily logs, outputs
│   │   ├── SOUL.md                ← Identity + rules (read-only)
│   │   ├── TOOLS.md               ← Your infrastructure + nav pointers
│   │   ├── memory/                ← Daily logs (YYYY-MM-DD.md)
│   │   └── handoffs/              ← Incoming work from other agents
│   └── ...
│
└── 04-Shared/                     ← CROSS-AGENT WORKSPACE
    ├── active/                    ← Currently in-progress shared work
    ├── handoffs/                  ← Completed handoffs awaiting pickup
    └── decisions/                 ← Decisions that affect multiple agents
```

---

## 3. Rules of Engagement

### 3.1 Read Permissions
| Folder | Who Can Read |
|--------|-------------|
| `00-Company/` | ALL agents |
| `01-Wiki/` | ALL agents |
| `01-Wiki/_pending/` | ALL agents (BUT treat as "draft, not canonical") |
| `02-Projects/` | ALL agents |
| `03-Agents/[YourName]/` | That agent + Athena |
| `03-Agents/[OtherAgent]/` | Read-only (no writes) |
| `04-Shared/` | ALL agents |

### 3.2 Write Permissions
| Folder | Who Can Write |
|--------|--------------|
| `00-Company/` | Athena only |
| `01-Wiki/` (direct) | Cem only (via approval of `_pending/`) |
| `01-Wiki/_pending/` | Compiler + agents (via promotion flagging) |
| `02-Projects/` (new folder) | **Athena only — see §10 Project Intake Rule** |
| `02-Projects/[existing]` | Assigned agent + Athena |
| `03-Agents/[YourName]/` | That agent + Athena |
| `03-Agents/[OtherAgent]/handoffs/` | Any agent (deposit only) |
| `04-Shared/active/` | Any agent working on shared task |
| `04-Shared/handoffs/` | Any agent (deposit), receiver (pickup) |
| `04-Shared/decisions/` | Athena only |

### 3.3 No Overwrites
Agents NEVER overwrite another agent's files. You can:
- **Deposit** a file into their `handoffs/` folder
- **Create** a new file in `04-Shared/`
- **NOT** edit files you didn't create (except your own folder)

---

## 4. Handoff Protocol

When Agent A completes work that Agent B needs:

### Step 1: Create Handoff File
```markdown
# Handoff: [Brief Title]
**From:** [Agent A] | **To:** [Agent B] | **Date:** YYYY-MM-DD
**Priority:** P0/P1/P2/P3
**Project:** [project name]

## What Was Done
[Summary of completed work]

## What You Need to Do
[Clear next actions for receiving agent]

## Files Referenced
- [paths to relevant files]

## Context
[Any background the receiver needs]

## Deadline
[When this needs to be picked up]
```

### Step 2: Deposit
Place the file in ONE of:
- `03-Agents/[ReceiverName]/handoffs/` — direct to agent
- `04-Shared/handoffs/` — if multiple agents need it

### Step 3: Notify
Athena routes the notification. Agents don't message each other directly.

### Step 4: Acknowledge
Receiving agent reads the handoff, moves it to their `memory/` folder, and logs acknowledgment.

---

## 5. Shared Work Protocol

When two or more agents collaborate on the same deliverable:

1. **Athena creates** a folder in `04-Shared/active/[task-name]/`
2. **Each agent writes** their contribution as a separate file (no shared editing)
3. **Athena synthesises** the parts into the final deliverable
4. **Completed work** moves to the relevant `02-Projects/` folder

Example:
```
04-Shared/active/procurement-zone-redesign/
├── README.md              ← Athena: scope, deadline, assignments
├── ava-strategic-prd.md   ← Ava: business requirements
├── harry-data-spec.md     ← Harry: data model + API spec  
└── hermes-build-log.md    ← Hermes: implementation notes
```

This prevents overwrites while keeping all contributions visible.

---

## 6. Session Bootstrap — What Every Agent Must Do

At the START of every session, each agent should:

1. **Read** `00-Company/compiled/TASK_SHEET.md` — check assigned tasks
2. **Read** `03-Agents/[YourName]/handoffs/` — check for incoming work
3. **Read** `00-Company/AGENT_COLLABORATION.md` — if unsure about process
4. **Read** relevant `02-Projects/` folders for active work
5. **Read** `02-Projects/_INDEX.md` before assuming what projects exist

This sequence MUST be referenced in each agent's TOOLS.md under a `## Session Bootstrap` section.

---

## 7. How Agents Find Things

### "Where do I look for X?"

| Looking For | Where to Find It |
|-------------|-----------------|
| My tasks | `00-Company/compiled/TASK_SHEET.md` |
| Company strategy | `00-Company/STRATEGY.md` |
| Who does what | `00-Company/AGENT_ROSTER.md` |
| Skill definitions | `00-Company/skills/SKILLS_INDEX.md` |
| How to collaborate | `00-Company/AGENT_COLLABORATION.md` (this file) |
| Project list (canonical) | `02-Projects/_INDEX.md` |
| Project status | `02-Projects/[name]/README.md` |
| Work handed to me | `03-Agents/[MyName]/handoffs/` |
| Shared work in progress | `04-Shared/active/` |
| Reference knowledge | `01-Wiki/[topic]/` |
| Draft knowledge (treat as uncertain) | `01-Wiki/_pending/` |
| Cron jobs | `00-Company/compiled/CRON_SCHEDULE.md` |
| Another agent's context | `03-Agents/[TheirName]/` (read-only) |

### "When should I look?"

| Trigger | Action |
|---------|--------|
| Session start | Read TASK_SHEET + check handoffs |
| Before starting a task | Check if related work exists in `02-Projects/` |
| Before writing a report | Check `01-Wiki/` for existing context |
| After completing work | Deposit handoff if another agent needs it |
| When stuck | Read `04-Shared/decisions/` for prior decisions on the topic |
| Before creating new project | **See §10 Project Intake Rule** |

---

## 8. Decision Log

When a cross-agent decision is made (e.g., "we're using Supabase not raw PG"), Athena logs it:

```
04-Shared/decisions/YYYY-MM-DD-[topic].md
```

All agents can reference these to avoid re-debating settled questions.

---

## 9. Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Edit another agent's files | Create a handoff or shared file |
| Message agents directly | Route through Athena |
| Duplicate work that exists | Search vault first |
| Assume another agent knows something | Include context in handoffs |
| Store shared work in your own folder | Use `04-Shared/` |
| Skip session bootstrap | Always check tasks + handoffs first |
| **Create a new project folder when chatting with Cem** | **Follow §10 Project Intake Rule — flag overlap, wait for approval** |
| **Quote from `01-Wiki/_pending/` as canonical truth** | **Only quote from validated `01-Wiki/` pages** |

---

## 10. Project Intake Rule (NEW v2.0)

**Problem solved:** 61 folders in `02-Projects/` with duplicates like `pulse-dashboard/` + `pulse-dashboard-v2/` + `pulse-unified/` + `command-center/`. Agents create new folders when Cem asks about work, without checking if a sibling already exists.

### The Rule
No agent may create a new folder in `02-Projects/` except Athena. Athena creates a new project folder only when ALL of the following are true:

1. **Search first**: Athena searches `02-Projects/_INDEX.md` and the folder tree for related keywords (title words, synonyms, component names).
2. **Overlap check**: If any existing folder scores "possibly related," Athena pastes the candidate list to Cem and asks: *"Before I create `[name]`, should this be part of `[existing-folder]`?"*
3. **Cem approval**: Cem confirms "new" or "merge into X." No silent creation.
4. **Canonical name**: New folders follow `domain-object-qualifier` naming (e.g., `marketplace-walmart-launch`, `dashboard-pulse-v3`, `finance-royalty-reporting`). No bare verbs, no duplicate stems.
5. **Register**: New folder is added to `02-Projects/_INDEX.md` with owner, status, parent domain, and one-line purpose.

### What Other Agents Do Instead
When Ava/Hermes/Harry recognise a new project is needed:
- Create a handoff in `03-Agents/Athena/handoffs/` titled `project-intake-[proposed-name].md`
- Include: proposed name, purpose, why existing folders don't cover it, suggested owner
- Athena picks it up, runs the overlap check, gets Cem approval, creates the folder

### Enforcement
The nightly compiler (see `CLAUDE_CODE_COMPILER_SPEC.md`) lints for:
- Folders created since last run that are not in `_INDEX.md` → flag as VIOLATION
- Pairs of folders with >70% keyword overlap → flag as POSSIBLE DUPLICATE

Violations go into `00-Company/compiled/VAULT_HEALTH.md` for Cem review.

---

## 11. Pending Validation Workflow (NEW v2.0)

**Problem solved:** Wiki pages auto-promoted from raw agent logs become canonical truth without human sign-off. Agents then read them as gospel, act on incorrect context, and compound the error.

### The Rule
The compiler never writes directly to `01-Wiki/[topic]/`. Instead:

1. **Draft**: Promotions from agent logs land in `01-Wiki/_pending/YYYY-MM-DD/[topic].md`.
2. **Digest**: Compiler appends a validation list to `00-Company/compiled/PENDING_APPROVAL.md` after each run.
3. **Notify**: Athena pings Cem on Telegram with the digest link.
4. **Approve**: Cem reviews each pending page (30s-2min each). Options: approve / edit / reject.
5. **Promote**: On approval, Athena (or the compiler in "approved" mode) moves the page from `_pending/` to `01-Wiki/[topic]/` and logs the approval in CHANGE_LOG.

### Agent Behaviour
- Pages in `01-Wiki/[topic]/` = canonical. Agents quote them as truth.
- Pages in `01-Wiki/_pending/` = draft. Agents may *reference* them with the disclaimer "unvalidated as of [date]" but MAY NOT base decisions solely on them.
- Stale pending pages (>7 days unapproved) get flagged in VAULT_HEALTH for Cem.

### Migration
Existing auto-promoted pages (like those listed at the bottom of INDEX.md under "Auto-promoted Wiki Pages") should be moved into `01-Wiki/_pending/` retroactively so Cem can sign off. This is a one-time task for the first compiler run after v2.0 goes live.

---

*This framework exists to prevent agents from operating in blind silos while protecting against accidental overwrites, project sprawl, and unvalidated knowledge. Athena enforces it. The nightly compiler lints it.*