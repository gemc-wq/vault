# Skill: Security Audit
**Owner:** Sentinel | **Schedule:** Daily 4AM ET + triggered on GitHub push detection
**Priority:** P0 — any finding escalates immediately
**Model:** Gemma 4 for scanning, Haiku for assessment

---

## Purpose

Scan all code repositories, vault files, and deployed endpoints for exposed API keys, secrets, credentials, and security misconfigurations. Prevent accidental exposure of business-critical credentials.

---

## Scan Targets

### 1. Git Repositories (all repos in /Users/openclaw/projects/)

**Pattern matching** — scan all files for:

```
# API Key Patterns
sk-[a-zA-Z0-9]{20,}           # OpenAI / Anthropic keys
AKIA[A-Z0-9]{16}              # AWS access keys
AIza[a-zA-Z0-9_-]{35}         # Google API keys
ghp_[a-zA-Z0-9]{36}           # GitHub personal access tokens
gho_[a-zA-Z0-9]{36}           # GitHub OAuth tokens
xoxb-[0-9]{10,}               # Slack bot tokens
xoxp-[0-9]{10,}               # Slack user tokens
Bearer [a-zA-Z0-9_-]{20,}     # Bearer tokens (in code, not headers)
supabase_service_role_key      # Supabase service keys (should NEVER be in frontend)
password\s*=\s*['"][^'"]+      # Hardcoded passwords
PRIVATE KEY                    # Private key blocks

# Ecell-Specific
79e2ca622a7e                   # OpenClaw gateway token (partial match)
8741359019:AAG                 # Telegram bot token (partial match)
```

**Check .gitignore** — every repo must exclude:
- `.env*`
- `*.key`, `*.pem`
- `credentials.json`, `token.json`, `client_secret*.json`
- `data/gmail_token.json`
- `*_token.json`

**Git history scan** (weekly only — expensive):
```bash
git log -p --all -S "sk-" --diff-filter=D  # Keys added then "deleted"
git log -p --all -S "AKIA" --diff-filter=D
```
If found in history: key must be rotated, not just removed from HEAD.

### 2. Vault Files (/Users/openclaw/Vault/)

Scan all .md files for credential patterns. Known acceptable locations:
- `TOOLS.md` files (document where keys are stored, not the keys themselves)
- Anything else with an actual key value = P0 alert

### 3. ZEUS Agent Data (/Users/openclaw/zeus-agent/)

Critical files to verify are NOT exposed:
- `.env` — must not be committed
- `data/gmail_token.json` — must not be committed
- `data/memory.db` — contains conversation data

### 4. Deployed Endpoints

Check for unauthenticated access:
```bash
# ecell.app endpoints — should require auth
curl -s -o /dev/null -w "%{http_code}" https://ecell.app/api/health

# Supabase — anon key should have RLS
# Verify no tables have RLS disabled with public read
```

### 5. Supabase RLS (Row Level Security)

Check that all tables with sensitive data have RLS enabled:
```sql
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND rowsecurity = false;
```
Any table with `rowsecurity = false` that contains business data = WARNING.

---

## Processing Flow

```
Daily 4AM ET:
  1. For each repo in /Users/openclaw/projects/:
     a. git pull (if remote exists)
     b. Scan HEAD for secret patterns
     c. Check .gitignore is comprehensive
     d. Check for new .env files not in .gitignore
  2. Scan Vault for credential patterns
  3. Verify ZEUS .env and tokens not exposed
  4. Check deployed endpoints for auth
  5. Compile findings

  If ANY secret found:
    → P0 IMMEDIATE alert to Athena → Cem
    → Include: which file, which key type, exposure risk
    → Recommend: rotate key, add to .gitignore, remove from history

  If no secrets found:
    → Log clean scan, no alert (silent)

Weekly (Sunday 3AM ET):
  6. Git history deep scan for removed-but-still-in-history keys
  7. Supabase RLS audit
  8. Full endpoint auth check
```

---

## Known Credentials to Protect

| Credential | Location (should be) | Risk if Exposed |
|------------|---------------------|-----------------|
| OpenClaw Gateway Token | zeus-agent/.env | Full agent access |
| Telegram Bot Token | zeus-agent/.env | Bot hijack |
| Gmail OAuth Token | zeus-agent/data/gmail_token.json | Email access |
| Google Client Secret | ~/.config/gws/client_secret.json | OAuth impersonation |
| Supabase Service Key | ecell-app/.env.local | Full DB access |
| BigQuery Service Account | ~/.config/gcloud/ | Data warehouse access |
| Amazon SP-API keys | TBD (being set up) | Marketplace access |
| Xero API keys | Harry's iMac | Financial data |
| Shopify Admin API | ecell-app/.env | Store admin |

---

## Alert Format

```
--- SENTINEL SECURITY ALERT ---
Severity: CRITICAL
Skill: security-audit
What: {key type} found in {file path}
Detail: Line {N} of {file} contains what appears to be a {key type}
Exposure: {committed to git / in public file / in vault}
Risk: {what an attacker could do with this key}
Action: 
  1. Rotate the key immediately
  2. Add file/pattern to .gitignore
  3. If committed to git: purge from history with git filter-repo
---
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Scan coverage | 100% of repos, 100% of vault .md files |
| Time to detect new exposure | <24 hours (daily scan) |
| False positive rate | <5% (tune patterns over time) |
| Key rotation response time | <1 hour after alert |

---

## Changelog
- 2026-04-13 — Created. Pattern list, scan targets, known credentials inventory, RLS check.
