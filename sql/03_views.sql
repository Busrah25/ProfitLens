-- ==================================================
-- ANALYTICS VIEWS
-- ==================================================
-- Purpose:
--   Defines reusable, business-logic views that power
--   dashboards and downstream analytics.
--
-- Why views:
--   - Centralize profit logic
--   - Ensure consistency across reports
--   - Keep application-layer queries simple
-- ==================================================

-- --------------------------------------------------
-- Order Profit View
-- --------------------------------------------------
-- Grain: One row per order
--
-- Calculates revenue, cost components, and profit
-- at the order level using transactional line-item data.
-- This view serves as the foundation for all profitability
-- analysis in ProfitLens.
CREATE OR REPLACE VIEW analytics.order_profit_view AS
SELECT
    o.order_id,
    o.customer_id,
    o.region_id,
    o.order_date,

    -- Total revenue from all items in the order
    SUM(oi.item_price * oi.quantity) AS gross_revenue,

    -- Total product cost based on unit cost and quantity
    SUM(p.unit_cost * oi.quantity) AS product_cost,

    -- Shipping cost model
    -- Assumes flat shipping fees by delivery speed
    CASE
        WHEN o.shipping_speed = 'express' THEN 15.00
        ELSE 7.00
    END AS shipping_cost,

    -- Discount cost applied at the order level
    -- COALESCE ensures null-safe calculations
    COALESCE(
        SUM(oi.item_price * oi.quantity) * o.discount_rate,
        0
    ) AS discount_cost,

    -- Gross profit calculation
    -- Revenue minus product, shipping, and discount costs
    SUM(oi.item_price * oi.quantity)
      - SUM(p.unit_cost * oi.quantity)
      - CASE
            WHEN o.shipping_speed = 'express' THEN 15.00
            ELSE 7.00
        END
      - COALESCE(
            SUM(oi.item_price * oi.quantity) * o.discount_rate,
            0
        ) AS gross_profit

FROM raw.orders o
JOIN raw.order_items oi
    ON o.order_id = oi.order_id
JOIN raw.products p
    ON oi.product_id = p.product_id
GROUP BY
    o.order_id,
    o.customer_id,
    o.region_id,
    o.order_date,
    o.shipping_speed,
    o.discount_rate;

-- --------------------------------------------------
-- Customer Profit View
-- --------------------------------------------------
-- Grain: One row per customer
--
-- Aggregates order-level profitability to the customer level.
-- Used for customer segmentation, ranking, and lifetime
-- profitability analysis.
CREATE OR REPLACE VIEW analytics.customer_profit_view AS
SELECT
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(gross_revenue) AS total_revenue,
    SUM(gross_profit) AS total_profit,
    AVG(gross_profit) AS avg_profit_per_order
FROM analytics.order_profit_view
GROUP BY customer_id;
