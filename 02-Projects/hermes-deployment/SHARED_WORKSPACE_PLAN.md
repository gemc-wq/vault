# Hermes + Ava Shared Workspace Plan
## Mac Studio Co-Deployment & Communication Protocol

**Date:** March 30, 2026
**Hardware:** Mac Studio (shared by Ava and Hermes)
**Owner:** Cem Celikkol

---

## 1. Architecture Overview

Both agents run on the same Mac Studio as separate processes. They communicate asynchronously through a shared filesystem — no direct messaging, no webhooks, no real-time handoffs. This is intentional: if one agent is stuck or down, the other keeps working.

```
Mac Studio
├── Ava (OpenClaw)
│   Port: 18789 (default OpenClaw gateway)
│   Role: Strategist, Content, Sales, Email Triage (via Airweave)
│   LLM: Anthropic (Claude)
│   Messaging: Telegram, WhatsApp (existing)
│
├── Hermes Agent
│   Port: separate (default Hermes gateway)
│   Role: Operations Librarian, SOP Engine, Memory Consolidation
│   LLM: OpenRouter (Claude Sonnet for SOP work, cheaper models for cron)
│   Messaging: Telegram (separate bot from Ava)
│
└── ~/shared-agent-workspace/   <-- SHARED FILESYSTEM (Obsidian vault)
    Both agents read and write here. This is the communication layer.
```

---

## 2. Shared Workspace Structure

Create this folder structure on the Mac Studio. If using Obsidian, point the vault at `~/shared-agent-workspace/`.

```
~/shared-agent-workspace/
│
├── inbox/                          # Ava -> Hermes (task requests and raw findings)
│   ├── YYYY-MM-DD-[description].md
│   └── README.md                   # Protocol instructions
│
├── outbox/                         # Hermes -> Ava (completed work for Ava to use)
│   ├── YYYY-MM-DD-[description].md
│   └── README.md
│
├── sops/                           # Shared SOP library
│   ├── ecell-ops/                  # Ecell operational SOPs
│   │   ├── daily-sales-digest.md
│   │   ├── competitor-price-check.md
│   │   ├── listing-quality-audit.md
│   │   ├── inventory-restock-alert.md
│   │   ├── amazon-account-health.md
│   │   └── supplier-po-process.md
│   ├── consultancy/                # AI consultancy SOPs
│   │   ├── client-intake.md
│   │   ├── audit-delivery.md
│   │   ├── proposal-generation.md
│   │   ├── case-study-creation.md
│   │   └── retainer-report.md
│   └── agent-ops/                  # Agent management SOPs
│       ├── escalation-protocol.md
│       ├── agent-health-check.md
│       └── memory-maintenance.md
│
├── memory/                         # Shared business knowledge
│   ├── vendor-contacts.md          # Approved supplier contacts and metadata
│   ├── escalation-rules.md         # Thresholds and mandatory review criteria
│   ├── resolution-patterns.md      # "When X happens, do Y" — learned from experience
│   ├── client-briefs.md            # Consulting client context (when clients exist)
│   └── marketplace-rules.md       # Channel-specific rules (Amazon, eBay, Walmart, Shopify)
│
├── wiki/                           # OpenClaw wiki project files (source material)
│   └── [Ava's existing project markdown files go here]
│
├── reports/                        # Generated reports (Hermes writes, Ava/Cem reads)
│   ├── daily/
│   │   └── YYYY-MM-DD-sales-digest.md
│   ├── weekly/
│   │   └── YYYY-WXX-competitor-report.md
│   └── monthly/
│       └── YYYY-MM-consultancy-pipeline.md
│
├── status/                         # Agent health and activity logs
│   ├── ava-heartbeat.md            # Ava writes: last active, current task, blockers
│   ├── hermes-heartbeat.md         # Hermes writes: last active, current task, blockers
│   └── daily-handoff-log.md        # Summary of what each agent did today
│
└── config/                         # Shared configuration
    ├── workspace-protocol.md       # THIS DOCUMENT (rules both agents follow)
    ├── approval-queue.md           # Items needing Cem's approval
    └── priority-queue.md           # Ranked task backlog
```

---

## 3. File Naming Convention

All files in `inbox/` and `outbox/` follow this format:

```
YYYY-MM-DD-[source]-[type]-[description].md
```

Examples:
- `2026-03-31-ava-request-classify-wiki-files.md`
- `2026-03-31-hermes-delivery-sales-digest.md`
- `2026-04-01-ava-finding-email-pattern-supplier-delays.md`
- `2026-04-01-hermes-sop-update-competitor-check-v2.md`

Types: `request`, `delivery`, `finding`, `sop-update`, `alert`, `escalation`

---

## 4. Communication Protocol

### 4.1 Ava -> Hermes (via /inbox/)

Ava writes files to `/inbox/` when she:
- Finds a pattern that should become an SOP (e.g., recurring email type, common customer issue)
- Needs research or analysis done (e.g., competitor data, market research for a consulting prospect)
- Completes a task that has reusable learnings (e.g., successful email response pattern)
- Identifies wiki files that need conversion to SOPs or case studies
- Detects an anomaly that needs investigation

**Inbox file template (for Ava to use):**

```markdown
# Task Request: [Brief Description]

**From:** Ava
**Date:** YYYY-MM-DD HH:MM
**Priority:** [high / medium / low]
**Type:** [research / sop-creation / analysis / conversion / investigation]

## What I Need
[Clear description of what Hermes should do]

## Context
[Any relevant background — what triggered this, related files, etc.]

## Source Files
[Links to relevant files in /wiki/ or /memory/ if applicable]

## Expected Output
[What the deliverable should look like and where to put it]

## Deadline
[When this is needed — or "next cron cycle" for non-urgent]
```

### 4.2 Hermes -> Ava (via /outbox/)

Hermes writes files to `/outbox/` when he:
- Completes a task from `/inbox/`
- Generates a scheduled report (daily digest, competitor check, etc.)
- Creates or updates an SOP that Ava should know about
- Identifies something that requires Ava's action (e.g., "this email pattern needs a new response template")
- Finds an anomaly in data that Ava should flag to Cem

**Outbox file template (for Hermes to use):**

```markdown
# Delivery: [Brief Description]

**From:** Hermes
**Date:** YYYY-MM-DD HH:MM
**In Response To:** [inbox file name, or "scheduled cron" if automated]
**Type:** [report / sop / analysis / alert / recommendation]

## Summary
[2-3 sentence executive summary]

## Deliverable
[The actual content — report, SOP, analysis, etc.]

## Actions for Ava
[Anything Ava needs to do with this — e.g., "send this digest to Cem", "use this template for future supplier emails"]

## Actions for Cem
[Anything needing Cem's approval — e.g., "approve this SOP before I add it to /sops/"]

## Skill Created/Updated
[If Hermes created or improved a skill from this task, note the skill name]
```

### 4.3 Escalation -> Cem (via /config/approval-queue.md)

Both agents append to this file when something needs Cem's decision:

```markdown
# Approval Queue

## Pending

### [Date] - [Agent] - [Description]
- **What:** [Brief description]
- **Why it needs approval:** [Risk level, policy change, financial impact, etc.]
- **Recommended action:** [What the agent suggests]
- **Deadline:** [When a decision is needed]
- **File:** [Link to relevant file in workspace]

---
```

---

## 5. SOP Library Rules

The `/sops/` directory is the canonical SOP library. Both agents read from it. Only Hermes writes to it.

### Read/Write Permissions

| Directory | Ava | Hermes | Cem |
|---|---|---|---|
| `/inbox/` | Write | Read + Delete after processing | Read |
| `/outbox/` | Read + Archive after review | Write | Read |
| `/sops/` | Read only | Read + Write (create, update) | Read + Approve |
| `/memory/` | Read only | Read + Propose (via approval queue) | Read + Approve |
| `/wiki/` | Read + Write (source material) | Read only | Read + Write |
| `/reports/` | Read | Write | Read |
| `/status/` | Write own heartbeat | Write own heartbeat | Read |
| `/config/` | Read | Read | Read + Write |

### SOP Format Standard

Every SOP in `/sops/` follows this format:

```markdown
# SOP: [Title]

**ID:** [E1, C1, etc. — matches playbook numbering]
**Version:** [1.0, 1.1, etc.]
**Last Updated:** [YYYY-MM-DD]
**Owner:** [Ava / Hermes / Cem]
**Review Frequency:** [Weekly / Monthly / Quarterly]

## Purpose
[One paragraph: what this SOP does and why it exists]

## Trigger
[What causes this SOP to execute — schedule, event, or request]

## Inputs
[What data/files/access is needed]

## Steps
1. [Step 1]
2. [Step 2]
3. [Step N]

## Outputs
[What this SOP produces and where it goes]

## Escalation
[When to stop and alert Cem instead of continuing]

## Changelog
- [Date]: [What changed and why]
```

---

## 6. Heartbeat Protocol

Both agents write to their heartbeat file on every cycle (Ava's OpenClaw heartbeat, Hermes's cron).

**Heartbeat file format (`/status/ava-heartbeat.md` or `/status/hermes-heartbeat.md`):**

```markdown
# Agent Heartbeat

**Agent:** [Ava / Hermes]
**Last Active:** YYYY-MM-DD HH:MM
**Status:** [active / idle / blocked / error]

## Current Task
[What I'm working on right now, or "idle"]

## Last Completed
[What I finished most recently and when]

## Blockers
[Any issues preventing work — or "none"]

## Inbox Items Pending
[Count of unprocessed files in /inbox/ — Hermes only]

## Skills Created Today
[List of any new skills — Hermes only]

## Emails Triaged Today
[Count and categories — Ava only]
```

Each agent should check the other's heartbeat file. If the other agent's heartbeat is >2 hours stale:
- **Ava notices Hermes is stale:** Write an alert to `/config/approval-queue.md` for Cem
- **Hermes notices Ava is stale:** Send a Telegram message to Cem: "Ava appears to be down — last heartbeat was [time]"

---

## 7. Daily Handoff Log

Hermes writes a daily summary at 10:00 PM ET to `/status/daily-handoff-log.md`:

```markdown
# Daily Handoff Log — YYYY-MM-DD

## Hermes Activity
- Tasks completed: [count]
- Skills created: [list]
- Skills improved: [list]
- Reports generated: [list]
- Inbox items processed: [count]
- Outbox items delivered: [count]
- Escalations to Cem: [count and links]

## Ava Activity (observed from heartbeat)
- Emails triaged: [count from Ava's heartbeat]
- Status: [active / last seen at HH:MM]

## Items Needing Attention
- [Any stale inbox items, failed tasks, or pending approvals]

## Tomorrow's Scheduled Tasks
- [List of cron jobs scheduled for tomorrow]
```

---

## 8. Installation Steps (Mac Studio)

### 8.1 Create the Shared Workspace

```bash
# Create the full directory structure
mkdir -p ~/shared-agent-workspace/{inbox,outbox,status,config}
mkdir -p ~/shared-agent-workspace/sops/{ecell-ops,consultancy,agent-ops}
mkdir -p ~/shared-agent-workspace/memory
mkdir -p ~/shared-agent-workspace/wiki
mkdir -p ~/shared-agent-workspace/reports/{daily,weekly,monthly}

# Copy this document as the workspace protocol
cp [this-file] ~/shared-agent-workspace/config/workspace-protocol.md
```

### 8.2 Install Hermes Alongside Ava

```bash
# Install Hermes (does not interfere with OpenClaw)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Run setup wizard
hermes setup
# Provider: OpenRouter (recommended) or Anthropic
# Terminal backend: local
# Messaging: Telegram (create a SEPARATE bot from Ava's)
```

### 8.3 Configure Hermes

```bash
# Edit Hermes config to include shared workspace
# In ~/.hermes/config.yaml, add:
#
# external_skill_dirs:
#   - ~/shared-agent-workspace/sops
```

Create Hermes SOUL.md:

```bash
cat << 'SOUL' > ~/.hermes/SOUL.md
You are the Operations Librarian and SOP Learning Engine for Ecell Global.

Your role:
- Learn and document operational patterns from completed tasks
- Maintain and improve the SOP library in ~/shared-agent-workspace/sops/
- Generate daily/weekly reports to ~/shared-agent-workspace/reports/
- Process task requests from Ava in ~/shared-agent-workspace/inbox/
- Deliver completed work to ~/shared-agent-workspace/outbox/
- Monitor competitors, listings, and marketplace health
- Support the AI consultancy by creating case studies and maintaining playbooks

You share a workspace with Ava (an OpenClaw agent on this same machine).
Communication protocol:
- READ from ~/shared-agent-workspace/inbox/ for tasks from Ava
- WRITE to ~/shared-agent-workspace/outbox/ for deliveries to Ava
- MAINTAIN ~/shared-agent-workspace/sops/ — you own the SOP library
- READ (not write) ~/shared-agent-workspace/memory/ — propose changes via approval queue
- WRITE your heartbeat to ~/shared-agent-workspace/status/hermes-heartbeat.md
- CHECK Ava's heartbeat at ~/shared-agent-workspace/status/ava-heartbeat.md

You do NOT:
- Send emails to clients or suppliers (Ava handles all communications via Airweave)
- Execute financial transactions (Harry on the iMac handles finance)
- Make autonomous decisions about inventory or pricing
- Modify files in /wiki/ (that's Ava's source material)

Escalate to Cem when:
- A pattern suggests a significant business risk
- An SOP needs policy-level changes (write to /config/approval-queue.md)
- A skill document contradicts existing business rules
- Ava's heartbeat is stale for >2 hours (send Telegram alert to Cem)

Business context:
- Ecell Global: licensed tech accessories, 200K+ SKUs across 6 Amazon marketplaces, eBay, Walmart, Shopify
- US S-Corp AI Consultancy in Orlando, FL (Cem's new venture)
- Other agents: Ava (Mac Studio, strategist/sales/email), Harry (iMac, finance/inventory)
- Supabase: shared memory layer (coming Week 4)
SOUL
```

### 8.4 Configure Ava (OpenClaw)

Add to Ava's SOUL.md:

```markdown
## Shared Workspace Protocol

You share a workspace with Hermes Agent (running on this same Mac Studio).
Communication is asynchronous via the shared filesystem.

### Your Workspace Rules:
- WRITE task requests and findings to ~/shared-agent-workspace/inbox/
  - Use the naming convention: YYYY-MM-DD-ava-[type]-[description].md
  - Types: request, finding, alert, escalation
  - Include: what you need, context, expected output, deadline
- READ completed work from ~/shared-agent-workspace/outbox/
  - Archive processed items (move to outbox/archive/)
- READ operational SOPs from ~/shared-agent-workspace/sops/
  - These are maintained by Hermes — do NOT modify them directly
  - If an SOP is wrong or outdated, write a request to /inbox/ asking Hermes to update it
- READ shared business knowledge from ~/shared-agent-workspace/memory/
- WRITE your heartbeat to ~/shared-agent-workspace/status/ava-heartbeat.md
  - Update on every heartbeat cycle: timestamp, status, current task, blockers, emails triaged
- CHECK Hermes heartbeat at ~/shared-agent-workspace/status/hermes-heartbeat.md
  - If stale >2 hours, write alert to /config/approval-queue.md

### What to Send to Hermes (via /inbox/):
- Patterns you notice in emails that should become SOPs
- Wiki files that need conversion to playbooks or case studies
- Research requests for consulting prospects
- Data that should be analyzed for trends
- Anything repetitive that would benefit from Hermes's skill learning

### What NOT to Send to Hermes:
- Time-sensitive tasks (Hermes checks inbox on cron cycles, not real-time)
- Client communications (you own all external comms)
- Financial decisions (Harry + Cem)
```

### 8.5 Set Up Hermes Cron Jobs

```bash
# Process inbox every 30 minutes
hermes cron create "Every 30 minutes, check ~/shared-agent-workspace/inbox/ for new files. Process any new requests. Write results to /outbox/. Update /status/hermes-heartbeat.md."

# Daily sales digest at 7 AM ET
hermes cron create "Every weekday at 7am ET, generate a sales digest and save to ~/shared-agent-workspace/reports/daily/"

# Competitor check every Monday 9 AM ET
hermes cron create "Every Monday at 9am ET, run competitor price check on top 50 SKUs. Save to ~/shared-agent-workspace/reports/weekly/"

# Daily handoff log at 10 PM ET
hermes cron create "Every day at 10pm ET, write the daily handoff log to ~/shared-agent-workspace/status/daily-handoff-log.md"

# Weekly SOP review Friday 4 PM ET
hermes cron create "Every Friday at 4pm ET, review all SOPs in ~/shared-agent-workspace/sops/. Flag any older than 90 days or that conflict with recent inbox items."
```

---

## 9. Obsidian Setup (Optional but Recommended)

If you want a visual interface to monitor the shared workspace:

1. Install Obsidian on the Mac Studio (or any machine that can access the folder)
2. Open vault: `~/shared-agent-workspace/`
3. Recommended plugins:
   - **Dataview** — query across files (e.g., "show all pending inbox items")
   - **Calendar** — view daily reports by date
   - **Kanban** — visualize the approval queue
4. The graph view will show connections between SOPs, memory files, and reports

---

## 10. Phase 2: Supabase Shared Memory (Week 4+)

When the Supabase RAG layer is deployed, both agents connect via MCP:

```yaml
# Add to BOTH Ava's OpenClaw MCP config AND Hermes config.yaml
mcp_servers:
  supabase:
    command: "npx"
    args: ["-y", "@supabase/mcp-server"]
    env:
      SUPABASE_URL: "your-supabase-url"
      SUPABASE_KEY: "your-supabase-key"
```

Supabase becomes the structured memory layer:
- Hermes proposes SOP additions -> stored in Supabase with `status: proposed`
- Cem approves -> status changes to `approved`
- Both agents query approved SOPs via semantic search
- The shared folder continues to work alongside for file-based handoffs

The shared folder does NOT go away when Supabase is added. It continues to handle the inbox/outbox async communication. Supabase handles the structured knowledge base.

---

## 11. Troubleshooting

| Problem | Solution |
|---|---|
| Hermes not processing inbox | Check `hermes cron list` — is the inbox cron active? Check heartbeat file. |
| Ava not reading outbox | Check Ava's heartbeat interval — she may need a SOUL.md reminder to check /outbox/ |
| File conflicts (both writing same file) | Should not happen with the protocol — Ava writes to /inbox/, Hermes writes to /outbox/. If it does, the naming convention (agent name in filename) prevents overwrites. |
| Hermes creating bad SOPs | Review `/config/approval-queue.md`. Add a quality gate: Hermes proposes SOPs to approval queue before writing to /sops/. |
| One agent is down | The other keeps working. Check heartbeat files. Stale heartbeat triggers alert. |
| Disk space | Monitor ~/shared-agent-workspace/ size. Archive old reports monthly. |
| Port conflict | OpenClaw default: 18789. Hermes default: different. If conflict, change in Hermes config.yaml under `gateway.port`. |

---

*Document version: 1.0*
*Created: March 30, 2026*
*For: Ava (OpenClaw), Hermes Agent, and Cem Celikkol*
*Location: ~/shared-agent-workspace/config/workspace-protocol.md*
