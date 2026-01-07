import numpy as np

def summarize_forecast(forecast_df):
    df = forecast_df.copy()

    start = df["yhat"].iloc[0]
    end = df["yhat"].iloc[-1]
    peak = df.loc[df["yhat"].idxmax()]
    low = df.loc[df["yhat"].idxmin()]

    growth_percent = round(((end - start) / start) * 100, 2)

    # Trend
    if growth_percent > 5:
        trend = "upward"
    elif growth_percent < -5:
        trend = "downward"
    else:
        trend = "stable"

    # Volatility
    volatility = np.std(df["yhat"])
    avg = np.mean(df["yhat"])
    volatility_ratio = volatility / avg

    if volatility_ratio > 0.25:
        risk = "high"
    elif volatility_ratio > 0.15:
        risk = "moderate"
    else:
        risk = "low"

    # Business recommendation
    if trend == "upward" and risk != "high":
        recommendation = "Increase inventory and maintain current pricing."
    elif trend == "downward":
        recommendation = "Reduce inventory risk and review pricing strategy."
    elif risk == "high":
        recommendation = "Avoid aggressive promotions and monitor demand closely."
    else:
        recommendation = "Maintain current operations and monitor performance."

    return {
        "trend": trend,
        "growth_percent": growth_percent,
        "peak_date": str(peak["ds"].date()),
        "peak_value": round(peak["yhat"], 2),
        "low_date": str(low["ds"].date()),
        "risk_level": risk,
        "recommendation": recommendation
    }
