# IT Department — Role Profiles & Automation Assessment
*Created: 2026-03-09 by Ava | Source: PH Staff Roster + Email Analysis*

---

## IT Team (5 staff, ₱117,000/mo ≈ $2,000 USD/mo)

### 1. Patrick Gaña — Jr. Software Engineer (₱25,000/mo)
**Actual role: Operations Engine Operator (effectively runs the entire order-to-label pipeline)**

**Daily tasks (verified from email trail, March 9 2026):**
- 02:00 AM — Generate Amazon Shipping labels for US/FL PO Wave 1
- 02:00 AM — Generate Fanatics US labels for US/FL PO Wave 1
- 02:02 AM — Generate FL Stamps/USPS labels Wave 1
- 02:02 AM — Create QR code labels for FL PO printing
- 02:03 AM — Create Stamps scan form + USPS form for FL
- 02:19 AM — Generate Daily SO for Sage MFG
- 02:39 AM — Generate USPS Buy Shipping acceptance scan forms (PH)
- 02:40 AM — Generate USPS Buy Shipping transaction report
- 02:42 AM — Generate USPS Stamps transaction report
- 03:44 AM — Respond to process documentation requests

**Key responsibilities:**
- Runs Zero automated PO scripts (manual fallback when automation fails)
- Generates picking lists via `sage_generate_picking_list_split.php`
- Creates and distributes label PDFs to FL and PH production
- Manages PO filtering rules (hardcoded PHP on EC2)
- Handles carrier-specific label generation (Amazon Buy Shipping, USPS, Stamps, RM, Veeqo)
- Generates scan forms for USPS/Stamps
- Creates daily SO reports for Sage MFG
- Troubleshoots Zero errors, carrier API issues, label failures

**Knowledge:** Only person who fully understands Zero scripts, cron jobs, PO filtering logic, and carrier integration. Drew's primary knowledge transfer target.

**Automation impact:** 80-90% of daily tasks are label generation + report emails that Veeqo automates. Remaining 10-20% is exception handling + Zero script maintenance.

**Transition recommendation:** Retain during parallel run (4-6 weeks). Can transition to Ops Coordinator role OR be replaced once Veeqo fully operational. Critical to document everything before any transition.

---

### 2. Mechelle Ann Gaña — Jr. Support Engineer (₱21,000/mo)
**Actual role: International Label Operator**

**Verified tasks (from email trail):**
- Generates DHL Warenpost labels for DE (Germany) POs
- Generates Deutsche Post (DP) labels — tracked and priority
- Generates Royal Mail label files for PH AMG1 orders
- Combines labels into PDFs
- Saves to GDrive and distributes

**Knowledge:** Label generation for international carriers (DHL, DP, RM). Subset of Patrick's knowledge.

**Automation impact:** 100% replaceable by Veeqo. All carriers she manages (DHL, DP, RM) are Veeqo-supported.

**Note:** Mechelle Ann Gaña — same surname as Patrick Gaña. Likely family members.

---

### 3. Jeric Tyron Padilla — Sr. Support Engineer (₱20,000/mo)
**Actual role: FBA Coordinator + Zero Data Entry**

**Verified tasks (from email trail):**
- Generates daily Zero Report — Sales Downloads
- Uploads POs to FL/PH Zero
- Creates FBA shipment preparations (per Drew's handover)
- Generates RM International Tracked Labels for AMG1 POs
- Generates daily SO for Sage MFG
- Stamps scan forms for FL printing

**Knowledge:** FBA shipment prep, Zero PO uploads, sales reporting.

**Automation impact:** 90%+ replaceable. FBA shipment prep is 10-step manual process that Amazon's Send to Amazon workflow + Veeqo handles. Daily reports replaceable by BQ → dashboard.

---

### 4. Dickel Pineda — Sr. Network & Systems Admin (₱33,000/mo)
**Actual role: IT Infrastructure Lead**

**Responsibilities (inferred):**
- Manages NAS storage (QNAP) in PH office
- Network administration for PH office
- Server maintenance (Zero EC2 instances, local servers)
- Hardware support for printing + image generation
- Manages IT infrastructure for 3 PH office locations

**Automation impact:** Partially replaceable. NAS + network still needed while image generation is on-premises. Once image pipeline moves to cloud, infrastructure needs shrink dramatically.

**Transition recommendation:** Chad takes over hardware/infra management. Dickel role eliminated or reduced to part-time.

---

### 5. Albert Bulaon — Jr. Network & Systems Admin (₱18,000/mo)
**Actual role: Network Support / Dickel's assistant**

**Responsibilities (inferred):**
- Junior network support under Dickel
- Printer/hardware maintenance
- General IT helpdesk

**Automation impact:** 100% redundant if Dickel's role is absorbed by Chad.

---

## Summary: IT Team Automation Assessment

| Staff | Salary | Role | Automatable | Recommendation |
|---|---|---|---|---|
| Patrick Gaña | ₱25,000 | Operations engine | 80-90% | Retain during transition → Ops Coordinator or exit |
| Mechelle Ann Gaña | ₱21,000 | International labels | 100% | Redundant once Veeqo handles intl carriers |
| Jeric Tyron Padilla | ₱20,000 | FBA + data entry | 90%+ | Redundant once Veeqo + FBA automation live |
| Dickel Pineda | ₱33,000 | Infrastructure lead | 60-70% | Replaced by Chad (image tools + hardware) |
| Albert Bulaon | ₱18,000 | Network support | 100% | Redundant with Dickel |

**Total IT cost:** ₱117,000/mo (~$2,000 USD)
**Post-automation:** 1 person (Chad) → ~₱25-33K/mo (~$500 USD)
**Savings:** ~₱84-92K/mo (~$1,500 USD/mo, ~$18K/yr)

---

## ❓ Open Question for Cem
**Who are the "other 2 guys" on Patrick's team?**
Based on roster, Patrick's immediate IT colleagues are:
- Mechelle Ann Gaña (labels)
- Jeric Tyron Padilla (FBA/Zero)
- Dickel Pineda (infrastructure)
- Albert Bulaon (network support)

**Who is Chad?** Not in the PH staff roster. Is he:
- A new hire?
- An existing staff member being reassigned?
- An external contractor?

Need clarification to complete the transition plan.

## Related
- [[wiki/12-org/PH_STAFF_ROSTER|PH Staff Roster]] — Full team salaries and roles
- [[wiki/23-drew-handover/PATRICK_WORKFLOW_PICKLIST_TO_IMAGE|Patrick's Workflow]] — What Patrick does daily
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE_MAP|Zero Infrastructure Map]] — Systems the team operates
- [[wiki/23-drew-handover/MEETING_CEM_BEA_PATRICK_2026-03-09|Meeting Notes Mar 9]] — Call with Patrick/Bea
