import os
import pandas as pd
from backend.models.forecast_summary import summarize_forecast
from backend.models.gpt_summary import generate_gpt_summary
from flask import send_file
from backend.utils.pdf_report import generate_forecast_pdf
from backend.utils.chart_generator import generate_forecast_chart
from backend.models.forecast_accuracy import forecast_accuracy
from flask import Flask, jsonify, request, send_file
from backend.utils.bundle_export import create_zip_bundle

from flask import Flask
from backend.utils.geo_pdf import generate_geo_pdf


from backend.utils.chart_generator import generate_anomaly_chart
from backend.utils.anomaly_pdf import generate_anomaly_pdf
from backend.utils.geo_pdf import generate_geo_pdf

from flask import Flask, render_template, request, jsonify, redirect
from backend.models.forecast_accuracy import forecast_accuracy
from backend.models.forecasting import prophet_forecast
from backend.models.sentiment import sentiment_summary
from backend.models.anomaly import detect_anomalies
from backend.models.pricing import price_optimization
from backend.models.promotion import promotion_impact
from backend.models.geo import region_wise_analysis
from backend.utils.validator import validate_sales_data
from backend.models.forecast_summary import summarize_forecast
from backend.models.ai_summary import generate_ai_summary

# ---------------- APP CONFIG ----------------
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

UPLOAD_DIR = "backend/uploads/default"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- HELPERS ----------------
def load_sales():
    return pd.read_csv(os.path.join(UPLOAD_DIR, "sales.csv"))

def load_reviews():
    path = os.path.join(UPLOAD_DIR, "reviews.csv")
    return pd.read_csv(path) if os.path.exists(path) else None

# ---------------- PAGES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        sales = request.files.get("sales_file")
        reviews = request.files.get("reviews_file")

        if not sales:
            return "Sales CSV required", 400

        sales_path = os.path.join(UPLOAD_DIR, "sales.csv")
        sales.save(sales_path)

        df = pd.read_csv(sales_path)
        ok, msg = validate_sales_data(df)
        if not ok:
            return msg, 400

        if reviews:
            reviews.save(os.path.join(UPLOAD_DIR, "reviews.csv"))

        return redirect("/final-dashboard")

    return render_template("upload.html")

@app.route("/final-dashboard")
def final_dashboard():
    return render_template("final_dashboard.html")

@app.route("/forecasting")
def forecasting_page():
    return render_template("forecasting.html")

@app.route("/anomaly")
def anomaly_page():
    return render_template("anomaly.html")

@app.route("/pricing")
def pricing_page():
    return render_template("pricing.html")

@app.route("/promotion")
def promotion_page():
    return render_template("promotions.html")

@app.route("/geo")
def geo_page():
    return render_template("geo.html")

@app.route("/sentiment-page")
def sentiment_page():
    return render_template("sentiment.html")

# ---------------- APIs ----------------
@app.route("/products")
def products():
    df = load_sales()
    return jsonify(
        df[["product_id", "product_name"]]
        .drop_duplicates()
        .to_dict(orient="records")
    )

@app.route("/forecast")
def forecast():
    df = load_sales()
    product = request.args.get("product")
    days = int(request.args.get("days", 30))

    # ✅ Only filter when product is actually selected
    if product and product.strip() != "":
        df = df[df["product_name"] == product]

    if df.empty:
        return jsonify({"actual": [], "forecast": []})

    actual_df, forecast_df = prophet_forecast(df, periods=days)

    return jsonify({
        "actual": actual_df.assign(ds=lambda x: x["ds"].astype(str))
                           .to_dict(orient="records"),
        "forecast": forecast_df.assign(ds=lambda x: x["ds"].astype(str))
                               .to_dict(orient="records")
    })




@app.route("/forecast-summary")
def forecast_summary():
    df = load_sales()
    actual, forecast = prophet_forecast(df)
    return jsonify(summarize_forecast(forecast))


@app.route("/forecast-ai-summary")
def forecast_ai_summary():
    try:
        df = load_sales()
        _, forecast = prophet_forecast(df)
        summary = summarize_forecast(forecast)
        return jsonify(generate_ai_summary(summary))
    except Exception:
        return jsonify({
            "ai_summary": "Upload valid sales data to generate AI insights."
        })

@app.route("/forecast-accuracy")
def forecast_accuracy_api():
    df = load_sales()
    product = request.args.get("product")

    if product:
        df = df[df["product_name"] == product]

    actual_df, forecast_df = prophet_forecast(df)
    return jsonify(forecast_accuracy(actual_df, forecast_df))

@app.route("/forecast-gpt-summary")
def forecast_gpt_summary():
    try:
        df = load_sales()
        actual_df, forecast_df = prophet_forecast(df)
        summary = summarize_forecast(forecast_df)
        return jsonify(generate_gpt_summary(summary))
    except Exception as e:
        return jsonify({
            "gpt_summary": "GPT insights unavailable.",
            "error": str(e)
        })

@app.route("/download-forecast-pdf")
def download_forecast_pdf():
    df = load_sales()

    actual_df, forecast_df = prophet_forecast(df)
    summary = summarize_forecast(forecast_df)
    ai_text = generate_ai_summary(summary)["ai_summary"]
    accuracy = forecast_accuracy(actual_df, forecast_df)

    chart_img = generate_forecast_chart(actual_df, forecast_df)
    pdf = generate_forecast_pdf(ai_text, accuracy, chart_img)

    return send_file(
        pdf,
        as_attachment=True,
        download_name="sales_forecast_report.pdf",
        mimetype="application/pdf"
    )

@app.route("/download-forecast-bundle")
def download_forecast_bundle():
    df = load_sales()

    actual_df, forecast_df = prophet_forecast(df)
    summary = summarize_forecast(forecast_df)
    ai_text = generate_ai_summary(summary)["ai_summary"]
    accuracy = forecast_accuracy(actual_df, forecast_df)

    csv_bytes = forecast_df.to_csv(index=False)

    chart_img = generate_forecast_chart(actual_df, forecast_df)
    pdf = generate_forecast_pdf(ai_text, accuracy, chart_img)

    zip_file = create_zip_bundle(csv_bytes, pdf)

    return send_file(
        zip_file,
        as_attachment=True,
        download_name="sales_forecast_bundle.zip",
        mimetype="application/zip"
    )

@app.route("/download-anomaly-pdf")
def download_anomaly_pdf():
    df = load_sales()
    product = request.args.get("product")

    data = detect_anomalies(df, product)
    anomalies = data[data["anomaly"]]

    chart_img = generate_anomaly_chart(data)
    pdf = generate_anomaly_pdf(anomalies, chart_img)

    return send_file(
        pdf,
        as_attachment=True,
        download_name="anomaly_report.pdf",
        mimetype="application/pdf"
    )



@app.route("/sentiment")
def sentiment():
    reviews_df = load_reviews()
    return jsonify(sentiment_summary(reviews_df))

@app.route("/anomalies")
def anomalies():
    df = load_sales()
    product = request.args.get("product")

    data = detect_anomalies(df, product)

    # 🔑 Frontend expects `ds`
    data["ds"] = data["date"].astype(str)

    return jsonify({
        "count": int(data["anomaly"].sum()),
        "data": data[[
            "ds",
            "units_sold",
            "anomaly",
            "severity",
            "reason"
        ]].to_dict(orient="records")
    })




@app.route("/price-optimize")
def price_optimize():
    df = load_sales()
    product = request.args.get("product")

    result = price_optimization(df, product)
    return jsonify(result)



@app.route("/promotion-impact")
def promotion_impact_api():
    df = load_sales()
    product = request.args.get("product")
    return jsonify(promotion_impact(df, product))


@app.route("/geo-analysis")
def geo_analysis():
    geo_df = region_wise_analysis(load_sales())

    top_row = geo_df.sort_values("total_revenue", ascending=False).iloc[0]

    return jsonify({
        "summary": {
            "total_regions": int(geo_df["region"].nunique()),
            "top_region": top_row["region"],
            "top_product": top_row["top_product"]
        },
        "regions": geo_df.to_dict(orient="records")
    })


    return jsonify(response)

@app.route("/state-geo")
def state_geo():
    df = load_sales()
    state_df = state_wise_analysis(df)
    return jsonify(state_df.to_dict(orient="records"))

    


@app.route("/download-geo-pdf", methods=["GET", "POST"])
def download_geo_pdf():
    df = load_sales()
    geo_df = region_wise_analysis(df)

    top_row = geo_df.sort_values("total_revenue", ascending=False).iloc[0]

    geo_data = {
        "summary": {
            "total_regions": len(geo_df),
            "top_region": top_row["region"],
            "top_product": top_row["top_product"]
        },
        "regions": geo_df.to_dict(orient="records")
    }

    # If POST request with map image → use it, else fallback to static
    map_image_base64 = None
    if request.method == "POST":
        try:
            data = request.get_json()
            map_image_base64 = data.get("map_image")
        except:
            pass

    pdf_buffer = generate_geo_pdf(geo_data, map_image_base64=map_image_base64)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="geospatial_sales_report.pdf",
        mimetype="application/pdf"
    )




from backend.utils.sentiment_pdf import generate_sentiment_pdf

@app.route("/download-sentiment-pdf", methods=["POST"])
def download_sentiment_pdf():
    reviews_df = load_reviews()  # or however you load it
    sentiment_data = sentiment_summary(reviews_df)

    chart_image = None
    if request.is_json:
        json_data = request.get_json()
        chart_image = json_data.get("chart_image")

    pdf_buffer = generate_sentiment_pdf(sentiment_data, chart_image)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="customer_sentiment_report.pdf",
        mimetype="application/pdf"
    )
# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
