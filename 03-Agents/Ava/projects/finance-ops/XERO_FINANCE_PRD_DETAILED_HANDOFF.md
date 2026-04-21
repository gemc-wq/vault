# Xero Finance Ops App — Detailed PRD Handoff
Date: 2026-04-20 | Owner: Ava | Status: Draft Detailed Handoff

## 1. Executive Summary
This project is an internal finance operations app for Ecell that sits between inbound finance inputs and Xero.

It is designed to solve two operational finance problems:
1. intake and posting of supplier invoices and finance documents,
2. creation and posting of journals from operational finance source files such as inventory usage, COGS adjustments, and related reports.

The app must support both:
- **Ecell Global UK**
- **Ecell Global Inc (US)**

This is not a lightweight integration script. It is a structured internal workflow with review, approval, audit trail, and multi-org handling from day one.

## 2. Problem Statement
The current finance process is too manual and too fragmented.

Documents arrive by email, upload, or scan. They are manually reviewed, manually interpreted, then manually entered into Xero. Operational reports are turned into journals manually with weak traceability.

This creates the following risks:
- duplicate entry,
- posting into the wrong org,
- inconsistent tax treatment,
- incomplete source traceability,
- poor auditability,
- excessive manual workload.

## 3. Product Goal
Create a finance operations layer that:
- ingests inbound AP documents,
- extracts and normalizes the relevant fields,
- routes them to the correct org,
- applies tax/account rules,
- sends them through human review,
- posts approved bills and journals into Xero,
- stores the full audit trail locally.

## 4. Primary User Types
### Finance reviewer
Needs to review extracted data, correct mistakes, and approve posting.

### Operations reviewer
Needs to upload and validate operational source reports for journal creation.

### Admin / maintainer
Needs to manage orgs, mappings, supplier matches, tax/account logic, and sync state.

## 5. Core Modules
### Module A — Auth and Org Management
Supports:
- separate Xero OAuth connections for UK and US,
- token/tenant management,
- org routing,
- org-specific settings.

### Module B — AP Document Intake
Supports:
- PDF upload,
- image upload,
- later email intake,
- OCR/field extraction,
- supplier matching,
- duplicate checks,
- draft bill creation workflow.

### Module C — Journal Engine
Supports:
- source file upload,
- parsing reports,
- applying journal mapping rules,
- draft journal generation,
- approval before posting.

### Module D — Sync and Query Layer
Supports:
- syncing finance objects from Xero to local DB,
- querying bills, invoices, payments, journals, contacts, and accounts locally,
- avoiding reliance on live-only Xero queries.

### Module E — Audit and Operations Log
Supports:
- source file registry,
- posting logs,
- sync logs,
- error history,
- retry history,
- final Xero IDs.

## 6. Functional Requirements
### FR1. Multi-org routing
The app must require explicit org routing for every document or posting action.

No shared assumptions between UK and US are allowed for:
- tax codes,
- account codes,
- contacts,
- currency,
- tracking categories.

### FR2. Invoice / bill intake
The app must support:
- uploaded PDFs,
- scanned images,
- document OCR/extraction,
- extraction of vendor name, invoice number, invoice date, totals, tax, currency, and line items where possible.

### FR3. Supplier matching
The app must:
- search existing Xero suppliers/contacts before proposing a new supplier,
- attempt supplier matching using name and prior matched history,
- allow reviewer override,
- support unresolved supplier workflow,
- optionally create new contact only after review.

### FR4. Duplicate detection
The app must attempt duplicate prevention before any draft posting using combinations such as:
- org,
- supplier,
- invoice number,
- invoice date,
- total amount.

Duplicates should be flagged before posting, never silently ignored.

### FR5. Prior-posting comparison logic
Before proposing nominal/account coding, the app should inspect the most recent similar posted invoice for that supplier where appropriate, so the reviewer can see how similar invoices were previously coded.

This should be advisory, not blindly automatic.

### FR6. Bill posting flow
The app must support:
1. extract
2. review
3. correct
4. approve
5. post to correct Xero org
6. store Xero response metadata and local audit record

### FR7. Document retention and record keeping
The original invoice/document and its posting lineage must be retained in shared drive storage to support accurate record keeping for both UK and US compliance expectations.

The app should preserve:
- original source document,
- stored shared-drive reference,
- upload/posting linkage,
- Xero object linkage.

### FR8. Xero-native document workflow compatibility
The design should recognize that Xero already supports invoice upload plus AI-assisted bill creation.

The app may either:
1. mirror that workflow externally with stronger review/routing/audit logic, or
2. complement Xero by using shared-drive storage plus structured review before Xero creation.

This is a product-shape choice, not something to ignore.

### FR9. Journal posting flow
The app must support:
1. upload source file
2. parse rows
3. apply mapping rules
4. build draft journal
5. review
6. approve
7. post to correct org
8. store source linkage and posting outcome

### FR7. Query layer
The app must provide local query capability for:
- bills
- invoices
- payments
- journals
- contacts
- accounts
- source files
- posting logs

### FR8. Auditability
Every posting action must preserve:
- source file or source document reference,
- reviewer identity if available,
- timestamp,
- org,
- mapping used,
- posting result,
- Xero object ID,
- correction/retry history.

## 7. Detailed Workflow Requirements
### 7.1 AP document workflow
1. document arrives by upload or intake source
2. raw file stored with unique ID
3. extraction engine processes document
4. app proposes org, supplier, totals, tax, and line-item interpretation
5. reviewer corrects any mistakes
6. duplicate check runs
7. approved document becomes draft/postable bill
8. bill posts to Xero
9. result logged locally

### 7.2 Journal workflow
1. operational report uploaded
2. report type identified
3. mapping rules selected
4. rows transformed into journal lines
5. reviewer checks account/tax/org routing
6. journal posted to Xero
7. source linkage and result stored locally

## 8. VAT and Tax Rules Requirements
### UK company requirements
The system must support explicit VAT handling rules for the UK entity, including cases such as:
- standard VAT present on supplier invoice,
- zero-rated invoice,
- outside scope / no VAT,
- overseas supplier logic,
- missing VAT number or incomplete tax detail,
- tax override by reviewer,
- preservation of original invoice evidence.

### US company requirements
The US entity should support its own tax/account rules without inheriting UK VAT assumptions.

## 9. Exception Handling Requirements
The system must explicitly handle:
- supplier not found,
- invoice number missing,
- duplicate invoice suspected,
- org ambiguous,
- OCR confidence weak,
- totals mismatch,
- tax extraction mismatch,
- unsupported file type,
- posting failure,
- Xero auth/token failure,
- invalid account/tax code mapping.

## 10. Review State Model
Suggested states:
- `received`
- `extracted`
- `needs_review`
- `duplicate_flagged`
- `ready_to_post`
- `posted`
- `failed`
- `needs_retry`
- `archived`

## 11. Data Model Areas
### Org configuration
- xero_orgs
- org_settings
- auth_tokens_metadata

### Mapping configuration
- account_code_mappings
- tax_code_mappings
- supplier_mappings
- journal_mapping_rules

### Intake and source tracking
- source_documents
- source_files
- extraction_runs
- review_actions

### Finance objects mirror
- bills
- invoices
- payments
- journals
- contacts
- accounts

### Operational logs
- posting_jobs
- posting_attempts
- sync_jobs
- sync_errors

## 12. Security and Governance Requirements
- no secrets in docs,
- no autonomous posting in MVP,
- human review before posting,
- local audit trail mandatory,
- org separation mandatory.

## 13. MVP Definition
MVP is successful when the system can:
1. connect to both Xero orgs,
2. sync core finance objects locally,
3. ingest an uploaded invoice and create a reviewed bill in Xero,
4. ingest an operational report and create a reviewed journal in Xero,
5. query posted results from local UI.

## 14. Explicitly Out of Scope
- autonomous posting with no review,
- bank reconciliation,
- payroll,
- forecasting,
- management accounting suite,
- procurement automation.

## 15. Best-Practice Requirements To Incorporate
- search existing suppliers first before proposing new supplier creation,
- check duplicates before any entry/posting action,
- inspect prior similar posted invoices to suggest likely nominal/account treatment,
- preserve original documents in shared-drive storage for record keeping,
- decide clearly whether the product should mirror Xero's upload-plus-AI flow or layer on top of it.

## 16. Open Inputs Still Needed
- exact Xero account code mappings,
- exact UK VAT treatment preferences for edge cases,
- finance inboxes to monitor,
- source report types for journal engine,
- permission model for reviewers,
- final decision on whether source-of-truth document storage stays shared-drive-first, Xero-attachment-first, or dual-write.
