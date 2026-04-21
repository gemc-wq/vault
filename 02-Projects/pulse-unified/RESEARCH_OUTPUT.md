Loaded cached credentials.
Error stating path anthropic-ai/sdk'"
```bash


---
# FILE: wiki/17-harry-workspace/projects/amazon-sp-api/SP-API-GUIDE.md

# Amazon Selling Partner API (SP-API) Implementation Guide

This guide provides a comprehensive overview of the requirements, setup, and practical implementation details for accessing the Amazon Selling Partner API (SP-API) for **Ecell Global / Head Case Designs** on US and UK marketplaces.

## 1. Developer Registration Process

To access the SP-API, you must first register as a developer in Amazon Seller Central.

### How to Register
1. Log in to [Seller Central](https://sellercentral.amazon.com) (US) or [Seller Central UK](https://sellercentral.amazon.co.uk) as the **Primary Account User**.
2. Go to **Apps & Services** > **Develop Apps**.
3. Click **Developer Central** and then **Register as a Developer**.
4. Complete the Developer Profile application.

### Requirements
*   **Professional Selling Account:** Individual accounts are not eligible.
*   **Company Information:** Legal name, address, and contact details.
*   **Data Protection Policy (DPP) Compliance:** You must answer a detailed security questionnaire (approx. 20-30 questions) covering:
    *   Network protection (firewalls, IDS/IPS).
    *   Access management (unique IDs, MFA for all users).
    *   Encryption at rest (AES-256) and in transit (TLS 1.2+).
    *   Incident response plans.
    *   Vulnerability management (regular scanning).
*   **Acceptable Use Policy (AUP):** Agreement to only use data for permitted purposes (e.g., fulfilling orders, tax calculations).

### Timeline for Approval
*   **Typical:** 5–10 business days.
*   **Note:** If requesting "Restricted" roles (PII access), Amazon may request additional documentation or a 3rd-party audit, which can extend the timeline to several weeks.

### Self-Authorized vs. Public App
| Feature | Self-Authorized (Private) | Public App |
| :--- | :--- | :--- |
| **User Base** | Exclusive to your own organization. | Multiple external sellers. |
| **Authorization** | Simple "Self-Authorization" via Seller Central. | Full OAuth 2.0 flow (Login with Amazon). |
| **Review** | Standard developer review. | Rigorous review + Appstore listing required. |
| **Recommendation** | **Best for Ecell Global** for internal tools. | Only if you plan to sell the software. |

---

## 2. Authentication Setup

SP-API uses a multi-layered authentication approach: **LWA (Login with Amazon)** for OAuth and **IAM (AWS Identity and Access Management)** for signing requests.

### Required Credentials
*   **LWA Client ID & Client Secret:** Generated when you create your app in Seller Central.
*   **Refresh Token:** Obtained after authorizing your app. For private apps, this is generated once during self-authorization.
*   **AWS IAM User/Role:**
    *   **Access Key ID & Secret Access Key:** Used to sign requests using Signature Version 4 (SigV4).
    *   **IAM Policy:** Must have `execute-api:Invoke` permission on the SP-API resources.
    *   **IAM ARN:** The User/Role ARN must be associated with your Developer Profile in Seller Central.

### Step-by-Step Setup
1.  **Create IAM User/Role:** In AWS Console, create a user with "Programmatic: ENAMETOOLONG: name too long, stat '/Users/openclaw/.openclaw/workspace/anthropic-ai/sdk'"
```bash


---
# FILE: wiki/17-harry-workspace/projects/amazon-sp-api/SP-API-GUIDE.md

# Amazon Selling Partner API (SP-API) Implementation Guide

This guide provides a comprehensive overview of the requirements, setup, and practical implementation details for accessing the Amazon Selling Partner API (SP-API) for **Ecell Global / Head Case Designs** on US and UK marketplaces.

## 1. Developer Registration Process

To access the SP-API, you must first register as a developer in Amazon Seller Central.

### How to Register
1. Log in to [Seller Central](https:/sellercentral.amazon.com) (US) or [Seller Central UK](https:/sellercentral.amazon.co.uk) as the **Primary Account User**.
2. Go to **Apps & Services** > **Develop Apps**.
3. Click **Developer Central** and then **Register as a Developer**.
4. Complete the Developer Profile application.

### Requirements
*   **Professional Selling Account:** Individual accounts are not eligible.
*   **Company Information:** Legal name, address, and contact details.
*   **Data Protection Policy (DPP) Compliance:** You must answer a detailed security questionnaire (approx. 20-30 questions) covering:
    *   Network protection (firewalls, IDS/IPS).
    *   Access management (unique IDs, MFA for all users).
    *   Encryption at rest (AES-256) and in transit (TLS 1.2+).
    *   Incident response plans.
    *   Vulnerability management (regular scanning).
*   **Acceptable Use Policy (AUP):** Agreement to only use data for permitted purposes (e.g., fulfilling orders, tax calculations).

### Timeline for Approval
*   **Typical:** 5–10 business days.
*   **Note:** If requesting "Restricted" roles (PII access), Amazon may request additional documentation or a 3rd-party audit, which can extend the timeline to several weeks.

### Self-Authorized vs. Public App
| Feature | Self-Authorized (Private) | Public App |
| :--- | :--- | :--- |
| **User Base** | Exclusive to your own organization. | Multiple external sellers. |
| **Authorization** | Simple "Self-Authorization" via Seller Central. | Full OAuth 2.0 flow (Login with Amazon). |
| **Review** | Standard developer review. | Rigorous review + Appstore listing required. |
| **Recommendation** | **Best for Ecell Global** for internal tools. | Only if you plan to sell the software. |

---

## 2. Authentication Setup

SP-API uses a multi-layered authentication approach: **LWA (Login with Amazon)** for OAuth and **IAM (AWS Identity and Access Management)** for signing requests.

### Required Credentials
*   **LWA Client ID & Client Secret:** Generated when you create your app in Seller Central.
*   **Refresh Token:** Obtained after authorizing your app. For private apps, this is generated once during self-authorization.
*   **AWS IAM User/Role:**
    *   **Access Key ID & Secret Access Key:** Used to sign requests using Signature Version 4 (SigV4).
    *   **IAM Policy:** Must have `execute-api:Invoke` permission on the SP-API resources.
    *   **IAM ARN:** The User/Role ARN must be associated with your Developer Profile in Seller Central.

### Step-by-Step Setup
1.  **Create IAM User/Role:** In AWS Console, create a user with "Programmatic'
Here are the four requested deliverables for the PULSE Unified Product DB project.

***

# 1. DATA_SOURCE_MAP.md

This document maps all known data sources for Ecell Global's product and sales information.

| Source Type | Location | Name / Table | Records | Freshness | Contents & Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Data Warehouse** | BigQuery | `headcase.tblDesigns` | 110,635 | Assumed Live (Mirror) | **PRODUCT MASTER**. Contains `DesignID`, `DesignName`, `DesignLabel` (the `design_code`), `LineupID`, and `ImageURL`. This is the core source for all creative assets. |
| **Data Warehouse** | BigQuery | `headcase.tblDesignProductAvailability` | 1,230,108 | Assumed Live (Mirror) | Maps `DesignID` to `DesignProductID`. **CRITICAL** for understanding what combinations are possible, but `DesignProductID` is not defined. |
| **Data Warehouse** | BigQuery | `headcase.tblLineups` | ~ | Assumed Live (Mirror) | Contains `LineupID`, `Lineup` (Brand/License name). This is the master list of brands like Peanuts, Liverpool FC, etc. |
| **Data Warehouse** | BigQuery | `zero_dataset.orders` | 2,802,015 | Live (Daily Sync) | Transactional data. Contains `custom_label` (the full SKU), `paid_date`, `net_sale`, `marketplace`. Rich source for sales velocity but requires parsing. |
| **Data Warehouse** | BigQuery | `zero_dataset.amazon_active_listings` | 3,441,323 | March 5, 2026 | **KEY FOR GAP ANALYSIS**. Contains `seller_sku`, `asin1`, `item_name`, `price`. The `seller_sku` is parseable. This is the definitive list of what is live on Amazon. |
| **Data Warehouse** | BigQuery | `zero_dataset.walmart_active_listings` | 95,640 | March 4, 2026 | Contains `sku`, `item_id`, `product_name`, `price`, `gtin`, `upc`. The definitive list of what is live on Walmart. |
| **Transactional DB**| Supabase | `orders` | 305,053 | Stale (ends Feb 17, 2026) | A partial, pre-parsed mirror of the BigQuery orders table. Has useful parsed columns (`product_type_code`, `device_code`, etc.) but is incomplete and not current. |
| **Transactional DB**| Supabase | `inventory` | 9,805 | Assumed Live | Physical blank stock levels. Not directly part of the product *definition*, but critical for availability. |
| **Transactional DB**| Supabase | `walmart_listings` | 201 | **STALE**. Only 201 of 95k rows. | Useless in its current state. The BQ version supersedes this. |
| **Transactional DB**| Supabase | `amazon_listings`, `active_listings` | 0 | Empty | Schema exists but tables are empty. Intended for this project's output. |
| **Local File** | `data/amazon/` | `Active+Listings+Report...txt` | 3,441,323 | March 5, 2026 | The raw source for the `amazon_active_listings` BQ table. Confirms data is available but needs to be in a queryable format. |
| **Local File** | `data/walmart/`| `ItemReport...csv` | 95,640 | March 4, 2026 | The raw source for the `walmart_active_listings` BQ table. |
| **Local File** | `data/amazon/` | `BusinessReportbychildAmazonUS...xlsx`| 80,001 | Feb 24, 2026 | **CRITICAL BEHAVIORAL DATA**. Contains `Child ASIN`, `SKU`, `Sessions`, `Conversion Rate`. Links listing performance to our internal SKU. |
| **Local File** | `data/` | `Royalty_Advance_summary.xlsx` | 37 licenses | Assumed Current | Financial data on license obligations. Not a core product data source, but essential for prioritization. |
| **Legacy DB** | PH Network | `192.168.20.160` (MySQL) | Unknown | **LIVE MASTER** | The true source of truth for the `headcase` dataset. BQ is a mirror. Direct access is not available, BQ is the proxy. |
| **Legacy Infra** | PHP Scripts | `zero/` folder | N/A | Legacy | Contains hardcoded MWS credentials and broken BQ ETL logic with `2014` dates. Source of data integrity issues. |
| **API** | BigCommerce | (Not connected) | 1,890,000 | N/A | **MAJOR GAP**. The GoHeadCase storefront, which feeds Target+ and others, is a black hole. Contains product IDs that need mapping to `DesignID`. |

***

# 2. UNIFIED_SCHEMA.md

This is the target Supabase schema designed to create a single source of truth for all Ecell Global products.

```sql
-- Represents a physical product category, e.g., 'Snap Case', 'Desk Mat'
CREATE TABLE product_types (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL, -- e.g., 'HTPCR', 'HDMWH'
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Represents a device, e.g., 'iPhone 16 Pro Max'
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL, -- e.g., 'IPH16PM', 'SAMGS25U'
    name TEXT,
    family TEXT, -- e.g., 'iPhone 16'
    brand TEXT, -- e.g., 'Apple', 'Samsung'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Represents a brand or license, e.g., 'Peanuts', 'Liverpool FC'
CREATE TABLE lineups (
    id BIGINT PRIMARY KEY, -- From headcase.tblLineups.LineupID
    name TEXT NOT NULL, -- From LineupLabel
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Represents a single creative design asset, e.g., 'Snoopy'
CREATE TABLE designs (
    id BIGINT PRIMARY KEY, -- From headcase.tblDesigns.DesignID
    lineup_id BIGINT REFERENCES lineups(id),
    code TEXT UNIQUE NOT NULL, -- From DesignLabel, e.g., 'PNUTSNF'
    name TEXT, -- From DesignName
    image_url TEXT,
    status INT, -- From DesignStatus
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- The UNIFIED PRODUCT TABLE. A unique, sellable item.
-- This represents the combination of a design on a specific product type for a specific device.
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_type_id INT NOT NULL REFERENCES product_types(id),
    device_id INT NOT NULL REFERENCES devices(id),
    design_id BIGINT NOT NULL REFERENCES designs(id),
    sku_fragment TEXT NOT NULL, -- Generated: {product_type.code}-{device.code}-{design.code}
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(product_type_id, device_id, design_id)
);

-- Marketplace-specific information for a given product.
CREATE TABLE marketplace_listings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id),
    marketplace TEXT NOT NULL, -- e.g., 'amazon_us', 'walmart_us', 'ebay_uk'
    sku TEXT NOT NULL, -- The full seller SKU, e.g., 'HTPCR-IPH16PM-PNUTSNF-COL'
    marketplace_product_id TEXT, -- e.g., Amazon ASIN, Walmart Item ID
    variant_info TEXT, -- e.g., 'COL', 'MAT'
    title TEXT,
    price NUMERIC(10, 2),
    currency TEXT,
    gtin TEXT,
    upc TEXT,
    url TEXT,
    status TEXT, -- e.g., 'ACTIVE', 'INACTIVE'
    is_buy_box_eligible BOOLEAN,
    last_synced_at TIMESTAMPTZ,
    UNIQUE(product_id, marketplace)
);

```

***

# 3. MIGRATION_PLAN.md

This is a step-by-step plan to ETL data from BigQuery into the new Supabase `UNIFIED_SCHEMA`.

**Pre-requisite:** Establish a secure connection or use a data transfer tool (e.g., `gsutil` for CSV exports, or a Python script with BQ and Supabase clients) to move data from BigQuery to Supabase.

### Step 1: Populate Core Dimension Tables

These tables have no dependencies on each other and can be loaded in parallel.

1.  **`lineups`**:
    *   **Extract**: `SELECT LineupID, LineupLabel FROM headcase.tblLineups`
    *   **Transform**: Map `LineupID` to `id`, `LineupLabel` to `name`.
    *   **Load**: Insert into `supabase.lineups`.

2.  **`product_types`**:
    *   **Extract**: `SELECT DISTINCT product_type_code FROM zero_dataset.orders WHERE product_type_code IS NOT NULL`
    *   **Transform**: Create a record for each unique `product_type_code`.
    *   **Load**: Insert into `supabase.product_types`.

3.  **`devices`**:
    *   **Extract**: `SELECT DISTINCT device_code FROM zero_dataset.orders WHERE device_code IS NOT NULL`
    *   **Transform**: Create a record for each unique `device_code`. (Further transformation could parse the code to populate `family` and `brand`).
    *   **Load**: Insert into `supabase.devices`.

### Step 2: Populate `designs` Table

This table depends on `lineups` being populated first.

1.  **Extract**: `SELECT DesignID, LineupID, DesignLabel, DesignName, ImageURL, DesignStatus FROM headcase.tblDesigns`
2.  **Transform**:
    *   Map `DesignID` to `id`.
    *   Map `LineupID` to `lineup_id`.
    *   Map `DesignLabel` to `code`.
    *   Map `DesignName` to `name`.
    *   Map `ImageURL` to `image_url`.
    *   Map `DesignStatus` to `status`.
3.  **Load**: Insert into `supabase.designs`.

### Step 3: Populate the Unified `products` Table

This is the most critical step and depends on all previous tables. It involves creating the canonical product definition.

1.  **Extract**: The ideal source is `headcase.tblDesignProductAvailability` joined with other tables to resolve product and device codes. However, since `DesignProductID` is opaque, we will generate combinations from `zero_dataset.orders` as a starting point.
    `SELECT DISTINCT product_type_code, device_code, design_code FROM zero_dataset.orders WHERE product_type_code IS NOT NULL AND device_code IS NOT NULL AND design_code IS NOT NULL`
2.  **Transform**:
    *   For each unique row from the query:
        *   Look up `product_types.id` from `product_type_code`.
        *   Look up `devices.id` from `device_code`.
        *   Look up `designs.id` from `design_code`.
        *   Generate `sku_fragment` as `{product_type_code}-{device_code}-{design_code}`.
    *   Create a new record with the looked-up foreign keys.
3.  **Load**: Insert the transformed records into `supabase.products`.

### Step 4: Populate `marketplace_listings`

This step links the canonical products to their real-world listings on each marketplace.

1.  **Extract (Amazon)**: `SELECT seller_sku, asin1, item_name, price FROM zero_dataset.amazon_active_listings`
2.  **Transform (Amazon)**:
    *   For each row, parse the `seller_sku` to get `product_type_code`, `device_code`, `design_code`, and `variant_info`.
    *   Create the `sku_fragment` as `{product_type_code}-{device_code}-{design_code}`.
    *   Look up the corresponding `products.id` using the `sku_fragment`.
    *   Prepare a `marketplace_listings` record:
        *   `product_id`: The ID found above.
        *   `marketplace`: 'amazon_us' (or derive from source).
        *   `sku`: The full `seller_sku`.
        *   `marketplace_product_id`: `asin1`.
        *   `variant_info`: The parsed variant.
        *   `title`, `price`, `status`, etc.
3.  **Load (Amazon)**: Insert into `supabase.marketplace_listings`.
4.  **Extract (Walmart)**: `SELECT sku, item_id, product_name, price, gtin, upc FROM zero_dataset.walmart_active_listings`
5.  **Transform (Walmart)**: Repeat the parsing and lookup process as with Amazon data.
6.  **Load (Walmart)**: Insert into `supabase.marketplace_listings`.

***

# 4. GAP_REPORT.md

This report identifies missing data and broken processes that must be addressed to create a complete and accurate Unified Product Database.

### 1. Missing ASIN → SKU → DesignID Bridge
*   **Gap:** While we have all the component parts, the bridge isn't explicitly built. We have Amazon listings with `(seller_sku, asin)` and Headcase data with `(DesignID, design_code)`.
*   **How to Fill:** The `MIGRATION_PLAN` outlines the solution. Parsing the `seller_sku` from `amazon_active_listings` is the key. The `seller_sku` contains the `design_code`, which is the `DesignLabel` in `tblDesigns`. This allows us to join marketplace data (`asin`, `sessions`, `conversion`) to our internal product master (`DesignID`, `LineupID`).

### 2. Incomplete BigCommerce Integration
*   **Gap:** Data for the GoHeadCase storefront (1.89M products), which feeds Target+, is completely missing. We cannot perform gap analysis for these crucial channels. We don't know how BigCommerce `product_id` maps to our `DesignID`.
*   **How to Fill:** A dedicated connector must be built for the BigCommerce API. The top priority is to extract the full product catalog, including the `SKU` and any custom fields that might contain the `DesignID` or constituent codes.

### 3. Ambiguous UPC/GTIN Authority
*   **Gap:** The Walmart data contains `gtin` and `upc`, but the master Amazon listings do not. It is unclear where these codes are generated and managed. Without a master source, we cannot reliably list products on marketplaces that require them (like Target+).
*   **How to Fill:** Investigate the Zero infrastructure and PHP codebase. There is likely a script or database table responsible for generating or storing these codes. If one does not exist, a process for generating and assigning them must be created and stored in the `marketplace_listings` table.

### 4. No Definitive Image Source
*   **Gap:** `headcase.tblDesigns.ImageURL` is the most likely candidate for the master product image. However, other systems (BigCommerce, legacy folders) might hold different or higher-resolution images.
*   **How to Fill:** Confirm that `ImageURL` is the single source of truth. A script should be run to check a sample of these URLs for validity. If other sources exist, a consolidation strategy is needed, potentially storing a master image in Supabase Storage and referencing it from the `designs` table.

### 5. Broken BigQuery Sync & Data Staleness
*   **Gap:** The analysis of the `zero/` folder revealed that ETL scripts are likely broken, referencing hardcoded `2014` dates. This calls the "liveness" of the `zero_dataset` in BigQuery into question. Furthermore, key Supabase tables (`orders`, `walmart_listings`) are demonstrably stale.
*   **How to Fill:** The legacy PHP ETL scripts must be abandoned. A new, reliable data pipeline must be built to sync the local PH MySQL master (`192.168.20.160`) to BigQuery daily. The Supabase data should be considered a temporary, read-only cache populated by this project, not a live data source itself.

### 6. Undefined `DesignProductID`
*   **Gap:** The `tblDesignProductAvailability` table, which should define all valid `Design` x `Product` combinations, uses an opaque `DesignProductID`. We do not know what this ID maps to (e.g., a specific device or product type).
*   **How to Fill:** This requires institutional knowledge. The information is likely buried in the legacy Zero PHP code or database. Reverse-engineering the code that uses this table is the most likely way to decipher its meaning. Without it, we are forced to infer valid combinations from historical order data, which may be incomplete.
