from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

def generate_anomaly_pdf(anomalies, chart_img):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, height - 40, "Sales Anomaly Report")

    pdf.drawImage(
        ImageReader(chart_img),
        40, height - 320,
        width=500, height=250
    )

    y = height - 360
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, y, "Date")
    pdf.drawString(120, y, "Units")
    pdf.drawString(190, y, "Severity")
    pdf.drawString(280, y, "Reason")

    y -= 15
    pdf.setFont("Helvetica", 9)

    for _, row in anomalies.iterrows():
        if y < 50:
            pdf.showPage()
            y = height - 50

        pdf.drawString(40, y, str(row["date"].date()))
        pdf.drawString(120, y, str(row["units_sold"]))
        pdf.drawString(190, y, row["severity"])
        pdf.drawString(280, y, row["reason"])
        y -= 14

    pdf.save()
    buffer.seek(0)
    return buffer
