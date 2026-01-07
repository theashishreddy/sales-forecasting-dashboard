def generate_ai_summary(summary):
    trend = summary["trend"]
    growth = summary["growth_percent"]
    risk = summary.get("risk_level", "moderate")

    if trend == "upward":
        outlook = "a positive growth trajectory"
        advice = "Increase inventory gradually and maintain current pricing."
    elif trend == "downward":
        outlook = "a declining demand pattern"
        advice = "Reduce inventory risk and review pricing or promotions."
    else:
        outlook = "stable demand with minor fluctuations"
        advice = "Maintain steady inventory levels and monitor demand."

    confidence_note = {
        "low": "Forecast confidence is high due to low volatility.",
        "moderate": "Forecast confidence is moderate with some demand variation.",
        "high": "Forecast uncertainty is high; demand may fluctuate significantly."
    }

    return {
        "ai_summary": (
            f"The sales forecast indicates {outlook}. "
            f"Expected overall change is {growth}%. "
            f"Peak demand is projected around {summary['peak_date']}, "
            f"with lower sales near {summary['low_date']}. "
            f"{confidence_note.get(risk, '')} "
            f"Recommended action: {advice}"
        )
    }

