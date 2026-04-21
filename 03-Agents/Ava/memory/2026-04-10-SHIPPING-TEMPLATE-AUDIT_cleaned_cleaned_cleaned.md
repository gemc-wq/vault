# Apr 10 — Shipping Template Audit Priority

**Decisions**
- **Cem (CEO):** Use Reduced Shipping Template (2-day) instead of standard (5-7+ days) to prevent conversion rate drops.

**Deliverables**
- Amazon US Listings & Traffic reports: `~/Downloads/Amazon US Listings Report`

**Blockers**
- Shipping template compliance analysis is pending completion of Codex analysis.

**Knowledge**
- **Process:** 100% compliance for active listings is required; delivery time directly impacts conversion rates.
- **Technical (Cron):** Shipping Template Audit runs Wednesdays at 2:00 AM; currently verifies template correctness only (no compliance % or gap alerts).
- **Technical (Paths):**
    - Conversion Dashboard KPIs: