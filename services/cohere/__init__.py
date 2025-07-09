import logging
from config import Config

logger = logging.getLogger(__name__)
logger.debug("OpenAI service package initialized.")
logger.debug(f"Using OpenAI API Key: {Config.OPENAI_API_KEY[:5]}...")  # Masked for safety
