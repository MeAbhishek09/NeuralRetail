import mlflow

# EXPERIMENT


mlflow.set_experiment(
    "NeuralRetail Forecasting"
)

# TRACK RUN

with mlflow.start_run():

    # Model Information

    mlflow.log_param(
        "model",
        "XGBoost"
    )

    mlflow.log_param(
        "n_estimators",
        500
    )

    mlflow.log_param(
        "learning_rate",
        0.05
    )

    mlflow.log_param(
        "max_depth",
        6
    )

    mlflow.log_param(
        "subsample",
        0.8
    )

    mlflow.log_param(
        "colsample_bytree",
        0.8
    )

    # Evaluation Metrics

    mlflow.log_metric(
        "MAPE",
        4.21
    )

    mlflow.log_metric(
        "MAE",
        1898.93
    )

    mlflow.log_metric(
        "RMSE",
        2532.51
    )

print(
    "XGBoost experiment logged successfully"
)