from fastapi import FastAPI
import pandas as pd

from src.recommendation.recommender import (
    recommend_products
)

# ==========================================
# CREATE API
# ==========================================

app = FastAPI(

    title="NeuralRetail API",

    description=(
        "Customer Segmentation, "
        "Demand Forecasting, "
        "Inventory Optimization and "
        "Recommendation API"
    ),

    version="1.0.0"
)

# ==========================================
# LOAD DATA
# ==========================================

# Load customer segments

segments_df = pd.read_csv(
    "data/processed/customer_segments_labeled.csv"
)

churn_df = pd.read_csv(
    "data/processed/customer_segments_labeled.csv"
)

inventory_intelligence = pd.read_csv(
    "data/processed/inventory_intelligence.csv"
)

churn_df["Churn"] = (
    churn_df["Recency"] > 90
).astype(int)

# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {

        "message": "NeuralRetail API Running"
    }

# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {

        "status": "healthy"
    }

# ==========================================
# CUSTOMER SEGMENTS
# ==========================================

@app.get("/segments")
def segments():

    return {

        "segment_distribution": (

            segments_df["Segment"]
            .value_counts()
            .to_dict()
        )
    }

# ==========================================
# FORECAST METRICS
# ==========================================

@app.get("/forecast")
def forecast():

    return {

        "model": "XGBoost",

        "mape": 4.21,

        "mae": 1898.93,

        "rmse": 2532.51
    }

# ==========================================
# INVENTORY RESULTS
# ==========================================

@app.get("/inventory")
def inventory():

    return {

        "safety_stock": 31900,

        "reorder_point": 273000,

        "eoq": 15860
    }

# ==========================================
# PRODUCT RECOMMENDATIONS
# ==========================================

@app.get("/recommend/{product_id}")
def recommend(
    product_id: str
):

    try:

        recommendations = (
            recommend_products(
                product_id
            )
        )

        return {

            "product": product_id,

            "recommendations": recommendations
        }

    except Exception:

        return {

            "error": (
                f"Product {product_id} not found"
            )
        }

# ==========================================
# API INFORMATION
# ==========================================

@app.get("/info")
def info():

    return {

        "project": "NeuralRetail",

        "modules": [

            "Customer Segmentation",

            "Demand Forecasting",

            "Inventory Optimization",

            "Recommendation System"
        ]
    }


@app.get("/churn")
def churn():

    active = (
        churn_df["Churn"] == 0
    ).sum()

    churned = (
        churn_df["Churn"] == 1
    ).sum()

    churn_rate = round(

        churned

        / len(churn_df)

        * 100,

        2
    )

    return {

        "active_customers": int(active),

        "churned_customers": int(churned),

        "churn_rate": churn_rate,

        "best_model": "Logistic Regression",

        "roc_auc": 0.737
    }


@app.get("/inventory-intelligence")
def inventory_intelligence_api():

    return (

        inventory_intelligence[
            "ABC_XYZ"
        ]

        .value_counts()

        .to_dict()
    )