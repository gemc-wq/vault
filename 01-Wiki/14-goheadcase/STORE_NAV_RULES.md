# Store Navigation + Product Routing Rules

## Goal
Keep navigation clean while preserving cross-sell.

## Storefronts
- Warehouse (main): broad audience
- Gaming (subdomain): gaming intent

## Product routing
### Warehouse-only
- Phone cases (snap/wallet)
- Tablet cases
- Laptop skins/cases/sleeves (Phase 1.5)
- AirPods holders (Phase 1.5)

### Gaming-only
- Console skins
- Controller accessories
- Handheld accessories

### Both (bridge)
- Desk mats / mouse mats

## Shopify implementation
Use a metafield/tag:
- `storefront_visibility`: `warehouse` | `gaming` | `both`

Frontends filter catalog by this flag.
