# from flask import Blueprint, jsonify, session
# from datetime import datetime, timezone, timedelta
# import numpy as np
# import logging

# from routes.session import save_conversation_to_file
# from utils.helpers import init_interview_data
# from services.tts_service import text_to_speech

# logger = logging.getLogger(__name__)
# question_bp = Blueprint('question_bp', __name__)

# # Constants
# FOLLOW_UP_PROBABILITY = 0.8
# MIN_FOLLOW_UPS = 2
# MAX_FOLLOW_UPS = 3
# MAX_DURATION_MINUTES = 20


# @question_bp.route('/get_question', methods=['GET'])
# def get_question():
#     logger.debug("Get question request received")

#     interview_data = session.get('interview_data')
#     if not interview_data or not interview_data.get('interview_started'):
#         logger.warning("Interview not started or data missing")
#         return jsonify({"status": "not_started"})

#     # Check interview time
#     elapsed = datetime.now(timezone.utc) - interview_data.get('start_time', datetime.now(timezone.utc))
#     if elapsed > timedelta(minutes=MAX_DURATION_MINUTES):
#         logger.info("Interview duration exceeded.")
#         return jsonify({"status": "time_exceeded", "message": "Interview time has ended."})

#     interview_data.setdefault('used_questions', [])
#     interview_data.setdefault('used_follow_ups', [])
#     interview_data.setdefault('follow_up_questions', [])
#     interview_data.setdefault('follow_up_count', 0)
#     interview_data.setdefault('current_question', 0)
#     interview_data.setdefault('conversation_history', [])

#     is_follow_up = False
#     current_q = None

#     # Decide: follow-up or main
#     if (
#         interview_data['follow_up_questions'] and
#         interview_data['follow_up_count'] < MAX_FOLLOW_UPS and
#         (interview_data['follow_up_count'] < MIN_FOLLOW_UPS or np.random.random() < FOLLOW_UP_PROBABILITY)
#     ):
#         for follow_up in interview_data['follow_up_questions']:
#             if follow_up not in interview_data['used_follow_ups']:
#                 current_q = follow_up
#                 interview_data['used_follow_ups'].append(current_q)
#                 interview_data['follow_up_count'] += 1
#                 is_follow_up = True
#                 break

#     # If no follow-up, go to next main question
#     if not current_q:
#         while interview_data['current_question'] < len(interview_data['questions']):
#             idx = interview_data['current_question']
#             q = interview_data['questions'][idx]
#             if q not in interview_data['used_questions']:
#                 current_q = q
#                 interview_data['used_questions'].append(current_q)
#                 interview_data['current_topic'] = interview_data['question_topics'][idx]
#                 interview_data['follow_up_count'] = 0
#                 interview_data['current_question'] += 1
#                 is_follow_up = False
#                 break
#             else:
#                 interview_data['current_question'] += 1

#     if not current_q:
#         logger.info("All questions exhausted, interview complete")
#         return jsonify({"status": "completed"})

#     interview_data['conversation_history'].append({"speaker": "bot", "text": current_q})
#     save_conversation_to_file([{"speaker": "bot", "text": current_q}])
#     interview_data['last_activity_time'] = datetime.now(timezone.utc)
#     session['interview_data'] = interview_data

#     # Convert to speech
#     try:
#         audio_data = text_to_speech(current_q)
#     except Exception as e:
#         logger.error(f"TTS error: {str(e)}")
#         audio_data = None

#     return jsonify({
#         "status": "success",
#         "question": current_q,
#         "audio": audio_data,
#         "question_number": interview_data['current_question'],
#         "total_questions": len(interview_data['questions']),
#         "is_follow_up": is_follow_up
#     })









from flask import Blueprint, jsonify, session
from datetime import datetime, timezone, timedelta
import numpy as np
import logging

from routes.session import save_conversation_to_file
from utils.helpers import init_interview_data
from services.tts_service import text_to_speech

logger = logging.getLogger(__name__)
question_bp = Blueprint('question_bp', __name__)

# Constants
FOLLOW_UP_PROBABILITY = 0.8
MIN_FOLLOW_UPS = 2
MAX_FOLLOW_UPS = 3
MAX_DURATION_MINUTES = 20


@question_bp.route('/get_question', methods=['GET'])
def get_question():
    logger.debug("📥 Get question request received.")
    logger.debug(f"📌 Session ID: {session.get('id', 'N/A')}")

    # Ensure interview_data is present
    interview_data = session.get('interview_data')
    if not interview_data:
        logger.warning("❗ Interview session not found. Reinitializing.")
        interview_data = init_interview_data()
        session['interview_data'] = interview_data

    if not interview_data.get('interview_started'):
        logger.warning("⛔ Interview not started yet.")
        return jsonify({"status": "not_started"}), 400

    # Ensure start_time exists
    start_time = interview_data.get('start_time')
    if not start_time:
        logger.warning("🕒 start_time missing — initializing now.")
        start_time = datetime.now(timezone.utc)
        interview_data['start_time'] = start_time

    # Check if interview time is over
    elapsed = datetime.now(timezone.utc) - start_time
    if elapsed > timedelta(minutes=MAX_DURATION_MINUTES):
        logger.info("⏳ Interview duration exceeded.")
        return jsonify({"status": "time_exceeded", "message": "Interview time has ended."}), 200

    # Validate questions and topics
    if not interview_data.get('questions') or not interview_data.get('question_topics'):
        logger.error("❌ Missing questions or topics in session.")
        return jsonify({"status": "error", "message": "Questions not initialized."}), 500

    # Defaults
    interview_data.setdefault('used_questions', [])
    interview_data.setdefault('used_follow_ups', [])
    interview_data.setdefault('follow_up_questions', [])
    interview_data.setdefault('follow_up_count', 0)
    interview_data.setdefault('current_question', 0)
    interview_data.setdefault('conversation_history', [])

    current_q = None
    is_follow_up = False

    # Follow-up logic
    if (
        interview_data['follow_up_questions'] and
        interview_data['follow_up_count'] < MAX_FOLLOW_UPS and
        (interview_data['follow_up_count'] < MIN_FOLLOW_UPS or np.random.random() < FOLLOW_UP_PROBABILITY)
    ):
        for follow_up in interview_data['follow_up_questions']:
            if follow_up not in interview_data['used_follow_ups']:
                current_q = follow_up
                interview_data['used_follow_ups'].append(current_q)
                interview_data['follow_up_count'] += 1
                is_follow_up = True
                break

    # Main question logic
    if not current_q:
        while interview_data['current_question'] < len(interview_data['questions']):
            idx = interview_data['current_question']
            q = interview_data['questions'][idx]
            if q not in interview_data['used_questions']:
                current_q = q
                interview_data['used_questions'].append(current_q)
                interview_data['current_topic'] = interview_data['question_topics'][idx]
                interview_data['follow_up_count'] = 0
                interview_data['current_question'] += 1
                is_follow_up = False
                break
            else:
                interview_data['current_question'] += 1

    if not current_q:
        logger.info("✅ All questions completed.")
        return jsonify({"status": "completed"}), 200

    # Log and store question
    logger.info(f"🎤 Serving {'follow-up' if is_follow_up else 'main'} question: {current_q}")
    interview_data['conversation_history'].append({"speaker": "bot", "text": current_q})
    save_conversation_to_file([{"speaker": "bot", "text": current_q}])
    interview_data['last_activity_time'] = datetime.now(timezone.utc)

    # Save session safely
    session['interview_data'] = interview_data
    session.modified = True

    # Text to speech
    try:
        audio_data = text_to_speech(current_q)
    except Exception as e:
        logger.error(f"🔊 TTS failed: {str(e)}")
        audio_data = None

    return jsonify({
        "status": "success",
        "question": current_q,
        "audio": audio_data,
        "question_number": interview_data['current_question'],
        "total_questions": len(interview_data['questions']),
        "is_follow_up": is_follow_up
    }), 200
