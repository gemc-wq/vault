# IMAGE MAKER APP — Full Brief for Ava
> From: Harry (COO) + Cem (CEO)
> Date: 2026-02-09
> Priority: HIGH — This is a core tool in the production pipeline

---

## What This App Does

A web-based tool that takes **design artwork files** + **device templates** and generates **professional product photography** ready for Amazon, eBay, and the website. Think of it as an internal Photoshop-on-autopilot for phone case product images.

## Where It Fits in the Pipeline

```
Idea Approved → Design Created → IMAGE MAKER APP → Product Images → QA → Go Live
                                  ^^^^ YOU BUILD THIS ^^^^
```

The Image Maker sits between "we have a design" and "we have listing-ready product photos." It's the tool that turns a flat 2D artwork file into photorealistic product shots on actual devices.

## Core Functionality

### Inputs
1. **Design artwork file** — The 2D design (PNG/SVG) that goes on the case
   - Uploaded by designer or pulled from Supabase `designs` table
2. **Device selection** — Which phone model (from `devices` table in Supabase)
3. **Case type** — Clear TPU, tough case, slim, etc.
4. **Shot selection** — Which angles to generate

### Processing
- Composite the design artwork onto the case template for the selected device
- Generate AI product photography using Gemini Pro image generation
- Apply the standard prompt templates (see below)
- Multiple angles: hero (30° isometric), front, back, sides, 360° rotation

### Outputs
- Set of product images (6-8 per product) in high resolution
- White background, studio lighting, Amazon-compliant
- Auto-upload to CDN (S3 or similar)
- Image URLs saved to Supabase `product_images` table
- Thumbnail gallery for QA review

## Shot Types Required

| Shot | Angle | Use |
|------|-------|-----|
| Hero | 30° isometric | Amazon main image, marketing |
| Front | 0° straight on | Alternate listing image |
| Back | 180° straight on | Show full design |
| Right Side | 90° | Show case thickness/buttons |
| Left Side | 270° | Alternate side view |
| Back Right (HERO) | 135° | Design + camera lip showcase |
| Lifestyle | Varies | Marketing/social (Phase 2) |

## Prompt Templates

### Standard Product Shot (Gemini Pro)
```
Subject: [DEVICE_NAME] [CASE_TYPE] case fitted on device, featuring [DESIGN_NAME] design centered on back plate below camera module.
Angle: [ANGLE_DESCRIPTION]
Orientation: Phone standing vertically upright.
Lighting: Professional studio softbox high-key, pure white background (RGB 255,255,255), soft contact shadow on floor.
Details: Sharp focus on the design and the crystal clear TPU bumper edges.
Tech Specs: 8k resolution, photorealistic, ray-traced, unreal engine 5 style, large format ready.
```

### Amazon Main Image Requirements
- Pure white background (RGB 255,255,255)
- Product fills 85%+ of frame
- No text, badges, props, or hands
- Minimum 1600px on longest side (ideally 2000px+)
- Sharp, well-lit, professional

### 360° Rotation (8 frames at 45° intervals)
See full prompt sequence in: `projects/design-automation/PHONE_CASE_IMAGE_GEN_PROMPTS.md`
Includes Python stitcher script to combine frames into GIF/MP4.

## Tech Stack Recommendation

- **Frontend:** Next.js (consistent with Head Case website)
- **UI Components:** Upload zone, device selector dropdown, shot picker checkboxes, preview gallery
- **Image Gen API:** Gemini Pro (via Google AI API)
- **Storage:** S3-compatible bucket for CDN (or Supabase Storage)
- **Database:** Supabase — reads `devices` and `designs`, writes to `product_images`
- **Deployment:** Same infrastructure as the Head Case website

## UI Flow

```
1. SELECT DESIGN
   → Upload artwork file OR pick from Supabase designs library
   → Preview the 2D design

2. SELECT DEVICE
   → Dropdown of devices from Supabase (searchable)
   → Shows device image/outline for reference

3. SELECT CASE TYPE
   → Clear TPU (default), Tough, Slim, Wallet

4. SELECT SHOTS
   → Checkboxes: Hero, Front, Back, Sides, Full 360°
   → "Generate All" default option

5. GENERATE
   → Progress bar / loading state
   → Each image appears as it's generated
   → Side-by-side comparison view

6. REVIEW & APPROVE
   → Gallery view of all generated images
   → Approve / Regenerate individual shots
   → "Approve All" button → saves to Supabase + uploads to CDN

7. BATCH MODE (Phase 2)
   → Select one design + multiple devices
   → Generate product shots for all selected devices in one go
   → Critical for new design rollout across 300+ models
```

## Supabase Integration

### Read From:
- `devices` — Populate device selector
- `designs` — Show available designs library
- `products` — Know which SKUs need images

### Write To:
- `product_images` — Save generated image metadata (URL, type, dimensions)
- `products` — Update status to 'images_ready' when complete
- `approvals` — Create approval request for QA review

### API Endpoints Needed:
```
GET  /api/devices          → List all active devices
GET  /api/designs          → List designs (with filters)
POST /api/generate         → Trigger image generation
POST /api/images/approve   → Approve images, upload to CDN
GET  /api/products/:id/images → Get all images for a product
```

## Supabase Connection

Schema file: `projects/ai-coo/supabase_schema.sql` (Harry will set up the database)
Harry will provide the Supabase URL + anon key once the project is created.

## Phase 1 vs Phase 2

### Phase 1 (Build Now)
- Single design + single device → generate shots
- Manual upload of artwork files
- Basic gallery review
- Save to Supabase

### Phase 2 (After Phase 1 Works)
- Batch mode (1 design → many devices)
- Pull designs directly from Supabase library
- Marketing image templates (lifestyle, social)
- Auto-trigger from N8N when new design is approved
- 360° video generation with stitcher

## Reference Files on Your Machine
- `projects/design-automation/PHONE_CASE_IMAGE_GEN_PROMPTS.md` — All prompt templates
- `AGENT_CONFIG.md` — Team structure and who does what

## Questions for Ava
1. Can you estimate build time for Phase 1?
2. Do you need Gemini Pro API key set up, or do you have access?
3. Any preference on the image storage approach (Supabase Storage vs external S3)?

---

*Brief prepared by Harry | 2026-02-09*
*Approved by Cem for handoff*
