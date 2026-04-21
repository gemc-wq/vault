# ListingForge — Product Specification
## AI-Powered Amazon Listing Image & Content Generator

**Version:** 1.0 Draft  
**Date:** 2026-02-08  
**Author:** Harry (Lead Automator)  
**Builder:** Ava (Lead Strategist / Claude Code)  
**Stakeholder:** Cem Celikkol (CEO, Ecell Global)

---

## 1. Vision

**One-liner:** Upload a product photo → get Amazon-ready listing images and optimized content in minutes.

**Long-term:** A SaaS app where any Amazon seller can take a photo on their phone, and the AI generates professional, Amazon-compliant listing images + SEO-optimized copy — eliminating the need for expensive product photography and copywriters.

**Strategy:** Build as an internal tool for Head Case Designs first. Dogfood with 8,000+ designs across 300+ devices. Once production-ready and proven, flip the switch to a public SaaS product.

---

## 2. Phases

### Phase 1 — Internal Tool (MVP)
- Head Case team only (Google SSO, company emails)
- Upload raw design files (.PNG, .PSD exports)
- Select target devices from Head Case device catalog
- AI generates Amazon-ready mockup images per device
- AI generates listing content (title, bullets, description, keywords)
- Review & approve workflow
- Export approved assets (download or push to marketplace)

### Phase 2 — Enhanced Internal
- Batch processing (upload multiple designs, auto-generate across all devices)
- Template management (save prompt templates per brand/license)
- Integration with Amazon SP-API (direct listing push)
- Integration with BigCommerce API (GoHeadCase.com)
- Analytics dashboard (generation stats, approval rates, time saved)

### Phase 3 — Public SaaS
- Public signup with Stripe billing (freemium: 5 free generations/month)
- Onboarding wizard for Amazon sellers
- Mobile-first photo capture (phone camera → AI processing)
- Broader product categories (not just phone cases)
- Usage tiers and API access for power sellers
- White-label option for agencies

---

## 3. Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| **Frontend** | Next.js 14+ (App Router) | React, responsive, SSR, Vercel-native |
| **Styling** | Tailwind CSS + shadcn/ui | Clean, modern, fast to build |
| **Backend** | Next.js API Routes | Same codebase, serverless |
| **Database** | Supabase (PostgreSQL) | Auth, Realtime, Storage, Row-Level Security |
| **File Storage** | Supabase Storage | Images, designs, generated assets |
| **Auth** | Supabase Auth (Google SSO) | Phase 1: company emails only. Phase 3: public signup |
| **AI — Images** | Google Gemini API (image generation) | Jeff's proven prompt approach for mockups |
| **AI — Content** | Gemini Flash / GPT-5.2 via API | SEO-optimized listing copy |
| **Hosting** | Vercel | Existing account (gemc99-boop), free tier works for internal |
| **Payments** | Stripe (Phase 3 only) | Industry standard for SaaS billing |

---

## 4. Database Schema (Supabase)

```sql
-- ============================================
-- USERS & TEAMS
-- ============================================

-- Extends Supabase auth.users
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users,
  full_name TEXT,
  avatar_url TEXT,
  role TEXT DEFAULT 'member',  -- 'admin', 'manager', 'member'
  team TEXT DEFAULT 'headcase', -- Phase 1: always 'headcase'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- DEVICE CATALOG
-- ============================================

CREATE TABLE devices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand TEXT NOT NULL,         -- 'Apple', 'Samsung', 'Google'
  model TEXT NOT NULL,         -- 'iPhone 16 Pro', 'Galaxy S25 Ultra'
  slug TEXT UNIQUE NOT NULL,   -- 'iphone-16-pro', 'samsung-galaxy-s25-ultra'
  category TEXT,               -- 'phone', 'tablet', 'watch'
  dimensions JSONB,            -- { width: 1440, height: 3200 } for image sizing
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- PRODUCTS (one per design concept)
-- ============================================

CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,            -- 'Naruto Shippuden Seal'
  brand TEXT,                    -- 'Naruto', 'MCFC', 'LFC', 'Peanuts'
  category TEXT,                 -- 'anime', 'football', 'entertainment', 'classic'
  license TEXT,                  -- 'NFL', 'WWE', 'Harry Potter', etc.
  target_devices UUID[],         -- references devices.id
  priority TEXT DEFAULT 'normal', -- 'urgent', 'high', 'normal', 'low'
  status TEXT DEFAULT 'draft',   -- draft → uploaded → generating → review → approved → published
  tags TEXT[],                   -- flexible tagging
  notes TEXT,
  created_by UUID REFERENCES auth.users,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- DESIGNS (raw uploaded artwork)
-- ============================================

CREATE TABLE designs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products ON DELETE CASCADE,
  file_path TEXT NOT NULL,       -- Supabase Storage path
  file_name TEXT,
  file_type TEXT,                -- 'png', 'jpg', 'psd'
  file_size BIGINT,
  thumbnail_path TEXT,           -- auto-generated thumbnail
  status TEXT DEFAULT 'uploaded', -- uploaded → approved → rejected
  reviewer_notes TEXT,
  uploaded_by UUID REFERENCES auth.users,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- GENERATED ASSETS (AI-created images)
-- ============================================

CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products ON DELETE CASCADE,
  design_id UUID REFERENCES designs ON DELETE CASCADE,
  device_id UUID REFERENCES devices,
  asset_type TEXT NOT NULL,      -- 'main_image', 'mockup_front', 'mockup_angled', 'lifestyle', 'infographic', 'a_plus'
  file_path TEXT NOT NULL,       -- Supabase Storage path
  thumbnail_path TEXT,
  generation_prompt TEXT,        -- for traceability & iteration
  generation_model TEXT,         -- 'gemini-pro', etc.
  generation_time_ms INTEGER,
  status TEXT DEFAULT 'pending_review', -- pending_review → approved → rejected → regenerating
  reviewer_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- GENERATED CONTENT (AI-created copy)
-- ============================================

CREATE TABLE content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products ON DELETE CASCADE,
  marketplace TEXT NOT NULL,     -- 'amazon_us', 'amazon_uk', 'amazon_de', 'bigcommerce', 'ebay'
  title TEXT,
  bullets TEXT[],                -- array of bullet points
  description TEXT,
  search_keywords TEXT[],
  backend_keywords TEXT[],       -- Amazon hidden keywords
  generation_model TEXT,
  status TEXT DEFAULT 'pending_review',
  reviewer_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- APPROVAL LOG (audit trail)
-- ============================================

CREATE TABLE approvals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type TEXT NOT NULL,     -- 'design', 'asset', 'content', 'product'
  entity_id UUID NOT NULL,
  action TEXT NOT NULL,          -- 'approved', 'rejected', 'regenerate'
  reviewer_id UUID REFERENCES auth.users,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- GENERATION JOBS (async processing tracker)
-- ============================================

CREATE TABLE generation_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products ON DELETE CASCADE,
  job_type TEXT NOT NULL,        -- 'image_generation', 'content_generation', 'batch'
  status TEXT DEFAULT 'queued',  -- queued → processing → completed → failed
  total_items INTEGER DEFAULT 0,
  completed_items INTEGER DEFAULT 0,
  error_message TEXT,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_assets_product ON assets(product_id);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_content_product ON content(product_id);
CREATE INDEX idx_generation_jobs_status ON generation_jobs(status);

-- ============================================
-- ROW LEVEL SECURITY (Phase 1: team-only)
-- ============================================

ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE designs ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE content ENABLE ROW LEVEL SECURITY;

-- Phase 1: All authenticated users in 'headcase' team can CRUD everything
CREATE POLICY "Team access" ON products FOR ALL USING (
  auth.uid() IN (SELECT id FROM profiles WHERE team = 'headcase')
);
CREATE POLICY "Team access" ON designs FOR ALL USING (
  auth.uid() IN (SELECT id FROM profiles WHERE team = 'headcase')
);
CREATE POLICY "Team access" ON assets FOR ALL USING (
  auth.uid() IN (SELECT id FROM profiles WHERE team = 'headcase')
);
CREATE POLICY "Team access" ON content FOR ALL USING (
  auth.uid() IN (SELECT id FROM profiles WHERE team = 'headcase')
);
```

---

## 5. UI / UX Flow

### 5.1 Dashboard (Home)
- Overview cards: Products in pipeline, pending reviews, recently published
- Quick action: "+ New Product" button
- Recent activity feed

### 5.2 New Product Flow
1. **Product Info** — Name, brand, license, category, tags
2. **Upload Design** — Drag & drop raw design file (PNG/JPG). Preview shown.
3. **Select Devices** — Grid of available devices with checkboxes. Search/filter by brand. "Select All" per brand.
4. **Review & Submit** — Summary of selections → "Generate" button

### 5.3 Generation Progress
- Real-time progress bar (Supabase Realtime subscription)
- Per-device status: queued → generating → done
- Estimated time remaining
- Content generation runs in parallel with image generation

### 5.4 Review & Approve
- **Image Review:** Gallery grid of all generated mockups per device
  - Side-by-side: original design vs generated mockup
  - Approve / Reject / Regenerate per image
  - Bulk approve/reject
- **Content Review:** Marketplace-tabbed view
  - Title, bullets, description shown per marketplace
  - Inline editing (tweak AI output before approving)
  - Approve / Reject / Regenerate per marketplace
- **Final Approval:** Once all images + content approved → product status = "approved"

### 5.5 Export / Publish
- **Download:** ZIP of all approved images (named per Amazon convention)
- **Copy Content:** One-click copy per marketplace (title + bullets + description)
- **Push to Marketplace (Phase 2):** Direct API push to Amazon / BigCommerce / eBay

### 5.6 Product Catalog
- Table/grid view of all products
- Filter by: status, brand, license, device, date
- Search by name
- Bulk actions (batch generate, batch approve)

---

## 6. AI Integration

### 6.1 Image Generation (Gemini API)

**Input:** Raw design file (PNG) + device specification  
**Output:** Amazon-compliant product images

**Image types to generate per device:**
1. **Main Image** — White background, product only, fills 85%+ of frame (Amazon requirement)
2. **Front Mockup** — Case on device, slight shadow, white background
3. **Angled Mockup** — 3/4 angle view, case on device
4. **Lifestyle Shot** — Case in context (desk, hand, pocket) — optional
5. **Infographic** — Key features callout overlay — Phase 2

**Existing GPT approach (from Notion — use as starting point):**
1. **Input:** Design brief/raw artwork → theme, style, elements
2. **Generation:** API call to image model (DALL-E 3 / Gemini) → generates variants
3. **Selection:** Human QA or AI Vision agent picks best
4. **Processing:** Upscale → remove background → vectorize if needed
5. **Mockup:** Overlay design on phone case template (Smart Object automation or programmatic compositing)
6. **Output:** Save to storage + create listing draft

**Brand consistency (from Notion "Prompt Book" concept):**
- Defined parameters for consistent AI-generated product shots (lighting, style, angles)
- System prompt defining brand voice for content generation
- Trained on "Brand DNA" so agents don't generate off-brand content

**Prompt template structure (refine iteratively):**
```
Generate a professional product photography image of a phone case with the following design: [DESIGN_DESCRIPTION]
Device: [DEVICE_MODEL]
Shot type: [SHOT_TYPE]
Requirements:
- White/clean background
- Photorealistic rendering
- Case properly fitted to device
- High resolution (2000x2000px minimum)
- Amazon product listing compliant
- Consistent lighting (soft studio, slight shadow)
- Design accurately represented on case surface
```

**Reference:** Jeff (designer) has a working Gemini Gem that produces quality mockups — Cem is creating a new prompt. Reference images in Drive: `design-automation/reference-images/`

### 6.2 Content Generation (Gemini Flash / GPT-5.2)

**Input:** Product metadata (name, brand, device, category, license)  
**Output:** Marketplace-specific listing content

**Per marketplace:**
- **Amazon US/UK/DE:** Title (200 char max), 5 bullet points, HTML description, search terms (250 bytes), backend keywords
- **BigCommerce:** Product title, description (HTML), SEO meta description
- **eBay:** Item title (80 char), item description, item specifics

**Prompt should include:**
- Brand guidelines / tone of voice per license
- SEO best practices per marketplace
- Character/byte limits per field
- Competitor analysis data for keyword optimization

---

## 7. API Routes

```
POST   /api/products              — Create new product
GET    /api/products              — List products (with filters)
GET    /api/products/[id]         — Get product detail
PATCH  /api/products/[id]         — Update product
DELETE /api/products/[id]         — Delete product

POST   /api/designs/upload        — Upload raw design file
GET    /api/designs/[id]          — Get design detail

POST   /api/generate/images       — Trigger image generation for product
POST   /api/generate/content      — Trigger content generation for product
GET    /api/generate/status/[jobId] — Check generation job status

POST   /api/assets/[id]/approve   — Approve generated asset
POST   /api/assets/[id]/reject    — Reject with notes
POST   /api/assets/[id]/regenerate — Re-run generation

POST   /api/content/[id]/approve  — Approve generated content
POST   /api/content/[id]/reject   — Reject with notes
PATCH  /api/content/[id]          — Edit content inline

GET    /api/export/[productId]    — Download ZIP of approved assets
POST   /api/publish/[productId]   — Push to marketplace (Phase 2)

GET    /api/devices               — List device catalog
POST   /api/devices               — Add device to catalog
```

---

## 8. Design & Branding

- Match Ecell Global / Head Case brand identity
- Clean, modern, minimal — white/grey palette with blue accents
- Responsive: works on desktop and mobile browsers
- Dark mode support (nice-to-have)
- Reference: Head Case website aesthetic, Orbit PM styling

---

## 9. Environment & Deployment

### Development
- Local dev: `npm run dev` (Next.js)
- Supabase local: `supabase start` (Docker)
- Environment variables in `.env.local`

### Production
- Vercel deployment (gemc99-boop account)
- Supabase cloud project (new project needed)
- Custom domain: TBD (e.g., `forge.ecellglobal.com` or `listingforge.com`)

### Required Environment Variables
```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
GOOGLE_GEMINI_API_KEY=
OPENAI_API_KEY=          # for content generation fallback
VERCEL_URL=
```

---

## 10. Reference Files

Available in Google Drive (`Clawdbot Shared Folder/design-automation/`):
- `reference-images/` — Mockup examples from Jeff (Naruto, MCFC, LFC)
- Pattern: dual-angle shots, white background, realistic case transparency
- Key: one raw design → multiple device mockups automatically

Existing internal apps for reference:
- **FBA Planner** — Python Streamlit on Cloud Run (similar internal tool pattern)
- **Sales Dashboard** — React/Express/Firestore on Cloud Run
- **Orbit PM** — Next.js on Vercel (Ava's build, good styling reference)

---

## 11. Success Metrics (Phase 1)

- Generate Amazon-ready images for a product across 10+ devices in under 5 minutes
- 80%+ first-pass approval rate (images don't need regeneration)
- Content generation matches or exceeds manually written listing quality
- Head Case team actively using it for new product launches

---

## 12. Open Questions / Dependencies

1. **Supabase project** — needs to be created (Cem or Harry to set up)
2. **Jeff's Gemini prompt** — critical for image generation quality. Cem has asked Jeff to share.
3. **Device catalog seed data** — need full list of Head Case's 300+ supported devices
4. **Amazon SP-API credentials** — Cem has existing key, needed for Phase 2 marketplace push
5. **App name** — working title "ListingForge" — confirm or change?
6. **Domain** — `forge.ecellglobal.com`? `listingforge.com`? `listingforge.app`?

---

## 13. Handoff Notes for Ava

**Ava — this is your build.** Use Claude Code + Codex (free on iMac).

**Priority order:**
1. Set up Next.js project with Supabase integration
2. Build the database schema (run migrations)
3. Build the UI flow: New Product → Upload → Select Devices → Generate
4. Integrate Gemini API for image generation (start with a placeholder prompt, we'll refine with Jeff's approach)
5. Integrate content generation (Gemini Flash for MVP)
6. Build the review/approve workflow
7. Export functionality (ZIP download)
8. Deploy to Vercel

**Styling:** Use Tailwind + shadcn/ui. Match the Orbit PM aesthetic you already built. Clean, minimal, Ecell brand colours.

**Don't block on:**
- Jeff's prompt — use a reasonable placeholder, we'll swap in the real one
- Amazon SP-API — that's Phase 2
- Stripe — that's Phase 3

**Do prioritize:**
- Clean, reusable architecture (this becomes a SaaS product later)
- Mobile-responsive from day one
- Good UX on the review/approve flow (this is where the team will spend most time)

---

*Spec created: 2026-02-08 by Harry*  
*For: Ava (Builder) | Approved by: Cem (CEO)*
