# Business Assumptions

This document outlines the key assumptions used in ProfitLens to model realistic business behavior.

These assumptions are intentionally simplified while remaining defensible and explainable.

---

## Pricing and Revenue

- Item revenue is calculated as:
  - item_price * quantity
- Base product price is assumed to be stable for the analysis period
- No dynamic pricing or promotions beyond discounts

---

## Costs

### Product Cost
- Product cost is derived from unit_cost in the product catalog
- Assumes cost is constant per unit

### Shipping Cost
- Flat shipping cost model
- Express shipping incurs higher cost than standard shipping
- Shipping cost applied at the order level

### Discount Cost
- Discount rate applied at the order level
- Discount cost calculated as a percentage of gross revenue

---

## Profitability

- Gross profit is calculated as:
  - gross_revenue
  - minus product_cost
  - minus shipping_cost
  - minus discount_cost

- Contribution margin represents profitability before overhead and fixed costs

---

## Data Scope

- All data is synthetic and used for demonstration purposes
- No external data sources are connected
- The project is designed to be reproducible and deterministic
