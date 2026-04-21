# Email Digest — 2026-04-07
*Extracted by Athena (librarian) | Filter: TO gemc@ or FROM @ecellglobal.com*

---

## 1. 🔴 IREN2 Process — Full Design-to-Replication Pipeline (Bea + Jessie)
**Thread:** Re: IREN2 project | **Date:** Apr 6-7 | **People:** Bea Pineda, Jessie Morales, Jay Mark, Tim, Joanna

### Bea's Full Process (Design → Replication for Phone Cases)

**Stage 1 — Initial Design:**
- Designer creates 1 raw PSD file using the **1-1 canvas template**
- Designer creates a .jpg submission and notifies Bea via **"FOR UPLOADING" Teams group**
- Bea uses the mock-up for manual product coding in trackers
- Mock-up submitted to licensors for approval (online or email)

**Stage 2 — Canvas Preparation:**
- Once concept approved, designer prepares **13 canvas templates total** to cover all device models
- These are the variants the replication script needs

**Stage 3 — Notification:**
- Designer notifies Bea via **"FOR REPLICATION / LISTING" Teams group**

**Stage 4 — Email Template (BEING REPLACED):**
- Bea generates email with: License Name, Product Type, Batch Number, Lineup Name, Tracker Link, Product Category, Canvas Repository Link
- **Cem's directive:** This manual email step → replaced by data entry to new app (ecell.app) with image links. Same DB for content, listing images, product images, listings.

**Stage 5 — Execution:**
- Replication Team extracts codes via Tracker Link
- Runs canvas templates through script + Dreco Tool
- Bea collates titles in separate tracker for Listings Team to do DB insert

### Jessie's Dreco Process (Replication)

**Dreco 1 — Creating RawImages (JPEGs):**
1. Get PSDs link + lineup tracker link from replication email
2. Take codes from tracker → put into **Photoshop ExtendScript Toolkit**
3. Run script → outputs JPEGs (these are what Dreco uses, NOT the PSDs directly)
4. PSD → JPEG conversion via Photoshop script first

**Dreco 1 — Rendering (Listing Image Creation):**
1. Ensure lineups are inserted into database (LSE)
2. Run Dreco1 → creates listing images
3. Hit "Replicate" button → generates all images
4. Window pops up when done

**Upload:**
- Drag lineup folder to AWS S3 server manually

### Technical Details (from earlier thread)
- **MySQL DB:** `elcell_co_uk_barcode` on 192.168.20.160 (local) + AWS RDS
- **IREN credentials:** `iren-images-renderer/src/main/resources/config.properties` (db155_* and dbrds_* keys)
- **Dreco credentials:** `Dreco/src/main/java/dreco/Configuration.java` (hardcoded in getDefault())
- **Red rectangle layer** = safe zone guide for camera/device holes (keeps logos/legal lines clear)
- **PSDs stored on 5TB drive**, organized by license folders
- **IREN uses jig data** from `t_jig_devices` table for width/height/padding
- **Device mapping:** e.g. TP-IPH17PRO → 2-1 category

### Cem's Vision (from reply)
> "Instead of email we will require data entry to a new app with image links. Same database for content, listing images, product images, listings. Centralised view from idea gen to sales, fulfillment, printing. Starting with One Piece."

**⚡ Action:** This maps directly to Blueprint V3 Stages 2-4. Bea's process doc is the current-state baseline for automation.

---

## 2. 🟡 Stock Reorder — Chris Yunun
**Thread:** Re: Cases Reorder April 01, 2026 | **Date:** Apr 7 | **People:** Chris Yunun, Karen Alfonso, Joanna Vitug

- Chris submitted weekly reorder for review/approval
- **Cem asked:** Did Chris add stock from last CN shipments to UK and FL before running?
- **Chris confirmed:** Disregarding all outstanding orders from Mar 3 and Mar 24
- **Implication:** Old POs being cleaned up, fresh reorder based on current stock levels

**⚡ Action:** Relates to Harry's procurement corrections (EOL removal + shipping split approval pending from Cem)

---

## 3. 🟡 DRECO/IREN Documentation Push — Bea
**Thread:** Re: April 8, 2026 - Vacation Leave Request | **Date:** Apr 7

- Bea is collating the **Design → Replication (Dreco) → Image Preparation (IREN) process in a single file**
- Target: deliver today (Apr 7)
- Quote: "I understand regarding DRECO and IREN and I've been pushing this since yesterday. I will definitely focus on this and meet with the relevant people so we can compile and share all"

**⚡ Action:** When Bea delivers this doc, librarian should extract and update wiki/35-iren-dreco/ and wiki/03-production/

---

## 4. 📦 Ben (Foxmail/CN) — Supplier Shipments
**From:** ben.ecellglobal@foxmail.com | **Date:** Apr 1 (4 shipments)

| Shipment | Route | Tracking | Contents |
|----------|-------|----------|----------|
| CN-PH-20260327 | UPS HK → PH | 1Z3153V10445842447 | Cases |
| CN-UK-20260327 | UPS HK → UK | 1Z3153V10443305709 | Cases |
| CN-US-20260330/31 | FedEx → US | 870106564699 / 870194309397 | Plastic sheets + cases |
| CN-US-20260325 | FedEx → US | 889956990728 | Small desk mats + cases |

**Earlier thread (Mar 26):** Ben asked about reactivating UPS HK account (cheaper than DHL). Cem/Ant involved.

**⚡ Action:** These shipments are the stock Chris Yunun should have added before running the reorder. Confirms CN supplier (Ben) is active and shipping to all 3 offices.

---

## 5. 🆕 Jay Mark — Shipping Tool Update
**Thread:** Re: QA Report — Ecell Shipping Tool v1.0 (EVRI repo) | **Date:** Apr 7

- Jay Mark confirms he'll **remove DHL from the shipping app** and simplify routing to just Evri (EU) and Royal Mail (UK)
- This is in response to Cem sending IP addresses to contacts and dropping DHL

**⚡ Action:** Jay Mark already productive on day 1. Ship tool simplification aligns with Blueprint V3 Stage 8.

---

## 6. 📋 S3 Image URL Rules (Jessie → Ava/Cem)
**Thread:** Re: S3 Image URL Rules — Need Full Documentation | **Date:** Mar 31

- Jessie provided complete S3 image URL rules + full spreadsheet attached
- Covers: image positions, naming conventions, path structure
- Sent to gemc@ (responding to Ava's request)

**⚡ Action:** Critical for ListingForge image upload paths. Should be in wiki/10-listingforge/ if not already.

---

*6 business threads extracted. 0 noise processed. Librarian digest complete.*
