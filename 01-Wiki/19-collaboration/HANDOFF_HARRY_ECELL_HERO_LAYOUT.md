# Handoff — Ecellglobal.com Hero Layout (Assets + Plan)

## Goal
Recreate the attached **clean light studio hero layout** (headline + CTA left, product cluster right) and **apply a single UV pattern/design across each product**.

## Reference hero layout
- Cem provided reference image in Telegram (message_id: 1827 / 1830). Use it as the layout target.

## Current asset locations (Drive via rclone)
Base folder:
- `gdrive:Clawdbot Shared Folder/collaboration/assets/`

### Product mockups (uploaded)
- `collaboration/assets/ecellglobal/hero/`
  - Example files: `IPH17PRO.jpg`, `IPH17PMAX.jpg`, `S25.jpg`, `89-39-PS5CS-1.jpg`, `89-39-SWTCH2-1.jpg`, `OVERLAY_FLOATING.png`

### Generated UV pattern pack (3 options)
- `collaboration/assets/ecellglobal/designs/generic-patterns/uv-pack-01/`
  - `uv_pattern_1_2048.png` (dots + arcs)
  - `uv_pattern_2_2048.png` (scanlines + microgrid)
  - `uv_pattern_3_2048.png` (topographic contours)
  - plus `*_preview_1920x1080.png`

### Existing exports
- Collection banner draft:
  - `collaboration/assets/_exports/2026-02-14-collection-banner/ecellglobal_collection_banner_1920x600.png`

- Hero option set (dark UV vibe, 3 copy variants A/B/C):
  - `collaboration/assets/_exports/2026-02-14-hero-options/`

## What’s missing to finish the real hero mock
To accurately apply designs to products at scale (camera holes / controller cutouts), we need either:
1) PSD smart-object mockups + dielines/cutout masks (best)
2) Or a hybrid placement engine (mask + perspective + importance-map) on top of flat JPG/PNGs (MVP).

## Proposed next steps (recommended)
1) Pick the winning UV pattern (1/2/3 or mix 1+2) and lock it as the **hero pattern**.
2) Build a **first-pass hero** by compositing the uploaded product mockups into the reference layout and applying the chosen pattern (fast).
3) In parallel, start the **template library**:
   - iPhone case (camera cutout)
   - Galaxy case (camera cutout variant)
   - PS5 controller (complex cutouts)
   - Laptop skin (simple plane)
4) Add “smart placement” logic so key elements (logos/text) avoid cutouts.

## Output sizes to generate
- 1920×1080 (homepage)
- 1200×630 (link preview)
- 1080×1350 (social)

---

If you want, I can also export a simple CSV manifest of all assets + their Drive paths for easier planning.
