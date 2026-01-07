-- ==================================================
-- ProfitLens Database Schemas
-- ==================================================
-- Purpose:
--   Creates logical schemas to separate raw ingested
--   data from analytics-ready models.
--
-- Why this matters:
--   Schema separation improves maintainability,
--   governance, and prevents accidental overwrites.
-- ==================================================

-- Raw schema holds untransformed source data
CREATE SCHEMA IF NOT EXISTS raw;

-- Analytics schema holds transformed, business-ready tables and views
CREATE SCHEMA IF NOT EXISTS analytics;
