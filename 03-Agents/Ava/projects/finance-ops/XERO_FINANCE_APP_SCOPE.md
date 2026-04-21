# SCOPE.md — Xero Finance Ops App

## Project
Build an internal finance operations app for Ecell that connects to Xero and supports both:
- **Ecell Global UK**
- **Ecell Global Inc (US)**

This app should become the working layer between inbound finance documents / operational reports and Xero.

---

## Primary Objectives

### 1) AP Document Intake -> Xero
Automate the intake and recording of:
- supplier invoices
- receipts
- emailed finance documents
- uploaded PDFs
- scanned images/documents

Core workflow:
1. ingest document from email or upload
2. extract key fields
3. match supplier and org
4. create draft record for review
5. post approved bill/expense record into Xero
6. store audit trail and Xero IDs locally

### 2) Journal Posting from Operational Reports
Support journal creation from internal usage/cost reports, especially:
- inventory usage
- COGS adjustments
- stock consumption
- manual accounting adjustments from operational files

Core workflow:
1. upload report/source file
2. parse report rows
3. apply mapping rules
4. generate journal draft
5. review/approve
6. post journal to correct Xero org
7. store audit log and source linkage

### 3) Query / Reporting Layer
Provide an internal query app for finance data after sync from Xero.

Initial query scope:
- invoices
- bills
- receipts/expense-type records
- payments
- journals
- contacts
- accounts

Capabilities:
- search
- filtering
- org switching (UK / US)
- exports
- simple operational finance views

---

## Product Shape
This is an **internal app**, not a one-off script.

### Core modules
1. **Auth & Org Management**
   - Xero connection per org
   - UK / US separation
   - tenant/token management

2. **Document Intake**
   - email intake
   - PDF/image upload
   - OCR / extraction
   - supplier matching
   - review queue

3. **Bill / Receipt Posting**
   - create Xero bills or expense-like finance records
   - duplicate checking
   - posting status tracking

4. **Journal Engine**
   - ingest inventory/usage reports
   - apply accounting mappings
   - create journal drafts
   - post journals to Xero

5. **Sync & Query Layer**
   - pull Xero data into local database
   - query/search/report over local tables
   - never rely on live-Xero-only UI queries

6. **Audit / Logging**
   - source file registry
   - posting jobs
   - sync jobs
   - error handling
   - retry history

---

## Org Model
The app must support **multi-org from day one**.

### In scope
- separate UK and US Xero connections
- separate tokens / tenant IDs
- separate mappings per org
- separate tax/account/tracking logic per org
- org selector in internal UI

### Do not assume shared logic for
- tax codes
- account codes
- contacts
- invoice numbering behavior
- currency
- tracking categories

---

## Recommended MVP

### Phase 1 — Foundation
- Xero auth working for UK + US
- local secret/env setup
- local DB schema
- sync jobs for:
  - Organisation
  - Accounts
  - Contacts
  - Bills
  - Invoices
  - Payments
  - Journals
- basic internal dashboard shell

### Phase 2 — AP Intake MVP
- upload PDF/image documents
- optional email intake stub
- extraction pipeline
- review screen
- supplier/org selection
- draft bill creation in Xero
- posting log

### Phase 3 — Journal MVP
- upload operational usage report
- apply journal mapping rules
- generate draft journals
- approve/post to Xero
- store posting outcome locally

### Phase 4 — Query Layer
- list/search/filter:
  - bills
  - invoices
  - payments
  - journals
  - contacts
- org toggle
- date filters
- exports

---

## Functional Requirements

### Document Intake
- accept uploaded PDF/image files
- support scanned documents
- support email-driven intake later
- parse vendor name, invoice number, date, currency, totals, tax, line items where possible
- allow human correction before posting

### Xero Posting
- post to correct org
- handle contact matching/creation rules
- map tax/account codes
- prevent duplicates where possible
- save Xero IDs and response payload metadata

### Journal Posting
- accept CSV/XLSX-like operational reports
- allow configurable mapping rules
- support draft-first workflow
- preserve source file reference

### Query / Reporting
- query local DB, not only Xero live
- support UK/US separation
- support exports for finance review

---

## Non-Functional Requirements
- internal-only app
- secure secret handling (local env / secret store only)
- no credentials in shared docs, MEMORY.md, TOOLS.md, or Drive
- auditability for all postings
- clear error handling and retry flow
- human-in-the-loop for MVP postings

---

## Initial Data Model Areas

### Config / orgs
- xero_orgs
- org_settings
- tax_code_mappings
- account_code_mappings
- supplier_mappings
- journal_mapping_rules

### Intake
- inbound_emails
- inbound_documents
- parsed_documents
- document_review_queue

### Sync raw
- xero_contacts_raw
- xero_accounts_raw
- xero_invoices_raw
- xero_bills_raw
- xero_payments_raw
- xero_journals_raw

### Posting / audit
- xero_sync_runs
- xero_posting_jobs
- xero_bill_creations
- xero_journal_creations
- source_file_registry
- error_log

---

## Explicitly Out of Scope for MVP
- fully autonomous posting with no human review
- complete procurement/PO workflow automation
- bank reconciliation automation
- payroll integration
- full management reporting suite
- deep forecasting/planning models

---

## Current Build Direction
Build as:
- **backend:** Xero integration + sync + posting services
- **database:** local operational/query layer
- **frontend:** internal finance ops dashboard

Priority order:
1. auth and org connections
2. sync foundation
3. AP document intake
4. journal posting
5. query/reporting views

---

## Success Criteria
MVP is successful when the app can:
1. connect to UK and US Xero orgs
2. sync core finance objects locally
3. ingest an invoice/receipt document and create a reviewed bill in Xero
4. ingest an inventory usage report and create a journal in Xero
5. query posted/synced transactions from the internal UI
