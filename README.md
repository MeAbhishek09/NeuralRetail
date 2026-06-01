# 🛒 NeuralRetail: AI-Powered Retail Intelligence Platform

## Overview

NeuralRetail is an end-to-end AI-powered retail analytics platform that combines customer intelligence, demand forecasting, inventory optimization, and recommendation systems into a unified dashboard and API.

The platform helps retailers:

* Understand customer behavior
* Forecast future demand
* Optimize inventory decisions
* Generate product recommendations
* Visualize business insights through dashboards

---

## Project Setup

### Backend Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Prophet
* FastAPI

### Dashboard & Visualization

* Streamlit
* Plotly
* Matplotlib
* Seaborn

### Experiment Tracking

* MLflow

### Development Environment

* Python 3.10
* Jupyter Notebook
* VS Code

---

## Datasets Used

### 1. Online Retail II Dataset

The Online Retail II dataset contains transactional records from a UK-based online retail company.

Used for:

* Customer Analytics
* RFM Analysis
* Customer Segmentation
* Customer Churn Prediction
* Product Performance Analysis
* Geographic Sales Analysis
* Recommendation System
* Revenue and Sales Analytics

Key Features:

* Invoice Information
* Customer Information
* Product Information
* Quantity Purchased
* Unit Price
* Revenue
* Country

---

### 2. M5 Forecasting Dataset

The M5 Forecasting dataset contains historical sales data from Walmart stores.

Used for:

* Demand Forecasting
* Business-Level Sales Prediction
* Inventory Optimization
* Safety Stock Calculation
* Reorder Point (ROP)
* Economic Order Quantity (EOQ)
* Inventory Intelligence
* ABC Analysis
* XYZ Analysis
* ABC-XYZ Inventory Matrix

Key Features:

* Daily Sales
* Calendar Information
* Event Data
* SNAP Indicators
* Product Demand History

---


## Project Architecture

### Customer Intelligence Pipeline

Online Retail II

↓

Data Cleaning

↓

RFM Feature Engineering

↓

Customer Segmentation (K-Means)

↓

Dashboard

---

### Demand Intelligence Pipeline

M5 Dataset

↓

Business-Level Aggregation

↓

Feature Engineering

↓

Prophet Forecasting

↓

XGBoost Forecasting

↓

Inventory Optimization

↓

Dashboard

---

### Recommendation Engine

Online Retail II

↓

Customer-Item Matrix

↓

Item-Based Collaborative Filtering

↓

Cosine Similarity

↓

Product Recommendations

---

## Features Implemented

### Customer Intelligence

* Data Cleaning
* Revenue Feature Creation
* RFM Analysis
* K-Means Customer Segmentation

### Demand Intelligence

* Prophet Forecasting
* XGBoost Forecasting
* Lag Features
* Rolling Window Features
* Event Features

### Inventory Optimization

* Safety Stock
* Reorder Point
* Economic Order Quantity (EOQ)

### Recommendation System

* Customer-Item Matrix
* Cosine Similarity
* Item-Based Collaborative Filtering

### Dashboard

* Executive Overview
* Customer Intelligence
* Forecasting Analytics
* Inventory Insights
* Recommendations

### API

* FastAPI Backend
* Forecast Endpoints
* Inventory Endpoints
* Recommendation Endpoints

---

## Results

### Forecasting Performance

| Model   | MAE     | RMSE    | MAPE  |
| ------- | ------- | ------- | ----- |
| Prophet | 2637.53 | 3361.51 | 5.98% |
| XGBoost | 1898.93 | 2532.51 | 4.21% |

### Best Model

XGBoost achieved the best forecasting performance with:

MAPE = 4.21%

Approximately 29.6% improvement over Prophet.

---

## Recommendation System Statistics

* Customers: 4312
* Products: 3111
* Similarity Metric: Cosine Similarity

---

## Technology Stack

### Machine Learning

* Scikit-Learn
* XGBoost
* Prophet

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly
* Streamlit

### Backend

* FastAPI

### Model Persistence

* Joblib

---

## Project Structure

AMDOX/

├── apps/

│   ├── dashboard/

│   └── api/

├── data/

│   ├── raw/

│   └── processed/

├── models/

│   ├── forecasting/

│   └── recommendation/

├── notebooks/

├── reports/

├── src/

│   ├── mlflow_tracking/

│   └── recommendation/

└── README.md

---

## Future Enhancements

* MLflow Experiment Tracking
* Docker Deployment
* Category-Level Forecasting
* Product-Level Forecasting
* Deep Learning Recommendation Models
* Cloud Deployment

---

## Author

Abhishek

B.Tech Computer Science & Engineering

Central University of Jharkhand
