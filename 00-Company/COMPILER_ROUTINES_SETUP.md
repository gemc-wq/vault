# Vault Nightly Compiler — Routines Setup Guide
**Created:** 2026-04-19 | **Status:** RECOMMENDED APPROACH (supersedes launchd spec)
**Prerequisite:** Vault must be a git repo pushed to GitHub (private)
**Owner:** Cem (one-time setup) | Athena (prompt maintenance)

---

## Why This Replaces the Launchd Spec

The original plan in `CLAUDE_CODE_COMPILER_SPEC.md` used launchd + bash + Obsidian REST API running on ZEUS. It works, but requires:
- ZEUS always on and awake at 02:00 ET
- Obsidian Local REST API running reliably (it hung on us earlier today)
- Bash script, plist, telegram-send, log directory, error handling
- Separate approval UX (checking `_pending/` folder)

Claude Code Routines (launched April 14, 2026) delivers the same outcome better:
- Runs on Anthropic's cloud — ZEUS can be asleep
- No local infra to maintain
- Approval gate = GitHub PR review (much better UX, mobile-friendly, versioned)
- Schedule + API + GitHub triggers can be combined
- Automatic audit trail via git

**Decision:** Use Routines as primary. Keep launchd spec as fallback if Routines hits daily limits or you need sub-hour cadence that exceeds 15 runs/day.

---

## How the Workflow Changes

### Before (launchd + `_pending/`)
```
02:00 Compiler runs on ZEUS
  → reads vault via Obsidian REST API
  → writes to 01-Wiki/_pending/
  → writes compiled/ outputs
  → sends Telegram summary
08:00 Cem reviews PENDING_APPROVAL.md
  → approves/edits/rejects pages one by one
  → approved pages move to 01-Wiki/
```

### After (Routines + Pull Request)
```
02:00 Routine fires on Anthropic cloud
  → clones vault git repo
  → branches to claude/vault-compile-YYYY-MM-DD
  → writes directly to 01-Wiki/, rebuilds compiled/
  → commits + opens PR with summary
08:00 Cem gets GitHub mobile push notification
  → reviews PR diff on phone or laptop
  → inline comments for edits, merge for approval, close for reject
  → local vault pulls updates
```

PR merged = canonical truth. Full diff visible. Every compile is a reviewable, revertible commit.

---

## Prerequisites — Git-ify the Vault

Skip this section if the vault is already a GitHub repo.

### 1. Initialize git in the vault

```bash
cd /Users/openclaw/Vault
git init
```

### 2. Create `.gitignore`

```bash
cat > .gitignore << 'EOF'
# Obsidian workspace state (per-machine, don't version)
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/workspaces.json

# Obsidian trash
.trash/

# Obsidian hotkeys (personal)
.obsidian/hotkeys.json

# Claude Code build artifacts
node_modules/
.DS_Store

# Temp files
*.tmp
*.swp
*~

# Large legacy codebases (not vault knowledge)
02-Projects/zero-codebase/
02-Projects/ppc-autoresearch/
EOF
```

**Note on zero-codebase and ppc-autoresearch:** These are 36K+ and 5K+ files of legacy reference code. Gitignoring keeps vault repo lean. If they need to be accessible to the compiler, create a separate repo for them and link via submodule later.

### 3. First commit and push to GitHub

```bash
# Create a private repo on GitHub first, e.g. cem/ecell-vault
# Then:

git add -A
git commit -m "Initial vault commit"
git branch -M main
git remote add origin git@github.com:cem/ecell-vault.git
git push -u origin main
```

### 4. Install Obsidian Git plugin (optional but recommended)

Automates local commits of your manual vault edits so the remote stays in sync.

- Obsidian → Settings → Community plugins → Browse → "Obsidian Git" → Install + Enable
- Settings: auto-commit every 15 min, auto-push on commit
- This way, when you edit a note in Obsidian, it's committed and pushed automatically. The nightly routine then sees your latest work.

---

## Setting Up the Routine

### Path A — Web UI (recommended for first setup)

1. Go to **claude.ai/code/routines**
2. Click **"Create routine"**
3. Fill in:
   - **Name:** `Vault Nightly Compiler`
   - **Repository:** select `cem/ecell-vault`
   - **Prompt:** paste the contents of `00-Company/skills/compiler/ROUTINE_PROMPT.md` (see that file — short dispatcher that reads the full prompt from the repo)
   - **Model:** `claude-sonnet-4-6` (recommended balance). Upgrade to Opus 4.7 for the monthly deep compile later.
   - **Triggers:** add a **Schedule** trigger → `0 2 * * *` (02:00 UTC = 22:00 ET previous day; adjust to `0 6 * * *` for 02:00 ET)
   - **Connectors:** leave blank for v1. Add Slack later if desired.
   - **Branch prefix:** default `claude/` (keep this — it's the safety rail)
4. Save.

### Path B — CLI

From Claude Code:

```
/schedule
```

Follow the prompts. Specify the repo, paste the prompt, confirm cadence.

### Cron timing note

Routines schedule triggers use standard cron expressions. Your earlier spec said 02:00 ET. If the Routines timezone is UTC (check the UI — it typically is), then:
- 02:00 ET standard time = 07:00 UTC → `0 7 * * *`
- 02:00 ET daylight time = 06:00 UTC → `0 6 * * *`
- Or use 02:00 UTC to just have it run overnight without caring about your timezone → `0 2 * * *`

Verify in the Routines UI which timezone it displays.

---

## Additional Routines to Set Up

With 15 runs/day on Max, you have headroom. Recommended layer-in over Weeks 1-2:

### 1. Weekly Digest (Monday 08:00 ET)
- **Trigger:** schedule `0 12 * * 1` (Mon 12:00 UTC = 08:00 ET)
- **Prompt:** reference `00-Company/skills/compiler/WEEKLY_PROMPT.md` (to be written)
- **Model:** Sonnet 4.6
- Builds WEEKLY_DIGEST.md with decisions, completions, corrections, health trends

### 2. Monthly Deep Compile (1st of month, 03:00 ET)
- **Trigger:** schedule `0 7 1 * *`
- **Prompt:** reference `00-Company/skills/compiler/MONTHLY_PROMPT.md` (to be written)
- **Model:** Opus 4.7
- Re-indexes wiki, rebuilds MOC, audits cross-references, strategic briefing

### 3. Alert Triage (API trigger, no schedule)
- **Trigger:** API webhook only
- **Prompt:** `Triage the alert in this payload. Read CHANGE_LOG and BLOCKERS. Write a triage note to 04-Shared/active/alerts/ and open PR.`
- **Model:** Haiku 4.5 (fast, cheap)
- Hook up to any monitoring system later (SP-API failures, Supabase alerts, etc.)

### 4. Project Intake Polisher (API trigger from Telegram bot)
- **Trigger:** API webhook
- **Prompt:** `Process this project intake request. Search _INDEX.md for overlap. Draft canonical spec. Open PR.`
- **Model:** Sonnet 4.6
- Your Telegram bot POSTs to this when you ask an agent to "start a new project for X"

Budget check: 1 (nightly) + 1 (weekly, averaged 0.14/day) + 1 (monthly, 0.03/day) = ~1.2/day baseline. Plenty of room for ad-hoc alerts and intake requests.

---

## How the PR Review Workflow Works for You

### Morning (08:00 ET, 5-minute review)

1. Phone buzz — GitHub notification: *"cem/ecell-vault: PR #47 opened — [compile] 2026-04-20 (12 promotions, 3 blockers)"*
2. Tap notification → opens GitHub mobile
3. Review diff:
   - **Promotions in `01-Wiki/`**: read each one, is it accurate?
   - **Rebuilt `compiled/` files**: spot-check PROJECT_BOARD and BLOCKERS
   - **New `corrections.md` entries**: are they captured correctly?
4. Actions available:
   - **Merge** = approve everything in this compile
   - **Comment on a specific file** = request edit (compiler reads comments next run)
   - **Close PR** = reject this compile entirely (rare)
   - **Suggest change** (GitHub's inline edit) = fix directly in the diff, then merge

### Later in the day
- `git pull` on ZEUS (or auto-pull via Obsidian Git plugin) → local vault is in sync
- Continue your work in Obsidian as normal — your edits auto-commit and push
- Tomorrow's compile picks up from your latest state

### When you disagree with something the compiler did
- Don't fight it in the PR. Just close that PR.
- Edit the source (agent memory log or project doc) to fix the misunderstanding
- Next run will re-evaluate from the corrected source
- Add a rule to the routine prompt if the misunderstanding is systemic

---

## Daily Limits & Cost

**Max plan:** 15 runs/day included. Metered overage available.

**Your expected usage:**
- Nightly compile: 1/day = 30/month
- Weekly digest: 0.14/day avg = 4/month
- Monthly deep: 0.03/day avg = 1/month
- Alert triage (ad hoc): ~0-3/day avg
- **Total expected: 2-5 routine runs/day** — comfortably inside 15/day

**Usage limits:** routines draw down the same subscription limits as interactive Claude Code sessions. If the nightly compile runs while you're sleeping, no conflict with your daytime Claude Code work.

**If you ever hit the 15/day cap:** metered overage billing kicks in (priced per run). Or downgrade cadence. Or migrate that routine to the launchd fallback approach.

---

## Safety Rails

1. **Branch prefix `claude/`**: routine can never push to `main` directly. Always a branch. Always a PR.
2. **PR required to merge**: your approval is the gate. Nothing becomes canonical without your click.
3. **Full git history**: every compile is a commit, revertible forever.
4. **Rate limits**: worst case is a spiraling routine burns 15 runs/day — capped.
5. **Kill switch**: routines can be disabled in the web UI in one click.
6. **Zero local impact**: a misbehaving routine can't wedge ZEUS or Obsidian — it runs in the cloud.

---

## Fallback Plan

If Routines has issues (it's research preview):
- Revert to `CLAUDE_CODE_COMPILER_SPEC.md` launchd approach
- Both specs share the same core prompt file (`00-Company/skills/compiler/PROMPT.md`) — swap the execution layer, keep the logic
- Document the issue to Anthropic feedback

---

## Setup Checklist

- [ ] Vault is git-initialized with proper `.gitignore`
- [ ] Vault pushed to private GitHub repo (`cem/ecell-vault` or similar)
- [ ] Obsidian Git plugin installed + configured (auto-commit 15 min, auto-push on commit)
- [ ] `00-Company/skills/compiler/PROMPT.md` committed to repo (full prompt — see that file)
- [ ] `00-Company/skills/compiler/ROUTINE_PROMPT.md` committed (short dispatcher that references PROMPT.md)
- [ ] Routine created at claude.ai/code/routines
- [ ] First run triggered manually via "Run now" button in Routines UI
- [ ] First PR reviewed and merged
- [ ] GitHub mobile notifications enabled on phone
- [ ] Schedule trigger active
- [ ] Three consecutive nightly runs complete successfully
- [ ] Decommission the `BLOCKERS.md` "Gemma 4 unavailable" line

---

## Open Questions for Cem

1. **GitHub account for the repo.** Personal account, Ecell org account, or a new dedicated account?
2. **Who should have access to the repo?** Just you, or also Jay Mark / other humans on the team?
3. **`zero-codebase/` and `ppc-autoresearch/`:** gitignore them (my recommendation), put them in a separate repo, or include them? Including them will slow every git operation.
4. **Timezone for schedule trigger.** Routines UI will show the active timezone — confirm, set to 02:00 ET.
5. **First-run timing.** Manually trigger during the day so you can watch the PR as it opens?

---

## Changelog
- 2026-04-19 — Created. Supersedes launchd approach in `CLAUDE_CODE_COMPILER_SPEC.md` as primary recommendation.