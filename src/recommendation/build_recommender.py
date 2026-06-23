import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv(
    "\data\processed\clean_online_retail.csv"
)

product_counts = df["StockCode"].value_counts()

valid_products = product_counts[
    product_counts >= 10
].index

df = df[
    df["StockCode"].isin(valid_products)
]

customer_item_matrix = pd.pivot_table(
    df,
    index="Customer ID",
    columns="StockCode",
    values="Quantity",
    aggfunc="sum",
    fill_value=0
)

customer_item_matrix = (
    customer_item_matrix > 0
).astype(int)

item_similarity = cosine_similarity(
    customer_item_matrix.T
)

similarity_df = pd.DataFrame(
    item_similarity,
    index=customer_item_matrix.columns,
    columns=customer_item_matrix.columns
)

product_map = (
    df[
        ["StockCode", "Description"]
    ]
    .drop_duplicates()
)

joblib.dump(
    similarity_df,
    "\models\recommendation\item_similarity.pkl"
)

joblib.dump(
    product_map,
    "\models\recommendation\product_map.pkl"
)

print("Recommendation model saved.")
