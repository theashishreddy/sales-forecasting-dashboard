# backend/models/sentiment.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()

def sentiment_summary(df):
    """
    Analyzes customer sentiment from reviews DataFrame.
    Expected column: 'review_text'
    """
    if df is None or df.empty or "review_text" not in df.columns:
        return {
            "total_reviews": 0,
            "avg_sentiment": 0.00,
            "positive_count": 0,
            "neutral_count": 0,
            "negative_count": 0,
            "mood": "No Data",
            "insight": "No reviews available. Upload a reviews.csv with a 'review_text' column to enable sentiment analysis.",
            "positive_samples": [],
            "negative_samples": []
        }

    # Work on a copy to avoid modifying original
    df = df.copy()
    texts = df["review_text"].fillna("").astype(str)

    # Compute compound score using VADER
    df["sentiment_score"] = texts.apply(lambda x: analyzer.polarity_scores(x)["compound"])

    total_reviews = len(df)
    avg_score = float(df["sentiment_score"].mean())

    # Classify using standard VADER thresholds
    positive_count = int((df["sentiment_score"] >= 0.05).sum())
    negative_count = int((df["sentiment_score"] <= -0.05).sum())
    neutral_count = total_reviews - positive_count - negative_count

    # Determine overall mood and insight
    if avg_score >= 0.05:
        mood = "Mostly Positive 😊"
        insight = "Excellent! Customers are generally satisfied with your products and service."
    elif avg_score <= -0.05:
        mood = "Mostly Negative 😞"
        insight = "Action required: Many customers are unhappy. Consider reviewing product quality, delivery, or support."
    else:
        mood = "Neutral 😐"
        insight = "Sentiment is balanced. Focus on converting neutral experiences into positive ones through better engagement."

    # Top 3 most extreme samples
    positive_samples = (
        df[df["sentiment_score"] >= 0.05]
        .nlargest(3, "sentiment_score")["review_text"]
        .tolist()
    )
    negative_samples = (
        df[df["sentiment_score"] <= -0.05]
        .nsmallest(3, "sentiment_score")["review_text"]
        .tolist()
    )

    return {
        "total_reviews": total_reviews,
        "avg_sentiment": round(avg_score, 2),
        "positive_count": positive_count,
        "neutral_count": neutral_count,
        "negative_count": negative_count,
        "mood": mood,
        "insight": insight,
        "positive_samples": positive_samples,
        "negative_samples": negative_samples
    }