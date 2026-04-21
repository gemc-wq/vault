# Pick List → Image Creation Workflow — Patrick Gaña
*Source: Email from Patrick (p.gana@ecellglobal.com), March 9 2026*
*Subject: Re: Workflow for Pick List creation and then to image creation tool*

---

## Step 1: PO Creation (Manual fallback if automated PO fails)
- **Manual process:** GDrive folder with screenshots: https://drive.google.com/drive/folders/1C8vX66643afK5_DbPq2HfxiPICuRqHFd
- **Automated PO:** `http://34.196.137.61/barcode/zero_generate_purchase_order_automated_phAMG1_wh.php` (Zero 1 server)

## Step 2: Generate Picking List
- GDrive folder with screenshots: https://drive.google.com/drive/folders/1gM6ZwGystk2Yi9ycZixYSBiq8zzD0Gl8

## Step 3: Generate Labels from Different Couriers
- GDrive folder with screenshots: https://drive.google.com/drive/folders/1eyUGBfjyslRQWW0DD3yClJ13_h-NeeWg

## PO Filtering Rules — HARDCODED in Zero
- **Script:** `https://zero.ecellglobal.com/barcode/zero_POFiltering.php`
- Rules are hardcoded in PHP — no UI to change them
- Changes require editing the PHP script directly on the server

## Picking List Rules — HARDCODED in Zero
- **Script:** `http://34.196.137.61/barcode/sage_generate_picking_list_split.php`

### Current Picking List Rules:
| Region | Carrier/Service |
|---|---|
| **US Amazon Orders** | Amazon Buy Shipping |
| **US Amazon (USPS)** | USPS Buy Shipping |
| **US Non-Amazon** | Stamps.com and Veeqo |
| **UK Orders** | Royal Mail Click & Drop RM24 Tracked LBT (TRN for Large Letter, TPN for Parcel) |
| **UK Buy Shipping** | Amazon generated labels using RM24 Tracked LBT |
| **Japan Orders** | Printed small stickers → PH Production |
| **Other Countries** | Royal Mail Click & Drop International (MTK for Large Letter, MP7 for Parcel) |

## Veeqo Usage (Current)
- **PH US Labels (Amazon):** Automated link generates Amazon Buy Shipping labels
- **PH US Labels (Non-Amazon):** Stamps.com
- **FL Labels (Amazon):** Same automated link
- **FL Labels (Non-Amazon):** **Veeqo** ← already in use for non-Amazon FL orders
- **Veeqo CAN be used for all US POs** — currently only used for FedEx/Non-Amazon FL

## Image Prep Trigger
1. MFG PO created in Zero
2. **Automated PO notification sent via email**
3. Staff receive email → open **HPT (Head case Production Tool)** 
4. HPT renders the print images for the PO items
5. Images stored on local NAS

## Key Contacts
- **Patrick Gaña** — IT, knows all scripts and rules
- **Jae (Joanna Rose Vitug)** — PH Production Manager, j.vitug@ecellglobal.com
- **Chad** — Image gen workflow (per Cem's meeting with Patrick and Chad)

## Implications for Veeqo Migration
1. PO filtering rules are hardcoded PHP → need to be replicated as Veeqo tab/filter configurations
2. Picking list carrier rules → map directly to Veeqo's carrier selection per channel
3. The "automated PO email → HPT" trigger is the bridge between order management and image creation
4. If Veeqo replaces Zero for label creation, the CSV export of shipped items replaces the automated PO email as the trigger for HPT
5. HPT (the image rendering tool) stays — it's the legacy tool Chad will manage with AI assistance

## Related
- [[wiki/23-drew-handover/ZERO_INFRASTRUCTURE|Zero Infrastructure]] — System these scripts run on
- [[wiki/23-drew-handover/PATRICK_IT_TEAM_PROFILE|Patrick IT Team]] — Who runs this workflow
- [[wiki/03-production/PRINT_FILE_PIPELINE|Print File Pipeline]] — Downstream image generation
- [[wiki/03-production/DAILY_PRINT_PRODUCTION|Daily Print Production]] — Full production cycle
- [[wiki/04-shipping/SOP_SHIPPING_LABELS|SOP: Shipping Labels]] — Label generation step
- [[wiki/23-drew-handover/VEEQO_REPLACEMENT_ANALYSIS|Veeqo Replacement]] — How Veeqo automates this
