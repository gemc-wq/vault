# ListingForge Pipeline Vision — Ideation to Marketing
**Version:** 1.0 | **Date:** 2026-04-09
**Author:** Cem (brain dump) + Athena (structured draft)
**Status:** DRAFT — for review and expansion
**References:** Operational Blueprint V3, LISTINGFORGE_PROJECT_BRIEF_V1, DRECO Architecture Brief

---

## 1. The Vision

A single, AI-managed pipeline that starts the moment a license is signed (or a new range is commissioned) and flows automatically through to live listings AND marketing assets — with human approval only at critical gates.

**One data entry point. Everything downstream is automated or AI-assisted.**

```
LICENSE SIGNED / NEW RANGE
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 1: IDEATION & CONTEXT CAPTURE                                │
│  ─────────────────────────────────────                              │
│  • License metadata entered (brand, licensor, royalty %, territory) │
│  • LLM auto-generates:                                             │
│      - Target demographic profile                                   │
│      - Lifestyle context keywords                                   │
│      - Brand colour palette + mood                                  │
│      - Marketing angle (sports/anime/fashion/kids/etc.)             │
│  • Human reviews + approves context (GATE 1)                       │
│                                                                     │
│  Output: marketing_attributes row in DB per license/brand           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 2: DESIGN CREATION                                           │
│  ────────────────────────                                           │
│  • Creative brief auto-generated from Stage 1 context               │
│  • PH design team creates Master PSD (1 per design)                │
│  • Design registered in DB with design_code, license link           │
│  • Human approves design (GATE 2)                                  │
│                                                                     │
│  Output: Approved Master PSD + design_code in DB                    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 3: LISTING IMAGE GENERATION (ListingForge)                   │
│  ────────────────────────────────────────────────                   │
│  3A. Main Image (I1)                                                │
│      • Composition engine: Master PSD + jig data + device mockup    │
│      • Pure white #FFFFFF background (Amazon compliant)             │
│      • Automated across ALL devices via format mapping              │
│                                                                     │
│  3B. Feature/Lifestyle Images (I2-I5) ← THIS IS THE KEY EXTENSION  │
│      • AI reads marketing_attributes from Stage 1                   │
│      • Generates CONTEXTUAL backdrops driven by brand identity:     │
│                                                                     │
│        ┌─────────────────┬──────────────────────────────────────┐   │
│        │ License/Brand   │ Lifestyle Context (LLM-generated)   │   │
│        ├─────────────────┼──────────────────────────────────────┤   │
│        │ Powerpuff Girls │ Pastel pink/red palette, youthful,  │   │
│        │                 │ bedroom desk, colourful accessories  │   │
│        ├─────────────────┼──────────────────────────────────────┤   │
│        │ Snoopy/Peanuts  │ Warm, nostalgic, younger female     │   │
│        │                 │ audience, cozy home setting          │   │
│        ├─────────────────┼──────────────────────────────────────┤   │
│        │ NFL (generic)   │ Tailgate party, beer on table,      │   │
│        │                 │ outdoor, adult male sports fan       │   │
│        ├─────────────────┼──────────────────────────────────────┤   │
│        │ Real Madrid     │ Sports bar, atmospheric lighting,    │   │
│        │                 │ wooden table, adult, aspirational    │   │
│        ├─────────────────┼──────────────────────────────────────┤   │
│        │ Naruto          │ Urban/modern, anime aesthetic,       │   │
│        │                 │ moody lighting, teen/young adult     │   │
│        ├─────────────────┼──────────────────────────────────────┤   │
│        │ One Piece       │ Adventure, vibrant, ocean/nautical,  │   │
│        │                 │ young adult, energetic               │   │
│        └─────────────────┴──────────────────────────────────────┘   │
│                                                                     │
│      • Base composition: phone on flat surface, angled view         │
│      • Backdrop CHANGES per brand, driven by lifestyle context      │
│      • Image gen: Gemini 3 Flash Image / Nano Banana 2             │
│      • Human spot-checks sample (GATE 3 — sampling, not every SKU) │
│                                                                     │
│  Output: 5 images per device SKU, uploaded to S3                    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 3.5: MARKETING ASSET GENERATION ← NEW STAGE                 │
│  ────────────────────────────────────────────────                   │
│  Same lifestyle context from Stage 1 + same lifestyle images from  │
│  Stage 3B are repurposed into marketing assets:                     │
│                                                                     │
│  A. SOCIAL MEDIA POSTS                                              │
│     • Lifestyle image cropped/formatted for Instagram, Facebook,    │
│       TikTok dimensions                                             │
│     • LLM generates caption + hashtags from brand context           │
│     • Output: ready-to-post assets per platform                     │
│                                                                     │
│  B. EMAIL CAMPAIGN IMAGES                                           │
│     • Hero banner from best lifestyle image                         │
│     • GoHeadCase email template populated automatically             │
│     • Feeds into Klaviyo/Shopify Email (11K subscribers, 0 campaigns│
│       sent = massive untapped opportunity)                          │
│                                                                     │
│  C. A+ CONTENT / ENHANCED BRAND CONTENT                             │
│     • Amazon A+ and Walmart Rich Media modules                      │
│     • Lifestyle images + product story auto-composed                │
│     • Brand-specific template per marketplace                       │
│                                                                     │
│  Output: Social assets, email banners, A+ content modules           │
│  Human approves marketing batch (GATE 4)                            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 4: CONTENT & SKU PREP                                        │
│  ───────────────────────────                                        │
│  • LLM writes listing copy (title, bullets, description) using      │
│    the SAME brand context from Stage 1                              │
│  • SKU generated: product_type + device + design_code + variant     │
│  • EAN/GTIN assigned                                                │
│  • All content blocks assembled (images + copy + SKU + EAN)         │
│                                                                     │
│  Output: Complete listing-ready content package per SKU              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STAGE 5: GO LIVE                                                   │
│  ───────────                                                        │
│  • Auto-push to marketplaces (Amazon, Walmart, Shopify, OnBuy,     │
│    Kaufland, Target+)                                               │
│  • Marketing assets scheduled for social + email                    │
│  • Daily monitoring via EOD reports + PULSE dashboard               │
│                                                                     │
│  Output: Live listings + active marketing campaigns                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. The Key Insight

**One context entry drives everything.**

When someone enters "Powerpuff Girls" as a license, the LLM immediately knows:
- Target audience: younger female, 8-16
- Colour palette: pinks, reds, pastels, bright
- Lifestyle setting: bedroom desk, colourful accessories, playful
- Marketing tone: fun, girly, vibrant
- Social hashtags: #PowerpuffGirls #PhoneCase #GirlPower

That same context object drives:
1. The creative brief for the PH design team
2. The AI backdrop prompts for listing images
3. The product copy for listings
4. The social media post captions
5. The email campaign hero images
6. The A+ content modules

**No one specs this manually for each step.** The LLM generates it once at ideation, a human approves it once, and it flows through the entire pipeline.

---

## 3. The marketing_attributes Table

```sql
CREATE TABLE marketing_attributes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_id UUID REFERENCES licenses(id),
    brand_name TEXT NOT NULL,           -- 'Powerpuff Girls'
    target_demographic TEXT,            -- 'younger female, 8-16'
    colour_palette TEXT[],              -- ['#FF69B4', '#FF1493', '#FFB6C1']
    mood_keywords TEXT[],               -- ['playful', 'vibrant', 'girly']
    lifestyle_setting TEXT,             -- 'bedroom desk, colourful accessories'
    lifestyle_surface TEXT,             -- 'white desk', 'wooden bar table', 'concrete bench'
    lifestyle_props TEXT[],             -- ['colourful stickers', 'hair clips', 'notebook']
    backdrop_prompt TEXT,               -- Full prompt for AI image gen
    marketing_tone TEXT,                -- 'fun, energetic'
    social_hashtags TEXT[],             -- ['#PowerpuffGirls', '#PhoneCase']
    age_rating TEXT,                    -- 'all-ages', 'teen', 'adult'
    gender_skew TEXT,                   -- 'female', 'male', 'neutral'
    category TEXT,                      -- 'anime', 'sports', 'fashion', 'kids', 'music'
    llm_generated BOOLEAN DEFAULT true, -- Was this auto-generated?
    human_approved BOOLEAN DEFAULT false,
    approved_by TEXT,
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**LLM auto-populates this at license onboarding.** Human reviews and approves. All downstream stages read from it.

---

## 4. Human Gates (Approval Points)

| Gate | Stage | Who | What they approve |
|------|-------|-----|-------------------|
| GATE 1 | Ideation | Cem / Bea | Brand context + lifestyle keywords |
| GATE 2 | Design | Bea / Creative Lead | Master PSD artwork |
| GATE 3 | Listing Images | Bea (sampling) | Spot-check 3-5 device renders per design |
| GATE 4 | Marketing Assets | Cem / Marketing | Social posts + email campaigns before publish |

Everything between gates is fully automated.

---

## 5. What Exists vs. What Needs Building

| Component | Status | Where |
|-----------|--------|-------|
| License onboarding (Stage 1) | Blueprint V3 specced, tables in progress | Jay Mark building ecell.app |
| marketing_attributes table | Specced in DRECO brief, not yet in Supabase | This document defines schema |
| LLM context generation | Concept proven in DRECO Module A | Needs building |
| Design creation (Stage 2) | Existing PH workflow | No change needed |
| Main listing image (Stage 3A) | POC working — 12 iPhones verified | ListingForge repo |
| Lifestyle images (Stage 3B) | Feature images experimental, Gemini stub | Needs Gemini integration |
| Marketing assets (Stage 3.5) | NOT BUILT — new stage | Needs full build |
| Content/SKU prep (Stage 4) | Partially automated via existing tools | Needs integration |
| Go Live (Stage 5) | Walmart Lister built, Shopify live | Needs unified push |

---

## 6. Priority Build Order

1. **marketing_attributes table in Supabase** — foundation for everything
2. **LLM context generator** — auto-populate marketing_attributes from license name
3. **Gemini lifestyle image integration** — replace experimental feature images with brand-contextual backdrops
4. **Marketing asset formatter** — crop/resize lifestyle images for social + email dimensions
5. **LLM copy generator** — listing titles, bullets, descriptions from same context
6. **Social post pipeline** — caption + hashtag generation, platform-specific formatting
7. **Email campaign pipeline** — GoHeadCase hero banners + Klaviyo/Shopify Email integration

---

*This document captures Cem's vision for the end-to-end pipeline. It should be read alongside the Operational Blueprint V3 and the ListingForge handoff documents.*
