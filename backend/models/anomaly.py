import pandas as pd
import numpy as np

def detect_anomalies(df, product=None):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    # 🔑 FORCE product-wise detection
    if product:
        df = df[df["product_name"] == product]

    daily = df.groupby("date")["units_sold"].sum().reset_index()

    mean = daily["units_sold"].mean()
    std = daily["units_sold"].std()

    # Handle edge case
    if std == 0 or pd.isna(std):
        daily["z_score"] = 0
        daily["anomaly"] = False
    else:
        daily["z_score"] = (daily["units_sold"] - mean) / std
        daily["anomaly"] = abs(daily["z_score"]) > 1.5  # 🔑 LOWER THRESHOLD

    def severity(z):
        if abs(z) > 3:
            return "Critical"
        elif abs(z) > 2:
            return "Moderate"
        elif abs(z) > 1.5:
            return "Mild"
        return "Normal"

    daily["severity"] = daily["z_score"].apply(severity)

    def reason(z):
        if z > 0:
            return "Sudden demand spike"
        elif z < 0:
            return "Unexpected demand drop"
        return "Normal behavior"

    daily["reason"] = daily["z_score"].apply(reason)

    return daily


    # ---------- RESIDUALS ----------
    merged["residual"] = merged["y"] - merged["yhat"]

    mean = merged["residual"].mean()
    std = merged["residual"].std()

    merged["z_score"] = (merged["residual"] - mean) / std

    # ---------- ANOMALY RULE ----------
    merged["anomaly"] = merged["z_score"].abs() > 1.5

    # ---------- SEVERITY ----------
    def severity(z):
        if abs(z) >= 3:
            return "Critical"
        elif abs(z) >= 2:
            return "Moderate"
        elif abs(z) >= 1.5:
            return "Mild"
        return "Normal"

    merged["severity"] = merged["z_score"].apply(severity)

    # ---------- AI REASON ----------
    def reason(z):
        if z > 1.5:
            return "Sales significantly higher than forecast"
        elif z < -1.5:
            return "Sales significantly lower than forecast"
        return "Within expected range"

    merged["reason"] = merged["z_score"].apply(reason)

    # Rename for frontend compatibility
    merged.rename(columns={"y": "units_sold"}, inplace=True)

    return merged
