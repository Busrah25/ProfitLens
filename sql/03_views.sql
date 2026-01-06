-- =========================================
-- ANALYTICS VIEWS
-- =========================================

CREATE OR REPLACE VIEW analytics.order_profit_view AS
SELECT
    o.order_id,
    o.customer_id,
    o.region_id,
    o.order_date,

    SUM(oi.item_price * oi.quantity) AS gross_revenue,

    SUM(p.unit_cost * oi.quantity) AS product_cost,

    -- simple shipping model (realistic assumption)
    CASE
        WHEN o.shipping_speed = 'express' THEN 15.00
        ELSE 7.00
    END AS shipping_cost,

    COALESCE(
        SUM(oi.item_price * oi.quantity) * o.discount_rate,
        0
    ) AS discount_cost,

    -- gross profit
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
JOIN raw.order_items oi ON o.order_id = oi.order_id
JOIN raw.products p ON oi.product_id = p.product_id
GROUP BY
    o.order_id,
    o.customer_id,
    o.region_id,
    o.order_date,
    o.shipping_speed,
    o.discount_rate;
    
CREATE OR REPLACE VIEW analytics.customer_profit_view AS
SELECT
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(gross_revenue) AS total_revenue,
    SUM(gross_profit) AS total_profit,
    AVG(gross_profit) AS avg_profit_per_order
FROM analytics.order_profit_view
GROUP BY customer_id;
