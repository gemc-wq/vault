# Vault Secret Incident Response
Date: 2026-04-20
Status: Active
Owner: Cem

## Situation
Initial Vault push exposed real secrets in the git repository and git history. Gitleaks reported 144 findings, including active credentials in markdown, code, JSON key files, archived memory files, and operational docs.

This is an incident, not a hygiene warning.

## Immediate objectives
1. Rotate or revoke active credentials
2. Remove raw secrets from current working tree
3. Rewrite git history to purge exposed material
4. Re-scan until clean enough to proceed
5. Only then resume Vault automation setup

---

## P0 Rotate / Revoke first

### Confirmed completed
- GitHub tokens revoked

### Next high-priority rotations
1. Google / GCP
   - Gemini API keys
   - exposed BigQuery service account keys
   - any GCP-linked API keys or service-account auth

2. AWS
   - any IAM/API credentials if present in incident set

3. Supabase
   - service-role key
   - any admin-grade credentials

4. Slack
   - bot token
   - app token

5. Shopify
   - admin API tokens

6. BigCommerce
   - access token
   - client secret

7. Walmart
   - client secret

8. Anthropic
   - exposed API key

9. Other vendor/API keys
   - Firecrawl
   - Apify
   - Gamma
   - NVIDIA
   - Airweave
   - any other live key found in leak report

---

## DELETE now
These are primarily credential-bearing files or extracted dumps and should be removed from the repo, not preserved.

- `02-Projects/fulfillment-portal/jaymark-bq-key.json`
- `02-Projects/fulfillment-portal/harry-bq-key.json`
- `02-Projects/fulfillment-portal/evri-docs/evri_credentials.md`
- `02-Projects/fulfillment-portal/drew-credentials-extracted.md`

Potential additional delete candidates after review:
- any other raw `*.json` key files
- files whose main value is passwords, API keys, or extracted credentials
- duplicated archived notes that exist only as secret-bearing snapshots

---

## SCRUB and keep
These are real docs/code/assets and should be cleaned, not deleted.

### Core docs / reference files
- `03-Agents/Ava/TOOLS.md`
- `01-Wiki/21-ava-archive/TOOLS.md`
- `01-Wiki/17-harry-workspace/MEMORY (1).md`
- `01-Wiki/17-harry-workspace/daily/2026-02-16.md`
- `01-Wiki/17-harry-workspace/daily/2026-02-17.md`
- `01-Wiki/17-harry-workspace/daily/2026-02-20.md`
- `01-Wiki/23-drew-handover/CLOUD_AND_DNS_CREDENTIALS.md`
- `03-Agents/Ava/memory/2026-03-03.md`
- `03-Agents/Ava/memory/2026-03-04.md`
- `03-Agents/Ava/memory-archive/2026-03-03.md`
- `03-Agents/Ava/memory-archive/2026-03-04.md`
- related cleaned/duplicated memory derivatives containing the same tokens

### Active project docs
- `02-Projects/amazon-report-middleware/PRD.md`
- `02-Projects/amazon-report-middleware/HANDOFF.md`
- `02-Projects/amazon-data-analytics/SOP_SHIPPING_TEMPLATE_OPTIMIZATION.md`
- `02-Projects/dashboard-product-entry/DEV_BRIEF.md`
- `02-Projects/pulse-dashboard/CODEX_BRIEF.md`
- `02-Projects/shopify-repush/SHOPIFY_PRODUCT_SPEC_V2.md`
- `02-Projects/supabase-rls-fix/RLS_REMEDIATION.md`
- `01-Wiki/31-listings-management/SOP_WEEKLY_ACTIVE_LISTINGS_AUDIT.md`
- `00-Company/Infrastructure/ATHENA_ZEUS_INTEGRATION.md`

### Code files needing env migration
- `02-Projects/brain-memory-layer/brain-memory-layer/brain_search.py`
- `02-Projects/brain-memory-layer/brain-memory-layer/sync_brain.py`
- `02-Projects/command-center/setup.py`
- `02-Projects/new-products/scripts/gemini_image_gen.py`
- `02-Projects/shopify-repush/prepare_shopify_data.py`
- `02-Projects/walmart-lister/walmart_api_uploader.py`
- `02-Projects/walmart-lister/walmart_lister.py`

### Scrub rule
Replace raw values with one of:
- env var names
- placeholders like `[REDACTED]`
- storage references only, no live value

---

## ENV migration direction

### Move to env / secret storage
- API keys
- DB passwords
- service-role keys
- access tokens
- OAuth client secrets
- webhook/shared secrets

### Keep in docs only as references
Use patterns like:
- `Stored in macOS Keychain`
- `Stored in Secret Manager`
- `Use ENV var: SUPABASE_SERVICE_ROLE_KEY`
- `Rotate quarterly`

Never keep raw values in docs.

---

## Git history rewrite plan
Do this only after rotation/revocation work and working-tree cleanup are done.

### Preferred approach
Use `git filter-repo` to remove or replace secret-bearing paths/content.

### High-level steps
1. commit the cleaned working tree
2. install `git-filter-repo` if needed
3. remove raw key files entirely from history
4. purge sensitive content from docs/code history where necessary
5. force-push cleaned history
6. re-run gitleaks

### Reminder
History rewrite without prior rotation is not enough.
If a secret was exposed, rotate it first.

---

## Re-scan gate
Do not resume Vault automation until:
- major active secrets have been rotated
- raw key files are removed
- scrubbed docs/code are committed
- history has been rewritten if needed
- gitleaks results are materially reduced and understood

---

## Suggested execution order tonight
1. rotate Google / GCP secrets
2. rotate AWS if any are live in findings
3. rotate Slack, Supabase, Shopify, BigCommerce, Walmart, Anthropic
4. delete raw key and credential-dump files
5. scrub active docs and code
6. commit cleanup
7. rewrite history
8. force-push
9. re-run gitleaks
10. only then continue Vault setup
