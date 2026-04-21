# API Reference: Amazon Selling Partner (SP) - Orders & Financials

This document provides the technical schema for Amazon SP-API endpoints required for sales analytics and universal database design.

## 1. Core Endpoints

| Endpoint | Operation | Description |
|----------|-----------|-------------|
| `/orders/v0/orders` | `getOrders` | Returns a list of orders (header-level info). |
| `/orders/v0/orders/{orderId}` | `getOrder` | Returns specific order details. |
| `/orders/v0/orders/{orderId}/orderItems` | `getOrderItems` | Returns item-level details (SKU, quantity, price). |
| `/finances/v0/orders/{orderId}/financialEvents` | `listFinancialEventsByOrderId` | Returns exact fees, commissions, and taxes. |

---

## 2. Order Header Schema (`getOrders`)

**Root Object:** `Order`

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `AmazonOrderId` | `string` | Amazon-defined ID (3-7-7 format). |
| `SellerOrderId` | `string` | Seller-defined internal ID. |
| `PurchaseDate` | `string (ISO 8601)` | Timestamp when the order was placed. |
| `LastUpdateDate` | `string (ISO 8601)` | Timestamp of last modification. |
| `OrderStatus` | `enum` | `Pending`, `Unshipped`, `PartiallyShipped`, `Shipped`, `Canceled`, `Unfulfillable`, `InvoiceUnconfirmed`. |
| `FulfillmentChannel` | `enum` | `AFN` (FBA) or `MFN` (FBM). |
| `SalesChannel` | `string` | Sales channel (e.g., `Amazon.com`). |
| `ShipServiceLevel` | `string` | Shipping method (e.g., `Standard`). |
| `OrderTotal` | `Money` | Object containing `CurrencyCode` and `Amount`. |
| `NumberOfItemsShipped` | `integer` | Count of units shipped. |
| `NumberOfItemsUnshipped` | `integer` | Count of units awaiting shipment. |
| `MarketplaceId` | `string` | Obfuscated Marketplace ID (see Marketplaces section). |
| `IsBusinessOrder` | `boolean` | `true` if buyer is a verified business. |
| `IsPrime` | `boolean` | `true` if it is an Amazon Prime order. |
| `IsReplacementOrder` | `boolean` | `true` if this order replaces a previous one. |
| `ShippingAddress` | `Address` | Object (Name, City, CountryCode, PostalCode, State). |

---

## 3. Order Item Schema (`getOrderItems`)

**Root Object:** `OrderItem`

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `ASIN` | `string` | Amazon Standard Identification Number. |
| `SellerSKU` | `string` | Seller's stock keeping unit. |
| `OrderItemId` | `string` | Unique identifier for the item in the order. |
| `Title` | `string` | Product title. |
| `QuantityOrdered` | `integer` | Number of units ordered. |
| `QuantityShipped` | `integer` | Number of units shipped. |
| `ItemPrice` | `Money` | Total price for the items (excluding tax). |
| `ItemTax` | `Money` | Total tax on the items. |
| `ShippingPrice` | `Money` | Shipping charges for this item. |
| `ShippingTax` | `Money` | Tax on shipping charges. |
| `PromotionDiscount` | `Money` | Total discount from promotions. |
| `TaxCollection` | `Object` | Details if Amazon collects tax (`MarketplaceFacilitator`). |
| `ConditionId` | `string` | Item condition (e.g., `New`, `Used`). |
| `ConditionSubtypeId` | `string` | Sub-condition (e.g., `Mint`, `VeryGood`). |

---

## 4. Financial Schema (`listFinancialEventsByOrderId`)

This endpoint is critical for **Actual Net Sales** and **Fees**. The `OrderItems` list in the Financials API includes `FinancialEvents` like `ShipmentEvent`.

### Fee & Amount Fields
| Field Path | Data Type | Key Fee Types |
|------------|-----------|---------------|
| `ItemChargeList` | `Array<ChargeComponent>` | `Principal`, `ShippingCharge`, `Tax`, `GiftWrap`. |
| `ItemFeeList` | `Array<FeeComponent>` | `FBAPerUnitFulfillmentFee`, `Commission`, `FixedClosingFee`. |
| `PromotionList` | `Array<Promotion>` | `PromotionAmount`, `PromotionType`. |

---

## 5. Currency & Amounts Structure

All monetary values use the `Money` object:
```json
{
  "CurrencyCode": "USD",
  "Amount": "25.99"
}
```
*   **CurrencyCode:** 3-letter ISO code (e.g., USD, GBP, EUR, JPY).
*   **Amount:** String representation of a decimal value (avoids float precision issues).

---

## 6. Amazon Marketplace Identifiers

| Region | Country | Marketplace ID | Country Code |
|--------|---------|----------------|--------------|
| NA | USA | `ATVPDKIKX0DER` | `US` |
| NA | Canada | `A2EUQ1WTGCTBG2`| `CA` |
| EU | UK | `A1F83G8C2ARO7P`| `UK` / `GB` |
| EU | Germany | `A1PA6795UKMFR9`| `DE` |
| EU | France | `A13V1IB3VIYZZH`| `FR` |
| EU | Italy | `APJ6JRA9NG5V4` | `IT` |
| EU | Spain | `A1RKKUPIHCS9HS`| `ES` |
| FE | Japan | `A1VC38T7YXB528`| `JP` |
| FE | Australia| `A39IBJ37TRP1C6`| `AU` |

---

## 7. Fields for Sales Analytics

1.  **Net Revenue Calculation:**
    *   `Net Revenue = Principal (ItemPrice) - Commission - FBAPerUnitFulfillmentFee`.
2.  **Refunds & Cancellations:**
    *   `OrderStatus = 'Canceled'`: Order was canceled before shipping.
    *   `RefundEvent` (from Finances API): Indicates a processed refund for a previously shipped order.
3.  **Fulfillment Channel:**
    *   `AFN`: Amazon Fulfilled. Use to isolate FBA fees.
    *   `MFN`: Merchant Fulfilled. Use to calculate shipping costs manually if not via Buy Shipping.
4.  **Promotions:**
    *   `PromotionDiscount`: Critical for understanding "Gross vs Net" price.
5.  **Marketplace Tracking:**
    *   `MarketplaceId`: Map this to specific countries to handle multi-currency conversion and VAT reporting.
