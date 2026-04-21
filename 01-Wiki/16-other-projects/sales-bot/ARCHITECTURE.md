# Head Case Designs — AI Sales Search + Chat Architecture

> **Project:** Semantic search + conversational sales agent for [goheadcase.com](https://goheadcase.com)
> **Date:** 2026-02-17 (v2 — refined per Cem's priorities)
> **Author:** Harry (AI COO) for Ecell Global
> **Status:** Architecture Proposal — Ready for Review

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Core Challenge: Semantic Search Over 1.89M Products](#2-the-core-challenge)
3. [Current Data Assets (Audited)](#3-current-data-assets)
4. [Recommended Architecture](#4-recommended-architecture)
5. [Deep Dive: Semantic Search Engine](#5-deep-dive-semantic-search-engine)
6. [Deep Dive: Sales-Ranked Results](#6-deep-dive-sales-ranked-results)
7. [Deep Dive: Delivery Estimates](#7-deep-dive-delivery-estimates)
8. [Deep Dive: Returns & CS Knowledge](#8-deep-dive-returns--cs-knowledge)
9. [Frontend: Search-First Experience](#9-frontend-search-first-experience)
10. [Cart Integration](#10-cart-integration)
11. [Data Pipeline Design](#11-data-pipeline-design)
12. [Implementation Phases](#12-implementation-phases)
13. [Vertex AI Search for Commerce vs Alternatives](#13-vertex-ai-search-for-commerce-vs-alternatives)
14. [Cost Estimates](#14-cost-estimates)
15. [Risks & Mitigations](#15-risks--mitigations)

---

## 1. Executive Summary

### The Problem
GoHeadCase.com has **1.89M product variants** — but BigCommerce's default search is keyword-based. A customer searching **"valentine case for iPhone 16"** gets results only if products are literally tagged "valentine." They won't find the hearts collection, the love-themed designs, or the pink/red cases that are thematically perfect. Revenue is lost to bad search.

### The Solution
A **search-first AI experience** that combines:

1. **Semantic search** — understands *intent and meaning*, not just keywords. "Valentine case" → hearts, love, pink, red, romantic designs. "Something cute for my daughter" → Kawaii, Peanuts, playful designs.

2. **Sales-ranked results** — best sellers surface first, not random catalog order. Uses real BigCommerce order data (18,656 orders) + design-level sales signals.

3. **Conversational assistant** — the search bar *can talk back*. Helps narrow 1.89M products to the 3-4 perfect ones through guided discovery, upsell, and cross-sell.

4. **Delivery estimates** — answers "when will I get it?" based on shipping destination, fulfillment location (UK/US/Philippines), and carrier.

5. **Returns policy** — embedded knowledge from existing CS bot, integrated into the same experience.

### Architecture in One Sentence
**Vertex AI Search for Commerce** (semantic product retrieval + conversion-optimized ranking) → **Cloud Run orchestrator** (Gemini Flash for sales reasoning + delivery/returns logic) → **Custom search widget** (BigCommerce Storefront API for add-to-cart).

---

## 2. The Core Challenge

### Why Keyword Search Fails for Head Case

| Customer Search | What They Want | What Keyword Search Returns |
|----------------|---------------|----------------------------|
| "valentine case for iPhone 16" | Hearts, love, pink/red cases for iPhone 16 | Only products literally tagged "valentine" (few/none) |
| "something cute for my daughter" | Kawaii, Peanuts, playful, pastel designs | Nothing (no product named "cute for daughter") |
| "harry potter iphone 16 pro max tough case" | Specific licensed design + device + case type | Might work, but won't rank by popularity |
| "matching phone and tablet cases" | Same design across devices | Nothing (keyword can't do cross-device matching) |
| "professional looking case" | Minimal, leather, matte black designs | Nothing (no product tagged "professional") |
| "NFL Chiefs case" | Kansas City Chiefs licensed designs | Maybe, if "Chiefs" is in product name |

### What Semantic Search Does Differently

Semantic search works by converting product data into **embedding vectors** — dense numerical representations of meaning. When a user searches "valentine case," the search engine:

1. Converts the query to a vector
2. Finds products whose vectors are *close in meaning* — not just matching words
3. Returns products with **hearts, love, romantic, pink, red** themes because those concepts are semantically close to "valentine"

The critical ingredient: **what text do we embed?** For Head Case, it's:
- Design name + design title (e.g., "Deathly Hallows" + "Harry Potter Deathly Hallows Design")
- **Design keywords** from `cfxb2b_db.design_keywords` (38,245 designs have rich keyword text like "College Crimson Tide Bama Champions Big Al Angry Elephant")
- Category/type labels (Animals, Kawaii, Patterns, Romantic, etc.)
- Personality tags (Fashionista, Hipster, Sporty, Playful, Romantic)
- Color information (on Black, on Pink, on Clear, etc.)
- Brand name (NFL, WWE, Harry Potter, Peanuts)
- Device model + case type

This combined text creates a **rich semantic fingerprint** for each product that captures its visual theme, style, mood, and identity — far beyond any single keyword.

---

## 3. Current Data Assets (Audited)

### BigQuery Project: `instant-contact-479316-i4`

#### headcase dataset (Datastream — real-time sync from production DB)

| Table | Rows | Key Fields | Role |
|-------|------|-----------|------|
| `tblDesigns` | 110,215 (92,638 active) | DesignID, DesignName, DesignLabel, LineupID, ImageURL | Core design catalog |
| `tblDesignProductAvailability` | 1,227,979 | DesignID ↔ ProductColorID, IsApproved | Design × product matrix |
| `tblDesignGroupAvailability` | 70,300 | DesignID ↔ GroupID, IsApproved | Design × group matrix |
| `tblLineups` | 10,248 | LineupID, Lineup, LineupLabel | Design collections |
| `tblLineupTypes` | 3,305 | LineupID ↔ TypeID | Collection → category |
| `tblLineupPersonalities` | 2,207 | LineupID ↔ PersonalityID | Collection → style |
| `tblTypes` | 27 | TypeID, Type, Description | Categories (Animals, Kawaii, Patterns, etc.) |
| `tblPersonalities` | 8 | PersonalityID, Personality | Styles (Fashionista, Hipster, Sporty, Playful, Romantic, etc.) |
| `tblTags` | 42 | TagID, TagName | Searchable tags |
| `tblDesignTags` | 445 | DesignID ↔ TagID | Design → tag mapping |

#### cfxb2b_db dataset (Datastream — real-time sync from B2B/operations DB)

| Table | Rows | Key Fields | Role |
|-------|------|-----------|------|
| `design_keywords` | 38,266 | DesignID, Keywords (rich text) | **🔑 THE SEMANTIC GOLDMINE** — rich keyword phrases per design |
| `design_titles` | 815,274 | DesignID, LanguageID, Title | Multi-language design titles |
| `brands` | ~200+ | BrandID, Name, Label, BrandStatus | Brand catalog (NFL, WWE, LFC, etc.) |
| `lineups_brand` | 9,859 | LineupID ↔ BrandID | Lineup → brand mapping |
| `products` | 72 | ProductID, ProductCode, Description | Case type catalog (72 product types) |
| `product_types` | 17 | ProductTypeID, ProductName | Case categories (Phone Cases, Gaming, Audio, etc.) |
| `product_colors` | 222 | ProductColorID, ProductID, ColorID | Product ↔ color mapping |
| `colors` + `color_titles` | 100+ | ColorID, Title | Color names (Black, Pink, Clear, etc.) |
| `prices` | 1,162 | BrandID, ProductColorID, CurrencyID, Price | Price matrix |
| `units` | 2,292 | UnitID, Description, UnitBrandModel, Compatibility | Device models (iPhone 16 Pro Max, Galaxy S25, etc.) |
| `sales` | 25,091 | SaleID, BrandID, Quantity, SaleDate | **Sales volume data** (up to 2018 — need to supplement with BC orders) |

### BigCommerce Store: `otle45p56l`

| Data | Count | Access |
|------|-------|--------|
| Orders (shipped) | 17,815 | REST Management API v2 `/orders` |
| Orders (total) | 18,656 | Includes pending, refunded, etc. |
| Products/Variants | ~1.89M | REST Catalog API v3 `/catalog/products` |
| Recent order avg | ~$19.95 | Single-item orders typical |

### Key Data Insight
The `cfxb2b_db.design_keywords` table is the **semantic search foundation**. Each design has a rich keyword phrase:
```
DesignID 153533: "College Crimson Tide Bama 18th Eighteenth National Champions 2020 2021 Team Logotype Marks Logo"
```
This is exactly the kind of text that embeds well for semantic search. Combined with category, personality, and brand data, we have everything needed to build a world-class search index.

**For sales ranking**, we need to combine:
1. `cfxb2b_db.sales` (25K rows, historical)
2. BigCommerce orders (18,656 orders with line items — current data)
3. BigCommerce analytics (views, add-to-cart events)

---

## 4. Recommended Architecture

### Two-Layer System

```
┌──────────────────────────────────────────────────────────────────────┐
│                    LAYER 1: SEMANTIC SEARCH ENGINE                    │
│                                                                      │
│  Vertex AI Search for Commerce                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Product Data Store (from BigQuery)                            │  │
│  │  • 1.89M products with rich semantic text                     │  │
│  │  • Design keywords + titles + categories + personalities      │  │
│  │  • Custom attributes: sales_rank (numeric), brand, device     │  │
│  │                                                                │  │
│  │  Capabilities:                                                 │  │
│  │  ✅ Semantic search (vector embeddings, intent understanding) │  │
│  │  ✅ Boost/bury by sales_rank (best sellers first)            │  │
│  │  ✅ Faceted filtering (device, case type, brand, price)      │  │
│  │  ✅ Autocomplete with semantic awareness                     │  │
│  │  ✅ "More like this" recommendations                         │  │
│  │  ✅ Conversational filtering (multi-turn refinement)         │  │
│  │  ✅ KPI-optimized ranking (learns from user events)          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↕ API                                   │
├──────────────────────────────────────────────────────────────────────┤
│                    LAYER 2: INTELLIGENT AGENT                        │
│                                                                      │
│  Cloud Run (Python/FastAPI)                                          │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Gemini 2.0 Flash (reasoning engine)                          │  │
│  │                                                                │  │
│  │  ✅ Natural language → search query translation               │  │
│  │  ✅ Result enrichment (sales context, upsell suggestions)    │  │
│  │  ✅ Delivery estimate calculation                            │  │
│  │  ✅ Returns policy knowledge                                 │  │
│  │  ✅ Upsell logic (soft gel → tough case)                     │  │
│  │  ✅ Cross-sell logic (phone → matching tablet case)          │  │
│  │  ✅ Brand-aware responses (licensed brand guidelines)        │  │
│  │  ✅ Session memory (Firestore)                               │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↕ API                                   │
├──────────────────────────────────────────────────────────────────────┤
│                    FRONTEND: SEARCH + CHAT                           │
│                                                                      │
│  Custom Widget on goheadcase.com (via Script Manager)                │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  🔍 Enhanced Search Bar (replaces/augments default BC search) │  │
│  │  💬 Chat Panel (slides open for conversational refinement)    │  │
│  │  🛒 Product Cards with Add-to-Cart (Storefront API)          │  │
│  │  📦 Delivery Estimate Badge on each product                  │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Deep Dive: Semantic Search Engine

### 5.1 Why Vertex AI Search for Commerce (Not Generic Vertex AI Search)

| Capability | Search for Commerce | Generic Vertex AI Search |
|-----------|-------------------|------------------------|
| Semantic understanding | ✅ Commerce-tuned LLMs (trained on Google Shopping) | ✅ General-purpose |
| Product-specific intent | ✅ Understands "valentine" → hearts/love/red | ⚠️ Weaker for product context |
| Boost/bury by numeric attribute | ✅ Built-in `boostSpec` with conditions | ✅ Supported |
| User event learning | ✅ Trains on view/click/cart/purchase events | ❌ Not built-in |
| KPI optimization | ✅ Optimizes for conversion, CTR, revenue | ❌ Not available |
| Autocomplete | ✅ Commerce-tuned completions | ⚠️ Basic |
| Recommendations | ✅ "Bought together", "Similar items" | ❌ Separate setup |
| Conversational search | ✅ Multi-turn filtering agent | ⚠️ Requires Dialogflow CX |
| Catalog limit | ✅ 4M products (search enabled) | ✅ 10M documents |
| Facets & filtering | ✅ Dynamic facets from user behavior | ✅ Manual config |

**Commerce wins** because it understands that "valentine" is semantically related to hearts/love/romance *in a shopping context* — not just in general text. This is the Google Shopping intelligence applied to your catalog.

### 5.2 Building the Semantic Product Document

Each product in the Vertex AI Search data store needs a **rich text document** that captures its full semantic identity. This is what gets embedded and searched against.

#### The Semantic Text Formula

```
{design_title} - {design_keywords} | 
{brand_name} {lineup_name} | 
{category}: {category_description} | 
Style: {personalities} | 
{case_type_description} for {device_model} | 
Color: {color_name} |
Tags: {tag_names}
```

#### Example: A Real Product

```json
{
  "id": "HC-IP16PM-TOUGH-153533",
  "title": "Alabama Crimson Tide 18th National Champions - Tough Case for iPhone 16 Pro Max",
  "description": "College Crimson Tide Bama 18th Eighteenth National Champions 2020 2021 Team Logotype Marks Logo. Sports design featuring Alabama Crimson Tide championship artwork. Perfect for the college sports fan. Tough dual-layer protection case.",
  
  "categories": ["Sports", "Characters"],
  "brands": ["College Sports"],
  "tags": ["college", "football", "champions", "alabama", "crimson tide"],
  
  "attributes": {
    "device_model": {"text": ["iPhone 16 Pro Max"]},
    "case_type": {"text": ["Tough Case"]},
    "design_name": {"text": ["Crimson Tide 18th Champions"]},
    "lineup": {"text": ["Alabama Crimson Tide"]},
    "personality": {"text": ["Sporty", "Outgoing"]},
    "color": {"text": ["on Black"]},
    "sales_rank": {"numbers": [847]},
    "total_sold": {"numbers": [23]},
    "price_usd": {"numbers": [24.99]}
  },
  
  "priceInfo": {
    "price": 24.99,
    "originalPrice": 29.99,
    "currencyCode": "USD"
  },
  
  "images": [
    {"uri": "https://images.goheadcase.com/...", "height": 800, "width": 800}
  ],
  
  "uri": "https://goheadcase.com/products/alabama-crimson-tide-...",
  "availability": "IN_STOCK"
}
```

#### The "Valentine Search" Example — How It Works

User searches: **"valentine case for iPhone 16"**

1. **Query understanding:** Vertex AI Search for Commerce interprets "valentine" as a *thematic concept* → hearts, love, romance, pink, red
2. **Semantic matching:** Finds products where the embedded text has high cosine similarity to the valentine concept:
   - Design keywords containing: "heart", "love", "romantic", "passion", "valentine"
   - Personality tags: "Romantic"
   - Colors: "on Pink", "on Red", "on Rose Gold"
   - Categories: "Patterns" (heart patterns), "Inspiration" (love quotes)
3. **Device filtering:** `device_model = "iPhone 16"` narrows to compatible products
4. **Sales-ranked results:** Among semantic matches, products with higher `sales_rank` appear first
5. **Results returned:** Top 3-4 heart/love-themed iPhone 16 cases, best sellers first

### 5.3 Enriching Search Quality with Design Keywords

The `design_keywords` table is our secret weapon. **38,245 designs** have human-written keyword phrases that capture the *visual and thematic essence* of each design. This is far richer than product titles alone.

But 92,638 designs are active — meaning ~54K designs *lack* keywords. For those, we'll generate semantic descriptions:

#### Strategy for Missing Keywords

| Approach | Coverage | Quality | Cost |
|----------|---------|---------|------|
| Use existing `design_keywords` (38K) | 41% | ⭐⭐⭐⭐⭐ Human-written | Free |
| Generate from design name + lineup + category + personality | 100% | ⭐⭐⭐ Derived | Free |
| Gemini Vision API on design images (batch) | 100% | ⭐⭐⭐⭐⭐ Visual analysis | ~$50 one-time |
| Combine all three | 100% | ⭐⭐⭐⭐⭐ Best possible | ~$50 one-time |

**Recommended:** For designs *with* keywords, use them as the primary semantic text. For designs *without*, use Gemini Vision to generate descriptions from the design images (`tblDesigns.ImageURL`). This is a one-time batch job (~55K images × ~$0.001/image = ~$55).

The generated descriptions would look like:
```
"Colorful watercolor heart pattern on white background. Romantic 
valentine theme with pink, red, and purple hearts in various sizes. 
Soft, feminine, playful aesthetic."
```

This gets embedded alongside the structured attributes to create an incredibly rich semantic index.

### 5.4 Handling 1.89M Products Efficiently

1.89M individual product variants would be wasteful to embed individually — many are the *same design* on different devices/case types. Instead:

#### Smart Indexing Strategy

```
Level 1: DESIGN (92,638 unique designs)
  → Rich semantic embedding (keywords, description, brand, personality)
  → This is what gets semantically searched

Level 2: VARIANT (1.89M product variants)  
  → Metadata (device, case type, color, price, stock, sales_rank)
  → This is what gets filtered and displayed

Search Flow:
  1. Semantic search finds top DESIGNS matching query intent
  2. Filter by device/case-type/availability to get specific VARIANTS
  3. Rank variants by sales_rank within each design
  4. Return top N product cards
```

Vertex AI Search for Commerce supports this via the **primary-variant** product structure:
- **Primary product** = the design (semantic content, shared across variants)
- **Variants** = device + case type combinations (price, stock, URL)

This means we index ~92K semantic documents (manageable, fast) while serving 1.89M purchasable variants. The primary-variant structure also enables **variant rollup** — showing one card per design with a "Available for 47 devices" badge.

---

## 6. Deep Dive: Sales-Ranked Results

### 6.1 The Ranking Formula

Results should be ranked by: **semantic_relevance × sales_popularity**

Vertex AI Search for Commerce provides two mechanisms:

#### Mechanism 1: Boost by Custom Numeric Attribute (`sales_rank`)

We add a `sales_rank` numeric attribute to each product, computed from order data. Then apply a boost:

```json
{
  "boostSpec": {
    "conditionBoostSpecs": [
      {
        "condition": "sales_rank: IN(1e, 100e)",
        "boost": 0.8
      },
      {
        "condition": "sales_rank: IN(100e, 500e)",
        "boost": 0.5
      },
      {
        "condition": "sales_rank: IN(500e, 2000e)",
        "boost": 0.2
      }
    ]
  }
}
```

This means: among semantically relevant results, top-100 sellers get a strong boost, top-500 get a moderate boost, etc.

#### Mechanism 2: User Event-Based Optimization (Auto-Learning)

After launch, we feed real user events (views, clicks, add-to-cart, purchases) back to Vertex AI Search for Commerce. Over time (minimum ~10K events), it automatically learns which products convert better and adjusts ranking accordingly. This is the **KPI optimization** feature — it literally optimizes for revenue per session.

### 6.2 Computing `sales_rank`

We have two sales data sources:

**Source 1: BigCommerce Orders (18,656 orders, current)**
```sql
-- Extract order line items and aggregate by product
-- BigCommerce API: GET /v2/orders/{id}/products for each order
-- Or bulk export via V3 API

-- Result: bc_order_items table
-- product_id, variant_id, sku, quantity, date_ordered
```

**Source 2: cfxb2b_db.sales (25,091 rows, historical)**
```sql
-- Already in BigQuery, but only has BrandID + Quantity
-- Need to join with design/product mappings for design-level sales
```

**Combined Sales Rank Computation:**

```sql
CREATE OR REPLACE TABLE headcase.design_sales_rank AS
WITH bc_sales AS (
  -- BigCommerce order line items (exported via Cloud Function)
  SELECT 
    design_id,
    SUM(quantity) AS bc_units_sold,
    COUNT(DISTINCT order_id) AS bc_order_count,
    MAX(order_date) AS last_sold_date
  FROM headcase.bc_order_items
  WHERE order_status IN ('Shipped', 'Completed', 'Awaiting Fulfillment')
  GROUP BY design_id
),
historical_sales AS (
  -- cfxb2b_db historical sales (weighted lower — older data)
  SELECT
    lb.LineupID,
    SUM(s.Quantity) AS hist_units_sold
  FROM `cfxb2b_db.sales` s
  JOIN `cfxb2b_db.lineups_brand` lb ON s.BrandID = lb.BrandID
  GROUP BY lb.LineupID
),
design_scores AS (
  SELECT
    d.DesignID,
    COALESCE(bc.bc_units_sold, 0) AS recent_sales,
    COALESCE(bc.bc_order_count, 0) AS recent_orders,
    COALESCE(hs.hist_units_sold, 0) AS historical_sales,
    -- Weighted score: recent sales count 3×, historical 1×
    (COALESCE(bc.bc_units_sold, 0) * 3.0 + COALESCE(hs.hist_units_sold, 0) * 1.0) AS raw_score,
    -- Recency bonus: designs sold in last 30 days get 50% boost
    CASE WHEN bc.last_sold_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
         THEN 1.5 ELSE 1.0 END AS recency_multiplier
  FROM `headcase.tblDesigns` d
  LEFT JOIN bc_sales bc ON d.DesignID = bc.design_id
  LEFT JOIN historical_sales hs ON d.LineupID = hs.LineupID
  WHERE d.DesignStatus = 1
)
SELECT
  DesignID,
  recent_sales,
  recent_orders,
  historical_sales,
  CAST(raw_score * recency_multiplier AS INT64) AS score,
  -- Rank 1 = best seller
  ROW_NUMBER() OVER (ORDER BY raw_score * recency_multiplier DESC) AS sales_rank
FROM design_scores;
```

This runs as a **scheduled BigQuery job** (daily), feeding into the Vertex AI Search data store.

### 6.3 Additional Ranking Signals

Beyond sales volume, we can boost by:

| Signal | Source | Boost Strategy |
|--------|--------|---------------|
| **Sales velocity** (trending up) | BC orders, last 7d vs 30d | Boost trending designs +0.3 |
| **Review rating** | BigCommerce product reviews | Boost 4+ stars +0.2 |
| **Margin** | `cfxb2b_db.prices` | Optionally boost higher-margin products |
| **Newness** | `tblLineups.DateAdded` | Boost designs <30 days old +0.2 |
| **Licensed brand** | `cfxb2b_db.brands` | Boost licensed (NFL, HP, etc.) +0.1 |
| **In-stock** | BigCommerce inventory | Bury out-of-stock -0.9 |

---

## 7. Deep Dive: Delivery Estimates

### 7.1 Shipping Rules

| Destination | Carrier | Fulfillment Location | Estimated Delivery |
|------------|---------|---------------------|-------------------|
| **UK** | Royal Mail First Class | UK warehouse OR Philippines | UK: 1-3 business days; Philippines→UK: 7-14 business days |
| **Europe** | Royal Mail International OR Deutsche Post | Philippines | 7-14 business days |
| **US** | USPS Standard | US warehouse OR Philippines | US: 3-7 business days; Philippines→US: 10-21 business days |
| **US (premium)** | FedEx 2-Day | US warehouse | 2 business days |
| **Rest of World** | Royal Mail International | Philippines | 14-28 business days |

### 7.2 Implementation

The agent calculates delivery estimates dynamically:

```python
def estimate_delivery(destination_country: str, product_sku: str) -> dict:
    """
    Returns delivery estimate based on destination and fulfillment location.
    """
    fulfillment = get_fulfillment_location(product_sku)
    
    estimates = {
        ("UK", "UK_WAREHOUSE"): {
            "carrier": "Royal Mail First Class",
            "min_days": 1, "max_days": 3,
            "label": "1-3 business days"
        },
        ("UK", "PHILIPPINES"): {
            "carrier": "Royal Mail First Class", 
            "min_days": 7, "max_days": 14,
            "label": "7-14 business days (made to order)"
        },
        ("US", "US_WAREHOUSE"): {
            "carrier": "USPS Standard",
            "min_days": 3, "max_days": 7,
            "label": "3-7 business days",
            "premium_option": {
                "carrier": "FedEx 2-Day",
                "min_days": 2, "max_days": 2,
                "label": "2 business days",
                "additional_cost": "$X.XX"
            }
        },
        ("US", "PHILIPPINES"): {
            "carrier": "USPS Standard",
            "min_days": 10, "max_days": 21,
            "label": "10-21 business days (made to order)"
        },
        ("EU", "PHILIPPINES"): {
            "carrier": "Royal Mail / Deutsche Post",
            "min_days": 7, "max_days": 14,
            "label": "7-14 business days"
        }
    }
    
    # Determine if product is in local warehouse or made-to-order
    # Most HCD products are print-on-demand from Philippines
    # Some popular SKUs may be pre-stocked in UK/US warehouses
    
    return estimates.get((region, fulfillment), default_estimate)
```

### 7.3 UX Integration

- **On product cards:** Show "📦 Delivers in 3-7 days to US" badge
- **In chat:** "When will I get it?" → agent asks for country if not known, then calculates
- **Proactive:** If user's IP geolocates to UK, pre-set delivery context

---

## 8. Deep Dive: Returns & CS Knowledge

### 8.1 Folding in N8N CS Bot Knowledge

The existing N8N CS bot (GPT-4o-mini) has trained responses for:
- Returns policy (14-day window, conditions, process)
- Shipping FAQs
- Order tracking
- Damaged/defective items

We **don't duplicate** this — we integrate it.

### 8.2 Integration Strategy

```
User message → Intent Classification
  ├── SEARCH intent (80%) → Vertex AI Search → Product results
  ├── SALES intent (10%) → Gemini reasoning → Upsell/cross-sell
  ├── DELIVERY intent (5%) → Delivery estimate logic
  └── CS/SUPPORT intent (5%) → Route to CS knowledge base
```

**For CS intents**, the agent has embedded knowledge:

```python
CS_KNOWLEDGE = {
    "returns_policy": """
        Head Case Designs Returns Policy:
        - 14-day return window from delivery date
        - Items must be unused, in original packaging
        - Customer pays return shipping unless item is defective
        - Refund processed within 5-7 business days of receiving return
        - Custom/personalized items are non-returnable
        - Defective items: free replacement or full refund, no return shipping cost
        
        To initiate a return:
        1. Contact us at support@goheadcase.com with order number
        2. We'll provide a return authorization and address
        3. Ship the item back within 14 days
        4. Refund or exchange processed on receipt
    """,
    "shipping_policy": """...""",
    "order_tracking": """
        To track your order:
        1. Check your email for a shipping confirmation with tracking number
        2. Visit the carrier's website (Royal Mail, USPS, FedEx) with the tracking number
        3. Or reply with your order number and I'll look it up
    """
}
```

For complex support issues (refund processing, order modifications), the agent hands off to the N8N CS bot or creates a support ticket.

---

## 9. Frontend: Search-First Experience

### 9.1 Design Philosophy

This is NOT a chatbot widget in the corner. It's an **enhanced search experience** that replaces/augments BigCommerce's default search.

```
┌─────────────────────────────────────────────────────────────┐
│  goheadcase.com header                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  🔍 Search for cases... "valentine iPhone 16"       [→] │ │
│  │     ┌─────────────────────────────────────────────────┐ │ │
│  │     │ Suggested: ❤️ Valentine's Collection            │ │ │
│  │     │            📱 iPhone 16 Pro Cases               │ │ │
│  │     │            💝 Romantic Designs                  │ │ │
│  │     └─────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Showing results for "valentine case for iPhone 16"      ││
│  │  💬 Need help? Chat with our shopping assistant →        ││
│  │                                                          ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   ││
│  │  │ [Image]  │ │ [Image]  │ │ [Image]  │ │ [Image]  │   ││
│  │  │ Hearts   │ │ Love     │ │ Rose     │ │ Romantic  │   ││
│  │  │ Pattern  │ │ Letters  │ │ Gold     │ │ Floral    │   ││
│  │  │ ⭐ #1   │ │ ⭐ #2   │ │ ⭐ #5   │ │ ⭐ #8    │   ││
│  │  │ $19.99   │ │ $19.99   │ │ $24.99   │ │ $19.99    │   ││
│  │  │📦 3-7d  │ │📦 3-7d  │ │📦 3-7d  │ │📦 7-14d  │   ││
│  │  │[🛒 Add] │ │[🛒 Add] │ │[🛒 Add] │ │[🛒 Add]  │   ││
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   ││
│  │                                                          ││
│  │  Also in Tough Case ($24.99) | Also for iPad ($22.99)   ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  💬 Shopping Assistant (expandable panel)                 ││
│  │  ┌──────────────────────────────────────────────────────┐││
│  │  │ 🤖 I found 47 valentine-themed designs for your     │││
│  │  │    iPhone 16! The Hearts Pattern is our #1 seller   │││
│  │  │    this month. Want me to show you:                  │││
│  │  │    • Matching iPad cases?                            │││
│  │  │    • Tough Case upgrades for more protection?        │││
│  │  │    • Different color options?                         │││
│  │  │                                                      │││
│  │  │ [Type a message...]                          [Send]  │││
│  │  └──────────────────────────────────────────────────────┘││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Two Modes

| Mode | Trigger | Experience |
|------|---------|-----------|
| **Search Mode** | User types in search bar | Instant results grid, semantic autocomplete, faceted filters |
| **Chat Mode** | User clicks "Chat with assistant" or asks a question | Conversational panel, guided discovery, delivery/returns Q&A |

Both modes share the same backend — the difference is frontend presentation.

### 9.3 Technical Implementation

**Widget stack:** React + TailwindCSS, bundled to <80KB gzipped
**Injection:** BigCommerce Script Manager → Footer → All Store Pages
**Search bar:** Intercepts/augments the existing BigCommerce search form
**Results:** Rendered in a custom overlay/panel (not BigCommerce's default results page)

```javascript
// Injected via BigCommerce Script Manager
<script>
(function() {
  const script = document.createElement('script');
  script.src = 'https://storage.googleapis.com/hcd-search-widget/v1/widget.js';
  script.async = true;
  script.onload = function() {
    HCDSearch.init({
      endpoint: 'https://hcd-search-agent-xxxxx.run.app',
      storeHash: 'otle45p56l',
      mode: 'search-first',     // Search bar + expandable chat
      position: 'integrated',    // Augments existing search, not floating widget
      autocomplete: true,
      deliveryEstimates: true,
      salesBadges: true,         // Show "Best Seller", "Trending" badges
      theme: {
        primaryColor: '#1a1a2e',
        accentColor: '#e94560',
        fontFamily: 'inherit'
      }
    });
  };
  document.head.appendChild(script);
})();
</script>
```

---

## 10. Cart Integration

### 10.1 BigCommerce REST Storefront API

Confirmed working — allows add-to-cart from JavaScript on the storefront:

```javascript
// Add to cart — runs in same-origin storefront context
async function addToCart(productId, variantId, quantity = 1) {
  const carts = await fetch('/api/storefront/carts', {
    credentials: 'same-origin'
  }).then(r => r.json());
  
  const endpoint = carts.length > 0 
    ? `/api/storefront/carts/${carts[0].id}/items`
    : '/api/storefront/carts';
  
  const result = await fetch(endpoint, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      lineItems: [{ quantity, productId, variantId }]
    })
  }).then(r => r.json());
  
  // Update cart counter in header
  updateCartBadge(result.lineItems.physicalItems.length);
  
  return result;
}
```

**Key facts:**
- ✅ Same-origin, session-cookie auth (no API key needed on frontend)
- ✅ Works on BigCommerce-hosted Stencil storefronts
- ✅ Returns full cart state after adding
- ✅ Supports product options/variants (needed for device-specific products)
- ✅ Can redirect to checkout: `window.location = '/checkout'`

### 10.2 "Add to Cart" from Chat

When the agent recommends a product and the user says "add it to my cart":

1. Agent returns product_id + variant_id in the response payload
2. Frontend widget calls `addToCart(productId, variantId)`
3. Cart counter updates in the BigCommerce header
4. Agent confirms: "Added! 🛒 Your Hearts Pattern Tough Case for iPhone 16 Pro Max is in the cart. Ready to checkout, or want to keep browsing?"

---

## 11. Data Pipeline Design

### 11.1 Pipeline Overview

```
┌────────────────────────────┐     ┌──────────────────────────────┐
│  Source: headcase DB       │     │  Source: cfxb2b_db           │
│  (MySQL → Datastream)      │     │  (MySQL → Datastream)        │
│                            │     │                              │
│  tblDesigns (92K)          │     │  design_keywords (38K)       │
│  tblLineups (10K)          │     │  design_titles (815K)        │
│  tblTypes (27)             │     │  brands (200+)               │
│  tblPersonalities (8)      │     │  lineups_brand (9.8K)        │
│  tblDesignProductAvail(1.2M│     │  products (72 case types)    │
│  tblLineupTypes (3.3K)     │     │  units (2.3K devices)        │
│  tblLineupPersonalities    │     │  prices (1.2K)               │
│  tblDesignTags             │     │  sales (25K)                 │
│  tblTags                   │     │  colors + color_titles       │
└──────────┬─────────────────┘     └──────────┬───────────────────┘
           │  Real-time sync                   │  Real-time sync
           ↓                                   ↓
┌──────────────────────────────────────────────────────────────────┐
│                    BigQuery                                       │
│                    (instant-contact-479316-i4)                    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  NEW: headcase.bc_order_items                            │    │
│  │  (BigCommerce orders → Cloud Function, daily export)     │    │
│  │  order_id, product_id, variant_id, sku, design_id,      │    │
│  │  quantity, price, order_date, customer_country           │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  NEW: headcase.design_sales_rank                         │    │
│  │  (Scheduled query, daily)                                │    │
│  │  DesignID, recent_sales, historical_sales, sales_rank    │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  NEW: headcase.design_semantic_text                      │    │
│  │  (One-time generation + periodic refresh)                │    │
│  │  DesignID, semantic_description (from keywords +         │    │
│  │  Gemini Vision for designs without keywords)             │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  NEW: headcase.products_for_vertex                       │    │
│  │  (Materialized view, refreshed daily)                    │    │
│  │  DENORMALIZED: all above joined into Vertex AI Search    │    │
│  │  for Commerce import format                              │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────┬───────────────────────────────┘
                                   │  Scheduled import (daily)
                                   ↓
                    ┌──────────────────────────────┐
                    │  Vertex AI Search for Commerce │
                    │  Product Catalog Data Store    │
                    │  ~92K primary products         │
                    │  ~1.89M variants               │
                    │                                │
                    │  + User Events (real-time)     │
                    └──────────────────────────────┘
```

### 11.2 The Denormalized Product View

```sql
CREATE OR REPLACE TABLE headcase.products_for_vertex AS
WITH 
  -- Design semantic text: keywords + generated descriptions
  design_text AS (
    SELECT 
      d.DesignID,
      d.DesignName,
      d.DesignLabel,
      d.ImageURL,
      dt.Title AS design_title,
      dk.Keywords AS design_keywords,
      dst.semantic_description  -- Gemini-generated for designs without keywords
    FROM headcase.tblDesigns d
    LEFT JOIN cfxb2b_db.design_titles dt 
      ON d.DesignID = dt.DesignID AND dt.LanguageID = 1
    LEFT JOIN cfxb2b_db.design_keywords dk 
      ON d.DesignID = dk.DesignID AND dk.LanguageID = 1
    LEFT JOIN headcase.design_semantic_text dst 
      ON d.DesignID = dst.DesignID
    WHERE d.DesignStatus = 1
  ),
  
  -- Brand per lineup
  lineup_brands AS (
    SELECT lb.LineupID, b.Name AS brand_name, b.Label AS brand_label
    FROM cfxb2b_db.lineups_brand lb
    JOIN cfxb2b_db.brands b ON lb.BrandID = b.BrandID
    WHERE b.BrandStatus = 1
  ),
  
  -- Categories per lineup (may have multiple)
  lineup_categories AS (
    SELECT lt.LineupID, STRING_AGG(DISTINCT t.Type) AS categories
    FROM headcase.tblLineupTypes lt
    JOIN headcase.tblTypes t ON lt.TypeID = t.TypeID
    GROUP BY lt.LineupID
  ),
  
  -- Personalities per lineup
  lineup_styles AS (
    SELECT lp.LineupID, STRING_AGG(DISTINCT p.Personality) AS personalities
    FROM headcase.tblLineupPersonalities lp
    JOIN headcase.tblPersonalities p ON lp.PersonalityID = p.PersonalityID
    GROUP BY lp.LineupID
  ),
  
  -- Tags per design
  design_tag_text AS (
    SELECT dt.DesignID, STRING_AGG(DISTINCT t.TagName) AS tags
    FROM headcase.tblDesignTags dt
    JOIN headcase.tblTags t ON dt.TagID = t.TagID
    GROUP BY dt.DesignID
  ),
  
  -- Sales rank
  sales AS (
    SELECT DesignID, sales_rank, recent_sales, score
    FROM headcase.design_sales_rank
  )

SELECT
  CONCAT('HCD-', CAST(dtx.DesignID AS STRING)) AS id,
  
  -- Title: design name + case type + device (for primary, generic)
  CONCAT(COALESCE(dtx.design_title, dtx.DesignName), ' - Head Case Designs') AS title,
  
  -- Rich description for semantic embedding
  CONCAT(
    COALESCE(dtx.design_title, dtx.DesignName), '. ',
    COALESCE(dtx.design_keywords, dtx.semantic_description, ''), '. ',
    'Brand: ', COALESCE(lb.brand_name, 'Head Case Designs'), '. ',
    'Category: ', COALESCE(lc.categories, 'General'), '. ',
    'Style: ', COALESCE(ls.personalities, 'General'), '. ',
    COALESCE(dtt.tags, '')
  ) AS description,
  
  -- Structured attributes
  lb.brand_name AS brand,
  lc.categories,
  ls.personalities,
  dtx.DesignName AS design_name,
  l.Lineup AS lineup_name,
  l.LineupLabel AS lineup_label,
  dtx.ImageURL AS primary_image_url,
  
  -- Sales ranking
  COALESCE(s.sales_rank, 999999) AS sales_rank,
  COALESCE(s.recent_sales, 0) AS total_sold,
  COALESCE(s.score, 0) AS sales_score,
  
  -- Tags for filtering
  dtt.tags

FROM design_text dtx
JOIN headcase.tblLineups l ON dtx.LineupID = l.LineupID
LEFT JOIN lineup_brands lb ON l.LineupID = lb.LineupID
LEFT JOIN lineup_categories lc ON l.LineupID = lc.LineupID
LEFT JOIN lineup_styles ls ON l.LineupID = ls.LineupID
LEFT JOIN design_tag_text dtt ON dtx.DesignID = dtt.DesignID
LEFT JOIN sales s ON dtx.DesignID = s.DesignID;
```

### 11.3 Refresh Schedule

| Pipeline Step | Frequency | Method | Duration |
|--------------|-----------|--------|----------|
| Datastream (headcase + cfxb2b_db) | Real-time | Already active | Continuous |
| BigCommerce order export | Daily | Cloud Function → BigQuery | ~30 min |
| Sales rank computation | Daily | Scheduled BigQuery query | ~2 min |
| Semantic text generation | One-time + monthly | Gemini Vision batch | ~4 hours initial |
| Denormalized view refresh | Daily | BigQuery materialized view | ~5 min |
| Vertex AI Search import | Daily | Scheduled import from BigQuery | ~30-60 min |
| User event ingestion | Real-time | JavaScript pixel → API | Continuous |

---

## 12. Implementation Phases

### Phase 1: Semantic Search Foundation (Weeks 1-4)
**Effort: ~60 hours | Priority: 🔴 Critical**

| Task | Hours | Details |
|------|-------|---------|
| **BigCommerce order export pipeline** | 10 | Cloud Function: paginate orders API, extract line items, map to design IDs, write to BigQuery |
| **Sales rank computation** | 6 | BigQuery scheduled query joining BC orders + historical sales, computing weighted rank |
| **Semantic text generation for designs without keywords** | 10 | Gemini Vision batch job on ~55K design images; store in `design_semantic_text` table |
| **Denormalized product view** | 8 | BigQuery SQL joining all tables into Vertex AI Search import format |
| **Vertex AI Search for Commerce setup** | 12 | Enable API, create catalog, configure primary-variant structure, import from BigQuery, configure boost rules |
| **Boost rules & search quality testing** | 8 | Test "valentine iPhone 16" and 20+ semantic queries; tune boost weights |
| **User event tracking pixel** | 6 | JavaScript snippet for detail-page-view, search, add-to-cart, purchase events |

**Milestone:** Semantic search API working — "valentine case for iPhone 16" returns heart/love-themed cases ranked by sales.

### Phase 2: Intelligent Agent (Weeks 4-6)
**Effort: ~40 hours | Priority: 🔴 Critical**

| Task | Hours | Details |
|------|-------|---------|
| **Cloud Run orchestrator** | 12 | FastAPI service: receives user query, calls Vertex AI Search, enriches with Gemini Flash |
| **Gemini system prompt engineering** | 8 | Sales personality, upsell/cross-sell rules, brand awareness, tone |
| **Delivery estimate module** | 6 | Shipping rules engine (UK/EU/US carriers, Philippines/UK/US fulfillment) |
| **Returns/CS knowledge base** | 4 | Embed GoHeadCase policies, intent routing for CS queries |
| **Session management** | 4 | Firestore for conversation history, device context, shopping intent |
| **Query intent classification** | 6 | Search vs chat vs delivery vs support routing |

**Milestone:** Working API that takes natural language, returns smart product results + conversational responses.

### Phase 3: Frontend Widget (Weeks 6-8)
**Effort: ~45 hours | Priority: 🟡 High**

| Task | Hours | Details |
|------|-------|---------|
| **Search bar component** | 10 | Autocomplete dropdown, semantic suggestions, "Ask assistant" toggle |
| **Results grid** | 10 | Product cards with image, title, price, sales badge, delivery estimate, Add-to-Cart |
| **Chat panel** | 8 | Expandable conversational interface, product card rendering in chat |
| **BigCommerce cart integration** | 6 | Storefront API calls, cart counter update, variant selection |
| **Script Manager deployment** | 3 | Embed code, test on all page types, mobile responsive |
| **Cross-browser/mobile testing** | 4 | iOS Safari, Chrome, Firefox, tablet, mobile |
| **Search bar integration** | 4 | Intercept existing BC search or overlay alongside it |

**Milestone:** Live search + chat widget on goheadcase.com. Customers can search semantically, get sales-ranked results, and add to cart.

### Phase 4: Optimization & Learning (Weeks 8-11)
**Effort: ~35 hours | Priority: 🟢 Medium**

| Task | Hours | Details |
|------|-------|---------|
| **User event volume monitoring** | 4 | Need ~10K events before KPI optimization kicks in |
| **Conversion funnel analytics** | 8 | Search → click → add-to-cart → purchase tracking, attribution |
| **A/B testing** | 8 | Test: semantic search vs default BC search conversion rate |
| **Search quality iteration** | 8 | Review top queries, tune boost weights, add synonym controls |
| **Upsell/cross-sell effectiveness** | 4 | Track which recommendations convert, refine logic |
| **Documentation & runbook** | 3 | Ops procedures, monitoring alerts, data refresh troubleshooting |

**Milestone:** Data-driven proof that semantic search improves conversion. Personalization begins learning.

### Phase 5: Advanced (Weeks 11-14)
**Effort: ~30 hours | Priority: 🔵 Nice-to-have**

| Task | Hours | Details |
|------|-------|---------|
| **Visual search** ("find cases like this image") | 8 | Gemini Vision API: user uploads photo → find similar designs |
| **Proactive engagement** | 6 | Exit-intent popup, cart abandonment nudge, product page assistant |
| **Multi-language search** | 6 | German, French, Spanish (design_titles has multi-language data) |
| **Seasonal campaign support** | 4 | NFL season, holiday themes, Valentine's Day collection boosts |
| **Email capture & abandoned cart** | 6 | Capture leads from chat, trigger abandoned cart emails |

---

### Total Effort Summary

| Phase | Duration | Hours | Cumulative |
|-------|----------|-------|-----------|
| Phase 1: Semantic Search Foundation | Weeks 1-4 | 60h | 60h |
| Phase 2: Intelligent Agent | Weeks 4-6 | 40h | 100h |
| Phase 3: Frontend Widget | Weeks 6-8 | 45h | 145h |
| Phase 4: Optimization | Weeks 8-11 | 35h | 180h |
| Phase 5: Advanced | Weeks 11-14 | 30h | 210h |
| **Total** | **~14 weeks** | **~210h** | |

**MVP (Phases 1-3): 8 weeks, ~145 hours** — Semantic search + sales ranking + chat + cart integration live on site.

---

## 13. Vertex AI Search for Commerce vs Alternatives

### Option A: Vertex AI Search for Commerce + Cloud Run (✅ RECOMMENDED)

**Pros:**
- Commerce-tuned semantic models (trained on Google Shopping data)
- Understands "valentine" → hearts/love/red *in a shopping context*
- Built-in boost/bury by numeric attributes (sales_rank)
- User event learning → KPI-optimized ranking over time
- Primary-variant product structure perfect for our design×device model
- BigQuery native import
- Autocomplete, recommendations, conversational search included
- 4M product limit (our 1.89M fits)
- Merchandising console for non-technical team

**Cons:**
- $4/1K queries (Enterprise) or $1.50/1K (Standard)
- Requires Google Sales onboarding for Commerce tier
- 2-3 week initial setup for full catalog ingestion
- Less control than fully custom system

### Option B: Custom RAG with Vertex AI Vector Search + Gemini

**Pros:**
- Total control over embedding model, ranking algorithm, search behavior
- Can use any embedding model (text-embedding-004, custom fine-tuned)
- Potentially cheaper at scale (no per-query fees beyond compute)
- Can implement exact custom ranking formula

**Cons:**
- **3-5× more engineering effort** (~500+ hours)
- Must build: embedding pipeline for 1.89M products, vector index, ANN search, ranking layer, autocomplete, faceting, filtering — all from scratch
- Must maintain: index freshness, embedding drift, search quality monitoring
- No built-in recommendations, conversational filtering, or KPI optimization
- No merchandising console — everything is code
- Ongoing ops burden for a small team

**Verdict:** Custom RAG only makes sense if Vertex AI Search for Commerce doesn't meet a specific technical requirement (it does) or cost is prohibitive at massive scale (it isn't at our volume).

### Option C: Third-Party Search (Algolia, Typesense, Meilisearch)

**Pros:**
- Fast to set up
- Good keyword + typo-tolerance search
- Some have AI/vector search features

**Cons:**
- Most lack the *commerce-specific* semantic understanding
- Algolia pricing gets expensive at 1.89M records
- No integrated recommendations or conversational commerce
- Would still need separate chat/agent layer
- Doesn't leverage existing GCP infrastructure

### Option D: BigCommerce's Built-in Search (Enhanced)

**Pros:**
- Zero additional cost
- No integration needed

**Cons:**
- **This is what we're replacing.** Keyword-only, no semantic understanding.
- Cannot rank by external sales data
- No conversational capability

---

## 14. Cost Estimates

### Monthly Operating Costs (Post-Launch)

Assumptions:
- 50K monthly search sessions, avg 3 queries each = **150K queries/month**
- Growing to 100K sessions over 6 months

| Component | Quantity | Unit Cost | Monthly |
|-----------|----------|-----------|---------|
| **Vertex AI Search Enterprise** | 150K queries | $4/1K | $600 |
| *— or Standard tier* | *150K queries* | *$1.50/1K* | *$225* |
| **Index storage** | ~10 GB (92K designs) | $5/GB (10 free) | $0 |
| **Cloud Run (orchestrator)** | ~500 vCPU-hours | $0.09/vCPU-hr | $45 |
| **Gemini 2.0 Flash** | 150K calls, ~1K tokens avg | $0.075/1M input | $15 |
| **Firestore (sessions)** | 50K docs | Free tier | $0 |
| **BigQuery** | Existing + minimal adds | On-demand | $20 |
| **Cloud Function (order sync)** | Daily runs | Free tier | $0 |
| **Total (Enterprise)** | | | **~$680/mo** |
| **Total (Standard)** | | | **~$305/mo** |

**Why lower than v1 estimate:** Using primary-variant structure means we index ~92K semantic documents (not 1.89M), dramatically reducing storage and per-query costs. The variant filtering is metadata-level, not separate search queries.

### One-Time Costs

| Item | Cost |
|------|------|
| Gemini Vision batch (55K images) | ~$55 |
| Development (145h MVP at internal rate) | $0 (Cem/Harry time) |
| Domain verification for search | $0 |
| **Total one-time** | **~$55** |

---

## 15. Risks & Mitigations

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|-----------|------------|
| 1 | **Semantic quality not good enough** — "valentine" doesn't find hearts | High | Medium | Design keywords (38K) are rich; supplement with Gemini Vision descriptions; test with 50+ semantic queries before launch |
| 2 | **BigCommerce order→design_id mapping** is non-trivial | Medium | High | BC products may not store design_id — need to reverse-map via SKU patterns or product name parsing. Investigate BC product custom fields. |
| 3 | **Vertex AI Search for Commerce requires Google Sales engagement** | Medium | Medium | Start with generic Vertex AI Search (supports structured data + boost); upgrade to Commerce tier when onboarding approved |
| 4 | **Search widget conflicts with BC theme** | Medium | Medium | Overlay approach (don't modify theme); test with current theme version; use shadow DOM for style isolation |
| 5 | **User event volume too low** initially for personalization | Low | High | Sales-rank boosting works from day 1 (static); KPI optimization kicks in after ~10K events (~1 month) |
| 6 | **Licensed brand IP issues in AI responses** | High | Low | Never generate brand imagery; only surface existing product images; strict system prompt guidelines |
| 7 | **Philippines fulfillment → longer delivery estimates** may hurt conversion | Medium | Medium | Be transparent; frame as "made to order" (premium feel); highlight local warehouse items when available |
| 8 | **Stale search index** — new products not appearing | Medium | Low | Daily refresh pipeline; can add manual trigger for urgent updates |

---

## Appendix A: The "Valentine Search" Test Case

This is the litmus test for whether our search works. Here's the expected flow:

**Query:** "valentine case for iPhone 16"

**Step 1: Query Understanding (Vertex AI Search)**
- Intent: product search
- Theme: valentine → love, hearts, romance, pink, red
- Device: iPhone 16
- Case type: not specified (show all types)

**Step 2: Semantic Retrieval**
Matches designs where the embedded text is semantically close to "valentine/love/hearts":
- Designs with keywords containing: heart, love, romantic, valentine, passion
- Designs with personality: Romantic
- Designs in categories: Patterns (heart patterns), Inspiration (love quotes)
- Designs with colors: Pink, Red, Rose Gold

**Step 3: Sales-Ranked Filtering**
- Filter to: device = iPhone 16 (any variant: Pro, Pro Max, standard, Plus)
- Sort by: semantic relevance × sales_rank boost
- Return top 8 results

**Step 4: Agent Enrichment (Gemini Flash)**
- Groups by case type availability
- Adds upsell note: "Also available in Tough Case for extra protection"
- Adds cross-sell: "Matching iPad cases available"
- Adds delivery estimate based on user's detected country

**Expected Result:**
```
🔍 "valentine case for iPhone 16" — 47 results

1. ❤️ Hearts Pattern Collection - Soft Gel Case ($19.99) ⭐ Best Seller
   📦 Delivers in 3-7 days to US
   [Add to Cart]

2. 💕 Love Letters Design - Tough Case ($24.99) 🔥 Trending
   📦 Delivers in 3-7 days to US  
   [Add to Cart]

3. 🌹 Rose Gold Romantic Floral - Hybrid Case ($22.99)
   📦 Delivers in 7-14 days (made to order)
   [Add to Cart]

4. 💝 Be Mine Valentine - Soft Gel Case ($19.99)
   📦 Delivers in 7-14 days (made to order)
   [Add to Cart]

💡 These designs also come in Tough Case (+$5) for drop protection!
📱 Want to see matching iPad/tablet cases?
```

---

## Appendix B: API Reference

| API | Docs | Purpose |
|-----|------|---------|
| Vertex AI Search for Commerce | [cloud.google.com/retail/docs](https://docs.cloud.google.com/retail/docs) | Product search, recommendations, boost/bury |
| Vertex AI Search (Generic) | [cloud.google.com/generative-ai-app-builder](https://docs.cloud.google.com/generative-ai-app-builder/docs) | Fallback if Commerce tier unavailable |
| BigCommerce Catalog API | [developer.bigcommerce.com/docs/rest-catalog](https://developer.bigcommerce.com/docs/rest-catalog) | Product export |
| BigCommerce Orders API | [developer.bigcommerce.com/docs/rest-management/orders](https://developer.bigcommerce.com/docs/rest-management/orders) | Sales data export |
| BigCommerce Storefront API | [developer.bigcommerce.com/docs/rest-storefront](https://developer.bigcommerce.com/docs/rest-storefront) | Cart management |
| BigCommerce Scripts API | [developer.bigcommerce.com/docs/rest-management/scripts](https://developer.bigcommerce.com/docs/rest-management/scripts) | Widget injection |
| Gemini API (Vertex AI) | [cloud.google.com/vertex-ai/generative-ai](https://cloud.google.com/vertex-ai/generative-ai/docs) | Agent reasoning + Vision for descriptions |
| BigQuery | [cloud.google.com/bigquery/docs](https://cloud.google.com/bigquery/docs) | Data pipeline |

## Appendix C: Quick Start Checklist

- [ ] Enable Vertex AI Search for Commerce API in `opsecellglobal`
- [ ] Contact Google Sales for Commerce tier onboarding (or start with generic Vertex AI Search)
- [ ] Build BigCommerce order export Cloud Function
- [ ] Create `headcase.bc_order_items` table in BigQuery
- [ ] Run sales rank computation
- [ ] Run Gemini Vision batch on designs without keywords
- [ ] Create denormalized `products_for_vertex` table
- [ ] Create Vertex AI Search catalog with primary-variant structure
- [ ] Import products from BigQuery
- [ ] Configure boost rules (sales_rank)
- [ ] Test 50+ semantic queries, validate quality
- [ ] Build Cloud Run agent orchestrator
- [ ] Build search widget
- [ ] Deploy via BigCommerce Script Manager
- [ ] Add user event tracking pixel
- [ ] Monitor, iterate, optimize

---

*This document is a living architecture guide. Version 2 — refined per Cem's priorities: semantic search first, sales-ranked, delivery estimates, returns knowledge.*
