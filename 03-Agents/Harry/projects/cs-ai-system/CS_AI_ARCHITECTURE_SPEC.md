# CS AI System Architecture Spec
**Project:** Unified Customer Service AI — Ecell Global  
**Author:** Harry (AI COO)  
**Date:** 2026-02-18  
**Status:** DRAFT — Awaiting Cem review

---

## Overview

Two parallel CS AI systems serving distinct audiences:

| System | Brand | Audience | Goal |
|--------|-------|----------|------|
| **ESale AI Hub** | esaleglobal.com | New business / B2B prospects | Lead gen + conversion |
| **GoHeadCase AI Support** | goheadcase.com | Existing customers | Support + retention |

This spec covers **ESale AI Hub** (Phase 1 priority).

---

## ESale AI Hub — Three-Channel Architecture

### Channel 1: AI Chat Widget (Website)

**Purpose:** Inbound lead qualification + instant response on esaleglobal.com  
**Placement:** Persistent widget on esaleglobal.com (Ava to provision space in redesign)  
**Capability:**
- Greet visitors, understand their business type and needs
- Answer FAQs about products, MOQ, lead times, licensing
- Qualify intent: browsing vs. buying signal
- Route hot leads → notify sales team via Slack/email
- Log all conversations to Supabase

**Stack:**
- Frontend: Floating chat widget (React, embeddable script)
- AI: Claude Sonnet via Anthropic API (brand-safe, good at structured reasoning)
- Backend: Next.js API route or N8N webhook
- Storage: Supabase `conversations` table

---

### Channel 2: AI Outreach Assistant

**Purpose:** Proactive new business development — first-touch and follow-up sequences  
**Trigger:** Manual target list upload or automated prospect discovery  
**Capability:**
- Personalised first-touch email generation (company-specific context)
- Multi-step follow-up sequences (Day 1, Day 3, Day 7, Day 14)
- A/B test subject lines and CTAs
- Track open/reply/book rates
- Log all outreach activity to Supabase

**Channels (confirmed 2026-02-18):**
- ✅ Email (Resend/Postmark — multi-step sequences)
- ✅ LinkedIn (Phantombuster or LinkedIn API — first-touch + follow-up)
- ⚠️ Phone / AI cold calling — pending Cem confirmation (large build, Phase 2 candidate)

**Scale design:** System must be multi-brand from day one — will serve future SaaS spin-offs beyond ESale Global.

**Stack:**
- Orchestration: N8N workflow
- AI: GPT-5.2 for email copy generation
- Email delivery: Resend (transactional) or existing SMTP
- Storage: Supabase `outreach_contacts` + `outreach_sequences` tables

---

### Channel 3: AI Voice Assistant (Phone)

**Purpose:** Inbound CS phone line — qualify, inform, escalate  
**Number:** Existing Ecell Global CS phone number (via Twilio SIP trunking)  
**Capability:**
- Answer calls 24/7 with natural voice
- Understand caller intent (support, sales, wholesale enquiry)
- Collect caller details, log the call summary
- Escalate urgent calls to human → trigger Slack alert
- Handle FAQs verbally

**Stack:**
- Telephony: Twilio (UK + US numbers confirmed — inbound call webhook → N8N)
- Speech-to-Text: Google Cloud STT (Vertex — supports all required languages)
- AI Brain: Claude Sonnet (intent classification + response generation)
- Text-to-Speech: ElevenLabs (configured per region)
- Storage: Supabase `voice_calls` table

**Voice profiles (confirmed 2026-02-18):**
| Region | Number | Languages | ElevenLabs Voice |
|--------|--------|-----------|-----------------|
| US | Twilio US | English, Spanish | US English voice + ES voice |
| UK | Twilio UK | English | UK English voice |
| EU | TBD | German, Italian, French, Spanish | Multilingual voice model |

**Language detection:** Caller language auto-detected via Google STT → routes to correct voice profile + response language.

**Hot lead alerts:** Slack + Email (both confirmed)

---

## Unified Supabase Database Schema

**Project:** nuvspkgplkdqochokhhi (existing ESale project)

### Tables

```sql
-- All inbound chat conversations
CREATE TABLE conversations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  channel TEXT NOT NULL, -- 'chat' | 'email' | 'voice'
  contact_name TEXT,
  contact_email TEXT,
  contact_company TEXT,
  contact_phone TEXT,
  intent TEXT, -- 'lead' | 'support' | 'browsing' | 'wholesale'
  status TEXT DEFAULT 'new', -- 'new' | 'qualified' | 'handed_off' | 'closed'
  summary TEXT,
  transcript JSONB, -- full message history
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Outreach contacts and sequences
CREATE TABLE outreach_contacts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT,
  email TEXT,
  company TEXT,
  linkedin_url TEXT,
  industry TEXT,
  status TEXT DEFAULT 'new', -- 'new' | 'contacted' | 'replied' | 'booked' | 'unsubscribed'
  sequence_step INTEGER DEFAULT 0,
  last_contacted_at TIMESTAMPTZ,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Voice call log
CREATE TABLE voice_calls (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  caller_number TEXT,
  caller_name TEXT,
  duration_seconds INTEGER,
  intent TEXT,
  summary TEXT,
  escalated BOOLEAN DEFAULT false,
  recording_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Unified contact directory (deduped across all channels)
CREATE TABLE contacts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT,
  email TEXT UNIQUE,
  company TEXT,
  phone TEXT,
  source TEXT, -- 'chat' | 'outreach' | 'voice' | 'manual'
  lifecycle_stage TEXT DEFAULT 'prospect', -- 'prospect' | 'lead' | 'customer'
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## GoHeadCase AI Support (Phase 2 — Separate Track)

**Audience:** Existing GoHeadCase.com customers  
**Use case:** Order status, returns, product questions, complaints  
**Recommended platform:** **Vertex AI Agent Builder** (Google Cloud)  
  - Already in Google Cloud ecosystem (project: opsecellglobal)  
  - Native BigQuery integration for order data  
  - Grounding against product catalog  
  - Handoff to human agent via email  
**Timeline:** After ESale AI Hub is live

---

## Build Phases

### Phase 1 (This week)
- [ ] Draft Supabase schema + create tables
- [ ] Brief Ava: chat widget space on esaleglobal.com
- [ ] Confirm outreach channel: email only vs email + LinkedIn
- [ ] N8N workflow skeleton for AI chat backend

### Phase 2 (Next 2 weeks)
- [ ] AI Chat widget: frontend embed + API route
- [ ] Outreach assistant: N8N sequence engine + Resend integration
- [ ] Supabase dashboard view for Cem (leads pipeline)

### Phase 3 (Following 2 weeks)
- [ ] Voice assistant: Twilio + ElevenLabs + Claude
- [ ] Unified contact dedup logic
- [ ] Slack alerts for escalations + hot leads

### Phase 4 (Separate project)
- [ ] GoHeadCase Vertex AI support agent
- [ ] Amazon FBA data pull for esale app

---

## Decisions Confirmed (2026-02-18)

| # | Question | Answer |
|---|----------|--------|
| 1 | Outreach channels | Email + LinkedIn + Phone (cold calling TBC — may be Phase 2) |
| 2 | Phone provider | Twilio (UK + US numbers already set up) |
| 3 | Hot lead alerts | Slack + Email both |
| 4 | Voice languages | US: EN+ES / UK: EN / EU: DE+IT+FR+ES |
| 5 | CRM for v1 | Supabase (long-term source of truth) |
| 6 | Chat widget entry | Quick buttons: Shop / Support / Partner with us |

## Open Questions

1. **Outreach phone:** AI cold calling (auto-dial prospects) or manual? Cold calling = Phase 2 recommendation.
2. **EU phone number:** Do we have/need a Twilio EU number for the voice agent?
3. **ElevenLabs multilingual:** Use ElevenLabs Turbo v2.5 (multilingual model) or separate voice per language?

---

*Next step: Cem reviews + answers open questions → Harry starts Phase 1 build*
