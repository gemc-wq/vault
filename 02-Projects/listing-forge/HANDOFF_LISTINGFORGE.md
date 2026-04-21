# ListingForge — Handoff Document

**Status:** POC working end-to-end. Main listing images verified across 12 iPhone devices.
**Last updated:** 2026-04-09

---

## 1. What this replaces

Legacy "DRECO" workflow required **13 manual Photoshop templates per design** to generate phone case listing images. ListingForge replaces that with:

- A **single master PSD per layout format** (1-1, 1-5, 1-7, 1-8, etc.)
- **Automated green-screen compositing** of the design onto device mockup templates
- **Batch generation** across all devices in ~55 seconds (12 main images, 6 format PSDs loaded once)

Target scale: 600–1000+ listing images per design run in production.

---

## 2. How it works

### Data flow

```
┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│  Format PSDs       │     │  Device Mockups    │     │  Mask Cache        │
│  Input/1-1.psd     │     │  IPH17.jpg (etc.)  │     │  .mask_cache/      │
│  Input/1-5.psd     │     │  green-screen back │     │  PNG + meta JSON   │
│  Input/1-8.psd     │     │  1600x1600 JPG     │     │  per mockup hash   │
└──────────┬─────────┘     └──────────┬─────────┘     └──────────┬─────────┘
           │                          │                          │
           ▼                          ▼                          ▼
     extract_design         detect_green_mask            get_or_create_mask
     (psd-tools)            (HSV + PCA orientation)      (file-hash cache)
           │                          │                          │
           └──────────────┬───────────┴──────────────────────────┘
                          ▼
              composite_design_into_mockup
              (scale by long_extent, rotate to mask angle,
               alpha-composite through mask)
                          │
                          ▼
              Output/{device_id}.jpg
              Output/{device_id}-{n}.jpg  (features, experimental)
```

### Key technical decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Format PSDs | 1 per layout class (1-1, 1-5, 1-7, 1-8) | Elements pre-positioned per device aspect ratio; matches legacy artist workflow |
| Design extraction | Full `Lineup Name Here/Sticker Collage` group composite | Native proportions preserved; no stretching of licensed artwork |
| Green detection | HSV two-tier + connected-component filter | Handles JPEG compression artifacts and rejects reflected green on front of case |
| Mask orientation | PCA on mask pixel coords | Detects tilted/rotated cases in feature mockups; `long_extent` used for scaling |
| Mask caching | File-hash keyed PNG + JSON | ~8ms cache hit vs ~300ms detection; meta JSON carries orientation |
| Design scaling | Scale by oriented `long_extent`, not axis-aligned bbox | Correct size regardless of phone tilt |
| Format → device map | YAML config (`layout_format` field per device) | Future: Supabase lookup using same data shape |

---

## 3. Codebase layout

```
Listing Image Creator/
├── app.py                    # Streamlit dev UI (Ecell-styled)
├── config/
│   └── devices.yaml          # Format PSDs + device→format mapping + feature templates
├── listing_forge/
│   ├── __init__.py
│   ├── cli.py                # Click CLI: generate / masks / inspect
│   ├── config.py             # YAML loader → PipelineConfig
│   ├── models.py             # Dataclasses: DeviceConfig, FormatPSD, GreenMask, DesignArtwork
│   ├── psd/
│   │   ├── extractor.py      # PSD parsing + group composite (psd-tools)
│   │   └── guide_parser.py   # Safe-area red-rectangle detection from guide layers
│   ├── mask/
│   │   ├── green_screen.py   # HSV detection + PCA orientation + alpha gradient
│   │   └── cache.py          # File-hash mask caching (binary PNG + meta JSON)
│   └── compose/
│       ├── compositor.py     # Design-into-mockup compositing (rotate → scale → alpha blend)
│       └── scaler.py         # (Legacy helper, unused in current path)
├── .gitignore
├── HANDOFF.md                # This file
└── E-commerce Image Pipeline Modernization Brief.md
```

**Not versioned (see `.gitignore`):**
- `Input/` — 1.6GB of format PSDs
- `Output/` — generated listing images
- `Output Listing Image1 Green Screen/` — device mockup templates
- `Output Listing Image features/` — feature image templates
- `.mask_cache/` — regenerated on first run
- `database files/` — CSV exports (large, external source of truth)

---

## 4. Running it

### CLI (batch)

```bash
# Generate all devices
python3 -m listing_forge generate --config config/devices.yaml

# Single device
python3 -m listing_forge generate --device IPH17

# Rebuild mask cache
python3 -m listing_forge masks

# Inspect a PSD's layer structure
python3 -m listing_forge inspect Input/1-1.psd
```

**Expected timing:** 6 format PSDs load once (~15s each = ~90s), then ~0.2s per device composite. Full run: ~95s for 12 main images + 5 IPH17 feature images.

### Streamlit dev UI

```bash
python3 -m streamlit run app.py --server.port 8501
```

Open http://localhost:8501.

**Sidebar (top to bottom):**
1. **Design Code** — Manual / Database / CSV Upload tabs. Database tab is a Supabase stub. CSV upload parses any column named `design_code`/`code`/`sku`. For POC, this is a reference field — actual PSD loading still uses the YAML config.
2. **Feature Images** — Off (default) / Composite (experimental) / Gemini (coming soon).
3. **Models** — device multiselect.
4. **Output Quality** — JPEG compression slider (95 = marketplace standard).

**Header:** brand mark, LISTINGFORGE title, POC status badge, metric row (devices, format PSDs, feature templates, output size).

### Config file (`config/devices.yaml`)

```yaml
psd_source:
  design_group: "Lineup Name Here/Sticker Collage/Group 1"
  design_with_bg: "Lineup Name Here/Sticker Collage"

formats:
  "1-1": { psd: "Input/1-1.psd", guide: "guides/1-1" }
  "1-5": { psd: "Input/1-5.psd", guide: "guides/1-5 <!>" }
  "1-7": { psd: "Input/1-7.psd", guide: "guides/1-7 <!>" }
  "1-8": { psd: "Input/1-8.psd", guide: "guides/1-8" }
  # ...

output:
  directory: "Output"
  format: "jpg"
  quality: 95
  size: [1600, 1600]
  mask_cache_dir: ".mask_cache"

devices:
  IPH17:
    mockup: "Output Listing Image1 Green Screen/IPH17.jpg"
    layout_format: "1-8"
    features:
      - "Output Listing Image features/IPH17-1.jpg"
      - "Output Listing Image features/IPH17-2.jpg"
      # ...
```

---

## 5. What works

- **12 iPhone devices** — main listing image verified across IPH13, IPH15, IPH15PLUS, IPH15PRO, IPH15PMAX, IPH16, IPH16PLUS, IPH16PRO, IPH17, IPH17AIR, IPH17PRO, IPH17PMAX.
- **Format-aware compositing** — each format PSD (1-1, 1-5, 1-7, 1-8) loaded once per run and shared across devices using that format.
- **Native-resolution scaling** — design scales by long-axis extent, preserving element size relative to the case back. No stretching.
- **Green screen detection** — HSV-based, robust to JPEG artifacts and reflections. Rejects non-case-back green via largest-connected-component filter.
- **Mask caching** — 8ms cache hit vs 300ms detection. Cache key = file hash + device ID.
- **CLI + Streamlit UI** — both production paths working.
- **Ecell-branded UI** — Cobalt + Zinc + Inter per the Ecell Global style guide.

---

## 6. Known issues & open work

### Feature images (experimental)

The compositor uses PCA to detect the long axis of the green region and rotate the design to match, but this only solves the *rotation angle*, not the *top-vs-bottom direction*. For heavily tilted or upside-down feature mockups, the design may end up 180° off. Current workarounds:

- **Feature Images is defaulted to `Off`** in the Streamlit UI.
- Users can opt into `Composite (experimental)` for a best-effort render.
- `Gemini (coming soon)` is a stub — the plan is to hook up Gemini image-gen for true context-aware feature image creation.

**Disambiguation fix (not yet implemented):** find the camera cutout (largest hole inside the mask) and use its position to determine which end of the case is "top."

### Design code lookup

The Design Code sidebar section is currently a **reference field only** — it accepts manual input, a stub database list, or CSV upload, but it doesn't actually swap PSDs. The PSDs are still loaded from the YAML config.

**Production path:** replace the `formats` section of `devices.yaml` with a Supabase query keyed by design code. The `load_design_for_format` function in `app.py` is already cached per PSD path, so it will cleanly support this.

### Device → format mapping

Currently hardcoded in `config/devices.yaml`. `database files/jig_devices.csv` exists but the format column isn't obvious from the export. Leave as-is until Supabase migration.

### Guide layers

Only `1-1` has a populated guide rectangle. `1-2` through `3-1` have empty placeholder guides. The safe-area parser handles this gracefully (falls back to full canvas), and the native-resolution compositor doesn't rely on the safe area for scaling — it's only used for the design extraction hint. No action needed for POC.

### Streamlit hot-reload

Streamlit does not always pick up CSS-only edits. If the UI looks stale after an edit, restart the server:

```bash
lsof -ti :8501 | xargs kill && python3 -m streamlit run app.py --server.port 8501
```

---

## 7. Future migration path

Ordered by priority:

1. **Gemini feature image plugin** — replace PCA compositing for feature images with Gemini image generation. The `Feature Images` radio in the sidebar already has a slot for this.
2. **Supabase design code lookup** — replace YAML `formats` section with a Supabase query. Match the existing `FormatPSD` dataclass shape.
3. **S3 upload** — add an upload step after `generate_listing_image` using SKU-based naming: `{SKU}-{format}.jpg`.
4. **FastAPI backend** — wrap the composition engine so multiple frontends (Streamlit dev, React production) can call it.
5. **SKU parsing** — auto-resolve device + design + variant from an SKU string like `HTPCR-IPH17PMAX-BOSCEL-001`.
6. **Multiple marketplaces** — feature template sets per marketplace (Amazon/Walmart/eBay/etc.).

---

## 8. Debugging playbook

### "Design is stretched / wrong proportions"
Check `content_h` in `listing_forge/compose/compositor.py`. It should equal `design.psd_size[1]` (PSD native height, typically 3600). If scaling uses the axis-aligned bbox instead of `mask.long_extent`, rotated cases will be wrong.

### "Green fringe at case edges"
The `pad` variable in `compositor.py` controls overlap. Currently 12px. Increase if visible seams appear.

### "Feature mockup shows design upright even though phone is tilted"
Make sure the mask cache is fresh — delete `.mask_cache/` and re-run. Old cached masks from before the orientation fix lack `angle_deg` metadata.

### "Green screen detection picks up wrong region"
Check `hue_range` in `green_screen.py`. Default is `(80, 160)`. If a mockup has an unusual green tone, expand. The `largest connected component` filter should handle reflections automatically.

### "PSD loading is slow"
Expected — 15s per format PSD is the `psd-tools` baseline. Format PSDs are cached per run, so the total is `N_formats × 15s`, not `N_devices × 15s`.

---

## 9. Contacts & references

- **Brief:** `E-commerce Image Pipeline Modernization Brief.md`
- **Business context:** `Modernizing Print-on-Demand Asset Pipeline.md`
- **Style guide:** Ecell Global Dashboard Style Guide (Cobalt #0047AB, Zinc neutrals, Inter)
- **Legacy workflow:** DRECO (manual Photoshop template pipeline)

---

## 10. Test run recipe

Quick smoke test after pulling the repo:

```bash
# 1. Install
pip3 install -r requirements.txt  # psd-tools, pillow, numpy, scipy, click, streamlit, pyyaml, pandas

# 2. Drop the PSDs and mockups into place
#    Input/1-1.psd ... Input/3-1.psd
#    Output Listing Image1 Green Screen/IPH*.jpg
#    Output Listing Image features/IPH17-*.jpg

# 3. Generate one device
python3 -m listing_forge generate --device IPH17

# 4. Verify
ls Output/IPH17.jpg  # should exist, ~425KB
```

If that works, run the full pipeline:

```bash
python3 -m listing_forge generate
```

Expected: 12 main images in `Output/` within ~95 seconds.
