# Apr 10 — Shipping Template Audit Priority

**Decisions**
- **Cem (CEO):** Items must use the Reduced Shipping Template (2-day) instead of the standard Amazon template (5-7+ days) to prevent conversion rate drops.

**Deliverables**
- Amazon US Listings & Traffic reports: `~/Downloads/Amazon US Listings Report`

**Blockers**
- Shipping template compliance analysis is pending completion of the Codex analysis.

**Knowledge**
- **Process:** 100% compliance for all active listings is required; delivery time is directly correlated to conversion rates.
- **Technical (Cron):** Shipping Template Audit cron runs **Wednesdays at 2:00 AM**. Currently verifies template correctness only; does not yet track compliance percentages or generate gap alerts.
- **Technical (Paths):**
    - Conversion Dashboard KPIs: `/Users/openclaw/Vault/01-Wiki/26-conversion-dashboard/`
    - Cron Schedule: `/Users/openclaw/Vault/00-Company/compiled/CRON_SCHEDULE.md`
    - Amazon Shipping Methods: `/Users/openclaw/Vault/01-Wiki/04-