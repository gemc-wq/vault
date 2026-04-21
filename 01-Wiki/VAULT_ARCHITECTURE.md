# VAULT_ARCHITECTURE.md

## Purpose
The Obsidian Vault is the **3rd layer of memory** in the 4-layer system.

Memory model:
1. **Built-in memory** — tiny auto-injected compact facts and pointers
2. **Injected operating files** — `AGENTS.md`, `SOUL.md`, and related injected operating instructions
3. **Vault reference/continuity layer** — long-lived reference material for business continuity, historical context, mission, blueprints, and agent workspaces
4. **Session search** — searchable archive recall for past work when needed

The vault is a **reference layer**, not the primary system of record for operational project status.
The **wiki remains the single source of truth** for business knowledge and project documentation.

---

## Structural Rules

### 1. Wiki stays separate
- `wiki/` remains the canonical knowledge base
- project specs, SOPs, architecture, process docs, and operational knowledge belong in the wiki
- avoid duplicating wiki content inside the vault unless explicitly creating reference mirrors

### 2. Vault role
The vault should hold:
- north-star materials
- mission statements
- blueprint/reference material
- agent workspace context
- continuity material that helps survive OpenClaw resets, upgrades, or memory loss
- handoff notes across agents

The vault should **not** become a second competing wiki.

### 3. Agent workspace split
Create separate vault workspace areas for:
- **Ava Workspace**
- **Harry Workspace**
- **Hermes Workspace**
- **ZEUS/ATHENA Workspace**
- **Shared Workspace / Handoffs**

### 4. Daily memory logging is mandatory
For Ava, Harry, and Hermes:
- save daily logs every day in their primary agent workspace memory system
- update project state when meaningful work happens
- log decisions, corrections, blockers, and carry-forwards
- do not rely on chat memory alone

---

## Recommended Vault Structure

```text
Vault/
  00-shared/
    handoffs/
    mission/
    blueprints/
    reference/
  01-ava/
    workspace/
    memory/
    tools/
    rules/
  02-harry/
    workspace/
    memory/
    tools/
    rules/
  03-hermes/
    workspace/
    memory/
    tools/
    rules/
  04-zeus/
    workspace/
    continuity/
    rules/
```

### Shared layer
**`00-shared/`** contains:
- mission statements
- north star docs
- company blueprint
- shared reference materials
- inter-agent handoffs

### Agent layers
Each vault agent area should contain:
- `workspace/` — reference notes and working continuity context relevant to that agent
- `rules/` — vault-facing operating rules, continuity rules, and handoff conventions

Important:
- the vault is **not** where the agent's primary `MEMORY.md` and `TOOLS.md` live
- each agent's core `MEMORY.md`, `TOOLS.md`, and daily memory logs remain in that agent's primary OpenClaw/Hermes workspace infrastructure
- the vault is a third-layer reference and continuity system only

---

## Workspace-side Rules

### Ava
Ava should maintain and update in her primary workspace:
- `SOUL.md`
- `USER.md`
- `TOOLS.md`
- `MEMORY.md`
- `memory/YYYY-MM-DD.md`
- project docs in `wiki/`

The vault may contain Ava continuity/reference material, but not her primary agent memory system.

### Harry
Harry should maintain in his own primary workspace infrastructure:
- `SOUL.md`
- `TOOLS.md`
- `MEMORY.md`
- daily memory logs
- project updates written into the correct wiki destinations

The vault may contain Harry continuity/reference material, but not his primary agent memory system.

### Hermes
Hermes should maintain in his own primary workspace infrastructure:
- `SOUL.md`
- `TOOLS.md`
- `MEMORY.md`
- daily memory logs
- project updates/handoffs captured durably

The vault may contain Hermes continuity/reference material, but not his primary agent memory system.

### ZEUS / ATHENA
ZEUS is the master orchestrator agent (Claude Agent SDK on Mac Studio, ~/zeus-agent/).
ZEUS has a **hybrid memory model** distinct from the other agents:

- **Vault access: READ-ONLY** — ZEUS reads CLAUDE.md, TASKS.md, STRATEGY.md, MISSION.md, and any vault file on demand, but does NOT write to the shared Obsidian vault. This prevents file corruption risk from a Telegram-driven bot.
- **Local workspace writes** — ZEUS writes to `~/zeus-agent/data/` (its private Layer 3b):
  - `data/working-context.md` — active task context (overwritten on checkpoint)
  - `data/mistakes.md` — logged corrections and lessons
  - `data/decisions-log.md` — decision history with optional Codex verdicts
  - `data/daily/YYYY-MM-DD.md` — daily chronological logs
- **Session archive (Layer 4)** — SQLite at `data/memory.db` for cross-session search
- **MCP tools** — memory_mcp.py exposes all 4 layers via MCP:
  - `vault_session_start` — reads key vault files + local context on session start
  - `vault_read_file`, `vault_search`, `vault_list_directory` — read vault
  - `local_checkpoint`, `local_append_daily_log`, `local_session_end`, `local_log_mistake` — write to local data/
  - `session_log`, `session_search`, `store_decision` — SQLite Layer 4

**Session flow:**
1. Session starts → `vault_session_start` (reads vault + local working-context + today's log)
2. Working → `local_checkpoint` every 3-5 tool calls
3. Task done → `local_append_daily_log` + update working-context
4. Session ends → `local_session_end` (flush to daily log, clear working-context)

**Future**: When Agent-Zeus/ folder is created in the vault with proper write permissions, ZEUS will gain write access to its own vault partition (like Agent-Shared/ model).

---

## Saving Rules

### Always save
When any agent learns something durable, save it to one of:
- wiki project doc
- `TOOLS.md`
- `MEMORY.md`
- daily memory log
- vault reference/handoff area

### Do not rely on chat-only memory
OpenClaw updates, compaction, tool failures, and model changes can lose context.
If it matters, write it down.

### Routing rule
- **Business knowledge / SOP / specs / project truth** → `wiki/`
- **Agent operational notes / environment info / local access details** → primary-workspace `TOOLS.md`
- **Long-term distilled memory** → primary-workspace `MEMORY.md`
- **Raw chronological history** → primary-workspace `memory/YYYY-MM-DD.md`
- **Cross-agent continuity / business continuity / blueprint references** → Vault

---

## Immediate Implementation Plan
1. Create vault-aligned top-level folders in workspace for mirrored structure planning.
2. Create explicit agent rules docs for Ava/Harry/Hermes.
3. Add memory logging rules for all agents.
4. Keep wiki separate and authoritative.
5. Use the vault as resilience/reference, not as the execution system of record.

---

## Cem directive captured — 2026-04-02
- The vault is the **3rd layer of memory**.
- Use it as reference material for business continuity.
- Keep **wiki separate** as the single source of truth.
- Restructure around:
  - Ava workspace
  - Harry workspace
  - Hermes workspace
  - shared workspace for handoffs
- Create rules for how each agent's primary `MEMORY.md` and `TOOLS.md` reference the vault and wiki layers.
- Ensure all agents save daily memory logs and update projects from their primary workspace infrastructure.
