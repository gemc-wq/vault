# Unified Production Pipeline — Handover Document

**Version**: 1.0
**Last updated**: 2026-04-09
**Repository**: https://github.com/gemc-wq/unified-production
**Owner**: Ecell Global — Production Engineering
**Status**: MVP complete, in pilot on production floor

---

## 1. Purpose

This application replaces two legacy tools used on the Ecell Global production floor:

| Legacy tool | Language | Role |
|-------------|----------|------|
| **IREN** | Java (Swing) | Consumed order POs and produced print-ready jig TIFFs for the CMYK printers |
| **LAZCUT** | Standalone | Produced SVG cut files from EPS templates for the CO₂ laser cutter |
| **DRECO** | C# / .NET | Generated marketplace listing images (not migrated yet — Phase 4) |

Both legacy tools read from the same IREN MySQL database and consumed PSD artwork files from shared folders. They were fragile, Windows-only, and required a designer or senior operator to run. The unified pipeline replaces the **IREN + LAZCUT** lanes with a single FastAPI web app that any trained operator can use from any machine on the network.

---

## 2. Business Context

- **Scale**: ~1,500 print jobs/week across UK, FL, and PH facilities
- **Products**: Hard cases (HC), TPU gel cases (TP), leather wallets (LB), hybrid cases (HY), matte cases, armour cases, snap cases, soft gel cases
- **Devices**: ~1,400 device SKUs (iPhone, Samsung, Pixel, Huawei, Xiaomi, etc.)
- **Throughput target**: Operator should be able to go from PO file upload → downloadable print + laser cut outputs in under 2 minutes for a typical 20-item batch
- **Print workflow**: Operator drops the **Amalgamated_PO_Export** XLSX (generated nightly by Zero ERP) into the app, previews the groups, runs the pipeline, and downloads the ZIP to the printer PC
- **Laser workflow**: Same PO file — items with matching EPS cut files are auto-routed to best-fit packing so the laser operator maximises sheet utilisation

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (HTML/CSS/JS)                   │
│               static/index.html + app.js                   │
└────────────────────────┬────────────────────────────────────┘
                         │  HTTP (form-data)
┌────────────────────────▼────────────────────────────────────┐
│                  FastAPI (main.py)                          │
│ ┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌─────────┐│
│ │ routes_     │ │ routes_      │ │ routes_    │ │ routes_ ││
│ │ config      │ │ orders       │ │ manual     │ │ jobs    ││
│ └─────────────┘ └──────┬───────┘ └─────┬──────┘ └────┬────┘│
└────────────────────────┼───────────────┼─────────────┼─────┘
                         │               │             │
         ┌───────────────┼───────────────┼─────────────┘
         │               │               │
         ▼               ▼               ▼
  ┌──────────────┐ ┌────────────┐ ┌─────────────┐
  │ order_       │ │ design_    │ │ SQLite      │
  │ sources      │ │ resolver   │ │ (data/db.py)│
  │ (CSV/XLSX)   │ │ (PSD/JPG)  │ │ jobs +      │
  │              │ │            │ │ job_outputs │
  └──────┬───────┘ └─────┬──────┘ └─────────────┘
         │               │
         ▼               ▼
   ┌──────────────────────────┐
   │ engine/jig/              │
   │  - renderer (grid)       │
   │  - bestfit (laser)       │
   │  - svg/pdf generators    │
   │  - overlay_preview       │
   └──────────┬───────────────┘
              │
              ▼
   ┌──────────────────────┐
   │  output/{job_id}/    │
   │   - design TIFFs     │
   │   - white ID TIFFs   │
   │   - cut SVGs + PDFs  │
   │   - overlay previews │
   │   - manifest.json    │
   └──────────────────────┘
```

### Tech stack

- **Backend**: Python 3.9+, FastAPI, Uvicorn, Pydantic Settings
- **Image processing**: Pillow, psd-tools
- **Excel / CSV**: openpyxl, stdlib csv
- **PDF**: reportlab (grid mode), hand-built minimal PDF (bestfit mode)
- **Database**: SQLite with WAL mode (runtime only, not the source of truth)
- **Frontend**: Plain HTML/CSS/JS — no build step, no bundler, no framework
- **No external services required** — fully local, fully offline capable

### Why these choices

- **No framework on the frontend**: operators run this in Chrome/Safari; a React build step is unnecessary overhead for what is essentially a form + results viewer
- **SQLite not Postgres**: there's no multi-writer contention, and keeping it self-contained means the app starts with zero infrastructure
- **CSV data not a database**: the jig/device dimensions came from an IREN MySQL dump; moving them into a real database is Phase 2 (Supabase — see §13)
- **psd-tools not ImageMagick**: the PSD structure is layered and we need to skip canvas/guides, which ImageMagick flattens

---

## 4. Project Structure

```
unified-production/
├── main.py                      # FastAPI app + uvicorn entry
├── config.py                    # Pydantic settings (env-overridable)
├── requirements.txt             # Pinned dependencies
├── README.md                    # Quick start + reference
├── HANDOVER.md                  # This file
├── .gitignore
│
├── api/                         # HTTP route modules
│   ├── __init__.py
│   ├── routes_config.py         # Dropdown data
│   ├── routes_orders.py         # Batch pipeline (the big one)
│   ├── routes_manual.py         # Single-design test runs
│   └── routes_jobs.py           # Job history + ZIP download
│
├── engine/                      # Business logic (no HTTP concerns)
│   ├── __init__.py
│   ├── measurements.py          # Load jig_tables/jig_devices CSVs
│   ├── design_resolver.py       # Find + load PSD/JPG/PNG per item
│   ├── replicator.py            # Scale + crop to device dimensions
│   ├── order_sources/
│   │   ├── __init__.py
│   │   └── csv_source.py        # CSV/XLSX parser with flexible headers
│   └── jig/
│       ├── __init__.py
│       ├── renderer.py          # Grid layout rendering + label band
│       ├── bestfit.py           # SNFDH bin packing for laser
│       ├── svg_generator.py     # EPS → SVG cut conversion
│       ├── pdf_generator.py     # EPS → PDF cut conversion
│       └── overlay_preview.py   # Cut lines overlaid on design (QA)
│
├── models/                      # Dataclasses
│   ├── __init__.py
│   ├── order.py                 # OrderItem
│   └── measurements.py          # JigMeasure, JigDeviceMeasure, ReplicationMeasure
│
├── data/                        # Database layer
│   ├── __init__.py
│   ├── db.py                    # SQLite schema + CRUD
│   └── migrate_csv.py           # Standalone CSV → SQLite importer
│
├── static/                      # Frontend
│   ├── index.html
│   ├── app.js
│   └── style.css
│
└── Database files/              # (gitignored) IREN MySQL exports
    ├── jig_tables.csv
    ├── jig_devices.csv
    ├── jig_measurement.csv
    ├── headcase.sql
    ├── replication.sql
    └── cem db dump jig.sql
```

**Runtime-only (gitignored):**
- `output/{job_id}/` — per-job output directory
- `uploads/` — temporary upload staging
- `production.db`, `production.db-shm`, `production.db-wal` — SQLite files

---

## 5. Data Flow: A Single Batch Run

### Step 1: Upload & parse

```
POST /api/parse-order
  file: Amalgamated_PO_Export2026-04-01.xlsx
  default_manufacturer: UK
```

`engine/order_sources/csv_source.py` reads the XLSX, detects columns (flexible header matching), and returns:

```json
{
  "filename": "...",
  "total_items": 4,
  "total_quantity": 4,
  "groups": [
    {
      "product": "TP",
      "device": "IPH16PRO",
      "manufacturer": "UK",
      "total_quantity": 1,
      "po_numbers": ["2326807"],
      "items": [...]
    },
    ...
  ]
}
```

The frontend populates the **Production Summary** table from this payload.

### Step 2: Full pipeline

```
POST /api/process-order-batch
  order_file: ...
  source: csv_upload
  default_manufacturer: UK
  layout_mode: auto
  jig_size: 6042
  design_files[]: (optional)
```

Inside `_run_order_pipeline`:

1. Build a **design catalog** by scanning upload folder + design search dirs
2. For each parsed row:
   - `resolve_design_for_item()` finds the matching PSD/JPG/PNG
   - `load_design_image()` composites the PSD (skipping canvas/guides/Background)
   - `replicate()` produces a replicated RGB preview JPG (for the UI)
3. Split items by layout:
   - `layout_mode == "auto"`: items with an EPS cut file → bestfit, others → grid
   - `layout_mode == "grid"`: all items → grid
   - `layout_mode == "bestfit"`: all items → bestfit
4. For each bucket, call `_render_groups()` or `_render_groups_bestfit()`
5. Write `manifest.json` and update the SQLite job record

### Step 3: Rendering — Grid mode (`engine/jig/renderer.py`)

For each `{product}_{device}_{manufacturer}` group:

1. Look up `JigMeasure` from `jig_tables.csv` — sheet dimensions, margin, offset, count_x, count_y, rotation
2. Look up `JigDeviceMeasure` from `jig_devices.csv` — device slot width/height, border radius, flip, padding
3. Expand items by quantity, chunk by `count_x * count_y`
4. For each chunk:
   - Create a white canvas at sheet dimensions
   - For each item:
     - `compose_with_label_band()` — 1cm white band at top with `{mfr} - {product} - {device}`, design scaled into the remaining area
     - Rotate by `jm.rotation` (typically 90°)
     - Flip per `dm.flip`
     - Apply rounded corners
     - Paste at grid position (right-to-left, bottom-to-top)
   - Paint the white ID jig with pink overlay + centered text labels
5. `save_jig()` writes design TIFF + white TIFF + JPG previews
6. `generate_cut_svg()` and `generate_cut_pdf()` build cut-line files from EPS templates

### Step 4: Rendering — Bestfit mode (`engine/jig/bestfit.py`)

Used for laser cut items. All items packed onto shared sheets regardless of product/device.

1. Expand items by quantity → `List[JigItem]`
2. Build sort keys from SKU, pass to `bestfit_pack()`
3. **SNFDH algorithm**:
   - Sort by SKU alphabetically (tiebreak: height descending)
   - Place items on horizontal shelves left-to-right
   - Rotate items 90° if it helps them fit
   - Open new shelf when current is full, open new sheet when current is full
4. For each placement:
   - `compose_with_label_band()` — same label band as grid mode
   - Rotate 90° if the packer rotated this item
   - **Mirror horizontally** (XOR with `dm.flip`) — laser prints face-down, so the final image must be mirrored
   - Apply rounded corners
   - Paste at packed position
5. Generate mirrored SVG cut lines via `_eps_to_svg_group(flip_horizontal=not dm.flip, ...)`

---

## 6. Critical Features Explained

### 6.1 PSD handling

Production PSDs from `DRECO Input files Phone Back Case/` have this layer structure:

```
├── Background           (solid pixel layer — SKIP)
├── Lineup Name Here     (group — KEEP, contains the design)
│   └── Sticker Collage
│       ├── BG           (solid colour fill — this is the design background)
│       └── Group 1      (the actual artwork)
├── guides               (group — SKIP, contains red guide rectangles)
│   ├── 1-1              (visible guide for this device)
│   ├── 1-2              (invisible guides for other devices)
│   └── ...
└── canvas               (group — SKIP, bright green overspray area)
    └── green
```

The default `psd.composite()` flattens everything including the bright green canvas and the red guide rectangles. Our `_composite_psd_design()` in `engine/design_resolver.py` filters the top-level layers:

```python
_PSD_SKIP_LAYERS = {"background", "bg", "canvas", "guides"}
```

Anything else is composited onto a transparent canvas, preserving the design artwork exactly. If all layers match the skip list (unusual PSDs), it falls back to the full composite.

**To debug an odd PSD**: open it in Photoshop, read the top-level layer names, and either rename or add to the skip list.

### 6.2 Design scaling & cropping

`engine/replicator.py` has two primitives:

- `uniform_scale_to_cover()` — scale to cover target dimensions **without cropping** (output is larger than target on one axis)
- `fill_size_and_crop()` — scale to cover AND center-crop to exact target dimensions

The renderers use `fill_size_and_crop()` because we need exact device dimensions. If you use `uniform_scale_to_cover()` without post-processing, the image will overflow the device slot and bleed into neighbouring slots.

### 6.3 Label band (camera hole area)

Every rendered design has a **1 cm white band at the top** (`CAMERA_LABEL_BUFFER_PX = 118` px at 300 DPI) containing:

```
{manufacturer} - {product} - {device}
```

e.g. `UK - HC - IPH16PMAX`

Implementation (`engine/jig/renderer.py:compose_with_label_band`):

1. Reserve the top `118` px of the `dev_h` for the label
2. Scale the design into `dev_w × (dev_h - 118)`
3. Paste the scaled design below the band
4. Draw the label text in the band, auto-shrinking the font if needed to fit

This happens **before** rotation and mirroring, so:

- Grid mode (no mirror): label reads normally
- Laser mode (mirrored for face-down printing): label is also mirrored, which is correct — when the printed sheet is flipped to its final face-up orientation, the text reads right

### 6.4 Laser face-down mirroring

Laser cut items (those routed to bestfit) are **mirrored horizontally** in:

- The design TIFF — `flip_horizontal(img)` in `render_bestfit_jig()`
- The SVG cut line — `flip_horizontal=not dm.flip` in `_eps_to_svg_group()`

This is XOR with `dm.flip` (per-device metadata for devices that need a base flip for camera cutout positioning). The net result: every laser print comes out correctly when the operator lays the sheet face-down on the laser bed.

The **white identification jig is NOT mirrored** — it stays right-reading because the operator uses it during trim/QA.

### 6.5 Layout auto-routing

`layout_mode = "auto"` (the default) routes items based on whether an EPS cut file exists:

```python
# api/routes_orders.py
for entry in resolved_entries:
    if has_cutfile(item.product, item.device, item.manufacturer):
        laser_entries.append(entry)
    else:
        grid_entries.append(entry)
```

`has_cutfile()` checks `LAZCUT/Good for UK/` (UK/DE) or `LAZCUT/FL cutfiles/` (FL/PH) for `{product}-{device}.eps`. If found → bestfit. If not → grid.

Operators can force a mode via the dropdown for troubleshooting.

### 6.6 Jig sizes

Two physical laser bed sizes:

| Preset | Dimensions (px @ 300 DPI) | Dimensions (mm) |
|--------|---------------------------|-----------------|
| **6042** | 7205 × 4961 | 610 × 420 |
| **7151** | 8386 × 6024 | 710 × 510 |

Selected via the `#jig-size` dropdown (available in both batch and manual modes). Passed through as `jig_size` form field → `_run_order_pipeline` → `JIG_SIZE_PRESETS` lookup in `api/routes_orders.py`.

**To add a new jig size**: edit `JIG_SIZE_PRESETS` in `api/routes_orders.py` and add `<option>` entries in `static/index.html`.

### 6.7 Production Summary panel

The main content area always shows a **Production Summary** panel instead of an empty state. It has three modes:

1. **Empty** (initial): "Ready for input"
2. **Preview** (after parsing order): stat cards + table showing parsed groups with `Ready` status
3. **Complete** (after run): stat cards + table showing rendered jigs with `Complete` status

Columns: `#`, `PO Number`, `Product`, `Device`, `Country`, `Qty`, `Layout`, `Jig Size`, `Status`.

The **status badge in the header** is oversized (200 px wide, 16 px bold) so operators can see the current state from across the production floor.

---

## 7. Order File Format

The parser accepts the exact **Amalgamated_PO_Export** XLSX format from Zero ERP. Column detection is flexible — any of these header names work:

| Internal field | Recognized column names |
|----------------|------------------------|
| PO Number | `HPT_PO_Number`, `po_number`, `po`, `order_number`, `purchase_order`, `reference`, `order_ref` |
| Product | `ProductCode`, `product_code`, `product`, `producttype` |
| Device | `Unit`, `unit_code`, `device`, `device_code`, `phone` |
| Quantity | `Quantity`, `qty`, `count`, `units` |
| SKU / Custom Label | `Custom_Label`, `sku`, `product_sku`, `item_code`, `itemcode` |
| Label (design name) | `label`, `design`, `design_name`, `design_label`, `Custom_Label`, `name` |
| Manufacturer | `Sage_Server`, `manufacturer`, `mfr`, `server`, `location` |
| Image path | `image`, `image_path`, `file`, `filepath`, `design_file`, `design_path` |
| Family code | `family`, `family_code`, `lineup`, `lineup_code` |

Manufacturer aliases (case-insensitive):

| Input | Normalised |
|-------|-----------|
| `United Kingdom`, `UK` | `UK` |
| `Germany`, `DE` | `DE` |
| `Philippines`, `PH` | `PH` |
| `Florida`, `FL` | `FL` |

### Example: Amalgamated PO row

```
HPT_PO_Number    ProductType-Unit    Quantity    ProductCode    Unit        Custom_Label                        Sage_Server
2326807          HTPCR-IPH16PRO     1           TP             IPH16PRO    HTPCR-IPH16PRO-HPOTDH37-HOP         UK
```

Parsed as:

```python
OrderItem(
    sku="HTPCR-IPH16PRO-HPOTDH37-HOP",
    product="TP",
    device="IPH16PRO",
    quantity=1,
    label="HTPCR-IPH16PRO-HPOTDH37-HOP",
    manufacturer="UK",
    po_number="2326807",
    ...
)
```

---

## 8. Output Files

Each run creates `output/{job_id}/`:

```
output/a3f7b2c1/
├── design-inputs/              # Copies of any uploaded design files
├── items/                      # Per-item replicated preview JPGs
│   ├── 001_hc-iph16pmax_replicated.jpg
│   └── ...
├── groups/
│   ├── hc-iph16pmax-uk/        # Grid group folder (slugified key)
│   │   ├── IPH16PMAX_HC_1-20.tif         # Design TIFF (20 items on sheet 1)
│   │   ├── IPH16PMAX_HC_1-20-W.tif       # White ID TIFF
│   │   ├── IPH16PMAX_HC_1-20_preview.jpg # Browser preview
│   │   ├── IPH16PMAX_HC_1-20-W_preview.jpg
│   │   ├── IPH16PMAX_HC_1-20_overlay.jpg # Cut lines overlaid for QA
│   │   ├── IPH16PMAX_HC_1-20-C.svg       # Laser cut SVG
│   │   └── IPH16PMAX_HC_1-20-C.pdf       # Laser cut PDF
│   └── bestfit/                # Laser bestfit folder
│       ├── bestfit_1-15.tif
│       └── ...
└── manifest.json               # Full run metadata
```

TIFFs are saved at 300 DPI with LZW compression.

---

## 9. Database Schema

`production.db` is a runtime SQLite file — it tracks job history but is **not the source of truth** for any business data. You can delete it and the app will recreate it.

### `jobs` table

| Column | Type | Notes |
|--------|------|-------|
| `id` | TEXT PK | 8-char hex |
| `source_type` | TEXT | `csv_upload`, `manual_upload`, etc |
| `source_filename` | TEXT | Original filename |
| `manufacturer` | TEXT | Default manufacturer |
| `status` | TEXT | `pending`, `running`, `completed`, `failed` |
| `created_at` | TEXT | ISO timestamp |
| `completed_at` | TEXT | ISO timestamp, nullable |
| `total_items` | INTEGER | Row count |
| `total_sheets` | INTEGER | Jig sheets rendered |
| `output_dir` | TEXT | Path to `output/{id}/` |
| `manifest_json` | TEXT | Full manifest as JSON |
| `error_message` | TEXT | Nullable |

### `job_outputs` table

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER PK | Autoincrement |
| `job_id` | TEXT FK | → `jobs(id)`, cascading delete |
| `group_key` | TEXT | e.g. `hc-iph16pmax-uk` or `bestfit` |
| `output_type` | TEXT | `design_tiff`, `white_tiff`, `cut_svg`, `cut_pdf`, `overlay_preview` |
| `file_path` | TEXT | Absolute path on disk |
| `sheet_index` | INTEGER | 1-based jig sheet number |
| `created_at` | TEXT | ISO timestamp |

**WAL mode** is enabled for better concurrent read performance.

---

## 10. Configuration

All settings are defined in `config.py` as a Pydantic `BaseSettings` and can be overridden via environment variables with the `PROD_` prefix or via a `.env` file.

| Setting | Default | Purpose |
|---------|---------|---------|
| `port` | `5050` | HTTP port |
| `host` | `0.0.0.0` | Bind address |
| `base_dir` | app root | Computed at import time |
| `output_dir` | `{base}/output` | Where jobs are written |
| `upload_dir` | `{base}/uploads` | Temporary upload staging |
| `static_dir` | `{base}/static` | Frontend files |
| `csv_data_dir` | parent of `base_dir` | Where `jig_*.csv` lives |
| `lazcut_base` | `{parent}/LAZCUT` | EPS cut file root |
| `design_search_dirs` | DRECO input folders | PSD/JPG search path |
| `output_dpi` | `300` | Render DPI |
| `tiff_compression` | `tiff_lzw` | `tiff_lzw`, `tiff_deflate`, `none` |
| `jpeg_preview_quality` | `85` | Preview JPG quality 1–95 |
| `font_path` | `""` (auto-detect) | Custom font for label band |
| `dreco_enabled` | `False` | Reserved for Phase 4 |
| `secondary_jigs_enabled` | `False` | Reserved for multi-sheet devices |

### Example `.env`

```
PROD_PORT=5050
PROD_OUTPUT_DIR=/mnt/shared/production_output
PROD_CSV_DATA_DIR=/mnt/shared/jig_data
```

---

## 11. Running in Production

### Local dev (current setup)

```bash
python3 main.py
```

Uses `uvicorn.run(..., reload=True)` — auto-reloads on file changes. Good for development.

### Production deployment (recommended when rolling out)

```bash
# With gunicorn + uvicorn workers
pip install gunicorn
gunicorn -w 2 -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:5050 \
  --timeout 600 \
  main:app
```

Why `-w 2`: each worker holds the measurements cache in memory and can process one pipeline request. Two workers let the app serve `/api/config` and file downloads while a run is in progress.

Why `--timeout 600`: large batch runs (50+ items) can take several minutes in the current synchronous pipeline. Increase if you see worker timeouts.

### systemd unit (Linux)

```ini
[Unit]
Description=Unified Production Pipeline
After=network.target

[Service]
Type=simple
User=ecell
WorkingDirectory=/opt/unified-production
ExecStart=/opt/unified-production/venv/bin/gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5050 --timeout 600 main:app
Restart=on-failure
EnvironmentFile=/etc/unified-production.env

[Install]
WantedBy=multi-user.target
```

### Docker (not set up yet, Phase 2)

A `Dockerfile` is planned but not yet implemented. The app should containerise cleanly — Python 3.11-slim base, `pip install -r requirements.txt`, copy app, expose 5050.

---

## 12. Frontend Notes

### No build step

The frontend is plain HTML/CSS/JS. Edit `static/index.html`, `static/app.js`, `static/style.css` directly. Uvicorn's `StaticFiles` serves them verbatim.

### State management

`app.js` uses a single `state` object:

```js
const state = {
    config: null,           // from /api/config
    mode: 'batch',          // 'batch' | 'manual'
    generating: false,      // true during a run
    results: null,          // from /api/process-order-batch or /api/generate
    orderPreview: null,     // from /api/parse-order
    orderFile: null,        // File object
    manualFiles: [],        // File[]
    batchDesignFiles: [],   // File[]
};
```

All DOM updates flow through render functions:

- `renderProductionSummary()` — the main table + stat cards
- `renderResults()` — the detailed per-group output cards
- `renderOrderSummary()` — the sidebar preview summary
- `populateSelects()` — dropdown data

### Style guide

Follows the **Ecell Global Dashboard Style Guide** (`wiki/33-design-system/ECELL_STYLE_GUIDE.md` in the Obsidian vault):

- **Brand**: Cobalt `#0047AB`, Cobalt Light `#E8F0FE`, Cobalt Dark `#003380`
- **Neutrals**: Zinc scale
- **Font**: Inter
- **Status**: Emerald / Amber / Red traffic light
- **Cards**: `rounded-2xl` + `shadow-sm`

The oversized status badge is intentional — operators need to read it from across the floor.

---

## 13. Phase Roadmap

### Phase 1: Production hardening (current, 80% done)

- [x] Core pipeline (parse → resolve → render → cut files)
- [x] Auto layout (laser vs grid)
- [x] Jig size selector
- [x] Label band
- [x] Laser mirroring
- [x] Production summary panel
- [x] Ecell style guide
- [ ] Background job queue for large batches (>50 items currently block the HTTP request)
- [ ] Secondary jig support for iPads/tablets
- [ ] Auto-cleanup of old job outputs (cron)
- [ ] Structured logging with file rotation

### Phase 2: Supabase migration

- Migrate `jig_tables.csv` and `jig_devices.csv` into Supabase tables with write-protection
- Build a web admin UI for editing device/jig data (vs. the current "edit the CSV and restart")
- **Bleed management**: per-device bleed settings editable by print operators. Bleed is intentionally NOT baked into the render pipeline — it will be a separate ad-hoc post-process applied to flagged device types
- Use existing Supabase project: `nuvspkgplkdqochokhhi` (Ecell catalog)
- Wire Supabase as an order source for real-time PO consumption (replace CSV drops)

### Phase 3: Cloud deployment

- Dockerise the app
- Deploy to AWS ECS or Google Cloud Run
- S3 / GCS output storage (optional — local disk works fine for now)
- API key auth for remote access
- Basic health check endpoint

### Phase 4: DRECO marketplace lane

Currently out of scope. Would port the legacy DRECO C# marketplace image compositor (Amazon, eBay, Shopify listing variants) into Python. Requires:

- Template manager for overlay PNGs
- Perspective warp compositor
- Variant generator (9+ output types per SKU)
- S3 template cache

---

## 14. Known Issues & Limitations

### Currently working

- Grid mode: produces correct TIFFs + cut files for standard phone cases
- Bestfit mode: packs mixed laser items correctly, mirrors for face-down printing
- PSD handling: skips canvas/guides/Background, composites design group only
- Label band: 1cm band at top of every design with product/device code
- Production summary: populates on preview and after run
- Order file parsing: Amalgamated PO XLSX works out of the box

### Current limitations

1. **Background jobs**: large batches (>50 items) can take minutes and block the HTTP request. Operators may think the browser is frozen. **Workaround**: add a progress poller or use `gunicorn --timeout 600`. **Proper fix**: Phase 1 task 1.1 (worker queue).

2. **Secondary jigs**: devices that need multiple sheets (some iPads) only get the primary jig rendered. `get_secondary_jigs()` in `engine/measurements.py` returns the data but no renderer calls it yet.

3. **Bleed**: no bleed is currently applied. Previous overshoot logic was removed per product decision — bleed will be a separate ad-hoc process managed by print operators via a future admin UI (Phase 2).

4. **PSD structure dependency**: the design layer detection assumes the Ecell PSD convention (layers named `canvas`, `guides`, `Background`, etc.). A completely different PSD structure will need layer name updates in `engine/design_resolver.py:_PSD_SKIP_LAYERS`.

5. **Manual test quantity**: manual mode uses a fixed quantity per design; no grouping/deduplication.

6. **Job auto-cleanup**: output folders accumulate indefinitely. Manually delete old job folders or use `DELETE /api/jobs/{id}`.

7. **No authentication**: anyone on the network can access the app. Acceptable for the internal production floor, but must be addressed before any cloud deployment.

8. **Supabase + BigQuery order sources**: stubbed in the `order_sources` registry but return `planned` status — not yet implemented.

---

## 15. Troubleshooting

### Dropdowns empty on the Manual Test panel

Cause: `jig_tables.csv` and `jig_devices.csv` aren't being found.

Fix: ensure the `Database files/` folder exists in the project root with both CSVs. Check the startup logs — you should see:

```
[measurements] Loaded 512 jig table entries from .../jig_tables.csv
[measurements] Loaded 8199 jig device entries from .../jig_devices.csv
```

If you see `WARNING: jig_tables.csv not found`, check that `config.py:csv_data_dir` or the `DATABASE FILES/` fallback in `engine/measurements.py:_find_csv` points at the right location.

### PSD comes out with a bright green canvas background

Cause: the PSD has an unexpected top-level layer structure.

Fix: open the PSD in Photoshop, inspect the top-level layers, and either:
1. Rename the canvas layer to `canvas` or `bg`, OR
2. Add the canvas layer name to `_PSD_SKIP_LAYERS` in `engine/design_resolver.py`

### Loading spinner keeps spinning

Cause: `renderResults()` threw an error after `state.generating = false` was set but before `showResultsContainer()` was called.

Fix: the `finally` block in `processBatch()` / `generateManual()` now explicitly hides `dom.loadingState`. Also check the browser console for the actual error.

### "Port already in use" on startup

Cause: a previous instance is still running.

Fix:
```bash
lsof -i :5050
kill <pid>
```

Or change the port: `PROD_PORT=5051 python3 main.py`.

### Design image appears stretched horizontally

Cause: `uniform_scale_to_cover` was used without a crop step, letting the image overflow the slot.

Fix: the renderer now uses `fill_size_and_crop()` which scales AND center-crops to exact device dimensions. If you see stretching, check the `compose_with_label_band()` call in `renderer.py`/`bestfit.py`.

### Jig sizes are wrong / items overflow the sheet

Cause: `JIG_SIZE_PRESETS` in `api/routes_orders.py` doesn't match the physical laser bed.

Fix: measure the actual laser bed, convert to pixels at 300 DPI, and update `JIG_SIZE_PRESETS`. Also update the `<option>` labels in `static/index.html`.

---

## 16. File-by-File Reference

### `main.py`

Thin FastAPI entry point. Registers routers, mounts static files, initialises the database, and starts uvicorn. 55 lines.

### `config.py`

Pydantic `BaseSettings` with `PROD_` prefix. All paths computed from `_BASE_DIR`. 67 lines.

### `api/routes_config.py`

Single endpoint: `GET /api/config` returning products/devices/manufacturers/order_sources/design_extensions.

### `api/routes_orders.py`

The biggest file. Contains:

- `JIG_SIZE_PRESETS` — the two physical laser bed sizes
- `POST /api/parse-order` — preview endpoint
- `POST /api/process-order-batch` — full pipeline
- `_process_order_items()` — entry into the pipeline with job tracking
- `_run_order_pipeline()` — main flow: resolve designs, route to grid or bestfit
- `_render_groups()` — grid rendering loop
- `_render_groups_bestfit()` — bestfit rendering loop
- `_create_job()`, `_save_uploaded_files()`, `_cleanup_job()` — helpers

### `api/routes_manual.py`

Single endpoint: `POST /api/generate`. Wraps uploaded design files in synthetic `OrderItem`s and calls `_process_order_items()`. Used for quick single-design tests.

### `api/routes_jobs.py`

CRUD for job history + ZIP download:
- `GET /api/jobs` — list recent jobs
- `GET /api/jobs/{id}` — full job detail
- `GET /api/jobs/{id}/zip` — download all outputs as ZIP
- `DELETE /api/jobs/{id}` — delete job record and output files

### `engine/measurements.py`

Loads `jig_tables.csv` and `jig_devices.csv` at import time and caches globally. Provides:

- `get_device_measure(device, product, manufacturer)` — slot dimensions
- `get_jig_measure(manufacturer, product, device)` — sheet layout
- `get_replication_measure(product, device)` — print-ready dimensions
- `get_all_devices()`, `get_all_products()`, `get_all_manufacturers()` — dropdown data
- `_find_csv()` — searches multiple locations for the CSVs

### `engine/design_resolver.py`

Finds + loads the design artwork per item:

- `build_design_catalog()` — scan the design search dirs once, return a `{key: path}` map
- `resolve_design_for_item(item, catalog)` — priority lookup (explicit path → variant → catalog → placeholder)
- `load_design_image(path)` — PSD-aware loader
- `_composite_psd_design(psd)` — skips canvas/guides/Background
- `create_placeholder_design(item)` — colourful fallback when nothing matches

### `engine/replicator.py`

Image scaling primitives:

- `fill_size_and_crop(img, w, h)` — scale to cover + center-crop to exact size
- `uniform_scale_to_cover(img, w, h)` — scale to cover without crop
- `replicate(img, product, device)` — high-level: get replication measure and scale

### `engine/order_sources/csv_source.py`

CSV/XLSX parser with flexible header detection:

- `parse_order_file(path, default_mfr)` — dispatches by extension
- `_detect_column_mapping(headers)` — match headers to internal field names
- `_extract_order_item(row, column_map, default_mfr)` — build `OrderItem`
- `group_order_items(items)` — group by product+device+mfr, aggregate PO numbers

### `engine/jig/renderer.py`

Grid layout rendering:

- `CAMERA_LABEL_BUFFER_PX = 118` — 1cm at 300 DPI
- `compose_with_label_band(img, w, h, text)` — the label band helper
- `render_jig(items, jm, mfr)` — render a single jig sheet
- `render_all_jigs(items, jm, mfr)` — chunk items by capacity and render N sheets
- `save_jig(jig_result, dir, prefix)` — write TIFF + JPG preview files
- `make_rounded_corners`, `color_overlay`, `flip_horizontal`, `rotate_image`, `get_text_font`, `_position_image_on_jig` — primitives

### `engine/jig/bestfit.py`

SNFDH bin packing for laser items:

- `PackedItem` — dataclass: `(item_index, x, y, width, height, rotated)`
- `bestfit_pack(items, w, h, margin, allow_rotation, sort_keys)` — the algorithm
- `render_bestfit_jig(items, w, h, mfr)` — render packed sheets with label bands + mirroring
- `generate_bestfit_svg(...)` — SVG cut lines with mirroring
- `generate_bestfit_pdf(...)` — hand-built PDF cut lines
- `save_bestfit_jig(...)`, `save_bestfit_svg(...)`, `save_bestfit_pdf(...)` — writers

### `engine/jig/svg_generator.py`

Grid-mode SVG cut generation. Parses EPS `8BIM` path resources and emits transformed SVG path data. Also provides `has_cutfile()` (used by the auto layout router) and `_find_eps_cutfile()`.

### `engine/jig/pdf_generator.py`

Grid-mode PDF cut generation using reportlab.

### `engine/jig/overlay_preview.py`

Composites cut lines onto the design TIFF for QA verification. Generates one overlay JPG per jig sheet.

### `models/order.py`

`OrderItem` dataclass. Key fields: `sku`, `product`, `device`, `quantity`, `label`, `manufacturer`, `image_path`, `design_code`, `family_code`, `po_number`, `metadata`.

### `models/measurements.py`

Dataclasses: `JigMeasure`, `JigDeviceMeasure`, `ReplicationMeasure`.

### `data/db.py`

SQLite schema + CRUD: `init_db()`, `create_job()`, `update_job_status()`, `add_job_output()`, `list_jobs()`, `get_job()`, `delete_job()`. WAL mode enabled.

### `data/migrate_csv.py`

Standalone script to load the jig CSVs into SQLite tables. Not currently called by the main app (measurements.py loads the CSVs directly). Kept for future Phase 2 migration.

### `static/index.html`

The app shell. Two-mode panel (Batch Orders / Manual Test), production summary panel, results container, job history. ~220 lines.

### `static/app.js`

Frontend state + DOM logic. ~800 lines. See §12 for state model.

### `static/style.css`

Ecell style guide applied. ~1200 lines.

---

## 17. Contact & Escalation

- **Owner**: Ecell Global Production Engineering
- **Repo**: https://github.com/gemc-wq/unified-production
- **Dev environment**: Cem's MacBook (`/Users/cem/Desktop/IREN & DRECO Tools/unified-production`)
- **Production floor**: UK, FL, PH — pending rollout

For urgent production issues, fall back to the legacy IREN + LAZCUT tools (still installed on the current production PCs) until the underlying issue is diagnosed.

---

*End of handover document.*
