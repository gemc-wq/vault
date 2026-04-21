

\# ARCHITECTURE & PLANNING BRIEF: ListingForge (DRECO Modernization)  
**\*\*Target AI:\*\*** Claude Opus 4.6 (Execute in Plan Mode First)  
**\*\*Project Context:\*\*** Modernization of an e-commerce print-on-demand image generation pipeline.

\#\# 1\. Project Objective  
Transition the legacy "DRECO" (Lane 1\) asset generation tool into "ListingForge." The goal is to move from a manual, 13-template-per-design Photoshop workflow to a highly automated, single-source-of-truth pipeline. This system will dynamically generate listing-ready composite images across hundreds of device variants using a single Master PSD, guided by a canonical database.

\#\# 2\. Core Constraints & Technical Decisions  
Based on technical discovery, the architecture must adhere to the following constraints:

\* **\*\*Execution Environment:\*\*** The Proof of Concept (POC) **\*\*must run locally\*\***. Moving to a web-app upload model is planned for the future, but local execution is required now due to file sizes.  
\* **\*\*Composition Engine Engine:\*\*** **\*\*No costly paid composition APIs\*\*** (e.g., Adobe API). The solution must rely on open-source/local programmatic libraries (e.g., Python \`psd-tools\`, \`Pillow\`, \`ImageMagick\`, or headless scripting if absolutely necessary for Smart Objects).  
\* **\*\*Source File Specifications:\*\***  
    \* Format: High-resolution \`.psd\` files utilizing Smart Objects and safe zones.  
    \* Size: Extremely large (\~250MB+ per file).  
    \* Structure: The design relies on 13 legacy layout formats (1-1 through 3-1). Format **\*\*"1-1"\*\*** is the designated parent/master format. The new engine must dynamically map the 1-1 parent artwork to the other 12 ratios/placements programmatically.  
\* **\*\*Geometry/Jig Data:\*\*** Already compiled and available via CSV/DB. This data dictates the camera hole masks, scaling, and translation requirements to convert the 1-1 layout into the other formats.  
\* **\*\*AI Stack:\*\***  
    \* **\*\*Text/Metadata Engine:\*\*** Claude Sonnet 4.6 (for interpreting database marketing attributes and generating prompts/context).  
    \* **\*\*Image Generation Engine:\*\*** Gemini 3 Flash Image / Nano Banana 2 (for generating contextual, brand-appropriate backgrounds).  
\* **\*\*Feature Image Output:\*\*** The tool must generate 1 main image (pure white background for Amazon compliance) and 4 supporting feature images (e.g., MagSafe, drop protection). The layout and text for these feature overlays should be generated based on standard e-commerce marketing best practices.

\#\# 3\. System Architecture (Local POC)

The local POC should be structured into three distinct modules:

\#\#\# Module A: Data & Context Resolution  
1\.  Read the local \`jig\_coordinate\_data\` CSV to load spatial rules (scale, X/Y translation, mask path) for all target SKUs.  
2\.  Query the local database/CSV for the specific design's metadata (Brand, License Type).  
3\.  Pass metadata to Claude Sonnet 4.6 to generate semantic background prompts (e.g., "Minimalist modern sports locker room, out of focus").

\#\#\# Module B: Background Generation (AI Layer)  
1\.  Execute API calls to the image generation model (Gemini 3 Flash Image) using the prompts generated in Module A.  
2\.  Save the 4 contextual background plates locally.

\#\#\# Module C: Local Composition Engine  
1\.  Ingest the Master 1-1 PSD file (250MB+).  
2\.  **\*\*Critical Risk Area:\*\*** Parse the PSD to isolate the core artwork/Smart Object.   
3\.  For each required device SKU:  
    \* Apply mathematical transformations (scale/translate) to the 1-1 artwork based on the CSV jig data.  
    \* Apply the device-specific camera cutout mask.  
    \* **\*\*Output 1:\*\*** Composite over a \#FFFFFF background.  
    \* **\*\*Outputs 2-5:\*\*** Composite over the AI-generated backgrounds from Module B. Apply marketing-best-practice overlays (text/graphics for protection, materials, etc.).  
4\.  Save the final 5 flat output images (e.g., \`.jpg\` or \`.png\`) to a designated local output directory.

\#\# 4\. Required Output from Claude Opus (Plan Mode)

Claude, please review this brief and output a comprehensive technical plan addressing the following:

1\.  **\*\*Python Library Selection:\*\*** Analyze the viability of using \`psd-tools\` vs. other local Python imaging libraries specifically for handling 250MB PSDs containing Smart Objects. If Python cannot accurately parse the Smart Objects without rasterizing or losing fidelity, propose an alternative local automation path (e.g., Python driving local Photoshop via COM/AppleScript).  
2\.  **\*\*Data Structure:\*\*** Outline the required schema for the \`jig\_coordinate\_data\` CSV to ensure the Python engine has the exact geometric parameters needed to translate the 1-1 Master to a 3-1 or 1-8 placement.  
3\.  **\*\*Step-by-Step Code Architecture:\*\*** Provide a folder structure and pseudocode outline for the POC application.  
4\.  **\*\*Marketing Overlay Strategy:\*\*** Detail how the system will programmatically apply the "best practice" marketing text/icons onto Outputs 2-5 without clashing with the AI-generated backgrounds.  
