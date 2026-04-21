# Approval and Audit Workflow — Xero Finance Ops App
Date: 2026-04-20 | Owner: Ava | Status: Draft

## 1. Principle
Every finance posting must be explainable later.

## 2. Approval Workflow
### AP documents
1. source received
2. saved to shared drive with stable reference
3. extracted
4. supplier search against existing Xero contacts
5. duplicate check
6. reviewed
7. prior similar posting checked for nominal/account consistency
8. corrected if needed
9. approved
10. posted
11. logged

### Journals
1. source file uploaded
2. parsed
3. mapped
4. reviewed
5. approved
6. posted
7. logged

## 3. Minimum Audit Trail
For each posting store:
- source reference
- shared-drive document reference
- extracted values
- corrected values
- org selected
- tax/account mapping used
- prior similar posting reference if used
- posting timestamp
- Xero object id
- posting result
- retry history

## 4. Failure Handling
If posting fails:
- keep the full review context
- do not lose source lineage
- do not require total re-entry from scratch
- set status to `needs_retry`

## 5. Governance Requirement
The MVP must remain human-in-the-loop until Cem explicitly approves any reduced-review workflow.
