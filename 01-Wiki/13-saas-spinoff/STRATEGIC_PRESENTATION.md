# Ecell Global — Strategic Blueprint
## Executive Summary & Gap Analysis
### March 2026

---

# The Two Pillars

Ecell Global's transformation rests on two pillars. Everything else is a supporting project.

**Pillar 1: Revenue Growth** — $12.8M addressable
- 7 active revenue initiatives across Amazon, Target+, Walmart, OnBuy, Microsites, Kaufland
- $4.6M in Sports alone (76% of DTC)
- GoHeadCase Hub: $6M umbrella opportunity

**Pillar 2: Cost Reduction** — $105K/year savings
- PH headcount: 38 → 22 staff (16 reduced/redeployed)
- 3 automation tracks: Fulfillment, Listings, Customer Service
- 6-12 month transformation timeline

---

# Gap Analysis: Command Center vs Reality

| Project | Command Center Said | Actual Status | Gap |
|---------|-------------------|---------------|-----|
| Target+ | "Blocked" | LIVE, generating orders, Feedonomics deadline ~Mar 19 | Critical misstatement |
| ListingForge | Not listed | #1 cross-cutting blocker | Missing entirely |
| PH Automation | Not listed | $105K/yr savings mapped | Missing entirely |
| Fulfillment Orchestrator | Not listed | Harry built Phase 1 MVP | Missing — work already done |
| CS Chat Bot | Not listed | Phase 1 LIVE on N8N | Missing — already deployed |
| Mac Studio | "Active" | Complete, all agents migrated | Status correct |
| Sales Dashboard | "Blocked" | Phase 1 complete, GitHub access needed | Minor update |
| Sven Agent | "Blocked/crashing" | Migrated to Mac Studio, ready | Fixed |

**5 of 20 projects were materially wrong or missing. The two most urgent items (Target+, ListingForge) were invisible.**

---

# Pillar 1: Revenue Growth Stack

## P0 — Target+ / Feedonomics (URGENT)
- Revenue: $500K/yr
- Status: LIVE and generating orders
- Feedonomics contract ends ~March 19
- Cancellation initiated Feb 17 (email from Thew Maron, Commerce/Feedonomics)
- Jay Mark aligned on Shopify Marketplace Connect migration
- DECISION NEEDED: Platform preference, SKU count, monthly revenue

## P1 — Sports Microsite ($4.6M)
- 50/308 products loaded, prototype live
- Football = $4.2M (Liverpool, Arsenal, Barcelona top 3)
- Needs: Shopify Storefront API, device picker, image assets

## P1 — GoHeadCase Hub ($6M)
- Blocked on Shopify store creation (Cem action)
- Architecture: hub → category microsites → shared cart

## P1 — Walmart ($780K)
- 895 of top 1000 best sellers MISSING from Walmart
- Snap Cases ($350K), Desk Mats ($129K), Leather Wallets ($110K)
- Data partial: 10K of 95K loaded (pagination fix needed)

## P1 — Amazon FBA Conversions
- 76% of all revenue. SP-API key exists, not connected.
- BigQuery mirror active. 6.4GB listings ready to process on Mac Studio.
- Jay Mark's analysis: Naruto Itachi desk mat = biggest revenue leak (1,247 visitors, 2.57% CVR)

---

# Pillar 2: PH Automation & Cost Reduction

## Current PH Organization (38 Staff, ~$272K/yr)

### Production (10 staff)
- Joanna Rose (Mgr) + 9 staff
- Labels, picking, printing, image gen, QC
- **Automation target: 10 → 4** via Veeqo/ShipStation
- Harry built Fulfillment Orchestrator MVP (routing engine, label stubs, dispatch log)

### Listings (8 staff)
- Jay Mark (Lead), Jessie Morales (Replication Lead ₱42.5K/mo)
- 630 SKU replications/day per person (manual)
- Chad (Software Engineer) — maintains Dekr/Big C tools
- Patricia Shane — development background, AI candidate
- **Automation target: 8 → 4** via ListingForge

### Creative (6 staff)
- Bettina Pineda (Creative Mgr ₱101K/mo)
- Jeff — Figma, Samsung templates, coding background, AI-ready
- Nesley — detail-oriented, tested AI tools successfully, design + AI
- **Plan: Free from replication → actual design work**

### Customer Service (5 staff)
- Cris Guintu — most active (7 emails in sample), handles regulatory compliance
- Analiza Peralta — active but lower volume
- **Automation target: 5 → 3** via AI draft responses
- Phase 1 CS bot already live on N8N

### IT (5 staff)
- Bob left Feb 14, Chad absorbed some responsibilities
- 3 PH understudies handle day-to-day
- **Risk: cron jobs, API integrations, internal apps**

### HR (2) + Finance (2)
- Operational, no automation target

---

# Email & Communication Analysis

## Power Users (high activity, measurable output)
| Name | Role | Activity | Evidence |
|------|------|----------|----------|
| Jay Mark Catacutan | Listing Lead | 10 emails, daily completion reports, Amazon analysis, proactive strategy | Ran 28,855-product cross-analysis unprompted. Identified Naruto desk mat revenue leak. |
| Bettina Pineda | Creative Mgr | 10 emails, manages EOD reporting, skills evaluation, team coordination | Set up Slack EOD channels. Responsive, but Cem flagged lack of measurable outcomes in her reports. |
| Cris Guintu | CS | 7 emails, handles regulatory compliance (BE, ES markets) | Consistent, handles complex compliance. |
| Jessie Morales | Replication Lead | Low direct email but documented 630 SKU/day output | Produces measurable daily output. Cross-team quality gate. |

## Flagged for Review
| Name | Role | Concern |
|------|------|---------|
| Chad (Chadle Rei Miclat) | Software Engineer | Cem directly questioned overlap with Jessie. "High-level reports lacking measurable outcomes." Maintains Dekr/Big C tools but output unclear. 3 emails. |
| Leevis Manalansan | Unknown | 1 email (royalty report forward). No visible output. |
| Most IT staff | Various | No email activity in sample. Bob left, understudies visibility = zero. |

## AI-Ready Candidates (per Bettina + Jay Mark assessment, Feb 25)
- **Jeff** — Figma + coding background, creating Samsung S24/S25 templates, strong AI adoption
- **Nesley** — Detail-oriented, successfully tested AI tools, design + process skills  
- **Chadle** — Development background, potential for AI app work (Jay Mark nomination)
- **Patricia Shane** — Development background, AI candidate (Jay Mark nomination)

---

# Proposed New PH Org Chart (22 staff)

## Before: 38 staff, ~$272K/yr

Production (10) | Listings (8) | Creative (6) | CS (5) | IT (5) | HR (2) | Finance (2)

## After: 22 staff, ~$167K/yr (save ~$105K/yr)

### Production (4) — was 10
- Joanna Rose (Mgr) + 3 staff
- **Automated:** Veeqo/ShipStation for labels, pick lists, tracking sync
- **Harry's Fulfillment Orchestrator** handles routing logic

### Listings (4) — was 8
- Jay Mark (Lead) + Jessie (Replication) + 2 staff
- **Automated:** ListingForge for image compositing + copy generation
- Jessie shifts from manual replication → automation oversight
- Chad → AI/tools team OR evaluate

### Creative (4) — was 6
- Bettina (Mgr) + Jeff + Nesley + 1 staff
- **Freed from replication** → actual design, campaign assets, microsites
- Jeff + Nesley = AI-first creative production

### CS (3) — was 5
- Cris (Lead) + Analiza + 1 staff
- **Automated:** AI draft responses (N8N bot live), human approval loop
- Phase 2: voice agent (Twilio)

### IT (3) — was 5
- Absorbing Chad's skills or hiring AI-capable replacement
- Focus: maintain internal tools + support new automation

### HR (2) + Finance (2) — unchanged

---

# Automation Justification Map

| Dept | Current | Target | Reduction | Automation Tool | Status |
|------|---------|--------|-----------|-----------------|--------|
| Production | 10 | 4 | -6 | Veeqo/ShipStation + Fulfillment Orchestrator | MVP built by Harry |
| Listings | 8 | 4 | -4 | ListingForge (image + copy automation) | Specced, not built |
| CS | 5 | 3 | -2 | AI draft responses (N8N + Claude) | Phase 1 live |
| IT | 5 | 3 | -2 | Consolidation post-Bob departure | In progress |
| Creative | 6 | 4 | -2 | Redeployment (freed by ListingForge) | Pending ListingForge |
| **TOTAL** | **38** | **22** | **-16** | | **$105K/yr savings** |

---

# Critical Path

1. **This week:** Target+ / Feedonomics decision (deadline-driven)
2. **Next 2 weeks:** ListingForge build kickoff (unblocks everything)
3. **Month 1:** Amazon 6.4GB processing, Walmart gap completion, Sports microsite product load
4. **Month 2-3:** Fulfillment Orchestrator deployment, CS AI expansion, OnBuy UK launch
5. **Month 4-6:** GoHeadCase Hub launch, staff transition begins
6. **Month 6-12:** Full automation rollout, EU expansion (Kaufland), marketing funnels

**Total impact at 12 months:**
- Revenue: $12.8M addressable pipeline active
- Cost: $105K/yr recurring savings
- Staff: 38 → 22 (40% reduction, humane timeline with redeployment options)
