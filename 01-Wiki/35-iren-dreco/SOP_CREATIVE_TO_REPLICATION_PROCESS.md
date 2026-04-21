# SOP: Creative → Replication → Listing Image Process
**Source:** Bettina Pineda (Creative Manager) + Jessie Morales (IREN2 project)
**Date:** 2026-04-06 (extracted from emails)
**Owner:** Ava | **Status:** CANONICAL — as described by PH team

---

## Overview

Full end-to-end process for phone cases: from initial design creation through replication (DRECO) to listing image upload to AWS S3.

**Three phases:**
1. **Design** — Designer creates PSD artwork
2. **Replication** — DRECO tool generates listing images across all device models
3. **Upload** — Images pushed to AWS S3

---

## PHASE 1: DESIGN (Bettina's team)

### Step 1: Initial Design
- Designer creates one main raw file in **PSD format** using the **1-1 canvas template**
- This is the master artwork file for the design

### Step 2: Submission File
- Designer creates a `.jpg` submission file from the PSD
- Notifies Bettina via the **"FOR UPLOADING"** Teams group
- Bettina uses this mock-up as reference for manual product coding into trackers
- Mock-up is submitted online or via email to **licensors** for approval

### Step 3: Licensor Approval
- Design submitted to licensor
- Bettina inputs manual product coding into trackers during this phase

### Step 4: Canvas Preparation
- Once concept is **approved**, designer prepares remaining canvas templates
- **13 canvas templates total** — to accommodate replication script across all available device models
- After completing canvas files, designer notifies Bettina via **"FOR REPLICATION / LISTING"** Teams group

### Step 5: Email Template Creation (Bettina)
Bettina generates an email template with:
- **Header:** License Name + Product Type + Batch Number
- **Body:** Lineup Name, Tracker Link, Product Category, Canvas Repository Link

### Step 6: Replication + Listings Teams Notified
- **Replication Team:** Begins extracting codes via Tracker Link, runs canvas templates through script and DRECO tool
- **Bettina (simultaneously):** Collates all titles in separate tracker for Listings Team to perform database insert

---

## PHASE 2: REPLICATION — DRECO 1 (Jessie's team)

### Creating RawImages (JPEGs) — DRECO 1

**Step 1: Get inputs from replication email**
- PSD link (canvas repository)
- Lineup tracker link

**Step 2: Extract codes**
- Take the design codes from the tracker
- Input codes into **Photoshop ExtendScript Toolkit**
- Run the script while checking output

**Step 3: DRECO 1 Rendering — Listing Image Creation**

Pre-requisite before running:
- Ensure all lineups to render are **added/inserted to the database (LSE)**
- If lineups are in the database → ready to run DRECO 1

Execution:
1. Run DRECO 1 tool
2. Hit **"Replicate" button**
3. Tool creates listing images across all device models
4. Window pops up when replication is complete

---

## PHASE 3: UPLOAD TO AWS S3

**Step 1:** Once all images are complete
**Step 2:** Drag the **lineup folder** to the AWS S3 server
**Result:** Images available at `https://elcellonline.com/atg/{DESIGN}/{VARIANT}/{PREFIX}-{DEVICE}-{POS}.jpg`

---

## KEY DATABASES (from Jessie)

Two SQL database files shared:
- **headcase.sql** — headcase database (product/design data)
  - GDrive: https://drive.google.com/file/d/1e3vomGTl3C3zl1DQlYdFnFyza_oMcSMJ/view
- **replication.sql** — replication database (LSE — where lineups must be inserted before DRECO runs)
  - GDrive: https://drive.google.com/file/d/18FrZhLIoowj7_sdA4wBdQ29FHp0v2mNR/view

**Critical finding:** DRECO requires lineups to be **pre-inserted into the LSE database** before replication can run. This is the database handshake between the design approval phase and the replication phase.

---

## LISTINGFORGE INTEGRATION NOTES

This SOP maps directly to ListingForge's pipeline:

| Manual Step | ListingForge Automation |
|---|---|
| Designer creates 13 canvas templates | ListingForge uses jig_measurement data for all devices |
| Bettina sends email with tracker link | ecell.app license entry → design_code registered |
| Codes input to ExtendScript toolkit | ListingForge reads design_code from Supabase |
| DRECO renders images per device | ListingForge Lane 1 composites per device using Pillow |
| Lineup inserted to LSE database | SKU written to license_skus table in Supabase |
| Images dragged to S3 | Images auto-uploaded to S3 via script |

**Key difference:** Current process requires 13 PSD canvas files per design. ListingForge generates all device variants from ONE design file using jig coordinate data. This is the automation win.

---

## PEOPLE & CHANNELS

| Person | Role | Contact |
|---|---|---|
| Bettina Pineda | Creative Manager | b.pineda@ecellglobal.com |
| Jessie Morales | IREN2 / Replication | j.morales@ecellglobal.com |
| Teams group: "FOR UPLOADING" | Design submission notifications | — |
| Teams group: "FOR REPLICATION / LISTING" | Canvas completion notifications | — |

---

## BETTINA'S FULL PROCESS DOC

Bettina is currently collating the full Design → Replication (DRECO) → Image Preparation (IREN) process in a single file. **Due: April 7, 2026 (today PH time).**

When received, add to this SOP and update ListingForge spec accordingly.

---

*Source emails: gemc@ecellglobal.com inbox, April 6 2026 (PH time)*
*Extracted by Ava | Filed to wiki/35-iren-dreco/*
