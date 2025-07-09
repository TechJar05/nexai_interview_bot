# # services/__init__.py

# # Cohere services
# from .cohere import client, question_generator, followup_generator, encouragement_prompt, prompt_builder

# # Report services
# from .report import generate_interview_report, create_text_report_from_interview_data, save_admin_report_txt

# # Other services
# from . import tts_service
# from . import visual_service
# from . import scoring_service



# services/__init__.py

# OpenAI-based interview services
from services.cohere import question_generator, followup_generator, encouragement_prompt, prompt_builder

# Report services
from services.report.generator import generate_interview_report
from services.report.formatter import create_text_report_from_interview_data
# from services.report.file_manager import save_admin_report_txt
# Other services
from . import tts_service
from . import visual_service
from . import scoring_service
