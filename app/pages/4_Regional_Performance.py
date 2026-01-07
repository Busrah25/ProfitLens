import streamlit as st
from streamlit_app import run_query, FILTER_CLAUSE

st.header("Regional Performance")
st.caption(
    "Compares revenue, profit, and margin across regions to identify high-performing and underperforming markets."
)

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

df = run_query(query)

# Defensive calculations
df["margin_pct"] = (df["profit"] / df["revenue"]) * 100
df = df.fillna(0)

# ------------------------------
# KPI View
# ------------------------------
st.subheader("Regional Profit Ranking")
st.dataframe(
    df,
    use_container_width=True
)

# ------------------------------
# Visualization
# ------------------------------
st.subheader("Revenue vs Profit by Region")
st.bar_chart(
    df.set_index("region_name")[["revenue", "profit"]],
    use_container_width=True
)

st.subheader("Contribution Margin by Region (%)")
st.bar_chart(
    df.set_index("region_name")[["margin_pct"]],
    use_container_width=True
)
