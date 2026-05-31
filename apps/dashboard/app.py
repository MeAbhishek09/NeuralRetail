import streamlit as st
import pandas as pd
import plotly.express as px


import sys
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.append(PROJECT_ROOT)

from src.recommendation.recommender import recommend_products
# from src.recommendation.recommender import (
#     recommend_products
# )

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="NeuralRetail",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

segments_df = pd.read_csv(
    r"C:\Users\91991\Desktop\internships\AMDOX\data\processed\customer_segments_labeled.csv"
)

sales_df = pd.read_csv(
    r"C:\Users\91991\Desktop\internships\AMDOX\data\processed\daily_business_sales.csv"
)

sales_df["date"] = pd.to_datetime(
    sales_df["date"]
)

# =====================================================
# SIDEBAR
# =====================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Customer Intelligence",
        "Forecasting",
        "Inventory",
        "Recommendations"
    ]
)

# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    st.title("🛒 NeuralRetail Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Customers",
            segments_df["CustomerID"].nunique()
        )

    with col2:
        st.metric(
            "Avg Daily Demand",
            round(
                sales_df["sales"].mean()
            )
        )

    with col3:
        st.metric(
            "Best Forecast MAPE",
            "4.21%"
        )

    st.divider()

    fig = px.line(
        sales_df,
        x="date",
        y="sales",
        title="Business Sales Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# CUSTOMER INTELLIGENCE
# =====================================================

elif page == "Customer Intelligence":

    st.title("👥 Customer Intelligence")

    segment_counts = (
        segments_df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Segment",
        "Count"
    ]

    fig = px.pie(
        segment_counts,
        names="Segment",
        values="Count",
        title="Customer Segments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Segment Summary"
    )

    st.dataframe(
        segment_counts
    )

# =====================================================
# FORECASTING
# =====================================================

elif page == "Forecasting":

    st.title("📈 Forecasting")

    st.success(
        "Prophet MAPE : 5.98%"
    )

    st.success(
        "XGBoost MAPE : 4.21%"
    )

    fig = px.line(
        sales_df,
        x="date",
        y="sales",
        title="Historical Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# INVENTORY
# =====================================================

elif page == "Inventory":

    st.title("📦 Inventory Optimization")

    st.metric(
        "Safety Stock",
        "~31,900"
    )

    st.metric(
        "Reorder Point",
        "~273,000"
    )

    st.metric(
        "EOQ",
        "~15,860"
    )

    st.warning(
        "Inventory decisions are based on XGBoost demand forecasts."
    )




# Recommendations
elif page == "Recommendations":

    st.title("🎯 Product Recommendations")

    product_id = st.text_input(
        "Enter Product ID"
    )

    if product_id:

        recommendations = (
            recommend_products(
                product_id
            )
        )

        st.write(
            recommendations
        )