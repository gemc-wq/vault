# Listing Edit App — Planning Document

**Created:** April 12, 2026
**Owner:** Hermes
**Status:** Planning

---

## 1. Purpose

A web application for bulk editing Amazon listings with SKU-based filtering. Connects to Amazon via the Google Cloud middleware to make real-time updates.

---

## 2. Core Features

### 2.1 SKU Filtering (based on SKU_PARSING_RULES.md)

| Filter Type | Description | Example |
|-------------|-------------|---------|
| **Product Type** | First segment of SKU (with F prefix handling) | `HTPCR`, `HB401`, `HDMWH` |
| **Product Type + Device** | Product type AND device code combo | `HTPCR` + `IPH17PMAX` |
| **Design** | Design code (third segment) | `NARUICO`, `PNUTCHA`, `LFC` |
| **Marketplace** | US/UK/DE | Separate lists per marketplace |
| **Fulfillment** | FBA vs FBM | `F` prefix filter |
| **Current Shipping Template** | Filter by existing template | Default, Reduced, Nationwide Prime |

### 2.2 Edit Actions

| Action | Field | Bulk Support | Notes |
|--------|-------|--------------|-------|
| Update Shipping Template | `merchant-shipping-group` | Yes | Dropdown: Reduced / Default / Nationwide Prime |
| Update Price | `price` | Yes | Apply fixed price OR percentage adjustment |
| Preview Changes | — | Yes | Show affected SKUs before submitting |

### 2.3 Dashboard Integration

- Link from Amazon UK/US Dashboard to edit candidates
- Pre-filter based on dashboard insights (e.g., "Low conversion → switch to Reduced Shipping")

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      LISTING EDIT APP                           │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │   Frontend  │ ←→ │   Backend   │ ←→ │  Local Data Cache   │ │
│  │  (HTML/JS)  │    │  (Flask)    │    │  (SQLite/JSON)      │ │
│  └─────────────┘    └──────┬──────┘    └─────────────────────┘ │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MIDDLEWARE (Google Cloud Run)                   │
│  https://amazon-report-middleware-175143437106.europe-west1.run.app
│                                                                 │
│  Endpoints needed:                                              │
│  - GET /listings?marketplace=US&filters=...                    │
│  - PATCH /listings/bulk (shipping template, price)             │
│  - GET /shipping-templates                                     │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Amazon SP-API                                 │
│  - GET_MERCHANT_LISTINGS_ALL_DATA (read listings)              │
│  - POST /listings/v0/listings/{sku} (update pricing)           │
│  - PUT /feeds/v0/feeds (shipping template via feed)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Sources

### 4.1 Local Data (no API call needed)

| Source | Location | Refresh |
|--------|----------|---------|
| US Active Listings | `~/Downloads/US_Active_listings_report*.txt` | Weekly |
| UK Active Listings | `~/Downloads/UK_Live_listings_report*.txt` | Weekly |
| Business Reports | `~/Downloads/*BusinessReport*.csv` | Daily/Weekly |

### 4.2 Middleware API (real-time)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/listings` | GET | Fetch current listings from Supabase/BQ |
| `/listings/bulk` | PATCH | Update multiple listings |
| `/shipping-templates` | GET | List available templates |
| `/marketplace-status` | GET | Health check per marketplace |

---

## 5. SKU Parsing Logic

```python
def parse_sku(sku: str) -> dict:
    """Parse SKU into components per SKU_PARSING_RULES.md"""
    parts = sku.split('-', 3)  # Max 4 parts
    
    raw_type = parts[0] if len(parts) >= 1 else ''
    device_code = parts[1] if len(parts) >= 2 else ''
    design_code = parts[2] if len(parts) >= 3 else ''
    variant = parts[3] if len(parts) >= 4 else ''
    
    # FBA prefix handling
    FBA_EXCEPTIONS = {'FLAG', 'F1309', 'FRND', 'FKFLOR'}
    is_fba = raw_type.startswith('F') and raw_type not in FBA_EXCEPTIONS
    product_type = raw_type[1:] if is_fba else raw_type
    
    return {
        'sku': sku,
        'product_type_raw': raw_type,
        'product_type': product_type,
        'device_code': device_code,
        'design_code': design_code,
        'variant': variant,
        'is_fba': is_fba,
    }

# Product type display names
PRODUCT_TYPES = {
    'HTPCR': 'Soft Gel MagSafe',
    'HB401': 'Hard Case MagSafe',
    'HLBWH': 'Leather Wallet',
    'HB6CR': 'Clear MagSafe',
    'HB7BK': 'Black MagSafe',
    'HC': 'Hard Classic',
    'HDMWH': 'Desk Mat',
    'H8939': 'Gaming Skin',
    'HSTWH': 'Sticker',
}

# Brand/Design prefixes
BRAND_PREFIXES = {
    'NARU': 'Naruto',
    'PNUT': 'Peanuts',
    'HPOT': 'Harry Potter',
    'LFC': 'Liverpool FC',
    'AFC': 'Arsenal FC',
    'FCB': 'FC Barcelona',
    'RMCF': 'Real Madrid',
    'THFC': 'Tottenham',
    'CFC': 'Chelsea FC',
    'DRGB': 'Dragon Ball',
    'WWE': 'WWE',
    'NBA': 'NBA',
    'NFL': 'NFL',
}
```

---

## 6. UI Wireframe

```
┌──────────────────────────────────────────────────────────────────────┐
│  📦 LISTING EDIT APP                              [US ▼] [UK ▼] [DE ▼]│
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─ FILTERS ──────────────────────────────────────────────────────┐ │
│  │                                                                 │ │
│  │  Product Type:  [All Types        ▼]                           │ │
│  │  Device:        [All Devices      ▼]  (disabled if no type)    │ │
│  │  Design:        [All Designs      ▼]                           │ │
│  │  Fulfillment:   [All ▼]  [FBM only] [FBA only]                │ │
│  │  Current Template: [All ▼] [Default] [Reduced] [Nationwide]   │ │
│  │                                                                 │ │
│  │  [Apply Filters]  [Clear]  [Export CSV]                        │ │
│  │                                                                 │ │
│  │  Showing 1,234 SKUs from 7,500 total                           │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌─ BULK EDIT ────────────────────────────────────────────────────┐ │
│  │                                                                 │ │
│  │  [x] Select All  [1234 selected]                               │ │
│  │                                                                 │ │
│  │  ┌─ Shipping Template ──┐  ┌─ Price ────────────────────────┐  │ │
│  │  │ [ ] Update Shipping  │  │ [ ] Update Price               │  │ │
│  │  │ Template: [Reduced ▼]│  │ Type: [Fixed $ ___ ▼]          │  │ │
│  │  │                      │  │       [Percent +___% ]         │  │ │
│  │  │ Templates:           │  │                                │  │ │
│  │  │ • Reduced Shipping   │  │ Preview: $19.95 → $21.95       │  │ │
│  │  │ • Default Amazon     │  │                                │  │ │
│  │  │ • Nationwide Prime   │  │                                │  │ │
│  │  └──────────────────────┘  └────────────────────────────────┘  │ │
│  │                                                                 │ │
│  │  [Preview Changes]  [Submit to Amazon]                         │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌─ SKU TABLE ────────────────────────────────────────────────────┐ │
│  │ [x]│ SKU                    │ Type   │ Device    │ Design    │ …│ │
│  ├────┼────────────────────────┼────────┼───────────┼───────────┼──┤ │
│  │ [x]│ HTPCR-IPH17PMAX-NARUICO│ Soft   │ iPhone 17 │ Naruto    │ …│ │
│  │ [x]│ HTPCR-IPH17PRO-NARUICO │ Soft   │ iPhone 17 │ Naruto    │ …│ │
│  │ [ ]│ HTPCR-IPH16PMAX-NARUICO│ Soft   │ iPhone 16 │ Naruto    │ …│ │
│  │ [ ]│ HB401-IPH17PMAX-LFCKIT │ Hard   │ iPhone 17 │ Liverpool │ …│ │
│  │    │ ...                    │        │           │           │  │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  [◀ Prev]  Page 1 of 25  [Next ▶]  [Show: 50 ▼]                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 7. API Endpoints (Backend)

### 7.1 GET /api/listings

```
GET /api/listings?marketplace=US&product_type=HTPCR&device=IPH17PMAX

Response:
{
  "total": 1500,
  "filtered": 45,
  "page": 1,
  "page_size": 50,
  "data": [
    {
      "sku": "HTPCR-IPH17PMAX-NARUICO-AKA",
      "asin": "B0XXXXXXXXX",
      "product_type": "HTPCR",
      "device_code": "IPH17PMAX",
      "device_name": "iPhone 17 Pro Max",
      "design_code": "NARUICO",
      "brand": "Naruto",
      "is_fba": false,
      "price": 19.95,
      "shipping_template": "Default Amazon Template",
      "sessions_90d": 1250,
      "units_90d": 45,
      "conversion_rate": 3.6
    },
    ...
  ]
}
```

### 7.2 PATCH /api/listings/bulk

```
PATCH /api/listings/bulk
{
  "skus": ["HTPCR-IPH17PMAX-NARUICO-AKA", "HTPCR-IPH17PRO-NARUICO-AKA"],
  "marketplace": "US",
  "updates": {
    "shipping_template": "Reduced Shipping Template",
    "price": null  // or {"type": "fixed", "value": 21.95} or {"type": "percent", "value": 10}
  }
}

Response:
{
  "success": true,
  "submitted": 2,
  "job_id": "feed-abc123",
  "message": "Bulk update submitted. Check status at /api/jobs/feed-abc123"
}
```

### 7.3 GET /api/filters/options

```
GET /api/filters/options?marketplace=US

Response:
{
  "product_types": [
    {"code": "HTPCR", "name": "Soft Gel MagSafe", "count": 2500},
    {"code": "HB401", "name": "Hard Case MagSafe", "count": 1800},
    ...
  ],
  "devices": {
    "HTPCR": [
      {"code": "IPH17PMAX", "name": "iPhone 17 Pro Max", "count": 150},
      {"code": "IPH17PRO", "name": "iPhone 17 Pro", "count": 145},
      ...
    ]
  },
  "designs": [
    {"code": "NARUICO", "brand": "Naruto", "count": 500},
    {"code": "PNUTCHA", "brand": "Peanuts", "count": 450},
    ...
  ]
}
```

---

## 8. Middleware Integration

### 8.1 Current Middleware Capabilities

From `MIDDLEWARE_INTEGRATION_PLAN.md`:
- Base URL: `https://amazon-report-middleware-175143437106.europe-west1.run.app`
- Auth: `X-API-Key` header + `Authorization: Bearer` (gcloud identity token)
- Data flows to BigQuery `amazon_reports` dataset

### 8.2 New Endpoints Needed on Middleware

| Endpoint | Status | Notes |
|----------|--------|-------|
| GET /listings | Partial | Exists via BQ, needs filtering |
| PATCH /listings/bulk | NEW | Submit feed to SP-API |
| GET /shipping-templates | NEW | List available templates |
| GET /jobs/{id} | NEW | Check feed submission status |

### 8.3 SP-API Feed for Shipping Template

Shipping template updates use the `_POST_FLAT_FILE_INVLOADER_DATA_` feed type:

```xml
TemplateType=Offer
MerchantShippingGroup=Reduced Shipping Template
sku	merchant-shipping-group
HTPCR-IPH17PMAX-NARUICO-AKA	Reduced Shipping Template
HTPCR-IPH17PRO-NARUICO-AKA	Reduced Shipping Template
```

---

## 9. Security

| Concern | Solution |
|---------|----------|
| API Key Storage | Environment variables, never in code |
| User Auth | Simple API key for internal use (same as middleware) |
| Rate Limiting | Max 100 SKUs per bulk request |
| Audit Log | Log all changes to `~/Vault/03-Agents/Hermes/logs/` |

---

## 10. File Structure

```
~/Vault/03-Agents/Hermes/listing-edit-app/
├── app.py                  # Flask backend
├── sku_parser.py           # SKU parsing logic
├── middleware_client.py    # API client for middleware
├── templates/
│   └── index.html          # Main UI
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js          # Frontend logic
├── data/
│   ├── listings_us.json    # Cached listings
│   └── listings_uk.json
└── logs/
    └── audit.log           # Change history
```

---

## 11. Implementation Phases

### Phase 1: Read-Only (Week 1)
- [ ] Build Flask app with local data loading
- [ ] Implement SKU parsing
- [ ] Create filter UI
- [ ] Display SKU table with pagination

### Phase 2: Middleware Integration (Week 2)
- [ ] Connect to middleware API for live data
- [ ] Implement filter options endpoint
- [ ] Add shipping template dropdown

### Phase 3: Write Operations (Week 3)
- [ ] Implement bulk preview
- [ ] Connect to SP-API via middleware
- [ ] Add audit logging
- [ ] Test with small batch

### Phase 4: Dashboard Integration (Week 4)
- [ ] Add "Edit in Bulk" links from dashboard
- [ ] Pre-populate filters from dashboard context
- [ ] Production deployment

---

## 12. Questions for Cem

1. **Shipping Template Names** - Are these the exact names in Amazon?
   - "Reduced Shipping Template"
   - "Default Amazon Template"
   - "Nationwide Prime"

2. **Price Update Logic** - Should we support:
   - Fixed price (set to $X.XX)
   - Percentage adjustment (+X% or -X%)
   - Both?

3. **Middleware Write Access** - Does the current middleware support write operations, or do we need to add that?

4. **Approval Workflow** - Should bulk changes require approval before submission?

---

## 13. Success Metrics

| Metric | Target |
|--------|--------|
| Time to update 100 SKUs | < 5 minutes |
| Error rate on submissions | < 1% |
| Time saved vs manual | 90%+ |

---

*Plan created by Hermes | April 12, 2026*
