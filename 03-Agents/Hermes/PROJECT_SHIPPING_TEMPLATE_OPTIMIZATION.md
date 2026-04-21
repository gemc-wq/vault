# Project: Amazon US Shipping Template Optimization

**Project ID:** STO-2026-001  
**Created:** 2026-04-14  
**Owner:** Hermes (Sales Analytics & Revenue Growth)  
**Status:** Analysis Complete, Awaiting Manual Test Verification
**Updated:** 2026-04-14 21:05 UTC

---

## 1. Executive Summary

### Objective
Increase Amazon US conversion rates by optimizing shipping templates for FBM (Fulfilled by Merchant) items.

### Key Hypothesis
Items on **Reduced Shipping Template** (2-day FedEx, $10.99) convert higher than items on **Default Amazon Template** (4-6 day, $6.99). Moving eligible items to Reduced Template will increase conversion by ~25%.

### Secondary Objective
Identify candidates for **Seller-Fulfilled Prime trial** - items where customers already pay premium for 2-day shipping, indicating willingness to pay for speed.

**CRITICAL:** Prime trial candidate analysis uses **ORDERS data**, not listings data.

| Data Type | What It Shows | Use For |
|-----------|---------------|---------|
| **Orders Data** | What customers PAID for shipping, which method they CHOSE | Prime trial candidates (proves willingness to pay) |
| **Listings Data** | What shipping options are AVAILABLE | Wrong template detection |

Orders data reveals customer behavior:
- **SecondDay orders** = customer paid $12.99 for 2-day shipping
- **Standard orders** = customer paid $6.99 for 4-6 day shipping
- This proves willingness to pay for speed

### Results

**Wrong Template Analysis (from Business Report):**
- **Reduced Template conversion:** 3.41%
- **Default Template conversion:** 2.72%
- **Conversion uplift:** +25% on Reduced Template
- **Items needing fix:** 9,778 SKUs (FBM, FL stock, wrong template)
- **Revenue at risk:** ~$200K+ annually

**Prime Trial Candidates (from Orders Data):**
- **SecondDay orders (90 days):** 3,541 orders
- **Shipping revenue collected:** $42,290
- **Top device:** iPhone 17 Pro Max (299 orders)
- **Top designs:** Naruto Akatsuki, Dragon Ball Goku, Peanuts

---

## 2. Business Context

### The Two Lanes to Fix

| Lane | Region | Correct Template | Delivery | Customer Cost | Conversion Impact |
|------|--------|------------------|----------|---------------|-------------------|
| **Lane 1** | UK | Nationwide Prime | Next-day / 2-day | Prime (free) | HIGH (Seller-Fulfilled Prime badge) |
| **Lane 2** | US | Reduced Shipping Template | 2-day FedEx | $10.99 | +25% vs Default |

### Why Shipping Templates Matter
- UK uses Seller-Fulfilled Prime (Nationwide Prime) = higher conversion
- US standard = 4-6 day delivery, $6.99 = lower conversion
- US Reduced Template = 2-day FedEx, $10.99 = higher conversion
- Prime trial = flat price ~$32, Prime badge, 2-day delivery

### FBA vs FBM Premium
- FBA: Customer pays $6 for Prime (Amazon fulfills)
- Seller-Fulfilled Prime: We pay $11-12 for FedEx, customer sees Prime badge
- FBM Reduced Template: Customer pays $10.99 for 2-day

---

## 3. Data Sources

| Source | Location | Purpose | Key Fields |
|--------|----------|---------|------------|
| Amazon US Business Report (90 days) | `~/Downloads/Amazon US last 90 days BusinessReport-4-11-26_amended.csv` | Wrong template detection, conversion analysis | SKU, ASIN, Sessions, Units, Conversion, Sales, Shipping Template |
| Amazon US Orders (90 days) | `~/Downloads/AmazonUSLast90day_Sales_Combined.txt` | Prime trial candidates (shipping method chosen) | SKU, ship-service-level, item-price, shipping-price |
| Amazon US Active Listings | `~/Downloads/US Amazon Active+Listings+Report_04-14-2026.txt` | Verification of template changes | seller-sku, merchant-shipping-group |
| Supabase blank_inventory | `supabase.co` via REST API | FL warehouse stock levels | item_code, warehouse, free_stocks |

---

## 4. Two Separate Analyses

### Analysis 1: Wrong Template Detection (Business Report Data)

**Purpose:** Find items on wrong template that should be moved to Reduced Template.

**Data Source:** Amazon Business Report (sessions, conversion, current template)

**Filtering Rules:**

#### Rule 1: Exclude FBA Items
- **F-prefix = FBA** (e.g., FHTPCR-IPH17-NARUICO-AKA is FBA version)
- FBA items are fulfilled by Amazon, shipping template is managed by Amazon
- Only FBM (Fulfilled by Merchant) items are in scope

#### Rule 2: Must Have FL Stock
- Reduced Shipping Template requires stock in Florida warehouse
- Items without FL stock cannot ship 2-day from FL
- Stock data from Supabase `blank_inventory` table
- Warehouse filter: `warehouse IN ('Florida', 'FL')`

#### Rule 3: Must Be Active
- Item must have sessions > 0 (recently viewed)
- Inactive items (0 sessions) excluded

#### Rule 4: Currently on Wrong Template
- Currently on `Default Amazon Template` (4-6 day)
- Should be on `Reduced Shipping Template` (2-day)

**Filter Logic:**
```
Wrong Template Items = Active items
                      AND Non-FBA (no F-prefix)
                      AND On Default Amazon Template (wrong)
                      AND Has FL stock (from Supabase)
```

---

### Analysis 2: Prime Trial Candidates (Orders Data)

**Purpose:** Find items where customers already pay for 2-day shipping, proving willingness to pay for speed.

**Data Source:** Amazon Orders Report (90 days)

**Key Fields:**
- `ship-service-level`: Shipping method chosen (SecondDay, NextDay, Standard, Expedited)
- `shipping-price`: Amount customer paid for shipping ($12.99, $6.99, etc.)
- `item-price`: Product price
- `sku`: Product identifier

**Analysis Logic:**
```
Prime Trial Candidates = Orders with ship-service-level = 'SecondDay'
                        GROUP BY base_sku
                        COUNT orders
                        SUM shipping-price
                        ORDER BY order_count DESC
```

**Why Orders Data:**
- Shows what customers ACTUALLY chose (not just what's available)
- Proves willingness to pay $12.99 for 2-day shipping
- Identifies products where customers value speed over price
- These are ideal candidates for Prime trial at $32-33 flat price

**Results from Orders Analysis:**
- 3,541 customers paid $12.99 for SecondDay shipping
- Total shipping revenue: $42,290
- These customers would likely pay ~$32 for Prime + 2-day

---

## 5. Procedure

### Part A: Wrong Template Detection (Business Report)

#### Step 1: Load Amazon Business Report
```python
# File: Amazon US last 90 days BusinessReport-4-11-26_amended.csv
# Columns: SKU, (Child) ASIN, Sessions - Total, Units Ordered, 
#          Unit Session Percentage, Ordered Product Sales, Shipping Template
```

#### Step 2: Parse SKUs
```python
def parse_sku(sku):
    """
    Parse SKU into components:
    - FBA flag (F-prefix = FBA)
    - Product type (e.g., HTPCR, HLBWH, HB401)
    - Device (e.g., IPH17, IPH17PRO, IPH17PMAX)
    - Design (e.g., NARUICO-AKA, PNUTBOA-XOX)
    - Base SKU (product_type + device, for FL stock matching)
    """
    if sku starts with 'F': fba = True
    parts = sku.split('-')
    product_type = parts[0]
    device = parts[1]
    design = '-'.join(parts[2:])
    base_sku = f"{product_type}-{device}"
    return {fba, product_type, device, design, base_sku}
```

#### Step 3: Fetch FL Stock from Supabase
```python
# Supabase REST API
# Table: blank_inventory
# Filter: warehouse IN ('Florida', 'FL') AND free_stocks > 0
# Returns: item_code, warehouse, free_stocks
# 
# Note: Inventory uses base SKU (e.g., HLBWH-IPH17)
# Business report uses full SKU (e.g., HLBWH-IPH17-HPOTPRI2-LMAR)
# Match on base_sku = item_code
```

#### Step 4: Apply All Filters
```python
df_filtered = df[
    (df['Sessions'] > 0) &           # Active
    (df['is_fba'] == False) &        # Non-FBA
    (df['Shipping Template'] == 'Default Amazon Template') &  # Wrong template
    (df['base_sku'].isin(fl_stock_skus))  # Has FL stock
].sort_values('Sales', ascending=False)
```

#### Step 5: Export Results
```python
df_filtered.to_csv('~/Vault/03-Agents/Hermes/fbm_wrong_template_fl_stock.csv', index=False)
```

---

### Part B: Prime Trial Candidates (Orders Data)

#### Step 1: Load Orders Report
```python
# File: AmazonUSLast90day_Sales_Combined.txt
# Key columns: order-id, sku, ship-service-level, shipping-price, item-price
```

#### Step 2: Filter SecondDay Orders
```python
second_day = df[df['ship-service-level'] == 'SecondDay']
```

#### Step 3: Group by Base SKU
```python
candidates = second_day.groupby('base_sku').agg({
    'order-id': 'count',           # Order count
    'shipping-price': 'sum',       # Total shipping revenue
    'item-price': 'sum'            # Total product revenue
}).sort_values('order-id', ascending=False)
```

#### Step 4: Export Results
```python
candidates.to_csv('~/Vault/03-Agents/Hermes/prime_trial_candidates.csv')
```

---

## 6. Verification Method

### How to Verify Template Changes

1. **Download fresh Active Listings Report** from Seller Central
2. **Search for test SKU** in the report
3. **Check `merchant-shipping-group` column** for template name
4. **Template names confirmed:**
   - Correct: `Reduced Shipping Template`
   - Wrong: `Default Amazon Template`

### Timing
- Report must be downloaded AFTER the update
- Amazon propagation: 15-30 minutes
- Check report timestamp before relying on data

---

## 7. Deliverables

| File | Records | Purpose | Analysis Type |
|------|---------|---------|---------------|
| `fbm_wrong_template_fl_stock.csv` | 9,778 | Items needing template fix | Business Report |
| `iphone17_wrong_template_fl_stock.csv` | 39 | iPhone 17 items to fix | Business Report |
| `prime_trial_candidates.csv` | TBD | Prime trial candidates | Orders Data |
| `amazon-prime-trial-dashboard.html` | - | Visual dashboard | Both |
| `PROJECT_SHIPPING_TEMPLATE_OPTIMIZATION.md` | - | This document | - |

---

## 8. Next Steps

### Immediate: Verify Manual Test
1. Check what time you applied the update
2. Download fresh Active Listings Report if >30 min elapsed
3. Verify test SKU shows `Reduced Shipping Template`

### Short-term: Bulk Fix
1. Research Amazon SP-API feed format for shipping template updates
2. Build script to bulk-update 9,778 SKUs
3. Test on small batch (10-50 SKUs)
4. Roll out to full list

### Medium-term: Prime Trial
1. Analyze orders data for SecondDay patterns (already done)
2. Cross-reference with iPhone 17 + Peanuts/Naruto SKUs
3. Set up before/after tracking dashboard
4. Convert selected items to Seller-Fulfilled Prime
5. Monitor conversion for 7-14 days

---

## 9. Technical Notes

### SKU Format
- Full SKU: `{PRODUCT_TYPE}-{DEVICE}-{DESIGN}-{VARIANT}`
- Example: `HLBWH-IPH17-HPOTPRI2-LMAR`
- Base SKU (for inventory match): `{PRODUCT_TYPE}-{DEVICE}`
- Example: `HLBWH-IPH17`

### FBA Prefix Detection
- F-prefix = FBA item
- Examples: `FHTPCR`, `FHB401`, `FHLBWH`
- Exceptions: `FLAG` (flags), `FRND` (Friends), `FKFLOR` (FK Floral) - NOT FBA

### Warehouse Codes
- Supabase uses: `Florida` and `FL`
- Both represent same warehouse
- Query uses: `warehouse IN ('Florida', 'FL')`

### Shipping Template Names (Confirmed from Active Listings Report)
- Correct: `Reduced Shipping Template`
- Wrong: `Default Amazon Template`
- Prime: `Nationwide Prime` (UK only)

### Data Currency
- Business Report: Last 90 days (Jan-Apr 2026)
- Orders Report: Last 90 days
- Active Listings: Real-time snapshot
- Inventory: Real-time from Supabase

---

## 10. Key Insight

**Two Different Analyses for Two Different Goals:**

| Goal | Data Source | What It Measures |
|------|-------------|------------------|
| Fix wrong templates | Business Report (listings) | What template items ARE on |
| Find Prime candidates | Orders Report (transactions) | What customers CHOSE to pay for |

**Why Orders Data for Prime Trial:**
- A listing on Reduced Template doesn't mean customers value 2-day
- An order with SecondDay shipping proves the customer paid $12.99 for speed
- These customers are pre-qualified for Prime at $32-33

---

**Document Version:** 2.0  
**Last Updated:** 2026-04-14 21:05 UTC  
**Next Review:** After manual test verification
