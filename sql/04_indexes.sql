-- ==================================================
-- Performance Indexes
-- ==================================================
-- Purpose:
--   Improves query performance for analytics
--   and dashboard filtering.
--
-- Why this matters:
--   Indexes reduce latency and support
--   scalable dashboard usage.
-- ==================================================

-- Speed up joins and filters on orders
CREATE INDEX IF NOT EXISTS idx_orders_order_date
ON raw.orders(order_date);

CREATE INDEX IF NOT EXISTS idx_orders_customer
ON raw.orders(customer_id);

-- Improve aggregation performance on order items
CREATE INDEX IF NOT EXISTS idx_order_items_order
ON raw.order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product
ON raw.order_items(product_id);
