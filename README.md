# Sales Forecasting Dashboard

A Flask web app that turns uploaded sales data into forecasts, insights and downloadable reports. Upload a sales CSV (and optionally a customer reviews CSV) and the dashboard analyzes demand, anomalies, pricing, promotions, regions and sentiment.

## Features
- **Demand forecasting** with Facebook Prophet, per product or across all products, with a configurable horizon (default 30 days)
- **Forecast accuracy** metrics comparing actual and forecast values
- **AI-generated summaries** of forecast trends (OpenAI GPT, with a fallback message when unavailable)
- **Anomaly detection** on units sold, with severity and a reason for each anomaly
- **Price optimization** recommendations per product
- **Promotion impact** analysis
- **Geospatial analysis** of revenue by region, including top region and top product
- **Customer sentiment analysis** from reviews using VADER
- **Report exports:** forecast PDF, anomaly PDF, geo PDF, sentiment PDF, and a ZIP bundle (forecast CSV + PDF)

## Tech Stack
- Backend: Python, Flask, pandas, NumPy
- Forecasting and ML: Prophet, scikit-learn
- Sentiment: VADER
- Visualization and reports: Matplotlib, Pillow, PDF generation utilities
- AI summaries: OpenAI API
- Deployment: Gunicorn

## Project Structure
```
├── backend/
│   ├── app.py              # Flask app and routes
│   ├── database/           # SQLite setup scripts (init_db.py, insert_data.py)
│   ├── models/             # forecasting, anomaly, pricing, promotion, geo,
│   │                       # sentiment, AI/GPT summaries, forecast accuracy
│   ├── utils/              # validator, chart generator, PDF and ZIP exports
│   ├── uploads/            # user-uploaded CSVs (git-ignored)
│   └── requirements.txt
├── frontend/
│   ├── templates/          # base, index, upload, final_dashboard, forecasting,
│   │                       # anomaly, pricing, promotions, geo, sentiment
│   └── static/style.css
├── sales.csv               # sample sales data
├── reviews.csv             # sample reviews data
└── README.md
```

## Getting Started

**Requirements:** Python 3.10 to 3.12 recommended (Prophet may not support the newest Python releases yet).

```bash
git clone https://github.com/theashishreddy/sales-forecasting-dashboard.git
cd sales-forecasting-dashboard
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

Optional: enable GPT summaries by setting your OpenAI key.
```bash
export OPENAI_API_KEY=your_key_here     # Windows: set OPENAI_API_KEY=your_key_here
```

Run from the project root:
```bash
python -m backend.app
```

Open http://127.0.0.1:5000, go to **Upload**, and use the included `sales.csv` and `reviews.csv` to try the app.

### Production
```bash
gunicorn backend.app:app
```

## Data Format

**sales.csv** (required) must include at least:
`date`, `product_id`, `product_name`, `units_sold`, `region`

Price and revenue columns are needed for the pricing, promotion and geo analyses.

**reviews.csv** (optional) is used for sentiment analysis.

## Main Routes

| Route | Description |
|---|---|
| `/upload` | Upload sales and review CSVs |
| `/final-dashboard` | Combined dashboard |
| `/forecasting`, `/anomaly`, `/pricing`, `/promotion`, `/geo`, `/sentiment-page` | Individual analysis pages |
| `/forecast`, `/anomalies`, `/price-optimize`, `/promotion-impact`, `/geo-analysis`, `/sentiment` | JSON APIs |
| `/download-forecast-pdf`, `/download-forecast-bundle`, `/download-anomaly-pdf`, `/download-geo-pdf`, `/download-sentiment-pdf` | Report downloads |

## Forecasting Approach
Sales are modeled as a time series with Prophet, which captures trend and seasonality. Forecast quality is reported through an accuracy endpoint comparing actual and predicted values.



## Author
Ashish Reddy
