import streamlit as st
from streamlit_app import run_query, FILTER_CLAUSE

st.header("Customer Profitability")
st.caption(
    "Identifies top-performing customers and highlights accounts that generate low or negative profit."
)

query = f"""
SELECT
    cp.customer_id,
    cp.total_orders,
    cp.total_revenue,
    cp.total_profit,
    cp.avg_profit_per_order,
    CASE
        WHEN cp.total_profit >= 2000 THEN 'Platinum'
        WHEN cp.total_profit >= 500 THEN 'Gold'
        WHEN cp.total_profit > 0 THEN 'Silver'
        ELSE 'At Risk'
    END AS customer_tier
FROM analytics.customer_profit_view cp
JOIN raw.orders o
    ON cp.customer_id = o.customer_id
{FILTER_CLAUSE}
ORDER BY cp.total_profit DESC;
"""

df = run_query(query)

# ------------------------------
# Top Customers
# ------------------------------
st.subheader("Top Customers by Profit")
st.dataframe(
    df.head(20),
    use_container_width=True
)

# ------------------------------
# At Risk Customers
# ------------------------------
st.subheader("At Risk Customers")
at_risk = df[df["customer_tier"] == "At Risk"]

if at_risk.empty:
    st.success("No unprofitable customers in the selected period.")
else:
    st.dataframe(
        at_risk.head(10),
        use_container_width=True
    )
