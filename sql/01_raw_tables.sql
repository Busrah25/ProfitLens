-- ==================================================
-- RAW TABLES
-- Source-like operational data
-- ==================================================
-- Purpose:
--   Stores untransformed, source-aligned data that
--   represents core business entities.
--
-- Design philosophy:
--   - Preserve source granularity
--   - Enforce referential integrity
--   - Avoid business logic at the raw layer
-- ==================================================

-- --------------------------------------------------
-- Customers
-- --------------------------------------------------
-- Represents unique customers and their acquisition context.
-- Used for cohort analysis, segmentation, and lifetime value modeling.
CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id           UUID PRIMARY KEY,
    first_order_date      DATE NOT NULL,
    acquisition_channel   TEXT,
    customer_segment      TEXT
);

-- --------------------------------------------------
-- Products
-- --------------------------------------------------
-- Master product catalog with pricing and cost attributes.
-- Supports margin analysis and product-level profitability.
CREATE TABLE IF NOT EXISTS raw.products (
    product_id    UUID PRIMARY KEY,
    category      TEXT NOT NULL,
    base_price    NUMERIC(10,2) NOT NULL,
    unit_cost     NUMERIC(10,2) NOT NULL,
    weight_class  TEXT
);

-- --------------------------------------------------
-- Regions
-- --------------------------------------------------
-- Geographic dimension table used for regional performance analysis.
CREATE TABLE IF NOT EXISTS raw.regions (
    region_id    UUID PRIMARY KEY,
    region_name  TEXT NOT NULL
);

-- --------------------------------------------------
-- Orders
-- --------------------------------------------------
-- Order header table capturing transactional metadata.
-- One row per order.
CREATE TABLE IF NOT EXISTS raw.orders (
    order_id         UUID PRIMARY KEY,
    customer_id      UUID NOT NULL,
    region_id        UUID NOT NULL,
    order_date       DATE NOT NULL,
    shipping_speed   TEXT,
    discount_rate    NUMERIC(4,2),

    -- Link order to customer
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES raw.customers(customer_id),

    -- Link order to geographic region
    CONSTRAINT fk_orders_region
        FOREIGN KEY (region_id)
        REFERENCES raw.regions(region_id)
);

-- --------------------------------------------------
-- Order Items
-- --------------------------------------------------
-- Line-item level transaction details.
-- Enables granular revenue, cost, and margin calculations.
CREATE TABLE IF NOT EXISTS raw.order_items (
    order_item_id  UUID PRIMARY KEY,
    order_id       UUID NOT NULL,
    product_id     UUID NOT NULL,
    quantity       INT NOT NULL,
    item_price     NUMERIC(10,2) NOT NULL,

    -- Link line items to parent order
    CONSTRAINT fk_items_order
        FOREIGN KEY (order_id)
        REFERENCES raw.orders(order_id),

    -- Link line items to product catalog
    CONSTRAINT fk_items_product
        FOREIGN KEY (product_id)
        REFERENCES raw.products(product_id)
);
