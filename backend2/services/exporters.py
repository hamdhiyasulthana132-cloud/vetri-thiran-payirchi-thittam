from io import BytesIO

from docx import Document

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_txt(content: str) -> BytesIO:
    file = BytesIO()

    file.write(content.encode("utf-8"))
    file.seek(0)

    return file


def create_docx(title: str, content: str) -> BytesIO:
    document = Document()

    document.add_heading(title, level=1)

    for paragraph in content.split("\n"):
        document.add_paragraph(paragraph)

    file = BytesIO()

    document.save(file)
    file.seek(0)

    return file


def create_pdf(title: str, content: str) -> BytesIO:
    file = BytesIO()

    pdf = canvas.Canvas(file, pagesize=A4)

    width, height = A4

    x = 50
    y = height - 60

    pdf.setTitle(title)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, y, title)

    y -= 35

    pdf.setFont("Helvetica", 10)

    for line in content.split("\n"):
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 50

        # Basic wrapping
        words = line.split()
        current_line = ""

        for word in words:
            test_line = (
                current_line + " " + word
            ).strip()

            if pdf.stringWidth(test_line, "Helvetica", 10) < 500:
                current_line = test_line
            else:
                pdf.drawString(x, y, current_line)
                y -= 15
                current_line = word

                if y < 50:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    y = height - 50

        if current_line:
            pdf.drawString(x, y, current_line)
            y -= 15

        y -= 5

    pdf.save()

    file.seek(0)

    return file