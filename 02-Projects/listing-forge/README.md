# ListingForge MVP

## Overview
ListingForge is the productized version of the Creative Pipeline image and content funnels. It automates the generation of product mockups and listing copy from raw design files and SKU definitions.

## Scope
- **Lane 1**: Automated Image Generation (incorporating legacy IREN/DRECO logic)
- **Lane 2**: Automated SEO Copy Generation (title/description via Echo)
- **Lane 3**: Bulk Marketplace Export (Shopify CSV, Walmart feed)

## Architecture
- Python/Pillow for image composite (see `lane1_poc_v3.py`)
- Claude Sonnet for SEO copywriting
- Pandas for bulk feed generation

## Next Steps
- Integrate Lane 1 POC with a test batch of artwork.
- Define the configuration schema for device jigs.