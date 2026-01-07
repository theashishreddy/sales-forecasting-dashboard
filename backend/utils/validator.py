REQUIRED_COLUMNS = {
    "date", "product_id", "units_sold", "price", "revenue", "region", "is_promo"
}

def validate_sales_data(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return False, f"Missing columns: {', '.join(missing)}"
    return True, "Valid dataset"
