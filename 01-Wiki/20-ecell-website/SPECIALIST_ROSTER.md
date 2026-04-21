# Ecell AI Specialist Roster
## The Swarm Architecture

*Drafted: 2026-01-30*
*Status: Planning*

---

## 🎯 Overview

A hybrid swarm model where **Harry (Claude Opus)** serves as the orchestrator/COO, coordinating specialized agents and skills for different domains.

```
                    ┌─────────────────────────┐
                    │      HARRY (COO)        │
                    │    Claude Opus 4.5      │
                    │   Orchestrator / PM     │
                    └───────────┬─────────────┘
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        │           │           │           │           │
        ▼           ▼           ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ CREATOR │ │ ANALYST │ │ DESIGNER│ │ MARKETER│ │DEVELOPER│
   │ Content │ │  Data   │ │  Visual │ │ Social  │ │   Web   │
   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

---

## 👔 The Orchestrator

### Harry — Chief Operations AI

| Attribute | Value |
|-----------|-------|
| **Role** | Orchestrator / Project Manager / COO |
| **Model** | Claude Opus 4.5 |
| **Location** | AWS (always-on) |
| **Responsibilities** | Strategy, coordination, planning, context management |

**What Harry Does:**
- Maintains big-picture context across all projects
- Assigns tasks to specialists
- Reviews and approves outputs
- Communicates with Cem
- Manages priorities and timelines
- Handles complex reasoning and planning

**What Harry Delegates:**
- Repetitive content generation
- Image creation/editing
- Data processing at scale
- Specialized domain tasks

---

## 🎨 The Specialists

### 1. THE CREATOR — Content Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Content Writer / Copywriter |
| **Implementation** | Sub-agent or Skill |
| **Model** | Claude Sonnet (fast, good writing) |
| **Trigger** | "Create content for...", "Write copy for..." |

**Responsibilities:**
- Social media posts (Instagram, TikTok, LinkedIn)
- Product descriptions
- Email marketing copy
- Ad copy
- Blog posts / articles

**Tools Needed:**
- Social posting skill (Instagram, TikTok APIs)
- Brand voice guidelines
- Product catalog access

**Output Examples:**
- 50 Instagram captions for Peanuts cases
- Email campaign for Harry Potter launch
- LinkedIn posts for B2B outreach

---

### 2. THE ANALYST — Data Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Data Analyst / Business Intelligence |
| **Implementation** | Skill + Harry |
| **Model** | Claude (complex analysis) or specialized |
| **Trigger** | "Analyze...", "Report on...", "What's trending..." |

**Responsibilities:**
- Sales data analysis
- Competitor research
- Trend identification
- Performance reporting
- ROI calculations
- Market research

**Tools Needed:**
- Access to sales data (CSV, database)
- Google Trends integration
- Social analytics APIs
- Visualization tools

**Output Examples:**
- Weekly sales report by license
- Competitor pricing analysis
- Social engagement dashboard
- Product performance rankings

---

### 3. THE DESIGNER — Visual Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Graphic Designer / Image Creator |
| **Implementation** | iMac Apps + AI Models |
| **Models** | Gemini 3 Pro, Nano Banana, DALL-E |
| **Location** | iMac (for Illustrator) + Cloud (for AI generation) |
| **Trigger** | "Design...", "Create image...", "Generate visual..." |

**Responsibilities:**
- Product images for Amazon/website
- Social media graphics
- Marketing materials
- Cut line automation (Illustrator)
- Image editing and enhancement

**Tools Needed:**
- Adobe Illustrator (iMac)
- Gemini Gem for product images
- Nano Banana Pro
- Creatify.ai (product videos)
- Google FLOW (video generation)

**Output Examples:**
- Amazon main images for new phone models
- Instagram story templates
- Product mockups
- Cut-ready EPS files

---

### 4. THE MARKETER — Social & Campaign Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Social Media Manager / Campaign Manager |
| **Implementation** | Sub-agent with scheduling skills |
| **Model** | Claude Sonnet |
| **Trigger** | "Schedule posts...", "Run campaign...", "Post to..." |

**Responsibilities:**
- Social media calendar management
- Post scheduling and publishing
- Influencer coordination
- Campaign performance tracking
- A/B testing
- Hashtag strategy

**Tools Needed:**
- Instagram API / Meta Business
- TikTok API
- LinkedIn API
- Scheduling tool (Buffer, Later, or custom)
- Analytics dashboards

**Output Examples:**
- 30-day content calendar
- Scheduled posts across platforms
- Campaign performance reports
- Influencer outreach lists

---

### 5. THE DEVELOPER — Web & Systems Specialist

| Attribute | Value |
|-----------|-------|
| **Role** | Web Developer / Systems Integrator |
| **Implementation** | Sub-agent |
| **Model** | Claude Sonnet (coding) |
| **Trigger** | "Build...", "Fix...", "Integrate...", "Automate..." |

**Responsibilities:**
- Website development (ecellglobal.com redesign)
- SaaS product development
- API integrations
- Automation scripts
- Legacy system improvements
- Internal tools

**Tools Needed:**
- Code editor access
- Git/GitHub
- Hosting platforms
- Database access
- API credentials

**Output Examples:**
- New ecellglobal.com B2B website
- SaaS product MVP
- Automated reporting scripts
- API integrations

---

### 6. THE WATCHER — Market Intelligence (Future)

*From the Autonomous Enterprise vision*

| Attribute | Value |
|-----------|-------|
| **Role** | Market Intelligence / Trend Spotter |
| **Implementation** | Scheduled agent |
| **Model** | Gemini 3 Pro (visual trend detection) |
| **Trigger** | Scheduled daily/weekly scans |

**Responsibilities:**
- Monitor competitor social channels
- Identify trending designs
- Track license popularity
- Alert on market opportunities
- Seasonal trend forecasting

**Tools Needed:**
- Social media scraping (Apify)
- Google Trends API
- Image analysis (Gemini)
- Alert system

---

### 7. THE GUARDIAN — Quality & Compliance (Future)

*From the Autonomous Enterprise vision*

| Attribute | Value |
|-----------|-------|
| **Role** | Quality Assurance / Brand Compliance |
| **Implementation** | Review agent |
| **Model** | Claude Opus (careful review) |
| **Trigger** | Before any external publish |

**Responsibilities:**
- Review content before posting
- Check brand guideline compliance
- Verify license usage rights
- Flag potential issues
- Maintain brand consistency

---

## 🔧 Implementation Priority

### Phase 1 — Now (Q1 2026)
| Specialist | Status | Priority |
|------------|--------|----------|
| Harry (Orchestrator) | ✅ Active | — |
| The Creator (Content) | 🔨 Build skill | HIGH |
| The Analyst (Data) | 🔨 Build skill | HIGH |
| The Designer (Visual) | ⏳ iMac setup | HIGH |

### Phase 2 — Next (Q2 2026)
| Specialist | Status | Priority |
|------------|--------|----------|
| The Marketer (Social) | 📋 Planned | MEDIUM |
| The Developer (Web) | 📋 Planned | MEDIUM |

### Phase 3 — Future
| Specialist | Status | Priority |
|------------|--------|----------|
| The Watcher (Intel) | 💡 Vision | LOW |
| The Guardian (QA) | 💡 Vision | LOW |

---

## 📋 Next Steps

1. **Set up iMac Node** — Unlocks Designer capabilities
2. **Build Content Creator skill** — Social post generation
3. **Build Data Analyst skill** — Sales/trend analysis
4. **Get sales data access** — Feed the Analyst
5. **Map social API access** — Instagram, TikTok posting

---

## 🔐 Security & Governance

- All specialists operate under Harry's coordination
- External actions (posting, emailing) require approval flow
- Sensitive data stays within secure perimeter
- Regular audits of agent actions
- Clear logging of all operations

---

*This roster will evolve as we build out capabilities.*
