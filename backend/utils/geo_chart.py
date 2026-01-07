import matplotlib.pyplot as plt
from io import BytesIO

def generate_geo_bar_chart(regions):
    regions_names = [r["region"] for r in regions]
    revenues = [r["total_revenue"] for r in regions]

    plt.figure(figsize=(6, 4))
    plt.bar(regions_names, revenues)
    plt.title("Total Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="PNG")
    plt.close()
    buf.seek(0)

    return buf
