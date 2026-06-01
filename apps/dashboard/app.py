import streamlit as st
import pandas as pd
import plotly.express as px

import sys
import os

# =====================================================
# PROJECT PATH
# =====================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.append(PROJECT_ROOT)

from src.recommendation.recommender import (
    recommend_products_with_names
)

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
    "Data/processed/customer_segments_labeled.csv"
)

sales_df = pd.read_csv(
    "Data/processed/daily_business_sales.csv"
)

pred_df = pd.read_csv(
    "Data/processed/xgboost_predictions.csv"
)

pred_df["date"] = pd.to_datetime(
    pred_df["date"]
)

inventory_df = pd.read_csv(
    "Data/processed/inventory_report.csv"
)

inventory_intelligence_df = pd.read_csv(
    "Data/processed/inventory_intelligence.csv"
)

monthly_revenue_df = pd.read_csv(
    "Data/processed/monthly_revenue.csv"
)

country_revenue_df = pd.read_csv(
    "Data/processed/country_revenue.csv"
)

top_products_df = pd.read_csv(
    "Data/processed/top_products.csv"
)

weekday_sales_df = pd.read_csv(
    "Data/processed/weekday_sales.csv"
)

top_quantity_df = pd.read_csv(
    "Data/processed/top_quantity_products.csv"
)

orders_per_day_df = pd.read_csv(
    "Data/processed/orders_per_day.csv"
)



# =====================================================
# SIDEBAR
# =====================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Sales Analytics",
        "Product Analytics",
        "Customer Analytics",
        "Geographic Analytics",
        "Forecasting & AI",
        "Operations Dashboard",
        "Recommendations"
    ]
)

# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    st.title("NeuralRetail Dashboard")

    st.markdown(
        """
        NeuralRetail is an AI-powered retail analytics platform
        combining customer segmentation, demand forecasting,
        inventory optimization and recommendation systems.
        """
    )

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
        width="stretch"
    )

# =====================================================
# CUSTOMER Analytics
# =====================================================
elif page == "Customer Analytics":

    st.title("Customer Analytics")

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

    churn_df = segments_df.copy()

    churn_df["Churn"] = (
        churn_df["Recency"] > 90
    ).astype(int)

    active = (
        churn_df["Churn"] == 0
    ).sum()

    churned = (
        churn_df["Churn"] == 1
    ).sum()

    churn_rate = round(
        churned / len(churn_df) * 100,
        2
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Active Customers",
        active
    )

    col2.metric(
        "Churned Customers",
        churned
    )

    col3.metric(
        "Churn Rate",
        f"{churn_rate}%"
    )

    st.markdown("""
    ### Churn Definition

    A customer is considered churned if they have not made a purchase in the last 90 days.

    Best Model:
    - Logistic Regression

    Performance:
    - ROC-AUC: 0.737
    """)
# =====================================================
# FORECASTING
# =====================================================

elif page == "Forecasting & AI":

    st.title("Forecasting & AI")

    col1, col2 = st.columns(2)

    col1.metric(
        "Prophet MAPE",
        "5.98%"
    )

    col2.metric(
        "XGBoost MAPE",
        "4.21%"
    )

    fig = px.line(
        sales_df,
        x="date",
        y="sales",
        title="Historical Sales"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    fig2 = px.line(
        pred_df,
        x="date",
        y=["sales", "prediction"],
        title="Actual vs Predicted"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

# =====================================================
# Operations Dashboard
# =====================================================
elif page == "Operations Dashboard":

    st.title("Operations Dashboard")

    cols = st.columns(3)

    for i, (_, row) in enumerate(
        inventory_df.iterrows()
    ):

        cols[i % 3].metric(
            row["Metric"],
            round(row["Value"])
        )

    matrix_counts = (

        inventory_intelligence_df[
            "ABC_XYZ"
        ]

        .value_counts()

        .reset_index()
    )

    matrix_counts.columns = [
        "Class",
        "Count"
    ]

    fig = px.bar(

        matrix_counts,

        x="Class",

        y="Count",

        title="ABC-XYZ Inventory Matrix"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )
    
    st.subheader(
    "ABC-XYZ Inventory Strategy"
    )

    st.markdown(
    """
    ### Inventory Classification Guide

    - **AX** → High Revenue + Stable Demand
        - Critical inventory
        - Never allow stockouts

    - **AY** → High Revenue + Moderate Variability
        - Monitor regularly
        - Maintain buffer stock

    - **AZ** → High Revenue + Highly Variable Demand
        - High safety stock required
        - Frequent forecasting

    - **BX / BY / BZ**
        - Medium priority products
        - Periodic inventory review

    - **CX / CY**
        - Low revenue products
        - Minimize inventory carrying cost

    - **CZ**
        - Low Revenue + Highly Variable Demand
        - Potential dead stock candidates
        - Consider clearance or discontinuation
    """
    )


elif page == "Inventory Intelligence":

    st.title(
        " Inventory Intelligence"
    )

    matrix_counts = (

        inventory_intelligence_df[
            "ABC_XYZ"
        ]

        .value_counts()

        .reset_index()
    )

    matrix_counts.columns = [

        "Class",

        "Count"
    ]

    fig = px.bar(

        matrix_counts,

        x="Class",

        y="Count",

        title="ABC-XYZ Inventory Matrix"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.dataframe(
        matrix_counts
    )

# =====================================================
# RECOMMENDATIONS
# =====================================================

elif page == "Recommendations":

    st.title("Product Recommendations")

    product_id = st.text_input(
        "Enter Product ID"
    )

    if product_id:

        try:

            recommendations = (
                recommend_products_with_names(
                    product_id
                )
            )

            if len(recommendations) > 0:

                st.dataframe(
                    recommendations
                )

            else:

                st.warning(
                    "No recommendations found."
                )

        except Exception:

            st.error(
                "Invalid Product ID"
            )


# Sales Analytics
elif page == "Sales Analytics":

    st.title("Sales Analytics")

    total_revenue = monthly_revenue_df["Revenue"].sum()

    st.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )

    # Monthly Revenue
    fig = px.line(
        monthly_revenue_df,
        x="YearMonth",
        y="Revenue",
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(fig, width="stretch")

    # Revenue by Weekday
    fig = px.bar(
        weekday_sales_df,
        x="Weekday",
        y="Revenue",
        title="Revenue by Weekday"
    )

    st.plotly_chart(fig, width="stretch")

    # Daily Orders Trend
    fig = px.line(
        orders_per_day_df,
        x="Date",
        y="Orders",
        title="Daily Orders Trend"
    )

    st.plotly_chart(fig, width="stretch")

    st.subheader("Revenue Table")

    st.dataframe(monthly_revenue_df)


# Product Analytics

elif page == "Product Analytics":

    st.title("Product Analytics")

    # Top Revenue Products
    fig1 = px.bar(
        top_products_df,
        x="Revenue",
        y="Description",
        orientation="h",
        title="Top Products by Revenue"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Top Quantity Products
    fig2 = px.bar(
        top_quantity_df,
        x="Quantity",
        y="Description",
        orientation="h",
        title="Top Products by Quantity Sold"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.subheader(
        "Top Revenue Products Table"
    )

    st.dataframe(
        top_products_df,
        use_container_width=True
    )


# Geographic Analytics

elif page == "Geographic Analytics":

    st.title("Geographic Analytics")

    fig = px.bar(
        country_revenue_df,
        x="Revenue",
        y="Country",
        orientation="h",
        title="Revenue by Country"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        country_revenue_df,
        use_container_width=True
    )
# =====================================================
# FOOTER
# =====================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "NeuralRetail v1.0"
)

