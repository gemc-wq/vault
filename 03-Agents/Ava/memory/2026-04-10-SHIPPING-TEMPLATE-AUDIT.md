# Apr 10, 4:24 PM — Shipping Template Audit Priority

## Problem Statement (from Cem)

**Increasing items are missing the Reduced Shipping Template and have only the default Amazon shipping template.**

**Impact:**
- Default template shows **long delivery times** (5-7+ days)
- Reduced Shipping Template shows **2-day delivery**
- **Delivery time ↔ Conversion is directly correlated**
- Items with long delivery times → lower conversion rates

**Current Status:**
- ✅ Amazon US Listings & Traffic reports downloaded to Mac Studio
- ✅ Ready for Codex agent analysis
- ❌ No analysis yet on shipping template compliance

---

## Action Items

### 1. Codex Analysis (Overnight)
**What:** Analyze Amazon US Listings report for shipping template gaps
- Count items with Reduced Shipping Template vs Default template
- Identify SKUs affected
- Calculate coverage percentage

**Data:** `~/Downloads/Amazon US Listings Report` (already on Mac Studio)

### 2. KPI to Track
**Metric:** Reduced Shipping Template compliance rate
- **Target:** 100% of active listings have Reduced Shipping Template
- **Current:** Unknown (needs Codex analysis)
- **Risk:** Items showing default shipping (long delivery) → lower conversion

### 3. Cron Status
- ✅ **Shipping Template Audit cron exists** → runs **2:00 AM Wednesday**
- ⚠️ **Current cron only verifies template correctness**, does NOT:
  - Track compliance percentage
  - Alert on gaps
  - Generate report for strategic review

### 4. Next Steps
1. Have Codex analyze downloaded reports
2. Generate gap report (which SKUs missing Reduced Shipping)
3. Update cron to include KPI tracking + alerts
4. Prioritize fixing high-volume designs first (HB401, HTPCR top sellers)

---

## Related Documentation
- Conversion Dashboard KPIs: `/Users/openclaw/Vault/01-Wiki/26-conversion-dashboard/`
- Cron Schedule: `/Users/openclaw/Vault/00-Company/compiled/CRON_SCHEDULE.md`
- Amazon Shipping Methods: `/Users/openclaw/Vault/01-Wiki/04-shipping/`

---

## Owner
Ava (Strategy) → Codex (Analysis) → Harry (Implementation)

