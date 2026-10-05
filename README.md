<div align="center">

# 📊 Sales Forecasting & Analytics Dashboard

An end-to-end, full-stack AI-driven web application that transforms raw sales and customer review data into actionable demand forecasts, anomaly detections, price optimizations, geospatial insights, and downloadable executive reports.

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.10-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/framework-Flask%203.0.3-black.svg)](https://flask.palletsprojects.com/)
[![Prophet](https://img.shields.io/badge/forecasting-Facebook%20Prophet-brightgreen.svg)](https://facebook.github.io/prophet/)
[![Render](https://img.shields.io/badge/deploy-Render-46E3B7.svg)](https://render.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 🚀 Key Features

- 📈 **Time-Series Demand Forecasting**: Forecast future units sold and revenue using **Facebook Prophet** with custom horizons (default 30 days), broken down by product or aggregate totals.
- 🎯 **Forecast Accuracy Metrics**: Built-in evaluation comparing actuals vs. predictions using MAPE, RMSE, and MAE.
- 🤖 **AI-Generated Executive Summaries**: Integrates OpenAI GPT to automatically generate concise business summaries and trend analyses (includes smart local fallback).
- 🚨 **Anomaly Detection**: Statistical and ML-driven outlier detection identifying sudden spikes or drops in sales volume, accompanied by severity ranking and root-cause indicators.
- 💲 **Price Optimization**: Price elasticity analysis and revenue-maximizing price point recommendations per product.
- 📢 **Promotion Impact Analysis**: Quantifies the lift in sales volume and revenue generated during promotional periods versus baseline sales.
- 🗺️ **Geospatial & Regional Intelligence**: Regional performance breakdown highlighting top-performing geographic territories and products.
- 💬 **Customer Sentiment Analysis**: Natural Language Processing (NLP) with **VADER** to score customer feedback and detect sentiment trends across regions and products.
- 📑 **Automated PDF & Bundle Exports**: One-click generation of styled executive PDF reports (Forecasting, Anomaly, Geo, Sentiment) and ZIP archive bundles with CSVs and charts.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.11, Flask 3.0.3, Gunicorn |
| **Forecasting & ML** | Facebook Prophet, Scikit-Learn, XGBoost, NumPy, Pandas |
| **NLP & Sentiment** | VADER Sentiment Analysis |
| **Visualization & Reporting** | Matplotlib, Seaborn, Pillow, ReportLab |
| **AI Summaries** | OpenAI GPT API |
| **Frontend** | Modern HTML5, Responsive CSS, Vanilla JavaScript, Chart.js / Dynamic SVGs |

---

## 📂 Project Structure

```text
sales-forecasting-dashboard/
├── backend/
│   ├── app.py                  # Main Flask application & API routes
│   ├── database/               # SQLite database setup & schemas
│   │   ├── init_db.py
│   │   └── insert_data.py
│   ├── models/                 # Analytical & ML logic modules
│   │   ├── forecasting.py      # Prophet time-series models
│   │   ├── forecast_accuracy.py# Forecast evaluation metrics
│   │   ├── forecast_summary.py # Trend summary computation
│   │   ├── anomaly.py          # Outlier detection algorithm
│   │   ├── pricing.py          # Elasticity & price optimization
│   │   ├── promotion.py        # Promo impact evaluation
│   │   ├── geo.py              # Regional performance analytics
│   │   ├── sentiment.py        # VADER review sentiment scoring
│   │   ├── gpt_summary.py      # OpenAI GPT integration
│   │   └── ai_summary.py       # AI summary orchestrator
│   ├── utils/                  # Helper utilities & report generators
│   │   ├── chart_generator.py  # Forecast & anomaly chart rendering
│   │   ├── geo_chart.py        # Regional bar chart generator
│   │   ├── validator.py        # CSV input validation
│   │   ├── pdf_report.py       # Forecast PDF generator
│   │   ├── anomaly_pdf.py      # Anomaly report PDF
│   │   ├── geo_pdf.py          # Geospatial report PDF
│   │   ├── sentiment_pdf.py    # Sentiment report PDF
│   │   └── bundle_export.py    # ZIP packaging (PDF + CSV)
│   └── uploads/                # User uploaded datasets (ignored in git)
├── frontend/
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── base.html           # Core layout & navigation
│   │   ├── index.html          # Landing page
│   │   ├── upload.html         # CSV upload interface
│   │   ├── final_dashboard.html# Unified executive dashboard
│   │   ├── forecasting.html    # Demand forecast page
│   │   ├── anomaly.html        # Anomaly inspector
│   │   ├── pricing.html        # Price optimizer
│   │   ├── promotions.html     # Promotion impact viewer
│   │   ├── geo.html            # Regional analytics
│   │   └── sentiment.html      # Sentiment analysis explorer
│   └── static/
│       └── style.css           # Custom modern stylesheet
├── app.py                      # Root WSGI entrypoint
├── Procfile                    # Web process config for Render / Heroku
├── render.yaml                 # Render Blueprint deployment config
├── requirements.txt            # Python dependencies
├── sales.csv                   # Sample sales dataset
├── reviews.csv                 # Sample reviews dataset
└── README.md
```

---

## ⚡ Getting Started (Local Setup)

### Prerequisites
- **Python 3.10 or 3.11** installed (recommended for pre-built Prophet wheels)
- **Git**

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/theashishreddy/sales-forecasting-dashboard.git
   cd sales-forecasting-dashboard
   ```

2. **Create and activate a virtual environment:**
   - **macOS / Linux:**
     ```bash
     python3.11 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **(Optional) Configure OpenAI API Key for AI Summaries:**
   - **macOS / Linux:**
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```
   - **Windows (PowerShell):**
     ```powershell
     $env:OPENAI_API_KEY="your-api-key-here"
     ```

5. **Run the application:**
   ```bash
   python -m backend.app
   ```
   Or run using Gunicorn (production mode):
   ```bash
   gunicorn -b 127.0.0.1:5000 backend.app:app
   ```

6. Open your browser and navigate to:
   **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## ☁️ Deployment Guide

### Deploying to Render (One-Click / Web Service)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```
2. Log in to [Render Dashboard](https://dashboard.render.com/) and click **New + > Web Service**.
3. Select your repository.
4. Set the following build and run parameters:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend.app:app`
5. Under **Environment Variables**, add:
   - `PYTHON_VERSION` = `3.11.9`
   - `OPENAI_API_KEY` = *(Optional: your OpenAI API Key)*
6. Click **Create Web Service**.

---

## 📋 Input Data Formats

You can use the provided sample datasets [`sales.csv`](sales.csv) and [`reviews.csv`](reviews.csv) or upload your own files.

### 1. `sales.csv` (Required)
| Column | Type | Example | Description |
|---|---|---|---|
| `date` | String / Date | `01-01-2024` | Transaction date |
| `product_id` | String | `P001` | Unique product identifier |
| `product_name` | String | `Wireless Earbuds`| Human-readable product name |
| `category` | String | `Electronics` | Product category |
| `units_sold` | Integer | `120` | Units sold on this date |
| `price` | Float / Int | `2999` | Unit price |
| `revenue` | Float / Int | `359880` | Total revenue (`units_sold * price`) |
| `region` | String | `South` | Sales territory (e.g. North, South, East, West) |
| `is_promo` | Integer (0/1) | `1` | Flag indicating active promotion |

### 2. `reviews.csv` (Optional for Sentiment)
| Column | Type | Example | Description |
|---|---|---|---|
| `review_id` | String | `R001` | Unique review identifier |
| `product_id` | String | `P001` | Corresponding product ID |
| `review_text` | String | `"Excellent sound quality and battery life"` | Customer review content |
| `rating` | Integer | `5` | Star rating (1–5) |
| `region` | String | `South` | Reviewer location |

---

## 📡 API & Route Reference

### Web Pages
| Route | Method | Description |
|---|---|---|
| `/` | `GET` | Landing page overview |
| `/upload` | `GET`, `POST` | Upload and validate `sales.csv` and `reviews.csv` |
| `/final-dashboard` | `GET` | Unified executive dashboard with all key metrics |
| `/forecasting` | `GET` | Interactive demand forecasting page |
| `/anomaly` | `GET` | Anomaly detection overview and drill-down |
| `/pricing` | `GET` | Price elasticity & revenue optimization view |
| `/promotion` | `GET` | Promotional lift and performance analytics |
| `/geo` | `GET` | Geospatial and regional sales breakdown |
| `/sentiment-page` | `GET` | Customer review sentiment analysis page |

### JSON APIs
| Endpoint | Method | Description |
|---|---|---|
| `/forecast` | `GET` | Returns Prophet forecast data (history, predicted, confidence intervals) |
| `/anomalies` | `GET` | Returns identified outliers, severity ratings, and reasons |
| `/price-optimize`| `GET` | Returns optimal price points and elasticity metrics |
| `/promotion-impact`| `GET` | Returns promotional vs. non-promotional metrics |
| `/geo-analysis` | `GET` | Returns regional sales and revenue aggregations |
| `/sentiment` | `GET` | Returns sentiment scores, category breakdowns, and sentiment distributions |

### Report Exports
| Route | Method | Output | Description |
|---|---|---|---|
| `/download-forecast-pdf` | `POST` | PDF | Comprehensive demand forecast executive report |
| `/download-forecast-bundle` | `POST` | ZIP | Archive containing forecast PDF and forecast CSV data |
| `/download-anomaly-pdf` | `GET` | PDF | Outliers and anomalies summary report |
| `/download-geo-pdf` | `POST` | PDF | Regional performance and geospatial distribution report |
| `/download-sentiment-pdf` | `POST` | PDF | Customer sentiment analysis and reviews report |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ashish Reddy**
- GitHub: [@theashishreddy](https://github.com/theashishreddy)
