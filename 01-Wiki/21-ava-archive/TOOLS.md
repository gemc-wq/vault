# TOOLS.md - Local Notes

## Credentials & Accounts

### Shared Identity (Harry & Ava)
- **Email:** harry@ecellglobal.com
- **Password:** [REDACTED_PASSWORD]
- **Purpose:** GitHub, Vercel, OAuth (OpenAI/Gemini)
- **Stored:** 2026-02-06

## API Keys

### Firecrawl
- Key: [REDACTED_FIRECRAWL_KEY]
- Purpose: Web scraping for competitor research
- Stored: 2026-02-02

### Apify
- Key: [REDACTED_APIFY_KEY]
- Purpose: Instagram/TikTok social data
- Stored: 2026-02-02

### ElevenLabs (SAG)
- Key: [REDACTED_ELEVENLABS_KEY]
- Purpose: Text-to-speech (natural voice generation)
- Stored: 2026-02-02

### Anthropic (Claude Sonnet 4.5)
- Key: [REDACTED_ANTHROPIC_KEY]
- Purpose: Content writing (per Cem's request)
- Stored: 2026-02-02

### OpenAI Whisper
- Key: Configured in openclaw.json
- Purpose: Speech-to-text

### Notion
- Key: Stored in ~/.config/notion/api_key
- Purpose: Project management

### Google Drive (rclone)
- Remote: gdrive
- Status: Connected and working

### Gemini
- Key: [REDACTED_GEMINI_KEY]
- Purpose: Web search, content generation, analysis (shared with Harry)
- Stored: 2026-02-02

### Gemini (Image Analysis - Dedicated)
- Key: [REDACTED_GEMINI_IMAGE_KEY]
- Purpose: Image analysis (Ava exclusive)
- Stored: 2026-02-02

### Airweave
- URL: https://app.airweave.ai
- API: https://api.airweave.ai
- Key (Cem): FKgDVMh5rKabjF2eOpIPM_oNMqEoyxb2Ns5cLqxv3IM
- Key (Harry): A_lap_FuyguMzNrWTwpHm7l38EG_4ryWT5Rpxl1LM1w
- Account: gemc@ecellglobal.com (primary), harry@ecellglobal.com (secondary)
- Org: Ecell Global
- Plan: Developer (Free) — 10 sources, 500 queries/mo, 50K entities/mo
- Collection: mirror-test-collection-xsvj7d (ID: 766d2326-9520-476b-823d-d1781ecea955)
- Expires: Jun 2, 2026 (90 days)
- SDK: airweave-sdk 0.9.8 (Python)
- Purpose: MIRROR-PRODUCT context retrieval evaluation
- Stored: 2026-03-04

### Gamma.app
- Key: [REDACTED_GAMMA_KEY]
- Purpose: AI presentation creation
- Stored: 2026-02-02

### N8N
- URL: https://n8n.ecellglobal.com
- API Key: [REDACTED_N8N_API_KEY]
- Login: gemc@ecellglobal.com / ecell_n8n_2026!
- SSH: gcloud compute ssh n8n-server --zone=us-east1-b --project=opsecellglobal
- Purpose: Email triage, CS automation, workflow automation
- Stored: 2026-02-28

### Supabase (Orders & Inventory)
- Project ID: auzjmawughepxbtpwuhe
- URL: https://auzjmawughepxbtpwuhe.supabase.co
- Anon key: [REDACTED_SUPABASE_ANON_KEY]
- Service role key (JWT): [REDACTED_JWT_PREFIX].eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1emptYXd1Z2hlcHhidHB3dWhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUyMDM0MSwiZXhwIjoyMDg2MDk2MzQxfQ.fSBkEs_WCqzUtyY0Z0KoNuL5vEiXrxQin5NmKRlFZzc
- Tables: orders (304K), inventory (9.8K), walmart_listings (loading)
- Views: v_inventory_alerts, v_sales_by_device, v_sales_by_product_type, v_stock_consumption, v_unmatched_skus
- Stored: 2026-03-03
