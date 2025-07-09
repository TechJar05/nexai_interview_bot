# services/cohere/client.py

import os
import logging
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)
logger.debug("Initializing OpenAI client...")

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Optionally assign alias
co = client  # Now you can import `co` if required
