# Claude Code Nightly Compiler — Technical Spec
**Created:** 2026-04-19 | **Status:** SPEC — ready to implement
**Replaces:** Gemma 4 local model compiler (currently broken per BLOCKERS.md)
**Owner:** Athena (prompt + logic) | Cem (infra install on ZEUS)

---

## TL;DR

A headless Claude Code process runs nightly at 02:00 ET under launchd on ZEUS (Mac Studio). It reads agent memory logs and project folders via the Obsidian MCP, filters and promotes knowledge into `01-Wiki/_pending/`, rebuilds all `00-Company/compiled/` outputs, lints vault health, and pings Cem on Telegram with a morning digest. Uses Cem's Claude Max subscription — effectively $0 within rate limits. Haiku 4.5 API fallback if limits hit (~$15-30/month).

---

## Why Claude Code (Not Something Else)

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Gemma 4 local (current) | $0 | Unreliable, weak reasoning, currently broken | ❌ Replace |
| N8N + raw API calls | Visual, familiar | Brittle, middleware layer we're removing | ❌ Against architecture |
| Claude Agent SDK (Node/Python) | Full control, production-grade | More setup, requires API key management | 🔸 Fallback option |
| **Claude Code CLI (headless)** | **Uses Max sub, native Obsidian MCP, fast to ship** | **Subject to subscription rate limits** | **✅ Primary choice** |
| Claude Code Routines (cloud) | Zero infra, Anthropic hosts | Research preview, less control, data leaves premises | 🔸 Future consideration |

**Decision:** Start with Claude Code CLI headless. If rate limits bite, migrate to Agent SDK + Haiku 4.5 API.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ZEUS (Mac Studio)                           │
│                                                                 │
│  launchd → /usr/local/bin/vault-compile.sh (02:00 ET)          │
│     │                                                           │
│     └─▶ claude -p "@/Users/openclaw/Vault/00-Company/skills/    │
│               compiler/PROMPT.md" \                            │
│             --allowed-tools "mcp__obsidian__*,Bash(git:*)" \    │
│             --max-turns 100 \                                  │
│             --output-format stream-json \                      │
│             --model sonnet-4-6 \                               │
│             > /var/log/vault-compile/$(date +%F).log           │
│                                                                 │
│  Obsidian MCP server (local REST API, port 27123)              │
│     └─▶ reads/writes /Users/openclaw/Vault/                   │
│                                                                 │
│  Post-run hook:                                                │
│     └─▶ telegram-send "@cem compile done: N pending"          │
└─────────────────────────────────────────────────────────────┘
```

---

## Run Phases

### Phase 0 — Prep (30s)
- Git commit vault state (pre-compile snapshot) → `git commit -am "pre-compile $(date -Iseconds)"`
- Read `00-Company/compiled/CHANGE_LOG.md` to find last successful run timestamp
- Read `00-Company/AGENT_COLLABORATION.md` and `00-Company/AGENT_ROSTER.md` for current rules/roster

### Phase 1 — Gather (2-5 min)
- List new/modified files in `03-Agents/*/memory/` since last run
- List new/modified files in `02-Projects/*/` since last run
- Read each modified file
- Build in-memory map: `{agent, date, decisions[], blockers[], corrections[], facts[], questions[]}`

### Phase 2 — Filter & Promote to Pending (5-10 min)
For each raw log entry:
- **Classify** — is this a: decision / process rule / fact / blocker / question / noise?
- **Noise** (chit-chat, session preamble, TODOs already on TASK_SHEET) → skip
- **Decision / rule / fact** → identify target wiki topic, draft update, write to `01-Wiki/_pending/YYYY-MM-DD/[topic]/[slug].md`
- **Blocker** → collect for Phase 3 BLOCKERS rebuild
- **Question** → collect for PENDING_APPROVAL digest ("Hermes asked X, no answer in vault")
- **Correction** (agent was corrected by Cem) → collect for the agent's `corrections.md` update

Pending files use frontmatter:
```yaml
---
source_agent: Hermes
source_log: 03-Agents/Hermes/memory/2026-04-18.md
source_turn: 14
confidence: medium | high
topic_target: 01-Wiki/11-product-intelligence/amazon-reporting-process.md
action: create | update | append
created_by_compile: 2026-04-19T02:15:00Z
---
```

### Phase 3 — Rebuild Compiled Outputs (5 min)
Overwrite with fresh content (staleness is the whole problem):

- **`00-Company/compiled/PROJECT_BOARD.md`** — scan `02-Projects/_INDEX.md` + each project's README frontmatter. Group by status. Flag projects with no update in 14+ days.
- **`00-Company/compiled/BLOCKERS.md`** — aggregate all blockers mentioned in recent logs + any project with status `🔴`.
- **`00-Company/compiled/TASK_SHEET.md`** — **preserve existing tasks** (never delete), mark newly-completed ones (per agent logs saying "done X"), add newly-identified tasks under appropriate pillar. Diff-write, not full-rewrite, to preserve Cem's edits.
- **`00-Company/compiled/VAULT_HEALTH.md`** — file counts, oversized files (>100KB), stale files (>30d in active projects), duplicate filenames, duplicate-folder candidates (>70% name overlap), violations of §10 Project Intake Rule.
- **`00-Company/compiled/PENDING_APPROVAL.md`** — list of files in `01-Wiki/_pending/` awaiting Cem review, grouped by topic.
- **`00-Company/compiled/CRON_SCHEDULE.md`** — last run + next run for all registered crons.

### Phase 4 — Correction Promotion (2 min)
For each agent that had corrections this cycle:
- Append to `03-Agents/[Agent]/memory/corrections.md` (create if missing)
- Draft wiki patch if correction contradicts a canonical wiki page → write to `01-Wiki/_pending/YYYY-MM-DD/corrections/[topic].md`

### Phase 5 — Lint (2 min)
Checks to run:
1. Any folder in `02-Projects/` not in `_INDEX.md` → flag `NEW_FOLDER_WITHOUT_REGISTRATION` in VAULT_HEALTH
2. Any folder pair with >70% name overlap → flag `POSSIBLE_DUPLICATE`
3. Files >100KB → flag `OVERSIZED`
4. Files not modified in 30+ days in active projects → flag `STALE`
5. Broken markdown links → flag `BROKEN_LINK`
6. `_pending/` pages older than 7 days → flag `STALE_PENDING`
7. Agent memory folders with no new log in 7+ days → flag `AGENT_INACTIVE`

All flags land in `VAULT_HEALTH.md`.

### Phase 6 — Commit & Report (1 min)
- Git commit: `git commit -am "vault-compile $(date -Iseconds)"`
- Append to `00-Company/compiled/CHANGE_LOG.md`:
  ```
  ## 2026-04-19 02:23 ET — Nightly Compile
  - Scanned: 47 files (34 agent memory, 13 project)
  - Promoted to _pending: 8 pages
  - Rebuilt: PROJECT_BOARD, BLOCKERS, TASK_SHEET, VAULT_HEALTH, PENDING_APPROVAL
  - Lint flags: 3 POSSIBLE_DUPLICATE, 5 STALE, 1 AGENT_INACTIVE (Harry, 8d)
  - Duration: 9m 14s
  - Model: sonnet-4-6
  - Tokens: 180k in, 42k out
  ```
- Post Telegram to Cem:
  ```
  🌙 Vault compile done (9m)
  • 8 pages pending approval
  • 3 vault health flags
  • Harry agent inactive 8 days
  Morning review: /Users/openclaw/Vault/00-Company/compiled/PENDING_APPROVAL.md
  ```

---

## The Compiler Prompt (stored at `00-Company/skills/compiler/PROMPT.md`)

*This is the canonical prompt the launchd job invokes. Athena maintains it.*

```markdown
You are the Ecell Global Vault Compiler. Your job runs nightly at 02:00 ET.

You have access to the Obsidian MCP server. The vault is at /Users/openclaw/Vault/.

Read AGENT_COLLABORATION.md v2.0 to understand the Pending Validation Workflow
and Project Intake Rule. Enforce them both.

Your six phases:

1. GATHER: list and read all new/modified files in 03-Agents/*/memory/ and
   02-Projects/*/ since the last run (timestamp in CHANGE_LOG.md).

2. FILTER & PROMOTE: for each file, classify contents. Promote decisions,
   process rules, and facts to 01-Wiki/_pending/YYYY-MM-DD/[topic]/[slug].md
   with the frontmatter schema in CLAUDE_CODE_COMPILER_SPEC.md.
   Skip noise. Collect blockers, questions, and corrections.

3. REBUILD COMPILED: overwrite PROJECT_BOARD, BLOCKERS, VAULT_HEALTH,
   PENDING_APPROVAL, CRON_SCHEDULE. Diff-write TASK_SHEET (preserve Cem edits).

4. CORRECTIONS: append to each agent's corrections.md where applicable. Draft
   wiki patches for contradictions to _pending/.

5. LINT: run all 7 lint checks. Write flags to VAULT_HEALTH.md.

6. REPORT: append to CHANGE_LOG.md. Write a Telegram summary to
   /tmp/compile-telegram.txt (the post-run hook will send it).

Rules:
- Never write directly to 01-Wiki/[topic]/ — always _pending/ first.
- Never delete files. Move to archive if needed.
- Never create a new folder in 02-Projects/ — that's Athena's job.
- Preserve Cem's manual edits. When in doubt, draft a diff to _pending/
  rather than overwriting.
- If unsure about classification, flag with `confidence: low` and let Cem
  review.
- If you hit any error, stop, write the error to /tmp/compile-error.txt,
  and exit non-zero so the post-run hook alerts Cem.

Begin Phase 1 now.
```

---

## Installation Steps (for Cem)

### 1. Create the compile script
```bash
sudo mkdir -p /var/log/vault-compile
sudo chown $(whoami) /var/log/vault-compile
mkdir -p ~/bin
```

Create `~/bin/vault-compile.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail

VAULT=/Users/openclaw/Vault
LOG=/var/log/vault-compile/$(date +%Y-%m-%d).log
PROMPT=$VAULT/00-Company/skills/compiler/PROMPT.md

cd $VAULT

# Pre-compile git snapshot (optional but recommended)
git add -A && git commit -m "pre-compile $(date -Iseconds)" || true

# Run Claude Code headless
claude -p "$(cat $PROMPT)" \
  --allowed-tools "mcp__obsidian__*,Bash(git:*)" \
  --max-turns 100 \
  --output-format stream-json \
  --model claude-sonnet-4-6 \
  > $LOG 2>&1

EXIT=$?

# Post-compile git commit
git add -A && git commit -m "vault-compile $(date -Iseconds)" || true

# Telegram notification
if [ -f /tmp/compile-telegram.txt ]; then
  telegram-send --config ~/.telegram-send.conf "$(cat /tmp/compile-telegram.txt)"
  rm /tmp/compile-telegram.txt
fi

if [ -f /tmp/compile-error.txt ]; then
  telegram-send --config ~/.telegram-send.conf "❌ Compile failed: $(cat /tmp/compile-error.txt)"
  rm /tmp/compile-error.txt
fi

exit $EXIT
```

```bash
chmod +x ~/bin/vault-compile.sh
```

### 2. Create the launchd plist

`~/Library/LaunchAgents/com.ecell.vault-compile.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ecell.vault-compile</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/openclaw/bin/vault-compile.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/var/log/vault-compile/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/vault-compile/stderr.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.ecell.vault-compile.plist
launchctl list | grep vault-compile   # verify
```

### 3. Validate before first automated run

Run manually once during waking hours:
```bash
~/bin/vault-compile.sh
tail -f /var/log/vault-compile/$(date +%F).log   # in another terminal
```

Check:
- Does `00-Company/compiled/PROJECT_BOARD.md` get a fresh timestamp?
- Are files appearing in `01-Wiki/_pending/`?
- Did BLOCKERS.md stop saying "Gemma 4 unavailable"?
- Did you get a Telegram summary?

If yes → let it run automated tomorrow. If no → check the log, iterate on the prompt.

### 4. Write `00-Company/skills/compiler/PROMPT.md`

Copy the prompt from the section above into that file. Athena iterates on it over time as the compiler's behaviour is tuned.

---

## Weekly and Monthly Cadence

Nightly is the base. Two higher-cadence runs add value:

### Weekly (Monday 08:00 ET, Sonnet 4.6)
Add to launchd with `Weekday = 1`. Extra steps:
- Build `00-Company/compiled/WEEKLY_DIGEST.md` summarising the week's decisions, deliverables, corrections, and health trends
- Flag `_pending/` pages older than 7 days
- Produce the "Projects Cem drove vs. projects agents completed autonomously" metric for the success dashboard

### Monthly (1st of month, Opus 4.7)
- Deep compile: re-index entire wiki, rebuild `01-Wiki/MOC.md`, audit cross-references
- Reconcile `02-Projects/_INDEX.md` against actual folder contents
- Suggest further consolidations if sprawl creeps back
- Produce a monthly strategic briefing for Cem

---

## Cost & Rate Limit Analysis

**Per-run token estimates:**
- Input: ~150-250K tokens (reading ~50 files + vault structure + prompt)
- Output: ~40-60K tokens (writing ~15-25 files)

**Under Max subscription:**
- Claude Code on Max: rate limits are high but not unlimited. A 250K-input job may hit limits if Cem is also using Claude Code interactively in parallel.
- Mitigation: compile runs at 02:00 ET, when Cem is asleep.

**If limits hit, Haiku 4.5 API fallback:**
- 250K input + 60K output × Haiku pricing ≈ **$0.50-$0.80 per run**
- Monthly: ~$15-25 (nightly) + ~$5 (weekly) + ~$5 (monthly Opus run) ≈ **$25-35/month**
- Well worth it vs. the drift cost of a broken compiler.

**Model routing inside one run (optional optimisation):**
- Phase 1 (gather): no LLM calls, just file I/O
- Phase 2 (filter): Haiku 4.5 for classification
- Phase 3 (rebuild): Sonnet 4.6 for synthesis
- Phase 4-5 (corrections + lint): Haiku 4.5
- Phase 6 (report): Haiku 4.5

This reduces cost by ~60% vs. all-Sonnet. Implement if fallback-to-API becomes the default.

---

## Failure Modes & Mitigations

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| Obsidian MCP server offline | Compiler can't read files | Post-run hook detects empty log → Telegram alert |
| Rate limit hit mid-run | stream-json shows 429 | Script retries 3× with backoff, then switches to Haiku API |
| Prompt drift produces bad output | VAULT_HEALTH flags spike or Cem sees garbage in _pending | Version-control the prompt. Roll back. |
| Git commit conflict | Git exit non-zero | Script logs and continues. Cem resolves. |
| launchd doesn't fire | No new CHANGE_LOG entry | Athena's morning check pings Cem if compile ≥ 2 runs missed |
| Compiler writes to canonical wiki instead of _pending | Wiki page changes without approval in log | Prompt rule + post-run diff check. Block and alert. |

---

## Monitoring Checklist (Athena runs daily)

1. Did last night's compile succeed? Check `CHANGE_LOG.md` for entry with today's date.
2. Is `PENDING_APPROVAL.md` fresh? Check timestamp.
3. Any alerts in `VAULT_HEALTH.md` that need Cem attention?
4. Backlog check: how many `_pending/` pages are >3 days old? If growing, nudge Cem.

---

## Open Items for Cem

- [ ] Confirm launchd on ZEUS (Mac Studio) is the right host. Alternative: iMac where Harry lives.
- [ ] Confirm Telegram bot token available for `telegram-send` install.
- [ ] Confirm Obsidian Local REST API plugin is stable (had a hang earlier today — may need to be restarted if it does this again during an automated run).
- [ ] Approve model choice: Sonnet 4.6 (recommended) vs. Haiku 4.5 (cheaper, experimental) vs. per-phase routing (most efficient, more complex).
- [ ] Approve cron time: 02:00 ET (current proposal) vs. something later/earlier.

---

## Changelog
- 2026-04-19 — Created. Primary technical spec for Breakdown #1 fix.