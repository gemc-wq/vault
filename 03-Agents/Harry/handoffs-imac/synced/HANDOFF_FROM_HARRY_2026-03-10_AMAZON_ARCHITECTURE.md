# HANDOFF FROM HARRY — Amazon-First Listings Intelligence / Centralized Database
*Date: 2026-03-10*
*To: Ava*
*From: Harry*
*Priority: High*

## Why this handoff exists
Cem wants the architecture and scope discussion captured cleanly and handed to you because your Mac Studio has more RAM/storage headroom for large-file ingestion and heavier data work.

## Current decision
Do **not** start with the full SKU-parsing / new-product creation engine.

### Immediate priority
Build **Stage 1: Amazon-first listings intelligence + centralized store** to identify:
- what is live on Amazon now
- what is selling best
- what devices / designs / product types are winning
- what is missing on Walmart / microsites / other channels
- what PH should list next

This is the fastest path to getting:
- Walmart bestsellers live
- GoHeadCase / microsites live with bestsellers
- other marketplaces seeded from proven Amazon winners

## Cem’s current architecture direction
### In scope now
1. **Centralized store / database**
   - holds Amazon live listings + performance-derived target matrix
   - supports gap analysis across channels
   - becomes the operational shortlist for what to launch next

2. **Amazon as primary source signal**
   - Amazon is core business seller
   - products should generally be proven on Amazon first
   - then expanded to Walmart / BigCommerce / Shopify / microsites / other channels

3. **Reactive target matrix**
   - may be updated on a weekly cron cadence
   - does not need to be SKU-only at first
   - can operate at a practical planning grain such as:
     - device
     - design
     - form factor / product type
   - goal = define core target products and listing gaps dynamically from what is actually selling

### Explicitly not Stage 1
- full ideation → creation database as the first build
- dependence on legacy Zero/PHP as the required source of truth
- trying to fix every old sync before creating a usable modern foundation

## Important constraints surfaced by Cem
- Amazon live listings export is currently available as a **TXT** file
- sample file already exists
- full file is believed to be around **6GB**
- ingesting giant raw files on the iMac is undesirable due to limited disk/RAM
- likely better for you / Mac Studio to handle heavy ingestion and staging

## Harry’s recommended architecture direction
### Stage 1 — centralized Amazon-first store
Build a clean store for:
- Amazon live listings
- Amazon performance / bestseller signals
- cross-channel listing presence
- target/gap matrix

### Stage 2 — recurring Amazon update pipeline
- daily live-listings refresh if possible
- weekly or regular performance update cadence
- use exports / API / reports without depending on old Zero if not needed

### Stage 3 — channel expansion layer
Use the target matrix to drive rollout into:
- Walmart
- GoHeadCase microsite
- smaller marketplaces
- Shopify / BigCommerce where relevant

### Later Stage — deeper product composition engine
The reusable rules-driven title / description / SKU parsing system is still important, but Cem is positioning it as **later foundation-building**, not the immediate implementation priority.

## Current schema/audit read from Harry
I started reviewing the old Supabase schema plus synced wiki/specs.

### Early conclusion
The old schema is **too high-level / marketing-oriented** for the immediate need.

### Useful reusable pieces
- products
- listings
- devices
- designs
- licenses

### Missing for current priority
- Amazon-first performance layer
- bestseller / opportunity scoring for rollout
- listing gap matrix across channels
- target product queue for PH
- channel rollout states and publish priority workflow

### Missing for later rules-driven engine
- reusable attributes/components for title composition
- parsing logic
- composition rules
- channel-specific mapping templates
- publish/readiness states in a more operational form

## Cem’s core objective in plain language
Move from planning/spec conversations into implementation.

What he wants right now:
- identify best-selling Amazon items/opportunities
- identify where those winners are not yet listed elsewhere
- create a clean spec with no overlaps
- modernize around BigQuery / Google stack / Supabase / whatever is best
- avoid depending on inaccessible local Zero logic if Amazon data can provide the needed signal anyway

## Recommended technical stance
### Best near-term pattern
- **Big raw TXT / report ingestion** should be handled via a stronger machine / local staging process
- do **not** make Supabase the first landing zone for a raw 6GB TXT
- better pattern:
  1. local staging / parsing on Mac Studio
  2. clean load into BigQuery or a curated database layer
  3. push smaller operational tables downstream

### Logical data layers
1. **Raw/source layer**
   - Amazon live TXT exports
   - Amazon reports / API data
2. **Centralized intelligence layer**
   - listings current state
   - performance signals
   - target matrix
   - channel gap tables
3. **Execution/output layer**
   - Walmart listing priorities
   - microsite seed sets
   - Shopify / BigCommerce feeds if needed

## What Harry suggests Ava owns next
1. Review current synced wiki/specs and Harry’s read above
2. Confirm best Stage 1 storage/processing stack on Mac Studio
3. Propose exact table model for:
   - Amazon live listings current
   - Amazon performance facts
   - channel presence matrix
   - target product matrix
   - rollout priority queue
4. Decide ingestion method for the ~6GB TXT:
   - direct parse to local staging DB
   - direct load to BigQuery via staged file
   - hybrid
5. Recommend the practical first deliverable for Cem:
   - Walmart bestsellers gap report
   - GoHeadCase bestseller seed list
   - weekly target-matrix update job

## Final summary
This is **not** “build the whole future product engine first.”

It is:
1. build a modern Amazon-first centralized intelligence layer
2. use it to identify winners + channel gaps
3. push those winners into Walmart / microsites / other channels
4. then build the deeper rules-driven product-composition system on top later

— Harry
