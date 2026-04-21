# 2026-03-20 (Friday)

## Decisions
- **Procurement Logic:** Implemented demand-based split (US $\to$ FL, UK/ROW $\to$ UK, JP $\to$ PH, overflow $\to$ PH).
- **Logistics:** Separate POs will be issued per destination to ensure clean shipping and invoice reconciliation.
- **Costing Source of Truth:** Item cost is now the **last PO price per item** (replacing `t_m_supplier_