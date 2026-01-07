import pandas as pd

def region_wise_analysis(df):
    df = df.copy()

    # Ensure numeric
    df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Revenue from CSV logic
    df["revenue"] = df["price"] * df["units_sold"]

    # -------- REGION AGGREGATION --------
    geo_df = (
        df.groupby("region", as_index=False)
        .agg(
            total_units=("units_sold", "sum"),
            total_revenue=("revenue", "sum")
        )
    )

    # -------- TOP PRODUCT PER REGION --------
    top_products = (
        df.groupby(["region", "product_name"])["units_sold"]
        .sum()
        .reset_index()
        .sort_values(["region", "units_sold"], ascending=[True, False])
        .groupby("region")
        .first()
        .reset_index()
    )

    geo_df = geo_df.merge(
        top_products[["region", "product_name"]],
        on="region"
    ).rename(columns={"product_name": "top_product"})

    # -------- PERFORMANCE LOGIC (✅ CORRECT PLACE) --------
    max_rev = geo_df["total_revenue"].max()

    def performance_label(r):
        if r >= 0.75 * max_rev:
            return "High"
        elif r <= 0.5 * max_rev:
            return "Low"
        else:
            return "Medium"

    geo_df["performance"] = geo_df["total_revenue"].apply(performance_label)


    

    return geo_df

def state_wise_analysis(df):
    df = df.copy()

    df["units_sold"] = pd.to_numeric(df["units_sold"])
    df["revenue"] = pd.to_numeric(df["revenue"])

    state_df = (
        df.groupby("state", as_index=False)
        .agg(
            total_units=("units_sold", "sum"),
            total_revenue=("revenue", "sum")
        )
    )

    return state_df

