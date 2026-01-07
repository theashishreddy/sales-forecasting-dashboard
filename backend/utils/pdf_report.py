from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime
import io

def generate_forecast_pdf(ai_summary, accuracy, chart_img):
    buffer = io.BytesIO()
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    elements.append(Paragraph("<b>Sales Forecast Report</b>", styles["Title"]))
    elements.append(Paragraph(f"Generated on: {datetime.now()}", styles["Normal"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph("<b>Forecast Chart</b>", styles["Heading2"]))
    elements.append(Image(chart_img, width=400, height=200))

    elements.append(Paragraph("<br/>", styles["Normal"]))
    elements.append(Paragraph("<b>AI Forecast Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(ai_summary, styles["Normal"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))
    elements.append(Paragraph("<b>Forecast Accuracy</b>", styles["Heading2"]))
    elements.append(
        Paragraph(
            f"MAPE: {accuracy['mape']}% | RMSE: {accuracy['rmse']}",
            styles["Normal"]
        )
    )

    doc.build(elements)
    buffer.seek(0)
    return buffer

