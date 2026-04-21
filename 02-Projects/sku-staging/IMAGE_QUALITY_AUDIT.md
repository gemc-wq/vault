# PULSE Champion Designs: Image Quality Audit

**Date:** March 14, 2026
**Auditor:** Sven (Creative & Marketing Director)
**Context:** Auditing image quality for the top 10 PULSE champion designs on BigCommerce for Walmart syndication.

## Walmart Requirements
- **Dimensions:** ≥ 1000x1000px
- **Format:** Standard web images (JPEG/PNG)
- **Content:** White background preferred, no watermarks, clear product focus

## Executive Summary
After querying the BigCommerce catalog API for the top 10 champions, all representative SKUs meet Walmart's baseline dimensional and format requirements. 
- **Format:** All images are delivered as standard `JPEG` (`.jpg`).
- **Dimensions:** The `url_zoom` assets provided by the BigCommerce CDN are universally `1280x1280px`.
- **Image Count:** Each champion design has a healthy image stack of 6 to 7 images.

## detailed Findings by Champion Design

| Rank | Design Code | Representative SKU | Image Count | Max Dimensions | Meets Walmart Specs? | Notes |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | **NARUICO** ($57.8K) | `HTPCR-IPH17-NARUICO-AKA` | 7 | 1280x1280 | ✅ Yes | Standard JPEGs. Image stack is fully populated. |
| 2 | **LFCLVBRD** ($54.1K) | `HTPCR-DESRE21PR-LFCLVBRD-BLK1` | 7 | 1280x1280 | ✅ Yes | Standard JPEGs. |
| 3 | **AFCLOGOS** ($42.6K) | `HTPCR-HP40-AFCLOGOS-BBN` | 7 | 1280x1280 | ✅ Yes | Standard JPEGs. |
| 4 | **PNUTCHA** ($39.9K) | `HLBWH-IPH14PRO-PNUTCHA-LCBR` | 6 | 1280x1280 | ✅ Yes | Leather Book Wallet format; 6 images. |
| 5 | **PNUTBOA** ($27.1K) | `HLBWH-IPH14PRO-PNUTBOA-LXOX` | 6 | 1280x1280 | ✅ Yes | Leather Book Wallet format; 6 images. |
| 6 | **FCBCRE** ($25.1K) | `HTPCR-DESRE21PR-FCBCRE-BLK` | 7 | 1280x1280 | ✅ Yes | Standard JPEGs. |
| 7 | **ADVEGRA** ($23.0K) | `HLBWH-DESRE21PR-ADVEGRA-LBMO` | 6 | 1280x1280 | ✅ Yes | Standard JPEGs. |
| 8 | **PNUTCBR** ($22.7K) | `HTPCR-IPH11-PNUTCBR-AUT` | 7 | 1280x1280 | ✅ Yes | Standard JPEGs. |
| 9 | **NARUCHA** ($21.7K) | `HTPCR-IPH17-NARUCHA-ITA` | 7 | 1280x1280 | ✅ Yes | Standard JPEGs. |
| 10 | **MCBDKIT25** ($21.1K) | `HLBWH-FIRE722-MCBDKIT25-LAWY` | 6 | 1280x1280 | ✅ Yes | Leather Book Wallet format; 6 images. |

## Potential Issues & Recommendations

1. **Dimensional Compliance is Assured:** 
   BigCommerce automatically generates and stores a `1280x1280` zoom layer (`url_zoom`) for all of these SKUs. Because Walmart requires a minimum of 1000x1000px, we can safely syndicate the `url_zoom` URLs directly to Walmart without upscaling.

2. **White Background & Watermarks:**
   - While the format and dimensions meet requirements, we must ensure that the primary (Image 1) shot for each listing has a pure white background and contains no promotional overlay text or branding watermarks (e.g., "Official Licensee" badges).
   - *Recommendation:* Our pipeline should explicitly map the cleanest, front-facing mockup (typically Image 1 or Image 7 based on the file naming structure `TP-CR-IPH17-1`) as the main Walmart image. 

3. **Format Validation:**
   - All pulled assets are standard `JPEG` (`.jpg`), which is perfectly compatible with Walmart's ingestion engine.

**Next Steps for Pipeline:**
Proceed with mapping the `url_zoom` field from BigCommerce directly into the Shopify/Walmart push feed. No new image rendering or resolution upscaling is required for these 10 champion designs.
