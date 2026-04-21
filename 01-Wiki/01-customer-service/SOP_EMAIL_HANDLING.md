# SOP: Customer Service Email Handling
*Version: DRAFT 0.1 | Created: 2026-02-11 | Status: IN DEVELOPMENT*

---

## Purpose
Standard operating procedure for AI-assisted customer service email handling across all channels.

---

## Scope
- Website email (headcasedesigns@ecellglobal.com)
- eBay messaging (4 stores)
- Amazon messaging (15 marketplaces)

---

## Current Process (Manual)
1. CS staff checks each email inbox manually
2. Reads customer email
3. Looks up order in database (if needed)
4. Types response manually
5. Sends reply

**Issues:** Slow response times, inconsistent tone, no context from previous interactions, hard to scale.

---

## Target Process (AI-Assisted)
1. Email arrives → auto-classified by platform and urgency
2. AI reads email + pulls customer history + looks up order data
3. AI drafts response following platform-specific rules
4. **Human reviews draft** (draft-only mode)
5. Human approves/edits → sends
6. Ticket logged with full context

---

## Platform-Specific Rules

### Website Email
- No content restrictions
- Can include links, promotions, cross-sell
- Response target: 24 hours (business days)

### eBay
- Reply through eBay messaging only
- No fee circumvention language
- Contact info allowed after active transaction
- Response target: 24 hours

### Amazon ⚠️ HIGH RISK
- Reply through Amazon system ONLY
- NO external links (account suspension risk)
- NO marketing or promotional content
- NO review solicitation
- 24-hour SLA including weekends/holidays
- Amazon AI scans all replies
- See: `MARKETPLACE_COMMUNICATION_RULES.md`

---

## Escalation Triggers
AI should add **[NEEDS REVIEW]** and escalate when:
- Customer threatens legal action
- Refund request over £/$/€50
- Product safety complaint
- Repeat complaint (3+ contacts)
- AI confidence is low
- Request doesn't match any known policy

---

## Response Templates
*To be developed per category:*
- [ ] Where is my order?
- [ ] I want to return/refund
- [ ] Item arrived damaged
- [ ] Wrong item received
- [ ] Order cancellation request
- [ ] Product question (pre-sale)
- [ ] Custom/personalized order inquiry
- [ ] Shipping time inquiry
- [ ] Replacement follow-up

---

## Metrics to Track
- Response time (first reply)
- Resolution time
- Customer satisfaction (if measurable)
- AI draft acceptance rate (% approved without edits)
- Escalation rate
- Platform-specific SLA compliance (especially Amazon)

---

*This SOP will be updated as the system is built and tested.*
