

# ---

**Project Brief: Modernized Print-on-Demand Commercial Asset Pipeline (Lane 1 Replacement)**

## **1\. Executive Summary & Objective**

**Project Name:** \[Insert Internal Project Name, e.g., 'ListingForge'\]

**Sponsor:** Cem

**Modernization Owner:** Athena

**Objective:**

Rebuild the existing legacy 'DRECO' (Replication) tool as a modernized, intelligent, web-based application driven by a single canonical database. The new system must automate the generation of market-ready listing images for hundreds of phone and tablet case device models, starting from *only one master design source file* (PSD), while maintaining the visual integrity of complex, licensed brand IP (logos, critical imagery).

**Modernization Standards (Core Principles):**

1. **Speed:** Faster path from approved design to listing assets (autolisting capable).  
2. **Coverage:** Scalable asset generation across *all* devices with minimal manual intervention.  
3. **Intelligence:** Convert hidden tribal knowledge (stored in old scripts and operator memory) into explicit database rules and AI-driven automation.  
4. **No Blind Preservation:** Do not clone legacy tool flaws; extract necessary business logic and apply modern, scalable, composable technology.

## ---

**2\. Legacy vs. Modernized Workflow Overview**

| Legacy Workflow (DRECO) | Modernized Workflow (ListingForge) |
| :---- | :---- |
| **Input:** 13 manual canvas templates (PSDs) per design to cover varying camera/case shapes. | **Input:** One (1) structured Master PSD source file. |
| **Logic:** Adobe ExtendScript (deterministic scripting) in Photoshop. | **Logic:** Backend service (e.g., Python/Pillow/Vector Masking) for composition \+ AI Image generation. |
| **Metadata:** Manual product coding into trackers; database insertion *before* rendering. | **Metadata:** Driven by a shared canonical model in Supabase; auto-inserted during design intake. |
| **Outputs:** Raw listing images on basic, fixed backgrounds. | **Outputs:** Five (5) distinct listing images per device, including contextual, AI-generated backdrops tailored to the brand. |
| **Approval:** Manual email/Teams notification. | **Approval:** Integrated web UI preview and approval flow. |
| **Storage:** Upload to AWS S3. | **Storage:** Auto-upload to S3 via deterministic naming conventions. |

## ---

**3\. Core Functional Requirements**

### **3.1. Design Source Lane (Intake & PSD Normalization)**

This modernized "Lane 1" begins *earlier* than legacy DRECO. It focuses on preparing the source asset for intelligent automation.

1. **Master PSD Rule:** The system must accept exactly *one* master PSD file containing the creative artwork.  
2. **IP Integrity (The Constraints):** The master PSD may contain licensed IP (logos, faces, specific textures). The composition logic must treat these layers as vectors or proportional constraints that *cannot* be warped, stretched, or have critical details (like faces or logos) obscured by varying camera hole masks.  
3. **Metadata Extraction:** Upon PSD ingestion, extract or require database registration for structured metadata (e.g., License Type, Brand Name, Design Variant Name).

### **3.2. Data Model (Supabase Consolidated Database)**

The system must be driven by a shared, canonical database, merging legacy "headcase" and "replication" databases into a modernization schema. Key tables are needed for:

1. **licenses / brands:** Metadata regarding licensing agreements and brand identity.  
2. **design\_code:** Registration of the unique master design.  
3. **jig\_coordinate\_data (Crucial):** Specific measurements, placement rules, safe areas, and masking geometry for *every* supported device and case type. This data must drive the composition engine.  
4. **marketing\_attributes:** Table mapping License/Brand to demographic and stylistic keywords for AI image prompting (e.g., Real Madrid \-\> "sports stadium bar", "atmospheric lighting", "wooden table").

### **3.3. Composition & Image Generation Engine**

The tool must automatically generate five (5) distinct images per device SKU (Device Model \+ Case Type).

#### **Output Requirements:**

1. **I1: Main Listing Image (Marketplace Compliant):**  
   * Case mock-up \+ phone device visualization.  
   * **Background:** 100% Pure White (\#FFFFFF).  
   * Must meet Amazon Main Image standards.  
2. **I2-I5: Feature/Supporting Images (Contextual AI):**  
   * Showcase product features using templates, but with dynamically generated backgrounds.  
   * **Background:** Dynamic AI-generated backdrop contextually relevant to the Brand/License and target demographic (e.g., Sport license \= stadium or bar setting; Fashion license \= runway or minimalist luxury setting).  
   * The backdrop data must be driven by the database marketing attributes.

### **3.4. AI Automation Layer (Metadata & Context)**

The database must provide the contextual data (Brand, Target Demo) to the composition engine. An LLM (e.g., Claude/Gemini) may assist by auto-completing missing demographic or marketing attribute data in the database based on the License type.

### **3.5. Web Application Interface (UX)**

An operator-facing web dashboard is required.

1. **Initiation:** Mechanism to point the app to a design asset in PSD format (located on local storage or S3).  
2. **Data Input/Confirmation:** UI to input or review key license/design metadata, leveraging AI autocomplete.  
3. **Preview Flow:**  
   * App must render a set of device variants (e.g., small camera, large central camera, tablet).  
   * Preview *all 5 outputs* for selected variants.  
4. **Approval:** Manual "Approve All" or "Review Needed" selection.  
5. **Action:** Upon approval, approved assets are saved deterministically to AWS S3.

### **3.6. Lane 2 (Print Production) Note**

Lane 2 (Manufacturing Print File Generation) is distinct. The requirement for Lane 2 print files is that they must be generated **"On-the-Fly"** during daily order processing.

* Print files must use the same raw source design asset (Master PSD) as the listing image to ensure fidelity.  
* This requirement prevents costly storage of pre-rendered high-res print files for hundreds of devices that may never sell.

## ---

**4\. Proposed Architectural Overview**

A composition-focused, server-side render architecture is needed to handle the constraint of not deforming IP.

* **Frontend:** React or similar modern web framework (Approval UI, dashboard).  
* **Database:** Supabase (PostgreSQL) for canonical product data, geometry (jig) data, and AI metadata.  
* **Backend Composition Engine:**  
  * *Option A (Legacy Path \- Not Preferred):* Photoshop via scripting.  
  * *Option B (Modern Path \- Preferred):* Python Backend (using services capable of interpreting PSD layers, masks, and smart objects, combined with vector logic like Pillow \+ external masking libraries).  
* **AI Backdrop Engine:** Integrated API (e.g., Stable Diffusion XL, DALL-E 3, or a similar Diffusion-based API) receiving prompt context from the Supabase marketing table.  
* **Storage:** Direct application output to AWS S3 (deterministic naming pattern).

## ---

**5\. Implementation Phases (Roadmap for Build)**

**Phase 1: Database & Intake (Foundations)**

* Consolidate legacy SQL files (headcase/replication) into a modernization Supabase schema.  
* Develop the jig\_coordinate\_data schema (critical masking data).  
* Create the Design Intake UI (manual data entry \+ AI autocomplete).

**Phase 2: Master PSD Composition (Logic)**

* Develop the composition engine to read ONE Master PSD and one camera hole mask (from jig data) and output a composite image.  
* *Key Milestone:* Prove the system can render a wide device (tablet) and a narrow device (phone) using the same PSD *without* obscuring a central logo with the camera hole and *without* deforming the licensed IP.

**Phase 3: AI Backdrop & Feature Templates (Intelligence)**

* Populate marketing attribute tables in the DB.  
* Integrate the AI background generation API.  
* Develop the feature template compositions (Protection, MagSafe, etc.) combining AI backdrops.

**Phase 4: Web UI Preview & Approval Flow**

* Build the frontend for previewing rendered mockups (all 5 images).  
* Implement approval logic and the S3 upload script (with deterministic naming).

**Phase 5: Lane 2 On-the-Fly integration**

* Develop the Print Production engine to generate TIFFs (printer-specific) upon order receipt, drawing from the same Master PSD asset.

# ---

