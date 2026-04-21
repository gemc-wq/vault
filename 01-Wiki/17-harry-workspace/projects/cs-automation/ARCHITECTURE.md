# CS Automation Architecture for Ecell Global

## 1. Executive Summary
This document outlines the technical architecture for automating customer service at Ecell Global / Head Case Designs. The goal is to unify support channels (Email, Chat, Voice) into a single intelligent "brain" powered by **n8n**, utilizing best-in-class AI tools for each modality while maintaining human oversight via **Chatwoot**.

**Core Philosophy:** Centralized Logic.
Instead of having separate bots for Chat and Voice, a single central n8n backend manages the "Brain" (knowledge base, order lookups, reasoning), ensuring consistent answers across all channels.

---

## 2. System Architecture Diagram

```mermaid
graph TD
    subgraph Channels
        Email[Gmail / Amazon SES]
        Chat[Typebot Widget]
        Voice[Vapi.ai + Twilio]
    end

    subgraph "The Brain (n8n Self-Hosted)"
        Router{Router Workflow}
        Classifier[AI Classifier Agent]
        OrderSys[Order Lookup (Magento/SQL)]
        KB[Vector Store / Pinecone]
        Composer[AI Response Composer]
    end

    subgraph "Human Agent (Chatwoot)"
        Inbox[Unified Inbox]
        Handoff[Human Handoff Trigger]
    end

    Email -->|Webhook/IMAP| Router
    Chat -->|API| Router
    Voice -->|Function Call| Router
    
    Router --> Classifier
    Classifier -->|Inquiry| KB
    Classifier -->|Order Status| OrderSys
    
    KB --> Composer
    OrderSys --> Composer
    
    Composer -->|Draft/Reply| Email
    Composer -->|Chat Reply| Chat
    Composer -->|Voice Speak| Voice
    
    Classifier -->|High Sentiment/Complexity| Handoff
    Handoff --> Inbox
```

---

## 3. Component Breakdown

### A. The Core: n8n (Self-Hosted)
- **Role:** Orchestration engine. Connects all inputs, processes logic, calls AI models, and sends responses.
- **Hosting:** Docker Compose on Ubuntu (AWS/DigitalOcean).
- **Security:** Traefik or Caddy Reverse Proxy with SSL.

### B. Channel 1: Email Automation
- **Flow:**
  1. **Ingest:** n8n polls Gmail/IMAP or receives SES webhook.
  2. **Classify:** LLM (GPT-4o-mini) analyzes intent (Order Status, Return, Product Q, Spam).
  3. **Action:**
     - *Simple (WISMO):* Auto-query database for tracking -> Generate Reply -> **Send**.
     - *Complex (Complaint):* Generate Draft -> Create Chatwoot Ticket -> **Human Review**.
- **Tools:** Gmail Node, OpenAI Node, HTTP Request.

### C. Channel 2: Chat (Typebot + Chatwoot)
- **Frontend:** **Typebot**. Best-in-class conversational UI (bubbles, inputs). Embedded on GoHeadCase.com.
- **Middleware:** Typebot sends user input to n8n webhook.
- **Handoff:** If AI fails or user requests human, Typebot opens a **Chatwoot** widget or pushes the conversation history into Chatwoot for an agent to take over.
- **Why:** Typebot is better than n8n's native chat for UX; Chatwoot is better for human agent management.

### D. Channel 3: Voice (Vapi.ai)
- **Provider:** **Vapi.ai**.
- **Role:** Handles telephony (STT/TTS) and turn-taking.
- **Integration:** Vapi is configured to call an n8n webhook for "fulfillment".
- **Flow:**
  1. Customer calls -> Vapi answers.
  2. Vapi sends audio transcript to n8n.
  3. n8n checks order status/KB.
  4. n8n returns text response -> Vapi speaks it.
- **Transfer:** Vapi can "warm transfer" to a human support line (SIP/PSTN) if sentiment triggers.

### E. Knowledge Base (RAG)
- **Data:** Shipping policies, Return windows, Product FAQ.
- **Storage:** Supabase (pgvector) or Pinecone.
- **Ingestion:** n8n workflow that scrapes the Help Center and updates the vector store weekly.

---

## 4. Cost Estimates (Monthly)

| Service | Tier | Est. Cost | Notes |
| :--- | :--- | :--- | :--- |
| **n8n** | Self-Hosted | $10 - $20 | Server cost (VPS) |
| **OpenAI** | API (Tier 1) | $50 - $100 | Based on token usage |
| **Vapi.ai** | Pay-as-you-go | ~$0.05/min | Voice automation only |
| **Twilio** | SIP Trunking | $10 + usage | Phone numbers & carriage |
| **Chatwoot** | Self-Hosted | $0 | Part of VPS |
| **Typebot** | Self-Hosted | $0 | Part of VPS |
| **Total** | | **~$100 - $150/mo** | vs $3000+ for human staff |

---

## 5. Technology Stack Recommendations
- **OS:** Ubuntu 24.04 LTS
- **Containerization:** Docker & Docker Compose
- **Database:** PostgreSQL (shared by n8n, Chatwoot, Typebot)
- **Proxy:** Caddy (simpler than Traefik/Nginx)
- **AI Models:**
  - *Router/Classifier:* GPT-4o-mini (Fast, cheap)
  - *Complex Replies:* GPT-4o or Claude 3.5 Sonnet (High quality)

