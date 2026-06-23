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
# LOAD RETAIL DATA
# =====================================================

retail_df = pd.read_csv(
    "Data/processed/clean_online_retail.csv"
)

retail_df["InvoiceDate"] = pd.to_datetime(
    retail_df["InvoiceDate"]
)

retail_df["Year"] = (
    retail_df["InvoiceDate"].dt.year
)

# =====================================================
# GLOBAL FILTERS
# =====================================================

st.sidebar.header(
    "Dashboard Filters"
)

country_filter = st.sidebar.selectbox(

    "Country",

    ["All"]

    +

    sorted(
        retail_df["Country"]
        .dropna()
        .unique()
        .tolist()
    )
)

year_filter = st.sidebar.selectbox(

    "Year",

    ["All"]

    +

    sorted(
        retail_df["Year"]
        .unique()
        .tolist()
    )
)

segment_filter = st.sidebar.selectbox(

    "Customer Segment",

    ["All"]

    +

    sorted(
        segments_df["Segment"]
        .unique()
        .tolist()
    )
)
# =====================================================
# APPLY FILTERS
# =====================================================

filtered_retail = retail_df.copy()

if country_filter != "All":

    filtered_retail = filtered_retail[

        filtered_retail["Country"]

        == country_filter
    ]

if year_filter != "All":

    filtered_retail = filtered_retail[

        filtered_retail["Year"]

        == year_filter
    ]
    
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

    st.title("🛒 NeuralRetail Dashboard")

    st.markdown(
        """
        NeuralRetail is an AI-powered retail analytics platform
        combining customer segmentation, demand forecasting,
        inventory optimization and recommendation systems.
        """
    )

    # ==========================================
    # KPI CALCULATIONS
    # ==========================================

    total_revenue = (
        filtered_retail["Revenue"]
        .sum()
    )

    total_customers = (
        filtered_retail["Customer ID"]
        .nunique()
    )

    total_orders = (
        filtered_retail["Invoice"]
        .nunique()
    )
    
    total_products = (
        filtered_retail["StockCode"]
        .nunique()
    )
    
    total_customers = (
        filtered_retail["Customer ID"]
        .nunique()
    )
    
    total_orders = (
        filtered_retail["Invoice"]
        .nunique()
    )

    avg_daily_demand = round(
        sales_df["sales"].mean()
    )

    churn_df = segments_df.copy()

    churn_df["Churn"] = (
        churn_df["Recency"] > 90
    ).astype(int)

    churn_rate = round(

        churn_df["Churn"]

        .mean()

        * 100,

        2
    )

    # ==========================================
    # ROW 1
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "💰 Total Revenue",
            f"${total_revenue:,.0f}"
        )

    with col2:

        st.metric(
            "👥 Customers",
            f"{total_customers:,}"
        )

    with col3:

        st.metric(
            "📦 Products",
            f"{total_products:,}"
        )

    # ==========================================
    # ROW 2
    # ==========================================

    col4, col5, col6 = st.columns(3)

    with col4:

        st.metric(
            "🧾 Orders",
            f"{total_orders:,}"
        )

    with col5:

        st.metric(
            "📈 Avg Daily Demand",
            avg_daily_demand
        )

    with col6:

        st.metric(
            "🔄 Churn Rate",
            f"{churn_rate}%"
        )

    # ==========================================
    # FORECAST KPI
    # ==========================================

    st.metric(
        "🤖 Best Forecast MAPE",
        "4.21%"
    )

    st.divider()

    # ==========================================
    # SALES TREND
    # ==========================================

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

    # ==========================================
    # MONTHLY REVENUE
    # ==========================================

    fig2 = px.line(

        monthly_revenue_df,

        x="YearMonth",

        y="Revenue",

        title="Monthly Revenue Trend"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    # ==========================================
    # EXPORT EXECUTIVE SUMMARY
    # ==========================================
    
    st.subheader(
        "📥 Export Executive Summary"
    )
    
    summary_df = pd.DataFrame({
    
        "Metric": [
    
            "Total Revenue",
    
            "Customers",
    
            "Products",
    
            "Orders",
    
            "Average Daily Demand",
    
            "Churn Rate (%)",
    
            "Best Forecast MAPE (%)"
        ],
    
        "Value": [
    
            total_revenue,
    
            total_customers,
    
            total_products,
    
            total_orders,
    
            avg_daily_demand,
    
            churn_rate,
    
            4.21
        ]
    })
    
    st.dataframe(
        summary_df,
        use_container_width=True
    )
    
    st.download_button(
    
        label="📄 Download Executive Summary CSV",
    
        data=summary_df.to_csv(index=False),
    
        file_name="executive_summary.csv",
    
        mime="text/csv"
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

# =====================================================
# RECOMMENDATIONS
# =====================================================

elif page == "Recommendations":

    st.title("🎯 Product Recommendation Engine")

    st.markdown(
        """
        Discover similar products using item-based
        collaborative filtering and cosine similarity.
        """
    )

    # ==========================================
    # TRENDING PRODUCTS
    # ==========================================

    st.subheader(
        "🔥 Top Selling Products"
    )

    trending_products = (

        retail_df

        .groupby(
            "Description"
        )["Revenue"]

        .sum()

        .sort_values(
            ascending=False
        )

        .head(10)

        .reset_index()
    )

    st.dataframe(
        trending_products,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # PRODUCT SELECTION
    # ==========================================

    product_options = (

        retail_df[
            ["StockCode", "Description"]
        ]

        .drop_duplicates()

        .dropna()

        .sort_values(
            "Description"
        )
    )

    selected_product = st.selectbox(

        "Select Product",

        product_options["Description"]
    )

    product_id = (

        product_options[

            product_options[
                "Description"
            ]

            == selected_product
        ]

        ["StockCode"]

        .iloc[0]
    )

    st.info(
        f"""
        Product Name: {selected_product}

        Product ID: {product_id}
        """
    )

    st.divider()

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================

    try:

        recommendations = (
            recommend_products_with_names(
                str(product_id)
            )
        )

        st.subheader(
            "🛍 Recommended Products"
        )

        if len(recommendations) > 0:

            st.dataframe(
                recommendations,
                use_container_width=True
            )

            st.success(
                """
                These products are frequently
                purchased together or exhibit
                similar purchasing behavior.

                Useful for cross-selling and
                upselling opportunities.
                """
            )

        else:

            st.warning(
                "No recommendations found."
            )

    except Exception as e:

        st.error(
            f"Recommendation Error: {e}"
        )

        

# =====================================================
# SALES ANALYTICS
# =====================================================

elif page == "Sales Analytics":

    st.title("📈 Sales Analytics")

    # ==========================================
    # KPI SECTION
    # ==========================================

    total_revenue = (
        monthly_revenue_df["Revenue"]
        .sum()
    )

    total_orders = (
        orders_per_day_df["Orders"]
        .sum()
    )

    avg_monthly_revenue = (
        monthly_revenue_df["Revenue"]
        .mean()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "💰 Total Revenue",
            f"${total_revenue:,.0f}"
        )

    with col2:

        st.metric(
            "🧾 Total Orders",
            f"{total_orders:,.0f}"
        )

    with col3:

        st.metric(
            "📊 Avg Monthly Revenue",
            f"${avg_monthly_revenue:,.0f}"
        )

    st.divider()

    # ==========================================
    # MONTHLY REVENUE TREND
    # ==========================================

    st.subheader(
        "Monthly Revenue Trend"
    )

    fig = px.line(

        monthly_revenue_df,

        x="YearMonth",

        y="Revenue",

        markers=True,

        title="Monthly Revenue Trend"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ==========================================
    # REVENUE BY WEEKDAY
    # ==========================================

    st.subheader(
        "Revenue by Weekday"
    )

    fig = px.bar(

        weekday_sales_df,

        x="Weekday",

        y="Revenue",

        title="Revenue by Weekday"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ==========================================
    # DAILY ORDERS TREND
    # ==========================================

    st.subheader(
        "Daily Orders Trend"
    )

    fig = px.line(

        orders_per_day_df,

        x="Date",

        y="Orders",

        title="Daily Orders Trend"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # ==========================================
    # REVENUE TABLE
    # ==========================================

    st.subheader(
        "Monthly Revenue Data"
    )

    st.dataframe(
        monthly_revenue_df,
        use_container_width=True
    )

    # ==========================================
    # BUSINESS INSIGHTS
    # ==========================================

    best_month = (

        monthly_revenue_df

        .sort_values(
            "Revenue",
            ascending=False
        )

        .iloc[0]
    )

    st.success(
        f"""
        Business Insight:

        Highest Revenue Month:
        {best_month['YearMonth']}

        Revenue:
        ${best_month['Revenue']:,.0f}
        """
    )

# =====================================================
# PRODUCT ANALYTICS
# =====================================================

elif page == "Product Analytics":

    st.title("🏆 Product Analytics")

    # ==========================================
    # KPI SECTION
    # ==========================================

    total_products = (
        retail_df["StockCode"]
        .nunique()
    )

    top_product = (
        top_products_df
        .iloc[0]["Description"]
    )

    top_product_revenue = (
        top_products_df
        .iloc[0]["Revenue"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📦 Products",
            total_products
        )

    with col2:

        st.metric(
            "🏆 Top Product",
            top_product[:20]
        )

    with col3:

        st.metric(
            "💰 Top Product Revenue",
            f"${top_product_revenue:,.0f}"
        )

    st.divider()

    # ==========================================
    # TOP PRODUCTS BY REVENUE
    # ==========================================

    st.subheader(
        "Top Products by Revenue"
    )

    fig1 = px.bar(

        top_products_df,

        x="Revenue",

        y="Description",

        orientation="h",

        title="Top Products by Revenue"
    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )

    # ==========================================
    # TOP PRODUCTS BY QUANTITY
    # ==========================================

    st.subheader(
        "Top Products by Quantity Sold"
    )

    fig2 = px.bar(

        top_quantity_df,

        x="Quantity",

        y="Description",

        orientation="h",

        title="Top Products by Quantity Sold"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    # ==========================================
    # PRODUCT TABLE
    # ==========================================

    st.subheader(
        "Top Revenue Products"
    )

    st.dataframe(
        top_products_df,
        use_container_width=True
    )

    # ==========================================
    # BUSINESS INSIGHT
    # ==========================================

    st.success(
        f"""
        Best Performing Product:

        {top_product}

        Revenue Generated:
        ${top_product_revenue:,.0f}
        """
    )


# Geographic Analytics
elif page == "Geographic Analytics":

    st.title("🌍 Geographic Analytics")

    total_countries = (
        country_revenue_df["Country"]
        .nunique()
    )

    top_country = (
        country_revenue_df
        .iloc[0]["Country"]
    )

    top_country_revenue = (
        country_revenue_df
        .iloc[0]["Revenue"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Countries",
        total_countries
    )

    col2.metric(
        "Top Country",
        top_country
    )

    col3.metric(
        "Revenue",
        f"${top_country_revenue:,.0f}"
    )

    st.divider()

    fig = px.bar(
        country_revenue_df,
        x="Revenue",
        y="Country",
        orientation="h",
        title="Revenue by Country"
    )

    st.plotly_chart(
        fig,
        width="stretch"
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
    """
    ### 🛒 NeuralRetail

    **Datasets Used**

    📦 Online Retail II
    - Customer Analytics
    - Segmentation
    - Churn Prediction
    - Recommendations

    📈 M5 Forecasting
    - Demand Forecasting
    - Inventory Optimization

    **Version:** v1.0
    """
)