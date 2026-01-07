import matplotlib.pyplot as plt
import io
from io import BytesIO

def generate_forecast_chart(actual_df, forecast_df):
    buffer = io.BytesIO()

    plt.figure(figsize=(6, 3))
    plt.plot(actual_df["ds"], actual_df["y"], label="Actual", marker="o")
    plt.plot(forecast_df["ds"], forecast_df["yhat"], label="Forecast", linestyle="--")

    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.title("Sales Forecast")
    plt.legend()
    plt.tight_layout()

    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    return buffer




def generate_anomaly_chart(df):
    fig, ax = plt.subplots(figsize=(8, 4))

    ax.plot(df["date"], df["units_sold"], label="Sales", color="blue")

    anomalies = df[df["anomaly"]]
    ax.scatter(
        anomalies["date"],
        anomalies["units_sold"],
        color="red",
        label="Anomaly",
        zorder=5
    )

    ax.set_title("Sales Anomaly Detection")
    ax.legend()
    ax.grid(True)

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return buf

