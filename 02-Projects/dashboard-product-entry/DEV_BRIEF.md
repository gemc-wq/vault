# Dashboard + Product Entry — Development Brief

> Orbit task: `dashboard-product-entry`
> Priority: HIGH | Owner: Ava | Builder: Forge (Codex CLI)
> Created: 2026-03-07

## Goal
A dashboard portal with Product Entry form (single + CSV bulk upload) that writes to Supabase and triggers an n8n webhook on create.

## Tech Stack
- **Framework:** Next.js 15 + React + Tailwind CSS
- **Database:** Supabase (existing project `auzjmawughepxbtpwuhe`)
- **Auth:** Supabase anon key (no login for MVP — internal tool)
- **Deploy:** Vercel (`ecells-projects-3c3b03d7` team)
- **Webhooks:** n8n at `https://n8n.ecellglobal.com`

## Supabase Connection
```
URL: https://auzjmawughepxbtpwuhe.supabase.co
Anon Key: [REDACTED_SUPABASE_ANON_KEY]
```

## Phase 1: Dashboard Shell
- App layout with sidebar navigation
- Home page with app cards (Product Entry, Sales Dashboard link, future apps)
- Responsive design, clean UI (shadcn/ui or similar)

## Phase 2: Product Entry — Single Form
- Fields: SKU (auto-generated preview), Product Name, Brand, License, Device, Product Type, Price, Image URL
- SKU format: `{BRAND}-{DEVICE}-{PRODUCT_TYPE}-{DESIGN_ID}` (preview updates live as fields change)
- Supabase insert on submit
- POST to n8n webhook URL on successful create (configurable via env var `N8N_WEBHOOK_URL`)
- Toast notifications for success/error

## Phase 3: CSV Bulk Upload
- Drag-and-drop CSV upload zone
- Column mapping UI (map CSV columns → DB fields)
- Validation preview (show errors before insert)
- Batch insert to Supabase
- Summary: X created, Y errors

## Schema (to be created in Supabase SQL Editor)
```sql
CREATE TABLE IF NOT EXISTS products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sku TEXT UNIQUE NOT NULL,
  product_name TEXT NOT NULL,
  brand TEXT,
  license TEXT,
  device TEXT,
  product_type TEXT,
  price NUMERIC(10,2),
  image_url TEXT,
  status TEXT DEFAULT 'draft',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS policy: allow anon insert/select for MVP (internal tool)
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON products FOR ALL USING (true) WITH CHECK (true);
```

## Blockers
- Schema creation requires Cem to paste SQL into Supabase SQL Editor (or share DB password)
- n8n webhook URL TBD — needs workflow created first

## Out of Scope (MVP)
- Auth/login (internal tool, no public access)
- Image upload (URL only for now)
- Edit/delete products
- Inventory integration

## Notes
- Existing Supabase tables: `orders` (304K rows), `inventory` (9.8K rows) — don't touch these
- The `products` table is NEW and separate from existing data
- Git repo: https://github.com/ecells-projects/dashboard-product-entry (create if doesn't exist)
