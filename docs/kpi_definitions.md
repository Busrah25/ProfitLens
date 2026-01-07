# KPI Definitions

This document defines the key metrics displayed in the ProfitLens dashboard.

---

## Total Revenue

Sum of all item-level revenue across orders.

Formula:
gross_revenue = item_price * quantity

---

## Total Profit

Total gross profit across all orders.

Formula:
gross_profit = gross_revenue - product_cost - shipping_cost - discount_cost

---

## Contribution Margin

Profitability as a percentage of revenue.

Formula:
contribution_margin = gross_profit / gross_revenue

---

## Active Customers

Count of unique customers with at least one order in the selected date range.

---

## Average Profit per Order

Average profit generated per order.

Formula:
avg_profit_per_order = total_profit / total_orders
