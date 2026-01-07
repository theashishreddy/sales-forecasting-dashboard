import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_summary(summary):
    prompt = f"""
You are a business data analyst.

Forecast insights:
- Trend: {summary['trend']}
- Growth: {summary['growth_percent']}%
- Peak date: {summary['peak_date']}
- Lowest date: {summary['low_date']}

Explain the sales outlook and suggest business actions in simple language.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate concise business insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=120
    )

    return {
        "gpt_summary": response.choices[0].message.content.strip()
    }
