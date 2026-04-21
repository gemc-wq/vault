# Security Hardening Before Progression

Date: 2026-04-20
Owner: Cem + Ava
Status: Pending scan before further vault automation

## Recommended revised action plan

### Step 1, do now, ~5 min
Run a secret scan on the just-pushed Vault repo.

On Mac Studio:

```bash
cd /Users/openclaw/Vault
brew install gitleaks # or trufflehog
gitleaks detect --source . --verbose
```

If clean:
- proceed to Step 2 with confidence

If findings:
- stop
- rotate credentials
- purge history with git filter-repo before doing anything else

### Step 2, ~20 min
Write a hardened V2 runbook plus secret migration plan into the Vault.

### Step 3, ~30 min
Install pre-push hooks and migrate any discovered secrets to `.env` per the plan.

## What V2 should contain

### Mandatory `.gitignore` additions
Beyond the already-discussed exclusions, add:

- `.env`, `.env.*`, `*.env`
- `**/secrets/`
- `**/credentials*`
- `**/*_token*`, `**/*_key*` (file patterns, not just env vars)
- `*.db`, `*.sqlite`, `*.sqlite3`
- `*.pickle`, `*.pkl`
- `**/exports/raw/`
- `**/downloads/`
- any file over 10MB, with git-lfs only if truly needed

### Pre-push hook
Use `gitleaks` or `git-secrets` before every push.

If a match is found:
- push blocks
- manual override requires explicit `--no-verify`
- override remains visible in shell history for audit

### Session capture redaction layer
Before any session file lands in `03-Agents/*/sessions/`, run a redaction step that:

- strips anything matching `sk-*`, `xoxb-*`, `Bearer *`, `api_key=*`, `password=*`
- replaces matches with `[REDACTED:type]`
- writes matches to a separate audit log so triggers are visible

### Manual-first flags
For operations previously treated as automatic:

- first 5 compile Routine runs: manual approval before commit
- first RAG index build: manual approval before publishing
- first session capture: manual review before committing to repo

## What `SECRET_MIGRATION_PLAN` should contain

### Categories to audit
- app runtime secrets, including Supabase URL/keys, OpenAI/Anthropic API keys, webhook URLs with embedded tokens
- OAuth credentials, including Xero UK, Xero US, Gmail, Google Drive, Telegram bot token
- database connection strings, including Supabase service role key and BigQuery service account JSON
- third-party tool keys, including A2X until sunset, courier API keys, licensor portal credentials
- agent-specific auth, including OpenRouter keys for Kimi K2.5 and OpenClaw session tokens

### Migration pattern per category
- audit current location, file and commit
- rotate if exposed in git history
- move to `.env.local` on Mac Studio and laptop where appropriate
- document references only in `CREDENTIALS_REGISTRY.md`, variable names only, never values
- set quarterly rotation schedule for critical secrets

## Recommendation
Proceed in this order:

1. scan existing repo and rotate anything exposed
2. write V2 runbook and migration plan into Vault
3. install pre-push hooks
4. migrate remaining hardcoded credentials to `.env`
5. re-run scan to confirm clean state
6. resume compile Routine setup

## Planning impact
This likely pushes compile Routine setup by 1 to 2 days. That is acceptable. Security debt compounds faster than feature debt.

## Pending user decision
- scan first, then write docs
- or write V2 and migration plan immediately after scan confirmation
