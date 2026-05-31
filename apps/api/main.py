from fastapi import FastAPI
import pandas as pd


from src.recommendation.recommender import (
    recommend_products
)

# ==========================================
# CREATE APP
# ==========================================

app = FastAPI(
    title="NeuralRetail API"
)

# ==========================================
# LOAD DATA
# ==========================================

segments_df = pd.read_csv(
    r"C:\Users\91991\Desktop\internships\AMDOX\data\processed\customer_segments_labeled.csv"
)

# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "NeuralRetail API Running"
    }

# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# ==========================================
# SEGMENTS
# ==========================================

@app.get("/segments")
def segments():

    return (
        segments_df["Segment"]
        .value_counts()
        .to_dict()
    )

# ==========================================
# FORECAST
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
# INVENTORY
# ==========================================

@app.get("/inventory")
def inventory():

    return {

        "safety_stock": 31900,

        "reorder_point": 273000,

        "eoq": 15860
    }



@app.get("/recommend/{product_id}")
def recommend(
    product_id: str
):

    recommendations = recommend_products(
        product_id
    )

    return {
        "product": product_id,
        "recommendations": recommendations
    }