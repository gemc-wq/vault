# Discovery Doc #2: NemoClaw, OpenClaw Starter Kits & SaaS Wrapper

> **Purpose:** Cross-channel research document. Use in Perplexity, Claude, ChatGPT, or hand to any research agent.
> **Created:** 2026-03-24 | **Author:** Ava (for Cem)
> **Status:** DISCOVERY — open questions, not decisions

---

## The Big Idea

**Pre-configured OpenClaw setups for specific business verticals, distributed as NemoClaw-compatible policy packs.**

A new business signs up → picks their vertical → answers a Q&A → gets a fully configured AI operations system with agents, cron jobs, memory, and dashboards. Day 1 productive.

This is our SaaS spin-off. **Ecell Global is Customer #1** — the e-commerce starter kit is battle-tested on $5M+ revenue before we sell it externally.

## What We Know About NemoClaw

### Core Architecture (from GTC 2026, Mar 17)
- **NemoClaw = Enterprise wrapper around OpenClaw**
- Not a competitor — it's OpenClaw + security + governance
- Installs with a single command on top of existing OpenClaw

### Key Components
| Component | What It Does |
|-----------|-------------|
| **OpenShell** | Open-source security runtime. Sandboxes agents at process level. YAML-based policy controls for file access, network, API calls |
| **Policy Engine** | Connects to existing SaaS company security/compliance infrastructure. Determines what agents CAN and CANNOT do |
| **Privacy Router** | Keeps sensitive data local. Routes to cloud models only when policy permits |
| **Nemotron Models** | NVIDIA's local LLMs (120B param). Run on DGX Spark, RTX workstations. Zero data leaves the building |
| **Guardrails** | Policy guardrails + privacy router = enterprise-grade data protection |

### Key Principles
- **Agent permissions mirror employee permissions** — same RBAC model
- **YAML policy files** define capabilities (like Kubernetes for agents)
- **Every SaaS company becomes a GaaS company** (Jensen Huang) — Generative-as-a-Service
- **Partners:** Cisco, CrowdStrike, Google, Microsoft Security, Box, Atlassian, Salesforce, SAP

### Status
- Early access / alpha preview
- `nemoclaw` CLI available
- Runs in Docker + OpenShell
- Default model: Nemotron 3 Super 120B (cloud) or local deployment

## Starter Kit Architecture

### What a Starter Kit Contains

```
starter-kit-ecommerce/
├── AGENTS.md                    # Pre-configured agent team
├── SOUL.md                      # Business persona template (Q&A fills gaps)
├── USER.md                      # Template (filled during onboarding Q&A)
├── agents/
│   ├── router/                  # Flash triage agent config
│   ├── analyst/                 # Sales/inventory analyst
│   ├── lister/                  # Marketplace listing agent
│   ├── creative/                # Image/content generation
│   ├── scout/                   # Market research, competitor intel
│   └── ops/                     # Operations, procurement, fulfillment
├── skills/
│   ├── marketplace-api/         # Amazon, Walmart, Shopify connectors
│   ├── inventory-tracker/       # Stock level monitoring
│   ├── pricing-optimizer/       # Dynamic pricing rules
│   ├── seo-content/             # SEO keyword + listing content
│   └── image-pipeline/          # Product image generation
├── crons/
│   ├── daily-sales-digest.yaml  # Morning revenue + order summary
│   ├── inventory-alerts.yaml    # Low stock warnings
│   ├── competitor-scan.yaml     # Weekly competitor price check
│   ├── listing-audit.yaml       # Weekly gap analysis
│   └── weekly-report.yaml       # Friday executive summary
├── policies/                    # NemoClaw YAML policies
│   ├── data-access.yaml         # What data agents can see
│   ├── external-comms.yaml      # What agents can send externally
│   └── api-permissions.yaml     # Which marketplace APIs are allowed
├── dashboards/
│   ├── pulse/                   # Velocity analytics
│   └── conversion/              # Session/conversion tracking
└── onboarding/
    └── questions.yaml           # Q&A flow for customization
```

### Onboarding Q&A (fills the gaps)

**E-commerce example:**
1. What's your company name?
2. Which marketplaces do you sell on? (Amazon, Walmart, Shopify, eBay, Etsy)
3. What product category? (Electronics, Fashion, Home, etc.)
4. How many SKUs? (<100, 100-1000, 1000-10000, 10000+)
5. Do you manufacture or resell?
6. What's your monthly revenue range?
7. Which channels do you want reports on? (Telegram, Slack, Discord, Email)
8. Do you have API keys for your marketplaces? (guided setup)
9. What's your biggest operational pain point?
10. Who else on your team needs access? (add team members)

**Professional services example:**
1. What type of services? (Consulting, Agency, Legal, Accounting)
2. What's your website URL?
3. How do you generate leads? (Inbound, Outbound, Referral, Ads)
4. What CRM do you use? (HubSpot, Salesforce, Pipedrive, None)
5. What's your average deal size?
6. How many clients per month?
7. What channels for reports? (Telegram, Slack, Email)

## Vertical Starter Kits

### 1. E-Commerce Marketplace Seller (OUR KIT — Battle-tested on Ecell)

**Agents:**
| Agent | Model | Role |
|-------|-------|------|
| Router | Flash Lite/Nano | Triage + context builder |
| Atlas | Gemini Pro | Sales analytics, pricing, performance reports |
| Lister | Sonnet/GPT-5.4 | Marketplace listing creation + optimization |
| Scout | Flash | Competitor intel, trend spotting, SEO |
| Creative | Gemini Pro + Image Gen | Product images, lifestyle shots, A+ content |
| Ops | Flash | Inventory alerts, procurement triggers, fulfillment |

**Cron Jobs:**
| Schedule | Job | Output |
|----------|-----|--------|
| Daily 7 AM | Sales digest | Revenue, orders, top sellers → Telegram/Slack |
| Daily 8 AM | Inventory alerts | Low stock, reorder triggers → Telegram/Slack |
| Daily 9 AM | Listing health | Suppressed/inactive listings → alert |
| Weekly Mon | Competitor scan | Price changes, new entrants → report |
| Weekly Mon | Listing gap analysis | Champions not listed → task list |
| Weekly Fri | Executive summary | Week review, KPIs, recommendations |
| Monthly 1st | Revenue report | Monthly P&L, marketplace breakdown |

**Skills:**
- Amazon SP-API connector (reports, listings, inventory)
- Walmart API connector (items, feeds, pricing)
- Shopify API connector (products, orders, fulfillment)
- SKU parser (product type, device, design, variant extraction)
- SEO content generator (title, bullets, description from SKU)
- Image CDN connector (product image retrieval + validation)
- Pricing optimizer (velocity-based dynamic pricing)
- PULSE analytics (best sellers, conversion, velocity signals)

### 2. Professional Services / Agency

**Agents:**
| Agent | Model | Role |
|-------|-------|------|
| Router | Flash Lite/Nano | Triage + context |
| Growth | Gemini Pro | Lead gen strategy, funnel analysis |
| Content | Sonnet | Blog posts, case studies, email sequences |
| Scout | Flash | Market research, competitor websites |
| Builder | Codex GPT-5.4 | Website updates, landing pages, forms |
| CRM | Flash | Pipeline tracking, follow-up reminders |

**Cron Jobs:**
| Schedule | Job | Output |
|----------|-----|--------|
| Daily 8 AM | Pipeline digest | New leads, follow-ups due, deals closing → Telegram/Slack |
| Daily 9 AM | Website analytics | Traffic, conversions, top pages → report |
| Weekly Mon | Content calendar | Blog/social posts scheduled this week |
| Weekly Wed | Competitor check | New content, pricing changes, reviews |
| Weekly Fri | Client report prep | Auto-draft weekly client updates |
| Monthly 1st | Growth report | Leads, conversions, revenue, CAC |

**Skills:**
- Google Analytics connector
- CRM connector (HubSpot/Salesforce/Pipedrive)
- Email outreach (sequences, follow-ups)
- Website builder (Next.js/React landing pages)
- SEO auditor (technical + content)
- Social media scheduler
- Invoice/proposal generator

### 3. Content Creator / Influencer

**Agents:**
| Agent | Model | Role |
|-------|-------|------|
| Router | Flash Lite/Nano | Triage |
| Creative | Gemini Pro + Image Gen | Content ideas, thumbnails, graphics |
| Writer | Sonnet | Scripts, captions, blog posts |
| Scout | Flash | Trend spotting, hashtag research |
| Analytics | Flash | Performance tracking across platforms |

**Cron Jobs:**
| Schedule | Job | Output |
|----------|-----|--------|
| Daily 8 AM | Trending topics | What's hot on TikTok/X/IG → content ideas |
| Daily 6 PM | Post performance | Today's engagement metrics |
| Weekly Mon | Content plan | 5 post ideas with hooks + formats |
| Weekly Fri | Growth report | Follower growth, top posts, engagement rate |

### 4. SaaS / Tech Startup

**Agents:**
| Agent | Model | Role |
|-------|-------|------|
| Router | Flash Lite/Nano | Triage |
| PM | Gemini Pro | Sprint planning, ticket triage, release notes |
| DevOps | Codex GPT-5.4 | Deployment, monitoring, incident response |
| Growth | Flash | Signup analytics, churn signals, NPS |
| Support | Sonnet | Customer ticket drafts, docs updates |

**Cron Jobs:**
| Schedule | Job | Output |
|----------|-----|--------|
| Daily 9 AM | Deployment report | What shipped, what failed, uptime |
| Daily 10 AM | Support digest | New tickets, unresolved, sentiment |
| Weekly Mon | Sprint review | Velocity, blockers, carry-over |
| Weekly Fri | Metrics dashboard | MRR, churn, signups, NPS |

## The SaaS Business Model

### Revenue Streams
1. **Starter Kit License** — $49-199/mo per vertical (includes agents, crons, skills, updates)
2. **Managed Hosting** — $99-499/mo (ClawCloud-style, we run the infrastructure)
3. **Custom Skills** — $500-5000 one-time (marketplace-specific integrations)
4. **Enterprise** — Custom pricing (NemoClaw deployment, on-prem, compliance)

### Why This Works
- **OpenClaw is free** — we're selling the configuration, not the platform
- **NemoClaw provides enterprise credibility** — NVIDIA partnership signal
- **Battle-tested** — every feature proven on Ecell's $5M+ business first
- **Recurring revenue** — monthly subscription for updates, new skills, support
- **Network effects** — more customers = more data on what works per vertical

### Competitive Advantage
- We're NOT selling a chatbot. We're selling **an AI operations team in a box.**
- No one else has pre-configured OpenClaw setups with working cron jobs, tested skills, and vertical-specific agent teams
- First mover in "OpenClaw-as-a-Service for SMBs"

## The Meta Angle (Cem's Insight)

> "We can use our own SaaS starter kit to sell the SaaS."

The professional services / SaaS starter kit can power our own sales operation:
- Lead gen agent finds potential customers (marketplace sellers, agencies)
- Content agent creates marketing materials
- CRM agent tracks pipeline
- **We eat our own dog food** — if the starter kit works for selling itself, it works

This is a live proof of concept: deploy the SaaS starter kit internally, use it to sell starter kits to others. Every customer interaction validates and improves the product.

## Open Research Questions

### On NemoClaw
1. What's the exact YAML policy format? Can we create custom policy templates per vertical?
2. Can NemoClaw policy packs be distributed as installable packages? (like skills on ClawHub)
3. What's the minimum hardware for NemoClaw? (Does it need NVIDIA GPU or can it run on any machine?)
4. How does the privacy router work technically? Can we configure data classification rules per vertical?
5. What's the licensing model for NemoClaw in a SaaS redistribution context?

### On Starter Kits
1. Best distribution format? (npm package? GitHub template? ClawHub skill pack?)
2. How to handle the onboarding Q&A? (CLI wizard? Web UI? Telegram bot?)
3. How to update deployed kits without breaking customizations? (semantic versioning? migration scripts?)
4. What's the minimum viable kit? (How few agents/crons to still be valuable?)
5. Should each kit have a "getting started" tutorial agent that walks the user through the first week?

### On Business Model
1. What's the TAM for "AI operations platform for SMBs"?
2. Who are the competitors? (Agency-in-a-box, AI SaaS tools, automation platforms)
3. Pricing sensitivity per vertical?
4. Channel strategy? (Direct, partnerships, ClawHub marketplace, AppSumo launch?)
5. What's the MVP we can ship in 30 days?

## Next Steps

1. **Set up NemoClaw test instance** — Cem is arranging this
2. **Research NemoClaw policy engine YAML format** — can we create custom policy packs?
3. **Finish e-commerce starter kit spec** — we're 80% there (PULSE, Conversion Dashboard, Walmart Lister, SKU parsing all built)
4. **Build the onboarding Q&A flow** — probably a simple CLI wizard first
5. **Test on a second business** — find a friendly marketplace seller to beta test
6. **Cem running parallel research** — Perplexity + Claude for cross-validation

---

*Use this doc to prompt Perplexity, Claude, or any research tool. Key query seeds:*
- "NemoClaw YAML policy engine format configuration"
- "NemoClaw OpenShell agent permissions enterprise setup"
- "OpenClaw starter kit distribution ClawHub"
- "AI operations platform SMB market size 2026"
- "Pre-configured AI agent teams for business verticals"
- "OpenClaw as a service business model"
- "NemoClaw vs raw OpenClaw enterprise deployment comparison"
