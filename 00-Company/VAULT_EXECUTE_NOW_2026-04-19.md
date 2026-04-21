# Execute Now — Runbook
**Created:** 2026-04-19 | **Status:** READY TO EXECUTE
**Estimated time:** 60-90 minutes end-to-end, done in one sitting or split across two
**Supersedes setup sections of:** COMPILER_ROUTINES_SETUP.md, CLAUDE_CODE_SESSION_CAPTURE.md

---

## Your Locked Configuration

All decisions made. Baked into every command below.

| Setting | Value |
|---------|-------|
| GitHub account | `gemc-wq` |
| Repo name | `ecell-vault` (suggested — change if you prefer) |
| Repo visibility | Private |
| Repo access | Cem only |
| Gitignore | `02-Projects/zero-codebase/`, `02-Projects/ppc-autoresearch/`, plus Obsidian workspace files |
| Compiler model | `claude-sonnet-4-6` |
| Weekly digest model | `claude-sonnet-4-6` |
| Monthly deep compile model | `claude-opus-4-7` |
| Archive policy | Keep forever |
| Telegram digest | Separate message, not attached to EOD |
| Correction scope | Telegram + Claude Code sessions (via session capture) |
| First run timing | Manually triggered during daytime (watch the PR land) |
| Schedule timezone | Verify in Routines UI — set to 02:00 ET equivalent |

---

## Sequence Overview

```
PART 1  — Git foundation            (~20 min)  PREREQUISITE
PART 2  — Session capture           (~15 min)  Parallel with Part 3
PART 3  — Create the Routine        (~10 min)  Web UI work
PART 4  — First manual run          (~15 min)  Daytime, watch the PR
PART 5  — Enable schedule           (~5 min)
PART 6  — Three-day smoke test      (72 hrs, passive)
```

Don't do Part 5 until Part 4 produces a PR you'd merge.

---

## Part 1 — Git Foundation

### 1.1 Pre-flight checks

From a terminal on ZEUS:

```bash
# Confirm git is installed
git --version   # expect git version 2.x or higher

# Confirm jq is installed (needed for session capture in Part 2)
jq --version || brew install jq

# Confirm you have SSH access to GitHub as gemc-wq
ssh -T git@github.com
# Expect: "Hi gemc-wq! You've successfully authenticated..."
# If "Permission denied": run `ssh-add ~/.ssh/id_ed25519` (or your key path) or set up SSH key for GitHub first
```

### 1.2 Create the GitHub repo

Go to https://github.com/new and create:
- **Owner:** `gemc-wq`
- **Repository name:** `ecell-vault`
- **Visibility:** Private
- **Initialise:** leave empty (no README, no .gitignore, no license). You're pushing an existing vault up.

Click Create. Leave the page open — you'll want the clone URL in a second.

Git created : https://github.com/gemc-wq/ecell-vault.git

### 1.3 Git-init the vault

```bash
cd /Users/openclaw/Vault

# Init git (skip if already a repo)
if [ ! -d .git ]; then
  git init
  git branch -M main
fi

# Set your identity in this repo
git config user.name "Cem"
git config user.email "cem@ecellglobal.com"   # change if you prefer a different email
```

### 1.4 Write the .gitignore

```bash
cat > .gitignore << 'EOF'
# Obsidian — per-machine workspace state, not vault knowledge
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/workspaces.json
.obsidian/hotkeys.json

# Obsidian trash
.trash/

# macOS noise
.DS_Store
._*

# Temp files
*.tmp
*.swp
*~

# Node / build artefacts if any ever land in the vault
node_modules/

# Large legacy reference codebases — NOT vault knowledge
# (42K+ files combined; bloats the repo and doesn't help the compiler)
02-Projects/zero-codebase/
02-Projects/ppc-autoresearch/

# Session capture state file (per-machine)
03-Agents/Cem-Code/.capture-state

# Compile logs (per-machine)
/var/log/vault-compile/
/var/log/cc-session-capture/
EOF
```

### 1.5 First commit and push

```bash
git add -A
git status   # review what's being added — confirm zero-codebase and ppc-autoresearch are NOT listed
git commit -m "Initial vault commit — pre-routines baseline"

# Add remote and push
git remote add origin git@github.com:gemc-wq/ecell-vault.git
git push -u origin main
```

If `git remote add` fails with "remote origin already exists", run `git remote set-url origin git@github.com:gemc-wq/ecell-vault.git` instead.

**Expected duration of push:** 1-3 minutes depending on vault size. 261 project docs + 314 wiki pages + 649 agent docs shouldn't exceed 50MB.

### 1.6 Install Obsidian Git plugin

1. Obsidian → Settings (`⌘,`) → Community plugins → Browse
2. Search: `Obsidian Git`
3. Install → Enable
4. Plugin settings:
   - **Auto commit-and-sync after file change:** `15 minutes` (or your preference)
   - **Auto pull on startup:** enable
   - **Auto push:** enable
   - **Commit message:** `vault: manual edits {{date}}`
   - **Pull before push:** enable

Test: edit any note, save, wait 15 min. Confirm you see a new commit in GitHub.

### 1.7 Part 1 checkpoint

- [ ] `ssh -T git@github.com` confirms `gemc-wq` auth works
- [ ] `gemc-wq/ecell-vault` exists on GitHub, private, initial commit visible
- [ ] `git ls-files 02-Projects/zero-codebase` returns nothing (properly excluded)
- [ ] Obsidian Git plugin installed, auto-commit enabled

If all four ✅ — Part 1 done. Proceed.

---

## Part 2 — Session Capture (Parallel with Part 3)

This captures your Claude Code work so the nightly compiler can learn from it. Do this in parallel with Part 3 if you want to save time — they're independent.

### 2.1 Create the Cem-Code agent folder

```bash
VAULT=/Users/openclaw/Vault
mkdir -p $VAULT/03-Agents/Cem-Code/sessions
touch $VAULT/03-Agents/Cem-Code/.capture-state
```

### 2.2 Create SOUL.md and TOOLS.md for Cem-Code

```bash
cat > $VAULT/03-Agents/Cem-Code/SOUL.md << 'EOF'
# Cem-Code — Session Record

This folder captures Cem's Claude Code sessions verbatim for compiler ingestion.

## Rules for the Compiler

1. **All content here is Cem-authored.** Treat as pre-approved.
2. **SOP/PRD updates Cem instructs inside a session are canonical** — do not route through pending/PR approval.
3. **Corrections Cem makes in-session** belong in the corrected agent's `corrections.md` OR in the relevant wiki page if it's an SOP/PRD correction.
4. **Questions Cem asks** are context, not work items — do not create tasks from them.
5. **Code Cem pastes in** is reference, not knowledge — do not promote to wiki.

## File Format

- `sessions/YYYY-MM-DD/{project-slug}__{session-id}.md`
- Project slug = Claude Code project (maps to a repo or directory)
- Session ID = Claude Code's internal identifier
- Content is a readable markdown rendering of the session JSON
EOF

cat > $VAULT/03-Agents/Cem-Code/TOOLS.md << 'EOF'
# Cem-Code — Tools

Cem-Code is not an interactive agent. It is a pseudo-agent representing Cem's Claude Code work.

Data source: `~/.claude/projects/*/sessions/*.json` on ZEUS
Capture: `~/bin/capture-cc-sessions.sh` (launchd, hourly)
Vault target: `03-Agents/Cem-Code/sessions/YYYY-MM-DD/`
Ingested by: nightly vault compiler (via Routines)
EOF
```

### 2.3 Write the capture script

```bash
mkdir -p ~/bin
cat > ~/bin/capture-cc-sessions.sh << 'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

VAULT=/Users/openclaw/Vault
SESSIONS_SRC=$HOME/.claude/projects
SESSIONS_DEST=$VAULT/03-Agents/Cem-Code/sessions
STATE_FILE=$VAULT/03-Agents/Cem-Code/.capture-state

mkdir -p $SESSIONS_DEST
touch $STATE_FILE

# Find session JSONs modified in the last 70 minutes (overlap for safety)
find $SESSIONS_SRC -name "*.json" -mmin -70 -type f 2>/dev/null | while read -r src; do
  session_id=$(basename "$src" .json)
  project_slug=$(basename $(dirname $(dirname "$src")))
  mtime=$(stat -f %m "$src")
  key="${project_slug}/${session_id}:${mtime}"

  # Skip if already captured at this mtime
  if grep -qxF "$key" $STATE_FILE 2>/dev/null; then
    continue
  fi

  date_str=$(date -r "$src" +%Y-%m-%d)
  dest_dir=$SESSIONS_DEST/$date_str
  mkdir -p $dest_dir
  dest_file="$dest_dir/${project_slug}__${session_id}.md"

  # Try structured JSON-to-markdown conversion
  if jq -e '.messages' "$src" > /dev/null 2>&1; then
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
    ' "$src" > "$dest_file"
  else
    # Fallback: try line-delimited JSON format (newer Claude Code)
    {
      echo "# Claude Code Session"
      echo "**Project:** ${project_slug}"
      echo "**Session ID:** ${session_id}"
      echo "**Captured:** $(date -Iseconds)"
      echo
      echo "---"
      echo
      jq -r 'select(.role) | "## " + (.role | ascii_upcase) + " — " + (.timestamp // "") + "\n\n" + (.content // .text // "[non-text content]") + "\n"' "$src" 2>/dev/null || cat "$src"
    } > "$dest_file"
  fi

  # Redaction — scrub common credential patterns
  sed -i '' -E '
    s/(api[_-]?key["'\'':=[:space:]]+)[A-Za-z0-9_-]{20,}/\1[REDACTED]/gI
    s/(secret["'\'':=[:space:]]+)[A-Za-z0-9_-]{20,}/\1[REDACTED]/gI
    s/(Bearer[[:space:]]+)[A-Za-z0-9._-]{20,}/\1[REDACTED]/g
    s/(password["'\'':=[:space:]]+)[^[:space:]]+/\1[REDACTED]/gI
    s/(sk-[A-Za-z0-9]{20,})/[REDACTED-OPENAI-KEY]/g
    s/(sk-ant-[A-Za-z0-9_-]{20,})/[REDACTED-ANTHROPIC-KEY]/g
    s/(ghp_[A-Za-z0-9]{20,})/[REDACTED-GITHUB-TOKEN]/g
    s/(xoxb-[A-Za-z0-9_-]+)/[REDACTED-SLACK-TOKEN]/g
  ' "$dest_file"

  echo "$key" >> $STATE_FILE
  echo "[$(date -Iseconds)] captured: $dest_file"
done

# Keep state file trim
if [ -f $STATE_FILE ] && [ $(wc -l < $STATE_FILE) -gt 10000 ]; then
  tail -10000 $STATE_FILE > $STATE_FILE.tmp && mv $STATE_FILE.tmp $STATE_FILE
fi
SCRIPT

chmod +x ~/bin/capture-cc-sessions.sh
```

### 2.4 Test manually

```bash
~/bin/capture-cc-sessions.sh
# Expect: one or more "captured: ..." lines if you've used Claude Code in the last 70 min
# If no recent sessions: do a short Claude Code session, wait a minute, re-run

# Verify
ls $VAULT/03-Agents/Cem-Code/sessions/$(date +%Y-%m-%d)/
```

Open one of the captured files in Obsidian. Spot-check:
- Is the markdown readable?
- Are any credentials visible in plaintext? (If yes, tighten the redaction sed patterns before proceeding.)

### 2.5 Install the launchd job

```bash
sudo mkdir -p /var/log/cc-session-capture
sudo chown $(whoami) /var/log/cc-session-capture

cat > ~/Library/LaunchAgents/com.ecell.cc-session-capture.plist << 'EOF'
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
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/var/log/cc-session-capture/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/cc-session-capture/stderr.log</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.ecell.cc-session-capture.plist
launchctl list | grep cc-session-capture   # verify
```

### 2.6 Part 2 checkpoint

- [ ] `~/bin/capture-cc-sessions.sh` runs without error
- [ ] Captured markdown files visible in `03-Agents/Cem-Code/sessions/YYYY-MM-DD/`
- [ ] Spot-check: no unredacted credentials in captured files
- [ ] launchd job loaded and in `launchctl list`
- [ ] Obsidian Git will auto-commit captured sessions on next 15-min cycle

Proceed to Part 3 (or do it in parallel while capture runs).

---

## Part 3 — Create the Routine

### 3.1 Verify Routines access

1. Open https://claude.ai/code
2. Confirm you can see "Routines" in the left sidebar. If not: ensure your Claude Max subscription has Claude Code on the web enabled. Settings → Subscription.

### 3.2 Create the nightly compile routine

1. Go to https://claude.ai/code/routines
2. Click **Create routine**
3. Fill in:

| Field          | Value                                                                                 |
| -------------- | ------------------------------------------------------------------------------------- |
| **Name**       | `Vault Nightly Compiler`                                                              |
| **Repository** | Connect GitHub, select `gemc-wq/ecell-vault`                                          |
| **Branch**     | `main` (the routine creates its own `claude/` branches off this)                      |
| **Model**      | `claude-sonnet-4-6`                                                                   |
| **Prompt**     | Paste the contents of `00-Company/skills/compiler/ROUTINE_PROMPT.md` (below)          |
| **Connectors** | Leave empty for v1                                                                    |
| **Triggers**   | **DO NOT add a schedule trigger yet.** Add it in Part 5 after the first run succeeds. |

### 3.3 The prompt to paste

Copy-paste into the "Prompt" field:

```
You are the Ecell Global Vault Compiler, running as a Claude Code Routine on a nightly schedule.

The cloned repository you're working in is the Ecell Global Obsidian vault. Your full operating instructions, phase sequence, output schema, and rules of engagement live at:

00-Company/skills/compiler/PROMPT.md

Read that file first. Follow it exactly. Do not improvise on the phases or file paths.

Also read the following before you begin, in this order:
1. 00-Company/AGENT_COLLABORATION.md — especially §10 Project Intake Rule and §11 Pending Validation Workflow
2. 00-Company/AGENT_ROSTER.md — current agents, models, platforms
3. 00-Company/compiled/CHANGE_LOG.md — find the last successful compile timestamp so you know what's new
4. INDEX.md — vault structure overview

Work on branch claude/vault-compile-YYYY-MM-DD (use today's date). When done, open a pull request titled:

[compile] YYYY-MM-DD — N promotions, B blockers, H health flags

PR description must include:
- Counts of files scanned, promoted, corrected, flagged
- Model used, run duration, token usage
- Top 3 items needing Cem's attention (if any)
- Any classification confidence concerns (confidence: low entries)

Rules:
- Never push to main. Always a PR.
- Never delete files. Move to archive.
- Never create new folders in 02-Projects/ — Athena does that.
- Preserve Cem's manual edits. If a file was edited by a human since last compile, diff-merge rather than overwrite.
- Content from 03-Agents/Cem-Code/sessions/ is Cem-authored — pre-approved, do not gate through pending.
- If you hit an unrecoverable error, commit what you have, open the PR with [FAILED] prefix, include the error in the description.

Begin by reading 00-Company/skills/compiler/PROMPT.md.
```

### 3.4 Save the routine

Click **Save**. Routine appears in your list, status "Not scheduled" (correct — we'll enable schedule in Part 5).

### 3.5 Part 3 checkpoint

- [ ] Routine exists in your routines list
- [ ] Model = Sonnet 4.6
- [ ] Repository = `gemc-wq/ecell-vault`
- [ ] No schedule trigger yet

---

## Part 4 — First Manual Run (Daytime)

**Do this when you have 15-20 minutes and can watch.**

### 4.1 Trigger it

In the routine's detail page, click **Run now**.

### 4.2 Watch it work

- Routine status changes to "Running"
- You can click into the live session to watch Claude Code's reasoning in real time
- Expected duration: 8-15 minutes for the first run (more files to scan than subsequent runs)

### 4.3 Review the PR

When status flips to "Completed":

1. Click the PR link in the routine output (or go to GitHub → `gemc-wq/ecell-vault` → Pull requests)
2. PR should be titled something like `[compile] 2026-04-19 — N promotions, B blockers, H flags`
3. Review the diff:
   - **`01-Wiki/` changes:** read each promoted page. Accurate? Source-attributed? Confidence appropriate?
   - **`00-Company/compiled/` changes:** check PROJECT_BOARD, BLOCKERS, TASK_SHEET. Fresh timestamps? Reasonable content?
   - **`03-Agents/*/corrections.md`:** any new entries? Do they reflect real corrections?
   - **PR description:** does it surface things needing your attention?

### 4.4 Decide

- **Looks good →** Merge the PR. Your vault now has its first clean compile.
- **Mostly good, minor issues →** Add inline comments on specific files, merge anyway. Next run will learn.
- **Structural problems →** Close the PR (don't merge). Iterate on `00-Company/skills/compiler/PROMPT.md` to fix the issue. Re-trigger via Run now.
- **Catastrophic →** Close the PR. Ping me (or ask Athena) with the specific failure. Do not enable schedule.

### 4.5 Pull locally

After merging:

```bash
cd /Users/openclaw/Vault
git pull
```

Obsidian will reload. Spot-check a promoted page in the UI to confirm it renders correctly.

### 4.6 Part 4 checkpoint

- [ ] First PR opened
- [ ] PR reviewed and merged (or iterated on)
- [ ] Local vault pulled
- [ ] Obsidian shows the new wiki content
- [ ] `BLOCKERS.md` no longer says "Gemma 4 unavailable"

If all ✅ — proceed to Part 5.

---

## Part 5 — Enable the Schedule

### 5.1 Determine the cron expression

In the Routines UI, check what timezone the schedule trigger uses. Typically UTC.

- **If UI shows UTC:** 02:00 ET during DST = `0 6 * * *`; standard time = `0 7 * * *`. Or use 02:00 UTC (22:00 ET previous day) = `0 2 * * *` if you don't want to worry about DST.
- **If UI shows local timezone:** `0 2 * * *` = 02:00 your time.

**Recommendation:** Start with `0 6 * * *` (UTC → 02:00 EDT). You'll be in DST through November.

### 5.2 Add the trigger

1. Routines UI → `Vault Nightly Compiler` → Edit
2. Triggers → Add trigger → Schedule
3. Cron expression: `0 6 * * *` (or per your calc)
4. Save

### 5.3 Enable mobile PR notifications

On your phone, GitHub app → Settings → Notifications:
- **Pull requests:** On
- **Push notifications for pull requests:** On
- **Scope:** Only repositories I'm watching

On GitHub web → `gemc-wq/ecell-vault` → click **Watch** → All activity

Now every compile PR wakes your phone overnight. Morning routine: glance at notification, tap, review diff, merge.

### 5.4 Part 5 checkpoint

- [ ] Schedule trigger active
- [ ] Phone GitHub notifications enabled
- [ ] Watching `gemc-wq/ecell-vault` for all activity

---

## Part 6 — Three-Day Smoke Test

Passive. Just watch.

- **Day 1 morning:** PR from overnight compile. Review, merge, pull.
- **Day 2 morning:** Same. Note any prompt issues — edit `PROMPT.md` directly, commit, next run picks it up.
- **Day 3 morning:** Third successful run. If all three were clean, the system is stable.

Milestones during smoke test:

- [ ] Three consecutive nightly compiles complete with PR
- [ ] At least one Claude Code session captured and ingested
- [ ] At least one correction or SOP/PRD update detected (likely if you're working in Claude Code)
- [ ] PROJECT_BOARD.md shows fresh data
- [ ] No compile has `[FAILED]` prefix

Once all ✅ — Breakdown #1 is solved. Move on to Breakdown #2 (merge map) and #3 (collaboration v2.0 rule enforcement).

---

## Rollback Plan

If anything goes catastrophically wrong:

### Rollback the Routine
- Routines UI → disable schedule trigger (one click) — stops future runs
- Close any open problematic PRs without merging — vault unaffected

### Rollback session capture
```bash
launchctl unload ~/Library/LaunchAgents/com.ecell.cc-session-capture.plist
rm ~/Library/LaunchAgents/com.ecell.cc-session-capture.plist
# Captured sessions remain in vault; delete folder if you want them gone:
# rm -rf /Users/openclaw/Vault/03-Agents/Cem-Code/sessions/
```

### Rollback git (hard reset)
```bash
cd /Users/openclaw/Vault
git log --oneline   # find the commit before things went wrong
git reset --hard <commit-hash>
# Or, nuclear option:
# rm -rf .git
```

The vault is just markdown files. Git and Routines never delete content — worst case you rewind commits and lose nothing.

---

## What You Are NOT Doing Yet

To stay focused, these are explicitly OUT of this session:

- **Project merge execution** (the 13 decision groups in PROJECT_MERGE_MAP_2026-04-19.md) — do separately after Part 6 succeeds
- **Agent SOUL.md updates** with v2.0 rules — Athena handles after compiler is stable
- **Weekly and monthly routines** — add after nightly is stable
- **Retroactive cleanup of Apr 17-19 auto-promotions** — first full compile will flag these; handle in the PR

---

## Final Sanity Check Before You Start

✅ You have:
- 60-90 minutes uninterrupted
- Access to ZEUS terminal
- Access to GitHub as `gemc-wq` (SSH key working)
- Claude Max subscription with Claude Code on the web enabled
- Obsidian open
- Daytime (so you can do Part 4 and watch)

If any of these are no: come back when they're all yes.

---

## Need Help Mid-Execution

If you hit a wall:
1. Don't force it. Note the specific error in `04-Shared/active/execute-now-issues/YYYY-MM-DD-[area].md`
2. Continue with what you can — Part 1, 2, 3 are independent; only Parts 4–6 require earlier parts complete
3. Ping me or Athena with the error and I'll unblock

---

## Changelog
- 2026-04-19 — Created. All 9 decisions locked, runbook pre-filled, commands copy-pasteable.