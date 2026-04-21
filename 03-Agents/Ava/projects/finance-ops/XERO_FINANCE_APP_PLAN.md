# Xero Finance Operations App — Plan
*Authored by Ava | Reviewed from Harry's research drop (Apr 4–9 2026)*

---

## What This Is

An internal finance operations layer that connects Ecell's operational data to Xero — for both UK and US entities. Not a one-off script. A proper internal app with a human-review-first workflow before anything posts to Xero.

**Trigger:** Cem wants to get Xero properly configured and automate AP intake and journal posting from operational reports (inventory, COGS, etc.).

---

## The Problem It Solves

Right now finance documents (supplier invoices, receipts, usage reports) are handled manually. This app automates intake, extraction, and posting — while keeping a human in the loop before anything hits Xero.

Three core pain points it addresses:
1. Supplier invoices / AP documents arriving via email or upload → manually entered into Xero
2. Inventory/COGS usage reports → manually journalled
3. No clean query layer for finance data across UK + US orgs

---

## Key Design Decisions

**Multi-org from day one.** UK and US are separate Xero connections with separate tax codes, account codes, contacts, currency, and tracking categories. No shared assumptions.

**Human-in-the-loop for MVP.** No autonomous posting. Every bill and journal goes through a review queue before it hits Xero.

**Local DB as the query layer.** Never rely on live Xero API calls for reporting. Sync to local tables, query locally. Faster and more resilient.

**Document intake is the first real unlock.** OCR → field extraction → supplier matching → draft bill creation. This removes the most manual work fastest.

---

## What Harry Has Built (as of Apr 4)

Harry built out the database schema and core inventory control pieces:

- **DB schema created** — 11 tables covering POs, packing lists, supplier invoices, goods receipts, stock alerts, inventory snapshots, supplier master
- **Stock-out monitor** — scans Gmail/Slack (via Airweave) for stock-out signals from China (CN), PH, UK, FL. Multi-lingual (EN/ZH/ES/TL) — Airweave handles the semantic search
- **BQ → Supabase inventory sync** — fixed traffic light thresholds (BLACK=0, RED<14d, YELLOW<21d, GREEN≥21d)
- **Migration script** — ready to run (`npx ts-node lib/migrate.ts`)

**Blockers Harry flagged:**
1. `gog` Gmail auth not set up (needed for email intake)
2. Xero US write auth still pending
3. DB migrations not yet run
4. Xero finance plugin auth incomplete

---

## Build Plan (4 Phases)

### Phase 1 — Foundation *(do first)*
- Xero OAuth working for UK + US tenants
- Local secret/env setup
- Core sync jobs: Organisations, Accounts, Contacts, Bills, Invoices, Payments, Journals
- Internal dashboard shell

### Phase 2 — AP Document Intake *(highest ROI)*
- PDF/image upload + optional email intake
- OCR + field extraction (vendor, date, amount, tax, line items)
- Supplier matching and org selection
- Review queue → approve → post draft bill to Xero
- Posting log with Xero IDs

### Phase 3 — Journal Engine
- Upload operational report (CSV/XLSX — inventory usage, COGS)
- Configurable mapping rules (report rows → journal lines)
- Draft journal → review → post to correct Xero org
- Source file stored, posting outcome logged

### Phase 4 — Query + Reporting
- Search/filter across bills, invoices, payments, journals, contacts
- UK / US org toggle
- Date filters + exports
- Simple finance views for internal use

---

## Explicitly Out of Scope (MVP)
- Autonomous posting with no human review
- Bank reconciliation
- Payroll
- Full management reporting / forecasting
- Procurement/PO automation (separate project)

---

## Success Criteria

MVP is done when the app can:
1. ✅ Connect to both UK and US Xero orgs
2. ✅ Sync core finance objects locally
3. ✅ Ingest an invoice PDF → create reviewed bill in Xero
4. ✅ Ingest an inventory report → create journal in Xero
5. ✅ Query posted transactions from internal UI

---

## Ava's Strategic Notes

**Priority call:** Unblock Xero auth first (both UK + US). Nothing else in this project moves without it. This is the current blocker and it needs Cem to action the OAuth setup.

**AP intake is the highest-value unlock.** Once documents can flow in automatically and hit Xero with one approval click, this removes significant manual finance work. Phase 2 should follow Phase 1 immediately.

**The journal engine (Phase 3) depends on clean account code mappings.** Harry will need input from Cem or the finance team on the exact Xero account codes for COGS, inventory adjustments, etc. This mapping work needs to happen in parallel with the build.

**Multi-lingual requirement is real.** The stock-out monitor already handles this via Airweave. The main app UI should default to English for MVP but the data layer needs to handle EN/ZH/ES/TL inputs.

**Next action for Cem:**
- Confirm Xero UK + US write access is granted to the app (OAuth)
- Provide Xero account codes for COGS / inventory journal mappings
- Confirm which email inboxes should be monitored for AP document intake

---

*Source: Harry's vault export — `XERO_FINANCE_APP_SCOPE.md` + `harry_daily_2026-04-04.md`*
*Last updated: 2026-04-09*
