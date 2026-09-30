from google import genai

from backend.config import GEMINI_API_KEY, GEMINI_MODEL


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI legal information assistant.

Your job is to provide general legal information in a clear,
simple and educational way.

Important rules:

1. Do not pretend to be a lawyer.
2. Do not claim that your response creates an attorney-client relationship.
3. Do not provide false certainty.
4. Explain that laws can differ by country, state and situation.
5. If the user's location or jurisdiction matters, ask them to verify
   the applicable local law.
6. Do not invent laws, sections, cases, citations or court decisions.
7. Use simple language.
8. Clearly separate general information from legal advice.
9. For urgent legal situations, recommend contacting a qualified lawyer
   or appropriate official authority.
"""


def get_client():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_legal_response(
    question: str,
    language: str = "English",
) -> str:

    client = get_client()

    prompt = f"""
{SYSTEM_INSTRUCTION}

Preferred language:
{language}

User's question:
{question}

Give a useful, structured answer.

Use this structure where appropriate:

1. Simple explanation
2. Important points
3. What the user can check or do next
4. Important limitations

Do not invent legal authorities or citations.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    if not response.text:
        return "No response was generated."

    return response.text