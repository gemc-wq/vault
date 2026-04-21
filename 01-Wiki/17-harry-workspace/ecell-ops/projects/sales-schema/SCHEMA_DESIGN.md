# Design Document: Head Case Designs Unified Sales Schema

## 1. Overview
This schema is designed to unify sales data from multiple marketplaces (Amazon, eBay, Etsy, BigCommerce, etc.) into a single, high-performance Supabase (PostgreSQL) database. It accounts for a print-on-demand model where physical inventory (blanks) is separate from digital assets (designs).

## 2. Key Architecture Decisions

### 2.1 Multi-Marketplace & Regional Handling
- **`marketplaces` Table**: Stores metadata for each channel (Amazon US, eBay UK, etc.) and maps them to a `region` (US, UK, EU, JP, AU).
- **`currencies` & `exchange_rates`**: Financial data is stored in both its original currency and a normalized `base_currency` (USD). A daily exchange rate table ensures accurate historical reporting.

### 2.2 SKU Decomposition (The Core Logic)
The SKU structure `[ProductType]-[DeviceModel]-[DesignCode]-[DesignVariant]` is decomposed:
- `product_types`: (e.g., Phone Case, Desk Mat)
- `devices`: (e.g., iPhone 16, Echo Dot 3)
- `designs`: (e.g., HP Marauder's Map, LFC Home Kit)
- **`inventory_items`**: This represents the "Blank Product" (ProductType + DeviceModel). Since the company is print-on-demand, the physical stock tracked is the unprinted case or mat.

### 2.3 Financial Integrity
- Prices and amounts are stored using `numeric(12, 4)` to avoid floating-point errors.
- `order_line_items` stores the price at the time of sale, including discounts and tax, extracted from marketplace-specific API structures.

### 2.4 Inventory Management (Event-Based)
- **`stock_movements`**: Instead of a simple "quantity" column, every change in stock is recorded as a movement (SALE, RESTOCK, RMA, ADJUSTMENT). Current stock is derived from these events.
- **`purchase_orders`**: Full lifecycle tracking from `DRAFT` to `RECEIVED`.

## 3. Vertex AI / RAG Integration
- Tables include a `search_vector` column (tsvector) for full-text search.
- A `metadata` (jsonb) column is provided on orders and items for future extensibility and to feed unstructured context into Vertex AI.

## 4. Sales Velocity & Reordering
- Sales velocity is not stored; it is calculated via the `top_sellers_by_region` materialized view and helper functions.
- `reorder_rules` allow for dynamic thresholds per `product_group` or `warehouse`.

---

## 5. ER Diagram Summary (Relationships)
- `marketplaces` 1:N `orders`
- `orders` 1:N `order_line_items`
- `inventory_items` 1:N `order_line_items` (linking SKU segments)
- `inventory_items` 1:N `stock_movements`
- `warehouses` 1:N `stock_movements`
- `suppliers` 1:N `purchase_orders`
- `purchase_orders` 1:N `po_line_items`
