# VAT and Accounting Rules — Xero Finance Ops App
Date: 2026-04-20 | Owner: Ava | Status: Draft Rules Layer

## 1. Purpose
This document defines the accounting and VAT logic layer that the app must support, especially for the UK entity.

It is not a substitute for final finance sign-off. It is the implementation rules layer the app must be able to represent.

## 2. Org Separation Rule
All tax and accounting rules must be org-specific.

Never assume UK logic applies to US.

## 3. UK VAT Handling Categories
The app should support at minimum:
- standard VAT invoice
- zero-rated invoice
- exempt / outside scope / no VAT
- overseas supplier with no UK VAT shown
- unclear tax treatment requiring manual review

## 4. Required Fields for Tax Review
Reviewer should see:
- supplier name
- supplier country if known
- invoice date
- net amount
- VAT amount
- gross total
- currency
- invoice number
- evidence attachment

## 5. UK Review Rules
### Rule A — standard VAT present
If valid VAT is shown and invoice evidence is clear, app should support mapping to the appropriate VAT code and bill record.

### Rule B — zero-rated or no VAT shown
Do not force a VAT code purely by habit. Reviewer must classify whether it is genuinely zero-rated, outside scope, or just incomplete.

### Rule C — overseas supplier
If supplier is overseas and invoice does not show UK VAT, do not assume normal domestic VAT treatment.
Flag for explicit review if needed.

### Rule D — unclear tax evidence
If tax evidence is unclear, extraction may continue but posting must remain blocked for reviewer decision.

## 6. Journal Rules
Operational journals should support:
- org-specific account mappings,
- balanced debit/credit outputs,
- source file linkage,
- reviewer confirmation before posting.

## 7. Contact and Supplier Rules
- do not silently create finance contacts without review in MVP
- allow supplier matching override
- preserve unmatched supplier state for review

## 8. Duplicate Control Rules
Potential duplicates should be flagged when matching combinations such as:
- same org
- same supplier/contact
- same invoice number
- same total
- near-identical date

## 9. Currency Rules
The app must preserve original invoice currency and not silently normalize away source values.

## 10. Implementation Note
Final VAT code names, account code mappings, and exception handling still require finance-owner confirmation before production posting is enabled.
