# Ecell Global — Company Overview
**Auto-compiled:** 2026-04-07 | **Source:** Vault (Gemma 4 26B)
**Includes:** Harry full vault sync, Ava business context, 6 skill files

---

# Ecell Global — Company Overview & Strategic Roadmap
*Auto-compiled: 2026-04-07 | Source: 01-Wiki + 02-Projects + **Harry Vault Sync***
*Vault Stats: 314 Wiki Pages | 46 Projects | 8 Specs | 17 Project Dirs | 14 Daily Logs*

---

# Ecell Global: Strategic Operational Overview

## 1. CURRENT STATE (Legacy "A")
**The Manual Multi-Channel Operator**

Ecell Global is a high-volume, labor-intensive print-on-demand (POD) entity. While generating **$5.5M–$6M in revenue**, the business is currently constrained by fragmented, legacy infrastructure and heavy manual intervention.

* **Core Business Model:** Multi-channel POD for tech accessories via Amazon, eBay, Etsy, and BigCommerce, fulfilled through global hubs (PH, UK, USA).
* **Scale & Complexity:** Managing **1.5M+ SKUs**, currently burdened by **77% dead stock** due to lack of programmatic pruning.
* **Legacy Infrastructure:** 
    * **Systems:** Fragmented PHP environments (Zero), manual spreadsheet-based procurement, and disconnected AWS/Ubuntu silos.
    * **Procurement:** Entirely manual PO creation, split logic, and supplier pricing managed within legacy PHP/Zero.
    * **Fulfillment:** Manual order-to-dispatch pipelines with high reliance on human "Print File Management" (5–7 staff daily).
* **Data Silos:** Disconnected sales data across marketplaces; no unified view of real-time inventory velocity or supplier performance.

---

## 2. TARGET STATE (Automated "B")
**The AI-Driven "Concept-to-Cash" Engine**

The vision is a transition from a manual workforce to an **AI Agent Ecosystem** powered by a unified, real-time data layer.

* **The Unified Data Layer:** A single source of truth utilizing **BigQuery**, **AWS Aurora**, and **Supabase**, integrating sales, inventory, and finance middleware.
* **Automated Procurement Control Tower:** A transition from manual PHP logic to an intelligent system featuring **automated reorder triggers** based on real-time velocity and **intelligent location splits** (US/UK/PH).
* **The "Zero 2.0" Production Lane:** An automated image generation pipeline that monitors BigQuery and triggers **ListingForge** to bridge the gap between new POs and marketplace-ready assets.
* **AI-Driven Fulfillment:** A centralized **Fulfillment Portal** managing outbound dispatch across all EU/UK/US marketplaces via a unified queue.
* **Financial Intelligence:** A comprehensive **Finance Middleware** tracking the full PO lifecycle (Ordered $\rightarrow$ Acknowledged $\rightarrow$ Produced $\rightarrow$ Shipped $\rightarrow$ Received) with integrated China portal tracking.

---

## 3. GAP ANALYSIS

### 🔴 Critical Gaps (Active Workstreams)
* **The Fulfillment Migration Gap:** The current end-to-end pipeline must be mapped and migrated from legacy manual handling to a **Veeqo-based flow** to reduce operational drag.
* **The Procurement Gap:** Transitioning from "Zero" (PHP-based) manual logic to the new **Procurement System Spec**, specifically addressing the lack of automated reorder triggers and intelligent inventory splitting.
* **The Production Bottleneck:** The "Print File Pipeline" remains a manual drag; the **Zero 2.0 Automation** is required to automate image generation and S3 asset management.
* **The Data Discrepancy Gap:** Significant variance identified between **Legacy PH Orders** and the new **Procurement Control Tower** (e.g., EOL item handling and line-item reconciliation).

---

## 4. PROJECT TIERS (The Harry Vault Roadmap)

### **Tier 1: Infrastructure & Data Foundation**
* **Finance Middleware Build:** Implementation of the 11-table SQL schema for PO lifecycle and supplier invoice tracking.
* **Unified Product Database:** Migration of fragmented data into a centralized **Supabase/BigQuery** architecture.

### **Tier 2: Automation & Intelligence**
* **Zero 2.0 Production Lane:** Deployment of the automated image generation and S3/ListingForge pipeline.
* **Procurement Control Tower:** Implementation of automated reorder triggers and intelligent inventory velocity monitoring.
* **PULSE & ListingForge:** AI-driven SKU pruning and automated SEO/Image generation.

### **Tier 3: Fulfillment & Logistics**
* **Veeqo Migration:** Execution of the Order Management/Fulfillment Migration Spec.
* **Fulfillment Portal MVP:** Launch of the web portal for the UK fulfillment team to manage global outbound dispatch.
