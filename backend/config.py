import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

APP_NAME = "LegalEase"
APP_VERSION = "1.0.0"

GEMINI_MODEL = "gemini-3.8-flash"