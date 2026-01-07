# backend/utils/geo_pdf.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from PIL import Image as PILImage, ImageDraw
from backend.utils.geo_chart import generate_geo_bar_chart
import requests

def generate_static_india_map(regions):
    map_url = (
        "https://upload.wikimedia.org/wikipedia/commons/"
        "thumb/3/3c/India_outline_map.png/800px-India_outline_map.png"
    )

    headers = {"User-Agent": "Mozilla/5.0 (SalesForecastingProject)"}
    response = requests.get(map_url, headers=headers, timeout=10)

    if response.status_code != 200:
        raise RuntimeError("Failed to download India map image")

    img_bytes = response.content

    try:
        base = PILImage.open(BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Downloaded file is not a valid image: {e}")

    draw = ImageDraw.Draw(base)

    coords = {
        "North": (400, 180),
        "South": (420, 520),
        "East":  (560, 330),
        "West":  (300, 330),
    }

    color_map = {
        "High": "green",
        "Medium": "orange",
        "Low": "red"
    }

    radius = 12
    for r in regions:
        region = r["region"]
        if region in coords:
            x, y = coords[region]
            color = color_map.get(r["performance"], "blue")
            draw.ellipse((x-radius, y-radius, x+radius, y+radius),
                         fill=color, outline="black", width=2)

    buf = BytesIO()
    base.save(buf, format="PNG")
    buf.seek(0)
    return buf


def generate_geo_pdf(geo_data, map_image_base64=None):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=(8.5*inch, 11*inch),
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    elements = []

    # Title & Summary (same as before)
    elements.append(Paragraph("Geospatial Sales Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    summary = geo_data["summary"]
    elements.append(Paragraph(
        f"<b>Total Regions:</b> {summary['total_regions']}<br/>"
        f"<b>Top Performing Region:</b> {summary['top_region']}<br/>"
        f"<b>Top Product Overall:</b> {summary['top_product']}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 30))

    # Bar Chart
    elements.append(Paragraph("Revenue Distribution by Region", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    chart_buf = generate_geo_bar_chart(geo_data["regions"])
    chart_buf.seek(0)
    elements.append(Image(chart_buf, width=6*inch, height=4*inch))
    elements.append(Spacer(1, 30))

    # MAP - Use captured map if provided, else fallback
    # ... inside generate_geo_pdf ...

# MAP - Use captured map (required now)
    elements.append(Paragraph("India Sales Performance Map", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    if map_image_base64:
        try:
            img_data = map_image_base64.split(",")[1]
            img_bytes = base64.b64decode(img_data)
            img_buffer = BytesIO(img_bytes)

        # Optional: Validate it's an image
            PILImage.open(img_buffer).verify()
            img_buffer.seek(0)

            map_img = Image(img_buffer, width=6*inch, height=4.5*inch)
            map_img.hAlign = "CENTER"
            elements.append(map_img)
        except Exception as e:
        # Graceful fallback text if something goes wrong
            elements.append(Paragraph(
                "<i>Note: Interactive map could not be embedded in PDF.</i>",
                styles["Italic"]
            ))
            print("Map embed failed:", e)  # Log for debugging
    else:
    # No map provided — show message
        elements.append(Paragraph(
            "<i>No map image provided for PDF.</i>",
            styles["Italic"]
        ))

    # Table (same as before, with formatting)
    elements.append(Paragraph("Region-wise Performance Details", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    table_data = [["Region", "Total Units", "Revenue (₹)", "Top Product", "Performance"]]
    for r in geo_data["regions"]:
        table_data.append([
            r["region"],
            f"{r['total_units']:,}",
            f"₹{r['total_revenue']:,}",
            r["top_product"],
            r["performance"]
        ])

    table = Table(table_data, colWidths=[1.4*inch, 1.2*inch, 1.5*inch, 1.6*inch, 1*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1f4e79")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f0f8ff"), colors.white]),
    ]))
    elements.append(table)

    pdf.build(elements)
    buffer.seek(0)
    return buffer