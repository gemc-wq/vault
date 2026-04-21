# Etsy API v3 Reference - Shop Receipts

This document details the data structures for Etsy Shop Receipts (Orders) based on the Etsy Open API v3.

## Endpoints
- **Get Shop Receipts:** `GET /v3/application/shops/{shop_id}/receipts`
- **Get Shop Receipt:** `GET /v3/application/shops/{shop_id}/receipts/{receipt_id}`

## Data Structure: ShopReceipt
The following fields represent the main receipt/order object.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `receipt_id` | Integer | Numeric ID for the receipt. |
| `receipt_type` | Integer | The numeric type of receipt (0 for listing, etc.). |
| `seller_user_id` | Integer | Numeric ID for the seller. |
| `seller_email` | String | The email address of the seller. |
| `buyer_user_id` | Integer | Numeric ID for the buyer. |
| `buyer_email` | String | The email address of the buyer (may be null). |
| `name` | String | The name of the recipient in the shipping address. |
| `first_line` | String | First line of the shipping address. |
| `second_line` | String | Second line of the shipping address (optional). |
| `city` | String | City of the shipping address. |
| `state` | String | State/Province of the shipping address. |
| `zip` | String | Zip/Postal code of the shipping address. |
| `country_iso` | String | 2-letter ISO code for the country. |
| `formatted_address` | String | Full formatted shipping address string. |
| `payment_method` | String | Payment method (e.g., "cc", "pp"). |
| `payment_email` | String | Email associated with the payment. |
| `status` | String | Order status (e.g., "Paid", "Completed", "Open"). |
| `is_paid` | Boolean | Whether the receipt is paid. |
| `is_shipped` | Boolean | Whether the receipt is marked as shipped. |
| `create_timestamp` | Integer | Epoch timestamp when the receipt was created. |
| `created_timestamp` | Integer | Alias for `create_timestamp`. |
| `update_timestamp` | Integer | Epoch timestamp when the receipt was last updated. |
| `updated_timestamp` | Integer | Alias for `update_timestamp`. |
| `message_from_seller` | String | Message from the seller to the buyer. |
| `message_from_buyer` | String | Message from the buyer to the seller. |
| `message_from_payment`| String | Message from the payment processor. |
| `total_price` | Money | The subtotal price (lines only). |
| `total_shipping_cost` | Money | The total shipping cost. |
| `total_tax_cost` | Money | The total tax cost. |
| `total_vat_cost` | Money | The total VAT cost. |
| `discount_amt` | Money | Total discount amount applied. |
| `gift_wrap_price` | Money | Price for gift wrapping. |
| `grandtotal` | Money | The total price (price + shipping + tax + gift wrap - discounts). |
| `transactions` | Array[Transaction] | List of line items (see below). |
| `refunds` | Array[ReceiptRefund] | List of refunds (if applicable). |

### Money Object Structure
Financial fields use a specific "Money" object:
- `amount` (Integer): The value in the smallest currency unit (e.g., 1000 for $10.00).
- `divisor` (Integer): The divisor to get the decimal value (usually 100).
- `currency_code` (String): ISO currency code (e.g., "USD").

---

## Data Structure: Transaction (Line Items)
Included in the `transactions` array of a ShopReceipt.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `transaction_id` | Integer | Numeric ID for the transaction. |
| `title` | String | Title of the listing at the time of purchase. |
| `description` | String | Description of the listing. |
| `seller_user_id` | Integer | ID of the seller. |
| `buyer_user_id` | Integer | ID of the buyer. |
| `create_timestamp` | Integer | Epoch timestamp when the transaction was created. |
| `paid_timestamp` | Integer | Epoch timestamp when the transaction was paid. |
| `shipped_timestamp` | Integer | Epoch timestamp when the transaction was shipped. |
| `quantity` | Integer | Number of items purchased. |
| `listing_id` | Integer | ID of the linked listing. |
| `product_id` | Integer | ID of the specific product/variation. |
| `sku` | String | SKU of the product (if defined). |
| `price` | Money | Price per unit. |
| `is_digital` | Boolean | Whether the item is a digital download. |
| `transaction_type` | String | Type (e.g., "listing"). |

---

## Fees and Adjustments
Etsy API v3 does not include granular transaction fees (Etsy Payments fees, listing fees) directly in the Receipt response. These must typically be retrieved from the **Ledger Entry** or **Payment** endpoints:
- `GET /v3/application/shops/{shop_id}/payments`
- `GET /v3/application/shops/{shop_id}/ledger/entries`

## Refunds
Refunds are represented in the `refunds` array:
- `amount` (Money): Amount refunded.
- `created_timestamp` (Integer): When the refund occurred.
- `reason` (String): Reason for the refund.
