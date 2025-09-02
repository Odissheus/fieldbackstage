from weasyprint import HTML, CSS
from pathlib import Path


def html_to_pdf_bytes(html: str) -> bytes:
    css_path = Path(__file__).resolve().parents[1] / "templates" / "report" / "styles.css"
    pdf_bytes = HTML(string=html).write_pdf(stylesheets=[CSS(filename=str(css_path))])
    return pdf_bytes

