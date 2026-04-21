# Delegait — NemoClaw Skills Inventory & Build Plan

> Source: Ava research (Mar 22) + Cem directive (Mar 24-25)
> Updated: 2026-03-25

---

## Complete Skill Catalog (35 Skills)

### 🧲 LEAD GENERATION & OUTREACH

| Skill | What it does | Tools/APIs |
|---|---|---|
| LinkedIn Automation | Profile visits → connect → value message → CTA | Cloud-safe LinkedIn tool |
| Cold Email Sequencer | AI-personalized 5-touch sequences | Instantly, Lemlist |
| Content Creator | Blog posts, social posts, threads from topic input | Claude/GPT + scheduler |
| Social Scheduler | Queue + post to LinkedIn, X, Instagram | Buffer, Typefully, native APIs |
| Lead Finder | Scrape directories, LinkedIn, local business lists | Apollo, web scraping |
| Data Enrichment | Company size, tech stack, intent signals, verified emails | Apollo, Clay, Clearbit |

### 🎯 QUALIFICATION & CRM

| Skill | What it does | Tools/APIs |
|---|---|---|
| AI Chatbot | Qualify visitors in real-time on website | OpenClaw widget or Intercom |
| Lead Scorer | Budget/timeline/decision-maker scoring → Hot/Warm/Cold | CRM + custom rules |
| CRM Manager | Auto-tag, pipeline updates, deal tracking | HubSpot/Pipedrive API |
| Follow-Up Agent | Engagement-based nudges, no lead goes cold | CRM triggers + email |
| Meeting Prep | Pre-call brief: who they are, what they need, what to pitch | CRM + LinkedIn data |
| No-Show Recovery | "Sorry we missed you" + one-click reschedule | Calendar + email |

### 📅 SCHEDULING & BOOKING

| Skill | What it does | Tools/APIs |
|---|---|---|
| Calendar Manager | Sync availability, book meetings, send confirmations | Google Calendar, Cal.com |
| Booking Router | High-score → instant book, Low-score → nurture | CRM score + calendar |
| Reminder Agent | 24h confirmations, post-meeting summaries + action items | Calendar + email |

### 💰 FINANCE & PAYMENTS

| Skill | What it does | Tools/APIs |
|---|---|---|
| Invoice Generator | Create + send branded invoices from deal data | Stripe Invoicing, Xero, QuickBooks API |
| Payment Processor | Accept payments via link, track status | Stripe, PayPal |
| Expense Tracker | Categorize bank transactions, flag anomalies | QuickBooks AI, Plaid |
| Cash Flow Monitor | Weekly: income, expenses, overdue, burn rate | Bank API → formatted report |
| Late Payment Chaser | Automated reminders at 7/14/30 days, escalating tone | Email sequences triggered by invoice status |
| Proposal Builder | Generate branded proposals from scope notes | Template engine + Claude/GPT |

### 📊 INTELLIGENCE & REPORTING

| Skill | What it does | Tools/APIs |
|---|---|---|
| Weekly Digest | Monday morning email: pipeline, revenue, leads, actions | Aggregates all sources → email |
| KPI Dashboard | Real-time metrics: MRR, leads, conversion, churn | Supabase/Airtable → dashboard |
| Competitor Monitor | Track competitor pricing, features, content | Web scraping + alerts |
| Content Analytics | Which posts/emails performed, engagement trends | Social APIs + email analytics |

### 🛠️ DELIVERY (client work)

| Skill | What it does | Tools/APIs |
|---|---|---|
| Client Site Builder | Build client websites from questionnaire answers | v0, Lovable, Vercel |
| Client Chatbot Setup | Deploy AI chatbot on client's site | OpenClaw or custom widget |
| Client CRM Config | Set up pipeline, tags, automations for client | HubSpot/Pipedrive API |
| Client Outreach Setup | Configure email domains, warm-up, sequences | Instantly, DNS, DKIM/DMARC |
| Client Onboarding | Guided setup: questionnaire → auto-build → review → launch | Multi-step workflow |
| Client Reporting | Weekly intelligence email to each client | Per-client data aggregation |

### 🔧 INFRASTRUCTURE

| Skill | What it does | Tools/APIs |
|---|---|---|
| Email Deliverability | Domain warm-up, SPF/DKIM/DMARC, reputation monitoring | DNS management + monitoring |
| Backup + Security | Data backup, access control, encryption | NemoClaw policy engine |
| Error Handler | Detect failed workflows, retry or escalate to Cem | Monitoring + alerting |
| Self-Improvement | Log what worked/failed, update playbooks over time | Memory files + performance data |

---

## Skill Build Phases

### Phase 1 — Foundation (Week 1): Delegait eats its own cooking

| Priority | Skills Needed |
|---|---|
| 🔴 P0 | Website Builder, Chatbot Widget, SEO Page Generator |
| 🔴 P0 | Email Sequencer, LinkedIn Outreach, Content Generator |
| 🔴 P0 | Lead Enrichment, Lead Scorer, CRM Connector |
| 🔴 P0 | Booking Agent, Calendar Sync, Payment Setup |

### Phase 2 — Client Delivery (Week 2-4): Build what we sell

| Priority | Skills Needed |
|---|---|
| 🟡 P1 | Client Site Builder, Client Chatbot Setup, Client CRM Config |
| 🟡 P1 | Client Onboarding, Meeting Prep, Follow-Up Agent, Proposal Builder |
| 🟡 P1 | Lead Scorer, Auto-Tagger, Pipeline Reporter |

### Phase 3 — Scale (Month 2-3): Optimize + grow

| Priority | Skills Needed |
|---|---|
| 🟢 P2 | Weekly Digest, KPI Dashboard, Cash Flow Monitor, Competitor Monitor |
| 🟢 P2 | Nurture Sequences, No-Show Recovery, Late Payment Chaser |
| 🟢 P2 | Content Analytics, Self-Improvement, Error Handler |

---

## Skills We Already Have vs Need to Build

| Status | Skill | Notes |
|---|---|---|
| ✅ Have | Web search, content writing, email reading | OpenClaw native |
| ✅ Have | Code generation (Forge/Spark) | Codex CLI |
| ✅ Have | Social posting patterns | Skills exist |
| ✅ Have | Calendar management | Google Calendar via gws |
| ✅ Have | Email sending | Telegram/channel, need SMTP skill |
| 🟡 Partial | CRM integration | Need HubSpot/Pipedrive API skill |
| 🟡 Partial | Invoice/payments | Need Stripe API skill |
| 🔴 Need | LinkedIn automation | Need cloud-safe LinkedIn skill |
| 🔴 Need | Cold email infrastructure | Need Instantly/Lemlist API skill |
| 🔴 Need | Lead enrichment | Need Apollo/Clay API skill |
| 🔴 Need | Website deployment | Need Vercel deploy skill |
| 🔴 Need | Client onboarding workflow | Custom multi-step skill |
| 🔴 Need | AI chatbot embed | Widget or Intercom skill |
| 🔴 Need | Email deliverability | DKIM/DMARC/warm-up skill |

---

## Totals

- **35 skills total**
- **13** we already have or can adapt from existing OpenClaw/Ecell work
- **6** partially built — need API connectors
- **16** need to be built — but most are API wrappers, not rocket science

---

## First Assignment for NemoClaw

**Build delegait.com** — The employee's first assignment is building its own company's front door.
