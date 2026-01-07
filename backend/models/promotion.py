def promotion_impact(df, product=None):
    df = df.copy()

    if product:
        df = df[df["product_name"] == product]

    # 🔑 Auto-generate promo flag if missing
    if "is_promo" not in df.columns:
        df["is_promo"] = (
            (df["price"] < df["price"].mean()) |
            (df["units_sold"] > df["units_sold"].quantile(0.75))
        ).astype(int)

    promo = df[df["is_promo"] == 1]
    non_promo = df[df["is_promo"] == 0]

    if promo.empty or non_promo.empty:
        return {
            "promo_units": 0,
            "non_promo_units": 0,
            "promo_revenue": 0,
            "non_promo_revenue": 0,
            "lift_percent": 0,
            "recommendation": "Insufficient promotion data."
        }

    promo_units = promo["units_sold"].mean()
    non_promo_units = non_promo["units_sold"].mean()

    lift = ((promo_units - non_promo_units) / non_promo_units) * 100

    return {
        "promo_units": round(promo_units, 2),
        "non_promo_units": round(non_promo_units, 2),
        "promo_revenue": round((promo["price"] * promo["units_sold"]).mean(), 2),
        "non_promo_revenue": round((non_promo["price"] * non_promo["units_sold"]).mean(), 2),
        "lift_percent": round(lift, 2),
        "recommendation": "Promotion inferred using price drop & demand spike logic."
    }
