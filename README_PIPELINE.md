# NeuralRetail — Full Project Pipeline

# Project Overview

NeuralRetail is an enterprise AI-powered retail intelligence platform built using:

* Machine Learning
* Deep Learning
* Forecasting
* Customer Analytics
* MLOps
* APIs
* Dashboarding
* Deployment Pipelines

The system contains two major AI pipelines:

1. Customer Intelligence Pipeline
2. Demand Forecasting Pipeline

Later both pipelines merge into a single enterprise platform.

---

# Full Architecture

```text
                    NEURALRETAIL PLATFORM

┌───────────────────────────────────────────────────────┐
│                                                       │
│                    DATA SOURCES                       │
│                                                       │
│  ┌──────────────────┐     ┌────────────────────────┐  │
│  │   M5 Dataset     │     │ Online Retail II       │  │
│  │                  │     │                        │  │
│  │ sales_df         │     │ customer transactions │  │
│  │ calendar_df      │     │ invoices              │  │
│  │ price_df         │     │ product purchases     │  │
│  └──────────────────┘     └────────────────────────┘  │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

# Pipeline 1 — Customer Intelligence

Dataset Used:

* Online Retail II

Goal:

* Understand customer behavior
* Predict churn
* Segment customers
* Build recommendation systems

---

# Step 1 — Data Cleaning

Input:

```text
retail_df
```

Cleaning Steps:

* Remove duplicates
* Remove missing Customer IDs
* Remove negative quantities
* Remove invalid prices
* Convert InvoiceDate to datetime
* Create Revenue column

Output:

```text
customer_df
```

Saved File:

```text
data/processed/clean_online_retail.csv
```

---

# Step 2 — RFM Feature Engineering

Input:

```text
customer_df
```

Features Created:

| Feature   | Meaning                  |
| --------- | ------------------------ |
| Recency   | Days since last purchase |
| Frequency | Number of purchases      |
| Monetary  | Total customer spending  |

Output:

```text
rfm_df
```

Saved File:

```text
data/processed/rfm_features.csv
```

---

# Step 3 — Customer Segmentation

Input:

```text
rfm_df
```

Models:

* KMeans
* DBSCAN

Goal:

* Identify VIP customers
* Identify low-value customers
* Identify high churn-risk groups

Outputs:

* Customer segments
* Cluster labels

---

# Step 4 — Churn Prediction

Input:

```text
customer_df + rfm_df
```

Models:

* XGBoost
* LightGBM

Goal:

Predict probability of customer churn.

Example:

```text
Customer 1001 → 92% churn risk
```

Outputs:

* churn scores
* retention lists

---

# Step 5 — Recommendation System (Later Phase)

Datasets Used:

* Online Retail II
* RetailRocket (later)

Goal:

Recommend products to users.

Example:

```text
Users who bought shoes also bought socks
```

Models:

* Collaborative Filtering
* Matrix Factorization
* Embedding-based recommendation
* Deep Learning recommenders

Outputs:

* personalized recommendations
* product ranking
* recommendation APIs

---

# Customer Intelligence Pipeline Summary

```text
Online Retail II
        ↓
customer_df
        ↓
RFM Features
        ↓
├── Customer Segmentation
├── Churn Prediction
└── Recommendation System
```

---

# Pipeline 2 — Demand Forecasting

Dataset Used:

* M5 Forecasting Dataset

Files Used:

| File                       | Purpose         |
| -------------------------- | --------------- |
| sales_train_validation.csv | sales history   |
| calendar.csv               | holidays/events |
| sell_prices.csv            | product pricing |

---

# Step 1 — sales_df Transformation

Current Format:

```text
wide format
```

Target Format:

```text
long format
```

Transformation:

```python
pd.melt()
```

Output:

```text
melted_df
```

---

# Step 2 — Merge calendar_df

Adds:

* real dates
* holidays
* weekends
* SNAP events
* special events

Output:

```text
sales_calendar_df
```

---

# Step 3 — Merge price_df

Adds:

* pricing information
* weekly price changes
* revenue intelligence

Output:

```text
forecasting_df
```

This becomes the final forecasting dataset.

---

# Step 4 — Forecasting Feature Engineering

Features Created:

* lag features
* rolling means
* rolling standard deviation
* holiday flags
* weekday/month features
* seasonal indicators

---

# Step 5 — Forecasting Models

Phase 1:

* Prophet

Phase 2:

* LSTM
* Temporal Fusion Transformer (TFT)

Goals:

* daily sales forecasting
* future demand prediction
* seasonal forecasting

Example:

```text
Next week sales = 150 units
```

Outputs:

* sales forecasts
* confidence intervals

---

# Step 6 — Inventory Optimization

Uses:

* forecast predictions
* historical demand
* lead time assumptions

Calculations:

* EOQ
* Safety Stock
* Reorder Point

Outputs:

* reorder recommendations
* stockout alerts
* inventory risk analysis

---

# Demand Forecasting Pipeline Summary

```text
sales_df
calendar_df
price_df
        ↓
Data Merge
        ↓
Forecasting Features
        ↓
Forecasting Models
        ↓
Inventory Optimization
```

---

# Final Platform Merge

Both pipelines combine into:

```text
FastAPI Backend
        ↓
PostgreSQL Database
        ↓
Streamlit Dashboard
        ↓
MLflow + Airflow
        ↓
Cloud Deployment
```

---

# Dashboard Modules

The final Streamlit dashboard will contain:

1. Executive KPI Dashboard
2. Forecasting Dashboard
3. Customer Intelligence Dashboard
4. Churn Dashboard
5. Inventory Dashboard
6. Recommendation Dashboard

---

# APIs

FastAPI Endpoints:

```text
/predict/demand
/predict/churn
/recommend/products
/inventory/reorder
/segment/customer
```

---

# MLOps Components

Tools Used:

* MLflow
* Airflow
* Evidently AI
* Docker
* Kubernetes (later)

Capabilities:

* experiment tracking
* model registry
* automated retraining
* drift monitoring
* CI/CD deployment

---

# Current Progress

| Module                | Status      |
| --------------------- | ----------- |
| Project Structure     | ✅           |
| Dataset Download      | ✅           |
| Retail Cleaning       | ✅           |
| Revenue Feature       | ✅           |
| Clean Dataset Saved   | ✅           |
| RFM Features          | I✅          |
| Forecasting Pipeline  | ✅           |
| Dashboard             | ✅           |
| APIs                  | ✅           |
| Recommendation System | ✅           |

---

# Future Roadmap

Phase 1:

* RFM
* Segmentation
* Forecasting baseline

Phase 2:

* Churn prediction
* Streamlit dashboard
* FastAPI APIs

Phase 3:

* MLflow
* Airflow
* Docker deployment

Phase 4:

* Recommendation system
* RetailRocket integration
* Advanced deep learning recommenders

---

# Final Goal

Build a full enterprise-grade AI retail intelligence platform capable of:

* demand forecasting
* churn prediction
* customer segmentation
* inventory optimization
* personalized recommendations
* automated MLOps pipelines
