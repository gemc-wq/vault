# CS Automation Architecture — eCELL Global / Head Case Designs
*Documented: 2026-02-10 | Source: Cem walkthrough + research*

---

## Vision

AI-assisted customer service across all channels — website email, eBay, Amazon — with platform-specific compliance rules, conversation history, and order data lookup. **Draft-only mode** initially for human review.

---

## Three Communication Channels

### 1. Website Email (headcasedesigns@ecellglobal.com)
- **Provider:** Google Workspace (Gmail)
- **Freedom:** Full — no platform restrictions
- **Approach:** Ticketing system + AI draft responses
- **Status:** Credentials saved, awaiting App Password or OAuth for IMAP access

### 2. eBay Messaging
- **Accounts:** e_cell, ecell_accessorize, head_case_designs, head_case_designs-us
- **Rules:** More relaxed than Amazon
  - Can share contact info (phone/email) AFTER transaction is active
  - No fee circumvention (don't direct off-platform to avoid fees)
  - CS bots allowed if following communication guidelines
  - eBay Robot & Agent Policy (2025): Bans buy-for-me bots but allows CS bots
- **Approach:** Reply through eBay messaging system
- **Status:** Cem sending eBay login credentials (for trial)
- **FAQ:** Saved at `projects/cs-automation/ebay_faq.docx`

### 3. Amazon Messaging
- **Rules:** STRICTEST — high suspension risk
  - 24-hour SLA (including weekends/holidays)
  - NO external links (even your own website)
  - NO marketing or promotional language
  - Amazon AI scans replies for violations
  - Must use Amazon's structured Message Types via SP-API
  - Seller liable for AI-generated content
- **Approach:** Must reply through Amazon Seller Central / SP-API Messaging
- **Status:** SP-API keys available, needs proper integration

---

## Ticketing System Recommendation

### Why a Ticketing System?
1. **Customer history:** AI needs full conversation context (e.g., replacement follow-ups)
2. **Multiple email addresses:** Unified view across sites
3. **Ticket status:** Open/pending/resolved changes the AI response
4. **SLA tracking:** Amazon's 24-hour requirement needs monitoring

### Recommended: Helpdesk Tool + AI Layer
- Use existing helpdesk (Freshdesk/FreeScout/similar) for:
  - Thread management
  - Multi-inbox support
  - Status tracking
  - SLA timers
  - Agent assignment
  - Reporting
- Layer AI on top for:
  - Draft response generation
  - Order data lookup (from Cloud SQL)
  - Platform-specific content filtering
  - Customer history context

### Alternative: Supabase Custom Build
- Every email → ticket record in Supabase
- Customer email as key
- AI reads full thread history + order data
- More control, but weeks to build
- **Decision: TBD — Cem to evaluate**

---

## Content Filters (Per Platform)

### Amazon Filter (CRITICAL)
The AI draft MUST be filtered before any Amazon message:
- Strip ALL URLs/links
- Remove any promotional language
- Remove any mention of external websites
- Remove discount codes or special offers
- Remove requests for reviews/feedback
- Add [NEEDS REVIEW] for complaints
- Enforce maximum response length
- Use only Amazon-approved Message Types

### eBay Filter
- Strip links to external sales channels
- Don't include pricing for items not on eBay
- Don't suggest buying outside eBay
- Contact info allowed only for active transactions
- More flexible tone allowed

### Website Email Filter
- No restrictions — full freedom
- Can include website links, promotions, etc.
- Can reference other platforms

---

## Order Data Access

### Phase 1 (Now): Google Cloud SQL Clone
- Non-production daily sync of AWS production database
- Safe for testing and development
- Contains full order history
- **Awaiting:** Connection details from Cem

### Phase 2 (Parallel): Marketplace APIs
- Amazon SP-API (Orders endpoint)
- eBay Fulfillment API
- BigCommerce API (website orders)
- **Awaiting:** API credential setup

### Phase 3 (Future): Supabase Unified Store
- Unified schema designed (see `projects/sales-schema/`)
- All platforms sync into one database
- Single query for any order from any channel

---

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| AI Brain | GPT-4o-mini via OpenRouter (N8N) | ~$0.01/email |
| Email Access | Google Workspace (IMAP/OAuth) | Existing |
| Workflow | N8N (self-hosted) | Free |
| Order Data | Google Cloud SQL → Supabase | Existing |
| Ticketing | TBD (Freshdesk / FreeScout / custom) | TBD |
| Content Filter | Rule-based + AI validation | Included |

---

## N8N Workflows Created

### 1. HeadCase CS Chat (ID: 2uLt3nnD8ExTiFCq)
- **Status:** Active
- Webhook-based chatbot for website
- GPT-4o-mini via OpenRouter
- System prompt with CS policies

### 2. HeadCase CS Email - AI Draft (ID: cXTD8CRCvjvYVYza)
- **Status:** Inactive (awaiting email auth)
- IMAP trigger → AI draft → log
- Draft-only mode (no auto-send)
- Needs App Password or OAuth to activate

---

## Compliance Reference
Full marketplace communication rules: `projects/cs-automation/MARKETPLACE_COMMUNICATION_RULES.md`

---

*Next steps: Get email auth working. Set up Cloud SQL connection. Trial on eBay first. Then expand to website email. Amazon last (highest risk).*
