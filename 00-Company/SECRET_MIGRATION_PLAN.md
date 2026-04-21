# Secret Migration Plan
**Date:** 2026-04-20
**Status:** Draft
**Owner:** Cem + Ava

---

## Objective
Move hardcoded credentials, API keys, passwords, service-role secrets, and auth material out of markdown/code/config files and into appropriate secret storage without breaking current workflows.

This is a controlled migration, not a blind search-and-replace exercise.

---

## Core rules

1. Never commit real secrets into git again.
2. If a secret may already be in git history, rotate first, then clean history.
3. Runtime code should read from environment variables or a proper secret manager.
4. Human-readable docs should contain references and variable names, not secret values.
5. Markdown files that currently act as credential notebooks must be replaced with a safer operating pattern.

---

## Secret categories and target storage

### 1. App runtime secrets
Examples:
- Supabase URLs and keys
- OpenAI / Anthropic / Gemini / OpenRouter keys
- webhook URLs with embedded auth
- service-role credentials used by scripts/apps

**Target:**
- `.env.local` for local app execution
- cloud secret manager for deployed services
- `.env.example` for placeholders only

**Action:**
- identify runtime consumers
- replace literals with env reads
- create documented variable names
- confirm local/dev/prod separation where needed

---

### 2. OAuth credentials
Examples:
- Xero UK / Xero US OAuth credentials
- Gmail / Google Drive tokens
- Telegram bot tokens
- other refresh tokens or client secrets

**Target:**
- secret manager or OS keychain for real tokens
- `.env.local` only when app runtime absolutely requires it and local risk is accepted
- docs store reference only, never value

**Action:**
- map token ownership and refresh model
- rotate anything exposed in git history
- remove raw values from markdown

---

### 3. Database credentials and connection strings
Examples:
- DB passwords
- connection URIs with embedded auth
- Supabase service-role key
- BigQuery service account JSON

**Target:**
- `.env.local` for local runtime if needed
- cloud secret manager for deployed services
- service account JSON stored outside repo

**Action:**
- extract credentials from tracked files
- replace with env var names
- separate read-only vs admin privileges
- prioritize rotation for service-role credentials

---

### 4. Third-party tool keys
Examples:
- courier APIs
- A2X or similar tool keys
- licensor portal credentials
- automation/webhook integrations

**Target:**
- secret manager or `.env.local` depending on runtime need
- reference-only documentation in vault

**Action:**
- inventory per tool
- classify whether still active
- retire stale keys where possible

---

### 5. Agent-specific auth and operational tokens
Examples:
- OpenClaw tokens
- session tokens
- OpenRouter / Kimi auth
- agent-local service secrets

**Target:**
- local config files outside git
- secret manager for shared automation
- keychain for workstation-only secrets where appropriate

**Action:**
- identify which agents need runtime access
- reduce duplication across markdown memory files
- remove raw values from agent docs

---

### 6. Human credential notebook content
Examples:
- markdown files holding usernames/passwords/API keys directly
- operational notes that include full tokens for convenience

**Target:**
- 1Password / Keychain / dedicated secure store
- a reference file such as `CREDENTIALS_REGISTRY.md` containing only:
  - system name
  - owner
  - where stored
  - variable names if applicable
  - rotation policy

**Action:**
- do not blindly delete before replacement exists
- create safer reference workflow first
- then scrub raw values from markdown

---

## Migration workflow

### Phase 1 — Audit
For each secret-like item found:
- file path
- secret type
- active or stale
- already committed to git history or not
- target storage
- rotation required or not

### Phase 2 — Triage
Priority order:
1. service-role keys and DB admin credentials
2. OAuth refresh/client secrets
3. broad-scope API keys
4. bot tokens and webhook auth
5. lower-risk local-only credentials

### Phase 3 — Migrate runtime dependencies
- patch scripts/apps to read env vars
- create `.env.example`
- test before deleting old path

### Phase 4 — Scrub documentation
- replace values with placeholders
- keep reference metadata only
- update docs to explain retrieval path

### Phase 5 — Rotate exposed secrets
If a secret was ever pushed into git:
- rotate it
- confirm replacement works
- then purge history if warranted by risk

### Phase 6 — Re-scan
Run gitleaks or equivalent again and confirm acceptable state.

---

## Suggested file pattern

### `.env.example`
Should contain names only, for example:
```env
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
TELEGRAM_BOT_TOKEN=
XERO_CLIENT_ID=
XERO_CLIENT_SECRET=
```

### `CREDENTIALS_REGISTRY.md`
Should contain references only, for example:
- Secret name
- Used by
- Storage location
- Rotation cadence
- Last rotated date

Never include secret values.

---

## Operational cautions

1. Some markdown files are currently dual-purpose, both documentation and secret storage. Do not mass-edit them without preserving needed reference context.
2. Some code paths may silently depend on hardcoded secrets. Test before removing literals.
3. Service account JSON files are especially risky and should never be tracked.
4. `.env` files themselves must be gitignored everywhere.
5. If a secret is exposed publicly or to any shared repo, assume rotation is required.

---

## Immediate next actions

1. run secret scan on current Vault repo
2. classify findings into the categories above
3. identify exposed-in-history credentials requiring rotation
4. patch runtime code/config to env vars where straightforward
5. create `.env.example` and `CREDENTIALS_REGISTRY.md`
6. scrub markdown notebooks after secure replacement path exists
7. re-run scan

---

## Definition of done
Migration is not done when secrets are merely hidden from view.
It is done when:
- runtime uses env or secret manager
- docs contain no raw values
- `.env` is ignored
- exposed secrets are rotated
- scans are acceptably clean
- future pushes are protected by hooks
