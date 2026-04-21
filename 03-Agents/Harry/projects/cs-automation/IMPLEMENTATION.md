# Implementation Plan: CS Automation

## Phase 1: Foundation & Email (Weeks 1-2)
**Goal:** Stand up the infrastructure and automate the highest volume channel (Email/Order Status).

### 1.1 Infrastructure Setup
- [ ] Provision Ubuntu VPS (min 4GB RAM, 2 vCPU).
- [ ] Install Docker & Docker Compose.
- [ ] Configure DNS (n8n.ecellglobal.com, chat.ecellglobal.com).
- [ ] Deploy **Caddy** (Reverse Proxy).
- [ ] Deploy **n8n** (Self-hosted).
- [ ] Deploy **PostgreSQL** (Database).

### 1.2 Email Workflow (WISMO - Where Is My Order)
- [ ] Connect Gmail/IMAP credentials to n8n.
- [ ] Build "Ingestion Workflow":
    - Trigger: On New Email.
    - Node: OpenAI (Classify Intent -> Order Status, Return, Other).
- [ ] Build "Order Lookup Tool":
    - Connect to Magento/SQL Replica or API.
    - Input: Order ID (extracted via Regex).
    - Output: Tracking Link, Status.
- [ ] Build "Reply Workflow":
    - If "Order Status" + Found -> Draft Reply with GPT -> Send (or Save Draft for review).

### 1.3 Knowledge Base
- [ ] Scrape GoHeadCase.com FAQ.
- [ ] Setup Qdrant or Pinecone (or n8n Vector Store).
- [ ] Create "RAG Workflow" to query KB for general questions.

---

## Phase 2: Chat & Human Handoff (Weeks 3-4)
**Goal:** Real-time support on the website with seamless human escalation.

### 2.1 Chatwoot Setup
- [ ] Deploy **Chatwoot** (Self-hosted via Docker).
- [ ] Create Inboxes (Website, Email).
- [ ] Add Agents (Support Team).

### 2.2 Typebot Integration
- [ ] Deploy **Typebot** (Self-hosted).
- [ ] Design "Triage Bot" flow:
    - "Hi, are you asking about an order?"
    - Collect Email/Order ID.
- [ ] Connect Typebot to n8n:
    - Send user input to n8n webhook.
    - n8n processes (uses Phase 1 logic) and returns answer.
- [ ] Implement Handoff:
    - If Sentiment < Negative OR User clicks "Talk to Human":
    - Typebot executes "Open Chatwoot Widget" or posts transcript to Chatwoot API.

---

## Phase 3: Voice Agents (Week 5+)
**Goal:** Handle inbound phone calls for simple queries.

### 3.1 Vapi.ai Configuration
- [ ] Purchase Phone Number (Twilio) and link to Vapi.
- [ ] Configure Vapi Assistant:
    - System Prompt: "You are the Head Case Designs support assistant..."
    - Tools: Define `lookup_order`, `check_return_policy` as function calls.
- [ ] Connect Vapi -> n8n:
    - n8n Webhook receives function calls.
    - Returns data (e.g., "Order #123 is Shipped, tracking is XYZ").

### 3.2 Testing & Refinement
- [ ] Stress test concurrent calls.
- [ ] Tune latency (aim for <800ms response).
- [ ] Setup "Warm Transfer" SIP URI to forward complex calls to the physical call center.

---

## Deployment Checklist
1. **Security**: Ensure `.env` files are not committed. Use Docker Secrets or locked-down file permissions.
2. **Backups**: Script daily dumps of the Postgres database and n8n `~/.n8n` directory.
3. **Monitoring**: Setup Uptime Kuma to ping the n8n webhook health check endpoint.
