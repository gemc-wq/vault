---
topic: vault-git-security-posture
last_updated: 2026-04-21
last_updated_by: compiler
source_agents: [Cem, Ava]
source_files:
  - 04-Shared/active/VAULT_SECRET_INCIDENT_RESPONSE_2026-04-20.md
  - 04-Shared/active/SECURITY_HARDENING_BEFORE_PROGRESS.md
  - 00-Company/VAULT_EXECUTE_NOW_V2.md
confidence: high
review_status: pending PR review
---

# Vault Git Security Posture

## Incident Summary (2026-04-20)

Initial vault push exposed 144 secrets (gitleaks findings). Vault automation setup is **paused** until remediation is complete.

**GitHub tokens:** Rotated ✅
**Remaining rotations required:**
- Google / GCP (Gemini API keys, BigQuery service account keys)
- AWS (IAM/API credentials if present)
- Supabase (service-role key, admin credentials)
- Slack (bot token, app token)
- Shopify (admin API tokens)
- BigCommerce (access token, client secret)
- Walmart (client secret)
- Anthropic (API key)
- Other: Firecrawl, Apify, Gamma, NVIDIA, Airweave

## Files to Delete from Repo

- `02-Projects/fulfillment-portal/jaymark-bq-key.json`
- `02-Projects/fulfillment-portal/harry-bq-key.json`
- `02-Projects/fulfillment-portal/evri-docs/evri_credentials.md`
- `02-Projects/fulfillment-portal/drew-credentials-extracted.md`

## Remediation Order (Cem's plan)

1. Rotate Google / GCP secrets
2. Rotate AWS if any are live in findings
3. Rotate Slack, Supabase, Shopify, BigCommerce, Walmart, Anthropic
4. Delete raw key and credential-dump files
5. Scrub active docs and code (replace raw values with env var references or `[REDACTED]`)
6. Commit cleanup
7. Rewrite history with `git filter-repo`
8. Force-push
9. Re-run gitleaks
10. Only then continue Vault automation setup

## Vault Automation Rollout Decision (v2 — 2026-04-20)

**Prior approach:** Optimistic automation. **New approach:** Manual-first hardening.

**Locked principles:**
1. Knowledge is syncable. Secrets are not.
2. Manual review beats convenience during first rollout.
3. Regex redaction is hygiene, not a security boundary.
4. No new automation until secret scan is clean enough to proceed.
5. Any file category that can contain credentials is excluded by default.

**Rollout sequence:** Secret scan → Git hardening → Secret migration → Session capture (local-first) → Create compiler routine → Manual-first trial runs (5 runs) → Enable schedule → Smoke test

## First 5 Compiler Runs — Manual Review Required

Per VAULT_EXECUTE_NOW_V2.md, the first 5 routine compiler runs must be reviewed manually before any PR is merged. Review checklist per run:
- No secret material in PR diff
- No wrong promotions into wiki
- No destructive or misleading edits

## OpenClaw Security Audit — 2026-04-19

Weekly security audit found **1 critical + 5 warnings**:

| Severity | Finding |
|----------|---------|
| 🔴 Critical | `ollama/gemma4:26b` exposed with sandbox off + web tools enabled (`prism`) |
| ⚠️ Warning | `gateway.control_ui.insecure_auth` |
| ⚠️ Warning | `config.insecure_or_dangerous_flags` |
| ⚠️ Warning | `tools.exec.security_full_configured` |
| ⚠️ Warning | `multi_user_heuristic` |
| ⚠️ Warning | `trusted_proxies_missing` (expected for local setup) |

## Credential Storage Rules

- Runtime code reads from `.env.local` or secret store — never from vault markdown
- Vault docs reference credential location only (e.g., `Stored in macOS Keychain`)
- Never store raw credential values in vault-tracked files
- Rotate critical secrets quarterly
