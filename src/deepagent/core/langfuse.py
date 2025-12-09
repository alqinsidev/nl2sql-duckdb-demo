from .config import settings
import os
from .logger import logger
from langfuse.langchain import CallbackHandler
from langfuse import get_client

# Initialize Langfuse Callback
langfuse_handler = None
if settings.LANGFUSE_PUBLIC_KEY and settings.LANGFUSE_SECRET_KEY:
    os.environ["LANGFUSE_SECRET_KEY"] = settings.LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_PUBLIC_KEY"] = settings.LANGFUSE_PUBLIC_KEY
    os.environ["LANGFUSE_HOST"] = settings.LANGFUSE_BASE_URL or "https://cloud.langfuse.com"
    
    # Verify connection
    langfuse = get_client()
    if langfuse.auth_check():
        logger.info("Langfuse connection verified successfully.")
    else:
        logger.error("Langfuse authentication failed. Please check your credentials and host.")

    langfuse_handler = CallbackHandler()
    logger.info("Langfuse integration enabled.")
else:
    logger.warning("Langfuse credentials not found. Tracing disabled.")
