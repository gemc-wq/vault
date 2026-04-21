# 2026-04-02

**Decisions**
- **Scope Expansion (Cem)**: Analysis must include all sold product types (not just high-revenue) to capture requirements for printers, branches, jig logic, cutlines, and finishing workflows.
- **Project Goal**: Create a product type × production requirement matrix for all sold types in the lookback period.

**Deliverables**
- **60-Day Product Type Sales Report**: CSV containing 40 product types, units, and net sales. Path: `projects/iren-dreco/output/product_type_sales_last_60d.csv`

**Blockers**
- **Resolved**: BigQuery query corrected to use `Sales_Record_Number`, `Quantity`, and `Net_Sale` (replacing non-existent `Amazon_Order_Id`).

**Knowledge**
- **Production Matrix Requirements**: Must capture product type code, units, net sales, production branch, hardware/location, asset/file types, technical specs (jig, cutline, white layer, bleed), and