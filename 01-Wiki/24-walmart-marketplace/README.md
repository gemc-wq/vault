# Walmart Marketplace Expansion
> **Owner:** Ava | **Status:** Active | **Updated:** 2026-03-18

## Overview
Push champion phone cases, desk mats, and gaming skins to Walmart via Shopify → Marketplace Connect, with direct API as Phase 2.

## Architecture
- **Parent:** Design (e.g., Naruto Akatsuki)
- **Variant 1:** Compatible Model (device)
- **Variant 2:** Case Type (HTPCR, HB401, HLBWH, HB6, HB7)
- **Variant Group ID:** `HCD-{DESIGN_CODE}`

## Current Status
- Walmart Lister tool: `projects/walmart-lister/walmart_lister.py` — generates Shopify CSV + Walmart multi-variant format
- CSVs generated: HTPCR (200 designs, 2,806 products), HB401 (100 designs, 605 products), Desk Mats (50 designs, 144 products)
- Total: 3,555 products with 100% EAN coverage
- EAN assignment engine: auto-assigns from 44K unassigned pool in local SQLite

## Champion Selection (FOUNDATIONAL)
- **Champions = Combined Back Case Revenue** (HTPCR + HC + HB401, all FBA merged)
- HTPCR = staple product; HB401 = newer, limited range; HC = phasing out
- ALL THREE contribute to identifying top-selling designs
- Combined elbow (80%): **590 designs** = $352K of $440K total US back case revenue
- This is the DEFINITIVE champion list for ALL marketplace expansion
- Never use HTPCR-only data for champion selection — always combine

## PULSE Elbow (product-specific)
- Combined back case design elbow: 590 designs = 80% revenue
- HTPCR-only design elbow: 183 designs = 80% revenue
- HB401-only design elbow: 179 designs = 80% revenue  
- Device elbow: 31 devices = 80% revenue (HTPCR), 13 devices (HB401)
- Desk mat elbow: 16 designs = 80% (went with 50 for 97%)

## Walmart API
- Keys: WALMART_API_KEY + WALMART_CLIENT_SECRET in Harry's .env on iMac
- Auth confirmed working: 2026-03-03
- Variant groups: up to 3 attributes per group
- Research: `research/walmart-variant-groups.md`

## Key Files
- `projects/walmart-lister/walmart_lister.py` — CLI tool
- `projects/sku-staging/walmart_matrix_combined.json` — full target matrix
- `projects/sku-staging/MARKETPLACE_EXPANSION_PLAN.md` — master plan
- `wiki/SKU_PARSING_RULES.md` — SKU parsing reference
- `research/walmart-upload-options.md` — connector comparison
