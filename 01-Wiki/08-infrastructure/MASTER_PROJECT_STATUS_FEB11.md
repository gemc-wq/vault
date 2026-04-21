# Master Project Status — eCELL Global AI Transformation
*Last updated: 2026-02-11 04:45 UTC*

---

## Active Projects

### 1. 🟡 CS Automation (Email + Chatbot)
**Priority: HIGH | Blocked on: Email auth + Cloud SQL**

| Item | Status | Blocker |
|------|--------|---------|
| N8N CS Chat workflow | ✅ Live | — |
| N8N Email Draft workflow | 🟡 Created, inactive | App Password / OAuth |
| Marketplace rules research | ✅ Complete | — |
| eBay FAQ ingested | ✅ Done | — |
| Ticketing system decision | 🔴 Pending | Cem to evaluate options |
| Cloud SQL connection | 🔴 Pending | Connection details from Cem |
| eBay trial | 🔴 Pending | eBay credentials from Cem |
| Amazon integration | ⏸️ Future | SP-API setup needed |

**Docs:** `projects/cs-automation/`

---

### 2. 🟡 Supabase Migration & Sales Schema
**Priority: HIGH | Partially complete**

| Item | Status | Notes |
|------|--------|-------|
| Product types table (61 items) | ✅ Deployed | Category fix applied Feb 11 |
| Brands table (30 brands) | ✅ Deployed | — |
| Device types table (11 categories) | ✅ Deployed | — |
| Device type column on devices | ✅ Deployed | 2,636 devices categorized |
| Views + Functions + Indexes | ✅ Deployed | search, selectors, counts |
| Unified sales schema design | ✅ Complete | `projects/sales-schema/UNIFIED_SCHEMA.sql` |
| API reference docs (4 platforms) | ✅ Complete | Amazon, eBay, Etsy, BigCommerce |
| Platform ingestion map (29 platforms) | ✅ Documented | 21 API + 8 CSV |
| Schema deployment to Supabase | 🔴 Pending | Needs data to validate against |
| Sales data ingestion | 🔴 Pending | Cloud SQL connection needed |

**Docs:** `projects/sales-schema/` + `projects/ai-coo/`

---

### 3. 🟡 Production Workflow Automation
**Priority: HIGH | Deep-dive in progress**

| Item | Status | Notes |
|------|--------|-------|
| Swimlane flowchart analyzed | ✅ Done | `projects/production-workflow/flowchart-1.png` |
| Daily production workflow doc | ✅ Complete | Detailed deep-dive |
| Shipping carrier rules | ✅ Documented | UK, US, Europe, Amazon override |
| Print file pipeline documented | ✅ Documented | TIFF + EPS workflows, 5-7 staff |
| Site capability matrix | 🔴 Pending | Table from Cem needed |
| Veco transition (US/UK) | 🟡 Nearly complete | Europe/international still manual |
| Print file automation | 🔴 Pending | Deep-dive needed on EPS workflow |
| Gemini Vision packing verification | ⏸️ Design phase | Concept agreed |
| EPS workflow documentation | 🔴 Pending | In Google Drive shared folder |
| Camera hole obstruction examples | 🔴 Pending | From Cem |

**Docs:** `projects/production-workflow/`

---

### 4. ⏸️ Vertex AI RAG (Website Chatbot + Packing App)
**Priority: MEDIUM | Plan complete, awaiting build**

| Item | Status | Notes |
|------|--------|-------|
| Implementation plan | ✅ Complete | `projects/vertex-ai-rag/IMPLEMENTATION_PLAN.md` |
| Estimated cost | ✅ ~$100/month | Chatbot + packing verification |
| Build timeline | ✅ 3 weeks estimated | — |
| Google Cloud account | ✅ Available | Cem confirmed |
| Product image database | 🔴 Not started | Needed for RAG |
| Build | ⏸️ Waiting | Cloud SQL + Supabase first |

---

### 5. ⏸️ Design Automation (The Creator Agent)
**Priority: LOW | Future**

| Item | Status | Notes |
|------|--------|-------|
| Green screen template decision | ✅ Agreed | Chroma key approach |
| Image gen pipeline concept | ✅ Discussed | For Amazon listings |
| EPS/PSD file handling | 🔴 Complex | Camera hole issues |
| Reference images saved | ✅ Done | `projects/design-automation/` |

---

## Infrastructure

### Nodes
| Node | Status | Notes |
|------|--------|-------|
| AWS Server (Ubuntu) | ✅ Running | Primary — Harry's home |
| Cem's iMac | 🔴 Disconnected | Node pairing broken, fixing tomorrow |
| Windows PC (dedicated) | 📅 Tomorrow | Cem setting up dedicated machine |

### Services
| Service | Status | URL |
|---------|--------|-----|
| N8N | ✅ Running | http://localhost:5678 |
| Clawdbot Gateway | ✅ Running | Port 18789 |
| Supabase | ✅ Active | nuvspkgplkdqochokhhi |

### TTS
- **Provider:** ElevenLabs (switched from OpenAI — quota exhausted)
- **Voice ID:** 8Ln42OXYupYsag45MAUy
- **Pipeline:** ElevenLabs API → MP3 → ffmpeg → OGG/Opus → Telegram voice

---

## Pending Items from Cem

| Item | Context | Priority |
|------|---------|----------|
| Cloud SQL connection details | Screenshots from Google Cloud Console | 🔴 High |
| App Password for headcasedesigns@ | Google Workspace, for CS email bot | 🔴 High |
| eBay login credentials | For CS chatbot trial | 🟡 Medium |
| Product type → site capability table | Which products print at which sites | 🟡 Medium |
| EPS workflow documentation | From Google Drive shared folder | 🟡 Medium |
| Camera hole obstruction examples | Before/after failures from current script | 🟡 Medium |
| Windows PC node setup | Dedicated machine for Harry | 📅 Tomorrow |
| Current MySQL inventory database | For inventory management module | ⏸️ Later |

---

## SKU Structure Reference

```
HC-IPH16-HPOTDH37-HOP
│   │      │       │
│   │      │       └── Design variant (digital file)
│   │      └────────── Design/Lineup code (digital file)
│   └───────────────── Device model (stockable unit)
└───────────────────── Product type (physical product)
```

- **Physical inventory** = Product Type + Device (blank product)
- **Design** = everything after device code (digital file, applied at print time)

---

## Cost Structure

| Resource | Cost | Notes |
|----------|------|-------|
| Harry (Opus 4.6) | API key | COO/strategy only |
| Default model | Sonnet 4.5 | Switched from Opus to save costs |
| Sub-agents | Gemini Flash | Pennies |
| N8N CS bot | GPT-4o-mini via OpenRouter | ~$0.01/interaction |
| ElevenLabs TTS | Pay-per-use | Voice notes |

---

*This file is the single source of truth for project status. Update after each working session.*
