# Vertex AI RAG Implementation Plan: Head Case Designs

**Version:** 1.0  
**Status:** Draft / Technical Design  
**Date:** February 2026

## Executive Summary
This document outlines the architecture and implementation roadmap for integrating Google Vertex AI into Head Case Designs' e-commerce and logistics workflows. The solution leverages **Vertex AI Search** for a geo-aware customer chatbot and **Gemini 2.5 Flash Vision** for an automated packing verification system.

---

## 1. Customer-Facing Chatbot (GoHeadCase.com)

### Vertex AI Search Configuration
- **Data Store Type:** Structured Data (Product Catalog).
- **Schema Design (12K+ Products):**
  - `id` (SKU): Primary identifier.
  - `title`: Product name (e.g., "Harry Potter Marauder's Map Leather Wallet Case").
  - `description`: Detailed product info, materials, and features.
  - `categories`: Array of categories (e.g., ["Phone Case", "Leather", "Harry Potter"]).
  - `image_url`: Primary product image for display in chat.
  - `product_url`: Direct link to GoHeadCase.com product page.
  - `price_us`, `price_uk`, `price_eu`: Regional pricing.
  - `sales_rank_us`, `sales_rank_uk`, `sales_rank_eu`: Regional popularity scores.
  - `license`: Brand name (e.g., "LFC", "Harry Potter", "Peanuts").
  - `region_availability`: Array of codes ["US", "UK", "EU"] for filtering.

### Geo-Location Detection & Logic
1.  **Detection:** Use CloudFront/Cloudflare headers or an IP-API (MaxMind) at the frontend to identify `user_region`.
2.  **Routing Logic:**
    - **US Market:** Prioritize Harry Potter, Peanuts, WWE, and NCAA/NFL.
    - **UK Market:** Prioritize Football Clubs (LFC, MCFC, etc.).
    - **EU Market:** Prioritize FC Barcelona, Inter Milan, and local clubs.
3.  **Vertex AI Filter:** Pass the region as a filter to the Search API: `filter: "region_availability: ANY('UK')"` and use `boost_spec` to rank results by `sales_rank_uk`.

### Gemini Flash Integration & Grounding
- **Model:** `gemini-2.5-flash` (Optimal for speed and cost).
- **Grounding:** Configured with the Vertex AI Search Data Store.
- **System Instruction:** 
  > "You are the Head Case Designs personal shopper. Use the provided product search results to recommend cases. If the user is in the UK, emphasize football kits. If in the US, focus on Harry Potter or Peanuts. Always provide the direct product URL and image."

### Chat Widget Implementation
- **Tech:** Custom Web Component (Shadow DOM) for easy embed on GoHeadCase.com (BigCommerce).
- **Flow:** 
  1. Visitor lands → Detect region (e.g., UK).
  2. User: "I need a case for iPhone 16."
  3. Backend: Query Vertex AI Search with `query="iPhone 16"`, `filter="UK"`, `boost="sales_rank_uk"`.
  4. Gemini: Processes top 5 results → Generates friendly recommendation with links/images.

---

## 2. Packing Verification App

### Architecture: Gemini Vision Direct
- **Approach:** Direct multimodal prompting (No RAG required).
- **Mobile Web App:** Simple React/Vue app with camera access (`navigator.mediaDevices.getUserMedia`).

### Workflow
1.  **Scan Order:** Packer scans the order barcode (pulls expected SKU from Supabase).
2.  **Capture Image:** Packer snaps a photo of the physical product being packed.
3.  **Verification Request:** App sends the photo + expected product description to Gemini Vision.
4.  **Prompt Example:**
    > "Identify the product in this image. Does it match the description: 'Liverpool FC Home Kit Red Crest Digi-Camo Phone Case for iPhone 16 Pro'? Verify the design, the club crest, and the camera cutout shape. Reply with: {'match': true/false, 'confidence': 0-1, 'reason': '...'}"

### Error Handling & Alerts
- **Mismatch:** If `match: false`, trigger a red UI alert and require supervisor override or re-scan.
- **Low Confidence:** Prompt the packer to retake the photo in better lighting.

### Performance & Cost
- **Latency:** ~2-4 seconds per scan.
- **Cost:** ~$0.0005 per scan (Gemini 2.5 Flash token rates for images).
- **Monthly (5K scans):** ~$2.50.

---

## 3. Technical Implementation

### Google Cloud Setup
1.  **Project:** Create `head-case-ai-prod`.
2.  **APIs:** Enable Vertex AI, Generative AI, and Cloud Run APIs.
3.  **IAM:** Create a service account with `Vertex AI User` and `Discovery Engine Viewer` roles.

### Data Sync (Supabase → Vertex AI)
- **Tool:** Scheduled Cloud Function (Node.js/Python).
- **Schedule:** Every 6 hours (CRON).
- **Logic:** Query Supabase `products` table → Format as JSONL → Upload to GCS → Trigger Vertex AI Search Indexing.

### Cost Breakdown (Estimated 20K Chat / 5K Scans)
| Item | Unit Cost | Monthly Total |
| :--- | :--- | :--- |
| Vertex AI Search Standard | $1.50 / 1K queries | $30.00 |
| Grounding Requests | $2.50 / 1K requests | $50.00 |
| Gemini 2.5 Flash (Tokens) | Mixed | ~$5.00 |
| Cloud Run Hosting | Standard | ~$15.00 |
| **Total Estimated** | | **~$100.00 / month** |

### Implementation Timeline
- **Week 1:** Data store creation, Supabase sync job, and basic RAG grounding testing.
- **Week 2:** Geo-location logic, Chat widget frontend, and Gemini prompt tuning.
- **Week 3:** Packing App MVP (Camera integration + Vision verification) and UAT.

---

## 4. Data Flow Diagrams

### Customer Chatbot Flow
```text
[Supabase DB] ──(Daily Sync)──▶ [Vertex AI Search Index]
                                       ▲
                                       │ (Search & Filter)
                                       │
[User Query] ──▶ [Backend / Gemini] ◀──┘
      │               │
      └─▶ [Response with Product Links] ──▶ [Web Chat Widget]
```

### Packing Verification Flow
```text
[Camera App] ──(Photo + Expected SKU)──▶ [Gemini 2.5 Flash Vision]
                                              │
[Supabase Orders] ◀──(Log Result)─────────────┤
                                              ▼
[Mobile UI] ◀────(MATCH / MISMATCH Alert)─────┘
```

---
*Created by Clawdbot for Head Case Designs.*
