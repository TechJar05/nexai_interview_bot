# from flask import Blueprint, request, jsonify, session
# from datetime import datetime, timezone
# import logging

# from utils.helpers import init_interview_data
# from services.cohere.question_generator import generate_initial_questions

# start_bp = Blueprint('start_bp', __name__)

# logger = logging.getLogger(__name__)

# @start_bp.route('/start_interview', methods=['POST'])
# def start_interview():
#     logger.info("Interview start request received")

#     data = request.get_json()
#     resume_text = data.get('resume_text', '')
#     jd_text = data.get('jd_text', '')
#     candidate_name = data.get('fileName', 'Candidate').split('.')[0].replace('_', ' ').replace('-', ' ')

#     # Initialize session
#     session['interview_data'] = init_interview_data()
#     interview_data = session['interview_data']

#     # Set interview parameters
#     interview_data['role'] = data.get('role', 'Software Engineer')
#     interview_data['experience_level'] = data.get('experience_level', 'fresher')
#     interview_data['years_experience'] = int(data.get('years_experience', 0))
#     interview_data['resume'] = resume_text
#     interview_data['jd'] = jd_text
#     interview_data['candidate_name'] = candidate_name
#     interview_data['start_time'] = datetime.now(timezone.utc)
#     interview_data['last_activity_time'] = datetime.now(timezone.utc)

#     logger.debug(f"Interview parameters set - Role: {interview_data['role']}, "
#                  f"Experience: {interview_data['experience_level']}, "
#                  f"Years: {interview_data['years_experience']}")

#     try:
#         questions, question_topics = generate_initial_questions(
#             interview_data['role'],
#             interview_data['experience_level'],
#             interview_data['years_experience'],
#             resume_text=resume_text,
#             jd_text=jd_text
#         )

#         interview_data['questions'] = [q["main"] for q in questions]
#         interview_data['follow_up_questions'] = []
#         interview_data['question_topics'] = question_topics

#         for q in questions:
#             interview_data['conversation_history'].append({
#                 "question": q["main"],
#                 "prepared_follow_ups": q["follow_ups"]
#             })

#         interview_data['interview_started'] = True
#         session['interview_data'] = interview_data

#         return jsonify({
#             "status": "started",
#             "total_questions": len(interview_data['questions']),
#             "welcome_message": f"Welcome to the interview for {interview_data['role']} position."
#         })

#     except Exception as e:
#         logger.error(f"Error starting interview: {str(e)}", exc_info=True)
#         return jsonify({"status": "error", "message": str(e)}), 500



from flask import Blueprint, request, jsonify, session
from datetime import datetime, timezone
import logging

from utils.helpers import init_interview_data
from services.cohere.question_generator import generate_initial_questions  # ✅ updated import (migrated from cohere)

start_bp = Blueprint('start_bp', __name__)
logger = logging.getLogger(__name__)

@start_bp.route('/start_interview', methods=['POST'])
def start_interview():
    logger.info("Interview start request received")

    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        jd_text = data.get('jd_text', '')
        candidate_name = data.get('fileName', 'Candidate').split('.')[0].replace('_', ' ').replace('-', ' ')

        # Initialize session
        session['interview_data'] = init_interview_data()
        interview_data = session['interview_data']

        # Set interview parameters
        interview_data['role'] = data.get('role', 'Software Engineer')
        interview_data['experience_level'] = data.get('experience_level', 'fresher')
        interview_data['years_experience'] = int(data.get('years_experience', 0))
        interview_data['resume'] = resume_text
        interview_data['jd'] = jd_text
        interview_data['candidate_name'] = candidate_name
        interview_data['start_time'] = datetime.now(timezone.utc)
        interview_data['last_activity_time'] = datetime.now(timezone.utc)

        logger.debug(f"Interview parameters set - Role: {interview_data['role']}, "
                     f"Experience: {interview_data['experience_level']}, "
                     f"Years: {interview_data['years_experience']}")

        # Generate interview questions using OpenAI
        questions, question_topics = generate_initial_questions(
            role=interview_data['role'],
            experience_level=interview_data['experience_level'],
            years_experience=interview_data['years_experience'],
            resume_text=resume_text,
            jd_text=jd_text
        )

        # Save questions to session
        interview_data['questions'] = [q["main"] for q in questions]
        interview_data['follow_up_questions'] = []
        interview_data['question_topics'] = question_topics

        for q in questions:
            interview_data['conversation_history'].append({
                "question": q["main"],
                "prepared_follow_ups": q["follow_ups"]
            })

        interview_data['interview_started'] = True
        session['interview_data'] = interview_data

        logger.info("Interview session initialized successfully.")
        return jsonify({
            "status": "started",
            "total_questions": len(interview_data['questions']),
            "welcome_message": f"Welcome to the interview for {interview_data['role']} position."
        })

    except Exception as e:
        logger.error(f"Error starting interview: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"Failed to start interview: {str(e)}"
        }), 500
