# SP-API Application Checklist

Follow these steps to get API access for Ecell Global / Head Case Designs.

## Phase 1: Infrastructure Preparation
- [ ] **AWS Setup:** Create an AWS Account (if not already existing).
- [ ] **IAM User:** Create an IAM User specifically for SP-API.
    - [ ] Attach an inline policy with `execute-api:Invoke` permissions.
    - [ ] Save the **Access Key ID** and **Secret Access Key**.
    - [ ] Copy the **User ARN** (e.g., `arn:aws:iam::123456789012:user/sp-api-user`).
- [ ] **Security Review:** Ensure your internal systems meet the Data Protection Policy (DPP):
    - [ ] Database encryption at rest (AES-256).
    - [ ] MFA enabled for all developers/users accessing the data.
    - [ ] Documented Incident Response Plan.

## Phase 2: Developer Registration
- [ ] **Primary User Login:** Log in to Seller Central as the Primary User.
- [ ] **Developer Profile:** Submit the Developer Profile application.
    - [ ] Select Roles: *Brand Analytics, Amazon Fulfillment, Finance and Accounting, Inventory and Order Tracking, Product Listing*.
    - [ ] **Crucial:** If you need customer names/addresses for shipping, select *Direct-to-Consumer Shipping (Restricted)*. (Requires extra scrutiny).
- [ ] **Wait for Approval:** Monitor email for "Case" updates in Seller Central (5-10 days).

## Phase 3: App Registration & Authorization
- [ ] **Create App:** Once approved, go to "Develop Apps" > "Add New App".
    - [ ] API Type: Selling Partner API.
    - [ ] IAM ARN: Paste the User ARN from Phase 1.
- [ ] **Get LWA Credentials:** Record the **Client ID** and **Client Secret**.
- [ ] **Self-Authorization:**
    - [ ] Click "Authorize" in the Actions menu next to your app.
    - [ ] Click "Authorize" again on the consent page.
    - [ ] **Record the Refresh Token** immediately. This is permanent.

## Phase 4: Integration
- [ ] **Test Sandbox:** Run a test call to the Sandbox endpoint using the `amazon-sp-api` library.
- [ ] **Marketplace Mapping:** Confirm Marketplace IDs:
    - [ ] US: `ATVPDKIKX0DER`
    - [ ] UK: `A1F8UWY8V6S5L6`
- [ ] **Implement Sync Jobs:**
    - [ ] Job 1: Poll for new Settlement Reports (Finance).
    - [ ] Job 2: Request daily Sales & Traffic report.
    - [ ] Job 3: Sync live Order data every 15 mins.
- [ ] **PII Deletion Logic:** Implement a script to automatically scrub buyer names/addresses from your database after 30 days.
