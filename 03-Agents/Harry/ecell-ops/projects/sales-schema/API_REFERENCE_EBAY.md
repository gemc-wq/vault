# eBay API Order Data Structure Reference

This document provides a comprehensive reference for the eBay **Fulfillment API** (`getOrder` endpoint), which is the modern standard for order management. It includes field names, data types, and specific details on how fees, refunds, and analytics-relevant data are represented.

## 1. Core Order Structure (Top-Level)
The `Order` object is the root container for all order data.

| Field Name | Data Type | Description |
|:---|:---|:---|
| `orderId` | `string` | Unique identifier for the eBay order. |
| `legacyOrderId` | `string` | (If applicable) The order ID from the legacy Trading API. |
| `salesRecordReference` | `string` | The Selling Manager sales record number (often used in UI). |
| `sellerId` | `string` | Unique eBay user ID of the seller. |
| `creationDate` | `string` | ISO 8601 timestamp of order creation. |
| `lastModifiedDate` | `string` | ISO 8601 timestamp of the last update to the order. |
| `orderFulfillmentStatus` | `string` | `NOT_STARTED`, `IN_PROGRESS`, `FULFILLED`, or `CANCELLED`. |
| `orderPaymentStatus` | `string` | `PAID`, `PENDING`, `FAILED`. |
| `buyer` | `Buyer` | Container for buyer info (User ID, Registration Address). |
| `buyerCheckoutNotes` | `string` | Comments left by the buyer during checkout. |
| `pricingSummary` | `PricingSummary` | Summary of cumulative costs (subtotal, shipping, tax, discounts). |
| `paymentSummary` | `PaymentSummary` | Details on payments received and refunds issued. |
| `cancelStatus` | `CancelStatus` | Details on cancellation requests and status. |
| `lineItems` | `LineItem[]` | Array of individual items in the order. |
| `fulfillmentStartInstructions` | `Fulfillment[]` | Shipping/pickup instructions (address, carrier, service). |
| `totalMarketplaceFee` | `Amount` | **Analytics Key**: Total fees accrued for this order (deducted from payout). |
| `totalFeeBasisAmount` | `Amount` | The base amount used to calculate Final Value Fees. |

---

## 2. Line Item Details (`lineItems`)
Each entry in the `lineItems` array represents a specific product/variant purchased.

| Field Name | Data Type | Description |
|:---|:---|:---|
| `lineItemId` | `string` | Unique identifier for the order line item. |
| `legacyItemId` | `string` | The listing ID (standard eBay Item ID). |
| `sku` | `string` | Seller-defined Stock-Keeping Unit. |
| `title` | `string` | Product title at the time of purchase. |
| `quantity` | `integer` | Number of units purchased. |
| `soldFormat` | `string` | `FIXED_PRICE` or `AUCTION`. |
| `lineItemCost` | `Amount` | Price per unit × quantity (before discounts). |
| `discountedLineItemCost`| `Amount` | Cost after line-level promotions. |
| `deliveryCost` | `DeliveryCost` | Shipping, handling, and import charges for this line. |
| `total` | `Amount` | Total for this line (Item + Tax + Shipping - Discounts). |
| `lineItemFulfillmentStatus`| `string` | `FULFILLED`, `IN_PROGRESS`, etc. |
| `variationAspects` | `NameValuePair[]`| For multi-variation listings (e.g., Color: Red, Size: XL). |
| `listingMarketplaceId` | `string` | The eBay site where it was listed (e.g., `EBAY_US`). |

---

## 3. Financial Representation (Fees & Refunds)

### Fees
eBay fees are primarily found in two places:
1.  **Order Level:** `totalMarketplaceFee` represents the total amount deducted from the seller's payout for that specific order.
2.  **Order Level:** `totalFeeBasisAmount` shows what the fee calculation was based on (usually Price + Shipping).
3.  **Taxes:** `ebayCollectAndRemitTax` (boolean) and `lineItems.ebayCollectAndRemitTaxes` indicate taxes eBay handles directly (Situs/Marketplace Facilitator taxes).

### Refunds
Refunds are tracked within the `paymentSummary` and individual `lineItems`.
-   **`paymentSummary.refunds[]`**: An array of refund objects.
    -   `refundId`: Unique ID for the refund.
    -   `amount`: The monetary value returned.
    -   `refundDate`: ISO 8601 timestamp.
    -   `refundStatus`: `PENDING`, `SUCCESSFUL`, `FAILED`.
-   **`lineItems[].refunds[]`**: Specific refunds associated with a single line item.

### Pricing Summary Breakdown (`pricingSummary`)
| Field | Description |
|:---|:---|
| `priceSubtotal` | Sum of all line item prices (pre-discount). |
| `priceDiscount` | Total order-level discounts (negative value). |
| `deliveryCost` | Total shipping cost before discounts. |
| `deliveryDiscount` | Shipping discounts (negative value). |
| `tax` | Total tax amount. |
| `total` | The "Grand Total" paid by the buyer. |

---

## 4. Analytics-Relevant Fields
To build a universal sales database, prioritize these fields for reporting:

1.  **Gross Sales:** `pricingSummary.priceSubtotal`
2.  **Net Sales:** `pricingSummary.total` minus `totalMarketplaceFee` and `tax`.
3.  **Buyer Geography:** `buyer.taxAddress.countryCode` and `fulfillmentStartInstructions.shippingStep.shipTo.contactAddress.countryCode`.
4.  **Order Velocity:** `creationDate` vs `paymentSummary.payments.paymentDate` (time to pay) vs `lastModifiedDate`.
5.  **SKU Performance:** Grouping by `lineItems.sku`.
6.  **Channel Attribution:** `lineItems.listingMarketplaceId` (identifies which eBay site drove the sale).
7.  **Promotion Efficacy:** `lineItems.appliedPromotions` (details on which marketing campaigns were active).

---

## Data Types Note
-   **`Amount` Object**: Most monetary fields use this structure:
    -   `value`: `string` (e.g., "19.99")
    -   `currency`: `string` (3-letter ISO code, e.g., "USD")
-   **`string` (Timestamps)**: All dates are ISO 8601 strings (UTC).
-   **`Enums`**: Status fields (Fulfillment, Payment, Refund) use specific string-based enumerations defined in the eBay documentation.

---
**References:**
- [eBay Fulfillment API - getOrder](https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrder)
- [eBay Fulfillment API - Order Type](https://developer.ebay.com/api-docs/sell/fulfillment/types/sel:Order)
