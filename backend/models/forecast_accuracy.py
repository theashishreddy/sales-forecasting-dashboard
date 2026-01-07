import numpy as np
import pandas as pd

def forecast_accuracy(actual_df, forecast_df):
    # align on dates that exist in both
    merged = pd.merge(
        actual_df, forecast_df, on="ds", how="inner"
    )

    y_true = merged["y"]
    y_pred = merged["yhat"]

    mape = (np.abs((y_true - y_pred) / y_true)).replace([np.inf, -np.inf], np.nan)
    mape = float(np.nanmean(mape) * 100)

    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

    return {
        "mape": round(mape, 2),
        "rmse": round(rmse, 2),
        "points_evaluated": int(len(merged))
    }
