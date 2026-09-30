from backend.services.exporters import (
    create_txt,
    create_docx,
    create_pdf,
)


def test_txt_export():

    file = create_txt("Hello LegalEase")

    data = file.read()

    assert b"Hello LegalEase" in data


def test_docx_export():

    file = create_docx(
        "LegalEase",
        "Test document",
    )

    data = file.read()

    assert len(data) > 0


def test_pdf_export():

    file = create_pdf(
        "LegalEase",
        "Test PDF document",
    )

    data = file.read()

    assert len(data) > 0