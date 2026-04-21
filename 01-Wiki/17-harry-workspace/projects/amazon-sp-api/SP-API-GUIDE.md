# Amazon Selling Partner API (SP-API) Implementation Guide

This guide provides a comprehensive overview of the requirements, setup, and practical implementation details for accessing the Amazon Selling Partner API (SP-API) for **Ecell Global / Head Case Designs** on US and UK marketplaces.

## 1. Developer Registration Process

To access the SP-API, you must first register as a developer in Amazon Seller Central.

### How to Register
1. Log in to [Seller Central](https://sellercentral.amazon.com) (US) or [Seller Central UK](https://sellercentral.amazon.co.uk) as the **Primary Account User**.
2. Go to **Apps & Services** > **Develop Apps**.
3. Click **Developer Central** and then **Register as a Developer**.
4. Complete the Developer Profile application.

### Requirements
*   **Professional Selling Account:** Individual accounts are not eligible.
*   **Company Information:** Legal name, address, and contact details.
*   **Data Protection Policy (DPP) Compliance:** You must answer a detailed security questionnaire (approx. 20-30 questions) covering:
    *   Network protection (firewalls, IDS/IPS).
    *   Access management (unique IDs, MFA for all users).
    *   Encryption at rest (AES-256) and in transit (TLS 1.2+).
    *   Incident response plans.
    *   Vulnerability management (regular scanning).
*   **Acceptable Use Policy (AUP):** Agreement to only use data for permitted purposes (e.g., fulfilling orders, tax calculations).

### Timeline for Approval
*   **Typical:** 5–10 business days.
*   **Note:** If requesting "Restricted" roles (PII access), Amazon may request additional documentation or a 3rd-party audit, which can extend the timeline to several weeks.

### Self-Authorized vs. Public App
| Feature | Self-Authorized (Private) | Public App |
| :--- | :--- | :--- |
| **User Base** | Exclusive to your own organization. | Multiple external sellers. |
| **Authorization** | Simple "Self-Authorization" via Seller Central. | Full OAuth 2.0 flow (Login with Amazon). |
| **Review** | Standard developer review. | Rigorous review + Appstore listing required. |
| **Recommendation** | **Best for Ecell Global** for internal tools. | Only if you plan to sell the software. |

---

## 2. Authentication Setup

SP-API uses a multi-layered authentication approach: **LWA (Login with Amazon)** for OAuth and **IAM (AWS Identity and Access Management)** for signing requests.

### Required Credentials
*   **LWA Client ID & Client Secret:** Generated when you create your app in Seller Central.
*   **Refresh Token:** Obtained after authorizing your app. For private apps, this is generated once during self-authorization.
*   **AWS IAM User/Role:**
    *   **Access Key ID & Secret Access Key:** Used to sign requests using Signature Version 4 (SigV4).
    *   **IAM Policy:** Must have `execute-api:Invoke` permission on the SP-API resources.
    *   **IAM ARN:** The User/Role ARN must be associated with your Developer Profile in Seller Central.

### Step-by-Step Setup
1.  **Create IAM User/Role:** In AWS Console, create a user with "Programmatic access" and attach a policy allowing `execute-api:Invoke`.
2.  **Register App in Seller Central:** Under **Develop Apps**, click "Add new app". Enter the **IAM ARN** created in step 1.
3.  **Retrieve LWA Credentials:** After creating the app, copy the Client ID and Client Secret.
4.  **Authorize & Get Refresh Token:** For a private app, click "Authorize" next to the app in Seller Central to receive your permanent Refresh Token.

---

## 3. Key API Endpoints & Reports

### a) Sales & Orders Data
To replicate "Business Report" (Sales & Traffic) CSV exports:
*   **Endpoint:** `GET /reports/2021-06-30/reports`
*   **Report Type:** `GET_SALES_AND_TRAFFIC_REPORT`
*   **Required Role:** Brand Analytics (must be Brand Registry enrolled).
*   **Orders API:** `GET /orders/v0/orders` for real-time order status and basic metadata.
*   **Orders Report:** `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL` for bulk historical order data.

### b) FBA Inventory Data
*   **FBA Inventory API:** `GET /fba/inventory/v1/summaries` for real-time fulfillable quantities.
*   **Inventory Report:** `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` (near real-time).
*   **Restock Recommendations:** `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`.
*   **Inventory Ledger:** `GET_LEDGER_SUMMARY_VIEW_DATA` for reconciling ins/outs (like a bank statement).

### c) Financial & Settlement Data
*   **Finances API:** `GET /finances/v0/financialEvents` for real-time individual transaction data (fees, refunds, promos).
*   **Settlement Reports:** `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` (The most critical for royalty calculations; generated every ~2 weeks).
*   **Role:** Finance and Accounting.

### d) Product Catalog
*   **Catalog Items API:** `GET /catalog/2022-04-01/items/{asin}`.
*   **Use Case:** Mapping ASINs to SKUs and retrieving product titles/images for reports.
*   **Role:** Product Listing.

---

## 4. Rate Limits & Quotas

SP-API uses a **Token Bucket** algorithm (Burst vs. Sustained).

| API Section | Sustained Rate | Burst Limit | Note |
| :--- | :--- | :--- | :--- |
| **Reports (Create)** | 0.0167 req/sec | 15 | Approx 1 request every 60 seconds. |
| **Orders** | 0.5 req/sec | 30 | Varies by operation. |
| **Finances** | 0.5 req/sec | 30 | |
| **Catalog Items** | 2.0 req/sec | 20 | |

**Critical Note:** Rate limits are per *Selling Partner + Application* pair. If you hit a 429 error, you must implement an **exponential backoff** strategy.

---

## 5. Compliance & Data Handling

### PII (Personally Identifiable Information)
*   Includes: Buyer Name, Address, Phone Number.
*   **Strict Rule:** PII must be deleted **30 days after order delivery** unless required for tax/legal reasons.
*   **Security:** PII data stores must be encrypted with AES-256 and restricted from general employee access.

### Data Retention
*   **Non-PII Data:** Can be stored for up to 18 months unless longer retention is required by law.
*   **Amazon Review:** Amazon periodically audits developers. They may ask for screenshots of your database schema, encryption configurations, or MFA setup.

---

## 6. Practical Implementation

### Recommended Architecture: Sync vs. Real-time
1.  **Settlement/Financials:** Use **Reports API** on a schedule. Settlements are generated by Amazon; your system should poll `getReports` to find new ones.
2.  **Sales Dashboard:** Use `GET_SALES_AND_TRAFFIC_REPORT` (requested daily) for aggregate data, and **Orders API** (polled every 15-30 mins) for "live" daily totals.
3.  **FBA Planning:** Request inventory reports every 4-8 hours.

### Recommended Libraries
*   **Node.js:** [`amazon-sp-api`](https://www.npmjs.com/package/amazon-sp-api) - Very popular, handles SigV4 signing and token refreshing automatically.
*   **Python:** [`python-amazon-sp-api`](https://github.com/saleweaver/python-amazon-sp-api) - Well-maintained wrapper for Python/Django environments.

### Marketplace Handling
*   **Regions:** US (North America) and UK (Europe) are in different regions.
*   **Endpoints:**
    *   NA: `https://sellingpartnerapi-na.amazon.com`
    *   EU: `https://sellingpartnerapi-eu.amazon.com`
*   You can use the same LWA credentials for both, but you must specify the correct region in your API calls.
