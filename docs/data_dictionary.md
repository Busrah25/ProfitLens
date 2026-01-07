# Data Dictionary

This document describes the structure and meaning of core fields used across the ProfitLens data model.

---

## raw.customers

| Column | Description |
|------|------------|
| customer_id | Unique customer identifier |
| first_order_date | Date of first purchase |
| acquisition_channel | How the customer was acquired |
| customer_segment | Business segment classification |

---

## raw.products

| Column | Description |
|------|------------|
| product_id | Unique product identifier |
| category | Product category |
| base_price | List price of product |
| unit_cost | Cost per unit |
| weight_class | Shipping weight category |

---

## raw.orders

| Column | Description |
|------|------------|
| order_id | Unique order identifier |
| customer_id | Customer placing the order |
| region_id | Geographic region |
| order_date | Date of order |
| shipping_speed | Shipping tier |
| discount_rate | Discount applied to order |

---

## raw.order_items

| Column | Description |
|------|------------|
| order_item_id | Line item identifier |
| order_id | Parent order |
| product_id | Purchased product |
| quantity | Units purchased |
| item_price | Price per unit |

---

## analytics.order_profitability

| Column | Description |
|------|------------|
| order_id | Order identifier |
| gross_revenue | Total revenue per order |
| product_cost | Cost of products sold |
| shipping_cost | Shipping cost |
| discount_cost | Discount cost |
| gross_profit | Order-level profit |
| contribution_margin | Profit before overhead |

---

## analytics.customer_profitability

| Column | Description |
|------|------------|
| customer_id | Customer identifier |
| total_orders | Number of orders |
| total_revenue | Total revenue |
| total_profit | Total profit |
| avg_profit_per_order | Average profit per order |
