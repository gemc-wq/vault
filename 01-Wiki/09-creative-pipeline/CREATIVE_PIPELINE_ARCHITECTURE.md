# Creative Pipeline Architecture
## "Concept to Cash" — Full Automation Flow

**Status:** Architecture Draft  
**Date:** 2026-02-07  
**Owner:** Harry (orchestration) + Jeff (design tooling)

---

## End-to-End Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRODUCT IDEA APP                             │
│  (Internal web app — React/Next.js on Vercel)                      │
│  • Enter new product idea (brand, device, design concept)          │
│  • Select target devices, categories, priority                     │
│  • Attach reference images / mood boards                           │
└──────────────┬──────────────────────────────────────────────────────┘
               │ writes to
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SUPABASE DB                                 │
│  Tables: products, designs, assets, content, approvals              │
│  • product_id, brand, device_list, status, created_by              │
│  • Realtime subscriptions for status changes                       │
│  • Storage bucket for design files + outputs                       │
└──────┬──────────────────┬───────────────────────────────────────────┘
       │ webhook/trigger  │ webhook/trigger
       ▼                  ▼
┌──────────────┐  ┌──────────────┐
│    ASANA     │  │    SLACK     │
│  Task created│  │  #designs    │
│  for designer│  │  notification│
└──────┬───────┘  └──────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DESIGNER (Photoshop)                              │
│  • Creates raw design file (.PSD / .PNG)                            │
│  • Uploads to Supabase Storage / Google Drive                       │
│  • Marks task "Ready for Review" in Asana                          │
└──────────────┬──────────────────────────────────────────────────────┘
               │ status → "pending_approval"
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    APPROVAL GATE #1                                  │
│  (In-app review — thumbnail + design preview)                       │
│  • Approve → triggers two parallel funnels                         │
│  • Reject → back to designer with notes                            │
└──────┬──────────────────┬───────────────────────────────────────────┘
       │                  │
       ▼                  ▼
┌──────────────────┐  ┌──────────────────────────────────────────────┐
│  IMAGE FUNNEL    │  │  CONTENT FUNNEL                              │
│  (N8N Workflow)  │  │  (N8N Workflow)                              │
│                  │  │                                              │
│  1. Fetch raw    │  │  1. Fetch product metadata from Supabase     │
│     design from  │  │  2. AI generates:                            │
│     Supabase     │  │     • Product title (SEO optimized)          │
│  2. Jeff's Gem   │  │     • Bullet points (per marketplace)        │
│     prompt →     │  │     • Description (Amazon, BigCommerce)      │
│     Gemini API   │  │     • Search keywords / tags                 │
│  3. Batch across │  │     • Social media copy                      │
│     all target   │  │  3. Save to Supabase (content table)         │
│     devices      │  │                                              │
│  4. Generate:    │  │  Model: GPT-5.2 or Gemini Flash              │
│     • Product    │  │                                              │
│       mockups    │  └──────────────────────────────────────────────┘
│     • Lifestyle  │
│       shots      │
│     • Amazon     │
│       listing    │
│       images     │
│  5. Save to      │
│     Supabase     │
│     Storage      │
│                  │
│  Model: Gemini   │
│  (Jeff's Gem)    │
└──────┬───────────┘
       │
       ▼ (both funnels complete)
┌─────────────────────────────────────────────────────────────────────┐
│                    APPROVAL GATE #2                                  │
│  (In-app review — images + content side by side)                    │
│  • Preview exactly how listing will look                           │
│  • Approve → feed to websites                                      │
│  • Reject individual items → re-run that funnel                    │
└──────────────┬──────────────────────────────────────────────────────┘
               │ status → "approved"
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTION (N8N Workflow)                       │
│  From Supabase → push to all channels via API:                     │
│  • Amazon SP-API (create/update listings)                          │
│  • BigCommerce (GoHeadCase.com) API                                │
│  • eBay API                                                        │
│  • Shopify micro-sites                                             │
│  • Social media (scheduled posts)                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Status |
|-----------|-----------|--------|
| **Product Idea App** | Next.js + Supabase Auth | 🔲 To Build |
| **Database** | Supabase (Postgres + Realtime + Storage) | 🔲 To Setup |
| **Task Management** | Asana (existing) | ✅ Connected |
| **Team Comms** | Slack (existing) | ✅ Connected |
| **Orchestration** | N8N (self-hosted) | ✅ Running |
| **Image Generation** | Gemini API (Jeff's custom Gem prompt) | ⏳ Awaiting prompt from Jeff |
| **Content Generation** | GPT-5.2 / Gemini Flash via N8N | ✅ API keys ready |
| **Distribution** | Amazon SP-API, BigCommerce, etc. | ⏳ SP-API application pending |

---

## N8N Workflows Needed

### 1. `design-approved` (Image Funnel)
**Trigger:** Supabase webhook on `designs.status = 'approved'`
1. Fetch raw design from Supabase Storage
2. Get target device list from product record
3. For each device → call Gemini API with Jeff's custom prompt
4. Generate: front mockup, angled mockup, lifestyle shot
5. Save all outputs to Supabase Storage
6. Update `assets` table with file references
7. Notify Slack #designs channel

### 2. `content-generation` (Content Funnel)  
**Trigger:** Supabase webhook on `designs.status = 'approved'`
1. Fetch product metadata (brand, device, design name, category)
2. Call AI (GPT-5.2) with marketplace-specific templates
3. Generate title, bullets, description, keywords per marketplace
4. Save to `content` table in Supabase
5. Mark as "content_ready"

### 3. `publish-to-marketplaces` (Distribution)
**Trigger:** Manual or on `products.status = 'fully_approved'`
1. Fetch approved images + content from Supabase
2. Format per marketplace requirements
3. Push via respective APIs (Amazon, BigCommerce, eBay)
4. Log results and update status

---

## Supabase Schema (Draft)

```sql
-- Products (one per concept)
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  brand TEXT,              -- 'Naruto', 'MCFC', 'LFC', etc.
  category TEXT,           -- 'anime', 'football', 'entertainment'
  target_devices TEXT[],   -- ['iphone-16-pro', 'samsung-s25', ...]
  priority TEXT DEFAULT 'normal',
  status TEXT DEFAULT 'draft',  -- draft → design → pending_approval → approved → published
  created_by UUID REFERENCES auth.users,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Designs (raw artwork per product)
CREATE TABLE designs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products,
  file_path TEXT,          -- Supabase Storage path
  file_type TEXT,          -- 'psd', 'png', 'ai'
  status TEXT DEFAULT 'pending',  -- pending → approved → rejected
  designer_notes TEXT,
  reviewer_notes TEXT,
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Assets (generated images)
CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products,
  design_id UUID REFERENCES designs,
  device TEXT,             -- 'iphone-16-pro'
  asset_type TEXT,         -- 'mockup_front', 'mockup_angled', 'lifestyle', 'transparent'
  file_path TEXT,          -- Supabase Storage path
  generation_prompt TEXT,  -- for traceability
  status TEXT DEFAULT 'pending_review',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Content (AI-generated copy)
CREATE TABLE content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products,
  marketplace TEXT,        -- 'amazon_us', 'amazon_uk', 'bigcommerce', 'ebay'
  title TEXT,
  bullets TEXT[],
  description TEXT,
  keywords TEXT[],
  status TEXT DEFAULT 'pending_review',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Approvals (audit trail)
CREATE TABLE approvals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type TEXT,        -- 'design', 'asset', 'content'
  entity_id UUID,
  action TEXT,             -- 'approved', 'rejected'
  reviewer UUID REFERENCES auth.users,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Key Dependencies / Blockers

1. **Jeff's Gemini Gem prompt** — needed to replicate his mockup generation process via API
2. **Supabase project setup** — need to create project + configure storage buckets
3. **Amazon SP-API credentials** — Cem has existing key, needs to share
4. **Product Idea App** — Ava to build (Next.js) or part of Control Centre?
5. **Gemini API access for image generation** — verify Gems can be called programmatically or if we need to extract/adapt the prompt for direct API use

---

## Open Questions

1. **Gemini Gems vs API:** Can custom Gems be called via API, or do we need to extract Jeff's prompt and call Gemini's image generation endpoint directly? Need to research this.
2. **Device templates:** Jeff's approach uses Gemini to generate the full mockup from a prompt. Our existing track1 tool uses Sharp to composite designs onto templates. Which approach for production?
3. **Approval UX:** In the Product Idea App, or separate? Slack-based approval buttons?
4. **Storage:** Supabase Storage vs Google Drive vs both? (Drive is good for designer access, Supabase for API access)
5. **Which marketplace APIs first?** Amazon SP-API is the biggest revenue driver.

---

*Created: 2026-02-07*

## Related
- [[wiki/03-production/PRINT_FILE_PIPELINE|Print File Pipeline]] — Downstream production
- [[wiki/06-design-automation/DESIGN_SYSTEM|Design System]] — Design file management
- [[wiki/23-drew-handover/BEA_CREATIVE_PROCESS|Bea Creative Process]] — Camera holes, image replication
- [[wiki/10-listingforge/PRODUCT_SPEC|ListingForge Product Spec]] — Listing automation
