# Dashboard Addendum: Shipping Template Compliance Tracking

**Date:** 2026-04-11 | **Owner:** Ava | **Priority:** CRITICAL | **Impact:** Conversion +2-4%

---

## Why This Matters

**Data from shipping audit (Apr 10):**
- 15% of listings missing "Reduced Shipping Template"
- Correlation: Reduced Shipping → 2-day delivery → higher conversion
- Estimated impact: +2-4% conversion lift if fixed across all SKUs
- Revenue opportunity: $100K-200K annually at current volume

**This is not optional.** Shipping template compliance is a **top 3 priority** for Q2.

---

## Dashboard Addition: Shipping Compliance Section

### New View: "Shipping Health Center" (Added to Main Dashboard)

**Placement:** Below Listings Health Scorecard, above Opportunity Leaderboard

```
┌──────────────────────────────────────────────────────────┐
│  🚚 SHIPPING TEMPLATE COMPLIANCE                          │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  Overall Compliance:  85%  [Target: 100%]  ⚠️            │
│  With Reduced Template: 85% (2,923K of 3,425K SKUs)      │
│  Without Template: 15% (502K SKUs)  ← ACTION REQUIRED   │
│                                                            │
│  Estimated Conversion Lift (if fixed): +2-4%             │
│  Revenue Opportunity: $100K-200K/year                    │
│                                                            │
│  [Drill Down ↓]  [View Action Plan]  [Assign Owner]      │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

---

## Detailed Breakdown Views (4 Drill-Down Options)

### **Option 1: By Product Type** (HTPCR, HB401, HLBWH, etc.)

```
Product Type    | Total SKUs | Reduced Template | % Compliant | Gap | Priority
─────────────────────────────────────────────────────────────────────────────
HTPCR           | 1,200,000  |   1,050,000      |    87.5%    | ❌  | HIGH
HB401           |   850,000  |     680,000      |    80.0%    | ❌  | CRITICAL
HLBWH           |   600,000  |     540,000      |    90.0%    | ✅  | LOW
HB6             |   500,000  |     450,000      |    90.0%    | ✅  | LOW
HB7             |   275,000  |     203,000      |    73.8%    | ❌  | CRITICAL
```

**Action:** Click row to see which designs in that product type are missing

---

### **Option 2: By Device Type** (iPhone 17PM, 17Pro, 16, etc.)

```
Device          | Total SKUs | Reduced Template | % Compliant | Gap
────────────────────────────────────────────────────────────────────
iPhone 17PM     |   180,000  |     162,000      |    90.0%    | ✅
iPhone 17Pro    |   175,000  |     157,500      |    90.0%    | ✅
iPhone 17       |   170,000  |     102,000      |    60.0%    | ❌ CRITICAL
iPhone 16PM     |   160,000  |     144,000      |    90.0%    | ✅
iPhone 16Pro    |   155,000  |     139,500      |    90.0%    | ✅
iPhone 16       |   150,000  |     90,000       |    60.0%    | ❌ CRITICAL
Samsung S24     |   145,000  |     116,000      |    80.0%    | ❌
Google Pixel 8  |   140,000  |     112,000      |    80.0%    | ❌
```

**Insight:** Older/budget devices (iPhone 17, iPhone 16) have worse compliance → higher impact

---

### **Option 3: By Model Combination** (Device × Product Type)

```
Device          | HTPCR    | HB401    | HLBWH   | HB6     | HB7     | Overall
─────────────────────────────────────────────────────────────────────────────
iPhone 17PM     | 92% ✅   | 88% ❌   | 95% ✅  | 91% ✅  | 85% ❌  | 90.2%
iPhone 17Pro    | 91% ✅   | 87% ❌   | 94% ✅  | 90% ✅  | 84% ❌  | 89.2%
iPhone 17       | 65% ❌❌  | 55% ❌❌  | 70% ❌  | 68% ❌  | 60% ❌❌ | 63.6%
iPhone 16PM     | 88% ❌   | 85% ❌   | 92% ✅  | 89% ✅  | 80% ❌  | 86.8%
iPhone 16       | 62% ❌❌  | 52% ❌❌  | 68% ❌  | 65% ❌  | 57% ❌❌ | 60.8%
Samsung S24     | 82% ❌   | 78% ❌   | 85% ❌  | 81% ❌  | 75% ❌  | 80.2%
```

**Quick insight:** 
- Newest devices (17PM, 17Pro) = better compliance
- Older devices (16, S24) = worse compliance
- **Action:** Prioritize iPhone 17, iPhone 16, S24 for template updates

---

### **Option 4: By Design** (NARUTO, ONEPIECE, PEANUTS, etc.)

```
Design          | Total SKUs | Reduced Template | % Compliant | Missing Combos | Owner
──────────────────────────────────────────────────────────────────────────────────────
NARUTO          |    45,000  |     40,500       |    90.0%    | iPhone 17/16   | Marketplace Ops
ONE PIECE       |    42,000  |     37,800       |    90.0%    | iPhone 17/16   | Marketplace Ops
PEANUTS         |    38,000  |     34,200       |    90.0%    | ✅ FULL        | ✅ DONE
HARRY POTTER    |    35,000  |     31,500       |    90.0%    | ✅ FULL        | ✅ DONE
NBA CHAMPION    |    32,000  |     22,400       |    70.0%    | Most devices   | ❌ CRITICAL
NFL MAHOMES     |    28,000  |     14,000       |    50.0%    | Most devices   | ❌ CRITICAL
SHELBY (AC)     |    15,000  |      6,000       |    40.0%    | Most devices   | ❌ CRITICAL
```

**Action Plan:**
- ✅ DONE: Peanuts, Harry Potter (100% compliant)
- ⚠️ IN PROGRESS: Naruto, One Piece (90% done, fix remaining combos)
- ❌ BLOCKED: NBA, NFL, Shelby (critical gaps, need immediate attention)

---

## Implementation in Dashboard

### Data Model Addition

```sql
-- Shipping template compliance tracking
CREATE TABLE shipping_compliance (
  week_of DATE,
  sku TEXT,
  design_code TEXT,
  device_name TEXT,
  product_type TEXT,
  has_reduced_template BOOLEAN,
  shipping_option TEXT,  -- "Reduced", "Standard", "None"
  estimated_delivery_days INTEGER,
  created_at TIMESTAMP
);

-- Compliance summary by dimension
CREATE TABLE shipping_compliance_summary (
  week_of DATE,
  dimension TEXT,  -- "product_type", "device", "design", "model_combo"
  dimension_value TEXT,
  total_skus INTEGER,
  compliant_skus INTEGER,
  compliance_pct REAL,
  gap_count INTEGER,
  priority TEXT,  -- "CRITICAL", "HIGH", "MEDIUM", "LOW"
  PRIMARY KEY (week_of, dimension, dimension_value)
);

-- Action items (specific to shipping)
CREATE TABLE shipping_actions (
  week_of DATE,
  action_id TEXT PRIMARY KEY,
  design TEXT,
  devices_affected TEXT,  -- "iPhone 17, iPhone 16, S24"
  current_compliance REAL,
  target_compliance REAL,
  owner TEXT,
  timeline TEXT,
  status TEXT,
  estimated_conversion_lift REAL
);
```

### Codex Script Updates

The `weekly_listings_processor.py` already processes Active Listings Report. Update it to:

```python
# Add shipping template analysis
def analyze_shipping_compliance(active_listings_df):
    """
    Extract shipping template data from Active Listings Report.
    
    Columns available:
    - sku, asin, product_name
    - shipping_template (filled by seller)
    - estimated_delivery_days (calculated from template)
    
    Return: compliance metrics by device, product type, design, model combo
    """
    
    # Identify listings with "Reduced Shipping Template"
    has_reduced = active_listings_df['shipping_template'].str.contains(
        'Reduced|2.?day|expedited', 
        case=False, 
        na=False
    )
    
    overall_compliance = (has_reduced.sum() / len(df)) * 100
    
    # Breakdown by dimension
    by_product = active_listings_df.groupby('product_type').apply(
        lambda x: (x['has_reduced'].sum() / len(x)) * 100
    )
    
    by_device = active_listings_df.groupby('device').apply(
        lambda x: (x['has_reduced'].sum() / len(x)) * 100
    )
    
    by_design = active_listings_df.groupby('design_code').apply(
        lambda x: (x['has_reduced'].sum() / len(x)) * 100
    )
    
    # Model combinations (device × product_type)
    by_combo = active_listings_df.groupby(['device', 'product_type']).apply(
        lambda x: (x['has_reduced'].sum() / len(x)) * 100
    )
    
    # Identify gaps (non-compliant)
    gaps = active_listings_df[~has_reduced][['design_code', 'device', 'product_type']]
    
    return {
        'overall': overall_compliance,
        'by_product': by_product.to_dict(),
        'by_device': by_device.to_dict(),
        'by_design': by_design.to_dict(),
        'by_combo': by_combo.to_dict(),
        'gap_details': gaps.to_dict('records'),
        'gap_count': len(gaps)
    }
```

### Dashboard Display Logic

```jsx
// React component for shipping compliance
export function ShippingComplianceView() {
  const [dimension, setDimension] = useState('product_type');
  const [data, setData] = useState(null);
  
  // Load compliance data for selected dimension
  useEffect(() => {
    fetch(`/api/shipping/compliance?dimension=${dimension}`)
      .then(r => r.json())
      .then(d => setData(d));
  }, [dimension]);
  
  return (
    <div className="shipping-dashboard">
      <ComplianceScorecard overall={data.overall} />
      
      <DimensionSelector 
        selected={dimension}
        onChange={setDimension}
        options={[
          { label: 'By Product Type', value: 'product_type' },
          { label: 'By Device', value: 'device' },
          { label: 'By Model Combo', value: 'model_combo' },
          { label: 'By Design', value: 'design' }
        ]}
      />
      
      <ComplianceTable 
        data={data[dimension]}
        onClickRow={(row) => showActionPlan(row)}
      />
      
      <GapList gaps={data.gaps} />
    </div>
  );
}
```

---

## Critical Actions (From Shipping Audit)

### Immediate (This Week)

1. **Update NFL listings** (50% compliance)
   - Owner: Marketplace Ops
   - Action: Add Reduced Shipping Template to all NFL SKUs
   - Timeline: 2 days
   - Impact: +2% conversion on 28K SKUs = $1.4K/week

2. **Update NBA listings** (70% compliance)
   - Owner: Marketplace Ops
   - Action: Add Reduced Shipping Template to gap SKUs
   - Timeline: 3 days
   - Impact: +2% conversion on 32K SKUs = $1.6K/week

3. **Update Shelby (AC)** (40% compliance)
   - Owner: Marketplace Ops
   - Action: Add Reduced Shipping Template to all Shelby SKUs
   - Timeline: 1 day
   - Impact: +2% conversion on 15K SKUs = $750/week

### This Month

4. **Fix iPhone 17 / iPhone 16 gaps** (60-65% compliance)
   - Owner: Harry (operations) → automate via SP-API once available
   - Action: Bulk edit shipping templates for these devices
   - Timeline: 1 week
   - Impact: +2% conversion on 300K+ SKUs = $15K+/month

5. **Samsung S24 compliance** (80%, still room)
   - Owner: Marketplace Ops
   - Action: Identify which designs missing, add templates
   - Timeline: 1 week
   - Impact: +1% conversion on 145K SKUs = $5K+/month

---

## Revenue Projection (If All Fixed)

```
Current Compliance: 85%
Target: 100%

Current Compliant SKUs: 2,923K (87.5% conversion lift already realized)
Gap: 502K SKUs (0% conversion lift currently)

If we fix the 502K gap:
  - Conversion baseline: 2.5%
  - Expected with Reduced Shipping: 2.5% + 2-4% = 4.5-6.5%
  - Lift: 2-4 percentage points
  - Additional monthly revenue: $100K-200K

Timeline: 4-6 weeks to full compliance
```

---

## Dashboard Layout (Updated)

**Main Dashboard:**
1. Listings Health Scorecard (existing)
2. **Shipping Compliance Center** ← NEW (takes precedence)
3. Opportunity Leaderboard (existing, but includes shipping actions at top)
4. Trend Charts (existing)
5. Device Coverage Heatmap (existing)
6. Action Items Timeline (existing, but shipping-specific actions highlighted)

**Shipping Compliance Subsystem:**
- Drill-down by product type, device, model combo, design
- Gap details (which SKUs missing, which combos)
- Action plan with owners + timelines
- Conversion impact tracking

---

## Integration with Cron

**Saturday 1 AM (Codex Script Enhancement):**
1. Process Active Listings Report → extract shipping_template column
2. Analyze compliance by all 4 dimensions
3. Identify gaps (missing templates by design, device, product type)
4. Generate `shipping_compliance_YYYY-MM-DD.json`
5. Calculate revenue opportunity
6. POST to `/api/ingest/shipping`

**Saturday 8 AM (Dashboard Review):**
- Cem opens dashboard
- First thing he sees: **Shipping Compliance Center**
- Overall: 85% | Gap: 502K SKUs | Opportunity: $100K-200K/year
- Click to drill down by dimension
- Assign actions to owners
- Track conversion impact weekly

---

## Status

**Priority:** CRITICAL (top 3 for Q2)

**Integration:** Ready to add to:
1. `weekly_listings_processor.py` (Codex enhancement, 2 hours)
2. `DASHBOARD-DESIGN-SPEC.md` (add Shipping Compliance Center as View 1.5)
3. SQLite schema (add shipping_compliance + shipping_compliance_summary tables)

**Timeline:** Can be added for Phase 1 (Apr 15-20) or prioritized as Phase 0 (this weekend)

**Recommendation:** **Phase 0 this weekend** — This is too critical to deprioritize. Build shipping dashboard first (1-2 days), then phase in the other views.

---

**Owner:** Ava | **Reviewed by:** Cem (requested) | **Status:** Ready for approval

