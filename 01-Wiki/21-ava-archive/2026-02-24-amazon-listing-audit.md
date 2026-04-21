# Nightly Mission — Amazon Listing Audit (Tue)
**Date:** 2026-02-24 (2:00am ET)
**Brand:** Head Case / GoHeadCase (Ecell Global)

## What I audited (data source)
I pulled and analyzed **233 NBA sample listings** from:
- `gdrive:.../Projects/goheadcase/NBA sample listings.xlsx`

This sheet looks like a BigCommerce export containing **draft/target Amazon titles** + **backend search terms** inside `CustomFields`.

---

## Executive summary (highest impact fixes)
1. **Title bloat is hitting Amazon’s ~200 character ceiling**
   - **AmazonTitle length:** min **132**, avg **170.5**, max **200** chars
   - Several SKUs are **exactly 200 chars**, meaning important words can be truncated in SERPs and on mobile.
2. **Redundant phrasing is wasting characters and hurting readability**
   - Common pattern: `Compatible with <Device> and Compatible with MagSafe` (duplicate “Compatible with”).
3. **Device model mismatch / formatting errors in a non-trivial subset**
   - **29/233** titles don’t contain the exact `DeviceModel` string from the product data.
   - Example issue: `Compatible with Apple iPhone 12 / and Compatible with MagSafe` (stray `/`).
4. **Backend keywords are consistent but overly “generic” (low incremental SEO lift)**
   - Backend search terms length: min **209**, avg **216.8**, max **218** chars.
   - Terms are mostly protective-case adjectives; limited inclusion of high-intent synonyms (e.g., “cover”, “phone cover”, “team case”) and device shorthand.

---

## Detailed findings

### A) Title template quality
**Current common title template** (observed):
`Head Case Designs Officially Licensed NBA <Design> <Team> <Case Type> [Military Grade Protection] Compatible with <Device> and Compatible with MagSafe`

**What’s good**
- Strong authority terms: *Officially Licensed*, *NBA*
- Includes team + design name (good differentiation)
- Includes device compatibility (critical)

**What’s hurting performance**
- **200-char ceiling pressure** from:
  - Repeating “Compatible with” twice
  - Long case-type naming (“Shockproof Bumper Case”, “Soft Gel Case” etc.)
  - In some cases “Black and White Logo Los Angeles Lakers …” style stacking

**Recommendation: enforce a tighter, consistent title spec**
Use a strict priority order and remove redundancy:

**Proposed Title Spec (<= 170–180 chars target):**
`Head Case Designs Officially Licensed NBA – <Team> <Design> – <Case Type> for <Device> (MagSafe Compatible) [Military Grade Protection]`

Notes:
- Replace **“Compatible with X and Compatible with MagSafe”** → **“for X (MagSafe Compatible)”**
- Use separators `–` to improve scanability
- Keep “Officially Licensed NBA” near the front


### B) Character limit / truncation risk
Top 5 longest titles in sample are **200 chars** (maxed out). These are at high risk of truncation.

**Action:** add an automated validator in the listing pipeline:
- hard fail at **>195 chars** (buffer for variation)
- warn at **>180 chars**


### C) Device-string mismatch (29 SKUs)
These may still be “technically correct” for humans but can break:
- internal QA rules
- device-based Amazon search match
- variation naming conventions

**Action:** ensure the exact device string appears in the title OR use a standardized device token mapping.
Example fix:
- Bad: `Compatible with Apple iPhone 12 / and Compatible with MagSafe`
- Good: `… for Apple iPhone 12 (MagSafe Compatible)`


### D) Backend keywords (GenericKeywords)
Current backend keyword set is consistent and clean (no duplicates detected), but it’s mostly protection adjectives.

**Action (quick win):** keep the protection terms, but add *high-intent synonyms* and *device shorthand* where allowed.
Suggested additions (rotate/AB test depending on device & category rules):
- `cover`, `phone cover`, `case cover`
- `team case`, `basketball case`, `nba team`
- device shorthand: `iphone 17 pro max`, `galaxy s21 plus`
- material synonyms: `tpu`, `silicone`, `bumper`

**Caution:** Amazon backend search terms policies change; avoid:
- competitor brand names
- repeated words
- promotional claims

---

## Prioritised fix list (do these in order)

### P0 (today / this week)
1. **Title cleanup macro:** replace `and Compatible with MagSafe` with `(MagSafe Compatible)` and remove duplicate “Compatible with”.
2. **Device string QA:** fix the **29** device mismatch rows (and catch any “/” artifacts).
3. **Title length guardrails:** enforce max length with a linter in the listing generation process.

### P1 (next 1–2 weeks)
4. **Standardize naming tokens** across all lines:
   - `for <Device>` instead of `Compatible with <Device>`
   - consistent case type naming (one canonical name per product type)
5. **Backend keyword refresh:** introduce 1–2 alternate keyword sets per product type (Gel vs Bumper) and A/B across a subset.

### P2 (when updating creative)
6. **Image set + A+ content checklist** (applies to every listing):
   - Main image: pure white, full case, high-res
   - 2–3 feature callouts: MagSafe compatibility, drop protection, material/finish
   - 1 lifestyle shot (in-hand / on device)
   - 1 “licensed authenticity” graphic (NBA + team mark per brand guidelines)
   - A+: cross-sell other teams/designs + brand story + quality proof points

---

## Example rewritten titles (copy/paste ready)
Below are example rewrites that preserve meaning but cut characters and improve readability.

### Example 1 (Gel case)
**Original (sample):**
`Head Case Designs Officially Licensed NBA Stripes Golden State Warriors Gel Case [Military Grade Protection] Compatible with Samsung Galaxy S21+ 5G and Compatible with MagSafe`

**Rewrite:**
`Head Case Designs Officially Licensed NBA – Golden State Warriors Stripes – Gel Case for Samsung Galaxy S21+ 5G (MagSafe Compatible) [Military Grade Protection]`

### Example 2 (Bumper case, long team/design)
**Original (sample):**
`Head Case Designs Officially Licensed NBA Black and White Logo Los Angeles Lakers Shockproof Bumper Case [Military Grade Protection] Compatible with Apple iPhone 15 Pro Max and Compatible with MagSafe`

**Rewrite:**
`Head Case Designs Officially Licensed NBA – Los Angeles Lakers Black & White Logo – Shockproof Bumper Case for iPhone 15 Pro Max (MagSafe Compatible) [Military Grade Protection]`

---

## Next automation step (optional but high leverage)
If you want, I can generate a **CSV “patch file”** that:
- rewrites `AmazonTitle` for all 233 rows using the new spec
- flags any row that still exceeds a chosen limit (e.g., 180 chars)

(That would let the team bulk-update listings instead of manual edits.)
