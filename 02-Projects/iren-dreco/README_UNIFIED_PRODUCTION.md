# Unified Production Pipeline

FastAPI application that unifies the IREN (print jig rendering) and LAZCUT (laser cut file generation) workflows into a single web app for Ecell Global's print-on-demand production.

Replaces the legacy Java IREN app and C#/.NET DRECO components with a modern Python stack that takes CSV/XLSX order exports and produces print-ready TIFFs, SVG/PDF laser cut files, and overlay previews.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/gemc-wq/unified-production.git
cd unified-production

# 2. Install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Provide the reference data
# The `Database files/` folder (gitignored) should contain:
#   - jig_tables.csv
#   - jig_devices.csv
#   - jig_measurement.csv
# These are the IREN MySQL exports. Copy from your backup to the project root.

# 4. Run
python3 main.py
# Open http://localhost:5050
```

---

## How It Works

1. **Upload** an `Amalgamated_PO_Export*.xlsx` order file (or any CSV/XLSX with SKU, product, device, quantity columns)
2. **Preview** parses rows, groups by product+device+manufacturer, and shows a production summary table
3. **Run pipeline** — for each group:
   - Resolve design artwork (PSD/JPG/PNG from the designated folders, or uploaded assets)
   - Composite PSD design layers (skipping canvas/guides/Background)
   - Scale and crop to device dimensions
   - Add 1cm label band above the camera hole with `{manufacturer} - {product} - {device}`
   - Place on a jig sheet (grid layout for print, best-fit packing for laser)
   - Render design TIFF + white ID TIFF + SVG/PDF cut lines + overlay preview
4. **Download** individual files or the full ZIP

### Layout Modes

- **Auto** (default): items with an EPS cut file in LAZCUT use best-fit packing, items without use the fixed grid
- **Grid**: always fixed grid based on jig_tables definitions
- **Best Fit**: always pack mixed sizes using SNFDH bin packing, sorted alphabetically by SKU

### Laser (Best-Fit) Items

- Designs are **mirrored horizontally** because laser prints face-down
- SVG cut shapes are also mirrored to match
- Sheet dimensions come from the jig size selector (6042 or 7151) — placement is dynamic within those bounds

### Jig Sizes

- **6042**: 7205 × 4961 px
- **7151**: 8386 × 6024 px

---

## Project Structure

```
unified-production/
├── main.py                      # FastAPI entry point
├── config.py                    # Pydantic settings (env-based)
├── requirements.txt
│
├── api/                         # FastAPI routers
│   ├── routes_config.py         # GET /api/config — dropdown data
│   ├── routes_orders.py         # POST /api/parse-order, /api/process-order-batch
│   ├── routes_manual.py         # POST /api/generate — manual test runs
│   └── routes_jobs.py           # GET /api/jobs, /api/jobs/{id}, ZIP download, delete
│
├── engine/                      # Core business logic
│   ├── measurements.py          # Load jig_tables + jig_devices CSVs
│   ├── design_resolver.py       # Find/load PSD/JPG/PNG artwork per item
│   ├── replicator.py            # Scale + crop design to device dimensions
│   ├── order_sources/
│   │   └── csv_source.py        # CSV/XLSX parser with flexible header detection
│   └── jig/
│       ├── renderer.py          # Grid layout jig rendering + label band helper
│       ├── bestfit.py           # SNFDH bin packing + laser jig rendering
│       ├── svg_generator.py     # EPS → SVG cut-line conversion
│       ├── pdf_generator.py     # EPS → PDF cut-line conversion
│       └── overlay_preview.py   # Composite design + cut lines for QA
│
├── models/                      # Dataclasses
│   ├── order.py                 # OrderItem
│   └── measurements.py          # JigMeasure, JigDeviceMeasure, ReplicationMeasure
│
├── data/                        # Database layer
│   ├── db.py                    # SQLite schema + CRUD for jobs + job_outputs
│   └── migrate_csv.py           # Standalone: load CSVs into SQLite (optional)
│
├── static/                      # Frontend (plain HTML/CSS/JS, no build step)
│   ├── index.html
│   ├── app.js
│   └── style.css
│
└── Database files/              # Gitignored — copy from your backup
    ├── jig_tables.csv           # Jig sheet grid definitions
    ├── jig_devices.csv          # Per-device slot dimensions
    └── jig_measurement.csv
```

---

## Order File Format

The parser accepts the Ecell `Amalgamated_PO_Export*.xlsx` format directly. Column detection is flexible — any of these aliases work:

| Field | Recognized columns |
|-------|-------------------|
| **PO Number** | `HPT_PO_Number`, `po_number`, `po`, `order_number`, `purchase_order`, `reference` |
| **Product** | `ProductCode`, `product_code`, `product`, `producttype` |
| **Device** | `Unit`, `unit_code`, `device`, `device_code`, `phone` |
| **Quantity** | `Quantity`, `qty`, `count`, `units` |
| **SKU / Custom Label** | `Custom_Label`, `sku`, `product_sku`, `item_code` |
| **Manufacturer** | `Sage_Server`, `manufacturer`, `mfr`, `server`, `location` |
| **Image path** | `image`, `image_path`, `file`, `design_file` |

Manufacturer aliases: `UK` / `United Kingdom`, `FL` / `Florida`, `DE` / `Germany`, `PH` / `Philippines`.

---

## Design Resolution

The `design_resolver` looks for artwork in this order:
1. Explicit `image_path` column from the order row
2. Variant mapping from `design_variants.csv` (if configured)
3. Catalog search by SKU, label, design code, family code, or SKU parts
4. Uploaded design assets for the current run
5. Known workspace folders: `DRECO Input files Phone Back Case/`, `DRECO Input file Leather Wallet 2/`
6. Generated placeholder artwork as a final fallback

### PSD Handling

PSD files contain both artwork and guide/canvas layers. The loader composites **only design layers**, skipping layers named `background`, `bg`, `canvas`, or `guides` (case-insensitive). This excludes:
- The bright canvas background color
- Red/blue alignment guide rectangles
- The Photoshop Background layer

If no design layers are detected, it falls back to the full composite.

---

## Label Band (Camera Hole Area)

Every rendered design has a **1 cm white band at the top** (where the camera hole is on most phone cases) containing:

```
{manufacturer} - {product} - {device}
```

e.g. `UK - HC - IPH16PMAX`

At 300 DPI, 1 cm = 118 px. The design is scaled to `dev_height - 118` and pasted below the band. The band text is drawn **before** rotation and mirroring, so:
- Grid mode: label reads normally on the print
- Laser mode (mirrored for face-down printing): label is also mirrored, which is correct — it reads right when the case is flipped to its final orientation

---

## Data Model

### Jobs Table (SQLite — `production.db`)

| Column | Notes |
|--------|-------|
| `id` | 8-char hex job ID |
| `source_type` | `csv_upload`, `manual_upload`, etc |
| `source_filename` | Original filename |
| `manufacturer` | Default manufacturer for the run |
| `status` | `pending`, `running`, `completed`, `failed` |
| `created_at` | ISO timestamp |
| `completed_at` | ISO timestamp |
| `total_items` | Row count |
| `total_sheets` | Jig sheets rendered |
| `output_dir` | Path to the run's output folder |
| `manifest_json` | Full manifest as JSON string |
| `error_message` | Error text if failed |

### job_outputs Table

One row per generated file (TIFF, SVG, PDF, preview, overlay) linked to the parent job via FK with cascading delete.

---

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Serves `static/index.html` |
| `GET` | `/api/config` | Returns products/devices/manufacturers/order_sources |
| `POST` | `/api/parse-order` | Parses a CSV/XLSX and returns the grouped preview |
| `POST` | `/api/process-order-batch` | Full batch pipeline — returns job manifest |
| `POST` | `/api/generate` | Manual mode — design-first single run |
| `GET` | `/api/jobs` | List recent jobs |
| `GET` | `/api/jobs/{id}` | Job details with full manifest |
| `GET` | `/api/jobs/{id}/zip` | Download all outputs as a ZIP |
| `DELETE` | `/api/jobs/{id}` | Delete job record and output files |
| `GET` | `/output/<path>` | Serves files from the output directory |
| `GET` | `/static/<path>` | Serves files from the static directory |

---

## Environment Variables

All settings can be overridden via environment variables with the `PROD_` prefix or via a `.env` file:

```bash
PROD_PORT=5050
PROD_HOST=0.0.0.0
PROD_OUTPUT_DIR=/path/to/output
PROD_CSV_DATA_DIR=/path/to/Database files
PROD_LAZCUT_BASE=/path/to/LAZCUT
PROD_FONT_PATH=/path/to/custom.ttf
PROD_TIFF_COMPRESSION=tiff_lzw
PROD_JPEG_PREVIEW_QUALITY=85
```

---

## Style Guide

The frontend follows the **Ecell Global Dashboard Style Guide** — see `wiki/33-design-system/ECELL_STYLE_GUIDE.md` in the Obsidian vault.

- **Brand**: Cobalt `#0047AB`, Cobalt Light `#E8F0FE`, Cobalt Dark `#003380`
- **Neutrals**: Zinc scale (`#FAFBFC` background, `#171717` text, `#e4e4e7` borders)
- **Font**: Inter
- **Status**: Emerald / Amber / Red traffic light
- **Cards**: `rounded-2xl` with `shadow-sm`
- **Status badge**: Extra-large (200px, 16px bold) for visibility from a production floor

---

## Known Limitations & Future Work

- **Background job processing**: large batches run synchronously on the HTTP request thread — works for 10–50 items, will need a worker queue for 100+
- **Secondary jigs**: the data model supports multiple jig sheets per device (iPads, tablets), but only the primary is rendered today
- **Database backend**: jig/device data is still CSV-based — planned migration to Supabase in Phase 2
- **Bleed**: intentionally not in the render pipeline. Bleed is a per-device-type ad-hoc adjustment managed by print operators through a separate process (likely an Illustrator script or a post-processing step).
- **BigQuery / Supabase order sources**: stubbed but not wired

See the Obsidian vault (`Claude plans/zazzy-doodling-wall.md`) for the full phase roadmap.

---

## Development Notes

### Running with auto-reload

`main.py` uses `uvicorn.run(..., reload=True)` so any file change reloads the server. Keep the terminal window visible to see import errors.

### Testing a single design manually

1. Switch to **Manual Test** mode
2. Pick product, device, manufacturer
3. Drop a PSD, JPG, or PNG into the upload zone
4. Choose Jig Size and Layout Mode
5. Click **Generate Manual Run**

### Testing a batch order

1. Stay in **Batch Orders** mode
2. Drop an `Amalgamated_PO_Export*.xlsx` file
3. Click **Preview Order** — the production summary table populates
4. Click **Run Full Pipeline** — outputs appear below

### Debugging PSD issues

```python
from psd_tools import PSDImage
psd = PSDImage.open('path/to/file.psd')
for layer in psd:
    print(f"{layer.name} visible={layer.is_visible()} bbox={layer.bbox}")
```

Layer names `background`, `bg`, `canvas`, `guides` are skipped by the loader. If a new PSD layout includes the design inside a differently-named group, update `_PSD_SKIP_LAYERS` in `engine/design_resolver.py`.

### Adding a new jig size

Edit `JIG_SIZE_PRESETS` in `api/routes_orders.py`:

```python
JIG_SIZE_PRESETS = {
    "6042": (7205, 4961),
    "7151": (8386, 6024),
    "newsize": (width_px, height_px),
}
```

Then add the option to both `<select id="jig-size">` and `<select id="manual-jig-size">` in `static/index.html`.

---

## License

Internal Ecell Global tool — not for external distribution.
