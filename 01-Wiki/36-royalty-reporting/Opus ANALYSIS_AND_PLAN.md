# Royalty Reporting Automation — Analysis, Gap Assessment & Implementation Plan

**Prepared by:** Claude (Anthropic) — peer review of ChatGPT 5.4 output  
**Date:** 2 April 2026  
**Status:** Plan mode — for Cem's review before execution  
**Source documents reviewed:**  
- `README.md`  
- `ROYALTY_CALCULATION.md`  
- `LEGACY_LOGIC_EXTRACTION.md`  
- `IMPLEMENTATION_MAP.md`

---

## Executive summary

The four documents form a strong discovery foundation. They correctly identify the three-layer architecture (source extractor → legacy logic engine → converter app), map the PHP rule engine's complexity, propose a sensible Supabase/BigQuery target schema, and recommend a pragmatic phased approach. However, **execution would stall** on several critical gaps: the converter app is inaccessible, no parity test artifacts exist, the unit-royalty formula is flagged but unresolved, and key technical decisions (runtime, hosting, auth) are deferred. This plan fills those gaps with concrete actions, owners, and sequencing.

### Strengths of the existing documents
- Thorough legacy PHP logic extraction — SKU rewrites, description mappings, exclusion rules all identified
- Correct identification that licensor-facing SKU ≠ internal analytics SKU
- Solid target schema design for Supabase/BQ with 11 normalised config tables
- Pragmatic "fast path first" delivery strategy
- Good validation SOP with row-level and batch-level checks
- Real edge cases documented from NHL sample (country naming, FBA rows, encoding noise)

### Critical gaps requiring immediate resolution
1. **Converter app is a black box** — repo inaccessible, I/O contract unknown
2. **No parity test kit** — no matched input/config/output triple exists for any licensor
3. **Unit royalty formula is ambiguous** — `Quantity / rate` vs `Quantity × rate`
4. **Brand-to-license bridge is fragile** — `brands.Label → f_property_name` relies on exact string match with no validation layer
5. **Exchange rate source undetermined** — legacy Sage vs BigQuery vs external API not decided
6. **No error recovery or idempotency design** — batch failures produce orphaned state
7. **Missing licensor coverage inventory** — no list of which licensors have working configs vs need new ones

---

## Gap analysis

### Category 1 — Blockers (must resolve before any build)

| # | Gap | Impact | Resolution |
|---|-----|--------|------------|
| G1 | Converter app repo inaccessible (`gemc-wq/royalty-report-converter` returns 404) | Cannot build batch wrapper without knowing input format, CLI interface, config schema, output naming | Cem to provide: corrected repo URL, or zip/local copy, or grant access to current GitHub token |
| G2 | No parity test artifacts for any licensor | Cannot validate that the new pipeline reproduces legacy output | Collect for NHL: (a) legacy export CSV, (b) JSON config used, (c) final output file, all for same date range |
| G3 | Unit royalty formula ambiguity: `Quantity / f_royalty_rate` in legacy PHP vs `SUM(quantity) * applicable_rate` in BigQuery SQL | Could produce incorrect royalty amounts for unit-rate licensors | Pull one real unit-rate licensor invoice, manually verify which formula matches, document the correct one |
| G4 | No inventory of which licensors have working JSON configs | Cannot scope Phase 1 batch — don't know coverage | Audit the converter app's config directory; list every JSON config with its licensor, last-updated date, and completeness status |

### Category 2 — Design gaps (must resolve before production)

| # | Gap | Impact | Resolution |
|---|-----|--------|------------|
| G5 | Brand-to-license bridge (`brands.Label → f_property_name`) has no validation or fuzzy-match fallback | Rows silently drop when Label doesn't exactly match | Add a `royalty_brand_bridge` validation table with canonical mappings and an exception report for unmatched brands |
| G6 | Exchange rate source not finalised | Different sources (Sage, HMRC, XE API) produce different rates on same date | Decide: use Sage ER for legacy parity in Phase 1, then migrate to a single canonical FX table in Phase 2 |
| G7 | Country normalisation rules not externalised | `USA` vs `United States` vs `United States Of America` causes territory misclassification | Build a `royalty_country_aliases` lookup table mapping all observed variants to canonical ISO-3166 codes |
| G8 | Channel/site naming not standardised | `Amazon.com (US)` vs `head_case_designs-us` etc. need stable mapping | Build a `royalty_channel_mappings` table (proposed in docs but not populated) |
| G9 | No idempotency or re-run safety | Re-running same date range could produce duplicate or conflicting outputs | Add `run_id` with upsert logic; output folders keyed by `{run_id}/{licensor}/` |
| G10 | No rollback mechanism | Bad batch run has no undo path | Keep source snapshot + normalised snapshot per run; never overwrite previous run outputs |

### Category 3 — Operational gaps (should resolve before go-live)

| # | Gap | Impact | Resolution |
|---|-----|--------|------------|
| G11 | No access control or audit trail | Anyone with CLI access can generate reports; no traceability | Phase 3 concern — add user auth + run log in portal |
| G12 | No scheduling or calendar integration | Reports must be triggered manually each period | Add optional cron/scheduler in Phase 3 |
| G13 | Output distribution not designed | Files land in a folder but don't reach licensors | Phase 3 — add email/SFTP/portal download per licensor preference |
| G14 | No monitoring or alerting | Failed runs go unnoticed | Add Slack/email notification on batch completion or failure |
| G15 | IMGC hardcoded overrides not fully documented | IMGC licensors have special name/rate overrides embedded in PHP arrays | Extract `imgc_royalty_info` mapping into a structured config table |

---

## Proposed implementation plan

### Phase 0 — Unblock (Week 1)

**Goal:** Remove the four blockers so building can start.

| Task | Owner | Deliverable | Est. effort |
|------|-------|-------------|-------------|
| 0.1 Provide converter app access | Cem | Working repo URL or zip | 1 day |
| 0.2 Collect NHL parity test kit | Cem + ops team | 3 files: source CSV, config JSON, expected output | 1 day |
| 0.3 Validate unit royalty formula | Cem + finance | Confirmed formula with worked example | 0.5 day |
| 0.4 Audit converter config directory | Dev (Claude Code) | `licensor_config_inventory.csv` listing all configs | 0.5 day |

### Phase 1 — Batch MVP (Weeks 2–4)

**Goal:** One-click batch generation using legacy-format export + existing converter.

| Task | Owner | Deliverable | Est. effort |
|------|-------|-------------|-------------|
| 1.1 Reverse-engineer converter I/O contract | Dev | Documented CLI interface, input schema, output naming rules, config structure | 2 days |
| 1.2 Build source extractor script | Dev | Python script: date range → legacy-format CSV from BigQuery/Zero | 3 days |
| 1.3 Build normalisation layer | Dev | Python module applying all legacy transforms (SKU rewrite, description, territory, FX, exclusions) | 5 days |
| 1.4 Build batch orchestrator | Dev | CLI: `royalty-batch run --from YYYY-MM-DD --to YYYY-MM-DD` | 2 days |
| 1.5 Build validation report generator | Dev | Summary JSON + exception CSVs per run | 2 days |
| 1.6 NHL parity test | Dev + Cem | Side-by-side comparison: row counts, GBP totals, royalty totals, SKU/description spot checks | 1 day |
| 1.7 Expand to 2–3 more licensors (LFC, NFL, WWE) | Dev + Cem | Parity confirmed on structurally different licensor types | 3 days |
| 1.8 Build country alias + channel mapping tables | Dev | Two JSON/CSV lookup files consumed by normalisation layer | 1 day |

**Phase 1 exit criteria:**
- NHL parity within ±1% on GBP totals and royalty totals
- At least 3 licensors passing parity
- All exception types generating clean reports
- Batch completes in under 10 minutes for a quarterly run

### Phase 2 — Rules externalisation (Weeks 5–8)

**Goal:** Move all royalty logic into durable Supabase/BQ tables so rules are version-controlled and editable without code changes.

| Task | Owner | Deliverable | Est. effort |
|------|-------|-------------|-------------|
| 2.1 Create Supabase schema (11 tables per IMPLEMENTATION_MAP spec) | Dev | Migration scripts + seed data | 3 days |
| 2.2 Extract all SKU rewrite rules from PHP into `royalty_sku_rewrite_rules` | Dev | Complete rule inventory per licensor | 3 days |
| 2.3 Extract all description mappings into `royalty_description_rules` | Dev | Complete mapping inventory per licensor | 3 days |
| 2.4 Migrate exchange rate history into `royalty_exchange_rates` | Dev + finance | Validated rate table with effective date windows | 2 days |
| 2.5 Migrate territory mappings into `royalty_territory_mappings` | Dev | Per-licensor territory rules | 2 days |
| 2.6 Migrate exclusion rules into `royalty_exclusion_rules` | Dev | Conflicting lineups, user suppressions | 1 day |
| 2.7 Repoint normalisation layer to Supabase | Dev | Phase 1 script now reads from DB instead of hardcoded rules | 3 days |
| 2.8 Re-run parity tests against Supabase-backed pipeline | Dev + Cem | Same parity thresholds as Phase 1 | 2 days |

**Phase 2 exit criteria:**
- All Phase 1 parity tests still pass with Supabase-backed rules
- Rules are editable via Supabase dashboard without code deploy
- Run history stored in DB with full audit trail

### Phase 3 — Production portal (Weeks 9–12)

**Goal:** Simple web UI for date-range runs, exception review, and output download.

| Task | Owner | Deliverable | Est. effort |
|------|-------|-------------|-------------|
| 3.1 Build web UI (date picker, run button, status) | Dev | Next.js or similar lightweight app | 5 days |
| 3.2 Run history dashboard | Dev | List of past runs with status, counts, download links | 2 days |
| 3.3 Exception review screen | Dev | Filterable table of unmatched SKUs, descriptions, territories | 3 days |
| 3.4 Output distribution (email/SFTP per licensor) | Dev | Configurable delivery per licensor | 3 days |
| 3.5 Scheduling (optional cron for recurring periods) | Dev | Quarterly/monthly auto-generation | 1 day |
| 3.6 Monitoring + Slack alerts | Dev | Notifications on completion/failure | 1 day |

---

## Technical decisions required from Cem

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| D1 | Runtime for batch scripts | Python / Node / Both | Python — better BigQuery/Supabase SDK support, Pandas for data transforms |
| D2 | Phase 1 rule storage | JSON files / Supabase from day 1 | JSON files — fastest path, migrate in Phase 2 |
| D3 | Hosting for batch runner | Local machine / Cloud VM / Supabase Edge Functions | Cloud VM (small EC2/GCE) — runs on schedule, accessible by team |
| D4 | Converter app preservation vs rewrite | Keep existing converter / Rebuild in Python | Keep existing — proven logic, rewrite only if unmaintainable |
| D5 | Exchange rate source for Phase 1 | Sage ER from legacy export / HMRC rates / XE API | Sage ER — matches legacy for parity testing |
| D6 | Which licensors to target first | NHL only / NHL + LFC + NFL | NHL first, then LFC + NFL once parity proven |

---

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Converter app is abandoned/broken | Medium | High — blocks entire Phase 1 | If unusable, rebuild output generation from JSON configs directly; adds 2 weeks |
| Legacy PHP contains undocumented edge cases | High | Medium — some licensor reports will be wrong initially | Parity testing catches these; maintain exception reports; iterate rule tables |
| Sage ER values differ from what BigQuery produces | Medium | Medium — GBP totals won't match | Use Sage ER as source of truth for Phase 1; reconcile in Phase 2 |
| IMGC/special licensors have complex overrides | High | Low–Medium — affects subset of licensors | Extract `imgc_royalty_info` into config table early; test separately |
| Team capacity for 12-week plan | Medium | High — delays compound | Phase 1 alone delivers 80% of value; Phase 2–3 can flex |

---

## Success metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to generate all licensor reports | < 10 min (was hours manual) | Timed batch run |
| Parity with legacy output | ±1% on GBP totals per licensor | Automated comparison script |
| Exception rate (unmatched rows) | < 2% of total rows | Exception report counts |
| Licensor coverage | 100% of active licensors with configs | Config inventory audit |
| Manual intervention required | Zero for standard quarterly run | Ops team feedback |

---

## Immediate next actions (this week)

1. **Cem:** Provide converter app access (corrected repo URL or zip)
2. **Cem:** Collect NHL parity test kit (source CSV + config JSON + expected output)
3. **Cem:** Confirm or deny: is the unit royalty formula `Quantity / rate` or `Quantity × rate`?
4. **Cem:** Confirm preferred runtime (Python recommended)
5. **Claude Code:** Once converter access is provided, reverse-engineer I/O contract and document
6. **Claude Code:** Build config inventory from converter's config directory

---

## Document quality notes (feedback on ChatGPT 5.4 output)

### What was done well
- Comprehensive legacy logic extraction with specific function names and PHP references
- Correct identification of the brand→property→royalty bridge chain
- Practical schema design that separates staging from normalised data
- Honest flagging of the unit-royalty ambiguity rather than guessing
- Good edge case documentation from real NHL sample data

### What could be improved
- **Too much repetition across documents** — the same architecture, SOP steps, and schema appear in both `IMPLEMENTATION_MAP.md` and `ROYALTY_CALCULATION.md`, making the total corpus ~2× longer than needed
- **No prioritised gap analysis** — gaps are listed as "open questions" but not ranked by blocking severity
- **No effort estimates or timeline** — the plan reads as a wish list rather than a project schedule
- **No risk register** — risks are mentioned inline but not formally tracked
- **No success metrics** — no way to know when the project is "done"
- **Missing technical decisions** — runtime, hosting, auth, and deployment are all deferred
- **Converter app is treated as a given** — but it's the single biggest dependency and has zero documentation in these files
