# Ecell Global — Master Business Process Blueprint
> Source: Cem's business process docs (Feb 8, 2026)
> PDF flowchart + DOCX brief saved in this folder
> Status: DRAFT — Mapping to automation plan

---

## Process Flow Overview

### Phase 1: IDEATION (Two Entry Points)

#### 1A. Human-Driven
- Cem or team enters new design/product idea
- Input: Database or Google Sheet
- Record in Ideation Intake
- **Approval gate:** Vet/approve idea → Yes = proceed, No = archive

#### 1B. AI-Driven (The Watcher)
- AI social channel research + trend listening
- Scrape using Apify (trending brands, tech accessories)
- Generate presentation and drop in Google Drive
- **Approval gate:** Same vet/approve step

### Phase 2: PRODUCT DEVELOPMENT (Parallel Tracks)

Once idea is approved → Create Product Master record

#### Track A: Images (Creative Team)
1. Creative designer creates mockup from assets
2. **Approval gate:** Mockup approved?
3. → AI automation generates full product imagery
4. → Upload to CDN
5. → Add image links to Product Master DB

#### Track B: Written Content (Listings Team)
1. Competitor/social scraping for context
2. Keywords research (Google Trends + Helium 10)
3. Top-selling competing products identified from Amazon
4. All input fed to Claude Sonnet 4.5
5. AI drafts listings (title, bullet points, description)
6. **Human review** of written content
7. → Save to Product Master DB

### Phase 3: QA
- Vet images + content together
- **Approval gate:** Pass QA? → Yes = proceed, No = rework (loop back)

### Phase 4: GO LIVE
- Batch list products via API
- Push to ecommerce platforms (Amazon, eBay, website)
- Product goes live

### Phase 5: MARKETING
- AI generates marketing content suggestions for various platforms
- **Approval gate:** Human approves
- Push to social/ad platforms
- Published → End

---

## Approval Gates Summary (Human-in-the-Loop)

| Gate | Phase | Decision |
|------|-------|----------|
| Idea Approval | Ideation | Proceed / Archive |
| Mockup Approval | Product Dev (Images) | Proceed / Rework |
| Content Review | Product Dev (Written) | Proceed / Rework |
| QA Check | QA | Pass / Rework |
| Marketing Approval | Marketing | Publish / Reject |

## Color Legend (from Flowchart)
- 🟣 **Purple** = AI tasks (automated)
- 🔵 **Blue** = Human tasks
- 🟠 **Orange** = Approval/Review gates

---

## Automation Mapping (TODO)

| Step | Current | Target | Owner | Tool |
|------|---------|--------|-------|------|
| Trend scraping | Manual | AI automated | Harry (Radar agent) | Apify + N8N |
| Presentation gen | Manual | AI automated | Harry (Prism agent) | Gamma API |
| Mockup creation | Human designer | AI-assisted | Ava (Iris agent) | Gemini Pro / Image Gen |
| Product imagery | Human designer | AI automated | Ava (Iris agent) | Image Maker pipeline |
| CDN upload | Manual | Automated | Harry (Nexus agent) | N8N + S3/CDN API |
| Keyword research | Manual | AI automated | Harry (Radar agent) | Google Trends + Helium 10 API |
| Competitor scraping | Manual | AI automated | Harry (Radar agent) | Apify + analysis |
| Listing copy | Manual | AI drafted | Ava (Echo agent) | Claude Sonnet 4.5 |
| Batch listing push | Semi-manual | API automated | Harry (Pixel agent) | Amazon SP-API + channel APIs |
| Marketing content | Manual | AI suggested | Ava (Echo agent) | LLM + templates |
| Social publishing | Manual | AI + approval | Harry (Nexus agent) | N8N + platform APIs |

---

## Supabase Tables Needed

### Core
- `ideas` — Ideation pipeline (source, status, approval)
- `products` — Product Master record
- `designs` — Design assets linked to products
- `images` — Product images (mockup → final, CDN URLs)
- `content` — Written content (titles, bullets, descriptions)
- `listings` — Where products are live (platform, status, URL)

### Supporting
- `trends` — Raw scraped trend data
- `competitors` — Competitor analysis data
- `keywords` — Keyword research results
- `marketing_content` — Generated marketing assets
- `approvals` — Approval queue (all gates in one table)

---

---

## Supporting Document: Implementation Plan (PPTX)

Full 6-week implementation plan saved as `IMPLEMENTATION_PLAN.pptx`.
Originally prepared with Airtable as the data hub — **we're replacing with Supabase**.

### Key Differences from Original Plan vs Our Setup

| Original Plan | Our Setup | Notes |
|---------------|-----------|-------|
| Airtable | **Supabase** | More powerful, SQL, free tier, API |
| Claude Max (coding) | **Ava has Claude Code FREE** | No $200/mo cost |
| DALL-E 3 | **Gemini Pro + our Image Maker** | Better quality, already set up |
| Hire/contractor ($50-80K) | **Harry + Ava** | We ARE the technical team |
| n8n Cloud ($20/mo) | **N8N self-hosted (free)** | Already running on VPS |
| Helium 10 only | **Apify + Helium 10 + custom scrapers** | More flexible |
| Asana | **Notion + Supabase approval queue** | Already in ecosystem |
| Slack alerts | **Telegram + Slack** | Both available |

### Cost Comparison
- **Original estimate:** $280-410/mo + $50-80K hire
- **Our actual cost:** ~$50-100/mo (API calls only) + $0 build cost (Harry + Ava)

### Timeline Adjustment
Original 6-week plan is aggressive but achievable. Key adjustment:
- Weeks 1-2: We're already past this (accounts, APIs, competitor monitoring exist)
- Weeks 3-4: Current priority — Supabase schema + content automation
- Weeks 5-6: Publishing + go-live

*Draft: 2026-02-09 — Awaiting Cem's review*
