# BigCommerce REST Management API Reference - Orders

This document details the data structures for BigCommerce Orders based on the REST Management API (V2).

## Endpoints
- **Get All Orders:** `GET /v2/orders`
- **Get an Order:** `GET /v2/orders/{order_id}`
- **Get Order Products:** `GET /v2/orders/{order_id}/products`
- **Get Order Shipping Addresses:** `GET /v2/orders/{order_id}/shipping_addresses`
- **Get Order Coupons:** `GET /v2/orders/{order_id}/coupons`

## Data Structure: Order
The main order object returned by `/v2/orders`. Many financial fields are strings representing floats.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Numeric ID of the order. |
| `customer_id` | Integer | ID of the customer. |
| `date_created` | String | RFC-2822 date created. |
| `date_modified` | String | RFC-2822 date last modified. |
| `date_shipped` | String | RFC-2822 date shipped. |
| `status` | String | Human-readable status (e.g., "Awaiting Fulfillment"). |
| `status_id` | Integer | Numeric ID of the status. |
| `subtotal_ex_tax` | String | Subtotal excluding tax. |
| `subtotal_inc_tax` | String | Subtotal including tax. |
| `total_tax` | String | Total tax amount. |
| `total_ex_tax` | String | Grand total excluding tax. |
| `total_inc_tax` | String | Grand total including tax. |
| `payment_status` | String | Status of payment (e.g., "paid", "partially refunded"). |
| `payment_method` | String | Name of the payment method. |
| `currency_code` | String | ISO currency code for display. |
| `default_currency_code`| String | ISO currency code for transaction. |
| `shipping_cost_ex_tax` | String | Shipping cost excluding tax. |
| `shipping_cost_inc_tax` | String | Shipping cost including tax. |
| `handling_cost_ex_tax` | String | Handling cost excluding tax. |
| `coupon_discount` | String | Total discount from coupons. |
| `discount_amount` | String | Total discount amount (manual + coupon). |
| `store_credit_amount` | String | Amount paid with store credit. |
| `gift_certificate_amount`| String | Amount paid with gift certificates. |
| `billing_address` | Object | Billing address (see sub-structure). |
| `order_source` | String | Origin of order (e.g., "www", "manual", "external"). |
| `external_id` | String | ID in external system (e.g., Amazon Order ID). |
| `customer_message` | String | Message left by customer. |
| `staff_notes` | String | Internal notes from staff. |

---

## Data Structure: Order Product (Line Items)
Returned by `/v2/orders/{order_id}/products`.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | ID of this product line item. |
| `order_id` | Integer | ID of the parent order. |
| `product_id` | Integer | ID of the catalog product. |
| `sku` | String | Product SKU. |
| `name` | String | Product name (customer-facing). |
| `type` | String | "physical", "digital", or "giftcertificate". |
| `base_price` | String | Per-unit base price. |
| `price_ex_tax` | String | Per-unit price excluding tax. |
| `price_inc_tax` | String | Per-unit price including tax. |
| `price_tax` | String | Per-unit tax amount. |
| `quantity` | Integer | Quantity ordered. |
| `total_ex_tax` | String | Line total excluding tax. |
| `total_inc_tax` | String | Line total including tax. |
| `total_tax` | String | Line total tax. |
| `weight` | Number | Product weight. |
| `is_refunded` | Boolean | Whether the item has been refunded. |
| `quantity_refunded` | Number | Quantity refunded. |
| `applied_discounts` | Array[Object] | Discounts applied to this item. |

---

## Data Structure: Shipping Address
Returned by `/v2/orders/{order_id}/shipping_addresses`.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | ID of the shipping address. |
| `first_name` | String | Recipient first name. |
| `last_name` | String | Recipient last name. |
| `company` | String | Recipient company. |
| `street_1` | String | Street address 1. |
| `street_2` | String | Street address 2. |
| `city` | String | City. |
| `state` | String | State/Province. |
| `zip` | String | Zip/Postal code. |
| `country` | String | Country name. |
| `country_iso2` | String | 2-letter ISO code. |
| `phone` | String | Telephone number. |
| `email` | String | Email address. |
| `shipping_method` | String | Name of shipping method selected. |
| `base_cost` | String | Base shipping cost for this address. |

---

## Fees, Refunds, and Coupons
- **Coupons:** Accessible via `/v2/orders/{order_id}/coupons`. Includes `code`, `amount`, and `type` (per_item_discount, per_total_discount, etc.).
- **Refunds:** BigCommerce uses a separate Payments/Refunds API. The Order object provides `payment_status`, but detailed refund events are usually under `/v3/orders/{order_id}/payment_actions/refunds`.
- **Fees:** Granular payment gateway fees (like Stripe fees) are generally not in the REST Order response and must be retrieved from the payment gateway directly.
