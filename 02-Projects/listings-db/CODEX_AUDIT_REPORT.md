# Codex Audit Report — Listings Data Pipeline PRD v1.0 + SOP v1.0
Date: 2026-04-15  
Auditor: Codex (GPT-5.4)  
Scope: Adversarial technical audit of architecture, schema, validation, recovery, integrations, operations, and build readiness.

## Executive Summary
The design direction is broadly correct: local full snapshot for reproducibility, Supabase for operational consumers, and BigQuery for historical analytics is a sensible split for this workload. The strongest part of the spec is its explicit focus on marketplace contamination as the primary failure mode. The weakest part is that several safeguards are described as if already enforceable, but are not yet specified tightly enough to guarantee safe implementation under crash, resume, duplicate-run, or partial downstream-failure conditions.

My bottom line: **do not reject the project, but do not build from these docs unchanged.** The architecture is viable, the tool choices are mostly defensible, and the SOP is operator-friendly. However, there are critical gaps around transactional boundaries, bootstrap/init behavior, duplicate-SKU handling, downstream rollback semantics, and exact export contracts. Those gaps are fixable in the PRD/SOP before implementation starts.

## 1. Architecture Quality
**Verdict: PASS_WITH_CONCERNS**

**Key findings**
- The three-tier model is sound. SQLite for authoritative local snapshots, Supabase for current operational state, and BigQuery for long-term history matches the three downstream consumer types.
- Marketplace isolation is strong at the filesystem and DB-file level. One DB per marketplace is the right correction to the earlier shared-table failure.
- Isolation is weaker at the query and process layer than the PRD implies. Resume flows, shared service-role credentials, and operator-selected paths still create implementation risk.
- The architecture assumes a clean phase ordering, but does not fully specify the commit boundary between local snapshot success and downstream pushes.

**Recommendations**
- Make the local SQLite commit the only authoritative success boundary. Everything after that must be modeled as asynchronous sync stages with resumable state, not part of a single implicit transaction.
- Add a per-cycle state machine: `validated -> loaded_local -> compliance_emitted -> supabase_synced -> bigquery_synced -> approved`.
- Add a filesystem lock per region so concurrent or duplicate runs cannot overlap.
- Verify DB filename against `_meta_marketplace.db_filename` on startup, not just the region field.

## 2. Schema Design
**Verdict: PASS_WITH_CONCERNS**

**Key findings**
- One SQLite file per marketplace is defensible and materially safer than a shared DB with a region column.
- Core fields needed by downstream systems are present: `asin`, `fulfillment_channel`, `item_condition`, `merchant_shipping_group`, `row_hash`, `base_sku`.
- The main table stores multiple snapshots in one table, but the uniqueness and indexing strategy is not enough for efficient “current snapshot” queries at scale without explicit snapshot scoping.
- The schema is missing a few hardening fields: normalized SKU key, source row number, validation reason, and explicit cycle ID in the snapshot table.

**Recommendations**
- Add `cycle_id`, `source_row_num`, `normalized_seller_sku`, and `validation_error_code` fields.
- Add a unique or diagnostic query gate for duplicate `seller_sku` within the same region and snapshot. Right now duplicates could quietly coexist if Amazon outputs malformed repeats.
- Replace the CHECK constraint that references `_meta_marketplace` with a safer implementation if SQLite rejects subqueries in CHECK in practice. If not enforceable, use triggers.
- Add a materialized “latest snapshot” view per DB for downstream local queries.

## 3. Performance & Feasibility
**Verdict: PASS_WITH_CONCERNS**

**Key findings**
- DuckDB is the right default recommendation. Pandas is too slow and memory-risky for repeated 6–10 GB TSV ingestion. MySQL adds operational burden that is not justified here.
- The claimed 1.5 GB/s is optimistic for end-to-end pipeline throughput. Raw scan speed may approach that, but validation, hashing, joins, SQLite writes, and cloud pushes will dominate.
- The SOP’s sample 16-minute regional runtime is plausible. The PRD target of under 10 minutes per 9 GB file is aggressive but not required for business viability.
- Storage is manageable if retention is enforced. It becomes a problem only if pruning is not automated or if full historical snapshots accumulate locally.

**Recommendations**
- Treat 15–20 minutes per marketplace as the real acceptance target for v1, not 10 minutes.
- Benchmark the SQLite write phase specifically. That is more likely than DuckDB ingest to become the bottleneck.
- Store only six snapshots locally, enforce pruning automatically, and VACUUM on a controlled schedule.
- Avoid pandas except for narrow post-load transformations.

## 4. Validation Gates
**Verdict: FAIL**

**Key findings**
- The anti-contamination gates are thoughtful, but they are not sufficient yet to guarantee safety.
- Currency and template heuristics are helpful but not deterministic. UK and US can overlap enough to evade simplistic statistical checks.
- No gate explicitly detects duplicate SKUs within a marketplace snapshot, malformed casing drift, or unexpectedly high suppression/removal patterns.
- Operator bypass is mostly prevented socially, but not fully structurally. `--resume`, bootstrap, and manual rollback paths are not defined tightly enough.

**Recommendations**
- Add hard gates for: duplicate `(seller_sku)` within same region/snapshot, null or blank `merchant_shipping_group` spikes, abnormal `REMOVED` rate, and empty `asin` spikes.
- Add account-level fingerprint validation if available from report metadata or stable marketplace-only header cues.
- Make validation output immutable per cycle and require explicit new cycle creation after any failed contamination event.
- Specify that `resume` may continue only from downstream sync steps, never from pre-commit validation/load steps.

## 5. Failure Modes & Recovery
**Verdict: FAIL**

**Key findings**
- The docs acknowledge many failure modes, but recovery is underspecified where it matters most: partial downstream sync after successful local commit.
- The SOP says rollback does not touch Supabase/BigQuery for mid-load crashes, but later sections allow resumed syncs. Those paths need exact invariants.
- Corrupted download detection is decent at the file-size/header level, but weak against semantically damaged files that still parse.
- There is no concrete dead-letter schema despite the PRD referencing one for persistent Supabase failures.

**Recommendations**
- Add explicit downstream sync checkpoint tables, including batch number, retry count, and last acknowledged cursor.
- Define idempotent upsert keys and replay semantics for Supabase and BigQuery.
- Add checksum logging for source file, row count, and per-batch hash totals so partial loads can be audited.
- Add and spec a `dead_letter_listings_sync` table now, or remove the dead-letter claim.

## 6. Integration Contracts
**Verdict: PASS_WITH_CONCERNS**

**Key findings**
- The required fields for Layer 0 and procurement are present.
- The `base_sku` join path is reasonable, assuming blank inventory remains keyed consistently to `item_code`.
- The shipping issues CSV contract is directionally right but underspecified for builders. Delimiter, encoding, quoting, date format, and exact column order are missing.
- `row_hash` exists locally and in BigQuery, but not clearly in Supabase operational tables where consumers may need change semantics.

**Recommendations**
- Publish exact CSV contracts with ordered headers, UTF-8 requirement, and sample rows.
- Add `row_hash` and `cycle_id` to `active_listings` or document why consumers must not rely on them there.
- Freeze enum vocabularies for `change_type`, `issue_type`, `severity`, and `status`.
- Add one contract test fixture per downstream consumer before build starts.

## 7. Operational Risk
**Verdict: PASS_WITH_CONCERNS**

**Key findings**
- The SOP is readable and operator-oriented. That is good.
- The cycle still depends too heavily on Cem for downloads and approvals. A single-person absence can stall the whole cadence.
- Harry is the sole script maintainer and incident responder of substance. That is a concentrated operational risk.
- Pre-flight checks are decent, but missing verification of alert channels, Dropbox handoff path existence, and current disk growth vs retention.

**Recommendations**
- Add a trained backup operator for downloads and approvals.
- Add a one-command environment self-test covering SQLite integrity, Supabase auth, BigQuery auth, and output directory permissions.
- Move Slack and Dropbox destination checks into pre-flight.
- Document who can perform emergency rollback if Harry is unavailable.

## 8. Unaddressed Requirements
**Verdict: FAIL**

**Key findings**
- The PRD does not fully reconcile the earlier wrong-template count discrepancy, even though the downstream urgency depends on it.
- Suppressed listings remain knowingly ambiguous, which is acceptable for v1, but the downstream implications are not clearly bounded.
- There is no explicit builder-facing bootstrap/init procedure for creating new marketplace DBs atomically.
- The docs do not specify a canonical source-of-truth for restricted-prefix rules beyond narrative references.

**Recommendations**
- Add a dedicated bootstrap/init spec and migration order.
- Add a machine-readable restricted-prefix config file rather than hardcoding lists in prose.
- Reconcile the 122k vs 9,778 discrepancy before downstream teams use severity counts for planning.
- Add a “known limitations” section for suppressed/removal ambiguity so consumers do not over-trust `REMOVED`.

## 9. Tech Stack Decisions
**Verdict: PASS**

**Key findings**
- DuckDB over pandas is the correct call.
- MySQL is not justified unless this evolves into a continuously updated multi-operator service.
- SQLite is acceptable for local snapshot authority if retention remains small and write patterns stay batch-oriented.
- Supabase for hot operational tables plus BigQuery for cold analytics is a sensible split.

**Recommendations**
- Keep DuckDB + SQLite + Supabase + BigQuery.
- Use DuckDB as staging/query engine only, not another persistent source of truth.
- Revisit SQLite only if local current-snapshot queries become too slow or if retention requirements expand beyond six snapshots.

## 10. Build Readiness
**Verdict: PASS_WITH_CONCERNS**

**Key findings**
- Codex can build this, but not cleanly from the docs as written.
- Ambiguities remain around init flow, transaction boundaries, resume semantics, exact downstream schemas, and enforcement of region constraints.
- The docs are strong enough for a shaped build, not for a blind implementation handoff.
- Risk is moderate, not because the architecture is wrong, but because a few missing details touch contamination prevention and recovery.

**Recommendations**
- Before implementation, revise PRD/SOP with: exact state machine, exact CSV contracts, exact dead-letter schema, duplicate-SKU gate, bootstrap/init procedure, and lock/resume rules.
- Estimate build as **3 to 5 days** for a careful v1 implementation plus **1 to 2 days** for benchmark, fixtures, and failure-path testing.
- Do not start with watched-folder automation. Manual trigger is safer for v1.

## Build-Readiness Score
**78 / 100**

Rationale: architecture is viable, schema is mostly adequate, and operational intent is clear. Score is held back by missing hard details in validation, recovery, and exact integration contracts.

## Final Recommendation
**proceed_with_conditions**

### Conditions before build
1. Add explicit cycle state machine and downstream resume semantics.  
2. Add duplicate-SKU, suppression-spike, and blank-template validation gates.  
3. Specify bootstrap/init procedure for new DB creation in one atomic transaction.  
4. Publish exact CSV/output contracts and enum vocabularies.  
5. Define dead-letter handling and idempotent replay for Supabase/BigQuery sync.  
6. Add region lockfile/concurrency control and startup verification of DB filename vs meta row.

If those six changes are made, I would support implementation on the current stack. Without them, the design is still too exposed to the exact kind of subtle corruption and recovery ambiguity this project is meant to eliminate.
