# Apr 10 — Shipping Template Audit Priority

**Decisions**
- **Cem (CEO):** Identified a critical issue where items are defaulting to the standard Amazon template (5-7+ days) instead of the Reduced Shipping Template (2-day), directly impacting conversion rates.

**Deliverables**
- Amazon US Listings & Traffic reports downloaded to Mac Studio: `~/Downloads/Amazon US Listings Report`

**Blockers**
- Shipping template compliance analysis is pending the completion of the Codex analysis.

**Knowledge**
- **Process:** Delivery time is directly correlated to conversion rates; the goal is 100% compliance for all active listings.
- **Technical (Cron):** The Shipping Template Audit cron runs **Wednesdays at 2:00 AM**. It currently only verifies template correctness; it does **not** yet track compliance percentages or generate gap alerts.
- **Technical (Paths):**
    - Conversion Dashboard KPIs: `/Users/openclaw/Vault/01-Wiki/26-conversion-dashboard/`
    - Cron Schedule: `/Users/openclaw/Vault/00-Company/compiled/CRON_SCHEDULE.md`
    - Amazon Shipping Methods: `/Users/openclaw/Vault/01-Wiki/04-shipping/`
- **Team Workflow:** Strategy (Ava) $\rightarrow$ Analysis (Codex) $\rightarrow$ Implementation (Harry).

**Carry-forwards**
- Perform Codex analysis on downloaded reports to identify SKUs missing the Reduced Shipping Template.
- Update the audit cron to include KPI tracking and automated gap alerts.
- Prioritize fixing high-volume designs (e.g., HB401, HTPCR) once gaps are identified.