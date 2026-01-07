import streamlit as st
from streamlit_app import run_query, FILTER_CLAUSE

# --------------------------------------------------
# Regional Performance Page
# Compares financial performance across geographic regions
# --------------------------------------------------

# Page title and business context
st.header("Regional Performance")
st.caption(
    "Compares revenue, profit, and margin across regions to identify high-performing and underperforming markets."
)

# --------------------------------------------------
# SQL Query
# Aggregates revenue and profit by region
# Uses the global date filter from the sidebar (FILTER_CLAUSE)
# --------------------------------------------------
query = f"""
SELECT
    r.region_name,
    SUM(op.gross_revenue) AS revenue,
    SUM(op.gross_profit) AS profit
FROM analytics.order_profit_view op
JOIN raw.regions r
    ON op.region_id = r.region_id
JOIN raw.orders o
    ON op.order_id = o.order_id
{FILTER_CLAUSE}
GROUP BY r.region_name
ORDER BY profit DESC;
"""

# Execute query and load results into a DataFrame
df = run_query(query)

# --------------------------------------------------
# Margin Calculation
# Defensive logic avoids division errors and missing values
# --------------------------------------------------
df["margin_pct"] = (df["profit"] / df["revenue"]) * 100
df = df.fillna(0)

# --------------------------------------------------
# Regional Ranking Table
# Highlights regions by profitability for quick comparison
# --------------------------------------------------
st.subheader("Regional Profit Ranking")
st.dataframe(
    df,
    use_container_width=True
)

# --------------------------------------------------
# Revenue vs Profit Visualization
# Shows volume versus profitability by region
# --------------------------------------------------
st.subheader("Revenue vs Profit by Region")
st.bar_chart(
    df.set_index("region_name")[["revenue", "profit"]],
    use_container_width=True
)

# --------------------------------------------------
# Contribution Margin Visualization
# Indicates operational efficiency across regions
# --------------------------------------------------
st.subheader("Contribution Margin by Region (%)")
st.bar_chart(
    df.set_index("region_name")[["margin_pct"]],
    use_container_width=True
)
