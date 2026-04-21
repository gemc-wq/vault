# ListingForge — One Pager
**Ecell Global | April 2026**

---

## The Problem

Every new license launch requires manual work at every step — creative briefs, image generation, listing copy, social posts, email campaigns. Each step is siloed. Brand context is re-specified (or lost) at each handoff. With 1.89M SKUs across dozens of licenses, this doesn't scale.

## The Solution: One Entry, Full Pipeline

**ListingForge** is an AI-managed pipeline that turns a single license onboarding into live listings AND marketing assets — automatically.

```
 LICENSE SIGNED
      │
      ▼
 ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
 │  IDEATION     │───▶│  DESIGN      │───▶│  IMAGES      │───▶│  MARKETING   │───▶│  GO LIVE     │
 │               │    │              │    │              │    │              │    │              │
 │ LLM generates │    │ PH team      │    │ Main (white) │    │ Social posts │    │ Amazon       │
 │ brand context │    │ creates      │    │ + 4 lifestyle│    │ Email banners│    │ Walmart      │
 │ demographics  │    │ Master PSD   │    │ AI backdrops │    │ A+ content   │    │ Shopify      │
 │ palette/mood  │    │              │    │ per brand    │    │              │    │ OnBuy + more │
 └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────────────┘
     GATE 1              GATE 2              GATE 3              GATE 4
   (Cem/Bea)          (Bea/Lead)          (sampling)          (Cem/Mktg)
```

**4 human gates. Everything between them is fully automated.**

## The Key Insight

**One context entry drives everything.** When "One Piece" is entered as a license, the LLM instantly knows:

| Attribute | Value |
|-----------|-------|
| Audience | Young adult, 16-25, male-skewing |
| Palette | Vibrant reds, blues, yellows |
| Setting | Ocean/nautical, adventure |
| Tone | Energetic, bold |
| Hashtags | #OnePiece #LuffyPhoneCase #Anime |

That same context object auto-generates: creative briefs → AI backdrop prompts → listing copy → social captions → email hero images → A+ modules. **Nobody re-specs it at each step.**

## What's Built vs. What's Needed

| Component | Status |
|-----------|--------|
| Main listing image engine (Stage 3A) | **POC working** — 12 iPhones verified |
| License onboarding (Stage 1) | Specced in Blueprint V3, Jay Mark building |
| Design workflow (Stage 2) | Existing PH process — no change needed |
| AI lifestyle backdrops (Stage 3B) | Experimental — needs Gemini integration |
| Marketing assets (Stage 3.5) | **New** — needs full build |
| Listing copy generation (Stage 4) | Partially automated |
| Multi-marketplace push (Stage 5) | Walmart Lister built, Shopify live |

## Impact

| Metric | Today | With ListingForge |
|--------|-------|-------------------|
| Time: license → live listings | Weeks | Days |
| Manual steps per design | 8-10 | 2 (approve context + approve design) |
| Marketing assets per launch | Near zero | Auto-generated per SKU |
| Email campaigns sent | 0 of 11K subs | Every launch, auto-formatted |
| Brand consistency | Varies by operator | DB-enforced, LLM-consistent |

## Tech Stack

- **Composition:** Python (psd-tools + Pillow) — local, no paid APIs
- **AI Images:** Gemini 3 Flash / Nano Banana 2 — brand-contextual backdrops
- **AI Text:** Claude Sonnet — copy, captions, prompts from brand context
- **Database:** Supabase (PostgreSQL) — `marketing_attributes` table is the backbone
- **Storage:** AWS S3 — deterministic naming, auto-upload

## Next Steps (Priority Order)

1. `marketing_attributes` table in Supabase — foundation for all downstream AI
2. LLM context generator — auto-populate from license name
3. Gemini lifestyle image integration — brand-contextual backdrops at scale
4. Marketing asset formatter — social + email dimensions from same images
5. Copy generator + go-live push — unified marketplace deployment

---

*Ecell Global — Any fan's favourite brand, on any device, everywhere they shop.*
