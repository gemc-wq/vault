# OPERATIONAL PLAYBOOK V2: Dual-Business AI Strategy
## LLM Council Synthesis — March 30, 2026 — REVISED
### Revenue-Urgent Edition

**Prepared for:** Cem Celikkol, CEO — Ecell Global Limited (UK) | US S-Corp AI Consultancy (Orlando, FL)
**Council Members:** GPT-5.4 · Claude Sonnet · Gemini Pro
**Status:** Final V2 — supersedes all V1 reports
**Urgency level:** SURVIVAL — EU sales declining, US consulting revenue required within 30 days

---

## TABLE OF CONTENTS

1. [What Changed from V1](#1-what-changed-from-v1)
2. [Council Consensus Summary](#2-council-consensus-summary)
3. [Ecell Autonomy Roadmap (Q1)](#3-ecell-autonomy-roadmap-q1)
4. [Agent Architecture SOP (Q2)](#4-agent-architecture-sop-q2)
5. [Email Triage System — Ava + N8N Hybrid (Q4)](#5-email-triage-system--ava--n8n-hybrid-q4)
6. [Wiki → Consulting IP Conversion (Q3)](#6-wiki--consulting-ip-conversion-q3)
7. [AI Consultancy Launch Playbook — US S-Corp (Q5)](#7-ai-consultancy-launch-playbook--us-s-corp-q5)
8. [Master SOP Library (Q8)](#8-master-sop-library-q8)
9. [Risk Register (Q6)](#9-risk-register-q6)
10. [90-Day Implementation Timeline (Q7)](#10-90-day-implementation-timeline-q7)
11. [Appendix: Action Items Master List](#11-appendix-action-items-master-list)

---

## BUSINESS CONTEXT

### Who Is Cem?
- CEO of Ecell Global Limited (UK, est. 2005) — manufacturing and online retail of licensed tech accessories
- Operates US S-Corp in Orlando, FL — US operations and growing US market
- Entities: UK (Ecell Global Ltd), US (S-Corp), Germany, Philippines, Japan
- **Revenue crisis: EU sales declining, US growing, needs new income streams immediately**
- Sells via goheadcase.com (Shopify), Amazon (US/UK/DE/FR/IT/ES), eBay, Walmart US
- Manages ~200K parent SKUs, 4–5M child ASINs
- Technical: Python, SQL, JavaScript, AWS, GCP, BigQuery, N8N, Xero, Freshdesk

### Current Agent Architecture (CORRECTED)

| System | Name | Hardware | Purpose | Key Integrations |
|--------|------|----------|---------|-----------------|
| OpenClaw | **Ava** | Mac Studio | Strategist, Content, Sales, Email Triage | Airweave (email), web browsing, research, content generation |
| OpenClaw | **Harry** | iMac | Finance, Inventory, Order Management | BigQuery, Walmart API, Xero, Shopify |
| N8N | — | Self-hosted | Deterministic automation, invoice processing | Gmail, Google Drive, Xero, webhooks |
| Claude Desktop + Cowork | — | Local | High-judgment productivity tasks | Direct interaction |
| Perplexity Computer | — | Cloud | Research, LLM Council, scoping | Web search, tools |
| Zero Fulfillment | — | AWS (Aurora RDS) | PO generation, inventory routing | MySQL 8.0, 476 tables, 439GB |
| Multi-Channel Feed Engine | — | AWS (RDS/SQS/Lambda) | Listing management (in development) | PostgreSQL, FastAPI, Next.js |

### Current Projects In Flight
1. **Multi-Channel Listing Feed Engine** — in development (scoping doc March 21, 2026)
2. **MIRROR-PRODUCT** — consumer AI app / Ecell spinoff (council recommended pause)
3. **Zero Fulfillment Modernization** — PHP → JSON/Cloud Run (council playbook March 28, 2026)
4. **Print-on-Demand Analytics Dashboard** — evolving to serverless (council recommended pause)
5. **OpenClaw Portfolio Intelligence Agent** — centralized project view
6. **Supabase RAG Memory** — shared semantic memory (planned, not started)

### Business Strategy (CORRECTED)
- **Ecell e-commerce (Ecell Global UK):** Maintain and optimize. EU declining, US growing. Reduce Cem's operational time to <10 hrs/week.
- **AI Consultancy (US S-Corp):** Launch ASAP under existing US S-Corp. Productize Ecell's AI workflows for US small businesses. **Primary new revenue stream. Revenue urgency = survival.**
- **Target:** First paying consulting client within 3–4 weeks, not 3 months.

---

## 1. WHAT CHANGED FROM V1

*Source: Scope Document V2 — llm-council-scope-v2.md*

The following corrections MUST be applied across all answers. V1 made assumptions that were wrong.

| # | V1 Assumption (Wrong) | V2 Correction (Authoritative) |
|---|----------------------|-------------------------------|
| 1 | The AI consultancy is a nice-to-have expansion | EU sales are declining. The consultancy launch is a **SURVIVAL play**. Every timeline must front-load revenue generation, not stabilisation. First client in **3–4 weeks** — not 3 months. |
| 2 | Generic OpenClaw instances | Two named agents: **Ava** (Mac Studio) — Strategist, Content, Sales, Email Triage via Airweave. **Harry** (iMac) — Finance, Inventory Control, Order Management via BigQuery/Walmart/Xero/Shopify. |
| 3 | Consultancy entity = Ecell Global UK | Entity = **existing US S-Corp in Orlando, FL**. No new entity needed. US clients, US invoicing, US market focus. Ecell Global UK handles existing e-commerce/manufacturing. Two entities stay separate. |
| 4 | Primary market = EU businesses | **Primary:** US small businesses (Orlando/FL first, then US-wide remote). **Secondary:** UK SMBs. **NOT primary:** EU businesses. EU is slowing — do not invest marketing spend there. |
| 5 | Build N8N email triage from scratch | Ava already has email access via Airweave. Correct architecture: N8N as reliable intake/safety-net → Ava as intelligent judgment layer for anything needing context. N8N handles receipts/tracking/spam deterministically. |

### The Hybrid Email Architecture (from Correction 5)

```
Email arrives
  → N8N catches it (100% reliable, never misses, near-zero cost)
  → N8N labels category + urgency (deterministic, fast)
  → Simple stuff: N8N auto-routes (receipts → Xero, tracking → archive, spam → delete)
  → Anything needing judgment: N8N passes to Ava via Airweave/webhook
  → Ava reads with full business context (SOUL.md, project knowledge, contact history)
  → Ava drafts response, decides action, or flags for Cem
  → High-risk items: Ava escalates to Cem instead of acting
```

---

## 2. COUNCIL CONSENSUS SUMMARY

*Source: Cross-council synthesis across GPT-5.4, Claude Sonnet, Gemini Pro*

### 3/3 Unanimous Agreements (All council members agreed)

1. **Revenue urgency is real and changes everything.** The 90-day plan must front-load revenue generation. First paying consulting client is a Week 3–4 target, not a Month 3 target. No council member disagrees.
2. **Ava is the intelligent communications layer from Day 1.** Her existing Airweave email access means no new email AI brain needs to be built. Exploit what already exists.
3. **Harry's domain is finance/inventory/orders only.** Harry must not drift into communications, sales, or ambiguous cross-functional work.
4. **N8N stays as the deterministic safety net underneath Ava.** N8N's value is reliability and simplicity — it never drops an email even when Ava is down.
5. **Supabase pgvector + RLS is the right shared memory substrate** — not free-form local state. Permissions must be explicit, Ecell and consultancy data must stay logically separated.
6. **Paperclip is a Week 4+ governance layer, not a Week 1 tool.** Adding governance overhead before time is freed would add hours in Week 1, which is unacceptable.
7. **The US SMB market has genuine demand in 2026.** 76% of small businesses use AI, only 14% have it embedded in core operations. The implementation gap is real and Cem's lived proof is the competitive moat.
8. **Cem's pricing must be in USD.** All consulting pricing from V1 in GBP is void.
9. **Two separate Paperclip companies** — `Ecell Ops` and `US Consultancy` — to prevent client data visibility contamination.
10. **MIRROR-PRODUCT and POD Analytics Dashboard must be paused immediately** to free Cem's cognitive bandwidth for the survival plays.

### 2/3 Divergences — With Council Verdicts

#### Divergence 1: How quickly should Ava be given autonomous send authority?

- **GPT-5.4:** Ava should draft first, with Cem approving all sends in Week 1–2. Expand autonomy category-by-category based on success rate data.
- **Claude Sonnet:** Same — first 30 days all drafts reviewed; then autonomous send only for pre-approved low-risk templates.
- **Gemini Pro:** Ava should draft responses for high-stakes emails and require Cem's one-click approval via Claude Desktop *before sending*, with no unilateral send authority for new client proposals or supplier negotiations.

**Verdict (2/3 + Gemini agrees on core restriction):** Ava drafts, Cem approves for all client-facing and high-stakes mail during the first 30 days. After 30 days, autonomous send only for pre-approved template types (acknowledgments, meeting confirmations, standard follow-ups). All council members agree: Ava must never have unilateral send authority for new client proposals, pricing negotiations, or major supplier decisions.

#### Divergence 2: When to deploy Supabase RAG memory

- **GPT-5.4:** Week 2 — add Supabase-backed approved memory for contacts, SOPs, and escalation rules as soon as N8N triage is stable.
- **Claude Sonnet:** Week 2 — concurrent with E6/E1 Ecell SOPs going live.
- **Gemini Pro:** Week 6 — focus Month 1 entirely on revenue sprint and basic agent operations; add RAG in Month 2.

**Verdict (2/3 majority — GPT-5.4 and Claude):** Deploy Supabase RAG in Week 2, but start with a minimal approved set — SOPs, contact briefs, escalation rules only. No free-form memory dump. This gives Ava grounded context without the overhead of a full RAG build. Gemini's Week 6 position is too slow given the revenue dependency on Ava performing well.

### Top 10 Unified Recommendations

1. N8N catch-all email intake live by Day 3, with deterministic rules removing receipts/tracking/spam.
2. Ava activated as sole intelligent comms reviewer and draft engine from Day 1.
3. Harry locked to finance/inventory/orders lane with hard approval thresholds from Day 1.
4. Pause MIRROR-PRODUCT and POD Dashboard immediately — no new development projects until first consulting client is signed.
5. Cem blocks minimum 15 hrs/week for consulting outreach and sales from Week 1 — before any additional automation work.
6. Consultancy P0 SOPs (C0-A through C0-E) built by Ava in Days 1–7.
7. First 4 US-framed case studies drafted by Ava from Ecell projects in Days 3–7.
8. Website live with USD pricing and Calendly booking by Day 10.
9. E&O professional liability insurance bound Day 1 (non-negotiable before first client call).
10. Supabase RAG deployed Week 2 with approved-only memory: SOPs, contacts, escalation rules, policy memory.

---

## 3. ECELL AUTONOMY ROADMAP (Q1)

*Source: Council Member 1 — GPT-5.4*

### Target Operating Principle

Ecell should be run as an **exception business**, not a founder-routed business. Ava owns judgment-heavy front-door work (nuanced email triage, contact-aware reply drafting, consulting/sales communications). Harry owns structured back-office work (finance review prep, inventory monitoring, order-management execution).

The immediate objective is not perfection. It is to get Cem to **one daily review block plus one short weekly ops review as fast as possible**, so the rest of his working time can be redeployed into selling consulting in Orlando and the broader US market.

### What Cem Should STOP Doing Immediately

1. **Stop treating his inbox as a manual command center.** N8N already supports reliable Gmail intake, classification, labels, and draft branching. Ava already has Airweave email context for higher-judgment decisions. There is no reason for Cem's eyes to touch most emails.
2. **Stop being the dispatcher between email, inventory, finance, and customer issues.** Paperclip and N8N are both built around explicit routing, ownership, and escalation rather than founder-side message passing.
3. **Stop using Ava or Harry as roaming generalists.** Current OpenClaw releases push toward bounded tool visibility, MCP-defined integrations, and explicit heartbeat control for safer production use.
4. **Stop spending founder time on receipts, tracking emails, standard supplier acknowledgments, and routine order-status signals.** These are exactly the sort of deterministic items N8N can classify and route without judgment.
5. **Stop delaying consulting outreach until Ecell is "fully automated."** The 2026 SMB market is already buying practical AI help. The implementation gap is now — not after a 90-day stabilisation program.

### What Cem Should START Doing Immediately

1. **Route every inbound business email through one N8N intake workflow** — no exceptions. Reliable catch-first routing is the cheapest way to stop inbox polling.
2. **Treat Ava as the judgment layer for communications, sales, and nuanced reply drafting.** Airweave is designed to give agents grounded access to synced mailbox context, including message metadata and attachments.
3. **Treat Harry as a structured executor for finance, inventory, and order actions only**, with hard approval thresholds for money movement, bulk listing impact, and large inventory commitments.
4. **Use Hermes only as the learning and condensation layer** — session search, memory protection, API reliability, SOP condensation. Not as a line-execution agent.
5. **Allocate protected weekly founder hours to consulting pipeline generation from Week 1.** This is now a survival move.

### Week 1 Changes That Free Time Immediately

These are the changes that matter most in the first seven days:

- Route all business mail into N8N intake with labels: `finance`, `inventory/orders`, `customer`, `supplier`, `sales/consulting`, `project`, `junk/auto`. Deterministic categorisation is the fastest path to inbox control.
- Let N8N auto-handle receipts, tracking notices, newsletters, and machine-generated updates **without Ava**. These items do not need contextual judgment.
- Send all "needs judgment" threads to Ava with a compact packet: `sender`, `thread_summary`, `urgency`, `confidence`, `prior_contact_history`, `proposed_next_action`.
- Push finance, inventory, and order actions from Ava to Harry **only after judgment is made**, so Harry is not spending cycles reading ambiguous communications.
- Force Cem out of ad hoc inbox checking by replacing it with **two fixed review windows per day** in Week 1, then one by end of Week 2.
- Reserve at least **15 founder hours in Week 1** for US consulting outreach, offer packaging, and meetings. This is the single most important business correction in V2.

### Revised Phase Plan

#### Phase 0: Emergency Founder-Time Recovery (Days 1–7)

| Priority | Change | Named Owner | Why Now | Effort | Expected Weekly Hour Impact |
|----------|--------|-------------|---------|-------:|----------------------------:|
| 1 | N8N catches all inbound business email; applies deterministic labels | N8N | Stops inbox polling immediately using proven Gmail intake patterns | 4–6 hrs | 5–7 hrs saved |
| 2 | Ava becomes the only intelligent comms reviewer | Ava | Uses existing Airweave mailbox context instead of building a new AI mail brain | 3–5 hrs | 3–5 hrs saved |
| 3 | Harry gets a hard queue for finance/inventory/orders only | Harry | Prevents domain drift and protects operational execution | 2–4 hrs | 2–3 hrs saved |
| 4 | Cem adopts fixed approval windows; stops ad hoc checking | Cem | Converts business from interrupt-driven to queue-driven | <1 hr | 3–5 hrs saved |
| 5 | Consulting outreach calendar blocked before more automation work | Cem + Ava | Revenue is survival-critical; first client target is Week 3–4 | 2–3 hrs | Protects 15+ hrs for selling |

**Phase 0 total expected weekly hours recovered: 13–20 hrs**

#### Phase 1: Exception Operations (Weeks 2–4)

| Priority | Change | Named Owner | Why Now | Effort | Expected Result by Day 30 |
|----------|--------|-------------|---------|-------:|--------------------------|
| 6 | Daily digest for approvals, risks, and unresolved exceptions | N8N + Ava | Replaces founder polling with one review surface | 2–4 hrs | Cem inbox review drops below 30 min/day |
| 7 | Harry handles A-item inventory and finance exception prep only | Harry | Keeps automation in high-value, bounded workflows | 8–12 hrs | Reduced ops interruptions; fewer stock/finance surprises |
| 8 | Hermes writes back patterns from resolved threads and actions | Hermes | Turns repeated work into reusable memory while protecting policy from free-form drift | 6–10 hrs | Better first-pass triage; less re-explaining |
| 9 | Supabase approved memory goes live for SOPs, contacts, resolution patterns | Hermes + Supabase | Gives shared retrieval with access control and semantic search | 8–14 hrs | Less context loss across Ava/Harry/Hermes |
| 10 | Cem spends protected blocks on closing first consulting client | Cem + Ava | Revenue must show up before full stabilisation | ongoing | First paid engagement target Week 3–4 |

#### Phase 2: Governance and Scale Without Founder Re-Capture (Weeks 5–12)

| Priority | Change | Named Owner | Why Later | Effort | Intended Outcome |
|----------|--------|-------------|-----------|-------:|------------------|
| 11 | Paperclip added in shadow mode as governance layer | Paperclip | Good for budgets, approvals, audit, and org charts — but not needed before time recovery | 6–10 hrs | Cost and delegation control without slowing Week 1 |
| 12 | Consulting company gets separate governance tree from Ecell | Paperclip | Separation is important given Paperclip's full in-company visibility model | 3–5 hrs | Cleaner confidentiality and spend isolation |
| 13 | Deeper automation added only where Ava success rate or Harry queue data proves value | Cem + Hermes | Measure first, automate second | variable | Expansion without hidden ops risk |

### Tool-by-Tool Role Map

| Tool / Agent | Primary Domain | Hard Boundary |
|-------------|---------------|--------------|
| **Ava** | Email triage, contact-aware drafting, sales follow-up, consulting IP, strategy | Does NOT own financial posting, inventory changes, order execution, or uncontrolled autonomous send on high-risk threads |
| **Harry** | Xero prep, reconciliations, BigQuery anomaly checks, Walmart/Shopify operational follow-through, inventory exceptions | Does NOT own first-pass inbox judgment, sales nuance, or ambiguous cross-functional work |
| **N8N** | Catch-all email intake, deterministic labelling, receipt/tracking/spam routing, digest assembly | Does NOT do contextual judgment, draft nuanced replies, or act on anything requiring business context |
| **Hermes** | Resolution pattern extraction, SOP condensation, retrieval tuning, memory write-back proposals | Does NOT make autonomous policy changes or execute high-risk actions |
| **Paperclip** | Company structure, budgets, approval routing, activity logs, heartbeat governance | Does NOT run in Week 1; is NOT the first-line operational brain |
| **Supabase** | Approved shared memory: SOPs, contact briefs, escalation rules, policy memory, execution logs | Is NOT a free-form memory dump; all writes are human-approved or Hermes-proposed + human-approved |

### Revised 30-Day To-Do List

#### Days 1–3

1. Route all business email through N8N first — no exceptions. Reliability matters more than sophistication at intake.
2. Create deterministic N8N rules for receipts, tracking, newsletters, spam, and machine notifications so those never touch Cem unless a rule fails.
3. Create the Ava triage packet schema: `thread_id`, `sender`, `summary`, `urgency`, `confidence`, `history`, `proposed_action`, `escalation_flag`.
4. Enforce Harry's queue boundary: finance, inventory, orders, reconciliations, and operational follow-through only.
5. Block Cem's calendar for consulting work **before** building anything else.

#### Days 4–7

6. Start daily founder digest with only: approvals, financial anomalies, customer-risk items, supplier/inventory risk, and consulting opportunities.
7. Set hard escalation rules: money movement, legal/compliance language, marketplace account risk, chargebacks, public reputation risk, unusual vendors, and bulk operational changes all go to Cem.
8. Have Ava draft the first consulting offer, outbound email variants, and local/US outreach list using Cem's real operating experience as the case study base.
9. Prepare one-page "what we did inside Ecell" proof sheet for prospects — focused on inbox triage, order/inventory operations, and founder time recovery.

#### Week 2

10. Launch Supabase memory with only approved SOPs, approved contacts, and approved resolution patterns — not raw free-form memory. Supabase RAG with RLS is strongest when permissions and document structure are explicit.
11. Have Hermes summarize resolved cases into reusable patterns and propose memory inserts — but keep human approval for policy-class memory.
12. Put Harry on top 20% revenue-driving SKUs/orders/issues only.
13. Begin founder outreach meetings and local Orlando network activity.

#### Week 3

14. Measure Ava autonomous triage success rate and Harry execution rework rate.
15. Tighten or expand N8N rules based on where Ava is overused or underperforming.
16. Push for first paid consulting pilot in Orlando/Florida/US SMB market — email/process automation as the entry offer.

#### Week 4

17. If intake reliability is stable, add Paperclip in shadow mode for budget logging, audit, and escalation visibility.
18. Split Ecell governance and consultancy governance into separate Paperclip companies before client work deepens.

### Net Result Target by Day 30

The realistic Day-30 goal is not full autonomy. The realistic goal is **Ecell operating at roughly 8–12 founder hours per week**, with Cem's best hours shifted into selling and delivery for the US consultancy. That level is achievable if N8N removes the inbox burden, Ava absorbs most judgment-heavy communications, Harry takes bounded operational execution, and Cem limits himself to scheduled approvals and high-risk exceptions.

---

## 4. AGENT ARCHITECTURE SOP (Q2)

*Source: Council Member 1 — GPT-5.4*

### Core Flow

```
Email / event arrives
  → N8N intake
  → deterministic route (receipts/tracking/spam) OR Ava review
  → Harry execution if operational action needed
  → Hermes memory writeback
  → Cem only for high-risk approvals
```

### Named Agent Roles

#### Ava — Strategist / Content / Sales / Email Triage

**Hardware:** Mac Studio
**Integrations:** Airweave (Outlook Mail connector), web browsing, research, content generation

**Owns:**
- Nuanced inbox triage
- Contact-aware drafting
- Sales follow-up drafts
- Consulting offer packaging
- Business-context judgment
- "What should we do next?" recommendations
- Consultancy lead research and outbound prospecting
- Client communications via Airweave

**Does NOT own:**
- Financial posting
- Inventory changes
- Order execution
- Uncontrolled autonomous sending on high-risk threads

**Key capability:** Airweave continuously syncs and exposes connected source data through unified retrieval. The Outlook Mail connector exposes message metadata and attachments Ava needs for grounded triage.

---

#### Harry — Finance / Inventory / Orders

**Hardware:** iMac
**Integrations:** BigQuery, Walmart API, Xero, Shopify, Zero Fulfillment

**Owns:**
- Xero review prep and reconciliations support
- BigQuery-driven anomaly checks
- Walmart/Shopify operational follow-through
- Low-stock investigations
- Order exceptions
- Post-judgment operational execution
- Daily margin monitoring of EU ASINs
- Inventory alert generation

**Does NOT own:**
- First-pass inbox judgment
- Sales nuance
- Relationship-sensitive drafting
- Ambiguous cross-functional work

---

#### Hermes — Learning / Condensation / Shared Memory Proposals

**Owns:**
- Resolution pattern extraction
- Session search
- SOP condensation
- Retrieval tuning
- Suggested updates to approved memory

**Does NOT own:**
- Autonomous policy changes
- Direct high-risk execution

**Notes:** Hermes' release train emphasizes session search improvements, stale-memory overwrite protections, API/server reliability, MCP capability, and OpenClaw migration/interoperability. Use Hermes as a parallel staff function — not a line manager.

---

#### Paperclip — Governance and Cost Control

**Owns:**
- Company structure and org charts
- Budgets and hard-stop controls
- Approval routing
- Activity logs
- Heartbeat-level governance

**Does NOT own:**
- Being the first thing Cem works on in Week 1
- First-line operational intelligence

**Notes:** Paperclip enforces a strict tree: every company has a single root, single-manager reporting, no matrix structure, full visibility within the company, and no automatic reassignment on termination. This makes separation between Ecell and Consultancy companies mandatory.

---

#### N8N — Deterministic Intake and Routing

**Owns:**
- 100% inbound email catch
- Auto-labelling
- Spam/newsletter/receipt/tracking handling
- Branching and logging
- Digest assembly
- Fallback routing when Ava is down

**Does NOT own:**
- Contextual judgment
- Nuanced reply drafting

---

### Handoff SOP

#### SOP-1: Intake

1. Every inbound email, alert, or support thread first enters N8N.
2. N8N normalises fields into a common object:

| Field | Description |
|-------|-------------|
| `source` | Origin mailbox / channel |
| `thread_id` | Unique thread identifier |
| `from` | Sender email + name |
| `subject` | Subject line |
| `summary` | Auto-generated summary |
| `attachments` | Attachment list |
| `classification` | Category label |
| `confidence` | Classification confidence score |
| `urgency` | low / normal / high / critical |
| `suggested_owner` | N8N / Ava / Harry / Cem |
| `risk_flags` | finance / legal / reputation / sales / supplier |

3. N8N checks deterministic rules first.

---

#### SOP-2: What N8N Handles Alone

N8N fully handles these without Ava:

- Receipts and invoices → finance intake path
- Shipping and tracking notices → archive
- Newsletters and spam → delete/spam folder
- Machine alerts already mapped to known routes
- Simple routing of support mail into Freshdesk or archive queues

The safe use of N8N is to automate only what is clearly low-risk. Current N8N Gmail AI patterns are built around "reply, draft, or nothing" decisions.

---

#### SOP-3: N8N → Ava Handoff

N8N passes to Ava when any of the following are true:

- The thread needs contextual judgment
- The sender relationship matters
- The next action is not obvious from rules
- The draft tone matters
- The thread touches sales, supplier negotiation, founder communications, or consulting pipeline
- Classifier confidence is below threshold
- Attachments or past context likely matter

**Handoff packet sent to Ava:**

```json
{
  "thread_id": "...",
  "source_mailbox": "...",
  "sender": "...",
  "subject": "...",
  "summary": "...",
  "classification": "...",
  "confidence": 0.0,
  "urgency": "low|normal|high|critical",
  "risk_flags": ["finance", "legal", "reputation", "sales", "supplier"],
  "recent_history": "...",
  "relevant_contacts": "...",
  "attachments": [{"name": "...", "type": "..."}],
  "suggested_next_step": "..."
}
```

---

#### SOP-4: Ava → Harry Handoff

Ava hands off to Harry **only after** she has reduced ambiguity to an operational instruction, such as:
- "prepare Xero categorisation recommendation for vendor Y"
- "check inventory risk for SKU cluster Z"
- "verify Walmart order exception and propose remedy"
- "compile finance anomalies for review"

Harry should not be processing ambiguous messages. Every handoff to Harry is a structured task, not a forwarded email.

---

#### SOP-5: Harry → Hermes Writeback

After Harry completes a task, Hermes captures:

- Issue type
- Inputs used
- Steps taken
- Outcome
- Escalation reason (if any)
- Candidate reusable pattern

Hermes proposes memory inserts; human approval required for any policy-class memory.

---

#### SOP-6: Escalation to Cem

Escalate immediately when any of these are true:

- Money movement or non-routine financial commitment
- Legal/compliance/tax language
- Marketplace suspension or reputation risk
- Supplier dispute on revenue-critical items
- Customer issue with public review, fraud, or chargeback exposure
- Large inventory purchase or stock allocation change
- Agent confidence below threshold after second pass
- Same thread bounces twice
- Memory retrieval is contradictory or incomplete

---

### Supabase RAG Design

Use Supabase as **approved shared memory**, not as a dump of everything. Supabase RAG with RLS applies access controls directly to similarity search — the right pattern for shared multi-agent memory with access boundaries.

#### Recommended Schema

| Table | Purpose | Write Owner | Read Owner |
|-------|---------|-------------|------------|
| `documents` | Top-level memory record for SOP, contact dossier, pattern, or policy | Human / Hermes-proposed | All authorised agents |
| `document_sections` | Chunked content with embeddings using `extensions.vector(384)` | Ingestion job | All authorised agents |
| `memory_patterns` | Structured "if X, do Y" operational patterns | Hermes draft + human approve | Ava, Harry, Hermes |
| `contact_briefs` | Approved relationship summaries for suppliers, clients, prospects | Ava/Human | Ava primarily |
| `escalation_rules` | Hard thresholds and no-go rules | Human only | N8N, Ava, Harry |
| `execution_logs` | Raw action summaries — not policy | N8N/Harry/Hermes | Hermes, Cem |
| `policy_memory` | Immutable approved business rules | Human only | All agents |

#### Permission Model

Keep Ecell and consultancy in **separate logical document ownership groups** from the start. Supabase RLS around vector search ensures similarity retrieval inherits the same access controls as normal row access — critical once Cem starts storing client information alongside Ecell information.

---

### Paperclip Org Structure

Because Paperclip enforces a strict tree, the cleanest setup is **two separate companies**: `Ecell Ops` and `US Consultancy`.

#### Ecell Ops Company

- **CEO / Board:** Cem
- **Comms & Strategy Lead:** Ava
- **Operations Lead:** Harry
- **Knowledge Steward:** Hermes
- **Automation Backbone:** N8N (infrastructure, not a person-like manager)

**Reporting tree:**
```
Cem
 └─ Ava
     └─ Harry
 └─ Hermes (parallel staff function)
```

#### US Consultancy Company

- **CEO / Board:** Cem
- **Growth & Delivery Lead:** Ava
- **Knowledge / Asset Steward:** Hermes
- **Future Ops Executor:** Add only when client volume justifies it

**Critical:** Do NOT put client work inside the Ecell company. Paperclip V1 gives all company agents full visibility into company tasks, goals, budgets, and activity logs.

---

### Budget Allocation — Revised by Named Agent

Start with low, explicit budgets so agent cost cannot become a second crisis.

#### Ecell Ops Monthly Pilot Budget

| Agent / System | Budget/Mo | Rationale |
|---------------|----------:|-----------|
| Ava | $150 | Judgment-heavy email, drafting, sales support |
| Harry | $120 | Structured ops execution |
| Hermes | $80 | Memory, summarisation, pattern extraction |
| N8N-related model/API spend | $75 | Intake classification, digesting, edge cases |
| Supabase | $25–$75 | pgvector + storage + queries |
| Paperclip | $20–$50 | Governance shadow mode only |
| **Total** | **~$470–$550** | **Conservative survival-mode stack** |

#### US Consultancy Monthly Pilot Budget

| Agent / System | Budget/Mo | Rationale |
|---------------|----------:|-----------|
| Ava | $150 | Outreach, discovery prep, drafting, proposals |
| Hermes | $50 | Asset reuse and proposal memory |
| N8N/API/supporting tools | $25–$50 | Lead intake and lightweight automations |
| **Total** | **~$225–$250** | **Enough to sell before scaling** |

---

## 5. EMAIL TRIAGE SYSTEM — AVA + N8N HYBRID (Q4)

*Source: Council Member 1 — GPT-5.4*

### Full Hybrid Architecture

**Core model:**
```
Email arrives
  → N8N catches it (100% reliable, always on)
  → N8N labels and routes deterministic items
  → Anything needing judgment → Ava via Airweave context
  → Ava decides / drafts / escalates
  → Harry executes operational follow-through where needed
  → Cem handles only high-risk items
```

### N8N vs Ava Split

#### What N8N Handles Alone (No Ava Involvement)

| Category | N8N Action |
|----------|-----------|
| Spam and newsletters | Auto-delete or spam folder |
| Shipping/tracking updates | Auto-archive to `/Logistics/` |
| Machine-generated marketplace notices (known rules) | Route to mapped destination |
| Receipts/invoices | Forward to Xero workflow |
| Support messages needing only deterministic ticket routing | Route to Freshdesk |
| No-reply service notifications | Auto-archive |
| Calendar invites (known domains) | Auto-accept |

**Rationale:** The modern safe automation pattern is to automate only what is clearly low-risk. N8N's current templates explicitly preserve control on sensitive email by preferring draft-or-nothing over risky auto-send.

#### What N8N Passes to Ava

Pass to Ava when **any** of the following conditions are met:

- Sender is a prospect, supplier, partner, key customer, or founder-level contact
- Thread needs interpretation, prioritisation, or nuanced tone
- Prior history matters to the decision
- Multiple plausible actions exist
- Message mixes operational and strategic implications
- Confidence is below threshold
- Attachment review matters
- Reply quality affects revenue or relationships

### Handoff Object (Exact Specification)

```json
{
  "thread_id": "...",
  "source_mailbox": "...",
  "sender": "...",
  "subject": "...",
  "summary": "...",
  "classification": "...",
  "confidence": 0.0,
  "urgency": "low|normal|high|critical",
  "risk_flags": ["finance", "legal", "reputation", "sales", "supplier"],
  "recent_history": "...",
  "relevant_contacts": "...",
  "attachments": [{"name": "...", "type": "..."}],
  "suggested_next_step": "..."
}
```

Airweave's Outlook Mail connector exposes the fields needed to build this packet, including subject, sender, recipients, dates, body preview, importance, attachment presence, and web links back to the original message.

### Autonomous vs Escalate Rules

#### What Ava Handles Autonomously

Ava should be allowed to act autonomously on:

- Low-to-medium risk business replies where context and tone matter but no regulated or financial commitment is made
- Consulting lead triage and first-draft outreach
- Supplier clarification requests below commitment thresholds
- Internal routing decisions
- Summary creation and next-step recommendations
- Draft generation for Cem review on important but noncritical threads
- Acknowledgment emails (after first 30 supervised days)
- Meeting confirmation emails
- Standard follow-up templates

#### What Ava Must ALWAYS Escalate to Cem

Escalate when any one of these is true:

- Legal, tax, compliance, fraud, or chargeback language
- Price commitment, payment promise, refund exception, or inventory commitment above threshold
- Public reputation or marketplace account risk
- Emotionally sensitive or adversarial thread where wording could materially change the outcome
- Board-level or founder-sensitive decision
- Low confidence after retrieval
- Contradictory memory or missing context
- Repeat failure on same thread
- Any new client proposal or pricing negotiation
- Any complaint or dissatisfied client signal
- Any email from unknown contact proposing partnership or investment
- Ava's confidence in classification is <80%

### Ava Strengths and How to Exploit Them

| Strength | How to Exploit |
|----------|---------------|
| Business-context reasoning across projects and threads | Give Ava only judgment-heavy mail, not mailbox sludge |
| Strong draft quality for nuanced replies | Preload SOUL.md guidance and contact briefs into approved memory |
| Contact-aware communications | Ask Ava for classification + proposed action + draft (not just a summary) |
| Ability to translate messy email into next actions | Use Ava heavily on consulting pipeline and supplier/customer nuance |
| Strength in sales/content/strategy work | Ava is the consultancy's primary comms and outreach engine |

### Ava Weaknesses and Design Responses

| Weakness | Design Response |
|----------|----------------|
| Memory loss between sessions | Keep approved memory in Supabase, not only inside Ava's local state; re-feed SOUL.md + client context at session start |
| Blockers / stuck sessions | If Ava cannot classify or draft within SLA, N8N must route the item to Cem with the same packet plus failure reason |
| Quality variance | Require Ava to output structured fields: classification, rationale, recommended owner, risk flags, draft, confidence. Low-confidence outputs auto-escalate. |
| Overreach risk | Disable autonomous sending for high-risk categories; require draft-only behavior there |
| Context contamination | Hermes may propose memory updates; policy memory remains human-approved only |

### Fallback Protocol When Ava Is Down

N8N must remain independently useful even if Ava is unavailable.

**N8N-only degraded mode (when Ava is down):**

- N8N still catches all mail
- N8N still labels and archives deterministic mail
- N8N still routes receipts/tracking/spam/support tickets
- N8N still creates founder digest and urgent alerts
- N8N drafts only from approved templates for very low-risk replies
- N8N escalates all judgment mail directly to Cem instead of waiting on Ava
- **Ava does NOT attempt to catch up on a backlog during a bad session** — Cem reviews backlog manually after restoration

### KPI Targets

| KPI | Definition | 30-Day Target | Why It Matters |
|-----|-----------|:-------------:|---------------|
| Ava autonomous success rate | % of Ava-handled threads requiring no Cem correction within 72h | 70%+ | Tells Cem whether to trust Ava more or tighten N8N rules |
| N8N deterministic clearance rate | % of inbound mail closed without Ava or Cem | 40–60% | Measures how much sludge is removed early |
| Cem manual-read rate | % of total business mail Cem must personally open | <20% | Direct founder time metric |
| Escalation precision | % of escalations Cem agrees were worth escalating | 85%+ | Prevents spammy "just in case" escalation |
| Ava rework rate | % of Ava drafts materially rewritten by Cem | <30% | Quality control |
| Ava outage impact | % of mail still processed correctly when Ava unavailable | >80% deterministic path | Proves fallback resilience |
| First-response SLA for important mail | % of high-priority mail triaged within same business day | >95% | Protects revenue and relationships |

**Decision rule:** If Ava's autonomous success rate stalls below target, inspect failure modes and decide whether those failure classes should become more deterministic inside N8N, more memory-backed through Supabase, or more tightly escalated to Cem.

### Current Airweave + OpenClaw Integration Pattern

The practical integration pattern for Cem:

1. Keep mailbox data synced into Airweave
2. Let Ava query Airweave-backed context for grounded triage
3. Use OpenClaw MCP definitions to manage that tool access cleanly
4. Keep N8N as the catch-first router underneath

Airweave publishes official setup and search skills that teach agents how to configure MCP and search collections. OpenClaw has mature MCP registry/serve commands for managing outbound MCP definitions and exposing routed conversations.

### Implementation Sequence for Q4

**Week 1:**
- N8N catches all email
- Deterministic rules remove sludge
- Ava receives only judgment mail
- Cem gets one daily digest plus urgent alerts

**Week 2:**
- Add Supabase-backed approved memory for contacts, SOPs, and escalation rules
- Hermes starts pattern extraction from resolved threads
- Begin measuring Ava autonomous success rate and rewrite rate

**Week 3:**
- Tighten N8N rules based on Ava misses
- Expand Ava autonomy in categories where she is consistently accurate
- Use Ava heavily on consulting outreach and relationship-driven communication

**Week 4:**
- If stable, add Paperclip shadow governance for audit, budgets, and escalation analytics

---

## 6. WIKI → CONSULTING IP CONVERSION (Q3)

*Source: Council Member 2 — Claude Sonnet*

### Context and Key Correction

The V1 pipeline architecture is sound. Two critical corrections for V2:

1. **Ava owns the weekly harvest** — not a future Hermes agent. Ava runs on Mac Studio, already has web browsing and research capability, and is the Strategist. Weekly wiki scanning is strategist work: pattern recognition, classification, triage.
2. **Case studies target US e-commerce founders** — language, examples, pain points, and legal context are all US-based. Specific US platforms: Amazon FBA/FBM, Shopify, Walmart Marketplace, TikTok Shop. Revenue figures in USD. Pain points framed for US operators.

### Document Classification Framework

Before conversion, Ava runs classification against each new wiki file.

**Classification Prompt (Ava executes via Claude Desktop or direct prompt):**

```
You are reviewing a project wiki file from an e-commerce AI implementation at Ecell Global.
Classify this document on three dimensions:

1. CONTENT TYPE: [Implementation Log / Agent Config / Workflow Design / Analysis Report /
   Error Log / System Architecture]
2. OUTCOME CLARITY: [Clear outcome documented / Partial outcome / No outcome documented]
3. REUSE POTENTIAL: [High (repeatable by US e-commerce SMB) / Medium (adaptable with context) /
   Low (Ecell-specific, no transfer value)]

Then extract:
- Core workflow being documented (1 sentence)
- US e-commerce relevance: Does this apply to Amazon FBA, Shopify, Walmart Marketplace,
  or multi-channel operations?
- Inputs required to execute this workflow
- Outputs/outcomes produced
- Tools/APIs involved
- Estimated time saved vs manual process (if calculable)
- Case study headline potential: Could this become a US client-facing case study? (yes/no + 1 sentence draft headline)

Output as structured JSON.
```

**Quality Gate 1:**

- REUSE POTENTIAL must be "High" or "Medium" to proceed
- OUTCOME CLARITY must be "Clear outcome documented" for client-facing conversion
- US e-commerce relevance must be confirmed for Track B conversion
- Files rated Low/No outcome → archived to `raw-intelligence/` folder

**Estimated Classification Time (Ava):** 30–45 minutes for up to 100 wiki files via a Python script batch-feeding files to the prompt. Ava returns JSON manifest.

### Three-Track Conversion Pipeline

#### TRACK A: Internal Playbooks (Ecell Operations)

**Purpose:** Standardize how Ava and Harry execute recurring workflows. These become the source truth for agent execution and eventually feed Supabase RAG memory.

**Owner:** Ava (converts), Cem (reviews once), Harry (executes finance/inventory variants)

**Internal Playbook Format Standard:**

```markdown
# [WORKFLOW NAME] — Internal Playbook

## Purpose
One-sentence description of what this workflow achieves.

## Agent Assignment
- Primary: [Ava / Harry / N8N]
- Ava executes if: [judgment required, email/comms involved, research required]
- Harry executes if: [finance data, inventory data, Xero, Walmart API, BigQuery]
- N8N executes if: [deterministic routing, receipts, tracking, simple conditionals]
- Reviewer: Cem (first 3 runs), then autonomous with weekly spot-check

## Trigger Condition
When does this workflow run? (time-based / event-based / manual trigger / Ava detects)

## Pre-conditions
- What must be true before starting
- Required data inputs
- Required tool access

## Step-by-Step Execution
1. [Step with exact tool/API call]
2. [Expected output format]
3. [Decision branch: IF [condition] THEN [action] ELSE [escalate to Cem]]

## Escalation Rules
- Escalate to Cem when: [specific condition — cost threshold, irreversible action, ambiguous data]
- Timeout threshold: [X minutes/hours]
- Fallback if escalation not received within [Y time]

## Quality Gate
- Success metric: [specific measurable output]
- How Ava/Harry confirms completion

## Review Frequency
[Weekly / Monthly / On system change]

## Last Updated
[Date] by [Human/Agent]
```

**Conversion Prompt (Ava runs this on classified High/Medium files):**

```
You are converting a raw project log into an internal operating playbook for AI agents
Ava and Harry.
The agents are technical and need precise instructions, not explanations.
Strip out all reasoning, history, and narrative.
Retain: exact steps, tool names, API endpoints, decision logic, and escalation conditions.
Determine whether this workflow belongs to Ava (strategy, content, email, research)
or Harry (finance, inventory, orders, Xero, BigQuery).
Output in the Internal Playbook format.
Flag any gaps where the original log is ambiguous with [NEEDS CLARIFICATION: ___].
```

**Quality Gate 2:** All [NEEDS CLARIFICATION] flags resolved → Cem validates accuracy once → Tested by running with Ava or Harry on one real task → Promoted to production.

**Estimated Time per Playbook:** 20 minutes (5 min Ava conversion + 15 min Cem review)

---

#### TRACK B: Client-Facing Templates (US Consultancy IP)

**Purpose:** Package Ecell's proven workflows into deliverables that US SMB clients receive after an Implementation engagement. These are the IP that justifies the $3,000–$8,000 price point.

**Revision:** All examples, case study headlines, and pain-point language are rewritten for US e-commerce founders. Specific references to:
- Amazon FBA/FBM (not "Amazon UK")
- Revenue in USD (not GBP)
- US platforms: Shopify, Walmart Marketplace, TikTok Shop
- US pain points: ASIN suppression, Section 3 account reviews, US return rates, FBA fee increases, Buy Box competition

**Format Standard (3-part deliverable per workflow):**

**Part 1 — "How We Built It" US Case Study (2 pages)**

```
HEADLINE: How [Ecell/Client] [Result] Using AI in [Timeframe]
Examples for US market:
- "How We Automated Amazon FBA Restock Decisions Across 200K SKUs — Cutting Manual Review
  from 8 Hours to 30 Minutes"
- "How We Eliminated Manual Invoice Entry for a 6-Channel E-Commerce Operation Using a
  $40/Month N8N Automation"
- "How We Generated 4M+ Amazon Listing Descriptions Without a Copywriting Team"

THE SITUATION: What problem existed before (in US e-commerce context)
THE SOLUTION: What was built (no code, tool names only — "automation tool," "AI agent")
THE RESULT: Measurable outcome (time saved, revenue impact, error reduction, in USD)
WHAT YOU NEED: Prerequisites any US e-commerce business must have to replicate this
```

**Part 2 — Implementation Guide (3–5 pages)**

```
WHAT THIS DOES: Plain English description
WHO THIS IS FOR: US e-commerce business type, size, tech requirements
WHAT YOU'LL NEED: Tools list with costs in USD and alternatives
STEP-BY-STEP GUIDE: Non-technical walkthrough
COMMON MISTAKES: Top 3 things that break this
EXPECTED TIMELINE: Week-by-week from start to live
HOW TO MEASURE SUCCESS: 3 KPIs to track (in US context — FBA fees, hourly rate saved,
  error rate)
```

**Part 3 — SOP Quick-Reference Card (1 page)**

```
[Workflow name]
INPUTS → PROCESS → OUTPUTS
FREQUENCY: [Daily/Weekly/Monthly]
OWNER: [Human role / AI agent]
ESCALATE IF: [condition]
```

**Conversion Prompt (Ava executes — US-market version):**

```
You are a business consultant converting a technical implementation log into a client
deliverable for US e-commerce business owners.
Your audience is a US small business owner selling on Amazon, Shopify, or Walmart —
no technical background.
NEVER mention code, APIs, or model names.
DO mention: hours saved per week, money saved in USD, errors eliminated, process speed.
USE US e-commerce language: FBA, ASIN, Buy Box, Shopify store, Walmart Marketplace.
Frame outcomes in US market context (USD, US business hours, US regulations).
Translate every technical step into a business outcome.
Use "you" throughout — write as if coaching the reader.
Output in the three-part Client Template format.
```

**Quality Gate 3 — Client Templates:**
- No technical jargon (Ava runs a second-pass check)
- At least one quantified outcome in USD or hours
- US e-commerce relevance confirmed
- Reviewed by Cem for accuracy once before first client delivery

**Estimated Time per Client Template:** 45 minutes (15 min Ava generation + 30 min Cem review + formatting)

---

#### TRACK C: SaaS Product Specifications

**Purpose:** Document workflows horizontal enough to become standalone SaaS products.

**Threshold for Track C:**
1. Applicable to 10+ different US businesses
2. Requires <2 hours of setup per client
3. Core value is the automation itself, not the consulting

**Ava's role:** Run US market validation research to confirm competitor landscape and US pricing benchmarks before any Track C document is created.

**Format Standard and quality gates from V1 remain valid. USD pricing throughout.**

---

### Master Conversion Workflow — Ava as Harvest Agent

```
STEP 1: WEEKLY WIKI HARVEST (15 min/week — Ava executes Monday morning)
  Owner: Ava (Mac Studio)
  Action: Scan OpenClaw wiki for new/updated files from past 7 days
  Method: Directory scan via file access or Python script Ava runs
  Output: JSON manifest of new files with metadata
  Ava also flags: any file that directly maps to a US e-commerce pain point
  → Ava sends Cem a Slack/email summary: "X new wiki files found. Y are Track B candidates."

STEP 2: BATCH CLASSIFICATION (30 min/batch — Ava executes)
  Owner: Ava
  Action: Run Classification Prompt against all new files
  Output: Classification JSON for each file — includes US relevance score and draft headline
  Ava self-triage: auto-archives Low/No outcome files without Cem involvement

STEP 3: TRIAGE DECISION (10 min/week — Cem only)
  Owner: Cem
  Action: Review Ava's classification summary (not raw JSON — Ava presents a readable brief)
  Decide: Which track (A/B/C) for each High/Medium file
  Output: Annotated list with track assignments → Ava proceeds

STEP 4: PARALLEL CONVERSION (runs async — Ava executes all tracks)
  Track A → Ava converts to Internal Playbook draft (assigns to Ava or Harry as appropriate)
  Track B → Ava enriches with US market context → Ava drafts Client Template
  Track C → Ava runs US competitor research → Ava drafts SaaS Spec
  All outputs tagged [DRAFT — AWAITING CEM REVIEW]

STEP 5: QUALITY REVIEW (20 min/week — Cem)
  Review Ava's converted drafts (Ava presents in a review-ready format, not raw markdown)
  Resolve any [NEEDS CLARIFICATION] flags
  Approve for publication

STEP 6: PUBLISH
  Track A → Markdown /playbooks folder (Ava updates, Harry reads for finance/inventory playbooks)
  Track B → Notion client template library or Google Drive (Ava organises)
  Track C → Product backlog (Notion or Linear)
  Ava updates the master IP inventory document

STEP 7: MAINTENANCE LOOP (monthly — Ava)
  Ava flags playbooks older than 90 days for review
  Ava alerts Cem to any playbook that has a corresponding system change
  Ava checks if new Ecell outcomes (performance data from Harry) should update existing case studies
```

**Total Weekly Time Commitment:** ~30 minutes (Cem) + Ava runs steps 1–4 and 7 autonomously.

### Revised Tooling Table

| Step | Agent/Tool | Why |
|------|-----------|-----|
| Wiki harvest + classification | Ava (Mac Studio) | She's the Strategist; pattern recognition across content is strategist work |
| Track A conversion | Ava → assigns to Ava or Harry | Ava knows which workflows belong to which agent |
| Track B enrichment | Ava (web research + US market context) | Ava has research capability; she ensures US framing |
| Track B narrative | Ava (Claude-based generation) | Business voice, US-market non-technical rewrite |
| Track C market validation | Ava (web research) | Competitor research, US pricing benchmarks |
| Track C PRD | Ava | Structured document output |
| RAG publishing (future) | Ava → Supabase | Semantic search for both Ava and Harry |

### US Market Case Study Priority (First 4 to Build)

These four Ecell projects translate most directly to US e-commerce founder pain points:

| # | Ecell Project | US-Targeted Headline | Key Outcome (USD Framing) |
|---|--------------|----------------------|--------------------------|
| 1 | N8N invoice/receipt automation | "We Eliminated 10+ Hours/Week of Manual Data Entry with a $40/Month Automation" | Time saved, error reduction, $40/mo N8N cost vs. $50/hr manual labor |
| 2 | Multi-Channel Feed Engine | "How We Generate Amazon Listings for 4M+ ASINs Without a Copywriting Team" | Scale, speed, cost saving vs. $0.10–0.50/listing copywriting market rate |
| 3 | BigQuery/Walmart analytics | "We Turned 3 Days of Manual Reporting into a 30-Minute Weekly AI Briefing" | Time saved, decision quality, applicable to any multi-channel US seller |
| 4 | Zero Fulfillment AI routing | "How AI Routes Purchase Orders Across 5 Countries — Zero Manual Decisions" | Speed, accuracy, scale — US 3PL and FBA hybrid operators will relate |

**IP Protection Note:** These are Cem's own operations. No NDA required. Post client work, add a consent clause in US client contracts for anonymised case study use.

---

## 7. AI CONSULTANCY LAUNCH PLAYBOOK — US S-CORP (Q5)

*Source: Council Member 2 — Claude Sonnet*

### Entity Context (Corrected)

**Operating entity:** Existing US S-Corp, Orlando, Florida. **No new entity setup required.**

- S-Corp is already formed — bypass all V1 "Option A/B/C" entity discussion
- Ecell Global UK handles UK/EU e-commerce operations (separate entity, separate invoicing)
- US consultancy invoices under the US S-Corp from Day 1
- Keep entities clean: no cross-invoicing between US S-Corp consulting revenue and UK e-commerce revenue without accountant guidance on transfer pricing

**S-Corp compliance reminders (existing entity — confirm annually):**

- Annual Report due May 1 to Florida Division of Corporations ($138.75 renewal fee for LLCs / $150 for corps)
- Form 1120-S federal tax return due March 15 (or extend to September 15 via Form 7004)
- Reasonable salary requirement: Cem must pay himself a reasonable W-2 salary from the S-Corp before taking distributions — confirm with CPA if not already doing this
- Payroll tax filings: Form 941 quarterly

### US Market Context (2026)

| Metric | US Market 2026 | UK Market 2026 |
|--------|---------------|----------------|
| AI consultant hourly rate (mid-level solo) | $150–300/hr | £90–180/hr |
| Typical SMB implementation project | $8,000–15,000 | £5,000–10,000 |
| Monthly retainer (ongoing support) | $2,000–8,000/mo | £750–2,500/mo |
| AI readiness audit (standalone) | $1,500–5,000 | £750–2,500 |
| Orlando/FL market rate (vs. SF/NY) | ~15–25% below national top | — |

**Key 2026 demand signals (US-specific):**

- 57% of US small businesses are investing in AI in 2026, up from 36% in 2023 — but most haven't achieved measurable ROI. That gap is the market.
- US SMB AI adoption projected to hit 55%+ — but the majority are using AI tools, not AI workflows. Cem sells workflows.
- LinkedIn's 2026 SMB report identifies "AI literacy and upskilling" as the #1 competitive differentiator. Cem's model of implementation + training is exactly what's in demand.
- Most US AI consultants charge $10,000–25,000 for what Cem can deliver for $3,000–8,000 by using his own proven templates. He's not the cheapest — he's the best value with real proof.

**The Orlando/FL angle:**

- Orlando has an ~80,000-professional tech ecosystem growing at 2x the national rate, anchored in simulation, gaming, defense, and increasingly AI
- Central Florida is home to substantial e-commerce operations (tourism merch, consumer goods, healthcare products) — all underserved for AI automation
- Florida has no state income tax — genuine selling point for the S-Corp margin
- Face-to-face credibility from local engagements (Chamber events, SBDC) builds the reputation that fuels US-wide remote work

### Ideal Customer Profile (US-Revised)

**Primary ICP — US E-Commerce SMB (the bullseye):**

- Online retailer, 1–15 staff
- Selling on Amazon (FBA/FBM), Shopify, Walmart Marketplace, or combinations
- Revenue: $500K–$5M/year
- Pain: Spending 20+ hours/week on manual listing management, inventory tracking, reporting, or customer service
- Tech sophistication: Uses Shopify/Amazon Seller Central but hasn't automated beyond basic Zapier triggers
- Decision maker: Founder/CEO
- Budget signal: Paying $200–600/month for tools that don't talk to each other

**Secondary ICP — Orlando/FL Local Businesses (face-to-face credibility builders):**

- Any local business with 2–20 staff and high-volume repetitive digital operations
- Professional services (accountants, marketing agencies, law firms) drowning in admin
- Tourism/hospitality vendors with inventory and booking complexity
- Physical product businesses with manual order management
- Revenue: $200K–$3M/year
- Value: These clients build local case studies and referral networks; fastest to close when you can walk in

**Tertiary ICP — UK SMBs:**

- Secondary channel only. Do not dedicate marketing spend here.
- These come inbound from Ecell Global's existing supplier/partner network

**ICP Anti-Profile (Do NOT pursue):**

- Businesses wanting "AI strategy" reports without implementation ($0 ROI, no repeat)
- Businesses with <$100K revenue (can't afford meaningful engagement)
- Enterprises (>250 staff) — procurement processes kill timeline
- Businesses hostile to technology or locked into inflexible legacy systems

### Service Packaging — USD Pricing (Validated Against US Market)

#### Tier 1 — AI Opportunity Audit

**Price:** $997 (entry) / $1,997 (comprehensive)
**Cem's Time:** 2–3 hours
**AI Leverage:** 85% (Ava handles questionnaire analysis, report draft, opportunity scoring)

**Market Validation:**

- US AI readiness assessments from established firms: $5,000–25,000
- Comparable solo operator audits (US market): $750–2,500
- At $997, this is below the "decision by committee" threshold for most founders — they can say yes without approval

**Deliverables:**

- Pre-audit questionnaire (Ava generates, Cem reviews in 20 min)
- 2-hour discovery call (Cem only — this is the sales conversation)
- AI Opportunity Report (Ava drafts from discovery call notes/transcript):
  - Top 3 automation opportunities ranked by ROI
  - Estimated time/cost savings per opportunity (in USD and hours/week)
  - Tool recommendations with costs
  - Implementation complexity rating
  - One "Quick Win" the client can implement themselves in <1 week
- 30-min debrief call (upsell conversation for Tier 2)

**AI-First Delivery Protocol:**

1. Client completes Ava-generated 20-question intake form (Typeform → Ava or N8N → Google Doc)
2. Ava reviews intake and prepares 5 tailored discovery questions for Cem
3. Discovery call is recorded
4. Recording transcript → Ava → Opportunity Report draft
5. Cem reviews and approves (30 min)
6. Report delivered within 48 hours of call

**Audit → Implementation conversion target:** 40–60%

---

#### Tier 2 — AI Implementation

**Price:** $3,000–$8,000 depending on scope

**Market Validation:**

- US AI consultants for SMBs charge $8,000–15,000 for standard implementations
- Cem's range is intentionally below market to accelerate first-client wins, but not low enough to signal low quality

**Scope Definition by Price Point:**

| Price | Scope |
|-------|-------|
| $3,000 | One workflow automation (email triage, inventory alerts, OR order processing) |
| $4,500 | Two connected workflows (e.g., email triage + CRM update) |
| $6,000 | Three workflows or one complex multi-system integration |
| $8,000 | Full e-commerce AI stack: 4–5 workflows + 60 days monitoring + training |

**Cem's Time:** 8–15 hours over 4–6 weeks
**AI Leverage:** 80% — Ecell templates handle 80% of technical implementation

**Deliverables:**

- Workflow implementation (N8N/Zapier automation, agent config, API integration)
- Custom SOP documentation for client's team (Ava drafts)
- 2 weeks post-launch monitoring
- 1-hour training session (can be async Loom — record once, reuse)

**Scope Creep Protection:** Contract specifies exact workflow names. New workflows = new engagement or Change Order at $750/additional workflow.

---

#### Tier 3 — AI Managed Service (Retainer)

**Price:** $1,500/month (standard) / $3,000/month (growth)

**Market Validation:**

- US AI consultant retainers: $2,000–8,000/month
- Cem's $1,500 standard retainer is priced ~25% below market minimum — intentional to capture first 5 retainer clients and build MRR fast
- Raise to $2,000 standard / $3,500 growth after first 5 retainer clients secured

**Deliverables (Standard — $1,500/mo):**

- Ongoing monitoring of implemented automations
- Monthly performance report (Ava generates from agent/workflow logs)
- Up to 2 hours maintenance/minor updates per month
- Response to issues within 24 business hours
- Ava handles routine client check-in communications via Airweave

**Deliverables (Growth — $3,000/mo):**

- Everything in Standard
- Monthly 45-min strategy call with Cem
- One new automation or improvement per month
- Priority response within 4 business hours
- Ava handles pre-call research and post-call action item drafting

**Revenue Math (USD):**

- Break-even: 2 standard retainer clients ($3,000 MRR with ~8 hrs/month total)
- Lifestyle floor ($5K+ MRR): 4 standard or 2 growth clients
- Target by Month 6: 6–8 standard retainer clients = $9,000–12,000 MRR recurring

### Pricing Validation Table

| Comparison Point | US Market Rate | Cem's Rate | Position |
|-----------------|----------------|------------|---------|
| AI readiness audit (US firm) | $5,000–25,000 | $997–1,997 | 80–95% below — no-risk entry |
| AI implementation (US solo consultant) | $8,000–15,000 | $3,000–8,000 | 45–60% below — template advantage |
| AI implementation (US agency) | $25,000–60,000 | $3,000–8,000 | 85–90% below — solopreneur edge |
| Monthly retainer (US solo consultant) | $2,000–8,000/mo | $1,500–3,000/mo | Competitive entry pricing |
| Monthly retainer (US agency) | $10,000–30,000/mo | $1,500–3,000/mo | Structural advantage |
| AI contractor hourly (US, mid-level) | $150–300/hr | Implied $200–250/hr | Fully competitive |

**Verdict:** Cem's pricing is aggressive for rapid first-client acquisition without undercutting quality signals. The $997 audit is priced to get "yes" without committee approval. The $3,000–8,000 implementation is priced to compete with the top US solo operators while being unbeatable on value. **Do not discount below these floors.**

### Lead Generation Strategy — US-Focused, Revenue-Urgent

**Priority order for Week 1–4 (survival timeline):**

#### Channel 1: Ava-Assisted LinkedIn Outreach (Start Day 1 — Highest Urgency)

**Target:** US e-commerce founders on LinkedIn with 500–10,000 connections, posting about operational pain — Amazon FBA sellers, Shopify merchants, Walmart marketplace operators.

**Ava's role (critical):**
1. Ava researches and builds a target list of 30 prospects/week (company size, platform, recent posts about operational pain)
2. Ava drafts personalised connection notes and Messages 2/3 from prospect's LinkedIn profile
3. Cem reviews each draft in 3–5 minutes, personalises if needed, sends
4. Ava tracks replies and drafts response options for Cem

**Outreach sequence (Ava drafts all):**

- Message 1: Genuine engagement with a specific post they made (Ava identifies the post, drafts the comment/message — never templated)
- Message 2 (7 days, no response): Short intro + one relevant US case study link
- Message 3 (7 more days): Final value add + clear offer ("Free 20-min call to see if your ops are automatable")

**Target:** 30 outreach contacts/week → 5–10% book calls → 1–2 discovery calls/week

---

#### Channel 2: Orlando/FL Local Business Networks (Start Week 1)

**Primary local channels:**

- **Orlando Chamber of Commerce (OCOC)** — networking events are free for members and prospective members. The April 2, 2026 Business Social at Joe's Crab Shack is immediately actionable. RSVP via smatthews@myococ.com.
- **East Orange County Chamber of Commerce (EOCC)** — Business Expo with 500+ attendees, 150+ exhibitors. Immediate local reach.
- **Innovate Orlando / Orlando Tech Community** — Startup-tier membership is FREE for pre-$1M revenue companies. Register at innovateorlando.io
- **Florida SBDC at UCF** — Free consulting for Florida businesses. Cem should engage as a guest expert, not a client. SBDC advisors regularly refer clients to specialists.
- **Hispanic Chamber of Commerce of Central Florida** — $525/year, diverse local business network with underserved AI consulting needs.

**Face-to-face strategy:** Attend 2 local events in the first 30 days. Don't pitch — demonstrate expertise. Specific tactic: offer a free 20-minute "AI Opportunity Assessment" at networking events. Ava schedules, Cem delivers. In-person demos consistently outperform cold outreach by 3–5x close rate.

---

#### Channel 3: US E-Commerce Communities (Start Week 2 — Ava Manages)

**Target communities:**

- **Reddit r/FulfillmentByAmazon** (~350K members) — High density of exactly Cem's ICP
- **Reddit r/shopify** (~500K members) — Active founder community
- **Reddit r/ecommerce** (~300K members) — Broad multi-platform operators
- **Seller forums:** Seller Central forums, Helium 10 Facebook groups, Jungle Scout community

**Ava's role (autonomous, supervised):**

- Ava monitors these communities weekly for questions about automation, operations, AI tools
- Ava identifies top 3–5 questions per week where Cem's expertise is directly relevant
- Ava drafts genuinely helpful answers (no pitch, no link unless directly relevant)
- Cem reviews in 5–10 min, posts under his own account

**Rule:** Never pitch directly. Provide genuine value. Signature/flair can mention "AI automation for e-commerce ops" + website link.

**Expected outcome:** 2–4 weeks of consistent presence → inbound DMs from founders with problems → these convert at significantly higher rates than cold outreach because they already know Cem is credible.

---

#### Channel 4: Florida Small Business Associations + SBDC (Start Week 2)

- **Florida SBDC Network** — 40+ offices across Florida, free consulting and resources, plus a referral network of founders actively seeking growth resources.
- **Florida Realtors, local professional associations** — Secondary channels for non-e-commerce local business leads

---

#### Channel 5: Partnership Pipeline (Start Week 3)

| Partner Type | US Version | Referral Offer |
|--------------|-----------|----------------|
| E-commerce accountants/CPAs | US e-commerce CPAs (Catching Clouds, A2X partners) | 10–15% referral fee or reciprocal |
| Shopify/WooCommerce developers | US Shopify Plus partners | They build the store, Cem automates it |
| Amazon listing optimization agencies | US agencies (Incrementum Digital, etc.) | Complementary services, not competitors |
| 3PL/fulfillment companies | US 3PLs seeking to add value to clients | Cem automates their clients' order flows |

---

### Website Requirements (US Version)

#### Phase 1 (Launch in Week 1–2)

**Domain:** `.com` domain — `ecellai.com`, `ecell-ai.com`, or Cem's personal brand `[name]ai.com`. Check availability. **Do NOT use ecellglobal.com** — keep the consultancy brand distinct from the UK e-commerce business.

**Build:** Framer (fastest to launch, $20/month Pro) or Webflow ($23/month). Can be live in 2 days.

**Must-have pages:**

1. **Home:** Single value proposition — "We automate the operations slowing your e-commerce business down." Target: Amazon FBA, Shopify, Walmart sellers. CTA: "Book a free 20-min intro call." Calendly embed.
2. **Services:** Three-tier pricing table in USD (Audit $997–1,997 / Implementation $3,000–8,000 / Managed Service $1,500–3,000/mo)
3. **Case Studies:** 4 Ecell-based US-framed case studies (initial; client cases added over time)
4. **About:** Ecell credibility story — 21 years, 200K+ SKUs, 5 sales channels, AI-native operations. "This is not theory — this is what I run every day." US S-Corp, based in Orlando, FL.
5. **Contact/Booking:** Calendly embed with "Free 20-min AI Opportunity Call" offer

#### Phase 2 (Month 2–3)

- Blog: Track B case studies published here (Ava populates on a schedule)
- Lead magnet: "AI Automation Audit Checklist for E-Commerce Operations" (PDF) → email capture → N8N follow-up sequence
- Testimonials: Add after first 2–3 US client engagements

**Cost estimate:**

| Item | Cost |
|------|------|
| Framer Pro | $20/month |
| .com domain | ~$12–15/year |
| Calendly | Free tier (upgrade to $10/month if needed) |
| **Total monthly recurring** | **~$20–30/month** |

---

### Legal: Florida S-Corp + US Professional Services

#### Operating Under the Existing US S-Corp

| Item | Action | Cost | Timeline |
|------|--------|------|----------|
| S-Corp "reasonable salary" | Confirm with CPA that Cem is taking a W-2 salary from the S-Corp | $0 (or CPA fee) | Before first invoice |
| Florida Business License | Confirm county occupational license for Orange County, FL covers consulting | $25–75/year | Week 1 |
| US Client Contract (MSA) | Ava generates Master Services Agreement draft using US law template | $0 (Ava) + $500–800 attorney review | Week 1–2 |
| Statement of Work template | Ava generates SOW template per engagement type | $0 | Day 1–2 |
| NDA | Ava generates mutual NDA (included in MSA) | $0 | Day 1 |
| IP ownership clause | All contracts: "All work product created during engagement is owned by client upon full payment" (work-for-hire under US copyright law) | In contract | Day 1 |
| E&O Insurance (Professional Liability) | US E&O/professional liability insurance. For a tech/AI consultant: $900–1,800/year for $1M coverage | $75–150/month | Week 1–2 |
| General Liability Insurance | Supplement E&O with general liability; bundle often cheaper | $50–100/month | Week 2 |
| US Data Processing | Include data handling clause in MSA covering client data under Florida FIPA and applicable state laws | In contract | Week 1 |
| Business bank account | If US S-Corp doesn't have a dedicated account: Mercury, Relay, or Chase Business | $0 (Mercury/Relay) | If needed |

**Key contractual protections (US law):**

1. Limitation of liability: Cap at 1x engagement fee (standard US tech consulting)
2. No performance guarantees on AI outcomes ("results may vary based on client's systems and data")
3. IP ownership: Work-for-hire; IP transfers on final payment
4. Confidentiality: Mutual NDA in MSA
5. Payment terms: 50% upfront, 50% on delivery (Implementation); monthly in advance (Retainer); full payment upfront for Audit
6. Governing law: Florida, Orange County jurisdiction

**E&O Insurance note:** At $60–150/month ($716–1,800/year), this is non-negotiable before the first client engagement. Use Next Insurance, Hiscox USA, or Embroker for fast online quotes for tech consultants. Quote and bind in 24 hours online.

---

### Ava's Role in the Consultancy (Detailed)

Ava is not just a document generator. She is the consultancy's research-and-communications engine.

| Consultancy Task | Ava's Role | Cem's Role |
|-----------------|-----------|------------|
| Prospect research | Builds target list, researches each prospect (LinkedIn, website, recent news), flags pain points | Reviews list, prioritises outreach |
| Outreach drafting | Writes all 3 messages in outreach sequence, personalised per prospect | Reviews, approves, sends (3–5 min/prospect) |
| Discovery call prep | Pre-call brief: company overview, key pain points, suggested questions | Reviews brief (10 min), leads call |
| Intake form analysis | Reads completed questionnaire, extracts key findings, flags high-opportunity signals | Reviews summary (10 min) |
| Opportunity Report drafting | Generates full report from call transcript/notes | Reviews and approves (30 min) |
| Proposal drafting | Generates proposal and SOW from Opportunity Report | Reviews and approves (15 min) |
| Client communication | Drafts all client emails (kickoff, updates, milestone, invoice follow-up) via Airweave | Approves key comms; auto-sends routine ones |
| Case study creation | Drafts Track B case study post-project | Reviews and approves (30 min) |
| LinkedIn content | Drafts 2 posts/week (case study + insight mix) | Approves and posts (10 min each) |
| Community monitoring | Monitors Reddit/forums weekly, drafts responses to relevant questions | Reviews and posts (5–10 min each) |
| Monthly client reports | Generates performance report from workflow logs | Reviews and sends |

**Ava's constraints to account for:**

- **Memory loss between sessions:** Ava needs a consultancy SOUL.md / client context file re-fed at the start of each session for new clients
- **Quality variance:** All client-facing comms require Cem's approval before sending (not autonomous for new clients)
- **Airweave dependency:** Ensure Ava's Airweave email access covers the consultancy-dedicated email address (separate from Ecell operations email)

### Accelerated 6-Month Timeline with Revenue Targets

**V1 started revenue in Month 2. V2 targets the first paying client in Week 3–4. Parallel-tracking consultancy setup with Ecell autonomy work is mandatory.**

| Week/Month | Focus | Key Actions | Revenue Target | Cem Hours/Week on Consultancy |
|-----------|-------|-------------|----------------|-------------------------------|
| **Week 1** | Foundation sprint | E&O insurance quoted and bound; MSA/SOW drafted by Ava; .com domain registered; Framer site 50% built; Ava briefed on consultancy research tasks; first 3 US case studies drafted by Ava from Q3 Track B; LinkedIn profile updated to "AI Automation Consultant \| Orlando, FL"; OCOC April 2 event registered | $0 | 6 hrs |
| **Week 2** | Launch + first outreach | Website live; Calendly live; Ava begins 30-prospect LinkedIn research list; first 10 outreach messages sent by Cem (Ava-drafted); join Innovate Orlando (free startup tier); first Reddit/community posts (Ava drafts, Cem posts); SBDC UCF introduction email | $0 | 8 hrs |
| **Week 3** | First discovery calls | Target 2–4 discovery calls booked; OCOC networking event (April 2); Ava preps research briefings for each discovery call prospect; Cem closes first Audit engagement | **$997–1,997 (first Audit)** | 10 hrs |
| **Week 4** | First revenue delivered | Deliver first Audit; debrief call; upsell to Implementation conversation; second discovery calls; 30 more LinkedIn outreach (Ava) | **$997–1,997** | 10 hrs |
| **Month 2** | First Implementation | Convert 1 Audit to Implementation ($3,000–6,000); second Audit booked; continue 30/week outreach (Ava); first community authority posts gaining traction | **$4,000–8,000** | 12 hrs |
| **Month 3** | Pipeline builds | 2nd Implementation active; first retainer offer to Month 2 client; 3rd Audit running; first external (non-Ecell) case study published | **$6,000–12,000** | 12 hrs |
| **Month 4** | MRR foundation | 2–3 concurrent clients; 2+ retainer clients ($3,000–6,000 MRR); Ava handling all client comms drafting via Airweave | **$7,000–15,000** | 12 hrs |
| **Month 5** | Scale | 4–5 active clients; $6,000–9,000 MRR from retainers; partnership pipeline active | **$9,000–18,000** | 12 hrs |
| **Month 6** | Review gate | Assess pricing (raise if closing >60%); consider hiring if >15 hrs/week on delivery | **$10,000–20,000** | 12–15 hrs |

**6-Month Revenue Range:** $37,000–77,000 USD
**6-Month Investment Required:** ~$2,000–4,000 (insurance, legal review, tools)
**Break-even:** 2 Audit clients + 1 Implementation client

**Net hours rule:** Consultancy hours are drawn from time freed by Ecell autonomy work. Week 1 consultancy adds 6 hours — this must be offset by at least 6 hours freed from Ecell via the Q1/Q2 autonomy roadmap. **If Ecell automation is behind, consultancy launch slows. This is the single most important dependency.**

---

## 8. MASTER SOP LIBRARY (Q8)

*Source: Council Member 2 — Claude Sonnet*

### Prioritisation Framework

V1's Time Liberation Score (TLS) remains valid. V2 adds a second multiplier: **Revenue Unlock Score (RUS)** — the degree to which this SOP directly enables or accelerates consultancy revenue.

**Combined Priority Score = TLS × (1 + RUS)**

**Priority Tier definitions:**

| Tier | Definition | Build By |
|------|-----------|---------|
| **P0 (Pre-launch)** | Without this SOP, the consultancy cannot operate | Days 1–14 |
| **P1 (Week 1–4)** | High daily impact; blocks Ecell autonomy OR consultancy first revenue | Week 1–4 |
| **P2 (Month 2–3)** | Meaningful time savings; builds on P1 being operational | Month 2–3 |
| **P3 (Month 4–6)** | Quality and scale improvements; not blocking | Month 4–6 |

---

### CONSULTANCY SOPs — P0 (Build Before First Client)

These SOPs must exist before Cem takes his first paid engagement. Ava is primary agent for all of them.

---

#### C0-A: Client Intake & Discovery SOP

**Priority:** P0 — Pre-launch
**Owner:** Ava (primary execution) + Cem (calls + approvals)
**Purpose:** End-to-end process from first contact to signed proposal

```
TRIGGER: New prospect books a discovery call via Calendly

STEP 1: INTAKE FORM (48 hrs before call — Ava executes)
  Ava sends intake questionnaire to prospect (20 questions via Typeform or Google Form)
  Questions cover: current tools, team size, biggest operational pain points,
  annual revenue range, current weekly hours on manual tasks, tech comfort level
  Ava monitors for completion; sends one reminder at 24 hours if not completed

STEP 2: PRE-CALL BRIEF (24 hrs before call — Ava executes)
  Ava researches prospect: LinkedIn, company website, recent news, competitor landscape
  Ava reads completed intake form
  Ava generates "Discovery Call Brief" for Cem:
    - Company overview (2 sentences)
    - Top 3 automation opportunities identified from intake
    - 5 tailored discovery questions
    - Suggested engagement tier (Audit / Implementation estimate)
    - Any red flags (small revenue, tech hostility signals)
  Cem reviews brief (10 min before call)

STEP 3: DISCOVERY CALL (Cem only — 45–60 min)
  Cem follows brief; explores pain points; qualifies budget signals
  Call recorded via Fireflies.ai or Otter.ai (auto-transcribed)

STEP 4: OPPORTUNITY REPORT GENERATION (within 2 hrs of call — Ava executes)
  Ava receives transcript
  Ava generates AI Opportunity Report using Track B template (Q3):
    - Executive summary
    - Top 3 automation opportunities with ROI estimates in USD
    - Tool recommendations with costs
    - Implementation complexity ratings
    - "Quick win" recommendation
    - Proposed engagement: Audit tier (confirm) or skip directly to Implementation offer
  Cem reviews draft (30 min) → approves or requests revision

STEP 5: REPORT DELIVERY + UPSELL (within 48 hrs of call)
  Ava sends report to prospect via email (Airweave)
  Ava schedules 30-min debrief call for Cem
  Debrief call = proposal call: Cem presents Implementation scope + price

STEP 6: PROPOSAL GENERATION (after debrief — Ava executes in real-time)
  Ava generates proposal (SOW + pricing + timeline) from debrief call notes
  Cem reviews (15 min) → sends via PandaDoc or DocuSign

STEP 7: CONTRACT AND ONBOARDING
  Client signs → Ava triggers C0-B (Project Kickoff SOP)
  50% upfront invoice sent immediately (Ava drafts, Cem approves)

ESCALATION RULES:
  → Ava pauses and alerts Cem if: prospect asks for custom pricing structure,
    mentions legal review, asks about subcontracting, or revenue signals are unclear
  → Ava handles autonomously: scheduling, form reminders, report delivery
    (after first 3 successful runs with Cem review)

QUALITY GATE:
  → Report has at least 3 quantified opportunities (USD/hours)
  → Proposal has clear scope statement with named deliverables
  → Payment terms confirmed before Cem commits any implementation time

REVIEW FREQUENCY: Monthly for first 3 months; quarterly thereafter
```

---

#### C0-B: Project Kickoff SOP

**Priority:** P0 — Pre-launch
**Owner:** Ava (comms + documentation) + Cem (technical setup)
**Purpose:** Consistent, professional onboarding for every new Implementation client

```
TRIGGER: Contract signed + 50% deposit received

STEP 1: WELCOME PACKAGE (Day 1 — Ava executes via Airweave)
  Ava sends welcome email to client:
    - Intro to the engagement process
    - Access requirements list (what Cem needs from client)
    - Project tracker link (Notion or Google Sheets — Ava sets up)
    - Kickoff call scheduling link (Calendly)

STEP 2: ACCESS GATHERING (Days 1–3 — Ava manages)
  Ava sends access request form (API keys, tool access, credentials — via secure form)
  Ava tracks completion; sends reminders if incomplete after 24 hrs
  Cem receives credentials via secure channel (1Password or similar)

STEP 3: KICKOFF CALL AGENDA (48 hrs before call — Ava drafts)
  Ava prepares:
    - Agenda for 45-min kickoff call
    - Current-state workflow map (from intake + discovery notes)
    - Target-state workflow map (from Opportunity Report)
    - Week-by-week implementation timeline
  Cem reviews (15 min)

STEP 4: KICKOFF CALL (Cem leads — 45 min)
  Walk through current-state vs target-state
  Confirm scope and timeline
  Identify client point-of-contact for implementation questions
  Set expectations: client's required time commitment (~2 hrs/week for first 2 weeks)

STEP 5: PROJECT DOCUMENTATION CREATED (same day — Ava)
  Ava creates project folder in Google Drive or Notion:
    - Client background doc
    - Scope document (finalised)
    - Access credentials log (encrypted reference)
    - Weekly update template
    - Implementation log (running)

ESCALATION RULES:
  → Alert Cem if client cannot provide required access within 5 business days
    (scope and timeline affected; Change Order may be needed)
  → Alert Cem if client pushes for scope change during kickoff call

REVIEW FREQUENCY: Monthly
```

---

#### C0-C: Proposal & Contract Generation SOP

**Priority:** P0 — Pre-launch
**Owner:** Ava (drafts all documents) + Cem (reviews + signs)
**Purpose:** Remove friction between verbal agreement and signed contract

```
TRIGGER: Cem says "go" after debrief call — client verbally agreed to proceed

STEP 1: PROPOSAL DRAFT (within 2 hrs — Ava executes)
  Ava generates engagement proposal from debrief call notes:
    - Executive summary (why this engagement)
    - Scope of work (named workflows, deliverables)
    - Timeline (week-by-week milestones)
    - Investment (USD, with breakdown)
    - Payment schedule (50% upfront, 50% on delivery)
    - What's not included (scope boundary)
    - Next steps
  Cem reviews (15 min) → approves or revises

STEP 2: SOW + MSA PACKAGE (Ava attaches to proposal)
  MSA (Master Services Agreement) — standard template, pre-approved by attorney
  SOW (Statement of Work) — customised per engagement scope
  NDA (embedded in MSA)
  Ava assembles package in PandaDoc or DocuSign template

STEP 3: SIGNATURE WORKFLOW
  Ava sends via PandaDoc/DocuSign to client (and Cem)
  Ava monitors signature status; sends one follow-up reminder at 48 hrs if unsigned
  Ava alerts Cem if not signed within 72 hrs

STEP 4: UPON SIGNATURE
  Ava sends invoice for 50% deposit (via QuickBooks or Wave for US invoicing)
  Ava triggers C0-B (Project Kickoff SOP)
  Ava files signed contracts in Google Drive under /Clients/[ClientName]/Legal/

CRITICAL: Do not begin ANY implementation work before:
  1. Contract signed by both parties
  2. 50% deposit received (confirmed in bank account)

REVIEW FREQUENCY: Quarterly (update pricing, terms as market evolves)
```

---

#### C0-D: AI Opportunity Audit Delivery SOP

**Priority:** P0 — Pre-launch (Tier 1 service, needed from Day 1)
**Owner:** Ava (report generation, comms) + Cem (calls + approval)

```
TRIGGER: Audit engagement paid ($997 or $1,997)

STEP 1: AUDIT INTAKE (same as C0-A Steps 1–2 — reuse that flow)

STEP 2: DISCOVERY CALL (Cem — 2 hrs total including prep)
  45-min call, recorded + transcribed

STEP 3: AUDIT REPORT GENERATION (Ava — within 4 hrs of call)
  Template structure:
    EXECUTIVE SUMMARY: 3 bullet wins available, estimated monthly value in USD
    OPPORTUNITY 1: [Name] — Current state, proposed automation, tools needed,
      ROI estimate ($X saved/month or Y hrs/week), implementation complexity (1–5)
    OPPORTUNITY 2: [Same format]
    OPPORTUNITY 3: [Same format]
    QUICK WIN: One thing they can do themselves in <1 week, free or <$50
    IMPLEMENTATION PATHWAY: What it would look like to work with Cem
      (soft intro to Tier 2, not a hard pitch)
    NEXT STEP: "Book 30-min debrief to review findings"
  Cem reviews report (30 min) → approves

STEP 4: DEBRIEF CALL (30 min — Cem)
  Walk through top 2–3 findings
  Present Implementation pathway as natural next step
  If client signals interest: move to C0-C (Proposal SOP)

STEP 5: DELIVERY + FOLLOW-UP
  Ava sends finalised report PDF within 24 hrs of debrief
  Ava sends follow-up email 5 days later if no Implementation decision
  Ava sends final "check-in" 14 days later with relevant case study link

QUALITY GATE:
  Every audit report must include at least one opportunity with:
  → Quantified ROI in USD (minimum: hours/week × implied client hourly rate)
  → Specific tool recommendation with monthly cost
  → Realistic "what this looks like to implement" timeline

REVIEW FREQUENCY: Monthly for first 6 months
```

---

#### C0-E: Case Study Creation SOP

**Priority:** P0 — Build first 4 case studies before first outreach
**Owner:** Ava (primary) + Cem (approval)

```
TRIGGER: (a) Conversion of Ecell project to client-facing IP [first 4 are Ecell-based]
         (b) Post-client engagement completion [all subsequent]

FOR ECELL-BASED CASE STUDIES (first 4):
  STEP 1: Ava reviews corresponding OpenClaw wiki files (Track B Q3 pipeline)
  STEP 2: Ava drafts using US case study format (3-part: case study + guide + quick-ref)
  STEP 3: Cem reviews (30 min) — validates all claims, confirms no sensitive IP exposed
  STEP 4: Ava formats as PDF + blog post version + LinkedIn snippet (3 formats from 1 draft)
  STEP 5: Cem approves → Ava publishes to website blog + LinkedIn

FOR CLIENT-BASED CASE STUDIES (post-engagement):
  STEP 1: At project close, Ava sends client a "Case Study Permission Request" email
    (pre-written template: client can approve full, anonymised, or decline)
  STEP 2: If approved: Ava gathers outcome data from client (brief email survey, 5 questions)
  STEP 3: Ava drafts case study using client data + engagement notes
  STEP 4: Cem reviews → client reviews anonymised version if required → publish

PUBLICATION WORKFLOW (Ava manages):
  1. PDF version → Google Drive /Public/CaseStudies/
  2. Blog post → website (Ava drafts, Cem publishes or Ava publishes if access granted)
  3. LinkedIn post → Ava drafts, Cem posts
  4. Update "Featured Case Studies" section on website

QUALITY GATE:
  Every case study must include:
  → Measurable outcome (time, money, error rate) in USD/hours
  → "Before" state (the pain — relatable to US e-commerce founders)
  → Specific business type (anonymised is fine, but ICP must be identifiable)
  → No technical jargon — tools are "automation software," not "N8N" or "Claude"

REVIEW FREQUENCY: Per project
```

---

### Ecell Operations SOPs — P1 (Immediate, Weeks 1–4)

| # | SOP Title | Purpose | Primary Agent | Ava vs Harry | Review Frequency |
|---|-----------|---------|---------------|--------------|-----------------|
| E1 | **Daily Sales Performance Digest** | Auto-generate morning briefing: revenue by channel, top/bottom SKUs, anomalies vs 7-day average | Harry | **Harry** (BigQuery + all channel data) → delivers to Cem | Monthly |
| E2 | **Inventory Restock Alert SOP** | PO recommendations when SKU days-of-cover falls below threshold; route to Cem for approval above $X | Harry | **Harry** (Zero Fulfillment + inventory data) → Cem approves above threshold | Monthly |
| E3 | **Amazon Account Health Monitoring** | Daily check of ODR, late shipment, cancellation rates across all Amazon marketplaces; alert if approaching threshold | Harry | **Harry** (Amazon SP-API) → escalates to Ava for any comms required | Weekly |
| E4 | **New Listing Generation SOP** | New SKU data → title/bullets/description for all channels → queue for human approval | Ava | **Ava** (strategist/content creator) → Harry receives inventory confirmation | Monthly |
| E5 | **Invoice & Receipt Processing SOP** | Receipt arrives → N8N extracts → categorises → posts to Xero → files | N8N primary | **N8N** executes; **Harry** reviews Xero reconciliation weekly | Quarterly |
| E6 | **Agent Escalation Protocol** | When Ava/Harry must pause and alert Cem: cost thresholds, irreversible actions, ambiguous data, external comms | Both agents | **Ava** escalates via Airweave email/flag; **Harry** escalates via alert | Monthly |
| E7 | **Weekly Agent Health Check SOP** | Review all active agent task logs, failure rates, memory gaps; fix recurring failures | Cem (human) | Ava and Harry each generate their own log summaries for Cem to review | Weekly |
| E8 | **Supplier PO Generation SOP** | Standard process for generating and sending POs; approval thresholds by PO value | Harry | **Harry** (Zero Fulfillment) → Cem approves above threshold | Monthly |

---

### Ecell Operations SOPs — P2 (Month 2–3)

| # | SOP Title | Purpose | Primary Agent | Ava vs Harry |
|---|-----------|---------|---------------|--------------|
| E9 | **Customer Escalation Routing SOP** | Freshdesk tickets above severity threshold → draft response → Cem approves | Ava | **Ava** reads Freshdesk escalation, drafts response via Airweave, Cem approves |
| E10 | **Channel Fee & Margin Monitoring SOP** | Weekly: pull fees from Amazon/eBay/Walmart, calculate net margin by SKU, flag margin-negative SKUs | Harry | **Harry** (BigQuery + channel fee APIs) |
| E11 | **Walmart API Sync SOP** | Daily reconciliation of Walmart inventory + price updates; alert on sync failures | Harry | **Harry** (Walmart API) |
| E12 | **Creative Asset Request SOP** | New image brief generated by AI → queued for Philippines team → QA checklist | Ava | **Ava** (content/strategy) drafts creative brief |
| E13 | **Shopify Store Update SOP** | Batch price changes, new collections, campaign pages | Ava | **Ava** (content/sales) manages Shopify content updates |
| E14 | **Returns & Refunds Processing SOP** | Auto-approve vs manual thresholds; Freshdesk + Xero credit notes | N8N + Harry | **N8N** routes; **Harry** generates Xero credit notes |
| E15 | **Monthly Financial Close SOP** | Xero reconciliation, revenue by entity, intercompany transfers | Harry | **Harry** (Xero integration) generates reconciliation; Cem reviews |
| E16 | **Amazon Advertising Campaign Review SOP** | Weekly: ACoS, TACoS, bid efficiency; recommend bid adjustments | Harry | **Harry** (Amazon Ads API) generates recommendations; Cem approves |

---

### Ecell Operations SOPs — P3 (Month 4–6)

| # | SOP Title | Purpose | Primary Agent |
|---|-----------|---------|---------------|
| E17 | **New License Partnership Evaluation SOP** | Evaluate new IP licensing opportunities | Ava (research) + Cem |
| E18 | **Annual Product Catalogue Refresh SOP** | Retire underperforming SKUs, promote new designs | Ava + Harry |
| E19 | **Multi-Country Tax Compliance SOP** | VAT/sales tax calendar for UK, DE, FR, IT, ES, US; automated reminders | N8N reminders + Harry (Xero) |
| E20 | **Agent Training & Onboarding SOP** | How to introduce a new agent to Ecell context | Cem (defines); Ava (documents) |
| E21 | **Competitor Price Monitoring SOP** | Weekly: sample competitor pricing on top 50 SKUs | Ava (web research) |
| E22 | **Supabase RAG Memory Maintenance SOP** | Monthly: add new playbooks to vector DB, retire outdated content | Ava + Cem |

---

### Consultancy SOPs — P1 (Month 1–2)

| # | SOP Title | Purpose | Owner | Ava vs Harry |
|---|-----------|---------|-------|--------------|
| C1 | **Wiki → IP Conversion SOP (from Q3)** | Weekly Ava-executed harvest, classification, Track A/B/C conversion | Ava (executes) + Cem (triage) | **Ava** fully owns this; Harry has no role |
| C2 | **Client Communication Templates SOP** | Library of standard client emails: kickoff, milestone, invoice reminder, retainer renewal | Ava (maintains + executes via Airweave) | **Ava** owns; Harry has no role |
| C3 | **Prospect Research SOP** | Before every discovery call: research company, identify pain points, prepare Cem briefing | Ava | **Ava** (research + strategy) |
| C4 | **LinkedIn Content Calendar SOP** | 2 posts/week: case study mix + insights; draft + schedule | Ava | **Ava** (content/sales) |

---

### Consultancy SOPs — P2 (Month 2–3)

| # | SOP Title | Purpose | Owner | Ava vs Harry |
|---|-----------|---------|-------|--------------|
| C5 | **Monthly Retainer Report SOP** | Auto-generate monthly client performance report from workflow/agent logs | Ava | **Ava** drafts; Harry may supply Ecell-side analytics if relevant |
| C6 | **Retainer Client Health Check SOP** | Monthly review: is client getting value? Churn risk? Action plan | Cem | **Ava** prepares health check brief; Cem reviews |
| C7 | **Scope Change & Change Order SOP** | When client requests out-of-scope work: evaluation, pricing, CO generation | Cem | **Ava** drafts Change Order document |
| C8 | **Partner Referral Management SOP** | Track US referral partners, fees owed, relationship touchpoints | Cem + Ava | **Ava** tracks and sends relationship touchpoint emails |
| C9 | **Implementation Handover SOP** | At project completion: documentation package, training delivery, knowledge transfer | Ava drafts; Cem delivers | **Ava** (all documentation); Cem delivers training call |

---

### Consultancy SOPs — P3 (Month 4–6)

| # | SOP Title | Purpose | Owner |
|---|-----------|---------|-------|
| C10 | **SaaS Product Specification SOP (Q3 Track C)** | When/how to convert a workflow to SaaS product | Cem + Ava |
| C11 | **Consultancy Financial Review SOP** | Monthly: revenue by client in USD, gross margin by type, pipeline forecast, MRR | Harry (financial data) + Cem (review) |
| C12 | **Client Offboarding SOP** | When client ends: final report, testimonial request, referral ask, keep-warm | Ava |
| C13 | **Template Library Maintenance SOP** | Quarterly review of Track B templates for accuracy + relevance | Ava + Cem |
| C14 | **US Pricing Review SOP** | Semi-annual: review USD pricing vs US market, win/loss rate, value delivered | Cem (uses Ava for market research) |
| C15 | **US Tax & Compliance SOP** | Quarterly: S-Corp Form 941, annual Form 1120-S, E&O renewal, FL annual report | Cem + US CPA (N8N calendar reminders) |

---

### Email Triage SOP — Hybrid N8N + Ava Model (Corrected from V1)

**V1 error:** Proposed building N8N email triage from scratch without acknowledging Ava's existing Airweave email access.

**Corrected hybrid model:**

```
EMAIL ARRIVES AT [consultancy@domain.com] AND/OR [cem@ecellglobal.com]

LAYER 1 — N8N (deterministic, always-on safety net):
  N8N monitors inbox continuously (webhook or polling)
  N8N classifies email by simple pattern matching:
    → Contains tracking number → auto-archive to /Logistics/
    → Contains invoice/receipt keywords → auto-forward to Xero workflow
    → Contains calendar invite → auto-accept if from known domain
    → Matches spam patterns → auto-delete or spam folder
    → Everything else → flag for Ava with category label
  Why N8N first: It never sleeps, never loses context, never gets confused
    by an unusual session. Zero emails dropped even if Ava is blocked.

LAYER 2 — AVA via Airweave (intelligent judgment layer):
  Ava receives N8N-flagged emails with category label
  Ava reads with full business context (SOUL.md, client list, project status)
  Ava classifies into:
    [CONSULTANCY LEAD] → Draft response + notify Cem
    [EXISTING CLIENT] → Draft update/response, send if routine, escalate if unusual
    [ECELL SUPPLIER/PARTNER] → Draft response or route to Harry if financial
    [ECELL CUSTOMER SERVICE] → Draft response, escalate threshold per E6 SOP
    [MEDIA/OPPORTUNITY] → Summarise + present options to Cem
    [ADMIN/FYI] → File and summary only, no action
    [URGENT/UNKNOWN] → Immediate Cem alert

AVA'S AUTONOMOUS SEND THRESHOLD (after first 30 days of supervised operation):
  Ava can send autonomously:
    → Acknowledgment emails ("Thanks for reaching out, Cem will be in touch within 24 hours")
    → Meeting confirmation emails
    → Standard follow-up templates
    → Routine client update emails (pre-approved template content)
  Ava ALWAYS escalates to Cem:
    → Any pricing negotiation or non-standard commercial request
    → Any complaint or dissatisfied client signal
    → Any legal reference (contract dispute, subpoena, regulatory inquiry)
    → Any email from new unknown contact proposing partnership or investment
    → Any email where Ava's confidence in classification is <80%

FALLBACK PROTOCOL (when Ava is blocked, down, or producing low-quality output):
  N8N continues to catch and label all emails
  N8N sends Cem a daily digest of any unprocessed emails
  Cem handles manually until Ava is restored
  Ava does NOT attempt to catch up on a backlog during a bad session —
    Cem reviews backlog manually after restoration

SETUP REQUIREMENTS:
  → Confirm Airweave email access covers consultancy-dedicated email
  → N8N webhook to Airweave endpoint documented in Ava's context
  → Ava has access to current client list, project status, contact database
  → First 30 days: All Ava drafts reviewed by Cem before send
  → Days 31+: Autonomous send for pre-approved template types only

REVIEW FREQUENCY: Monthly — review Ava's email handling log for errors/near-misses
```

---

### Master Priority View — Top 12 by Combined Score

| Rank | SOP | TLS | RUS | Why It's Critical | Build By |
|------|-----|:---:|:---:|-------------------|---------|
| 1 | C0-A: Client Intake & Discovery | 8.5 | 1.0 | Without this, Cem can't take a client professionally. Ava runs 80%. | Day 1–3 |
| 2 | C0-C: Proposal & Contract Gen | 8.0 | 1.0 | No contract = no revenue. Ava drafts, Cem approves in 15 min. | Day 1–3 |
| 3 | C0-D: AI Opportunity Audit Delivery | 8.0 | 1.0 | First product. Must be systematised before first client. Ava runs report. | Day 3–5 |
| 4 | C0-E: Case Study Creation | 7.5 | 1.0 | First 4 case studies = lead gen ammunition. Ava builds from Ecell wiki. | Days 2–7 |
| 5 | E6: Agent Escalation Protocol | 9.0 | 0.3 | Stops Ava/Harry babysitting — frees Cem's time for consulting. Both agents follow this. | Week 1 |
| 6 | E1: Daily Sales Digest | 9.5 | 0.2 | Eliminates 3–5 hrs/week Ecell reporting. Harry owns. | Week 1 |
| 7 | Email Triage: N8N + Ava Hybrid | 8.5 | 0.8 | Ava handles all client comms; frees Cem + enables consultancy comms at scale. | Week 1 |
| 8 | C0-B: Project Kickoff | 7.0 | 0.9 | Needed for first Implementation client. Ava runs onboarding. | Week 2 |
| 9 | E2: Inventory Restock Alerts | 8.5 | 0.1 | Prevents stockouts without daily monitoring. Harry owns. | Week 1–2 |
| 10 | E3: Amazon Account Health | 7.5 | 0.1 | Prevents account suspensions (catastrophic Ecell risk). Harry owns. | Week 1–2 |
| 11 | C1: Wiki → IP Conversion | 7.0 | 0.8 | Ava's weekly harvest creates the ongoing case study pipeline for consultancy. | Week 1–2 |
| 12 | E7: Weekly Agent Health Check | 8.0 | 0.4 | Ava + Harry each generate own logs. Converts reactive babysitting to 20-min weekly review. | Week 2 |

---

### SOP Creation Process (AI-Accelerated, Ava-Assisted)

**Step 1:** Record one real execution (video/audio narration, 10–15 min). Cem narrates: "I'm opening Seller Central, going to Account Health, checking this metric..."

**Step 2:** Feed transcript to Ava: "Convert this process narration into an SOP using the Internal Playbook format. Determine if this belongs to Ava or Harry. Flag any steps I didn't explain clearly as [NEEDS CLARIFICATION]." Ava produces draft in 5–10 min.

**Step 3:** Test with the relevant agent (Ava or Harry). Observe failures. Ava documents her own failures as gap flags in real-time.

**Step 4:** Cem resolves flags. Ava publishes final version to `/playbooks/` folder.

**Total time per SOP:** 1–2 hours for P0/P1 critical SOPs.

**SOP Sprint Plan (Days 1–30):**

| Period | SOPs to Build |
|--------|--------------|
| Days 1–3 | C0-A, C0-C, C0-D (Consultancy pre-launch essentials — Ava drafts all) |
| Days 4–7 | C0-B, C0-E (Project kickoff + first 4 case studies) |
| Week 2 | E1, E6, Email Triage SOP (Ecell autonomy core) |
| Week 2–3 | E2, E3, E7 (Ecell monitoring) |
| Week 3–4 | C1, C2, C4 (Consultancy pipeline) |
| Month 2 | E4, E5, E8 + Consultancy P2 SOPs as clients onboard |

---

## 9. RISK REGISTER (Q6)

*Source: Council Member 3 — Gemini Pro*

The parallel execution of Ecell's automation and a new US AI consultancy under a Florida S-Corp carries significant risks. With EU revenue actively declining, the primary risk is financial survival.

### Financial & Revenue Risks

---

**Risk 1: Revenue Timing Risk (The Survival Threat)**

| Field | Detail |
|-------|--------|
| **Severity** | CRITICAL |
| **Risk** | The consultancy must secure its first paying client by Week 3–4 to offset the accelerating decline in Ecell's EU revenue. If outreach fails or sales cycles stretch to 3 months, the business faces a critical cash flow deficit. |
| **Mitigation** | Do not wait for perfect IP or polished websites. In Week 1, deploy Ava to immediately begin outbound networking on LinkedIn and drafting proposals based on *current* internal Ecell case studies. Price the initial "Audit & Roadmap" package aggressively ($3,000–5,000 USD) to minimise friction and close fast. |
| **Contingency** | Identify the critical survival threshold for Ecell UK. If EU sales drop another 30% before consulting revenue hits, have a pre-planned cost-reduction protocol ready for the UK entity. |
| **Cost** | $0 (process decision) |

---

**Risk 2: EU Revenue Decline Acceleration**

| Field | Detail |
|-------|--------|
| **Severity** | HIGH |
| **Risk** | Ecell's declining EU operations could drain US cash reserves if they slip into unprofitability faster than anticipated, dragging down the US S-Corp's ability to fund the consultancy launch. |
| **Mitigation** | Harry must be tasked with daily margin monitoring of EU ASINs. Implement a strict rule: any EU marketplace channel or product line operating at a net loss for 14 consecutive days must be paused automatically by N8N. |
| **Cost** | ~2–4 hrs Harry configuration |

---

### Operational & Execution Risks

**Risk 3: Parallel Execution Overload (Solo Founder Burnout)**

| Field | Detail |
|-------|--------|
| **Severity** | HIGH |
| **Risk** | Running a declining e-commerce business while simultaneously launching a consultancy guarantees context switching. Solo founders attempting multi-table strategies often fail by spreading efforts too thin. |
| **Mitigation** | Institute ruthless time-boxing. Dedicate specific daily blocks to Ecell (e.g., mornings) and the consultancy (e.g., afternoons). Pause all non-critical development immediately (MIRROR-PRODUCT, POD Analytics). Use a single workspace for both to reduce friction. |
| **Cost** | $0 (management discipline) |

---

**Risk 4: Ava Reliability and Blast Radius**

| Field | Detail |
|-------|--------|
| **Severity** | HIGH |
| **Risk** | Ava operates as the intelligent email triage layer via Airweave. If she experiences a hallucination, memory loss, or gets stuck in a loop, she could send inappropriate responses to key Ecell suppliers or new high-value consulting prospects. |
| **Mitigation** | Implement the hybrid N8N + Ava architecture. N8N acts as the deterministic safety net. Ava should *draft* responses for high-stakes emails but require Cem's one-click approval before sending. Ava must never have direct unilateral send authority for new client proposals or major supplier negotiations. |
| **Cost** | Covered by N8N + Ava hybrid architecture already planned |

---

### Legal & Compliance Risks

**Risk 5: US S-Corp & UK Limited Company Conflict (Cross-Border Tax)**

| Field | Detail |
|-------|--------|
| **Severity** | HIGH |
| **Risk** | Running a US consultancy from a Florida S-Corp while maintaining central management and control of a UK Limited company creates severe cross-border tax risks. The IRS may view the UK company as a Controlled Foreign Corporation (CFC), potentially subjecting Cem to Subpart F or GILTI taxes on undistributed UK profits. Conversely, HMRC could argue the UK entity creates a permanent establishment for the US operations. |
| **Mitigation** | Ensure absolute operational, financial, and digital separation between the US S-Corp and Ecell Global UK. Maintain separate bank accounts, accounting software (Xero instances), and distinct agent roles. Engage a cross-border CPA immediately to model the GILTI exposure and ensure the Florida S-Corp does not accidentally absorb UK tax liabilities. |
| **Cost** | Cross-border CPA consultation fee (one-time) |

---

**Risk 6: Consulting Liability in the US Market**

| Field | Detail |
|-------|--------|
| **Severity** | MEDIUM-HIGH |
| **Risk** | Selling AI automation to US small businesses carries liability. If an agent built for a client makes an expensive mistake (e.g., runaway API costs or data deletion), the Florida S-Corp could be sued. |
| **Mitigation** | All US consulting contracts must include robust Limitation of Liability clauses capping damages at the fees paid. Require clients to sign waivers acknowledging the experimental nature of LLMs. Secure Professional Liability (E&O) insurance tailored for software/AI consultants operating in the US. |
| **Cost** | $75–150/month E&O insurance |

---

### Technology & Security Risks

**Risk 7: OpenClaw Vulnerabilities**

| Field | Detail |
|-------|--------|
| **Severity** | MEDIUM |
| **Risk** | Local agents connected to core business systems are a security risk. A recent vulnerability (CVE-2026-25253) exposed OpenClaw to remote code execution. |
| **Mitigation** | Run Ava and Harry on isolated network segments. Ensure strict API key scoping (least privilege) for BigQuery, Walmart API, and Shopify. Keep OpenClaw updated. |
| **Cost** | Covered by existing IT practices |

---

**Risk 8: Runaway API Costs for 24/7 Agents**

| Field | Detail |
|-------|--------|
| **Severity** | MEDIUM |
| **Risk** | Agents like Harry processing large inventory datasets via BigQuery, or Ava reading high-volume email streams, can spike API costs rapidly if using expensive models (e.g., Opus). |
| **Mitigation** | Set hard spending limits in the Anthropic dashboard. Route routine N8N email triage and standard data processing to Sonnet 3.5 or Haiku; reserve Opus strictly for complex strategic drafting or deep analysis. Budget explicitly per agent (see Section 4 budget table). |
| **Cost** | Covered by budget caps in Section 4 |

---

**Risk 9: Single Point of Failure (Cem)**

| Field | Detail |
|-------|--------|
| **Severity** | HIGH |
| **Risk** | As the sole operator and lead consultant, Cem is the bottleneck. If he is tied up fixing Zero Fulfillment PHP errors, the consulting revenue stream stops. |
| **Mitigation** | Force delegation. If a task requires manual data entry or routine routing, it must be handed to N8N or Harry. Cem must transition purely to high-level strategic oversight and client closing. Pause Zero Fulfillment PHP work — use the Cloud Run modernisation already planned. |
| **Cost** | $0 (management discipline) |

---

**Risk 10: Shared Infrastructure Bleed**

| Field | Detail |
|-------|--------|
| **Severity** | MEDIUM |
| **Risk** | Using the same N8N instance or agent memory layer (Supabase RAG) for both Ecell and the consultancy risks crossing data streams, potentially leaking Ecell supplier data to consulting clients. |
| **Mitigation** | Deploy physically or logically separated infrastructure. Ecell operations and the AI consultancy must run in isolated cloud environments or distinct database schemas. Separate Paperclip companies for each entity (see Section 4). |
| **Cost** | Supabase RLS implementation (~2–4 hrs setup) |

---

### Risk Register Summary

| # | Risk | Severity | Primary Mitigation | Cost |
|---|------|----------|-------------------|------|
| 1 | Revenue timing — consultancy fails to close in Week 3–4 | CRITICAL | Ava outbound Day 1; aggressive audit pricing; do not wait for perfect IP | $0 |
| 2 | EU revenue decline acceleration | HIGH | Harry daily EU margin monitoring; auto-pause loss-making channels at 14 days | 2–4 hrs |
| 3 | Solo founder burnout from parallel execution | HIGH | Time-boxing; pause MIRROR-PRODUCT + POD; Ava absorbs 80% of admin | $0 |
| 4 | Ava blast radius on bad day | HIGH | Hybrid N8N + Ava; Ava drafts only for high-stakes; one-click Cem approval | Covered |
| 5 | Cross-border US/UK tax conflict (GILTI/CFC) | HIGH | Entity separation; cross-border CPA; separate Xero, bank accounts, agent roles | CPA fee |
| 6 | Consulting liability (US client sues) | MED-HIGH | LOL clause at 1x fee; LLM waivers; E&O insurance bound before first call | $75–150/mo |
| 7 | OpenClaw vulnerability | MEDIUM | Isolated network segments; least-privilege API keys; keep updated | $0 |
| 8 | Runaway API costs | MEDIUM | Hard spending limits per agent; Haiku for routine tasks; budget caps | $0 |
| 9 | Cem as single point of failure | HIGH | Delegation to N8N/Harry; pause legacy PHP work; Cem = strategic only | $0 |
| 10 | Shared infrastructure data bleed | MEDIUM | Supabase RLS schema separation; separate Paperclip companies | 2–4 hrs |

---

## 10. 90-DAY IMPLEMENTATION TIMELINE (Q7)

*Source: Council Member 3 — Gemini Pro*

**Objective:** Secure consulting revenue within 4 weeks (Survival Goal) while simultaneously reducing Ecell operations to <10 hours/week.

**Constraint:** No week can add net hours to Cem's workload. Parallel execution is mandatory.

**Legend:** [Track A] = Ecell Autonomy | [Track B] = AI Consultancy Revenue

---

### Month 1: The Revenue Sprint & Rapid Triage (Weeks 1–4)

*Goal: Stop the bleeding, automate Ecell intake, and sign the first consulting client.*

---

#### Week 1: Immediate Relief & Go-to-Market Prep

| Track | Actions | Owner | Net Hours Impact |
|-------|---------|-------|-----------------|
| **[Track A] Triage & Stop** | Pause MIRROR-PRODUCT, POD Dashboard, and all non-urgent SOP creation | Cem | **-10 hrs** |
| **[Track A] Agent Deployment** | Activate hybrid N8N + Ava email triage via Airweave. N8N handles deterministic routing (receipts → Xero, tracking → archive). Ava drafts responses for supplier/customer exceptions. | Ava + N8N | **-5 hrs** |
| **[Track B] Offer Creation** | Package Ecell's internal automation success into a US-focused "Audit & Implementation" offering ($3k–$5k USD). Target market: Florida/US e-commerce SMBs. | Cem + Ava | **0 hrs (offset by Track A savings)** |

**Decision Gate:** Are you doing this? If not, explain why before moving to Week 2.

---

#### Week 2: Outbound Motion & Ecell Handoff

| Track | Actions | Owner | Net Hours Impact |
|-------|---------|-------|-----------------|
| **[Track A] Financial Ops** | Harry assumes daily BigQuery/Walmart/Shopify inventory syncing and basic Xero reconciliation. Cem only reviews anomalies. | Harry | **-5 hrs** |
| **[Track B] Lead Generation** | Ava begins aggressive outbound prospecting on LinkedIn targeting US SMB founders. Case studies (Ecell's N8N automation) go live on website. | Ava | **0 hrs** |
| **[Track B] Local Network** | Cem attends OCOC Business Social (April 2, 2026). SBDC UCF introduction email sent. | Cem | **+2 hrs (offset by Track A savings)** |

---

#### Week 3: First Client Proposals & Core System Migration

| Track | Actions | Owner | Net Hours Impact |
|-------|---------|-------|-----------------|
| **[Track A] Tech Debt** | Deploy Zero Fulfillment JSON/Cloud Run modernisation to stabilise core Ecell backend and reduce routing errors. | Cem + Harry | **-3 hrs (once live)** |
| **[Track B] Sales** | Cem conducts initial discovery calls booked by Ava. Send first proposals. | Cem | **0 hrs (offset)** |
| **[Track B] Follow-up** | Ava handles all post-call follow-ups, report drafting, proposal generation | Ava | **0 hrs** |

---

#### Week 4: DECISION GATE 1 — Revenue Check

| Track | Actions | Owner |
|-------|---------|-------|
| **[Track A] Review** | Are Ecell operations taking <15 hours/week? If not, refine Ava's email SOPs and Harry's inventory scripts. | Cem |
| **[Track B] The Close** | **TARGET: First paying client signed. Initial invoice paid into US S-Corp account.** | Cem |

**Decision Gate 1 Rule:** If no client is signed, aggressively discount the initial audit OR pivot the outreach messaging. Do not advance to Month 2 consulting expansion without initial validation. If needed, offer a free 20-min assessment at local Orlando events to generate trial closes.

---

### Month 2: Delivery & Ecell Optimization (Weeks 5–8)

*Goal: Deliver results for Client 1 while pushing Ecell to exception-only mode.*

---

#### Week 5: Parallel Delivery & Listing Automation

| Track | Actions | Owner | Net Hours Impact |
|-------|---------|-------|-----------------|
| **[Track A] Growth** | Deploy V1 of Multi-Channel Feed Engine to automate listing creation across US marketplaces. | Harry + Cem | **-4 hrs** |
| **[Track B] Client 1 Onboarding** | Begin implementation of Client 1's automation. Use isolated, dedicated infrastructure — do not mix with Ecell's stack. | Cem | **0 hrs** |

---

#### Week 6: RAG Memory & Scaling Outreach

| Track | Actions | Owner | Net Hours Impact |
|-------|---------|-------|-----------------|
| **[Track A] Stabilisation** | Implement Supabase RAG memory for Ava and Harry — moving from static Markdown files to persistent memory. | Cem + Ava | **+3 hrs (one-time setup)** |
| **[Track B] Sales Engine** | With Client 1 underway, Ava resumes outbound prospecting to fill pipeline for Client 2. | Ava | **0 hrs** |

---

#### Week 7: Productisation

| Track | Actions | Owner |
|-------|---------|-------|
| **[Track A] Hands-off** | Implement strict exception-based alerting via Slack/N8N for Ecell. Cem only intervenes if an alert fires. | N8N + Harry |
| **[Track B] IP Refinement** | Turn the workflows built for Client 1 into a repeatable template. Refine the USD pricing model based on actual hours/API costs incurred. | Cem + Ava |

---

#### Week 8: DECISION GATE 2 — Sustainability

| Track | Review Question | Decision Rule |
|-------|----------------|---------------|
| **[Track A]** | Is Ecell operating at <10 hours/week? | If not: identify the specific SOPs still blocking autonomy and prioritise them |
| **[Track B]** | Is the consultancy generating sufficient cash flow to offset EU revenue decline? | If yes: formalise the retainer model. If not: increase outbound volume; consider secondary contractor for Client 1 delivery. |

---

### Month 3: Scale and Retainers (Weeks 9–12)

*Goal: Secure MRR and fully abstract Cem from Ecell daily operations.*

---

#### Weeks 9–10: Securing MRR

| Track | Actions | Owner |
|-------|---------|-------|
| **[Track A] Monitor** | Harry completely manages Ecell inventory and finance reporting. Cem reviews weekly digest only. | Harry |
| **[Track B] Retainers** | Transition Client 1 from the initial build phase to a monthly "AI Ops" retainer ($1,000–2,000/mo) for ongoing monitoring and updates. | Cem + Ava |

---

#### Weeks 11–12: Pipeline Expansion & DECISION GATE 3

| Track | Actions | Owner |
|-------|---------|-------|
| **[Track A] Final Review** | Ecell operations must be fully maintained by Ava, Harry, and N8N. Cem at <10 hrs/week. | All agents |
| **[Track B] Scale** | Sign Client 2 and Client 3 using productised SOPs developed from Client 1. | Cem + Ava |

**Decision Gate 3:** Assess the dual-track strategy. Can the US S-Corp sustain Cem's income requirements indefinitely? If yes: formalise the consultancy as the primary focus and treat Ecell Global UK as a managed asset. If no: reassess scope and cost structure of Ecell UK.

---

### 90-Day Timeline Summary

| Period | Track A Target | Track B Target | Cumulative Hours Freed | Revenue Target |
|--------|---------------|---------------|----------------------|----------------|
| Week 1 | Email triage live; MIRROR-PRODUCT paused | Offer packaged; website 50% | 15 hrs/week | $0 |
| Week 2 | Harry on finance/inventory | Website live; 30 prospects in Ava's pipeline | 20 hrs/week | $0 |
| Week 3 | Zero Fulfillment stable | First discovery calls | 23 hrs/week | $0 |
| Week 4 | Ecell at ~15 hrs/week | **First client signed** | 25 hrs/week | **$997–1,997** |
| Month 2 | Feed Engine live; Supabase RAG | Client 1 delivery + retainer offer | 30 hrs/week | $4,000–8,000 |
| Month 3 | Ecell at <10 hrs/week | Client 2–3 signed; MRR established | 35 hrs/week | $6,000–12,000 |

---

## 11. APPENDIX: ACTION ITEMS MASTER LIST

*Source: Consolidated from all council reports*

### Days 1–3 (Pre-Revenue Critical)

| Priority | Action | Owner | Est. Hours | Cost (USD) | Due |
|----------|--------|-------|-----------|-----------|-----|
| 1 | Bind E&O Professional Liability Insurance (Next Insurance or Hiscox USA — online, same-day) | Cem | 0.5 hrs | $75–150/mo | Day 1 |
| 2 | Register .com domain for consultancy brand (decide name — 10-min decision) | Cem | 0.25 hrs | $12–15/year | Day 1 |
| 3 | RSVP to OCOC Business Social (April 2, 2026) — email smatthews@myococ.com | Cem | 5 min | $0 | Day 1 |
| 4 | Pause MIRROR-PRODUCT and POD Analytics Dashboard development | Cem | 15 min | $0 | Day 1 |
| 5 | Block Cem's calendar: minimum 15 hrs/week for consulting work | Cem | 30 min | $0 | Day 1 |
| 6 | Route all business email through N8N first — set up Gmail intake workflow | N8N/Cem | 4–6 hrs | $0 | Day 1–3 |
| 7 | Create deterministic N8N rules: receipts → Xero, tracking → archive, spam → delete | N8N/Cem | 2–3 hrs | $0 | Day 2–3 |
| 8 | Define Ava triage packet schema and configure N8N → Ava handoff | Cem + Ava | 2–3 hrs | $0 | Day 2–3 |
| 9 | Enforce Harry's domain boundary: finance/inventory/orders only | Cem | 1 hr | $0 | Day 2 |
| 10 | Ava drafts MSA + SOW + NDA templates (US law, Florida jurisdiction) | Ava (drafts) + Cem (reviews) | 1 hr (Ava) + 0.5 hr (Cem) | $0 → $500–800 attorney review | Days 1–2 |
| 11 | Build C0 SOP stack (Ava generates drafts for C0-A, C0-B, C0-C, C0-D, C0-E) | Ava (drafts) + Cem (reviews) | 3 hrs total | $0 | Days 1–3 |
| 12 | Set up US invoicing (QuickBooks Simple Start $30/mo or Wave free) under US S-Corp | Cem | 1 hr | $0–30/mo | Day 3 |

### Days 4–7 (First Week Completion)

| Priority | Action | Owner | Est. Hours | Cost (USD) | Due |
|----------|--------|-------|-----------|-----------|-----|
| 13 | Build Framer website with 5 pages + Calendly embed + USD pricing | Cem + Ava (copy) | 4–6 hrs | $20/mo Framer | Days 2–5 |
| 14 | Update LinkedIn profile to "AI Automation Consultant \| Orlando, FL" + consultancy website link | Cem | 0.5 hrs | $0 | Day 2 |
| 15 | Join Innovate Orlando (free startup tier) — innovateorlando.io | Cem | 0.25 hrs | $0 | Day 2 |
| 16 | Ava builds first 4 US case studies from Ecell projects (Q3 Track B) | Ava (drafts) + Cem (approves) | 3 hrs | $0 | Days 3–7 |
| 17 | Ava drafts first consulting offer, outbound email variants, and US outreach list | Ava | 2 hrs | $0 | Days 4–7 |
| 18 | Prepare one-page "what we did inside Ecell" proof sheet for prospects | Cem + Ava | 1 hr | $0 | Days 4–7 |
| 19 | Start daily founder digest (approvals, financial anomalies, customer-risk, consulting opportunities) | N8N + Ava | 2–4 hrs setup | $0 | Day 4 |
| 20 | Set hard escalation rules for Ava (see SOP-6 list) | Cem | 1 hr | $0 | Day 4 |

### Week 2 (Launch)

| Priority | Action | Owner | Est. Hours | Cost (USD) | Due |
|----------|--------|-------|-----------|-----------|-----|
| 21 | Website live + Calendly live | Cem | — | $0 | Week 2 |
| 22 | Ava begins 30-prospect LinkedIn research list (US e-commerce founders) | Ava | 2 hrs | $0 | Days 5–7 |
| 23 | Send first 10 LinkedIn outreach messages (Ava-drafted, Cem-approved) | Cem | 1 hr | $0 | Days 7–10 |
| 24 | Florida SBDC at UCF — introduction email + schedule meeting | Cem | 0.5 hrs | $0 | Week 2 |
| 25 | Launch Supabase memory: approved SOPs, contacts, escalation rules only | Cem + Hermes | 8–14 hrs | $25–75/mo | Week 2 |
| 26 | Hermes begins summarising resolved cases into reusable patterns | Hermes | 6–10 hrs | $80/mo | Week 2 |
| 27 | Harry on top 20% revenue-driving SKUs/orders/issues only | Harry | — | $120/mo | Week 2 |
| 28 | Confirm with US CPA: S-Corp reasonable salary + consulting services tax treatment | Cem | 1 hr | CPA fee | Week 1 |
| 29 | Engage cross-border CPA to model GILTI exposure and entity separation | Cem | 1 hr | CPA fee | Week 2 |
| 30 | First Reddit/community posts (Ava drafts, Cem posts — no pitch, genuine value) | Cem + Ava | 1 hr | $0 | Week 2 |

### Week 3 (First Revenue)

| Priority | Action | Owner | Due |
|----------|--------|-------|-----|
| 31 | Book 2–4 discovery calls (Ava outbound + OCOC event April 2) | Cem + Ava | Week 3 |
| 32 | Ava preps research briefings for each discovery call prospect | Ava | Before each call |
| 33 | Cem delivers first discovery call; records transcript | Cem | Week 3 |
| 34 | Ava generates first Opportunity Report from transcript | Ava | Within 2 hrs of call |
| 35 | Close first Audit engagement ($997–1,997) | Cem | Week 3–4 |
| 36 | Measure Ava autonomous triage success rate and rework rate | Cem | Week 3 |
| 37 | Tighten or expand N8N rules based on Ava performance data | Cem | Week 3 |

### Week 4 (First Client Signed)

| Priority | Action | Owner | Due |
|----------|--------|-------|-----|
| 38 | Add Paperclip in shadow mode for budget logging, audit, escalation visibility | Cem | Week 4 |
| 39 | Split Ecell governance and consultancy governance into separate Paperclip companies | Cem | Week 4 |
| 40 | Deliver first Audit; debrief call; upsell to Implementation | Cem + Ava | Week 4 |
| 41 | Push for first paid consulting pilot (Orlando/Florida/US SMB — email/process automation as entry offer) | Cem | Week 4 |

---

### Cross-Question Dependency Map

```
DAY 1–3:
  C0 SOPs (Ava drafts) → Legal docs (Ava drafts, attorney reviews) →
  US S-Corp confirmed operational for consulting → E&O insurance bound

DAYS 4–7:
  Q3 Track B activated → First 4 US case studies built by Ava →
  Website launch with case studies live → LinkedIn profile updated

WEEK 2:
  E6 + E1 Ecell SOPs → Harry activated for daily digest →
  Cem's Ecell time begins dropping → Freed hours redirected to consultancy
  LinkedIn outreach begins (Ava builds prospect list) → Discovery calls booked

WEEK 3–4:
  First discovery call → Ava prepares brief → Cem delivers call →
  Ava generates Opportunity Report → First Audit sold ($997–1,997)

MONTH 2:
  Audit converts to Implementation → First $3,000–8,000 revenue →
  Ava handles all client comms via Airweave → Retainer conversation begins
  Ecell running <15 hrs/week (Harry + N8N + Ava covering operations)

ONGOING:
  Q3 wiki harvest (Ava, weekly) feeds Q5 case study library
  feeds Q8 SOP refinements
```

**Single biggest dependency:** Ava's effectiveness as the consultancy engine depends on her being briefed with up-to-date context (SOUL.md + current client list) at each session. Cem must maintain Ava's context document as a living file — 10 minutes per week maximum if structured properly.

---

### Blockers Requiring Cem's Input (Action Required Before Day 3)

| # | Blocker | Action Needed | Deadline |
|---|---------|---------------|---------|
| 1 | Ava's consultancy email access | Confirm which email address Ava's Airweave access covers. If it's only Ecell operations email, a consultancy-dedicated email must be added to Airweave before Ava can handle client comms. | Day 1 |
| 2 | US S-Corp CPA confirmation | Before first US invoice, confirm with US CPA that the S-Corp is current on reasonable salary requirements and consulting services are properly categorised. | Week 1 |
| 3 | Discovery call recording tool | Confirm Ava can receive and process call transcripts from Fireflies.ai or Otter.ai. If not, define the manual transcript-to-Ava workflow. | Day 3 |
| 4 | Domain decision | Which brand name for the consultancy website? 10-minute decision from Cem required before Day 1 website work begins. Options: `ecellai.com`, `ecell-ai.com`, `[cemname]ai.com` | Day 1 |
| 5 | Attorney for MSA review | Identify a US business attorney for one-time MSA review ($500–800). Florida Bar referral service or Clerky/Cooley GO for tech consultant templates. | Week 2 |

---

### Days 1–14 Investment Summary

| Category | Amount (USD) |
|----------|-------------|
| E&O Insurance (first month) | $75–150 |
| Domain registration | $12–15 (one-time) |
| Framer website (first month) | $20 |
| Attorney MSA review | $500–800 (one-time) |
| CPA consultation | varies (existing relationship) |
| US invoicing tool | $0–30/mo (Wave free or QuickBooks) |
| **Days 1–14 hard costs total** | **~$650–1,500** |
| **Revenue unlocked by Day 28 (if first client closes)** | **$997–8,000** |
| **Days 1–14 total Cem time** | **~18 hours** |

---

## COUNCIL MEMBER ATTRIBUTION

| Section | Primary Source | Supporting Sources |
|---------|---------------|-------------------|
| What Changed from V1 | Scope Document V2 (llm-council-scope-v2.md) | — |
| Council Consensus Summary | Cross-council synthesis | All three members |
| Ecell Autonomy Roadmap (Q1) | Council Member 1 — GPT-5.4 | — |
| Agent Architecture SOP (Q2) | Council Member 1 — GPT-5.4 | — |
| Email Triage System (Q4) | Council Member 1 — GPT-5.4 | Council Member 2 — Claude Sonnet (Email Triage SOP section) |
| Wiki → IP Conversion (Q3) | Council Member 2 — Claude Sonnet | — |
| AI Consultancy Launch (Q5) | Council Member 2 — Claude Sonnet | Council Member 3 — Gemini Pro (market urgency framing) |
| Master SOP Library (Q8) | Council Member 2 — Claude Sonnet | — |
| Risk Register (Q6) | Council Member 3 — Gemini Pro | — |
| 90-Day Timeline (Q7) | Council Member 3 — Gemini Pro | Council Member 1 — GPT-5.4 (weekly structure) |
| Action Items Master List | Consolidated from all three members | — |

---

---

# SECTION 12: HERMES AGENT — HOW IT FITS YOUR STACK AND HOW TO USE IT

Source: Supplementary research — Hermes Agent documentation, migration guides, and community usage patterns (March 2026)

## 12.1 Why Hermes Solves Your Specific Pain Points

You described three core problems with OpenClaw: memory loss, constant coaching, and quality variance. Hermes Agent was built specifically to address these:

| Your Pain Point | OpenClaw (Current) | Hermes Agent (Solution) |
|---|---|---|
| Memory loss — agents forget SOPs | File-based SOUL.md/MEMORY.md. Lossy. Requires manual re-coaching. | 3-layer persistent memory: session + persistent facts + skill documents. FTS5 full-text search across all past sessions. |
| Constant coaching | Static config. You teach it once, it forgets. You teach it again. | Closed learning loop: when Hermes solves a hard problem, it writes a skill document automatically. Next time, it loads that skill. Gets smarter through use. |
| Quality variance | Output quality depends on how well the current session "remembers" context | Honcho dialectic user modeling — builds a profile of your preferences, decision patterns, and communication style across sessions. Stops asking questions it already knows the answer to. |
| Blockers / getting stuck | Manual intervention to unstick | Built-in retry logic, provider fallback chains (if one LLM fails, falls back to another), and subagent delegation for parallel work |

## 12.2 Where Hermes Fits in Your Architecture

Hermes does NOT replace Ava or Harry. It takes a specific role:

```
CEM (Strategic decisions only)
│
├── Ava (Mac Studio) — Strategist, Content, Sales, Email Triage via Airweave
│   KEEPS: All current responsibilities. She's your front-of-house.
│
├── Harry (iMac) — Finance, Inventory, Orders
│   KEEPS: BigQuery, Walmart API, Xero, Shopify. He's your back-office.
│
├── Hermes Agent (NEW — $5/mo VPS or Modal serverless)
│   ROLE: Operations Librarian + SOP Learning Engine + Memory Consolidation
│   - Learns from Ava and Harry's completed tasks
│   - Condenses resolutions into reusable skill documents
│   - Maintains Supabase RAG memory (proposes additions, you approve policy)
│   - Handles structured, repetitive tasks that benefit from compounding skill
│   - Runs cron jobs for monitoring and reporting
│   - Backup triage when Ava is down
│
├── N8N — Deterministic routing, invoice automation, email intake
│
└── Paperclip (Week 4+) — Governance, budgets, audit trail
```

### What Hermes Should Own (Start Here)

| Task | Why Hermes (Not Ava/Harry) | Benefit Over Time |
|---|---|---|
| SOP documentation and maintenance | Self-improving skills mean SOPs get better with each use | After 30 days, Hermes knows your SOPs better than any file |
| Competitor price monitoring | Repetitive, structured, benefits from pattern memory | Learns what "significant" price changes look like for your business |
| Customer service pattern extraction | Reads Freshdesk tickets, extracts patterns, creates response templates | Response quality improves as skill library grows |
| Daily sales digest generation | Structured report from BigQuery data | Learns your preferred format, metrics, and anomaly thresholds |
| Wiki-to-playbook conversion (Q3 Track A) | Weekly harvest, classification, conversion | Gets faster and more accurate at classification with each cycle |
| Listing quality audit | Checks listings against your quality standards | Builds a skill for each marketplace's requirements |
| Meeting prep / research briefs | Research + summarization for consulting calls | Learns your briefing format and what you consider relevant |

### What Hermes Should NOT Own

- Email triage (Ava owns this via Airweave — she has the relationship context)
- Client-facing communications (Ava owns — brand voice and sales judgment)
- Financial transactions or PO approvals (Harry + Cem approval)
- Anything requiring real-time messaging integration with clients/suppliers

## 12.3 How to Install Hermes Agent

### Option A: $5/month VPS (Recommended for Always-On)

Based on the [official quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart/) and [community setup guides](https://www.youtube.com/watch?v=tm4h8dG-xlI):

```bash
# 1. Rent a VPS ($5/mo — DigitalOcean, Hetzner, or Vultr)
# 2. SSH into your server
ssh root@your-vps-ip

# 3. Install Hermes (one command)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 4. Run setup wizard
hermes setup
# Choose: LLM provider (OpenRouter recommended for flexibility)
# Choose: Terminal backend (local)
# Choose: Messaging (Telegram for mobile access)

# 5. Start chatting
hermes

# 6. Connect Telegram for mobile access
hermes gateway
# Follow prompts to add Telegram bot token
# Restrict access to your user ID only

# 7. Run gateway as a service (24/7)
sudo systemctl enable hermes-gateway
sudo systemctl start hermes-gateway
```

### Option B: Serverless (Modal — Pay Only When Active)

Hermes supports [Modal](https://modal.com) as a terminal backend. Your environment hibernates when idle, costing nearly nothing. Good if you don't need 24/7 availability.

```bash
# Install locally first
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
# When asked for terminal backend, choose "modal"
```

### Option C: Run Locally on Existing Hardware

You already have a Mac Studio (Ava) and iMac (Harry). You could run Hermes on the same Mac Studio — it's lightweight. But this means Hermes is down when the Mac Studio is off.

```bash
# Install on Mac Studio alongside Ava
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
```

### LLM Provider Choice

| Provider | Best For | Cost |
|---|---|---|
| OpenRouter | Flexibility — route to Claude, GPT, DeepSeek, Gemini, or open models | Pay-per-token, varies by model |
| Anthropic (Claude) | Best quality for SOP writing and analysis | $3/$15 per M tokens (Sonnet) |
| Nous Portal | Native Hermes models, subscription-based | Subscription |
| Ollama (local) | Zero API cost, full privacy | Free (needs 16GB+ RAM, GPU recommended) |

Recommendation: Start with **OpenRouter** so you can switch models without reconfiguring. Use Claude Sonnet for SOP/analysis tasks, cheaper models for monitoring/cron.

## 12.4 Migrate from OpenClaw (If You Want to Move Tasks)

Hermes has an official migration path from OpenClaw via [`hermes claw migrate`](https://hermes-agent.nousresearch.com/docs/guides/migrate-from-openclaw):

```bash
# Preview what would happen (no files changed)
hermes claw migrate --dry-run

# Run migration (imports SOUL.md, MEMORY.md, skills, MCP servers, provider config)
hermes claw migrate --preset full
```

What gets migrated automatically:

| OpenClaw Source | Hermes Destination |
|---|---|
| `SOUL.md` (persona) | `~/.hermes/SOUL.md` |
| `MEMORY.md` (long-term memory) | `~/.hermes/memories/MEMORY.md` (parsed, merged, deduped) |
| `USER.md` (user profile) | `~/.hermes/memories/USER.md` |
| Daily memory files | Merged into main memory |
| Skills (all 4 sources) | `~/.hermes/skills/openclaw-imports/` |
| MCP server configs | `config.yaml` MCP section |
| Model/provider settings | `config.yaml` model section |
| Telegram/Discord/Slack tokens | `.env` file |
| Session reset policies | `config.yaml` session section |
| Cron jobs | Archived — recreate with `hermes cron create` |

What needs manual attention after migration:
- Cron jobs must be recreated (`hermes cron create`)
- WhatsApp needs re-pairing via QR code
- Any OpenClaw plugins need to be converted to Hermes skills or MCP servers
- Review archived files at `~/.hermes/migration/openclaw/<timestamp>/archive/`

**Important:** You are NOT migrating Ava or Harry to Hermes. They stay on OpenClaw. You're deploying Hermes as a NEW third agent with a different role. If you ever want to migrate specific skills or memory from Ava/Harry to Hermes, use `--source` to point at their OpenClaw directories selectively.

## 12.5 The Skill System — Why This Changes Everything

This is the core differentiator from OpenClaw. When Hermes completes a complex task, it doesn't just finish and move on. It synthesizes the approach into a **skill document** — a searchable markdown file stored in the [agentskills.io](https://agentskills.io) format.

```
~/.hermes/skills/
├── ecell-ops/
│   ├── daily-sales-digest/
│   │   └── SKILL.md          # How to pull BigQuery data and format the morning report
│   ├── competitor-price-check/
│   │   └── SKILL.md          # How to check competitor pricing on top 50 SKUs
│   └── listing-quality-audit/
│       └── SKILL.md          # Quality standards per marketplace
├── consultancy/
│   ├── audit-report-generation/
│   │   └── SKILL.md          # How to generate the AI Opportunity Report
│   ├── proposal-writing/
│   │   └── SKILL.md          # SOW/MSA generation patterns
│   └── case-study-creation/
│       └── SKILL.md          # Track B conversion format
└── openclaw-imports/
    └── [migrated from Ava/Harry if needed]
```

The agent manages these via the `skill_manage` tool:

| Action | What It Does |
|---|---|
| `create` | Agent builds a new skill from a successfully completed task |
| `patch` | Agent improves an existing skill based on new experience |
| `edit` | Major rewrite when approach fundamentally changes |
| `delete` | Remove an outdated skill |

**The compounding effect:** Week 1, Hermes takes 20 minutes to generate your sales digest because it's figuring out the format. Week 4, it takes 2 minutes because it loads the skill and just executes. By Month 3, Hermes has a custom skill library specifically tuned to your business — something no other agent framework provides.

## 12.6 Practical Setup — Your First Week with Hermes

### Day 1: Install and Configure

```bash
# Install on a $5 VPS
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup  # Choose OpenRouter, local backend, Telegram

# Connect Telegram (so you can message Hermes from your phone)
hermes gateway
# Add bot token, restrict to your user ID
```

### Day 2: Feed It Your Business Context

Create a context file that Hermes loads every session:

```bash
# Create ~/.hermes/SOUL.md
cat << 'EOF' > ~/.hermes/SOUL.md
You are the Operations Librarian and SOP Learning Engine for Ecell Global.

Your role:
- Learn and document operational patterns from completed tasks
- Maintain and improve the SOP library
- Generate daily/weekly reports from structured data
- Monitor competitors, listings, and marketplace health
- Support the AI consultancy by creating case studies and maintaining playbooks

You do NOT:
- Send emails to clients or suppliers (Ava handles all communications)
- Execute financial transactions (Harry handles finance)
- Make autonomous decisions about inventory or pricing (Harry + Cem)

Escalate to Cem when:
- A pattern suggests a significant business risk
- An SOP needs policy-level changes
- A skill document contradicts existing business rules

Business context:
- Ecell Global: licensed tech accessories, 200K+ SKUs
- Channels: Amazon (US/UK/DE/FR/IT/ES), eBay, Walmart, Shopify
- Other agents: Ava (strategist/sales/email), Harry (finance/inventory)
- Supabase: shared memory layer (when deployed)
EOF
```

### Day 3: First Task — Daily Sales Digest

Message Hermes via Telegram:

> "I need you to create a daily sales digest. Here's how I want it: pull yesterday's revenue by channel from BigQuery, compare to 7-day average, flag any channel that's down more than 15%, list top 5 and bottom 5 SKUs by revenue. Format as a clean summary I can read in 2 minutes. Schedule this to run every morning at 7am ET and send to me on Telegram."

Hermes will:
1. Execute the task
2. Create a skill document capturing the approach
3. Set up a cron job: `hermes cron create`
4. Next morning, load the skill and execute faster

### Day 4-5: SOP Harvesting

Message Hermes:

> "I'm going to share my OpenClaw wiki project files with you. For each one, I want you to: (1) classify it as Internal Playbook, Client Template, or SaaS Spec candidate, (2) convert Internal Playbooks into your skill format so you can execute them, (3) flag anything that needs my review. Start with these files: [share the wiki markdown files]"

Hermes will read the files, create skills from them, and start building the procedural memory that makes it more useful every day.

### Day 6-7: Competitor Monitoring

> "Set up a weekly competitor price check on our top 50 SKUs across Amazon US and UK. Compare against our current pricing. Alert me on Telegram if any competitor is more than 15% below our price. Run every Monday at 9am."

## 12.7 Hermes Cron — Scheduled Automations

Hermes has built-in cron support (like OpenClaw's Heartbeat, but more flexible):

```bash
# Create a scheduled task via natural language
hermes cron create "Every weekday at 7am ET, generate and send my daily sales digest to Telegram"

# Or via CLI
hermes cron create --schedule "0 11 * * 1-5" --task "Generate daily sales digest" --platform telegram

# List active crons
hermes cron list

# Delete a cron
hermes cron delete <id>
```

Recommended cron schedule for your setup:

| Schedule | Task | Platform |
|---|---|---|
| Weekdays 7:00 AM ET | Daily sales digest | Telegram |
| Mondays 9:00 AM ET | Competitor price check (top 50 SKUs) | Telegram |
| Fridays 4:00 PM ET | Weekly SOP review (flag stale skills) | Telegram |
| Daily 8:00 PM ET | Summarize Ava/Harry's completed tasks, extract learning | Internal (skill creation) |
| 1st of month 9:00 AM ET | Monthly consultancy pipeline report | Telegram |

## 12.8 Connecting Hermes to Your Stack via MCP

Hermes supports MCP natively. You can connect it to the same tools Ava and Harry use:

```yaml
# In ~/.hermes/config.yaml
mcp_servers:
  supabase:
    command: "npx"
    args: ["-y", "@supabase/mcp-server"]
    env:
      SUPABASE_URL: "your-supabase-url"
      SUPABASE_KEY: "your-supabase-key"
  
  # If you want Hermes to read from BigQuery (read-only)
  bigquery:
    command: "npx"
    args: ["-y", "@google-cloud/mcp-server-bigquery"]
    env:
      GOOGLE_PROJECT_ID: "your-project-id"
```

## 12.9 Cost Estimate

| Item | Monthly Cost |
|---|---|
| VPS (DigitalOcean/Hetzner) | $5-10 |
| LLM tokens via OpenRouter (moderate usage) | $30-80 |
| Supabase (free tier to start) | $0-25 |
| **Total** | **$35-115/month** |

Compare to the cost of your time re-coaching Ava and Harry: if Hermes saves you 5 hours/week of SOP coaching, that's worth $500+/week at consulting rates.

## 12.10 Timeline for Hermes Deployment

| When | Action | Effort |
|---|---|---|
| Week 2, Day 1 | Install Hermes on $5 VPS, configure OpenRouter + Telegram | 1-2 hours |
| Week 2, Day 2 | Write SOUL.md, feed business context | 1 hour |
| Week 2, Day 3 | First task: daily sales digest with cron | 30 min |
| Week 2, Day 4-5 | Feed OpenClaw wiki files, start SOP harvesting | 2-3 hours |
| Week 3 | Add competitor monitoring cron, listing quality audit skill | 1-2 hours |
| Week 4 | Connect to Supabase MCP (when RAG is deployed) | 2-3 hours |
| Month 2+ | Hermes skill library is compounding — less and less coaching needed | Decreasing |

**Total initial setup: ~8-12 hours across Week 2.**

After that, Hermes requires less attention each week as its skill library grows. That's the entire point — it's the one agent that gets less needy over time, not more.

---

*Playbook compiled: March 30, 2026*
*Version: V2 FINAL — Revenue-Urgent Edition*
*Next review: April 30, 2026 (after first client signed)*
*Maintained by: Ava (Mac Studio) — updates to be committed to OpenClaw wiki on Cem's approval*
