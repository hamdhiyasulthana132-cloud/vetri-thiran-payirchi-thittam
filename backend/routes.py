from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.ai_core.gemini_generator import generate_legal_response
from backend.schemas import LegalQuery, LegalResponse, DocumentRequest
from backend.services.exporters import (
    create_docx,
    create_pdf,
    create_txt,
)


router = APIRouter()


DISCLAIMER = (
    "LegalEase provides general legal information for educational "
    "purposes only. It is not a substitute for advice from a qualified "
    "legal professional."
)


@router.get("/status")
def status():
    return {
        "status": "online",
        "service": "LegalEase",
    }


@router.post(
    "/ask",
    response_model=LegalResponse,
)
def ask_legal_question(data: LegalQuery):

    try:
        answer = generate_legal_response(
            question=data.question,
            language=data.language,
        )

        return LegalResponse(
            answer=answer,
            disclaimer=DISCLAIMER,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/export/txt")
def export_txt(data: DocumentRequest):

    content = f"{data.title}\n\n{data.content}"

    file = create_txt(content)

    return StreamingResponse(
        file,
        media_type="text/plain",
        headers={
            "Content-Disposition":
                'attachment; filename="legalease_response.txt"'
        },
    )


@router.post("/export/docx")
def export_docx(data: DocumentRequest):

    file = create_docx(
        title=data.title,
        content=data.content,
    )

    return StreamingResponse(
        file,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
        headers={
            "Content-Disposition":
                'attachment; filename="legalease_response.docx"'
        },
    )


@router.post("/export/pdf")
def export_pdf(data: DocumentRequest):

    file = create_pdf(
        title=data.title,
        content=data.content,
    )

    return StreamingResponse(
        file,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                'attachment; filename="legalease_response.pdf"'
        },
    )