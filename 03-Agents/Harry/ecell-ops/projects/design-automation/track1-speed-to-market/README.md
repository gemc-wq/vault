# Track 1: Speed-to-Market — Device Mockup Generator

**AI-driven ecommerce image pipeline for Ecell Global / Head Case Designs**

Replaces the manual Photoshop smart object workflow (15-20 min/SKU) with automated device mockup generation (<5 seconds/SKU).

## Overview

This CLI tool takes a **flat design image** (the artwork that goes on a phone case, console skin, etc.) and automatically generates **ecommerce-ready product mockup images** for multiple marketplace listings.

### What It Generates

For each design + device combination:

| Output | Description |
|--------|-------------|
| 📸 **Front Shot** | Clean white-background product photo (Amazon-ready) |
| 📐 **Angled View** | 3D perspective view with drop shadow |
| 🔲 **Transparent PNG** | Alpha-channel version for custom backgrounds |
| 🎬 **Lifestyle Prompts** | Scene descriptions for Track 1b AI generation |

### Supported Devices

**📱 Phone Cases**
- iPhone 16 Pro / Pro Max
- iPhone 15
- Samsung Galaxy S25 / S25 Ultra
- Google Pixel 9 Pro

**🎮 Console Skins**
- PlayStation 5 / PS5 Digital
- Steam Deck / Steam Deck OLED

**🎮 Controller Skins**
- DualSense / DualSense Edge
- Xbox Wireless Controller

## Quick Start

```bash
# Install dependencies
npm install

# Generate sample design assets
npm run generate-templates

# Generate mockups for a single device
node src/index.js generate \
  --design input/sample-design.png \
  --device iphone-16-pro

# List all available devices
node src/index.js list
```

## CLI Commands

### `generate` — Single Device Mockup

```bash
node src/index.js generate \
  --design <path-to-design.png> \
  --device <device-id> \
  [--output <output-dir>] \
  [--sizes <presets...>] \
  [--verbose]
```

**Options:**
- `-d, --design <path>` — Path to flat design image (PNG/JPG) **(required)**
- `-D, --device <id>` — Device template ID **(required)**
- `-o, --output <dir>` — Output directory (default: `./output`)
- `-s, --sizes <presets...>` — Output size presets (default: `amazon amazon-hd`)
- `-v, --verbose` — Show detailed processing info

**Examples:**
```bash
# iPhone 16 Pro case mockup
node src/index.js generate -d artwork/nfl-eagles.png -D iphone-16-pro

# PS5 console skin, Shopify size
node src/index.js generate -d artwork/harry-potter.png -D ps5-console -s shopify

# All sizes for Amazon + eBay
node src/index.js generate -d artwork/wwe-design.png -D samsung-s25-ultra -s amazon amazon-hd ebay
```

### `batch` — Multi-Device Mockups

Generate mockups across ALL devices (or a specific category) from a single design.

```bash
node src/index.js batch \
  --design <path-to-design.png> \
  [--category <phone-case|console-skin|controller-skin>] \
  [--output <output-dir>] \
  [--sizes <presets...>]
```

**Examples:**
```bash
# All phone cases
node src/index.js batch -d artwork/peanuts.png -c phone-case

# All devices (every template)
node src/index.js batch -d artwork/design.png

# Only controller skins
node src/index.js batch -d artwork/design.png -c controller-skin -o ./controller-output
```

### `list` — Show Available Devices

```bash
node src/index.js list
node src/index.js list --category phone-case
```

### `info` — Device Template Details

```bash
node src/index.js info iphone-16-pro
node src/index.js info ps5-dualsense
```

## Output Size Presets

| Preset | Dimensions | Use Case |
|--------|-----------|----------|
| `amazon` | 1500×1500 | Amazon standard product image |
| `amazon-hd` | 2000×2000 | Amazon high-resolution |
| `shopify` | 2048×2048 | Shopify product photos |
| `ebay` | 1600×1600 | eBay listings |
| `square-sm` | 1000×1000 | Social media / thumbnails |

## Architecture

```
src/
├── index.js           CLI entry point (commander)
├── compositor.js      Image compositing engine (sharp)
├── templates.js       Device template configurations
├── utils.js           Image processing helpers
└── generate-templates.js  Sample asset generator
```

### Compositing Pipeline

1. **Design Input** — Load flat artwork PNG/JPG
2. **Device Frame** — Generate SVG device frame (case outline, camera module, etc.)
3. **Design Masking** — Clip design to case shape with rounded corners
4. **Compositing** — Layer design behind device frame
5. **Perspective Transform** — Apply affine transform for 3D angle view
6. **Shadow Generation** — Programmatic drop shadow from alpha channel
7. **Final Resize** — Output at marketplace-specific dimensions

### Adding New Devices

Edit `src/templates.js` and add a new entry to `DEVICE_TEMPLATES`:

```js
'new-device-id': {
  category: 'phone-case',           // phone-case | console-skin | controller-skin
  displayName: 'New Device Name',
  canvasSize: { width: 800, height: 1600 },
  caseShape: {
    width: 680, height: 1400,
    cornerRadius: 80,
    borderWidth: 12,
    borderColor: '#333333',
    cameraModule: { x: 60, y: 60, size: 220, lenses: 3, style: 'square' }
  },
  designArea: { x: 72, y: 300, width: 656, height: 950 },
  perspective: { rotateY: 25, rotateX: 5, scale: 0.85, offsetX: 50, offsetY: 30 },
  shadow: { blur: 40, offsetX: 15, offsetY: 25, opacity: 0.35, color: '#000000' }
}
```

## Roadmap

- **Track 1a** (this) — Local image processing with sharp ✅
- **Track 1b** — Gemini/AI lifestyle image generation from scene prompts
- **Track 1c** — Batch pipeline integration with product catalog (CSV/API)
- **Track 2** — Real-time preview web UI
- **Track 3** — Marketplace API auto-upload (Amazon, Shopify, eBay)

## Performance

| Operation | Time |
|-----------|------|
| Single device (2 sizes) | ~2-4s |
| Batch all phones (6 devices) | ~15-25s |
| Batch all devices (14 devices) | ~35-60s |

vs. Photoshop smart objects: **15-20 min per SKU** → **<5 seconds per SKU**

## License

Proprietary — Ecell Global
