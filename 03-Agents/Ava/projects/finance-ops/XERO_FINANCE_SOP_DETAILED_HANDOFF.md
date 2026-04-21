# Xero Finance Ops App — Detailed SOP Handoff
Date: 2026-04-20 | Owner: Ava | Status: Draft Detailed Handoff

## 1. Purpose
This SOP defines the operating procedure for AP document intake and journal posting into Xero for both UK and US entities.

The objective is to make finance posting reviewable, auditable, and multi-org safe.

## 2. Operating Rules
### Rule 1
Every posting must be explicitly tied to an org.

### Rule 2
No posting happens without review in MVP.

### Rule 3
Every posted record must preserve source lineage.

### Rule 4
Tax/account logic must be org-specific.

### Rule 5
Potential duplicates must be reviewed before posting.

## 3. AP Document Intake SOP
### Step 1 — Receive document
Input types:
- uploaded PDF
- uploaded image
- scanned finance doc
- later: email intake

### Step 2 — Register source
Create source record with:
- source id
- file path/reference
- received timestamp
- received method
- org if known

### Step 3 — Extract fields
Extract where possible:
- supplier name
- invoice number
- invoice date
- currency
- subtotal
- tax
- gross total
- line items

### Step 4 — Validate extraction
Check for:
- missing required fields
- conflicting totals
- weak OCR confidence
- unreadable supplier or invoice number

If weak, route to `needs_review` immediately.

### Step 5 — Match supplier and org
- search existing Xero suppliers/contacts first
- match to known supplier if possible
- review prior matched history if available
- propose org
- require reviewer confirmation if ambiguous

### Step 6 — Run duplicate check
Compare against posted and pending items using:
- org
- supplier
- invoice number
- date
- total

If duplicate suspected, mark `duplicate_flagged`.
Do not proceed to posting until reviewer resolves it.

### Step 7 — Compare prior similar posting
Before reviewer approval, surface the most recent similar posted invoice for that supplier if available, so nominal/account coding can be checked against prior treatment.

### Step 8 — Reviewer correction
Reviewer must verify:
- org
- supplier/contact
- tax treatment
- account assignment if relevant
- totals
- attachment correctness

### Step 9 — Save source document for record keeping
Before or alongside posting, ensure the original document is retained in shared-drive storage with a stable reference for audit and legal record keeping.

### Step 10 — Post draft bill
Once approved:
- create bill in correct Xero org
- capture Xero response
- store Xero ID locally
- update status to `posted`

### Step 11 — Log outcome
Record:
- who approved if available
- timestamp
- posting success/failure
- any warnings

## 4. Journal Posting SOP
### Step 1 — Receive source report
Accepted examples:
- inventory usage report
- COGS adjustment report
- stock consumption report
- manual adjustment support file

### Step 2 — Register file
Store:
- file reference
- uploaded timestamp
- report type
- intended org

### Step 3 — Parse report
- validate schema
- map columns
- identify rows for journal logic

### Step 4 — Apply journal mapping rules
- assign account codes
- assign org
- assign tax treatment if relevant
- generate balanced journal lines

### Step 5 — Reviewer validation
Reviewer checks:
- org routing
- account mappings
- totals
- balancing
- assumptions made by parser

### Step 6 — Post journal
- submit journal to Xero
- capture Xero journal ID or failure
- update local posting log

## 5. Review Checklist
Before any posting:
- correct org selected?
- source document/file attached?
- supplier/contact valid?
- duplicate check passed?
- tax treatment correct?
- totals correct?
- mapping rules valid?
- posting target confirmed?

## 6. VAT / Tax Handling SOP
### UK entity
Reviewer must classify the invoice as one of:
- standard VAT invoice
- zero-rated
- no VAT / outside scope
- overseas supplier / import-like treatment
- unclear / needs manual treatment

Tax treatment must never be assumed silently when source evidence is weak.

### US entity
No UK VAT assumptions should be inherited. Use org-specific tax/account treatment only.

## 7. Error Handling SOP
### If extraction fails
- keep source file
- mark `needs_review`
- allow manual entry/correction

### If duplicate suspected
- mark `duplicate_flagged`
- do not auto-post

### If posting fails
- log exact error
- keep source linkage
- set `needs_retry`
- do not lose reviewer corrections

### If Xero auth fails
- stop posting attempts
- mark failure clearly
- require auth remediation before retry

## 8. Status Model
Suggested statuses:
- received
- extracted
- needs_review
- duplicate_flagged
- ready_to_post
- posted
- failed
- needs_retry
- archived

## 9. Audit Requirements
For every posted object, retain:
- source file/document reference
- original extracted values
- reviewer-adjusted values
- org
- tax code/account mapping used
- Xero object ID
- posting timestamp
- retry history if any

## 10. Daily / Weekly Operating Rhythm
### Daily
- review new AP documents
- clear `needs_review`
- clear `duplicate_flagged`
- resolve failed postings

### Weekly
- review posting errors
- review unmapped suppliers
- review tax/account rule gaps
- review sync health

## 11. Product-Shape Decision To Resolve
Decide whether the app should:
1. mirror Xero's invoice-upload-plus-AI flow with added routing/review/audit safeguards, or
2. keep shared-drive-first document storage and use the app as the structured control layer before Xero posting.

## 12. Inputs Needed Before Build Completion
- final UK VAT rules by scenario
- account code map for journals
- source report formats for journal engine
- reviewer permissions and approval design
- final document-retention policy across shared drive and Xero attachments
