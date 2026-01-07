# backend/models/pricing.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def price_optimization(df, product=None):
    df = df.copy()

    if product:
        df = df[df["product_name"] == product]

    if df.empty:
        return {"error": "No sales data available for the selected product."}

    # Need at least 3 unique prices for meaningful elasticity
    data = df.groupby("price")["units_sold"].sum().reset_index()
    if len(data) < 3:
        return {
            "error": "Insufficient price variation. Need sales at 3+ different prices for optimization.",
            "current_prices": data["price"].tolist()
        }

    X = data[["price"]].values
    y = data["units_sold"].values

    model = LinearRegression()
    model.fit(X, y)

    min_price = data["price"].min() * 0.8   # Expand range slightly
    max_price = data["price"].max() * 1.2
    price_range = np.linspace(min_price, max_price, 50)

    predicted_demand = model.predict(price_range.reshape(-1, 1))
    predicted_demand = np.maximum(predicted_demand, 0)

    revenue = price_range * predicted_demand
    best_idx = np.argmax(revenue)

    optimal_price = round(float(price_range[best_idx]), 2)
    max_revenue = round(float(revenue[best_idx]), 0)

    # Correct elasticity interpretation
    elasticity_coef = float(model.coef_[0])
    abs_elasticity = abs(elasticity_coef)

    if abs_elasticity > 1:
        elasticity_type = "Elastic → Customers are price-sensitive"
    elif abs_elasticity < 1:
        elasticity_type = "Inelastic → Customers less sensitive to price"
    else:
        elasticity_type = "Unit Elastic"

    curve = [
        {
            "price": round(float(p), 2),
            "demand": round(float(d), 1),
            "revenue": round(float(r), 0)
        }
        for p, d, r in zip(price_range, predicted_demand, revenue)
    ]

    return {
        "optimal_price": optimal_price,
        "expected_revenue": int(max_revenue),
        "price_elasticity": round(elasticity_coef, 3),
        "elasticity_type": elasticity_type,
        "optimal_point": {
            "price": optimal_price,
            "revenue": int(max_revenue)
        },
        "curve": curve
    }