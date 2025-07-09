# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# print("COHERE_API_KEY from .env:", os.getenv('COHERE_API_KEY'))

# class Config:
#     # Flask Session
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
#     SESSION_TYPE = 'filesystem'
#     SESSION_COOKIE_NAME = 'session'
#     SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_session_data')

#     # Cohere Key
#     COHERE_API_KEY = os.getenv('COHERE_API_KEY', 'your-cohere-api-key-here')

#     # Django Backend URL
#     DJANGO_API_URL = os.getenv('DJANGO_API_URL')

#     # Interview Settings
#     MAX_RECORDING_DURATION = 520
#     PAUSE_THRESHOLD = 40
#     FOLLOW_UP_PROBABILITY = 0.8
#     MAX_FOLLOW_UPS = 3
#     MIN_FOLLOW_UPS = 2

#     # File Constants
#     CONVERSATION_FILE = "interview_conversation.txt"
#     LOG_FILE = 'interview_app.log'










# config.py
import os
from dotenv import load_dotenv

load_dotenv()
print("OPENAI_API_KEY from .env:", os.getenv('OPENAI_API_KEY'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_NAME = 'session'
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_session_data')

    # OpenAI Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

    # Django Backend URL
    DJANGO_API_URL = os.getenv('DJANGO_API_URL')

    MAX_RECORDING_DURATION = 520
    PAUSE_THRESHOLD = 40
    FOLLOW_UP_PROBABILITY = 0.8
    MAX_FOLLOW_UPS = 3
    MIN_FOLLOW_UPS = 2

    CONVERSATION_FILE = "interview_conversation.txt"
    LOG_FILE = 'interview_app.log'
