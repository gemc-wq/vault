# Vault Guide for Ava
**Purpose:** How to read, navigate, and contribute to the shared Ecell Global Vault.
**Updated:** 2026-04-10 | **By:** Athena

---

## Memory Hierarchy (3 Layers)

Every agent operates with three layers of memory. Understand which layer you're working in.

| Layer | What | Where | Lifespan |
|-------|------|-------|----------|
| **L1 — Local Workspace** | Identity files (SOUL.md, MEMORY.md, AGENTS.md, TASKS.md, TOOLS.md) | `/Users/openclaw/.openclaw/workspace/` | Read-only bootstrap — loaded at session start |
| **L2 — Daily Logs** | Session-specific notes, working context | `workspace/memory/YYYY-MM-DD.md` | Ephemeral — one per day, not shared |
| **L3 — Vault** | Canonical reference, source of truth, shared across ALL agents | `/Users/openclaw/Vault/` | Persistent — survives sessions, shared |

### Rules
- **Read Vault first** for canonical context (role definitions, business memory, operational procedures)
- **Write to Vault** for anything that needs to survive across sessions and be shared
- **Use local workspace** for working files and temporary project context
- **Sync back to Vault** at end of every session — key decisions, learnings, updated context

**The Vault is authoritative.** When someone says "check the Vault," they mean the source of truth — not a secondary reference.

---

## What is the Vault?

The Vault is the company's Layer 3 persistent memory — the organizational brain. It contains all project documentation, wiki knowledge, agent configs, and compiled reports. All agents share it.

**Location:** `/Users/openclaw/Vault/`

---

## Vault Structure

```
/Users/openclaw/Vault/
├── 00-Company/           ← Company-wide docs, skills, compiled reports
│   ├── compiled/         ← Auto-generated reports (task sheet, cron schedule, etc.)
│   ├── contacts/         ← Email tracking, staff contacts
│   └── skills/           ← 6 skill files (Creative, Sales, Ops, Marketing, Finance, Intel)
│
├── 01-Wiki/              ← Knowledge base — searchable reference docs
│   ├── 01-corporate/     ← Company structure, infrastructure, network
│   ├── 02-licensing/     ← License agreements, brand guidelines
│   ├── 03-marketplace/   ← Amazon, Walmart, Shopify, OnBuy, etc.
│   ├── 10-production/    ← Print pipeline, IREN, manufacturing
│   ├── 20-creative/      ← Design standards, PSD specs, image guidelines
│   ├── 30-finance/       ← Xero, royalties, COGS, procurement
│   ├── 35-iren-dreco/    ← ListingForge, IREN modernization, DRECO replacement
│   └── ...               ← Other topic folders
│
├── 02-Projects/          ← Active project folders (one per project)
│   ├── one-piece/        ← One Piece launch
│   ├── listing-forge/    ← ListingForge (DRECO replacement)
│   ├── iren-dreco/       ← IREN modernization + pipeline vision
│   ├── fulfillment-portal/
│   ├── finance-ops/
│   ├── infrastructure/   ← Tailscale, PH data bridge, BigQuery
│   ├── walmart/
│   ├── marketing/
│   └── ...               ← 40+ project folders
│
├── 03-Agents/            ← Agent-specific files
│   ├── Ava/              ← YOUR folder — memory, context, guides
│   │   └── handoffs/     ← Incoming work from other agents (check at session start)
│   ├── JayMark/          ← Jay Mark's service agreement, instructions
│   ├── Harry/            ← Harry's daily logs, finance specs
│   └── Hermes/           ← Hermes's SOPs, analytics, build logs
│
└── 04-Shared/            ← CROSS-AGENT WORKSPACE (NEW — Apr 14)
    ├── active/           ← In-progress shared work (multiple agents contributing)
    ├── handoffs/         ← Completed handoffs awaiting pickup
    └── decisions/        ← Cross-agent decisions (logged by Athena)
```

### Collaboration Rules
See `~/Vault/00-Company/AGENT_COLLABORATION.md` for the full framework:
- Agents deposit work into each other's `handoffs/` folders (never edit each other's files)
- Shared work goes in `04-Shared/active/[task-name]/` with separate files per agent
- Athena synthesises shared work into final deliverables

---

## Key Files You Should Know

| File | Path | Purpose |
|------|------|---------|
| **Task Sheet** | `00-Company/compiled/TASK_SHEET.md` | Centralized task tracker — check at session start |
| **Cron Schedule** | `00-Company/compiled/CRON_SCHEDULE.md` | All 14 cron jobs, times, engines |
| **Email Tracking** | `00-Company/contacts/EMAIL_TRACKING.md` | Staff contacts, email monitoring workflow |
| **Your Business Context** | `03-Agents/Ava/MEMORY_BUSINESS_CONTEXT.md` | 53KB curated company knowledge |
| **Pipeline Vision** | `02-Projects/iren-dreco/PIPELINE_VISION.md` | End-to-end pipeline: ideation → marketing |
| **ListingForge One-Pager** | `02-Projects/iren-dreco/LISTINGFORGE_ONE_PAGER.md` | Concise project summary |
| **Company Overview** | `00-Company/compiled/COMPANY_OVERVIEW.md` | Auto-compiled company snapshot |

---

## How to Read Vault Files

You have access through the OpenClaw workspace tools. To read a vault file:

1. **Direct path:** Read files using their full path starting with `/Users/openclaw/Vault/`
2. **Search:** Search the vault for keywords to find relevant docs
3. **List:** Browse directory contents to discover files

**Important:** The vault is READ-ONLY for agents. You can read anything, but writes go through Athena or the vault compiler.

---

## How to Contribute

Since you can't write directly to the vault, here's how to contribute:

### Option 1: Through Athena
Ask Athena (via OpenClaw) to save content to the vault. Example:
> "Athena, please save this competitive analysis to 02-Projects/walmart/COMPETITIVE_ANALYSIS.md"

### Option 2: Through Your Workspace
Write to your own workspace files. The vault compiler (nightly, Gemma 4) picks up relevant content and indexes it.

Your workspace: `/Users/openclaw/.openclaw/workspace/`
- `MEMORY.md` — your session notes
- `TASKS.md` — your task list
- `projects/` — your project working files
- `wiki/` — your wiki contributions

### Option 3: Tag for Filing
When you produce a report or analysis, tag it with:
```
[VAULT-FILE: 02-Projects/walmart/analysis.md]
```
Athena will pick this up during email/session scans and file it.

---

## Filing Conventions

### Project Files (02-Projects/)
- One folder per project
- Always include: README or brief, current status, next milestone
- Name files descriptively: `HANDOFF_LISTINGFORGE.md`, `PIPELINE_VISION.md`

### Wiki Files (01-Wiki/)
- Numbered topic folders (01-corporate, 02-licensing, etc.)
- Reference docs that don't change often
- Copy project docs here when they become stable reference material

### Compiled Reports (00-Company/compiled/)
- Auto-generated by Gemma 4 nightly
- Don't edit these directly — they get overwritten
- Source data comes from vault content + agent outputs

---

## Your Responsibilities

As CPSO + Creative Director, you own the organizational brain:

1. **Review** project docs for accuracy and completeness
2. **Flag** outdated information to Athena for updates
3. **Contribute** strategic analyses, competitive research, and planning docs
4. **Reference** vault context before making recommendations
5. **Track** your assigned tasks via the Task Sheet

---

## Quick Start Checklist

Every session, do this:
- [ ] Read `00-Company/compiled/TASK_SHEET.md` — check your assigned tasks
- [ ] Check your folder `03-Agents/Ava/` for any new instructions
- [ ] Reference relevant project files before starting work
- [ ] Tag outputs for vault filing when producing reports

---

*This guide is your map to the company's memory. Use it. The more you reference the vault, the smarter your recommendations become.*
