# backend/utils/sentiment_pdf.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
import base64

def generate_sentiment_pdf(data, chart_image_base64=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.8*inch,
        bottomMargin=0.8*inch,
        leftMargin=0.8*inch,
        rightMargin=0.8*inch
    )
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1e40af")
    ))

    elements = []

    # Title
    elements.append(Paragraph("Customer Sentiment Analysis Report", styles["CustomTitle"]))
    elements.append(Spacer(1, 20))

    # Summary Table
    summary_data = [
        ["Metric", "Value"],
        ["Total Reviews Analyzed", f"{data.get('total_reviews', 0):,}"],
        ["Average Sentiment Score", f"{data.get('avg_sentiment', 0):+.2f}"],
        ["Overall Mood", data.get('mood', 'N/A')]
    ]
    summary_table = Table(summary_data, colWidths=[3.2*inch, 3.2*inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e40af")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ("ROWBACKGROUNDS", (1,0), (-1,-1), [colors.HexColor("#f8fafc"), colors.white]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("PADDING", (0,0), (-1,-1), 12),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 40))

    # Full Captured View (Chart + Indicators)
    elements.append(Paragraph("Sentiment Distribution", styles["Heading2"]))
    elements.append(Spacer(1, 20))

    if chart_image_base64:
        try:
            img_str = chart_image_base64.split(",")[1] if "," in chart_image_base64 else chart_image_base64
            img_bytes = base64.b64decode(img_str)
            img_buffer = BytesIO(img_bytes)
            full_view_img = Image(img_buffer, width=7*inch, height=5.5*inch)
            full_view_img.hAlign = "CENTER"
            elements.append(full_view_img)
        except Exception as e:
            print(f"Full view embedding failed: {e}")
            elements.append(Paragraph("<i>Visual could not be embedded.</i>", styles["Italic"]))
    else:
        elements.append(Paragraph("<i>No visual provided.</i>", styles["Italic"]))

    elements.append(Spacer(1, 40))

    # AI Insight
    elements.append(Paragraph("AI Business Insight", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(data.get("insight", "No insight available."), styles["Normal"]))
    elements.append(Spacer(1, 40))

    # Sample Reviews
    elements.append(Paragraph("Sample Customer Reviews", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Top Positive Reviews", styles["Heading3"]))
    for review in data.get("positive_samples", [])[:4]:
        elements.append(Paragraph(f"• “{review}”", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Top Negative Reviews", styles["Heading3"]))
    for review in data.get("negative_samples", [])[:4]:
        elements.append(Paragraph(f"• “{review}”", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer