# SOP: Amazon Shipping Template Optimization

**Version:** 1.0  
**Created:** 2026-04-14  
**Owner:** Athena  
**Status:** DRAFT — awaiting Cem review  
**Scope:** US, UK, DE (separate pipelines per marketplace)

---

## 0. Purpose

Fix FBM listings that are on the wrong shipping template to increase conversion rate. Each marketplace has its own correct template, its own data files, and its own pricing model. **They must never be mixed.**

| Marketplace | Wrong Template | Correct Template | Expected CVR Uplift |
|-------------|---------------|-----------------|---------------------|
| US | Default Amazon Template | Reduced Shipping Template (2-day FedEx, $10.99) | ~25% (2.72% → 3.41%) |
| UK | Default Amazon Template | Nationwide Prime (next-day, Prime badge) | TBD — no analysis yet |
| DE | Standardvorlage Amazon | Reduced Shipping Template | TBD — no analysis yet |

**Secondary objective (separate workflow):** Identify Seller-Fulfilled Prime trial candidates. This requires **orders data**, not listings data — covered in Section 12.

---

## 1. Data Sources — What Exists, Where It Lives

### 1.1 Primary: Active Listings Report (per marketplace)

| Property | Detail |
|----------|--------|
| Source | Amazon Seller Central → Reports → All Listings |
| Format | Tab-delimited TSV, UTF-8 |
| Size | US: ~370MB (5.1M rows), DE: ~5.2GB, UK: similar |
| Refresh | Cloud Scheduler cron, Monday 06:00 UTC |
| Pipeline | SP-API → GCS (8MB gzip chunks) → BigQuery `amazon_reports` |
| BQ table | `merchant_listings_all_data_{marketplace}` |
| Key columns | `seller_sku`, `asin1`, `price`, `quantity`, `fulfillment_channel` |

**CRITICAL: Shipping template column (`merchant-shipping-group`) is NOT in the current BQ table.** The `custom=true` report option was added to cron jobs on Apr 14 but hasn't run yet. First run with shipping template data: **Monday Apr 20, 06:00 UTC.** Until then, shipping template data only exists in the manually amended CSV files.

### 1.2 Secondary: Business Report (per marketplace)

| Property | Detail |
|----------|--------|
| Source | Amazon Seller Central → Business Reports → Detail Page Sales and Traffic |
| Format | CSV, comma-delimited, UTF-8 with BOM |
| Size | ~8-12MB per file (~80,000 rows) |
| Refresh | Manual download by Cem |
| Location | `~/Downloads/` |

**Column name inconsistency across marketplaces:**

| Column | US Format | UK/DE Format |
|--------|-----------|-------------|
| Sessions | `Sessions - Total` (hyphen) | `Sessions – Total` (em-dash) |
| Units | `Units Ordered` | `Units ordered` (lowercase) |
| Conversion | `Unit Session Percentage` | `Unit Session Percentage` (same) |
| Sales | `Ordered Product Sales` | `Ordered Product Sales` (same) |

**Standard export has 20 columns. Does NOT include SKU or Shipping Template.**

The `_amended` files in `~/Downloads/` have 2 extra columns manually appended: `SKU` and `Shipping Template`. These were created by cross-referencing the Business Report with the Active Listings Report. DE reports also include a `Title` column (23 columns total).

**The Business Report is ASIN-level, not SKU-level.** One ASIN can map to multiple SKUs (e.g., FBA + FBM twins). The amended files resolved this by appending the SKU, but this is a manual process and may not be 1:1.

### 1.3 Inventory: Supabase `blank_inventory`

| Property | Detail |
|----------|--------|
| Source | Supabase (synced from internal systems) |
| Connection | `https://auzjmawughepxbtpwuhe.supabase.co` |
| Auth | Service role key (bypasses RLS) |
| Table | `blank_inventory` |
| Rows | 41,479 total; FL warehouse: ~1,195 active SKUs |
| Key columns | `item_code`, `warehouse`, `free_stocks` |

**Inventory uses base SKU format** (first 2 segments only):
- Inventory: `HLBWH-IPH17`
- Listings: `HLBWH-IPH17-HPOTPRI2-LMAR`
- **Join key:** First two hyphen-delimited segments of the listing SKU = `item_code` in inventory

**Warehouse codes for FL stock:**
```sql
warehouse IN ('Florida', 'FL')  AND  free_stocks > 0
```

### 1.4 Orders Data (for SFP analysis ONLY — Section 12)

| Property | Detail |
|----------|--------|
| File | `~/Downloads/AmazonUSLast90day_Sales_Combined.txt` |
| Format | Tab-delimited, UTF-8 (no BOM) |
| Size | ~12MB, ~26,700 rows |
| Refresh | Manual download |
| Key columns for SFP | `sku`, `ship-service-level`, `item-price`, `shipping-price` |

---

## 2. Data Separation Rules — NEVER MIX MARKETPLACES

Each marketplace has different:
- Shipping templates (names differ per marketplace)
- Pricing structures (USD vs GBP vs EUR)
- Fulfillment options (US has FedEx 2-day; UK has Royal Mail / Nationwide Prime; DE has DHL)
- Column name formats (US uses hyphens; UK/DE use em-dashes)

### 2.1 Storage Isolation

| Layer | US | UK | DE |
|-------|----|----|-----|
| BigQuery raw | `merchant_listings_all_data_us` | `merchant_listings_all_data_uk` | `merchant_listings_all_data_de` |
| BigQuery staging | `listings_staging` (partitioned by `loaded_at`, filtered by `marketplace_id`) | Same table, different partition | Same table, different partition |
| BigQuery curated | `listings` (clustered by `marketplace_id, asin`) | Same table, different cluster | Same table, different cluster |
| Local SQLite | `listings_us` table | `listings_uk_previous` table | `listings_de_current` table |
| Output CSVs | `fbm_wrong_template_us_YYYY-MM-DD.csv` | `fbm_wrong_template_uk_YYYY-MM-DD.csv` | `fbm_wrong_template_de_YYYY-MM-DD.csv` |

### 2.2 Validation Gate

Before ANY analysis runs, verify marketplace isolation:

```python
# MANDATORY CHECK — abort if marketplace is ambiguous
assert df['marketplace'].nunique() == 1, \
    f"ABORT: Multiple marketplaces in dataset: {df['marketplace'].unique()}"

marketplace = df['marketplace'].iloc[0]
log(f"Processing {marketplace} — {len(df)} rows")
```

### 2.3 Shipping Template Names by Marketplace

| Marketplace | Template Name | Meaning |
|-------------|--------------|---------|
| US | `Reduced Shipping Template` | 2-day FedEx, customer pays $10.99 |
| US | `Default Amazon Template` | 4-6 day standard, customer pays $6.99 |
| UK | `Nationwide Prime` | Seller-Fulfilled Prime, next-day/2-day, Prime badge |
| UK | `Default Amazon Template` | Standard shipping |
| DE | `Reduced Shipping Template` | Faster shipping option |
| DE | `Standardvorlage Amazon` | Default German template |

**These names are case-sensitive and must match exactly when filtering or updating.**

---

## 3. Procedure: Step-by-Step

### Phase 1: Data Acquisition

#### Step 1.1: Pull Active Listings Report

**Option A: Automated (after Apr 20)**
- Cloud Scheduler fires Monday 06:00 UTC
- Report flows: SP-API → GCS → BigQuery `merchant_listings_all_data_{marketplace}`
- With `custom=true`, the `merchant-shipping-group` column will be included
- **Verify column exists after first run** — if missing, the `custom` flag didn't take effect

**Option B: Manual (current state, before Apr 20)**
- Download from Seller Central → Reports → All Listings → Request Download
- Files land in `~/Downloads/` as TSV
- Must be loaded manually (Step 2)

**Option C: On-demand via middleware API**
```bash
# Request + wait + load to BQ (blocking, ~5 min)
curl -X POST \
  "https://amazon-report-middleware-175143437106.europe-west1.run.app/api/v1/reports/request-and-wait" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "X-API-Key: sk_live_ecell_2026" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "GET_MERCHANT_LISTINGS_ALL_DATA",
    "marketplace": "US",
    "report_options": {"custom": "true"}
  }'
```

#### Step 1.2: Download Business Report (manual)

1. Seller Central → Business Reports → Detail Page Sales and Traffic by Child Item
2. Select date range: Last 90 days
3. Download CSV
4. **Do NOT rename the file** — keep the original name for audit trail
5. Note: This is ASIN-level data. SKU is NOT included in the standard export.

#### Step 1.3: Fetch FL Stock from Supabase

```bash
# REST API — returns base SKUs with FL stock
curl "https://auzjmawughepxbtpwuhe.supabase.co/rest/v1/blank_inventory?select=item_code,warehouse,free_stocks&warehouse=in.(Florida,FL)&free_stocks=gt.0" \
  -H "apikey: SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer SERVICE_ROLE_KEY"
```

Or via Python:
```python
import requests

SUPABASE_URL = "https://auzjmawughepxbtpwuhe.supabase.co"
SUPABASE_KEY = "SERVICE_ROLE_KEY"  # from ~/.hermes/config/supabase.yaml

response = requests.get(
    f"{SUPABASE_URL}/rest/v1/blank_inventory",
    params={
        "select": "item_code,warehouse,free_stocks",
        "warehouse": "in.(Florida,FL)",
        "free_stocks": "gt.0"
    },
    headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
)
fl_stock = response.json()
fl_base_skus = set(item['item_code'] for item in fl_stock)
# Expected: ~1,195 base SKUs
```

---

### Phase 2: Data Staging

#### Step 2.1: Choose Processing Engine

| Option | When to Use | Pros | Cons |
|--------|-------------|------|------|
| **Python + pandas** | Files < 500MB, ad-hoc analysis | Fast iteration, flexible | Memory limits on large files |
| **Python + chunked pandas** | Files > 500MB (DE listings = 5.2GB) | Handles large files | Slower, more complex code |
| **BigQuery SQL** | Data already in BQ, need joins across tables | Scales to any size, no memory issues | Requires data in BQ first |
| **Local SQLite** | Persistent storage for delta analysis, weekly comparisons | Fast local queries, no API cost | Manual schema management |

**Recommended approach:**
1. **BigQuery** for raw data storage and heavy filtering (scales to millions of rows)
2. **Python** for orchestration, SKU parsing logic, and API calls
3. **SQLite** (`local_listings.db`) for week-over-week delta tracking
4. **CSV export** for final action lists (what to change)

#### Step 2.2: Load Active Listings into Processing Layer

**If loading from local TSV file to SQLite:**

```python
import pandas as pd
import sqlite3

# CRITICAL: Specify correct encoding and delimiter
# US files: UTF-8, tab-delimited
# UK/DE files: UTF-8 with BOM, tab-delimited
# Some DE files may be compressed/binary — check with `file` command first

def load_listings_tsv(filepath, marketplace):
    """Load Active Listings TSV into pandas DataFrame."""
    
    # Detect encoding
    encoding = 'utf-8-sig'  # handles BOM if present, works without BOM too
    
    # For large files (>1GB), use chunked reading
    filesize = os.path.getsize(filepath)
    
    if filesize > 1_000_000_000:  # >1GB
        chunks = pd.read_csv(
            filepath,
            sep='\t',
            encoding=encoding,
            dtype=str,          # Read everything as string first
            on_bad_lines='skip',
            chunksize=50000
        )
        df = pd.concat(chunks, ignore_index=True)
    else:
        df = pd.read_csv(
            filepath,
            sep='\t',
            encoding=encoding,
            dtype=str,
            on_bad_lines='skip'
        )
    
    # Add marketplace tag IMMEDIATELY
    df['marketplace'] = marketplace
    
    # Verify expected columns exist
    required_cols = ['seller-sku', 'asin1', 'price', 'quantity', 'fulfillment-channel']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in {marketplace} listings: {missing}")
    
    # Check for shipping template column
    shipping_col = None
    for candidate in ['merchant-shipping-group', 'merchant_shipping_group']:
        if candidate in df.columns:
            shipping_col = candidate
            break
    
    if shipping_col is None:
        print(f"WARNING: No shipping template column found in {marketplace} data.")
        print(f"Available columns: {list(df.columns)}")
        print("Was custom=true set in the report options?")
        df['merchant_shipping_group'] = None
    else:
        df.rename(columns={shipping_col: 'merchant_shipping_group'}, inplace=True)
    
    print(f"Loaded {len(df)} rows for {marketplace}")
    return df
```

**If data is already in BigQuery:**

```sql
-- Verify shipping template column exists after Apr 20 cron run
SELECT column_name
FROM `instant-contact-479316-i4.amazon_reports.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'merchant_listings_all_data_us';

-- If merchant_shipping_group column is present:
SELECT
    seller_sku,
    asin1,
    item_name,
    price,
    quantity,
    fulfillment_channel,
    merchant_shipping_group AS shipping_template,
    'US' AS marketplace
FROM `instant-contact-479316-i4.amazon_reports.merchant_listings_all_data_us`
WHERE fulfillment_channel != 'AMAZON_NA'  -- Exclude FBA
LIMIT 10;
```

#### Step 2.3: Store in SQLite (per-marketplace tables)

```python
def stage_to_sqlite(df, marketplace, db_path='local_listings.db'):
    """Stage listings into marketplace-specific SQLite table."""
    
    conn = sqlite3.connect(db_path)
    table_name = f"listings_{marketplace.lower()}_current"
    
    # Drop and recreate — each run is a full snapshot
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    conn.execute(f"""
        CREATE TABLE {table_name} (
            seller_sku              TEXT PRIMARY KEY,
            asin                    TEXT,
            item_name               TEXT,
            price                   REAL,
            quantity                INTEGER,
            fulfillment_channel     TEXT,
            merchant_shipping_group TEXT,
            product_type            TEXT,
            device                  TEXT,
            design                  TEXT,
            variant                 TEXT,
            is_fba                  INTEGER,
            base_sku                TEXT,
            marketplace             TEXT,
            loaded_at               TEXT
        )
    """)
    
    # Create indexes for filtering
    conn.execute(f"CREATE INDEX idx_{table_name}_design ON {table_name}(design)")
    conn.execute(f"CREATE INDEX idx_{table_name}_device ON {table_name}(device)")
    conn.execute(f"CREATE INDEX idx_{table_name}_product_type ON {table_name}(product_type)")
    conn.execute(f"CREATE INDEX idx_{table_name}_shipping ON {table_name}(merchant_shipping_group)")
    conn.execute(f"CREATE INDEX idx_{table_name}_fba ON {table_name}(is_fba)")
    conn.execute(f"CREATE INDEX idx_{table_name}_base_sku ON {table_name}(base_sku)")
    
    conn.commit()
    
    # Insert parsed data
    for _, row in df.iterrows():
        parsed = parse_sku(row['seller-sku'])
        conn.execute(f"""
            INSERT OR REPLACE INTO {table_name}
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            row['seller-sku'],
            row.get('asin1'),
            row.get('item-name', '')[:200],
            float(row['price']) if row.get('price') else None,
            int(row['quantity']) if row.get('quantity') else None,
            row.get('fulfillment-channel'),
            row.get('merchant_shipping_group'),
            parsed['product_type'],
            parsed['device_code'],
            parsed['design_code'],
            parsed['variant'],
            1 if parsed['is_fba'] else 0,
            parsed['base_sku'],
            marketplace
        ))
    
    conn.commit()
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"Staged {count} rows into {table_name}")
    conn.close()
```

---

### Phase 3: SKU Parsing

```python
# FBA exceptions — these start with F but are NOT FBA
FBA_EXCEPTIONS = {'FLAG', 'F1309', 'FRND', 'FKFLOR'}

def parse_sku(sku: str) -> dict:
    """
    Parse SKU into components.
    
    Format: {PRODUCT_TYPE}-{DEVICE_CODE}-{DESIGN_CODE}-{VARIANT}
    Examples:
        HTPCR-IPH17PMAX-NARUICO-AKA     → FBM, Soft Gel, iPhone 17 Pro Max, Naruto
        FHTPCR-IPH17PMAX-NARUICO-AKA    → FBA twin of above
        FLAG-IPH17-USCOUNTRY-USA        → NOT FBA (exception)
        HSTWH-L-WWE2JCEN-ICO           → Sticker (note: device='L' for large)
    
    Returns dict with: product_type, device_code, design_code, variant,
                       is_fba, base_sku, product_type_raw
    """
    if not sku or not isinstance(sku, str):
        return {
            'product_type_raw': '', 'product_type': '', 'device_code': '',
            'design_code': '', 'variant': '', 'is_fba': False, 'base_sku': ''
        }
    
    parts = sku.split('-')
    
    raw_type = parts[0] if len(parts) >= 1 else ''
    device_code = parts[1] if len(parts) >= 2 else ''
    design_code = parts[2] if len(parts) >= 3 else ''
    variant = '-'.join(parts[3:]) if len(parts) >= 4 else ''
    
    # FBA detection: F-prefix on product type, unless in exceptions list
    is_fba = (
        raw_type.startswith('F') 
        and raw_type not in FBA_EXCEPTIONS
        and len(raw_type) > 1  # Single 'F' is not FBA
    )
    product_type = raw_type[1:] if is_fba else raw_type
    
    # Base SKU = product_type + device (used for inventory matching)
    # Uses CLEANED product type (without F prefix)
    base_sku = f"{product_type}-{device_code}" if device_code else product_type
    
    return {
        'product_type_raw': raw_type,
        'product_type': product_type,
        'device_code': device_code,
        'design_code': design_code,
        'variant': variant,
        'is_fba': is_fba,
        'base_sku': base_sku,
    }
```

### Product Type Reference

| Code | Product Name | Typical Price (US) | Notes |
|------|-------------|-------------------|-------|
| HTPCR | Soft Gel / Thin Clear Case | $9.95-$14.95 | High volume, variable price |
| HB401 | Hybrid Hard Case (MagSafe) | $19.95 | Premium, **converts 4x vs HTPCR** |
| HLBWH | Leather Book Wallet | $24.95-$29.95 | Premium, variable by device |
| HB6CR | Clear MagSafe Case | $14.95-$19.95 | Variable price |
| HB7BK | Black MagSafe Case | $14.95-$19.95 | Variable price |
| HC | Hard Classic Case | $9.95 | Legacy product |
| HDMWH | Desk Mat | $29.95 | Non-phone product |
| H8939 | Gaming Skin | $14.95 | Non-phone product |
| HSTWH | Sticker | $4.95-$9.95 | Low-value, device='L'/'M'/'S' for size |

**IMPORTANT: Price is NOT fixed across all products.** HTPCR alone ranges from $9.95 to $14.95 depending on device tier. Wallet cases (HLBWH) range from $24.95 to $29.95. Any analysis that assumes a single fixed price is wrong.

---

### Phase 4: Apply Filters

#### Step 4.1: Filter Logic (Primary Objective)

```python
def filter_wrong_template(df, marketplace, fl_base_skus):
    """
    Filter to FBM items on wrong shipping template with FL stock.
    
    Args:
        df: DataFrame with parsed SKU columns
        marketplace: 'US', 'UK', or 'DE'
        fl_base_skus: set of base SKUs with FL warehouse stock
    
    Returns:
        DataFrame of items needing template change
    """
    
    # Define correct template per marketplace
    CORRECT_TEMPLATE = {
        'US': 'Reduced Shipping Template',
        'UK': 'Nationwide Prime',
        'DE': 'Reduced Shipping Template',
    }
    
    correct = CORRECT_TEMPLATE[marketplace]
    
    # Filter 1: Exclude FBA items
    mask_fbm = df['is_fba'] == 0
    
    # Filter 2: Must have FL stock (US) or appropriate warehouse stock (UK/DE)
    # For US: FL warehouse
    # For UK: UK warehouse (adjust warehouse filter accordingly)
    # For DE: UK warehouse (ships from UK to EU)
    mask_stock = df['base_sku'].isin(fl_base_skus)
    
    # Filter 3: Currently on WRONG template
    mask_wrong = df['merchant_shipping_group'] != correct
    
    # Filter 4: Must be active (has quantity or has been viewed)
    # Note: quantity=0 might still be listable (backorder), so check both
    mask_active = (df['quantity'].fillna(0).astype(int) > 0)
    
    # Filter 5: Must have a shipping template at all (not null)
    mask_has_template = df['merchant_shipping_group'].notna()
    
    # Combine
    filtered = df[mask_fbm & mask_stock & mask_wrong & mask_active & mask_has_template]
    
    # Log filter funnel
    print(f"--- Filter Funnel ({marketplace}) ---")
    print(f"Total rows:              {len(df)}")
    print(f"After FBM filter:        {mask_fbm.sum()}")
    print(f"After stock filter:      {(mask_fbm & mask_stock).sum()}")
    print(f"After wrong template:    {(mask_fbm & mask_stock & mask_wrong).sum()}")
    print(f"After active filter:     {(mask_fbm & mask_stock & mask_wrong & mask_active).sum()}")
    print(f"After has-template:      {len(filtered)}")
    print(f"--- End Funnel ---")
    
    return filtered
```

#### Step 4.2: Validation Checks (Run Before Proceeding)

```python
def validate_filtered_data(df, marketplace):
    """Run sanity checks on filtered data. Abort if any check fails."""
    
    errors = []
    
    # Check 1: Single marketplace
    if df['marketplace'].nunique() != 1:
        errors.append(f"CRITICAL: Multiple marketplaces in data: {df['marketplace'].unique()}")
    
    # Check 2: No FBA items leaked through
    fba_count = df[df['is_fba'] == 1].shape[0]
    if fba_count > 0:
        errors.append(f"CRITICAL: {fba_count} FBA items in filtered set")
    
    # Check 3: All items on wrong template (not already on correct)
    CORRECT = {'US': 'Reduced Shipping Template', 'UK': 'Nationwide Prime', 'DE': 'Reduced Shipping Template'}
    correct = CORRECT[marketplace]
    already_correct = df[df['merchant_shipping_group'] == correct].shape[0]
    if already_correct > 0:
        errors.append(f"WARNING: {already_correct} items already on correct template")
    
    # Check 4: Price sanity — no items with price=0 or price>$100
    if 'price' in df.columns:
        zero_price = df[df['price'].fillna(0) == 0].shape[0]
        high_price = df[df['price'].fillna(0) > 100].shape[0]
        if zero_price > 0:
            errors.append(f"WARNING: {zero_price} items with price=0")
        if high_price > 0:
            errors.append(f"WARNING: {high_price} items with price>100 — verify these are real")
    
    # Check 5: Reasonable count — if >50,000 items, something is likely wrong
    if len(df) > 50000:
        errors.append(f"WARNING: {len(df)} items — unusually high. Verify filters.")
    
    # Check 6: Template names are valid (no typos or unknown values)
    known_templates = {
        'Reduced Shipping Template', 'Default Amazon Template',
        'Nationwide Prime', 'Standardvorlage Amazon'
    }
    unknown = set(df['merchant_shipping_group'].dropna().unique()) - known_templates
    if unknown:
        errors.append(f"WARNING: Unknown template names found: {unknown}")
    
    if errors:
        print("\n=== VALIDATION RESULTS ===")
        for e in errors:
            print(f"  {e}")
        
        critical = [e for e in errors if e.startswith('CRITICAL')]
        if critical:
            raise ValueError(f"ABORTING: {len(critical)} critical validation errors")
    else:
        print(f"VALIDATION PASSED: {len(df)} items for {marketplace}")
```

---

### Phase 5: Output & Action List

#### Step 5.1: Generate Action CSV

```python
def export_action_list(df, marketplace, output_dir='~/Vault/02-Projects/amazon-data-analytics/outputs/'):
    """Export filtered items as action CSV, sorted by revenue impact."""
    
    from datetime import date
    today = date.today().isoformat()
    
    CORRECT = {'US': 'Reduced Shipping Template', 'UK': 'Nationwide Prime', 'DE': 'Reduced Shipping Template'}
    
    output = df[[
        'seller_sku', 'asin', 'product_type', 'device', 'design',
        'price', 'quantity', 'merchant_shipping_group', 'marketplace'
    ]].copy()
    
    output['target_template'] = CORRECT[marketplace]
    output['action'] = 'CHANGE_TEMPLATE'
    
    # Sort by price * quantity (proxy for revenue impact) descending
    output['revenue_proxy'] = output['price'].fillna(0) * output['quantity'].fillna(0)
    output = output.sort_values('revenue_proxy', ascending=False)
    output.drop(columns=['revenue_proxy'], inplace=True)
    
    filename = f"action_list_{marketplace.lower()}_{today}.csv"
    filepath = os.path.join(os.path.expanduser(output_dir), filename)
    output.to_csv(filepath, index=False)
    
    print(f"Exported {len(output)} items to {filepath}")
    return filepath
```

#### Step 5.2: Preview Before Push (Dry Run)

Before pushing any changes to Amazon, generate a human-readable diff:

```
=== DRY RUN: Template Change Preview ===
Marketplace: US
Items to change: 9,778
Current template: Default Amazon Template
Target template: Reduced Shipping Template

Top 10 by revenue impact:
  1. HSTWH-L-WWE2JCEN-ICO       $15.02 × 42 units  → Reduced Shipping Template
  2. HLBWH-IPAD102-DRGBSUSC-LGOK $29.40 × 9 units   → Reduced Shipping Template
  3. HLBWH-IPH17-HPOTPRI2-LMAR   $24.95 × 9 units   → Reduced Shipping Template
  ...

CONFIRM: Type 'APPLY US 9778' to proceed, or 'ABORT' to cancel.
```

---

### Phase 6: Push Changes to Amazon

#### Step 6.1: Method Selection

| Method | Batch Size | Speed | Use When |
|--------|-----------|-------|----------|
| SP-API Listings Items PATCH | 1 SKU per call, max 5/sec | ~100 SKUs/min | < 500 SKUs, need immediate feedback |
| SP-API Flat File Feed | Unlimited | 15-30 min processing | > 500 SKUs, bulk operations |
| Manual (Seller Central) | 1 at a time | Slow | Testing 1-2 SKUs |

**For 9,778 US SKUs: Use Flat File Feed.** PATCH would take ~98 minutes and risks rate limits.

#### Step 6.2: Feed File Format

```
sku	merchant-shipping-group
HSTWH-L-WWE2JCEN-ICO	Reduced Shipping Template
HLBWH-IPAD102-DRGBSUSC-LGOK	Reduced Shipping Template
HLBWH-IPH17-HPOTPRI2-LMAR	Reduced Shipping Template
```

Feed type: `POST_FLAT_FILE_INVLOADER_DATA`
Content type: `text/tab-separated-values; charset=UTF-8`

**BLOCKER: SP-API write scope required.** Current app only has Listings (read) role. Need `sellingpartnerapi::listings_items_v2021-08-01` scope added. Blocked on Patrick (PH).

#### Step 6.3: Rollback Plan

Before applying changes:
1. Export current state to `pre_change_snapshot_{marketplace}_{date}.csv`
2. Log every change to Supabase `migration_log` table
3. If issues detected: generate reverse feed file from snapshot
4. Supabase `action_reversals` table stores revert commands

---

## 4. Post-Processing: Data Cleanup

After each analysis run:

| Action | When | How |
|--------|------|-----|
| Archive previous SQLite tables | Before loading new data | Rename `listings_us_current` → `listings_us_previous` |
| Delete working DataFrames | After CSV export | `del df; gc.collect()` |
| Retain output CSVs | Always | Keep in `outputs/` with date stamp |
| Clear `~/Downloads/` source files | After confirmed load | Move to `~/Downloads/archive/` (don't delete) |
| Update BigQuery staging | After confirmed analysis | Next cron run overwrites with `WRITE_TRUNCATE` |

**Do NOT delete:**
- Output CSVs (action lists) — needed for audit trail
- SQLite `_previous` tables — needed for delta analysis
- BigQuery raw tables — needed for historical reference

**DO clean up:**
- In-memory DataFrames (large files consume GBs of RAM)
- Temporary/intermediate files
- Duplicate downloads in `~/Downloads/`

---

## 5. Error Handling

| Error | Detection | Response |
|-------|-----------|----------|
| Missing shipping template column | Column not in DataFrame after load | ABORT. Check `custom=true` in cron config. Re-request report with correct options. |
| Mixed marketplace data | `marketplace` column has >1 unique value | ABORT. Reload from separate files. |
| FBA items in filtered set | `is_fba=True` in output | ABORT. Check FBA prefix logic and exceptions list. |
| Supabase connection failure | REST API returns non-200 | RETRY 3x with 5s backoff. If still failing, proceed without stock filter but FLAG output as "unverified stock". |
| File encoding error | `UnicodeDecodeError` | Try `utf-8-sig`, then `latin-1`, then `cp1252`. Log which encoding worked. |
| BigQuery timeout | BQ job exceeds 300s | Retry once. If still failing, fall back to local SQLite. |
| SP-API rate limit (429) | HTTP 429 response | Exponential backoff: 1s, 2s, 4s, 8s. Max 5 retries. |
| Feed processing failure | Feed status = `FATAL` | Download feed processing report, identify failed SKUs, retry those only. |

---

## 6. Weekly Cadence

| Day | Time (ET) | Action | Owner |
|-----|-----------|--------|-------|
| Monday | 01:00 AM | Cloud Scheduler fires Active Listings crons | Automated |
| Monday | 06:00 AM | Verify BQ tables updated, check for shipping template column | Athena |
| Monday | 07:00 AM | Alert Cem if data issues detected | Athena |
| Saturday | 01:00 AM | Hermes runs weekly delta analysis (US) | Hermes |
| Saturday | 02:00 AM | Hermes runs weekly delta analysis (UK) | Hermes |
| Saturday | 03:00 AM | Hermes runs weekly delta analysis (DE) | Hermes |
| Ad-hoc | On demand | Run shipping template optimization | Athena + Cem |

---

## 7. Audit Trail Requirements

Every template change must be logged:

```python
audit_record = {
    'timestamp': datetime.utcnow().isoformat(),
    'marketplace': 'US',
    'sku': 'HTPCR-IPH17PMAX-NARUICO-AKA',
    'field': 'merchant_shipping_group',
    'old_value': 'Default Amazon Template',
    'new_value': 'Reduced Shipping Template',
    'method': 'feed',  # or 'patch' or 'manual'
    'feed_id': 'amzn1.feed.abc123',
    'status': 'submitted',  # submitted → processing → done/error
    'initiated_by': 'athena',
    'approved_by': 'cem'
}
```

Store in:
- Supabase `migration_log` table (persistent, queryable)
- Local CSV backup (redundancy)
- BigQuery `amazon_reports.listings_edit_log` (when middleware supports writes)

---

## 8. BigQuery Staging Architecture

### Current State (as of Apr 14)

```
amazon_reports dataset:
├── merchant_listings_all_data_us    ← 4.08M rows, RAW, NO shipping template column
├── listings                         ← EMPTY (schema has shipping_template)
└── listings_staging                 ← EMPTY (schema has shipping_template, partitioned)
```

### Target State (after Apr 20 + pipeline work)

```
amazon_reports dataset:
├── merchant_listings_all_data_us    ← RAW with shipping template column (custom=true)
├── merchant_listings_all_data_uk    ← RAW with shipping template
├── merchant_listings_all_data_de    ← RAW with shipping template
├── listings                         ← CURATED: parsed SKUs, clustered by marketplace+asin
├── listings_staging                 ← STAGING: daily load buffer, partitioned by loaded_at
└── listings_edit_log                ← AUDIT: every change pushed to Amazon

amazon_reports_stage dataset (NEW):
├── listings_parsed_us               ← VIEW over raw table with SKU segments split out
├── listings_parsed_uk               ← VIEW
└── listings_parsed_de               ← VIEW
```

### Parsed View SQL (auto-created per marketplace)

```sql
CREATE OR REPLACE VIEW amazon_reports_stage.listings_parsed_us AS
SELECT
    seller_sku AS sku,
    -- SKU parsing
    SPLIT(seller_sku, '-')[SAFE_OFFSET(0)] AS sku_segment_0,
    -- FBA detection
    CASE
        WHEN STARTS_WITH(SPLIT(seller_sku, '-')[SAFE_OFFSET(0)], 'F')
             AND SPLIT(seller_sku, '-')[SAFE_OFFSET(0)] NOT IN ('FLAG', 'F1309', 'FRND', 'FKFLOR')
        THEN TRUE
        ELSE FALSE
    END AS is_fba,
    -- Clean product type (strip F prefix for FBA)
    CASE
        WHEN STARTS_WITH(SPLIT(seller_sku, '-')[SAFE_OFFSET(0)], 'F')
             AND SPLIT(seller_sku, '-')[SAFE_OFFSET(0)] NOT IN ('FLAG', 'F1309', 'FRND', 'FKFLOR')
        THEN SUBSTR(SPLIT(seller_sku, '-')[SAFE_OFFSET(0)], 2)
        ELSE SPLIT(seller_sku, '-')[SAFE_OFFSET(0)]
    END AS product_type,
    SPLIT(seller_sku, '-')[SAFE_OFFSET(1)] AS device_model,
    SPLIT(seller_sku, '-')[SAFE_OFFSET(2)] AS design_code,
    -- Base SKU for inventory matching
    CONCAT(
        CASE
            WHEN STARTS_WITH(SPLIT(seller_sku, '-')[SAFE_OFFSET(0)], 'F')
                 AND SPLIT(seller_sku, '-')[SAFE_OFFSET(0)] NOT IN ('FLAG', 'F1309', 'FRND', 'FKFLOR')
            THEN SUBSTR(SPLIT(seller_sku, '-')[SAFE_OFFSET(0)], 2)
            ELSE SPLIT(seller_sku, '-')[SAFE_OFFSET(0)]
        END,
        '-',
        SPLIT(seller_sku, '-')[SAFE_OFFSET(1)]
    ) AS base_sku,
    -- Original columns
    asin1 AS asin,
    item_name,
    SAFE_CAST(price AS FLOAT64) AS price,
    SAFE_CAST(quantity AS INT64) AS quantity,
    fulfillment_channel,
    merchant_shipping_group AS shipping_template,
    'US' AS marketplace
FROM `instant-contact-479316-i4.amazon_reports.merchant_listings_all_data_us`;
```

---

## 9. Pricing Reality Check

**Hermes's plan assumed a fixed selling price. This is WRONG for most products.**

| Product Type | Price Model | US Price Range | Notes |
|-------------|-------------|---------------|-------|
| HB401 | Near-fixed | $19.95 | Most consistent pricing |
| HTPCR | Variable by device tier | $9.95 - $14.95 | Tier 1 devices higher |
| HLBWH | Variable by device | $24.95 - $29.95 | iPad wallets at top end |
| HC | Fixed | $9.95 | Legacy, phasing out |
| HDMWH | Fixed | $29.95 | Single price point |
| HSTWH | Variable by size | $4.95 - $9.95 | S/M/L sizes |
| HB6CR | Variable | $14.95 - $19.95 | |
| HB7BK | Variable | $14.95 - $19.95 | |

**Implication for analysis:** Revenue calculations must use actual `price` from the listings data, not assumed fixed prices. Any report showing "revenue at risk" must be based on real per-SKU prices.

---

## 10. UK-Specific Considerations

| Factor | UK Difference |
|--------|---------------|
| Correct template | `Nationwide Prime` (not `Reduced Shipping Template`) |
| Fulfillment | Seller-Fulfilled Prime via Royal Mail / Hermes courier |
| Prime badge | YES — SFP gives Prime badge, major conversion driver |
| Stock warehouse | UK warehouse (not FL) |
| Inventory filter | `warehouse IN ('UK', 'United Kingdom')` in Supabase |
| Currency | GBP — do not compare directly to USD figures |
| Column names | Use em-dashes (`–`) not hyphens (`-`) in Business Report |
| Samsung emphasis | A-series phones (A55, A35) more important in UK than US |
| HLBWH wallet distribution | Track separately — UK has different device mix |

---

## 11. DE-Specific Considerations

| Factor | DE Difference |
|--------|---------------|
| Default template name | `Standardvorlage Amazon` (German) |
| Correct template | `Reduced Shipping Template` |
| File encoding | UTF-8 with BOM — must use `utf-8-sig` |
| File size | 5.2GB — requires chunked processing |
| Fulfillment | Ships from UK warehouse to EU |
| Currency | EUR |
| Brands | Bundesliga clubs (BVB, Bayern), Real Madrid, Barcelona more prominent |
| Active Listings file | May be binary/compressed despite .txt extension — verify with `file` command |

---

## 12. Secondary Objective: SFP Trial Candidates (Orders Data)

**This section uses ORDERS data, not listings data. Completely separate pipeline.**

### 12.1 Data Source

| Property | Detail |
|----------|--------|
| File | `~/Downloads/AmazonUSLast90day_Sales_Combined.txt` |
| Format | Tab-delimited, 41 columns |
| Key columns | `sku`, `ship-service-level`, `item-price`, `shipping-price`, `quantity` |
| Rows | ~26,700 |

### 12.2 Analysis Logic

SFP candidates = customers who already choose premium shipping, proving willingness to pay for speed.

```python
# Load orders data
orders = pd.read_csv(
    '~/Downloads/AmazonUSLast90day_Sales_Combined.txt',
    sep='\t',
    encoding='utf-8',
    dtype=str
)

# Filter to SecondDay orders (premium shipping chosen by customer)
sfp_candidates = orders[orders['ship-service-level'] == 'SecondDay'].copy()

# Parse SKUs
sfp_candidates['parsed'] = sfp_candidates['sku'].apply(parse_sku)
sfp_candidates['product_type'] = sfp_candidates['parsed'].apply(lambda x: x['product_type'])
sfp_candidates['device'] = sfp_candidates['parsed'].apply(lambda x: x['device_code'])
sfp_candidates['design'] = sfp_candidates['parsed'].apply(lambda x: x['design_code'])

# Aggregate by design + device
sfp_summary = sfp_candidates.groupby(['product_type', 'device', 'design']).agg(
    order_count=('sku', 'count'),
    total_shipping_revenue=('shipping-price', lambda x: pd.to_numeric(x, errors='coerce').sum()),
    total_item_revenue=('item-price', lambda x: pd.to_numeric(x, errors='coerce').sum()),
    unique_skus=('sku', 'nunique')
).reset_index().sort_values('order_count', ascending=False)

print(f"Total SecondDay orders: {len(sfp_candidates)}")
print(f"Total shipping revenue: ${sfp_summary['total_shipping_revenue'].sum():,.2f}")
print(f"\nTop 10 SFP candidates:")
print(sfp_summary.head(10))
```

### 12.3 SFP Trial Selection Criteria

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| SecondDay orders | >= 10 in 90 days | Enough signal that customers want speed |
| Product type | HB401 or HTPCR preferred | Highest margin products |
| Device tier | Tier 1 (iPhone 17 family) | Newest devices, most sessions |
| Design | Top 20 by revenue | Don't test on low-traffic items |

### 12.4 SFP Economics

| Metric | Value |
|--------|-------|
| Customer pays (SecondDay FBM) | $10.99 |
| We pay (FedEx 2-day from FL) | ~$11-12 |
| Customer pays (SFP/Prime) | ~$0 (Prime free shipping) |
| We pay (SFP fulfillment) | ~$11-12 same |
| Benefit | Prime badge → higher conversion + Buy Box advantage |
| Flat fee model | ~$32/item (Amazon's SFP fee structure) — verify current rates |

**The SFP analysis requires orders data because only orders data shows:**
1. What `ship-service-level` the customer selected
2. What `shipping-price` the customer paid
3. Actual order volume per SKU (not just sessions/views)

Listings data cannot tell you any of this.

---

## 13. Decision Log

| # | Decision | Date | Rationale |
|---|----------|------|-----------|
| 1 | US-first for template fixes | TBD | 9,778 SKUs identified, ~$200K/year at risk, analysis most advanced |
| 2 | Use feed (not PATCH) for >500 SKUs | TBD | PATCH would take ~98 min for 9,778 SKUs; feed processes in 15-30 min |
| 3 | Separate SQLite tables per marketplace | 2026-04-14 | Prevents data mixing, enables independent analysis cycles |
| 4 | Orders data required for SFP analysis | 2026-04-14 | Listings data lacks ship-service-level, shipping-price, order volume |
| 5 | Price is NOT fixed across products | 2026-04-14 | HTPCR alone ranges $9.95-$14.95; use actual per-SKU price from data |

---

## 14. Open Items

| # | Item | Status | Owner |
|---|------|--------|-------|
| 1 | SP-API write scope | Blocked — waiting on Patrick (PH) | Cem |
| 2 | Verify `custom=true` produces shipping template column | Waiting — first cron run Apr 20 | Athena |
| 3 | Transfer middleware repo to Mac Studio | Waiting — Cem to `scp` | Cem |
| 4 | Confirm exact shipping template names in Seller Central | Need manual check | Cem |
| 5 | UK warehouse codes in Supabase | Need to query | Athena |
| 6 | DE Active Listings file format (binary vs text?) | Need to verify | Athena |
| 7 | UK/DE analysis — run after US proves out | Future | Hermes |
| 8 | SFP trial SKU selection | After primary objective complete | Cem |

---

**Document Version:** 1.0 DRAFT  
**Last Updated:** 2026-04-14  
**Next Review:** After Apr 20 cron run confirms shipping template column in BQ
