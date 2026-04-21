# Handoff: Sales Analytics Skill Doc
**From:** Ava | **To:** Athena | **Date:** 2026-04-14 | **Priority:** Ready to use

## What this is

Sales Analytics SOP written today — covers the full reporting hierarchy, conversion framework, and weekly report structure for Hermes. This is the source material for `skills/sales-analytics/SKILL.md`.

## Files ready

1. **Main SOP:** `Vault/01-Wiki/02-sales-data/SOP_SALES_DATA_REVIEW_AND_DASHBOARDS.md`
   - Full reporting hierarchy (Device → Product Type × Device → License → Design Parent → Design Child → SKU)
   - Conversion segmentation: UK vs US separate, FBA vs FBM, shipping template layer
   - PULSE framework + opportunity scoring + momentum scoring
   - Weekly report structure (6 sections)
   - Conversion action playbook (symptom → fix → owner table)
   - KPI roadmap (current vs coming online)

2. **Skill card copy:** `workspace/memory/skills/SKILL_SALES_ANALYTICS_REPORTING.md`

3. **PULSE specs (reference):**
   - `Vault/02-Projects/pulse-unified/PULSE_SPEC_V4.md`
   - `Vault/02-Projects/pulse-unified/PULSE_V2_SPEC.md`
   - `Vault/01-Wiki/25-pulse-dashboard/` (conversion baselines)

4. **Sales Dashboard V2 specs:** `Vault/01-Wiki/02-sales-data/sales-dashboard-v2-specs.md`

## Key decisions baked in (Cem confirmed today)

- **Hierarchy correction:** Removed redundant "Design" level. Now: License → Design Parent → Design Child
- **Stockable unit = Product Type × Device** — not device alone
- **UK vs US always separate** in conversion analysis — never aggregate
- **FBA vs FBM segmentation** via shipping template is the highest-priority conversion split once data flows
- **Content drivers (images, copy, keywords) = out of Hermes scope** — refer to Content skill

## For Athena's skills folder

Suggest mapping to your proposed structure as:
- `sales-analytics/SKILL.md` ← distil from the main SOP above
- `sales-analytics/reporting-structure.md` ← the hierarchy section
- `sales-analytics/decision-framework.md` ← the conversion action playbook

SKU parsing rules are already canonical at `00-Company/SKU-Parsing/SKU_PARSING_RULES.md` — no need to duplicate.

## Also: middleware docs filed today

Full technical handoff + PRD for the Amazon Report Middleware now at:
- `Vault/02-Projects/amazon-report-middleware/HANDOFF.md`
- `Vault/02-Projects/amazon-report-middleware/PRD.md`
- `Vault/02-Projects/amazon-report-middleware/CHANGES_LOG.md`

These feed into `data-pipeline/middleware-usage.md` in your skills structure.

**Status:** All files are in Vault. Ready for Athena to synthesise into skill docs.
