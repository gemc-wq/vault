# Apr 10, 2026

## Decisions
- **Saturday Cron Workflow**: Use manual downloads (Friday 5 PM) followed by automated processing (Saturday 1 AM) to ensure reliability without needing the Cloud Run API.
- **Trademark Compliance**: Use "for" instead of "fits" in product titles to ensure marketplace compliance.
- **Memory Hierarchy**: Vault is established as Layer 3 (the canonical source of truth for continuity).
- **Cloud Run API**: Postponed development (estimated 3-5 days) to avoid rushing an unready integration.
- **Daily Memory Sync**: Automated sync to Vault at 11 PM nightly.
- **Shipping Template Audit**: Queued for Codex analysis.
- **Listings KPI Dashboard**: On hold pending CEO decision.

## Deliverables
- **Shopify Product Title Optimization**: 248 titles updated with "Officially Licensed" and trademark-safe language.
- **S3 Image Rules Consolidation**: Created `S3-IMAGE-RULES-COMPLETE.md` documenting the 6-position standard (1 hero, 3 features, 2 lifestyle).
- **Amazon Data Analysis Framework**: Completed project brief, data extraction guide, and a 3-phase implementation roadmap.
- **`weekly_listings_processor.py`**: Production-ready Python script using chunked streaming (50K rows/chunk) to handle 6-7 GB files; includes SQLite schema (8 tables, 6 views).
- **Weekly Cron SOP**: Complete documentation for the Saturday 1 AM – 8 AM automated analysis window.
- **Shipping Template Audit**: Created `SHIPPING-TEMPLATE-AUDIT.md` identifying a 15% gap in "Reduced Shipping Template" usage.
- **Process Documentation**: Created `AVA-PROCESSING-SUMMARY.md` (15-point workflow breakdown).

## Blockers
- **Large File Processing**: 6-7 GB Active Listings files previously caused memory crashes; **Resolved** via chunked streaming implementation in the new Python script.
- **API Integration Gap**: Cloud Run Amazon Reports API lacks Amazon SP-API integration and credentials; **Resolved** by reverting to the manual download/automated processing approach for the Saturday cron.

## Knowledge
- **S3 Image Reference Path**: `GDrive/Brain/Projects/seo-content-creation/`
- **Weekly Cron Schedule**: Friday 5 PM (Manual Downloads) $\rightarrow$ Saturday 1 AM - 8 AM (Automated Analysis).
- **US KPI Metrics**: 7 categories tracked (delta, product type, device coverage, performers, efficiency, mobile, low-volume/high-conv).
- **Data Extraction**: Identified 18 new potential data points across Active Listings and Child ASIN reports.

## Carry-forwards
- **Decision Required**: Build an aggregated US KPI Dashboard or continue with weekly reports?
- **Decision Required**: Priority level for the Shipping Template analysis?
- **Decision Required**: Implementation of Opus 4.6 advisor for strategic reviews?
- **Task**: Execute Saturday 1 AM Cron and review results at 8 AM.