from pydantic import BaseModel, Field


class LegalQuery(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="User's legal information question",
    )

    language: str = Field(
        default="English",
        description="Preferred response language",
    )


class LegalResponse(BaseModel):
    answer: str
    disclaimer: str


class DocumentRequest(BaseModel):
    title: str
    content: str