# 2026-04-02

## Decisions
- **Scope Expansion for Print Jig Requirements**: Cem directed that the analysis must include **all** sold product types, not just high-revenue ones. This is necessary to capture requirements for different printers, branches, jig logic, cutlines, and finishing workflows.
- **Project Goal**: The primary objective is to create a **product type × production requirement matrix** for every sold type in the lookback period.

## Deliverables
- **60-Day Product Type Sales Report**: A CSV containing 40 sold product types, units, and net sales.
  - Path: `projects/iren-dreco/output/product_type_sales_last_60d.csv`

## Blockers
- **Resolved**: Initial BigQuery query failed because `Amazon_Order_Id` does not exist in the target table. The query was corrected to use `Sales_Record_Number`, `Quantity`, and `Net_Sale`.

## Knowledge
- **Production Matrix Requirements**: For each product type, the following data points must be captured:
  - Product type code, units sold, and net sales.
  - Production branch (e.g., direct print, LAZCUT, other).
  - Hardware/printer and location.
  - Source asset type, intermediate file type, and final output type.
  - Technical requirements: Jig needed (Y/N), cutline (Y/N), white layer (Y/N), bleed (Y/N).
  - Inventory dependencies (blank inventory) and known manual quirks.
- **Sales Concentration**: The top three product types (**HLBWH**, **HTPCR**, and **HC**) account for **92.04%** of net sales over the last 60 days.

## Carry-forwards
- **Production Mapping**: Cem will annotate the 40 identified product types with their respective production requirements.
- **Matrix Structuring**: Once annotations are received, the agent will structure the data into a formal production matrix and SOP.