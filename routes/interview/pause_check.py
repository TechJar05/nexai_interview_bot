from flask import Blueprint, jsonify, session
from datetime import datetime, timezone
import logging

from utils.helpers import init_interview_data
from services.cohere.encouragement_prompt import generate_encouragement_prompt
from services.tts_service import text_to_speech

logger = logging.getLogger(__name__)
pause_bp = Blueprint('pause_bp', __name__)

PAUSE_THRESHOLD = 40  # seconds


@pause_bp.route('/check_pause', methods=['GET'])
def check_pause():
    logger.debug("Check pause request received")

    interview_data = session.get('interview_data', init_interview_data())

    if not interview_data.get('interview_started', False):
        logger.warning("Pause check attempted before interview started")
        return jsonify({"status": "not_started"})

    current_time = datetime.now(timezone.utc)
    last_activity = interview_data.get('last_activity_time', current_time)
    seconds_since_last = (current_time - last_activity).total_seconds()

    logger.debug(f"Seconds since last activity: {seconds_since_last}")

    if seconds_since_last > PAUSE_THRESHOLD:
        logger.info(f"Pause detected ({seconds_since_last:.2f}s), generating encouragement prompt")

        encouragement = generate_encouragement_prompt(interview_data['conversation_history'])
        audio_data = text_to_speech(encouragement)

        interview_data['last_activity_time'] = current_time
        session['interview_data'] = interview_data

        return jsonify({
            "status": "pause_detected",
            "prompt": encouragement,
            "audio": audio_data
        })

    return jsonify({"status": "active"})
