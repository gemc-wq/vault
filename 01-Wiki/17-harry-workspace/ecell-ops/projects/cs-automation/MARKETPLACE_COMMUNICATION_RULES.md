# Marketplace Seller Communication Rules (2025-2026)

This document outlines the exact rules and policies for seller-to-buyer communication on Amazon and eBay. These rules are critical for maintaining account health and avoiding suspensions.

---

## 1. Amazon Seller Communication Rules

Amazon operates on a "Strict Necessity" principle. Any communication that is not essential to fulfill an order or provide customer service is generally prohibited.

### Allowed vs. Banned Content
*   **Permitted Messages:**
    *   Resolving order fulfillment issues.
    *   Requesting missing information to complete an order.
    *   Sending invoices.
    *   Scheduling delivery for large/bulky items.
    *   Requesting a product review or seller feedback (only once per order).
*   **Banned Content (Immediate Suspension Risk):**
    *   **Marketing/Promotions:** Offering discounts, coupons, or free gifts for future purchases.
    *   **External Links:** Links to your own website, social media, or any non-Amazon site.
    *   **Incentives:** Asking for a positive review in exchange for a refund, gift, or discount.
    *   **Persuasive Language:** Trying to influence the buyer's review or asking them to contact you before leaving a negative review.
    *   **Off-Platform Directing:** Asking the buyer to contact you via email or phone outside the Buyer-Seller Messaging (BSM) system.
    *   **Excessive Communication:** Sending multiple requests for reviews (Amazon already sends automated requests).

### External Link Policies
*   **Permitted:** Only links necessary for order fulfillment (e.g., carrier tracking pages) or links explicitly allowed by Amazon (e.g., help pages within Amazon).
*   **Suspension Trigger:** Including a URL to an external storefront or a "contact us" form on your own website. Amazon’s automated filters scan for strings like `.com`, `www.`, and `http` to flag accounts for review.

### Response Timeframes (SLA)
*   **Requirement:** Responses must be sent within **24 hours**.
*   **Timing:** This clock runs 24/7/365, including weekends and holidays.
*   **Metrics:** Failure to meet the 24-hour SLA negatively impacts your Contact Response Time (CRT) metric. While CRT doesn't always lead to immediate suspension, it severely damages Seller Performance ratings.

### Messaging API (SP-API)
*   **Model:** Messaging API v1.
*   **Functionality:** Sellers can fetch a list of "Available Message Types" for a specific order. You cannot send arbitrary text for all message types; some require pre-defined templates or specific parameters.
*   **Throttling:** Strict rate limits apply based on the seller's volume. Exceeding limits results in `429 Too Many Requests`.

### Recent Policy Changes (2025-2026)
*   **Enhanced AI Scanning:** Amazon has deployed more sophisticated LLM-based scanners to detect "veiled" incentives and persuasive language that older keyword-based filters missed.
*   **No Emojis/GIFs:** Messaging guidelines have tightened around professional formatting. Emojis and unnecessary images are increasingly flagged as unprofessional/promotional.

---

## 2. eBay Seller Communication Rules

eBay is generally more flexible than Amazon but strictly enforces "Off-Platform" rules to prevent fee circumvention.

### Allowed vs. Banned Content
*   **Permitted:**
    *   General product inquiries before purchase.
    *   Post-sale coordination (shipping, tracking, returns).
    *   Sharing personal contact info **only after** a transaction is active.
*   **Banned:**
    *   **Fee Circumvention:** Proposing to sell the item outside of eBay to avoid fees.
    *   **Spam:** Sending marketing emails to past buyers without their explicit consent.
    *   **Harassment:** Aggressive tone or repeated messages after a buyer has asked to stop.

### Link Policies
*   **Restricted:** You cannot include links to external websites, social media, or other marketplaces.
*   **Allowed:** Links to other eBay pages (e.g., your eBay Store, other eBay listings) are generally permitted.

### Response Timeframes
*   **Requirement:** No hard "24-hour" rule like Amazon for all messages, but **Top Rated Sellers (TRS)** are expected to respond to inquiries within 1 business day.
*   **Resolution SLA:** For "Item Not Received" or "Return" requests, sellers have **3 business days** to respond before eBay can step in.

### Messaging API
*   **Models:** Legacy Trading API (`AddMemberMessageAAQToPartner`) is still widely used, though eBay is moving toward more modern RESTful APIs.
*   **Features:** Allows sending member-to-member messages linked to a specific Item ID or Transaction ID.

---

## 3. Rules for Both Platforms

### Automated & AI Responses
*   **Amazon:** Permitted, but the seller is **100% responsible** for the content. If the AI generates a link or a promotional offer, the seller's account is suspended, not the software provider.
*   **eBay:** Permitted, but must comply with the "Member-to-Member Contact" policy. Automated "checkout agents" or "buy-for-me" bots are strictly prohibited by the 2025 Robot & Agent Policy.
*   **Disclosure:** While not strictly mandated in a "legal disclaimer" sense for every message, Amazon KDP rules (2025) and growing marketplace trends suggest that transparent disclosure is a "best practice" to avoid being flagged as a bot/spam.

### Contact Outside the Platform
*   **Zero Tolerance:** Both platforms strictly prohibit "transaction diversion."
*   **Suspension Triggers:**
    *   "Contact me at [email] for a discount."
    *   "Call us at [phone] to pay via credit card."
    *   "Visit our website [URL] for more items."

### Best Practices for AI Customer Service
1.  **Content Filtering:** Every AI-generated response must pass through a regex/LLM filter to strip out URLs, email addresses, and phone numbers.
2.  **Sentiment Guardrails:** Ensure the AI never uses "persuasive" or "incentive" based language (e.g., "If you like this, please give us 5 stars for a $5 coupon").
3.  **Human-in-the-Loop:** High-risk queries (e.g., negative reviews, account threats) should be escalated to a human.
4.  **Template Adherence:** On Amazon, prefer using the SP-API "Get Eligible Message Types" and only sending the required information.

---
*Last Updated: 2026-02-11*
*Source: Official Seller Central Documentation & eBay Policy Pages*
