# Claude Code Session Capture — Spec
**Created:** 2026-04-19 | **Status:** SPEC — ready to implement
**Triggered by:** Cem decision #4 (2026-04-19) — correction detection scope expanded to include Claude Code sessions
**Owner:** Cem (install) | Athena (monitoring)

---

## Why This Component Exists

Cem works extensively inside Claude Code — often asking it to update SOPs, PRDs, and project docs directly. Without capture, three things are lost:

1. **Corrections Cem makes in-session** ("no, that's wrong, the Walmart rule is X") evaporate when the session ends.
2. **SOP/PRD updates** Cem instructs Claude Code to perform don't propagate to other agents' knowledge — Ava/Hermes/Harry keep reading the old version because they have no awareness it changed.
3. **Decision context** (why Cem asked for a specific change) is lost, so future agents don't understand the reasoning.

Session capture turns Cem's Claude Code work into first-class agent memory, which then feeds the nightly compiler like any other agent log.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       ZEUS (Mac Studio)                          │
│                                                                 │
│  Cem works in Claude Code                                       │
│     │                                                           │
│     └─▶ session files saved to ~/.claude/projects/*/sessions/   │
│                                                                 │
│  launchd hourly job → ~/bin/capture-cc-sessions.sh              │
│     │                                                           │
│     └─▶ reads new session JSON files                           │
│         └─▶ converts to markdown                               │
│             └─▶ writes to Vault/03-Agents/Cem-Code/sessions/   │
│                                                                 │
│  Obsidian Git plugin (auto-commit every 15min)                 │
│     └─▶ commits new sessions, pushes to GitHub                 │
│                                                                 │
│  Next nightly Routine compile reads sessions like any log      │
└─────────────────────────────────────────────────────────────┘
```

---

## Where Claude Code Stores Sessions

As of Claude Code 2.x, session state lives at:
- **macOS:** `~/.claude/projects/<project-slug>/sessions/<session-id>.json`
- Each session is a JSON file containing full conversation history with timestamps
- Multiple projects = multiple slugs

The exact path can be verified with:
```bash
find ~/.claude -name "*.json" -newer /tmp/yesterday -type f 2>/dev/null | head
```

---

## Capture Script

**File:** `~/bin/capture-cc-sessions.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

VAULT=/Users/openclaw/Vault
SESSIONS_SRC=~/.claude/projects
SESSIONS_DEST=$VAULT/03-Agents/Cem-Code/sessions
STATE_FILE=$VAULT/03-Agents/Cem-Code/.capture-state

mkdir -p $SESSIONS_DEST
touch $STATE_FILE

# Find session files modified in the last hour that we haven't captured yet
find $SESSIONS_SRC -name "*.json" -mmin -60 -type f 2>/dev/null | while read -r src; do
  session_id=$(basename "$src" .json)
  project_slug=$(basename $(dirname $(dirname "$src")))
  
  # Skip if already captured at this file's current mtime
  mtime=$(stat -f %m "$src")
  key="${project_slug}/${session_id}:${mtime}"
  
  if grep -qxF "$key" $STATE_FILE 2>/dev/null; then
    continue
  fi
  
  # Convert JSON to readable markdown
  date_str=$(date -r "$src" +%Y-%m-%d)
  dest_dir=$SESSIONS_DEST/$date_str
  mkdir -p $dest_dir
  dest_file="$dest_dir/${project_slug}__${session_id}.md"
  
  # Use jq to extract messages into markdown
  # (install jq if not present: brew install jq)
  jq -r '
    "# Claude Code Session\n" +
    "**Project:** " + (.project // "unknown") + "\n" +
    "**Started:** " + (.started_at // "unknown") + "\n" +
    "**Session ID:** " + (.session_id // "unknown") + "\n\n" +
    "---\n\n" +
    (.messages // [] | map(
      "## " + (.role | ascii_upcase) + " — " + (.timestamp // "") + "\n\n" +
      (.content // "") + "\n\n"
    ) | join(""))
  ' "$src" > "$dest_file" 2>/dev/null || {
    # Fallback if JSON structure differs: just copy raw
    cp "$src" "${dest_file%.md}.json"
    continue
  }
  
  echo "$key" >> $STATE_FILE
  echo "Captured: $dest_file"
done

# Keep state file trim (last 30 days of entries)
if [ -f $STATE_FILE ]; then
  tail -10000 $STATE_FILE > $STATE_FILE.tmp && mv $STATE_FILE.tmp $STATE_FILE
fi
```

Make it executable:
```bash
chmod +x ~/bin/capture-cc-sessions.sh
```

---

## Launchd Job

**File:** `~/Library/LaunchAgents/com.ecell.cc-session-capture.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ecell.cc-session-capture</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/openclaw/bin/capture-cc-sessions.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>  <!-- every hour -->
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/var/log/cc-session-capture/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/cc-session-capture/stderr.log</string>
</dict>
</plist>
```

Load it:
```bash
sudo mkdir -p /var/log/cc-session-capture
sudo chown $(whoami) /var/log/cc-session-capture
launchctl load ~/Library/LaunchAgents/com.ecell.cc-session-capture.plist
launchctl list | grep cc-session-capture   # verify
```

---

## Agent Folder Setup

Create the Cem-Code "agent" folder (it's not really an agent, it's Cem-via-Claude-Code, but treating it as one gives the compiler a consistent interface):

```
03-Agents/Cem-Code/
├── SOUL.md              ← identity: "Cem working in Claude Code. All content here is Cem-authored."
├── TOOLS.md             ← nav pointer to vault
├── sessions/            ← captured sessions, YYYY-MM-DD/ subdirs
│   └── 2026-04-19/
│       └── ecell-vault__abc123.md
└── .capture-state       ← gitignored, tracks which sessions have been captured
```

Add to `.gitignore`:
```
03-Agents/Cem-Code/.capture-state
```

### Cem-Code SOUL.md

```markdown
# Cem-Code — Session Record

This folder captures Cem's Claude Code sessions verbatim for compiler ingestion.

## Rules for Compiler

1. **All content here is Cem-authored.** Treat as pre-approved.
2. **SOP/PRD updates Cem instructs inside a session are canonical** — do not route through pending approval.
3. **Corrections Cem makes in-session** ("no, wrong, fix to X") belong in the corrections.md of the agent being corrected, OR in the relevant wiki page if it's an SOP/PRD correction.
4. **Questions Cem asks** are context, not work items — do not create tasks from them.
5. **Code Cem pastes in** is reference, not knowledge — do not promote to wiki.

## Session File Format

- `YYYY-MM-DD/{project-slug}__{session-id}.md`
- Project slug indicates which Claude Code project (maps to a repo or directory)
- Session ID is Claude Code's internal identifier
- File content is a readable markdown rendering of the JSON session
```

---

## Compiler Integration

Update `00-Company/skills/compiler/PROMPT.md` Phase 1.2 target list to include:

```
Primary scan targets (in order of priority):
1. 03-Agents/Cem-Code/sessions/YYYY-MM-DD/  ← NEW: Cem's Claude Code work (authored-by-Cem)
2. 03-Agents/*/memory/                       ← agent daily logs
3. 03-Agents/*/handoffs/                     ← agent-to-agent handoffs
4. 02-Projects/*/                            ← project status, specs
5. 04-Shared/active/                         ← cross-agent active work
6. 04-Shared/decisions/                      ← cross-agent decisions
```

Update Phase 2.1 with the authorship rule:

```
Authorship discrimination:
- Content from 03-Agents/Cem-Code/sessions/ = Cem-authored = pre-approved.
  Any SOP/PRD update described in these sessions should be:
  • Applied directly to the canonical wiki page (not _pending/, not PR-gated)
  • Logged in the compile summary as "Cem SOP/PRD update propagated"
  • Cross-checked: do other agents' recent outputs reflect the old version? 
    If yes, flag in VAULT_HEALTH as "knowledge drift detected, agents reading stale"

- Content from other agents' memory/ = agent-authored = needs approval gate.
```

---

## Privacy / Data Considerations

Claude Code sessions can contain:
- API keys, tokens, database credentials pasted in prompts
- Customer data Cem was analyzing
- Source code from private repos

**Mitigations:**
1. **Redaction pre-commit.** Add a simple sed-based redactor in the capture script that scrubs known patterns (lines containing `API_KEY=`, `Bearer ey...`, `password=`, etc.) before writing the markdown. Starter list:
   ```bash
   # Add before the jq step in capture-cc-sessions.sh:
   # Run rendered markdown through redaction
   sed -i '' -E '
     s/(api[_-]?key["'\'':=[:space:]]+)[A-Za-z0-9_-]{20,}/\1[REDACTED]/gI;
     s/(secret["'\'':=[:space:]]+)[A-Za-z0-9_-]{20,}/\1[REDACTED]/gI;
     s/(Bearer[[:space:]]+)[A-Za-z0-9._-]{20,}/\1[REDACTED]/g;
     s/(password["'\'':=[:space:]]+)[^[:space:]]+/\1[REDACTED]/gI;
   ' "$dest_file"
   ```
2. **Private GitHub repo only.** The vault repo is private. Only Cem (and invited collaborators) can access.
3. **Gitignore sensitive session projects.** If a Claude Code project slug is known to contain credentials (e.g., `ecell-secrets/`), skip it in the capture script.
4. **Retention.** Sessions are captured as markdown and retained. If this becomes a liability, add a 90-day auto-purge (opposite of archive policy for business docs, which Cem wants indefinite).

---

## Success Metrics

In WEEKLY_DIGEST:
- Sessions captured per day (expect 3-10/day based on Cem's usage)
- SOP/PRD updates propagated (count per week)
- "Knowledge drift detected" flags (should trend down as propagation catches up)
- Redaction hits (if >0, tighten redaction patterns)

---

## Install Checklist

- [ ] `jq` installed (`brew install jq`)
- [ ] Create `03-Agents/Cem-Code/` folder with SOUL.md and TOOLS.md
- [ ] Write `~/bin/capture-cc-sessions.sh` and chmod +x
- [ ] Test manually: `~/bin/capture-cc-sessions.sh` — confirm new markdown files appear
- [ ] Verify redaction works by running on a session with a fake API key
- [ ] Install launchd plist and load it
- [ ] Add Cem-Code to `02-Projects/_INDEX.md`? No — it's not a project, it's an agent folder. Register in AGENT_ROSTER instead (as pseudo-agent, "Cem-via-Claude-Code").
- [ ] Update AGENT_ROSTER.md to list Cem-Code as a data source
- [ ] Update PROMPT.md Phase 1.2 + 2.1 per the integration section above
- [ ] First week: confirm sessions are being captured and compiled

---

## Fallback

If capture script has issues, the minimum viable version is:
```bash
rsync -a --include="*.json" ~/.claude/projects/ $VAULT/03-Agents/Cem-Code/sessions-raw/
```

This copies raw JSON into the vault. Less readable but not lost. Compiler can parse JSON on ingest.

---

## Changelog
- 2026-04-19 — Created in response to Cem decision #4 expanding correction-detection scope to Claude Code sessions.