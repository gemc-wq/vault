# Project: Amazon US Shipping Template Optimization

**Project ID:** STO-2026-001  
**Created:** 2026-04-14  
**Owner:** Hermes (Sales Analytics & Revenue Growth)  
**Status:** Analysis Complete, Awaiting Manual Test

---

## 1. Executive Summary

### Objective
Increase Amazon US conversion rates by optimizing shipping templates for FBM (Fulfilled by Merchant) items.

### Key Hypothesis
Items on **Reduced Shipping Template** (2-day FedEx, $10.99) convert higher than items on **Default Amazon Template** (4-6 day, $6.99). Moving eligible items to Reduced Template will increase conversion by ~25%.

### Secondary Objective
Identify candidates for **Seller-Fulfilled Prime trial** - items where customers already pay premium for 2-day shipping, indicating willingness to pay for speed.

### Results
- **Reduced Template conversion:** 3.41%
- **Default Template conversion:** 2.72%
- **Conversion uplift:** +25% on Reduced Template
- **Items needing fix:** 9,778 SKUs (FBM, FL stock, wrong template)
- **Revenue at risk:** ~$200K+ annually

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
| Amazon US Business Report (90 days) | `~/Downloads/Amazon US last 90 days BusinessReport-4-11-26_amended.csv` | Session & conversion data | SKU, ASIN, Sessions, Units, Conversion, Sales, Shipping Template |
| Amazon US Orders (90 days) | `~/Downloads/AmazonUSLast90day_Sales_Combined.txt` | Order-level shipping data | SKU, ship-service-level, item-price, shipping-price |
| Supabase blank_inventory | `supabase.co` via REST API | FL warehouse stock levels | item_code, warehouse, free_stocks |

---

## 4. Filtering Rules (Hard Requirements)

### Rule 1: Exclude FBA Items
- **F-prefix = FBA** (e.g., FHTPCR-IPH17-NARUICO-AKA is FBA version)
- FBA items are fulfilled by Amazon, shipping template is managed by Amazon
- Only FBM (Fulfilled by Merchant) items are in scope

### Rule 2: Must Have FL Stock
- Reduced Shipping Template requires stock in Florida warehouse
- Items without FL stock cannot ship 2-day from FL
- Stock data from Supabase `blank_inventory` table
- Warehouse filter: `warehouse IN ('Florida', 'FL')`

### Rule 3: Must Be Active
- Item must have sessions > 0 (recently viewed)
- Inactive items (0 sessions) excluded

### Rule 4: Currently on Wrong Template
- Currently on `Default Amazon Template` (4-6 day)
- Should be on `Reduced Shipping Template` (2-day)

### Filter Logic Summary
```
Final Dataset = Active items
               AND Non-FBA (no F-prefix)
               AND On Default Amazon Template (wrong)
               AND Has FL stock (from Supabase)
```

---

## 5. Procedure

### Step 1: Load Amazon Business Report
```python
# File: Amazon US last 90 days BusinessReport-4-11-26_amended.csv
# Columns: SKU, (Child) ASIN, Sessions - Total, Units Ordered, 
#          Unit Session Percentage, Ordered Product Sales, Shipping Template
```

### Step 2: Parse SKUs
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

### Step 3: Fetch FL Stock from Supabase
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

### Step 4: Apply Filters
```python
df_filtered = df[
    (df['Sessions'] > 0) &           # Active
    (df['is_fba'] == False) &        # Non-FBA
    (df['Shipping Template'] == 'Default Amazon Template') &  # Wrong template
    (df['base_sku'].isin(fl_stock_skus))  # Has FL stock
]
```

### Step 5: Sort and Export
```python
# Sort by Sales (descending) - highest revenue items first
df_filtered = df_filtered.sort_values('Sales', ascending=False)

# Export to CSV
df_filtered.to_csv('fbm_wrong_template_fl_stock.csv')
```

---

## 6. Results

### Conversion by Shipping Template

| Template | Total Sessions | Total Units | Total Sales | SKUs | Avg Conversion |
|----------|---------------|-------------|-------------|------|----------------|
| Reduced Shipping Template | 388,368 | 13,246 | $286,450 | 38,220 | **3.41%** |
| Default Amazon Template | 380,203 | 10,328 | $238,788 | 39,869 | **2.72%** |
| Nationwide Prime | 12,342 | 197 | $4,281 | 95 | 1.60% |

**Key Finding:** Reduced Template drives **25% higher conversion** than Default Template.

### Filtered Output

| Metric | Value |
|--------|-------|
| Items on wrong template (before FL filter) | 37,750 |
| Items with FL stock | 760 base SKUs |
| **Final items needing fix** | **9,778** |
| iPhone 17 family items | 39 |

### Prime Trial Candidates

| Metric | Value |
|--------|-------|
| SecondDay orders (90 days) | 3,541 |
| Shipping revenue | $42,290 |
| Top device | iPhone 17 Pro Max (299 orders) |
| Top designs | Naruto Akatsuki, Dragon Ball Goku, Peanuts |

---

## 7. Deliverables

| File | Items | Location |
|------|-------|----------|
| All FBM Wrong Template (FL Stock) | 9,778 | `~/Vault/03-Agents/Hermes/fbm_wrong_template_fl_stock.csv` |
| iPhone 17 Wrong Template (FL Stock) | 39 | `~/Vault/03-Agents/Hermes/iphone17_wrong_template_fl_stock.csv` |
| Prime Trial Dashboard | - | `~/Vault/03-Agents/Hermes/amazon-prime-trial-dashboard.html` |
| This Project Document | - | `~/Vault/03-Agents/Hermes/PROJECT_SHIPPING_TEMPLATE_OPTIMIZATION.md` |

---

## 8. Next Steps

### Immediate: Manual Test
1. Pick a test SKU from filtered list (e.g., HSTWH-L-WWE2JCEN-ICO)
2. Manually change shipping template in Seller Central to `Reduced Shipping Template`
3. Note the exact template name as it appears in Seller Central
4. Wait for propagation (15-30 minutes)
5. Verify via middleware API that template name matches

### Short-term: API Script Development
1. Research Amazon SP-API feed format for shipping template updates
2. Build script to bulk-update SKUs to correct template
3. Test on small batch (10-50 SKUs)
4. Roll out to full 9,778 items

### Medium-term: Prime Trial
1. Select iPhone 17 + Peanuts/Naruto SKUs for Prime trial
2. Set up before/after tracking dashboard
3. Convert to Seller-Fulfilled Prime
4. Monitor conversion, sessions, revenue for 7-14 days
5. Evaluate ROI and expand or rollback

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
- Exceptions: `FLAG` (flags), `FRND` (Friends), `FKFLOR` - NOT FBA

### Warehouse Codes
- Supabase uses: `Florida` and `FL`
- Both represent same warehouse
- Query uses: `warehouse IN ('Florida', 'FL')`

### Data Currency
- Business Report: Last 90 days (Jan-Apr 2026)
- Orders Report: Last 90 days
- Inventory: Real-time from Supabase

---

## 10. Appendices

### Appendix A: Top 20 Items Needing Fix

| SKU | ASIN | Product | Sessions | Units | Conversion | Sales |
|-----|------|---------|----------|-------|------------|-------|
| HSTWH-L-WWE2JCEN-ICO | B0F213JBXT | WWE Wristband | 730 | 42 | 5.75% | $630.59 |
| HLBWH-IPAD102-DRGBSUSC-LGOK | B0BC1CV358 | iPad 10.2 Wallet | 215 | 9 | 4.19% | $264.60 |
| HLBWH-IPH17-HPOTPRI2-LMAR | B0FQNMFQNN | iPhone 17 Wallet | 175 | 9 | 5.14% | $224.55 |
| ... | ... | ... | ... | ... | ... | ... |

### Appendix B: API Endpoints Used

```yaml
Supabase REST API:
  URL: https://auzjmawughepxbtpwuhe.supabase.co
  Table: blank_inventory
  Auth: Service role key (bypasses RLS)
  Query: ?select=item_code,warehouse,free_stocks&warehouse=in.(Florida,FL)&free_stocks=gt.0
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-14  
**Next Review:** After manual test completion
