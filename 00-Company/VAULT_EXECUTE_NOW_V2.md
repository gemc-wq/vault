# Execute Now — Runbook V2
**Created:** 2026-04-20 | **Status:** DRAFT HARDENED V2
**Purpose:** safer replacement for the Apr 19 runbook after real-world git hygiene and secret-handling gaps were exposed during initial execution.

---

## Executive Summary

This V2 keeps the original objective, getting Vault git sync, session capture, and compiler routines live, but changes the rollout posture from optimistic automation to manual-first hardening.

### What changed from V1
- broader `.gitignore` coverage
- mandatory pre-push audit gates
- no assumptions that the Vault is "mostly markdown" or inherently safe to push
- raw session capture is treated as sensitive local material first, not as automatically publishable vault knowledge
- Obsidian Git starts manual-push first
- secret migration is a prerequisite workstream, not an optional cleanup later

### Non-negotiable rule
If the repo contains exposed secrets in working tree or git history, stop setup work and remediate before enabling more automation.

---

## Locked principles for this rollout

1. **Knowledge is syncable. Secrets are not.**
2. **Manual review beats convenience during first rollout.**
3. **Regex redaction is hygiene, not a security boundary.**
4. **No new automation until secret scan is clean enough to proceed.**
5. **Any file category that can contain credentials, auth state, or large machine data is excluded by default.**

---

## Sequence Overview

```text
PART 0  — Secret scan + exposure triage         REQUIRED FIRST
PART 1  — Git hardening foundation              PREREQUISITE
PART 2  — Secret migration planning             REQUIRED BEFORE BROADER AUTOMATION
PART 3  — Session capture, local-first          AFTER HARDENING
PART 4  — Create compiler routine               AFTER CLEAN BASELINE
PART 5  — Manual-first trial runs               BEFORE SCHEDULE ENABLEMENT
PART 6  — Enable schedule                       ONLY AFTER REVIEW GATES PASS
PART 7  — Smoke test                            3 to 5 days
```

---

## PART 0 — Secret Scan + Exposure Triage

### 0.1 Run a local secret scan immediately

```bash
cd /Users/openclaw/Vault
brew install gitleaks
gitleaks detect --source . --verbose
```

Alternative if preferred:
```bash
brew install trufflehog
trufflehog filesystem .
```

### 0.2 If findings are clean enough to proceed
You may continue to Part 1.

### 0.3 If findings are not clean
Stop and do this in order:
1. identify which secrets are real and active
2. rotate exposed credentials
3. remove them from working tree
4. if already committed, purge git history with `git filter-repo` or equivalent
5. re-run scan before resuming

### 0.4 Minimum acceptance gate before continuing
- no active API keys sitting in tracked markdown/config/code files
- no DB passwords or service-role credentials in tracked files
- no unreviewed auth/session dumps in tracked folders

---

## PART 1 — Git Hardening Foundation

### 1.1 Pre-flight checks

```bash
git --version
jq --version || brew install jq
ssh -T git@github.com
```

Expected SSH result:
- authenticated as `gemc-wq`

### 1.2 Create the GitHub repo
Create private repo:
- owner: `gemc-wq`
- name: `ecell-vault`
- initialize empty

### 1.3 Git init and identity

```bash
cd /Users/openclaw/Vault

if [ ! -d .git ]; then
  git init
  git branch -M main
fi

git config user.name "Cem"
git config user.email "cem@ecellglobal.com"
```

### 1.4 Harden `.gitignore`

Use a broader baseline than V1.

```bash
cat > .gitignore << 'EOF'
# Obsidian
.obsidian/
!.obsidian/app.json
!.obsidian/appearance.json
!.obsidian/core-plugins.json
.trash/
.Trashes

# macOS / editor noise
.DS_Store
._*
*.tmp
*.swp
*~

# Node / build artefacts
node_modules/
dist/
build/
coverage/

# Secrets / auth material
.env
.env.*
*.env
**/secrets/
**/credentials*
**/*_token*
**/*_key*
*.pem
*.key
*.p12
*.mobileprovision

# Databases / raw exports / auth-state-like files
*.db
*.sqlite
*.sqlite3
*.sql
*.csv
*.tsv
*.xlsx
*.xls
*.parquet
*.pickle
*.pkl
*.gz
*.zip
*.tar
*.7z
*.jsonl

# Session temp / capture artefacts
03-Agents/*/sessions/*.tmp
03-Agents/Cem-Code/.capture-state

# Known heavy project folders
02-Projects/zero-codebase/
02-Projects/ppc-autoresearch/
02-Projects/amazon-data-analytics/dashboard/
02-Projects/unified-listings/data/
**/exports/raw/
**/downloads/

# Logs
/var/log/
**/logs/
EOF
```

### 1.5 Mandatory pre-push audit gate
Before any first push or large sync, run all of these:

```bash
cd /Users/openclaw/Vault

# Large files
find . -type f -size +25M

# Review staged file names
git diff --cached --name-only

# Look for likely risky tracked patterns
git ls-files | grep -Ei '(\.env|secret|token|oauth|\.db$|\.sqlite|\.csv$|\.tsv$|\.xlsx$|\.pem$|\.key$)' || true

# Confirm ignores are really active for representative bad paths
git check-ignore -v 02-Projects/zero-codebase/README.md || true
git check-ignore -v 02-Projects/amazon-data-analytics/dashboard/listings.db || true
```

### 1.6 Optional but recommended: secret scan before push

```bash
gitleaks detect --source . --verbose
```

### 1.7 First commit and push
Only do this after the above audit looks clean.

```bash
git add -A
git status
git commit -m "Initial vault commit — hardened baseline"
git remote add origin git@github.com:gemc-wq/ecell-vault.git 2>/dev/null || git remote set-url origin git@github.com:gemc-wq/ecell-vault.git
git push -u origin main
```

### 1.8 Part 1 checkpoint
- SSH auth works
- repo is private
- heavy folders are ignored
- no large tracked files remain
- secret scan is acceptable enough to continue

---

## PART 2 — Secret Migration Planning

This is no longer optional.

Before broader automation, create and review a secret migration plan that covers:
- app runtime secrets
- API keys
- OAuth credentials
- DB connection strings
- service account files
- human reference credentials currently sitting in markdown

### Required outcome
A file like `SECRET_MIGRATION_PLAN.md` exists and identifies:
- current location
- target storage
- whether rotation is required
- migration order
- rollback cautions

### Principle
- runtime code reads from `.env.local` or a proper secret store
- docs reference secret location, never store the secret value
- shared vault content should contain names, not secret material

---

## PART 3 — Session Capture, Local-First

### Important change from V1
Do **not** treat raw Cem or Claude Code sessions as automatically safe to commit into the Vault.

### Recommended model
1. raw session capture lands in a private local non-git directory first
2. a sanitizer/redaction pass runs
3. only reviewed or summarized output is promoted into Vault

### Required warning
Regex redaction is best-effort only. It must not be treated as complete protection.

### Suggested local paths
- raw capture: `~/Library/Application Support/Cem-Code-Sessions/`
- logs: `~/Library/Logs/cc-session-capture/`
- reviewed vault output: `03-Agents/Cem-Code/sessions/`

### First-run rule
For the first session capture:
- manual review before any commit
- if secrets appear, stop and tighten capture/redaction process

---

## PART 4 — Create the Compiler Routine

Only proceed after Parts 0 to 3 are in acceptable shape.

### Guardrail
Do not enable unattended scheduling on day one just because the UI works.

### Manual-first requirement
The first several routine runs should be human-reviewed before any commit/PR is merged.

---

## PART 5 — Manual-First Trial Runs

### Required review window
For the first 5 routine runs:
- review output manually
- inspect PR contents manually
- confirm no secret leakage
- confirm no wrong promotions into wiki or agent memory

### Fail conditions
Pause rollout if any run:
- exposes secret material
- misclassifies private scratch content as durable knowledge
- generates destructive or misleading edits

---

## PART 6 — Enable Schedule

Only enable schedule after:
- secret scan is clean enough
- at least 2 successful manual review cycles complete
- first capture flow has been reviewed
- no high-risk git hygiene issues remain

### Timezone note
Do not rely on assumptions. Verify whether the scheduler UI uses local time or UTC before setting the cron.

---

## PART 7 — Smoke Test

### Recommended duration
3 to 5 days

### Success conditions
- no secret exposure in PRs
- no large file regressions
- no accidental session dump commits
- compiler output remains reviewable and useful

---

## Rollback Plan

### Disable schedule
Disable the schedule trigger in the routine UI immediately.

### Disable session capture
Unload the local job and stop promotion into Vault.

### Reset git state if needed
```bash
cd /Users/openclaw/Vault
git log --oneline
git reset --hard <safe-commit>
```

If history itself is contaminated by secrets, use history rewrite and credential rotation, not just reset.

---

## What is explicitly out of scope for this first hardened rollout
- broad automatic secret rewrites without review
- unattended publish-on-capture session workflows
- git-lfs adoption for convenience before hygiene is stable
- expanding weekly/monthly routines before nightly is safe

---

## Final sanity check
Proceed only if these are true:
- secret scan done
- git ignore hardened
- no active secrets intentionally tracked
- no large tracked data files left
- manual review bandwidth available
- willingness to pause if first runs show leakage

If not, stop and harden first.
