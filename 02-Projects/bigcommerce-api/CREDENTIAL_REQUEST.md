# BigCommerce API Credential Request

**Purpose:** Enable PIE to query the 1.89M product catalog programmatically (instead of the 50GB TSV export)
**Time to complete:** ~5 minutes
**Who:** Cem (needs BigCommerce admin access)

---

## Steps

1. Log in to BigCommerce Control Panel
2. Go to **Settings → Store-level API accounts**
3. Click **Create API Account** → select **V2/V3 API Token**
4. Name it: `PIE - Product Intelligence` (or similar)
5. Set these **minimum scopes** (read-only is fine):
   - **Products:** `read-only`
   - **Orders:** `read-only` (for cross-reference)
   - **Content:** `read-only`
   - **Customers:** `none` (not needed)
   - **Information & Settings:** `read-only`
6. Click **Save**
7. **Copy or download** the credentials file — it shows:
   - **Store Hash** (e.g., `abc123def`)
   - **Access Token** (the `X-Auth-Token` value)
   - **Client ID** (for reference)

⚠️ The access token is only shown ONCE at creation. Download the credentials file.

---

## What I Need (send to Ava)

```
Store Hash: ___________
Access Token: ___________
Client ID: ___________ (optional but helpful)
```

## How It Will Be Used

```bash
# Example: List products (page 1)
curl -s "https://api.bigcommerce.com/stores/{STORE_HASH}/v3/catalog/products?limit=50" \
  -H "X-Auth-Token: {ACCESS_TOKEN}" \
  -H "Accept: application/json"
```

- **Read-only** — no writes, no deletes
- Query product catalog for PIE scoring (designs, devices, product types, pricing)
- Replace the 50GB TSV export with targeted API queries
- Rate limit: BigCommerce allows ~150 requests/sec for Essentials plan

---

*Created: 2026-03-09 by Ava*
*Unblocks: BigCommerce API connection test (P1), PIE catalog data (P0)*
