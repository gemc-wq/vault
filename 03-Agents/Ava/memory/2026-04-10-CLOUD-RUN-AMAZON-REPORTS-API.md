# Apr 10 — Cloud Run Amazon Reports API Investigation

**Cem asks:**
1. Can we edit listings via the middleware on Cloud Run?
2. Which Amazon report = "Sales Traffic by Child ASIN"?
3. Can we run that report via API (not manual download)?

---

## What I Found

### Current Status
- ✅ **Amazon Reports API exists** on Cloud Run (confirmed Apr 4 in TOOLS.md)
- ✅ **Status:** RUNNING
- ❌ **Code access:** Need Codex to inspect service details

### Cloud Run Services (Confirmed Running)
```
✔  ecell-dashboard     (deployed Apr 9)
✔  fba-planner         (deployed Apr 9)
✔  nbcu-po-app         (deployed Mar 20)
✔  procurement-system  (deployed Apr 7)
✔  sales-dashboard     (deployed Mar 4)
✔  sales-dashboard-v2  (deployed Mar 3)
```

**Amazon Reports API:** Not found as separate service. Likely embedded in `ecell-dashboard` or `sales-dashboard-v2`.

---

## Research Needed (For Codex Tonight)

### 1. Listing Edit Capability
**Question:** Does our Cloud Run service support SP-API `PutListingsItem` or `UpdateListingItem`?

**What to check:**
- Cloud Run service source code (GitHub repo)
- SP-API scope permissions in Cloud Run environment variables
- Check if `product_type_name` + `shipping_template` fields are editable

**If YES:** Can edit listings (including shipping template assignment) via API
**If NO:** Can only READ listings, cannot modify

### 2. "Sales Traffic by Child ASIN" Report
**Problem:** Amazon has dozens of report types. Need to identify the exact one.

**Candidates:**
- `GET_SALES_AND_TRAFFIC_BY_ASIN` (most likely)
- `GET_MERCHANT_LISTINGS_ALL_DATA`
- Custom Child ASIN report (may not be in standard API)

**What to check:**
- Amazon SP-API documentation: `/reports` endpoint
- Filter for reports containing "ASIN" + "TRAFFIC" or "SALES"
- Check if report is available via `CreateReport` endpoint

**Amazon report IDs to test:**
```
GET_SALES_AND_TRAFFIC_BY_ASIN
GET_SALES_AND_TRAFFIC_BY_CHILD_ASIN (if exists)
GET_MERCHANT_LISTINGS_DATA
GET_SALES_AND_TRAFFIC_REPORT
```

### 3. Can We Run It Via API?
**If report exists in SP-API:** YES, can run via Cloud Run
**If report is Seller Central-only:** Must continue manual download

**Implementation:** Cloud Run would need to:
1. Call CreateReport with report type ID
2. Poll GetReport until status = DONE
3. Download report via GetReportDocument
4. Store in Supabase or trigger analysis

---

## Questions for Cem

1. **Which Cloud Run service has Amazon Reports API?** 
   - `ecell-dashboard` or `sales-dashboard-v2`?
   - Or separate service I haven't found?

2. **Do we have SP-API credentials in Cloud Run?**
   - Needed to make API calls to Amazon
   - Verify refresh token + credentials are current

3. **What's the priority?**
   - Listing edit capability (for shipping templates)?
   - Or report automation (for sales traffic data)?
   - Or both?

---

## Action Plan

### Tonight (Codex Job)
1. Inspect Cloud Run service code (ecell-dashboard or sales-dashboard-v2)
2. Check SP-API capabilities + scope permissions
3. Look up Amazon report IDs in SP-API docs
4. Test if "Sales Traffic by Child ASIN" report exists

### Tomorrow (Based on Results)
1. **If listing edit available:** Document API endpoint + implement shipping template bulk update
2. **If report available:** Wire Cloud Run to pull weekly, trigger analysis
3. **If both missing:** Document blockers + plan implementation

---

## Related Documentation

- `TOOLS.md`: Amazon Reports API entry (status = RUNNING)
- `SOP_WEEKLY_REPORTS.md`: Current manual download process (Step 1)
- `SP-API-GUIDE.md` (Harry's vault): SP-API overview + capabilities
- Amazon SP-API docs: https://developer.amazon.com/docs/sp-api/

---

## Owner
Ava (strategy) → Codex (investigation) → Harry (implementation)

**Status:** Waiting for Codex results tomorrow morning.

