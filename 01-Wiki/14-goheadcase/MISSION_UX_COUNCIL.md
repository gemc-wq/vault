# GoHeadCase — Mission, Context, and Expert UX/CRO Council (v1)

*Drafted from our Feb 20 strategy conversation + council reviews (Gemini + Opus) and the GoHeadCase constraints.*

---

## 1) Background / Context (what’s true)
GoHeadCase / Head Case Designs is a **licensed-first** print-on-demand accessories business.

**Economic reality**
- Typical phone case: **$20 sale price** with **~$2.50 landed cost**.
- Royalty: **15–20%**.
- Amazon fees: **19–25%**.
- Confirmed by Cem: **~33% gross margin after all direct costs (incl. shipping + royalties + fees)**.

**Strategic reality**
- We are *not* Casetify. Fans often arrive with **IP intent**.
- The market is crowded (Amazon sellers, official stores, other licensees). License alone is not enough.
- Our two existential risks are:
  1) **CAC drift** (one bad month can erase profit)
  2) **Platform dependency** (Amazon changes can be existential)

Therefore: the plan must maximize **conversion efficiency** and build **first‑party customer ownership**.

---

## 2) North Star (highest-probability positioning)
### Primary North Star (Phase 1: 0–90 days)
**Licensed-first + performance-first:**
> “The safest, easiest place to buy the *right* officially licensed case (for the exact device), delivered fast, at a better price.”

**Messaging structure (consensus):**
- **Lead with identity/fandom** (why they want it)
- **Prove with trust + fit + protection + delivery** (why they trust us)

### Phase 2 (90–365 days)
Layer in Casetify-style strengths (drops, collabs, community) **after** the conversion machine + asset library are stable.

---

## 3) Mission (what we are building)
Build a **gold‑standard ecommerce system**—benchmarking Apple/Casetify/OtterBox-level UX and merchandising—that can be deployed as:
- a reusable **template** (homepage → collection → PDP → cart)
- universe-specific **landing pages** (Anime/Sports/Fantasy/etc.)
- a fast **creative engine** that outputs assets at scale

…while keeping margins safe by enforcing:
- disciplined CAC
- high conversion rate
- first-party capture (email/SMS) from Day 1

---

## 4) Operating model (lean studio)
### Human roles
- **Ava (PM / Creative Director):** briefs, priorities, acceptance criteria, quality bar.
- **Build Engineer (human dev):** implements storefront, performance, analytics, deployments.

### System role (the “engine”)
- **Harry (Engine Operator — a system, not a person):** automation workflows that churn out:
  - product images & variants
  - banners & modules
  - copy variants (PDP/landing)
  - listing + QA helpers

---

## 5) Expert Agent Council (specialists, RAG-backed)
All agents reference a shared **RAG library**:
- gold-standard screenshots + notes (Apple/Casetify/OtterBox/Fanatics/official stores)
- our own past experiments + results
- our template rules + asset specs

### A) Design Critic (Gold Standard Reviewer)
**Output:** ruthless gap analysis + prioritized fixes.
- Scores pages on hierarchy, typography rhythm, merchandising clarity, trust proof, motion polish, and mobile.

### B) Ecommerce UX Architect (Template Builder)
**Output:** wireframes + component specs + mobile rules.
- Converts strategy into a reusable module system.

### C) CRO Strategist (Unit Economics Guardian)
**Output:** experiments ranked by expected impact + CAC ceiling.
- Sets margin floor rules, CAC caps, and test design.

### D) Merchandising Director (Universe Builder)
**Output:** category logic, best-seller logic, bundles/cross-sell.
- Defines “Shop by IP → Shop by device → best sellers” flow.

### E) Creative Director (Asset System)
**Output:** campaign concepts + asset checklists (ratios, safe zones, counts).
- Ensures visuals are premium and consistent.

### F) Influencer/Growth Operator
**Output:** micro-influencer playbooks, affiliate structures, content briefs.
- Focus on low-CAC fan reach and attribution.

### G) Data Analyst (Amazon + BQ/Supabase)
**Output:** conversion by license/product/device + opportunity mining.
- Identifies high-sessions/low-conversion opportunities.

### H) Asset Librarian / QA Gate
**Output:** naming conventions, completeness checks, consistency enforcement.
- Prevents “placeholder” assets from shipping.

---

## 6) RAG Library (what we store)
1) **Gold Standard Library** (screenshots + annotated notes):
   - Apple product pages
   - Casetify: home, collab/drop pages, PDP, navigation
   - OtterBox: protection proof systems
   - Fanatics/official stores: sports merchandising

2) **Our Template Bible**:
   - module list + do/don’t rules
   - type scale, spacing, motion principles

3) **Asset Library**:
   - hero banners (desktop/mobile)
   - category tiles
   - macro textures
   - trust icons + license proof

4) **Experiment Log**:
   - hypotheses, variants, results

---

## 7) Immediate next steps (7–10 days)
### Step 1 — Decide Universe #1
Pick **Anime (US)** vs **Football (UK)** using a scoring rubric:
- catalog depth (design count)
- influencer access
- competition intensity
- shipping advantage
- conversion + margin profile

### Step 2 — Build the “Universe Landing Template v1”
Required modules:
1) Identity-led hero
2) Shop by IP
3) Shop by device (fast)
4) Best sellers
5) Trust row: licensed authenticity + fit guarantee + shipping + returns

### Step 3 — First-party capture from Day 1
- Package insert + QR → warranty/collector club + incentive
- Email/SMS flows: gift reminders, new drops, back-in-stock

### Step 4 — Asset Library Spec v1
Define exact counts + ratios + safe zones for the template.

### Step 5 — Micro-influencer pilot
- 10–30 creators
- affiliate codes + tracking plan
- weekly creative refresh cadence

---

## 8) Success metrics (Phase 1)
- Conversion rate lift (by universe landing)
- CAC within ceiling
- Email/SMS capture rate
- Repeat purchase rate off-Amazon (purchase #2)

---

## Appendix: SKU parsing (canonical rule)
SKU format: `ProductType-Device-DesignCode-Variant...`
Inventory match key: `ProductType-Device` only.

---

## Related
- [[wiki/14-goheadcase/MASTER_PROJECT_MAP|Master Project Map]] — Full project scope
- [[wiki/14-goheadcase/TEAM_MISSION_STRATEGY|Team Mission Strategy]] — Strategic direction
- [[wiki/14-goheadcase/DESIGN_HUB_SPEC|Design Hub Spec]] — Design system for GoHeadCase
- [[wiki/14-goheadcase/STORE_NAV_RULES|Store Navigation Rules]] — UX navigation
- [[wiki/14-goheadcase/PHASE0_MICRO_CATALOGUE|Phase 0 Micro Catalogue]] — MVP scope
- [[wiki/11-product-intelligence/PROJECT_BRIEF|PIE Project Brief]] — SKU selection feeds GoHeadCase
