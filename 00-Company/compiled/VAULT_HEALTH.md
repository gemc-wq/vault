# Vault Health Report
*Auto-compiled: 2026-04-21 — Vault Compiler (claude-sonnet-4-6)*

---

## File Counts

| Section | Markdown | Total Files |
|---------|----------|-------------|
| 00-Company | 49 | 60 |
| 01-Wiki | 408+ | 478+ |
| 02-Projects | 199 | 737 |
| 03-Agents | 651 | 671 |

---

## 🔴 Critical Issues

| Flag | File / Path | Detail | Severity |
|------|------------|--------|---------|
| SECURITY_INCIDENT | 04-Shared/active/VAULT_SECRET_INCIDENT_RESPONSE_2026-04-20.md | 144 gitleaks findings on initial push; active credentials exposed; vault automation paused | 🔴 P0 |
| CREDENTIAL_FILES_IN_REPO | 02-Projects/fulfillment-portal/jaymark-bq-key.json | Raw BigQuery service account key tracked in git; DELETE immediately | 🔴 P0 |
| CREDENTIAL_FILES_IN_REPO | 02-Projects/fulfillment-portal/harry-bq-key.json | Raw BigQuery service account key tracked in git; DELETE immediately | 🔴 P0 |
| CREDENTIAL_FILES_IN_REPO | 02-Projects/fulfillment-portal/evri-docs/evri_credentials.md | Credential dump in git; DELETE immediately | 🔴 P0 |
| CREDENTIAL_FILES_IN_REPO | 02-Projects/fulfillment-portal/drew-credentials-extracted.md | Extracted credentials in git; DELETE immediately | 🔴 P0 |

---

## ⚠️ Agent Inactivity

| Flag | Agent | Last Log | Days Inactive | Severity |
|------|-------|----------|---------------|---------|
| AGENT_INACTIVE | Harry | 2026-03-03 (cleaned) | 49 days | 🔴 Critical |
| AGENT_INACTIVE | Hermes | No date-stamped memory logs found | Unknown | ⚠️ Warning |
| AGENT_INACTIVE | Athena | No daily logs in 03-Agents/Athena/memory/ | Unknown | ⚠️ Warning |

---

## ⚠️ Oversized Files (>100KB)

| Flag | File Path | Size | Severity |
|------|-----------|------|---------|
| OVERSIZED | 02-Projects/hermes-deployment/OPERATIONAL_PLAYBOOK_V2.md | ~140KB | ⚠️ |
| OVERSIZED | 02-Projects/listings-db/LISTINGS_PIPELINE_PRD.md | ~116KB | ⚠️ |
| OVERSIZED | 03-Agents/Ava/SOUL_COUNCIL_REVIEW.md | ~106KB | ⚠️ |
| OVERSIZED | Cem's Notes/SOUL_COUNCIL_REVIEW.md | ~106KB | ⚠️ |
| OVERSIZED | Cem's Notes/ATHENA_SELF_AWARENESS_ARCHITECTURE.md | ~97KB | ⚠️ |

---

## ⚠️ Project Folder Issues

| Flag | Detail | Severity |
|------|--------|---------|
| NEW_FOLDER_WITHOUT_REGISTRATION | `02-Projects/_INDEX.md` does not exist — 54 project folders have no canonical registration. This is a §10 violation. Athena should create `_INDEX.md` and register all projects. | 🔴 High |
| POSSIBLE_DUPLICATE | `pulse-dashboard` + `pulse-dashboard-v2` + `pulse-unified` (3 folders, high keyword overlap — "pulse", "dashboard") | ⚠️ Medium |
| POSSIBLE_DUPLICATE | `walmart` + `walmart-lister` + `walmart-listing-audit` + `walmart-review-strategy` (4 folders, all "walmart" stem) | ⚠️ Medium |
| POSSIBLE_DUPLICATE | `prune` + `prune-app` (2 folders, identical stem) | ⚠️ Low |
| POSSIBLE_DUPLICATE | `finance` + `finance-ops` (2 folders, related stem — is `finance` superseded?) | ⚠️ Low |
| POSSIBLE_DUPLICATE | `fulfillment-dashboard` + `fulfillment-portal` (2 folders, related stem) | ⚠️ Low |

---

## ⚠️ Stale Active Projects (14+ days no update, not on-hold)

38 projects last modified 2026-04-07 (14 days ago). See PROJECT_BOARD.md stale section for full list.

---

## ⚠️ Orphan Handoffs (7+ days old, not yet 14-day threshold)

| Flag | File Path | Age | Severity |
|------|-----------|-----|---------|
| ORPHAN_HANDOFF (approaching) | 03-Agents/Athena/handoffs/ATHENA_HANDOFF_BUILD_LISTINGS_PROCUREMENT_2026-04-15.md | 6 days | ⚠️ Watch |
| ORPHAN_HANDOFF (approaching) | 04-Shared/handoffs/FROM_AVA_SHIPPING_TEMPLATE_PROJECT_PLAN.md | 7 days | ⚠️ Watch |
| ORPHAN_HANDOFF (approaching) | 04-Shared/handoffs/FROM_AVA_TO_ATHENA_SALES_ANALYTICS_SKILL.md | 7 days | ⚠️ Watch |
| ORPHAN_HANDOFF (approaching) | 04-Shared/handoffs/FROM_AVA_TO_ATHENA_SHIPPING_TEMPLATE_DASHBOARD_SHAPE.md | 7 days | ⚠️ Watch |
| ORPHAN_HANDOFF (approaching) | 04-Shared/handoffs/FROM_AVA_TO_HERMES_ADVISOR_REVIEW_SHIPPING_TEMPLATE.md | 7 days | ⚠️ Watch |
| ORPHAN_HANDOFF (approaching) | 04-Shared/handoffs/FROM_AVA_TO_HERMES_SOP_SALES_ANALYTICS.md | 7 days | ⚠️ Watch |

---

## ⚠️ Miscellaneous

| Flag | Detail | Severity |
|------|--------|---------|
| DUPLICATE_FILENAMES | 181 filenames appear in multiple locations (from prior compile; unchanged) | ⚠️ Medium |
| STRAY_FILES_IN_PROJECTS_ROOT | Loose .md files at `02-Projects/` root (not in project folders): AI_AUTONOMOUS_IMPACT_ANALYSIS.md, GOHEADCASE_PRODUCT_MATRIX.md, LISTINGS_MANAGEMENT_SYSTEM_SPEC.md, PRICING_OPTIMIZER_SPEC.md, WEEKLY_STRATEGIC_BRIEF_2026-03-06.md | ⚠️ Low |
| OPENCLAW_SECURITY | gemma4:26b exposed with sandbox off + prism web tools enabled (Ava audit 2026-04-19) — needs remediation | 🔴 High |
| MISSING_INDEX | `02-Projects/_INDEX.md` missing — Athena must create this (§10 Project Intake Rule) | 🔴 High |
| PENDING_VALIDATION_NEW | `01-Wiki/_pending/` directory created this run; no prior pending pages existed | ℹ️ Info |

---

## Run Stats

- Files scanned: ~5 (2 new 04-Shared/active files, 1 git commit diff, 2 handoff reviews)
- Promotions to `_pending`: 1 (vault-git-security-posture.md → 08-infrastructure)
- Corrections: 0
- New lint flags: 6 (4 credential files, 1 missing _INDEX.md, 1 OpenClaw security)
- Compiler: claude-sonnet-4-6
- Branch: claude/vault-compile-2026-04-21
