# VAULT_OPERATING_SYSTEM.md

## Purpose
Define how the 4-layer memory system works across built-in memory, injected operating files, primary agent workspaces, the vault, the wiki, and session-search recall.

---

# 1. Memory Stack

## Layer 1 — Built-in Memory
- tiny compact facts and pointers
- automatically injected into every prompt
- examples: name, key paths, short persistent facts, critical pointers
- should remain minimal and high value

## Layer 2 — Injected Operating Files
These are automatically injected every session and define how the agent behaves.

Examples include:
- `AGENTS.md`
- `SOUL.md`
- related core operating files injected by the runtime

Purpose:
- operating instructions
- identity/personality
- hard rules
- mandatory logging behavior

## Layer 3 — Obsidian Vault
The vault is the workhorse continuity and reference layer.

Characteristics:
- not auto-injected
- read on session start, after compaction, and during work when details are needed
- written during active work as checkpoints and durable continuity

Use it for:
- business continuity
- mission / north-star docs
- blueprints
- handoffs
- reference material
- project continuity summaries
- brain dumps / raw note intake
- agent workspace continuity notes

### Rule
The vault is not the primary memory/tools layer and not the canonical wiki.

## Layer 4 — Session Search
- searchable archive of prior sessions/conversations
- not manually written as part of normal workflow
- used as fallback/last-resort recall when prior work is referenced or cross-session context is needed
- useful for recovery when something was not distilled properly into other layers

## Important workspace rule
Primary agent operational files such as `TOOLS.md`, `MEMORY.md`, and daily memory logs remain in the standard OpenClaw / Hermes workspace infrastructure.
They are not moved into the vault.

**Exception: ZEUS/ATHENA** — ZEUS's primary workspace is `~/zeus-agent/data/` (local to Mac Studio), not the Obsidian vault. ZEUS reads the vault (READ-ONLY) and writes to its own local data directory. See Layer 3b below.

Use it for:
- business continuity
- mission / north-star docs
- blueprints
- handoffs
- reference material
- project continuity summaries
- brain dumps / raw note intake
- agent workspace continuity notes

### Rule
The vault is not the primary memory/tools layer and not the canonical wiki.

---

# 2. Canonical Routing Rules

## Wiki
Use `wiki/` for:
- project truth
- SOPs
- implementation plans
- architecture docs
- finalized business knowledge
- operational documentation intended as source of truth

## Primary Agent Workspace
Use primary workspace files for:
- `TOOLS.md` = agent operational notes, environment details, access paths, local conventions
- `MEMORY.md` = durable long-term agent memory
- `memory/YYYY-MM-DD.md` = daily chronological logs
- active agent execution context

## Vault
Use `vault/` for:
- reference layer
- continuity summaries
- handoffs
- raw intake / brain dumps
- mission / blueprint / north-star context
- cross-agent reference materials
- agent workspace continuity notes

---

# 3. Core Principle

## The vault does not replace the workspace
The vault supports continuity.
The workspace remains the agent's operational home.
The wiki remains the business source of truth.

### In plain language
- workspace = where the agent thinks and remembers operationally
- wiki = where the business truth lives
- vault = where continuity, reference, and raw-to-refined context live

---

# 4. Proposed Vault Structure

```text
vault/
  00-inbox/
    cem-brain-dumps/
    quick-captures/
  01-daily/
  10-projects/
  20-areas/
  30-reference/
    mission/
    blueprints/
    north-star/
  40-ai-workspaces/
    ava/
    harry/
    hermes/
    sessions/
    handoffs/
  90-archive/
```

---

# 5. How Each Layer Should Behave

## Inbox (`vault/00-inbox/`)
Purpose:
- capture raw human ideas before they are processed

Examples:
- brain dumps
- rough thoughts
- meeting snippets
- voice transcript dumps
- unstructured reminders

### Rule
Inbox notes are not canonical truth.
They must be processed into:
- wiki updates
- workspace memory updates
- handoffs
- project summaries

## Daily (`vault/01-daily/`)
Purpose:
- continuity bridge between human and agent activity
- optional reference mirror to primary daily memory logs

### Rule
Primary daily logs still belong in the agent workspace.
Vault daily notes may summarize or mirror key continuity context.

## Projects (`vault/10-projects/`)
Purpose:
- project continuity summaries
- project entry points
- quick-start readmes

### Rule
Project truth still lives in `wiki/`.
Vault project notes should summarize and link back to canonical wiki docs.

## Areas (`vault/20-areas/`)
Purpose:
- ongoing business functions and evergreen domains

Examples:
- licensing
- operations
- production
- finance
- growth

## Reference (`vault/30-reference/`)
Purpose:
- mission
- north star
- blueprint
- evergreen strategy context

## AI Workspaces (`vault/40-ai-workspaces/`)
Purpose:
- continuity notes for Ava/Harry/Hermes/ZEUS
- session summaries
- drafts
- handoffs

### Rule
These are not replacements for each agent's primary `MEMORY.md` / `TOOLS.md`.
They are continuity/reference layers only.

### ZEUS/ATHENA workspace (`vault/40-ai-workspaces/zeus/`)
ZEUS has a unique hybrid model:
- **Vault partition**: `vault/40-ai-workspaces/zeus/` — continuity notes, handoff references (future: write access)
- **Local primary workspace**: `~/zeus-agent/data/` — this is where ZEUS actually writes:
  - `working-context.md` — current task state (overwritten each checkpoint)
  - `daily/YYYY-MM-DD.md` — daily chronological logs
  - `mistakes.md` — corrections and lessons learned
  - `decisions-log.md` — decisions with reasoning + optional Codex verdicts
  - `memory.db` — SQLite session archive (Layer 4)

---

# 6. Agent Rules

## Ava
Ava's primary workspace remains authoritative for:
- `TOOLS.md`
- `MEMORY.md`
- `memory/YYYY-MM-DD.md`

Ava may use the vault to:
- store reference continuity notes
- maintain handoffs
- store project summaries and intake processing notes

## Harry
Harry's primary workspace remains authoritative for:
- `TOOLS.md`
- `MEMORY.md`
- daily memory logs

Harry may use the vault to:
- store continuity notes
- receive/send handoffs
- reference blueprint material

## Hermes
Hermes's primary workspace remains authoritative for:
- `TOOLS.md`
- `MEMORY.md`
- daily memory logs

Hermes may use the vault to:
- store continuity notes
- receive/send handoffs
- reference shared context

## ZEUS / ATHENA
ZEUS is the master orchestrator (Claude Agent SDK, Telegram bot, Mac Studio).

**Primary workspace**: `~/zeus-agent/data/` (NOT the vault)
- `working-context.md` — live task state
- `daily/YYYY-MM-DD.md` — daily logs
- `mistakes.md` — error corrections
- `decisions-log.md` — decision audit trail
- `memory.db` — SQLite session archive (Layer 4)

**Vault access**: READ-ONLY
- Reads CLAUDE.md, TASKS.md, STRATEGY.md, MISSION.md on session start
- Can read any vault file on demand via `vault_read_file`
- Can search vault via `vault_search`
- Does NOT write to the shared vault (prevents corruption from unattended bot)

**MCP interface** (`memory_mcp.py` v2.1):
| Tool | Layer | Direction | Purpose |
|------|-------|-----------|---------|
| `vault_session_start` | L3 | READ | Load key vault files + local context |
| `vault_read_file` | L3 | READ | Read any vault file by path |
| `vault_search` | L3 | READ | Grep vault for keyword matches |
| `vault_list_directory` | L3 | READ | List vault directory contents |
| `local_checkpoint` | L3b | WRITE | Save working-context (every 3-5 tool calls) |
| `local_append_daily_log` | L3b | WRITE | Append to today's daily log |
| `local_session_end` | L3b | WRITE | Flush session summary, clear working-context |
| `local_log_mistake` | L3b | WRITE | Log corrections and lessons |
| `session_log` | L4 | WRITE | Archive conversation to SQLite |
| `session_search` | L4 | READ | Search past sessions |
| `store_decision` | L3b+L4 | WRITE | Log decision to both local file + SQLite |

**Session lifecycle:**
```
Session start → vault_session_start (reads vault + local state)
Working       → local_checkpoint every 3-5 tool calls
Task done     → local_append_daily_log + local_checkpoint
Session end   → local_session_end (flush to daily log, clear context)
```

**Future**: ZEUS will gain vault write access to `vault/40-ai-workspaces/zeus/` once the Agent-Zeus partition is created.

---

# 7. Saving Workflow

## When new information appears
Ask:
1. Is this canonical business/project truth?
2. Is this agent operational memory?
3. Is this raw intake / continuity / reference?

### If yes:
- canonical truth -> `wiki/`
- agent operational memory -> primary workspace `TOOLS.md` / `MEMORY.md` / daily log
- raw intake / continuity / reference -> `vault/`

---

# 8. Brain Dump Processing SOP

## Input
Cem can add:
- raw notes
- strategic thoughts
- rough ideas
- reminders
- meeting summaries
- transcripts

## Landing zone
- `vault/00-inbox/cem-brain-dumps/`

## Processing flow
1. capture raw note
2. identify relevant project/domain
3. extract durable operational facts
4. update agent workspace memory if needed
5. update wiki if project truth changed
6. create handoff or continuity summary if needed
7. archive or tag processed raw note

---

# 9. Daily Memory Logging Rule

All agents must maintain daily memory logs in their **primary workspace**, not in the vault.

The vault may contain continuity summaries or mirrored summaries, but the official operational daily logging system remains in the agent workspace infrastructure.

---

# 10. Anti-Patterns

Do not:
- move `TOOLS.md` or `MEMORY.md` into the vault
- let vault become a second competing wiki
- store raw brain dumps as if they are canonical truth
- allow uncontrolled agent edits across all layers
- duplicate the same project truth in multiple places without a clear canonical owner

---

# 11. Implementation Order

1. finalize this operating system doc
2. correct all architecture references so `TOOLS.md` / `MEMORY.md` stay in primary workspaces
3. create inbox rules for Cem brain dumps
4. create daily note template
5. create project continuity template
6. restructure existing vault content into the new model
7. wire agent rules so primary workspace files reference vault + wiki behavior explicitly

---

# 12. Final Rule

If something matters:
- write it down
- put it in the correct layer
- keep the wiki authoritative
- keep primary workspace memory real
- keep vault useful, clean, and continuity-focused
