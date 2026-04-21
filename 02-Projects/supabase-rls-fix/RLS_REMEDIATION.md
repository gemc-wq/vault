# Supabase RLS Remediation — CRITICAL

**Date:** 2026-03-25
**Owner:** Harry (iMac)
**Priority:** P0 — Security
**Source:** Supabase email alert Mar 25 + Ava verification

## Problem
Row Level Security (RLS) is **disabled** on all tables in the `public` schema of project `auzjmawughepxbtpwuhe`. Anyone with the anon key (designed to be public/embeddable) can read ALL business data.

### Exposed Tables
| Table | Rows | Sensitive Data |
|-------|------|----------------|
| `orders` | 304,000+ | Order history, revenue, customer countries |
| `inventory` | 9,805 | Supplier names, PO prices, stock levels |
| `blank_inventory` | 5,190 | Raw material stock, supplier costs |
| `walmart_listings` | 201 | Walmart listing data |

## Fix (5 minutes)
All access is server-side via `service_role` key (scripts, dashboards). No client-side apps use `anon` key. So the fix is simple:

```sql
-- Enable RLS on all public tables
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.inventory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.blank_inventory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.walmart_listings ENABLE ROW LEVEL SECURITY;

-- Service role bypasses RLS by default in Supabase (postgres role)
-- But add explicit policy for safety:
CREATE POLICY "Service role full access" ON public.orders
  FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON public.inventory
  FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON public.blank_inventory
  FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON public.walmart_listings
  FOR ALL USING (auth.role() = 'service_role');
```

**Note:** `service_role` already bypasses RLS in Supabase by default, so the policies above are belt-and-suspenders. The critical step is the `ENABLE ROW LEVEL SECURITY` on each table — that alone blocks anon access.

## Verification
After applying, test with anon key:
```bash
curl 'https://auzjmawughepxbtpwuhe.supabase.co/rest/v1/inventory?limit=1' \
  -H "apikey: [REDACTED_SUPABASE_ANON_KEY]" \
  -H "Authorization: Bearer [REDACTED_SUPABASE_ANON_KEY]"
```
Should return empty array `[]` instead of data.

## Impact
- Zero downtime
- No code changes needed (all scripts use service_role key)
- Blocks unauthorized data access immediately
