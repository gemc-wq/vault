# Daily Notes — 2026-02-22 (Saturday)

**Decisions**
- **Fulfillment Orchestrator Routing:** 
    - Veeqo for Amazon USA; GDrive for print files.
    - EU fulfillment via Evri and Royal Mail; PH freight via DHL, Fed, and FedEx.
    - **Hard Routing Rules:** All Saturday orders route to PHL; H89, HST, and HDM orders route to UK and FL only.
- **Data Architecture:** BigQuery (`instant-contact-479316-i4`) is now the primary data source for the Fulfillment Orchestrator, replacing direct MySQL access.

**Deliverables**
- **Fulfillment Orchestrator Phase 1 (MVP):** Next.js 14 application located at `C:\Users\gemc\clawd\projects\fulfillment-orchestrator\`. 
    - Features: BigQuery integration, 3-layer routing engine, manual overrides (printer downtime, holiday, peak mode, force-to-PHL), and a 2-minute polling worker (caching to `data/orders-cache.json`).
    - Build log: `memory/fulfillment-orchestrator-build-log.md`.
- **Documentation Updates:** 
    - Updated `Brain/Projects/shipping/FULFILLMENT_ORCHESTRATOR_SPEC.md`.
    - Updated `MEMORY.md` (BigQuery details and routing rules) and Backend Ops Master Plan (B1.4).