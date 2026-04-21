# Design Hub Spec — Cross-sell from One Design

## Purpose
Make “design” the anchor. Users should be able to buy:
- a phone case (snap/wallet)
- and a desk mat
- (later) laptop skin, sleeve, AirPods holder

…from the same design page without hunting.

## UI requirements
- Product type selector (tabs or segmented control)
- Device selector (only for device-bound products)
- Case type selector (snap vs wallet)
- Preview area that updates
- Add-to-cart button per selection
- **Complete the set**: recommended add-ons (mat, alternate case type) with 1-click add

## Data model requirements (Shopify)
We can implement via:
- **One product per design** with variants per product type/device (may be too many), OR
- **Products per product type** and link them via a shared `design_id` metafield (recommended)

### Recommended linking
- `design_id` metafield on every product variant family
- `design_name`
- `design_tags` (sports/anime/etc.)

Then Design Hub queries all products with the same `design_id` and renders them together.

## Guardrails
- Never show a device option if we can’t fulfill it.
- If wallet not available for a device, hide it and show “snap available”.
