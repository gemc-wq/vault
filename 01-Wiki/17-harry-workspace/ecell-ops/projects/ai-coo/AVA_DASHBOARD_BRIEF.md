# ECELL DASHBOARD + PRODUCT ENTRY APP — Brief for Ava
> From: Harry (COO) + Cem (CEO)
> Date: 2026-02-09
> Priority: HIGH — Start immediately alongside Image Maker

---

## Overview

Build a central dashboard portal with two initial apps:
1. **Product Entry** — Manual data entry into Supabase (the human trigger for the pipeline)
2. **Image Maker** — Already briefed separately (AVA_IMAGE_MAKER_BRIEF.md)

Both apps live under one dashboard URL.

## Dashboard Portal

Simple landing page with app cards:
- 📝 **Product Entry** — "Create new products"
- 🖼️ **Image Maker** — "Generate product images"
- ✅ **Approval Queue** — "Review pending items" (Phase 2)
- 📊 **Pipeline View** — "Track product status" (Phase 2)

Clean, minimal UI. White/grey palette. No clutter.

## Product Entry App

### Two Input Modes

#### Mode 1: Single Entry Form
Fields:
- **Brand / Licensed Property** → searchable dropdown (from Supabase `licenses` table, active only)
- **Product Type** → dropdown (lookup table — Cem sending codes tomorrow)
- **Device Model** → searchable dropdown (from Supabase `devices` table, 1,645 models)
- **Design Group Code** → text input (e.g. KIT25)
- **Design Variation** → text input (e.g. HOM, AWY, THI)
- **Design Title** → text input (human-readable name)
- **Notes** → optional textarea

**SKU Auto-Generation (real-time as fields are filled):**
```
PRODUCT_TYPE_CODE - DEVICE_CODE - BRAND_CODE + DESIGN_GROUP - VARIATION
Example: H8939-DS5EGCT-RMCFKIT25-HOM
```

The SKU preview shows live below the form as the user fills fields.

**On Submit:**
- Creates record in Supabase `products` table (status: 'draft')
- Creates linked record in `designs` table
- Shows success message with generated SKU
- Option to "Create Another" or "View in Pipeline"

#### Mode 2: CSV Bulk Upload
- Drag-and-drop CSV upload zone
- Column mapping step (map CSV columns to: Brand, Product Type, Device, Design Group, Variation)
- Preview table showing parsed data + auto-generated SKUs
- Validate before import (highlight errors: missing fields, duplicate SKUs)
- "Import All" button → batch insert to Supabase
- Summary: "X products created, Y errors"

### Required CSV columns:
```
brand_code, product_type_code, device_code, design_group, variation, design_title
```

## Supabase Connection

**Project URL:** https://nuvspkgplkdqochokhhi.supabase.co
**Anon Key:** sb_publishable_NReQwcvnfMEdpCy6OfornQ_or7kwlJW

(Use the anon key in the frontend — Row Level Security will be configured later.
For now, use the service key server-side for writes.)

**Service Key (server-side only):** [REDACTED_SUPABASE_SECRET_KEY]

### Tables Used:
- `licenses` (READ) — Brand dropdown (filter: is_active = true)
- `devices` (READ) — Device model dropdown
- `products` (WRITE) — Create new product records
- `designs` (WRITE) — Create linked design records
- `approvals` (WRITE) — Create approval request on submit

### Data Already Loaded:
- 1,645 devices (Samsung, Apple, Google, etc.)
- 871 brands (465 active — Harry Potter, Peanuts, WWE, NFL, Liverpool FC, etc.)

## Tech Stack

- **Next.js** (consistent with Head Case website)
- **Supabase JS client** (@supabase/supabase-js)
- **Tailwind CSS** for styling
- **React Hook Form** or similar for form handling
- **Papa Parse** for CSV parsing (client-side)

## UI/UX Requirements

- Clean, minimal — matches Cem's aesthetic (white, grey, navy accents)
- Mobile-responsive (Cem reviews on phone)
- Fast — dropdowns should be instant (preload device/brand data)
- SKU preview updates in real-time as fields change
- Success/error states are clear and obvious
- No login required initially (internal tool, accessed via direct URL)

## N8N Integration Points

When a product is created, we'll set up N8N webhooks to:
1. **Notify Cem via Telegram** — "New product created: [SKU] [Design Title]"
2. **Trigger content generation** — Auto-kick Sonnet 4.5 for listing copy
3. **Trigger image generation** — Queue in Image Maker for product shots
4. **Add to approval queue** — Create approval request for QA

Harry will build the N8N workflows. Ava just needs to:
- POST to a webhook URL on product creation (Harry will provide the URL)
- Include the full product data in the webhook payload

## Build Order

1. **Dashboard shell** — Portal page with app cards
2. **Product Entry form** (single entry) — Dropdowns + SKU auto-gen + Supabase write
3. **CSV upload** — Bulk import mode
4. **Image Maker** — Per separate brief

## Questions for Ava
1. Can you start with the dashboard shell + product entry form today?
2. ETA for a working prototype with Supabase connected?
3. Any blockers I should resolve?

---

*Brief prepared by Harry | 2026-02-09*
*Approved by Cem: "LFG, let's get Ava to start coding"*
