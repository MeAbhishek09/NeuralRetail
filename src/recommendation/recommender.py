import joblib

similarity_df = joblib.load(
    r"C:\Users\91991\Desktop\internships\AMDOX\models\recommendation\item_similarity.pkl"
)

product_map = joblib.load(
    r"C:\Users\91991\Desktop\internships\AMDOX\models\recommendation\product_map.pkl"
)


def recommend_products(stock_code, top_n=5):

    if stock_code not in similarity_df.columns:
        return []

    recommendations = (
        similarity_df[stock_code]
        .sort_values(ascending=False)
        .iloc[1:top_n+1]
        .index
        .tolist()
    )

    return recommendations


def recommend_products_with_names(stock_code, top_n=5):

    recommendations = recommend_products(
        stock_code,
        top_n
    )

    results = product_map[
        product_map["StockCode"].isin(
            recommendations
        )
    ]

    return results[
        ["StockCode", "Description"]
    ]