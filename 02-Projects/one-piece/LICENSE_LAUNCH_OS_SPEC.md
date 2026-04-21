# License Launch OS — Spec v0.1
**Owner:** Ava (Strategy) | **Builder:** Harry | **Date:** 2026-04-06
**Pilot license:** One Piece
**Status:** DRAFT — for Cem review

---

## The Vision

Every time we sign a new license, there is currently no single place that tracks the journey from "contract signed" to "first sale live." Departments work in silos. This system changes that.

**License Launch OS** is a page in ecell.app where a human enters the license details once, and everything downstream — SKU generation, image creation, content creation, listing upload, and sales tracking — flows from that single source of truth.

---

## User Flow

```
HUMAN ENTERS LICENSE DETAILS (once)
         ↓
┌─────────────────────────────────────┐
│         LICENSE DETAILS PAGE        │
│  • License name: One Piece          │
│  • Licensor: Toei Animation / Viz   │
│  • Contract PDF: [upload]           │
│  • Royalty %: [enter]               │
│  • Territory: US, UK, EU            │
│  • Expiry: [date]                   │
│  • Design code prefix: ONEP         │
│  • Allowed product types: [select]  │
│  • SKU prefix auto-assigned: ✅     │
└─────────────────────────────────────┘
         ↓
TRACKER CREATED AUTOMATICALLY
         ↓
┌─────────────────────────────────────────────────────────────┐
│                    LAUNCH TRACKER                           │
│                                                             │
│  Phase 1: CREATIVE                                          │
│  ☐ Design brief created → [Sven]                           │
│  ☐ Character list approved → [Cem]                         │
│  ☐ Design files uploaded (PSD/EPS) → [PH Creative]         │
│  ☐ Images approved → [Sven/Cem]                            │
│                                                             │
│  Phase 2: LISTING PREP                                      │
│  ☐ SKUs generated from design codes                        │
│  ☐ EANs assigned                                           │
│  ☐ Listing images composited (ListingForge)                │
│  ☐ Titles/bullets generated (Echo)                         │
│  ☐ Content QA'd                                            │
│                                                             │
│  Phase 3: GO LIVE                                          │
│  ☐ Amazon US uploaded                                      │
│  ☐ Amazon UK uploaded                                      │
│  ☐ Shopify uploaded                                        │
│  ☐ Walmart staged                                          │
│                                                             │
│  Phase 4: MONITOR                                          │
│  ☐ First 7 days sales tracked                              │
│  ☐ PULSE velocity signal active                            │
│  ☐ Royalty accrual tracking live                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Page Structure in ecell.app

### `/licenses` — License Dashboard
- Grid of all active licenses with status indicator
- Click any → goes to license detail page
- Add New License button

### `/licenses/[id]` — License Detail Page

**Section 1: License Info**
- Name, licensor, territory, expiry, royalty %
- Contract PDF viewer (or GDrive link)
- Design code prefix + list of assigned design codes
- Allowed product types

**Section 2: SKU Generator**
- Human or AI enters: design code, character name, product types
- System generates full SKU list: `ONEP[CODE]-[DEVICE]-[DESIGN]-[VARIANT]`
- Export to CSV for bulk upload

**Section 3: Launch Tracker**
- Kanban-style: Creative → Listing Prep → Live → Monitoring
- Each card = one design or design group
- Assignee, status, due date, blocking flag
- Links to: design file, listing image, Amazon URL

**Section 4: Performance**
- Revenue this month vs royalty obligation
- Top 5 designs by velocity
- Alert: if royalty pace is below MG target

---

## Data Model

```sql
-- License master
licenses (
  id, name, licensor, design_prefix, royalty_pct,
  territory[], product_types_allowed[],
  contract_url, expiry_date, mg_annual, mg_currency,
  status [active|expired|pending]
)

-- Design codes under this license
license_designs (
  id, license_id, design_code, character_name,
  design_name, file_url, approved_at, approved_by
)

-- Launch tracker cards
launch_tasks (
  id, license_id, design_id, phase [creative|listing|live|monitor],
  task_name, assignee, status [todo|in_progress|done|blocked],
  due_date, blocking_reason, linked_url
)

-- SKUs generated
license_skus (
  id, license_id, design_id, seller_sku, asin,
  marketplace, listed_at, status [staged|live|suppressed]
)
```

---

## Integration Points

| System | How it connects |
|--------|----------------|
| ListingForge | Receives design_code + product_type → returns composite images |
| Echo (copy agent) | Receives design_name + product_type → returns title/bullets |
| EAN database | Auto-assigns EANs when SKUs are generated |
| Supabase orders | Revenue tracking per design_code |
| BigQuery | Royalty accrual calculations |
| GDrive | Contract PDF storage, design file storage |

---

## Build Plan

**Phase 1 — MVP (2 weeks, Harry builds)**
- License detail page with manual entry
- SKU generator (takes design code, outputs SKU list CSV)
- Basic launch tracker (static checklist, manual status updates)
- One Piece as pilot data

**Phase 2 — Automation hooks (4 weeks)**
- ListingForge integration → image auto-generates when design approved
- Echo integration → copy auto-generates
- EAN auto-assignment
- Slack notification on phase transitions

**Phase 3 — Intelligence layer (6 weeks)**
- Revenue vs royalty tracking live
- Velocity alerts (new license underperforming → flag)
- Automated royalty report generation

---

## One Piece Pilot — Starter Data

```
License: One Piece
Licensor: Toei Animation / Viz Media
Design prefix: ONEP
Royalty %: [Cem to confirm]
Territory: US, UK, EU, AU
Product types: HTPCR, HB401, HLBWH, HB6CR, HB7BK, HDMWH, H8939
Contract: [upload when available]

Starter design codes (from Sven brief):
ONEPGR5 — Gear 5 Luffy
ONEPSHA — Shanks
ONEPZON — Zoro
ONEPLAN — Nami
ONEPSNH — Sanji
ONEPCHO — Chopper
ONEPACO — Ace
ONEPYLA — Yamato
ONEBBCK — Blackbeard
ONEPIKM — Nika/Mythic
```

---

*Spec v0.1 — Cem to review and add contract details | Harry to build MVP by Apr 20*
