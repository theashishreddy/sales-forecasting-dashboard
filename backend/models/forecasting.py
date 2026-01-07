from prophet import Prophet
import pandas as pd

def prophet_forecast(df, periods=30):
    df = df.copy()

    # Convert date
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    # Aggregate daily sales
    daily = df.groupby("date")["units_sold"].sum().reset_index()
    daily.columns = ["ds", "y"]

    # Train model
    model = Prophet()
    model.fit(daily)

    # Future dates
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Actual data (historical only)
    actual = daily.copy()

    # Forecast with confidence intervals
    forecast_df = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]

    return actual, forecast_df
