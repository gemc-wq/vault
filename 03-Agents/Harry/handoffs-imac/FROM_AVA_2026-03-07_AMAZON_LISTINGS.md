# Ava → Harry: Amazon Active Listings → Supabase/BQ
**Date:** 2026-03-07 17:40 EST
**Priority:** P1 (PIE dependency)

## What Happened
- Cem uploaded Amazon US Active Listings (6.4GB, 3.44M SKUs) to GDrive
- It was in the Walmart folder — I've moved it to `Brain/Projects/Amazon/`
- Also moved Amazon US Session data XLSX there
- File: `Active+Listings+Report_03-05-2026.txt` (6.4GB, tab-separated)
- Too large for rclone download from Mac Studio (keeps timing out)

## Your Tasks

### 1. Load Amazon Active Listings to BQ or Supabase
- Decide: BigQuery table (probably better for 3.44M rows) or Supabase
- Table name suggestion: `amazon_us_listings` 
- Key columns we need: ASIN, SKU, item-name, price, quantity, status, fulfillment-channel
- Parse SKU into: product_type_code, device_code, design_code, design_variant
- This is the "what we have live" inventory for gap analysis

### 2. Weekly Cron — Amazon SP-API Listing Pull
- Cem wants automated weekly listing pulls for US, UK, and Germany
- Amazon SP-API keys should be available (check Cem's credentials)
- Cron: Weekly (Sunday night?) pull Active Listings Report via SP-API → load to BQ/Supabase
- Replicate across: US (amazon.com), UK (amazon.co.uk), DE (amazon.de)
- This replaces manual XLSX uploads

### 3. GDrive Amazon Folder
I've organized:
- `gdrive:Brain/Projects/Amazon/Active+Listings+Report_03-05-2026.txt` (6.4GB, US)
- `gdrive:Brain/Projects/Amazon/BusinessReportbychildAmazonUS_Jan1_Feb24 1.xlsx` (sessions data)
- Future: UK and DE listing reports go here too

## Why This Matters
PIE needs "what we have listed" (Amazon listings) vs "what we should have" (PIE scored output) to calculate gap analysis. Cem discovered HB401 converts at 2.5x snap case rate but has only $16K revenue — because it's under-listed. We need the listing inventory to quantify these gaps at scale.

## Context
- PIE brief updated to v2 with conversion metrics as core layer
- BC catalog (408K variants) being loaded to Supabase by Pixel
- BQ orders sync already running (your work — ✅)
- Dashboard PIE tabs being built by Codex

— Ava
