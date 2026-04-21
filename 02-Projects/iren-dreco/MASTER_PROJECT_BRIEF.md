# IREN / DRECO Modernization — Master Project Brief

**Date:** 2026-04-02  
**Owner:** Ava  
**Human Sponsor:** Cem  
**Status:** Active strategic scoping  

---

## 1. Purpose

This project is not about copying legacy internal tools for the sake of preservation. It is about extracting the real business logic from the existing DRECO and IREN systems, then rebuilding a more scalable, explicit, and automatable operating system for Ecell Global.

The modernization effort must support the company mission across all three pillars:

- **Coverage** — more approved designs on more devices across more marketplaces
- **Speed** — faster path from design approval to listing-ready assets and from order receipt to print-ready files
- **Intelligence** — explicit, inspectable rules instead of tribal knowledge buried in old code, file naming habits, and operator memory

---

## 2. Strategic framing

DRECO and IREN are not just "apps." They represent two critical operational lanes in the business.

### Lane 1 — Sales / Commercial Asset Lane
**DRECO wearing its image-replication hat**

Mission:
Turn approved design assets into market-leading listing images, store them in S3/CDN, and connect them into product/content creation workflows via Supabase.

Core flow:
`Design source asset -> replication/render rules -> listing image outputs -> S3/CDN -> Supabase item content/product creation`

Primary value:
- removes the listing-image bottleneck
- increases SKU coverage
- creates structured commercial asset outputs tied to product creation

### Lane 2 — Print Production Lane
**IREN wearing its manufacturing hat**

Mission:
Turn processed demand into location-specific, product-specific, printer-ready output files that can be used in production with minimal manual interpretation.

Core flow:
`Order/PO -> routing by location -> blank assignment -> production asset resolution -> IREN print generation -> printer-specific TIFF/output pack -> QA -> operator-ready production packet`

Primary value:
- reduces order-to-print time
- reduces production errors and manual prepress work
- creates a scalable POD manufacturing workflow

---

## 3. Why Lane 2 starts first

Cem directed that this project should begin with the **Print Production lane** rather than the Sales lane.

Reasoning:
- Lane 2 is closer to actual fulfillment and production outcomes
- Lane 2 can be defined concretely using hardware, file outputs, and current operator workflows
- Lane 2 is less blocked by incomplete global commercial asset coverage
- Cem already successfully created an IREN-style print file app prototype using Codex and sample images
- The Philippines environment contains high-res production files and the live operational runtime needed to inspect the real workflow

This means the immediate goal is not broad reverse engineering, but rather:

**define the true production SOP, hardware map, data flow, file states, and exception handling for Lane 2 first**

---

## 4. Lanes within the lanes

The top-level lanes are still too broad for implementation. Each lane must be broken into sub-lanes/stages with explicit inputs, outputs, decisions, and owners.

### Lane 1 — Sales sub-lanes
1. **Design Asset Intake**
   - ingest approved PSD/design files and metadata into a canonical asset structure
2. **SKU / Product Resolution**
   - determine valid sellable SKU combinations by design, device, product type, and marketplace
3. **Commercial Rendering**
   - DRECO-style replication of source assets into listing-ready visuals
4. **Asset Storage / Publication**
   - deterministic S3/CDN storage and naming
5. **Content Sync / Product Creation**
   - connect image outputs to Supabase item content and product creation flows

### Lane 2 — Print Production sub-lanes
1. **Order Intake / Routing**
   - assign jobs by location based on operations rules
2. **Blank Inventory Assignment**
   - match digital SKU to actual blank inventory by location and product type
3. **Production Asset Resolution**
   - determine which source/high-res/rendered image is needed for the print job
4. **Jig / Print File Generation**
   - IREN-style generation of print-ready TIFF and related outputs
5. **Image Check / QA**
   - validate outputs before production
6. **Operator Execution / Handoff**
   - package output into a print-ready work packet for staff

---

## 5. Upstream source lane must be included

A major correction in this discussion was that DRECO is **not the true start of the process**.

The true source starts earlier with the **graphic designer lane**:
- PSD creation
- multiple template sizes
- design asset preparation
- variant setup
- source file naming and organization

This designer source lane must be modeled explicitly because it is a likely place where an AI assist layer can create real leverage.

Potential AI leverage areas upstream:
- PSD normalization
- asset intake validation
- preflight checks before DRECO/replication
- design variant preparation
- structured metadata extraction from source assets

This means the future architecture is not just two lanes, but effectively:

`Designer Source Lane -> Sales Lane (DRECO) -> Print Production Lane (IREN/production)`

---

## 6. Illustrator scripting remains in scope

Cem explicitly flagged that Adobe Illustrator scripting should **not** be discounted.

Illustrator scripting may be highly relevant for:
- printer-ready template creation
- cutline generation
- bleed handling
- print-quality adjustments
- deterministic output preparation prior to printer-specific conversion

This is strategically important because not all automation should be AI-first. Some parts of the workflow may be better served by deterministic scripting layers, especially where print fidelity and repeatability matter.

**Conclusion:** Illustrator scripting should remain a live option in the modernization stack, especially inside Lane 2 and in the upstream/prepress stages.

---

## 7. Live PH environment is a critical source of truth

Cem confirmed he has remote login access to the live IREN/DRECO PC in the Philippines.

This materially changes the project because it lets us inspect runtime truth directly rather than inferring from code alone.

What the PH environment can reveal:
- actual app/runtime directories
- config files
- source asset locations
- high-res file locations
- template and cutline folders
- output folder conventions
- printer-specific file behavior
- manual operator actions and hidden tribal knowledge

This environment should be treated as the primary discovery source for Lane 2 SOP creation.

---

## 8. Shared core needed across all lanes

Although Sales and Print Production are distinct lanes, they must sit on top of a shared canonical model.

### Shared core components
- **Design identity** — what the design is and where source assets live
- **SKU identity** — canonical product/device/design/variant representation
- **Product/render family mapping** — how product codes resolve to render/output families
- **Device/jig mapping** — measurements, placements, safe areas, print geometry
- **Output identity** — naming patterns, storage paths, file states, versions

The long-term goal is to avoid two separate brains for sales assets and production assets.

---

## 9. Role of Supabase item content work

Lane 1 does not end at "image generated." The real endpoint is when rendered images are tied into structured content and product creation workflows.

This connects directly to the Supabase item content work Ava and Jay Mark have been shaping.

That means the final Lane 1 endpoint is:
- generated commercial image assets
- saved to deterministic storage paths
- linked into structured item content/product records in Supabase
- ready for downstream product/listing creation

---

## 10. Immediate project priority — Lane 2 SOP

The next concrete deliverable should be a **Lane 2 Production SOP / Architecture Spec** that defines:

1. product type -> printer / hardware map
2. location-specific production routing rules
3. blank inventory assignment logic
4. source image / high-res dependency rules
5. IREN output types and file states
6. printer-specific TIFF/output conversion behavior
7. QA / image-check process
8. exception handling for missing files, unsupported SKUs, wrong templates, etc.

This SOP should be built from:
- legacy tool analysis
- live PH runtime inspection
- sample files and outputs
- known operator workflows

---

## 11. LLM Council / multi-model review approach

Cem proposed using multiple models/agents to critique and improve the architecture decisions.

Recommended council roles:
- **Opus 4.6** — architecture critique, strategic challenge, system design review
- **Codex** — implementation structure, code-level reduction, technical blueprinting
- **Gemini 3.1** — image-generation / creative automation assessment, AI image-layer suitability

This should not be treated as model redundancy for its own sake. Each model should be used for its comparative advantage.

### Proposed use of council
- review master project framing
- critique lane definitions and sub-lanes
- assess best automation layer per stage (AI vs script vs web app vs deterministic tooling)
- challenge assumptions before build work starts

---

## 12. Working hypothesis for modernization direction

The likely future system is not a 1:1 clone of legacy apps. It is a clearer operating system with explicit stages:

### Future architecture hypothesis
1. **Designer Source Lane**
   - asset intake, preparation, and AI-assisted normalization
2. **Sales Lane (DRECO modernization)**
   - commercial image replication and S3/Supabase integration
3. **Production Lane (IREN modernization)**
   - routing, blank assignment, print file generation, QA, and operator handoff
4. **Supporting deterministic layers**
   - Illustrator scripting and printer-specific template tooling where precision matters

---

## 13. Recommended next documents

This master brief should become the anchor document. The next documents should build underneath it:

1. **Lane 2 Production SOP**
2. **PH IREN/DRECO Runtime Capture Checklist**
3. **Product Type × Printer / Output Matrix**
4. **Designer Source Lane Spec**
5. **Sales Lane (DRECO) Endpoint Spec**
6. **Shared Core Data Model Spec**
7. **LLM Council Review Notes**

---

## 14. Current decision summary

### Confirmed
- DRECO and IREN represent two critical operational lanes
- Lane 2 (Print Production) is the first modernization focus
- The designer source lane must be added upstream
- Illustrator scripting remains in scope as a production-quality tool
- The PH runtime environment is a critical source of truth
- A master project brief should serve as the anchor before deeper SOP work begins
- A multi-model council approach is appropriate for tool/architecture evaluation

### Not yet finalized
- exact Lane 2 SOP
- product type -> hardware/output matrix
- full designer source lane workflow
- shared core schema/tables
- exact role split across Harry / Jay Mark / Ava / sub-agents

---

## 15. Core project principle

Do not rebuild the legacy system blindly.

Instead:
- extract the real business logic
- define the critical endpoints
- make the hidden rules explicit
- choose the best automation tool per stage
- rebuild only what improves Coverage, Speed, and Intelligence

That is the modernization standard.
