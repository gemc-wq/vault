# Chad Miclat — Role Transition Plan
**Prepared by:** Ava (Strategy) | **Date:** 2026-03-31 | **For:** Cem Celikkol, Bettina Pineda

---

## Context

Chad was originally employed as a web developer. Over time, he inherited maintenance of several internal tools (Dreco1, IREN image pipeline, Dekr2 database, Poli Agora lister) from his predecessor Bobby, and took on additional responsibilities across GoHeadCase frontend, BigCommerce listings, eBay operations, and production tooling (LazCut).

This transition plan is driven by a strategic platform migration, not performance concerns. The business is moving from BigCommerce to Shopify, from legacy PHP/C#/.NET tools to cloud-based Python pipelines, and from manual listing operations to AI-assisted automation. These changes reduce the scope of Chad's current role significantly.

---

## Business Case

### Platform Revenue Reality (2026 YTD — Jan 1 to Mar 31)

| Platform | Orders | Revenue (USD) | Chad's Time Allocation |
|---|---|---|---|
| Amazon | 907 | $20,754 | 0% — runs through Zero |
| BigCommerce / GoHeadCase | 9 | $246 | ~40% (Poli, Dekr2, BC listings, GHC frontend) |
| Rakuten | 14 | $238 | ~10% (Poli Agora, format maintenance) |
| All other channels | 70 | $1,862 | ~5% |
| **Internal tools** | — | — | ~45% (Dreco1, LazCut, IREN, eBay banners) |

Chad's salary: ₱50,000/month (~$860 USD) — the same as Jay Mark Catacutan, who is building the replacement systems. BigCommerce + Rakuten combined revenue: $484 in 90 days (~$161/month). The platforms Chad primarily supports generate less than 20% of his monthly salary.

### Tools Being Replaced

| Tool | Built By | Chad's Role | Replacement | Timeline |
|---|---|---|---|---|
| Dreco1 (image replication) | Bobby (predecessor) | Maintenance, bug fixes | Iris AI agent (Python/Pillow) | In progress — 30-60 days |
| IREN (image renderer) | Bobby / legacy | Operational support | Iris AI agent (reverse-engineered Mar 29) | In progress |
| Dekr2 (product database) | Bobby / legacy | Feature additions | Jay Mark cfxb2b_db → Supabase sync | In progress |
| Poli Agora (BC/Rakuten lister) | Chad | Active development | Shopify + Codisto/Marketplace Connect | Active |
| GoHeadCase frontend | Chad + legacy | Ongoing revamp | Full Shopify rebuild (Forge/Spark agents) | Q2 2026 |
| LazCut (laser cut files) | Chad | Active development | **No replacement planned** | Ongoing need |
| ecellglobal.com | Chad (maintenance) | Layout fixes | Already rebuilt on Vercel | Complete |

---

## Recommendation: 30-Day Documentation Handover

### Week 1-2: Critical Documentation Sprint

Chad documents the following (deliverables required):

**1. Dreco1 Architecture Document** (current docs are 45 paragraphs of install instructions only)
- Full architecture: how the C# code interfaces with IREN's rendering engine
- Device template system: how new phone models are added
- Image output format specifications (angles, positions, file naming)
- Known bugs and workarounds
- Build and deployment pipeline (Visual Studio → publish → FileZilla → PH server)
- Dependencies: which DLLs, frameworks, and server configs are required

**2. LazCut Documentation**
- Architecture: how SVG cut layers are generated from print image files
- Device template system for laser cutting (how new devices are added)
- Calibration rules (the 2mm alignment fix for iPhone 16 Pro — what causes these issues)
- Who in production uses this and how

**3. Dekr2 Documentation**
- Database schema (which tables in cfxb2b_db it reads/writes)
- Bulk edit logic (the batch INSERT...ON DUPLICATE KEY UPDATE he optimised)
- API connections to BigCommerce

**4. Poli Agora Documentation**
- Upload pipeline: how it connects to BC, Rakuten, Amazon (via Feedonomics)
- Configuration for each marketplace
- Known limitations

### Week 3-4: Knowledge Transfer

- Walk Jay Mark through all documentation via video call (record for archive)
- Jay Mark validates he can perform basic Dreco1 maintenance
- Production team validates LazCut documentation is complete
- Chad resolves any open Dreco1/LazCut bugs before exit

### Deliverable Checklist

| # | Document | Format | Reviewer | Due |
|---|---|---|---|---|
| 1 | Dreco1 Architecture & Maintenance Guide | Markdown + video | Jay Mark | Week 2 |
| 2 | LazCut Architecture & Device Template Guide | Markdown + video | Production Manager (Jae) | Week 2 |
| 3 | Dekr2 Schema & Operations Guide | Markdown | Jay Mark | Week 1 |
| 4 | Poli Agora Pipeline Documentation | Markdown | Jay Mark | Week 1 |
| 5 | Knowledge Transfer Sessions (recorded) | Video | Jay Mark + Jae | Week 3-4 |

---

## Communication Approach for Bettina

### Key Messages:
1. **This is a platform migration decision, not a performance issue.** The business is moving from BigCommerce to Shopify, and from legacy C#/Java tools to cloud-based AI pipelines. Chad's tools are being replaced by this migration.
2. **Chad's contributions are acknowledged.** He maintained critical tools that kept operations running for years. The main image revision work (650+ lineups) was genuinely valuable.
3. **The documentation handover is essential.** Without it, tribal knowledge is lost. This is Chad's most important deliverable.
4. **LazCut is the one ongoing need.** If there's a case for retaining Chad in any capacity after the transition, it's LazCut maintenance — but this could be part-time or contracted.

### Suggested Response to Bettina:

> Hi Bea,
> 
> Thanks for the detailed summary of Chad's responsibilities. I appreciate his contributions, especially maintaining the internal tools that have kept our workflow running.
> 
> As you know, we're in the process of migrating from BigCommerce to Shopify and replacing several legacy tools with AI-powered systems. This means some of Chad's current responsibilities — particularly around Poli Agora, Dekr2, and GoHeadCase on BigCommerce — are being phased out as the new systems come online.
> 
> What I'd like to do is focus Chad's remaining time on thorough documentation of Dreco1, LazCut, Dekr2, and Poli Agora so that Jay Mark and the team can maintain these systems during the transition. This is the highest-value work Chad can do right now.
> 
> I'll send a specific documentation checklist for Chad to work through. Let's plan for a 30-day transition period.
> 
> Thanks,
> Cem

---

## Post-Transition Risk Mitigation

| Risk | Mitigation |
|---|---|
| Dreco1 breaks before Iris agent is ready | Jay Mark has documentation + recorded walkthrough. Emergency: contract Chad for hourly fix. |
| LazCut needs new device template | Document the process thoroughly. If recurring, contract Chad for specific deliverables. |
| Replication team blocked | Iris agent priority sprint to replicate Dreco1 output in Python. Target: functional by end of April. |
| Knowledge gaps discovered | All documentation delivered as markdown + video — searchable and rewatchable. |

---

## Financial Impact

- **Monthly savings:** ₱50,000 (~$860 USD)
- **Annual savings:** ₱600,000 (~$10,320 USD)
- **Transition cost:** ₱50,000 (one month documentation handover)
- **ROI:** Pays for itself in Month 2
- **Context:** Chad's salary equals Jay Mark's (₱50,000). Redirecting that budget to a second builder on the new stack (or saving it entirely) is a better use of funds than maintaining legacy tools on a platform generating $161/month.

---

*Prepared by Ava — based on analysis of Slack EODs (14 days), Google Drive projects, Supabase order data, MEMORY.md project history, and staff roster.*
