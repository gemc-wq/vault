# PH Staff Automation Map — Zero 2.0 + Agent Takeover
*Created: 2026-03-20 | Source: PH_STAFF_ROSTER, PATRICK_IT_TEAM_PROFILE, Zero docs, MEMORY.md*

---

## The Big Picture

38 PH staff × ₱1.27M/mo (~$22K USD/mo, ~$264K/yr).
Goal: Identify what AI agents + automation (Veeqo, Zero 2.0) can replace, and what stays human.

---

## DEPARTMENT: IT (5 staff, ₱117K/mo)

### Automation: Zero 2.0 + Veeqo replaces 80%+

| Staff | Role | What They Do Today | Replacement | Timeline | Status |
|-------|------|-------------------|-------------|----------|--------|
| **Patrick Gaña** (₱25K) | Operations engine | Runs Zero scripts, generates labels, picking lists, PO filtering, carrier APIs, scan forms. **Sole Zero knowledge holder.** | Zero 2.0 Order Agent + Fulfillment Agent + Veeqo | After parallel run (4-6 wk) | 🔴 CRITICAL PATH — must document everything first |
| Mechelle Ann Gaña (₱21K) | International labels | DHL Warenpost (DE), Deutsche Post, Royal Mail labels | Veeqo | Immediate once Veeqo handles intl carriers | 🟡 Harry working on this |
| Jeric Tyron Padilla (₱20K) | FBA + Zero data entry | FBA shipment prep, PO uploads, daily SO reports, RM labels | Veeqo + Zero 2.0 + BQ dashboards | 4-8 weeks | 🟡 Partially replaceable now |
| Dickel Pineda (₱33K) | Infrastructure lead | NAS, network, servers, hardware, printing infra | Chad (reassigned/new hire) | When image pipeline goes cloud | 🟢 Low urgency |
| Albert Bulaon (₱18K) | Network support | Junior support under Dickel | Eliminated with Dickel's role | Same as Dickel | 🟢 Low urgency |

**IT Savings:** ₱117K → ~₱25-33K (Chad only) = **~₱84-92K/mo saved (~$1,500/mo)**

---

## DEPARTMENT: PRODUCTION (10 staff, ₱271K/mo)

### Automation: Image pipeline (Ecell Studio) + Zero 2.0 Production Agent

| Staff | Role | What They Do Today | Replacement | Timeline | Status |
|-------|------|-------------------|-------------|----------|--------|
| **Jae Vitug** (₱80K) | Pre & Post Print Mgr | Manages print workflow end-to-end | Stays — production management still needs human oversight | N/A | ✅ Keep |
| Christopher Yunun (₱35K) | Warehouse Manager | Physical warehouse ops, stock checks, write-offs | Stays — physical warehouse needs a human | N/A | ✅ Keep |
| Amado Chan Jr. (₱20.3K) | Print Team Lead | Printing operations | Stays — physical printing | N/A | ✅ Keep |
| Archie Ocampo (₱20K) | Image Gen | Product image generation (IREN system) | Ecell Studio (AI mockup pipeline) | When Sven/image pipeline ready | 🟡 6-12 months |
| **Kamille Belena** (₱19.3K) | Image + Pick List | Image processing + picking list generation | Zero 2.0 Production Agent (picking) + Ecell Studio (images) | 4-8 weeks (picking), 6-12 mo (images) | 🟡 Partial |
| Patrick Lopez (₱14.8K) | Printing Operator | Physical printing | Stays — machine operator | N/A | ✅ Keep |
| Kimberly Ann Pertacorta (₱15K) | Image Processor | Image processing | Ecell Studio | 6-12 months | 🟡 |
| Nathaniel Pertacorta (₱25K) | Image Processor | Image processing | Ecell Studio | 6-12 months | 🟡 |
| Maricon Masangkay (₱23K) | QRP Team Leader | Quality/Receiving/Packing lead | Stays — physical QC | N/A | ✅ Keep |
| Cristina Santos (₱18.3K) | QRP | Quality/Receiving/Packing | Stays — physical QC | N/A | ✅ Keep |

**Production analysis:**
- Physical roles (printing, warehouse, QC): **5 stay** — machines need humans
- Image processing roles: **4 replaceable** by Ecell Studio AI pipeline (Archie, Kamille partially, Kimberly, Nathaniel)
- Picking list generation: **1 replaceable** by Zero 2.0 Production Agent (Kamille partially)
- **Production Savings:** ₱79.3K/mo potential (~$1,400/mo) once image pipeline operational

---

## DEPARTMENT: LISTINGS (8 staff, ₱210K/mo)

### Automation: Listing Automation Engine + Echo (copywriter) + Bolt (SEO)

| Staff | Role | What They Do Today | Replacement | Timeline | Status |
|-------|------|-------------------|-------------|----------|--------|
| **Jay Mark Catacutan** (₱50K) | Listing Lead | Content writing, listing management, team lead | Echo (Sonnet 4.6) + Listing Engine | Gradual — keep as QA reviewer | 🟡 Transition to review role |
| Patricia Shane Celeste (₱25K) | Graphics + Content | Design + content hybrid | Echo + Iris/Ecell Studio | 6-12 months | 🟡 |
| Jessie Morales (₱42.5K) | Design Replicator Lead | Replicating designs across devices/products | Listing Engine (SKU = Content model) | 3-6 months | 🟡 High impact |
| Chadle Rei Miclat (₱18K) | Design Replicator Lead | Same as Jessie | Same as Jessie | 3-6 months | 🟡 |
| Danica Matias (₱20K) | Jr. Graphic Designer | Design work | Ecell Studio | 6-12 months | 🟡 |
| Evita Margaux Carlos (₱18K) | Jr. Software Engineer | Unknown scope — likely internal tools | Potentially keep or retrain | TBD | ❓ Need to assess |
| Jay V. Callanta (₱16.1K) | Jr. Graphic Designer | Design work | Ecell Studio | 6-12 months | 🟡 |
| Mariela Razon (₱20K) | Listing Admin | Administrative listing tasks | Listing Engine | 3-6 months | 🟡 |

**Listings analysis:**
- **The SKU = Content model eliminates most manual listing work.** Design replication (Jessie, Chadle) is exactly what the Listing Engine automates.
- Jay Mark transitions from writer to QA/reviewer — verifying AI-generated copy. Still valuable.
- **Listings Savings:** ₱159.6K/mo potential (~$2,800/mo) — biggest automation target

---

## DEPARTMENT: CREATIVE (6 staff, ₱228K/mo)

### Automation: Ecell Studio + Iris (designer) + Sven (creative director)

| Staff | Role | What They Do Today | Replacement | Timeline | Status |
|-------|------|-------------------|-------------|----------|--------|
| **Bea Pineda** (₱101K) | Creative Manager | Oversees creative + graphics teams | Stays — creative direction needs human taste | N/A | ✅ Keep (reduced scope) |
| Jeffrey Mangilit (₱40K) | Sr. Graphic Designer | Senior design work | Ecell Studio + Iris | 6-12 months | 🟡 |
| Nina Joy Ganaban (₱31K) | Designer + Photographer | Design + product photography | Photography stays, design partial AI | Partial | 🟡 Keep for photography |
| Ricardo Dizon (₱21K) | Graphic Designer | Design work | Ecell Studio | 6-12 months | 🟡 |
| Nesley Joy Lansangan (₱20K) | Graphic Designer | Design work | Ecell Studio | 6-12 months | 🟡 |
| Tony Alapag (₱15K) | Jr. Graphic Designer | Junior design | Ecell Studio | 6-12 months | 🟡 |

**Creative analysis:**
- Bea stays but with smaller team — creative direction, brand standards, photography oversight
- 4-5 designers replaceable once Ecell Studio (AI image gen) is production-ready
- Photography (Nina Joy) stays — physical product shots can't be fully AI'd yet
- **Creative Savings:** ₱96K/mo potential (~$1,700/mo)

---

## DEPARTMENT: CUSTOMER SERVICE (5 staff, ₱303K/mo)

### Automation: N8N email triage + AI chatbot + CS architecture

| Staff | Role | Replacement | Timeline | Status |
|-------|------|-------------|----------|--------|
| **Analiza Peralta** (₱140K) | CS Manager | Stays — high-value escalations, licensor relationships | N/A | ✅ Keep |
| **Cris Guintu** (₱83.9K) | CS Asst. Manager | Stays — reduced scope with AI handling Tier 1 | N/A | ✅ Keep (review) |
| Jhamiela Alcantara (₱23.7K) | Team Leader | AI chatbot handles 60-70% of Tier 1 → reduces need | 6-12 months | 🟡 |
| Janine Alemana (₱18K) | CS Rep | AI chatbot + auto-responses | 6-12 months | 🟡 |
| Elliot Erwin Raquidan (₱37.7K) | Sr. QA Analyst | Stays — QA is critical for marketplace compliance | N/A | ✅ Keep |

**CS analysis:**
- CS is expensive (₱303K = highest dept) but high-touch. Marketplace compliance rules (Amazon TOS, eBay policies) require human judgment.
- AI chatbot can handle 60-70% of routine queries (where's my order, return policy, product questions)
- Reduce from 5 → 3 staff. Analiza + Cris + Elliot (QA) stay.
- **CS Savings:** ₱41.7K/mo (~$730/mo)

---

## DEPARTMENT: HR (2 staff, ₱45K/mo)

| Staff | Role | Status |
|-------|------|--------|
| Kyla Marie Egaran (₱23K) | HR Recruitment | As headcount shrinks, HR needs shrink. 1 person sufficient. |
| Angeline Rivera (₱22K) | HR Recruitment | Redundant if headcount drops 40%+ |

**HR Savings:** ₱22K/mo (~$385/mo)

---

## DEPARTMENT: FINANCE (2 staff, ₱95K/mo)

| Staff | Role | Status |
|-------|------|--------|
| Karen Keith Alfonso (₱55K) | Finance PH | ✅ Keep — PH-specific finance/compliance |
| Leevis Manalansan (₱40K) | Finance UK/US/DE/JP | ✅ Keep — multi-region finance. Xero integration may reduce workload but not eliminate. |

**Finance Savings:** None short-term. Xero automation reduces workload but both roles still needed.

---

## SUMMARY: Automation Impact

| Department | Current HC | Post-Automation HC | Savings (₱/mo) | Savings ($/mo) | Timeline |
|------------|-----------|-------------------|-----------------|----------------|----------|
| IT | 5 | 1 (Chad) | 84-92K | ~$1,500 | 4-8 weeks |
| Production | 10 | 6 | ~79K | ~$1,400 | 6-12 months |
| Listings | 8 | 2 | ~160K | ~$2,800 | 3-6 months |
| Creative | 6 | 2 | ~96K | ~$1,700 | 6-12 months |
| Customer Service | 5 | 3 | ~42K | ~$730 | 6-12 months |
| HR | 2 | 1 | ~22K | ~$385 | 3-6 months |
| Finance | 2 | 2 | 0 | $0 | N/A |
| **TOTAL** | **38** | **~17** | **~₱483K/mo** | **~$8,500/mo** | **6-12 months full** |

### Annual savings: ~$102K/yr
### Current PH payroll: ~$264K/yr
### Post-automation PH payroll: ~$162K/yr
### Reduction: **~55% headcount, ~39% cost** (managers are more expensive, so cost % lags headcount %)

---

## PHASING — What Goes When

### Phase 1: NOW → 8 weeks (Zero 2.0 v1 + Veeqo)
**Enables:** IT department automation
- Veeqo handles all label generation (Harry building this now)
- Zero 2.0 Order Ingest replaces Patrick's manual script runs
- **Staff impact:** Mechelle, Jeric become redundant. Patrick transitions to documenter/trainer then exits.
- **Savings:** ~₱66K/mo (~$1,150/mo)

### Phase 2: 3-6 months (Listing Engine + SKU=Content)
**Enables:** Listings department automation
- Listing Engine auto-generates listings from SKU templates
- Echo writes copy, Bolt does SEO
- Design replication becomes fully automated
- **Staff impact:** Jessie, Chadle, Mariela, Jay V, Danica become redundant. Jay Mark → QA reviewer.
- **Savings:** ~₱159K/mo (~$2,800/mo)

### Phase 3: 6-12 months (Ecell Studio + AI CS)
**Enables:** Creative + Production image roles + CS Tier 1
- Ecell Studio replaces manual image processing
- AI chatbot handles routine CS
- **Staff impact:** 4 image processors + 2 designers + 2 CS reps
- **Savings:** ~₱258K/mo (~$4,550/mo)

---

## CRITICAL DEPENDENCIES

| Dependency | Blocks | Owner | Status |
|------------|--------|-------|--------|
| Patrick knowledge transfer | Zero 2.0 (all phases) | Patrick + builder | 🔴 Not started |
| Veeqo intl carrier setup | IT Phase 1 | Harry | 🟡 In progress |
| Ecell Studio MVP | Creative + Production Phase 3 | Sven + TBD | 🔴 Not started |
| Listing Engine v1 | Listings Phase 2 | Ava + Forge/Spark | 🟡 SKU=Content model designed |
| AI CS chatbot | CS Phase 3 | TBD | 🔴 Not started |
| Jay Mark codebase push | Zero PHP extraction | Jay Mark (has Claude Code) | 🟡 Discussed, not executed |

---

## OPEN QUESTIONS FOR CEM

1. **Who is Chad?** Referenced as Dickel's replacement but not in PH roster. New hire? Reassignment? Contractor?
2. **Evita Margaux Carlos** — "Jr. Software Engineer" in Listings. What does she actually build? Could she help with Zero 2.0?
3. **Patrick knowledge transfer timeline** — When does Patrick start documenting? This blocks everything.
4. **Severance/transition plan** — What's the legal/cultural approach for PH staff reductions?
5. **Phase 1 builder** — Who builds Zero 2.0? Harry? External? Codex agent? Need to decide before starting.
6. **Bea's reduced role** — Does she stay full-time at ₱101K or shift to part-time/contractor?

## Related
- [[wiki/12-org/PH_STAFF_ROSTER|Full PH Staff Roster]]
- [[wiki/23-drew-handover/PATRICK_IT_TEAM_PROFILE|Patrick IT Team Profile]]
- [[wiki/30-zero-2/ZERO_2_BUILD_PLAN|Zero 2.0 Build Plan]]
- [[wiki/30-zero-2/ZERO_SYSTEM_SUMMARY|Zero System Summary]]
