from langchain_google_genai import ChatGoogleGenerativeAI
from .config import settings
from .logger import logger

def get_llm():
    if not settings.GOOGLE_API_KEY:
        logger.warning("GOOGLE_API_KEY not found in environment variables.")

    return ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME, 
        temperature=settings.TEMPERATURE,
        google_api_key=settings.GOOGLE_API_KEY
    )
