-- ==================================================
-- ANALYTICS TABLES
-- Business-ready, decision-support data
-- ==================================================
-- Purpose:
--   Stores transformed, analytics-ready data derived
--   from raw transactional tables.
--
-- Design philosophy:
--   - Encapsulate business logic once
--   - Optimize for dashboard consumption
--   - Avoid complex calculations in the BI layer
-- ==================================================

-- --------------------------------------------------
-- Order Profitability
-- --------------------------------------------------
-- Grain: One row per order
--
-- This table consolidates all revenue, cost, and profit
-- components at the order level. It serves as the
-- foundation for downstream customer and regional analysis.
CREATE TABLE IF NOT EXISTS analytics.order_profitability (
    order_id UUID PRIMARY KEY,
    customer_id UUID,
    region_id UUID,
    order_date DATE,

    -- Revenue and cost components
    gross_revenue NUMERIC(12,2),
    product_cost  NUMERIC(12,2),
    shipping_cost NUMERIC(12,2),
    discount_cost NUMERIC(12,2),

    -- Profitability metrics
    gross_profit NUMERIC(12,2),
    contribution_margin NUMERIC(12,2)
);

-- --------------------------------------------------
-- Customer Profitability
-- --------------------------------------------------
-- Grain: One row per customer
--
-- Aggregates order-level profitability to the customer level.
-- Used for customer segmentation, ranking, and lifetime value
-- analysis within the ProfitLens dashboard.
CREATE TABLE IF NOT EXISTS analytics.customer_profitability (
    customer_id UUID PRIMARY KEY,

    total_orders INT,
    total_revenue NUMERIC(14,2),
    total_profit NUMERIC(14,2),
    avg_profit_per_order NUMERIC(12,2)
);
