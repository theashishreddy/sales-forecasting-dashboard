import io
import zipfile

def create_zip_bundle(csv_bytes, pdf_bytes):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("sales_forecast.csv", csv_bytes)
        z.writestr("sales_forecast_report.pdf", pdf_bytes.getvalue())

    zip_buffer.seek(0)
    return zip_buffer
