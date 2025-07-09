



# import logging
# from datetime import datetime
# from openai import OpenAI
# from config import Config
# from services.tts_service import text_to_speech
# from utils.file_utils import html_to_pdf
# from services.cohere.client import client  
# logger = logging.getLogger(__name__)

# # Initialize OpenAI client
# client = OpenAI(api_key=Config.OPENAI_API_KEY)


# def generate_interview_report(interview_data):
#     try:
#         # Calculate interview duration
#         duration = "N/A"
#         if interview_data['start_time'] and interview_data['end_time']:
#             duration_seconds = (interview_data['end_time'] - interview_data['start_time']).total_seconds()
#             minutes = int(duration_seconds // 60)
#             seconds = int(duration_seconds % 60)
#             duration = f"{minutes}m {seconds}s"

#         # Calculate average rating
#         ratings = interview_data.get('ratings', [])
#         avg_rating = sum(ratings) / len(ratings) if ratings else 0
#         logger.debug(f"Average rating: {avg_rating:.1f}, based on {len(ratings)} ratings")

#         # Determine status based on average rating
#         if avg_rating >= 7:
#             status_class = "selected"
#         elif 4 <= avg_rating < 7:
#             status_class = "onhold"
#         else:
#             status_class = "rejected"

#         # Skill distribution
#         questions = interview_data.get('questions', [])
#         question_topics = interview_data.get('question_topics', [])
#         technical_scores, communication_scores, behavioral_scores = [], [], []

#         for i, (question, topic, rating) in enumerate(zip(questions, question_topics, ratings)):
#             topic_lower = topic.lower() if topic else ""
#             if "technical" in topic_lower or i < 10:
#                 technical_scores.append(rating)
#             elif "experience" in topic_lower or "role" in topic_lower or i < 15:
#                 behavioral_scores.append(rating)
#             communication_scores.append(rating * 0.4)

#         technical_avg = sum(technical_scores) / len(technical_scores) if technical_scores else 5
#         behavioral_avg = sum(behavioral_scores) / len(behavioral_scores) if behavioral_scores else 5
#         communication_avg = sum(communication_scores) / len(communication_scores) if communication_scores else 5
#         logger.debug(f"Skill averages - Technical: {technical_avg:.1f}, Communication: {communication_avg:.1f}, Behavioral: {behavioral_avg:.1f}")

#         total = max(technical_avg + communication_avg + behavioral_avg, 0.01)
#         technical_pct = (technical_avg / total) * 100
#         communication_pct = (communication_avg / total) * 100
#         behavioral_pct = 100 - technical_pct - communication_pct
#         logger.debug(f"Skill percentages - Technical: {technical_pct:.1f}%, Communication: {communication_pct:.1f}%, Behavioral: {behavioral_pct:.1f}%")

#         # Bar chart HTML
#         bar_chart_html = f"""
#         <div style="font-family: Arial, sans-serif; max-width: 400px; margin: 20px auto;">
#             <h4 style="text-align: center;">Skill Distribution</h4>
#             <div style="margin-bottom: 15px;">
#                 <span style="display: inline-block; width: 120px; font-weight: bold;">Technical 🛠</span>
#                 <div style="display: inline-block; width: 200px; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;">
#                     <div style="width: {min(technical_pct, 100)}%; background-color: #4CAF50; height: 20px;"></div>
#                 </div>
#                 <span style="margin-left: 10px;">{technical_pct:.1f}%</span>
#             </div>
#             <div style="margin-bottom: 15px;">
#                 <span style="display: inline-block; width: 120px; font-weight: bold;">Communication 🗣</span>
#                 <div style="display: inline-block; width: 200px; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;">
#                     <div style="width: {min(communication_pct, 100)}%; background-color: #2196F3; height: 20px;"></div>
#                 </div>
#                 <span style="margin-left: 10px;">{communication_pct:.1f}%</span>
#             </div>
#             <div style="margin-bottom: 15px;">
#                 <span style="display: inline-block; width: 120px; font-weight: bold;">Behavioral 🤝</span>
#                 <div style="display: inline-block; width: 200px; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;">
#                     <div style="width: {min(behavioral_pct, 100)}%; background-color: #FFC107; height: 20px;"></div>
#                 </div>
#                 <span style="margin-left: 10px;">{behavioral_pct:.1f}%</span>
#             </div>
#         </div>
#         """

#         conversation_history_text = "\n".join([
#             f"{item['speaker']}: {item['text']}"
#             for item in interview_data['conversation_history']
#             if 'speaker' in item
#         ])

#         # Create report prompt
#         report_prompt = f"""
# You are an expert AI HR assistant. Create an HTML interview evaluation report for a candidate applying for the role of {interview_data['role']}.


# Interview Duration: {duration}
# Average Rating: {avg_rating:.1f}/10

# Transcript:
# {conversation_history_text}

# Bar Chart:
# {bar_chart_html}

# Instructions:
# 1. Write clean semantic HTML only.
# 2. Use <h2>, <table>, and <ul> appropriately.
# 3. Include sections: Interview Summary, Key Strengths (table), Areas for Improvement (table), Visual Analysis (chart + ratings), Overall Recommendation (with ✅ or ❌).
# 4. DO NOT use markdown or external CSS.
# """

#         # Generate report using OpenAI
#         logger.debug("Sending prompt to OpenAI for HTML report generation")
#         report_response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a professional HTML interview report writer."},
#                 {"role": "user", "content": report_prompt}
#             ],
#             max_tokens=2000,
#             temperature=0.5
#         )

#         report_content = report_response.choices[0].message.content.strip()

#         # Generate voice summary
#         voice_prompt = f"""
# Summarize this interview report in 5–6 lines of spoken feedback:
# {report_content}

# Make it:
# - Conversational
# - Clear
# - Honest and positive
# """

#         logger.debug("Sending prompt to OpenAI for voice feedback")
#         voice_response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a professional voice assistant giving summary feedback."},
#                 {"role": "user", "content": voice_prompt}
#             ],
#             max_tokens=300,
#             temperature=0.5
#         )

#         voice_feedback = voice_response.choices[0].message.content.strip()
#         logger.debug("Voice feedback generated")

#         voice_audio = text_to_speech(voice_feedback)

#         return {
#             "status": "success",
#             "report": report_content,
#             "voice_feedback": voice_feedback,
#             "voice_audio": voice_audio,
#             "status_class": status_class,
#             "avg_rating": avg_rating,
#             "duration": duration
#         }

#     except Exception as e:
#         logger.error(f"Error generating report: {str(e)}", exc_info=True)
#         return {
#             "status": "error",
#             "message": str(e),
#             "report": "<p>Error generating report. Please try again.</p>",
#             "voice_feedback": "We encountered an error generating your feedback.",
#             "voice_audio": None
#         }




import logging
import os
from datetime import datetime
from openai import OpenAI
from config import Config
from services.tts_service import text_to_speech
from utils.file_utils import html_to_pdf

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_interview_report(interview_data):
    try:
        # Calculate interview duration
        duration = "N/A"
        if interview_data['start_time'] and interview_data['end_time']:
            duration_seconds = (interview_data['end_time'] - interview_data['start_time']).total_seconds()
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            duration = f"{minutes}m {seconds}s"

        # Calculate average rating
        ratings = interview_data.get('ratings', [])
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        logger.debug(f"Average rating: {avg_rating:.1f}, based on {len(ratings)} ratings")

        # Determine status based on average rating
        if avg_rating >= 7:
            status_class = "selected"
        elif 4 <= avg_rating < 7:
            status_class = "onhold"
        else:
            status_class = "rejected"

        # Skill distribution
        questions = interview_data.get('questions', [])
        question_topics = interview_data.get('question_topics', [])
        technical_scores, communication_scores, behavioral_scores = [], [], []

        for i, (question, topic, rating) in enumerate(zip(questions, question_topics, ratings)):
            topic_lower = topic.lower() if topic else ""
            if "technical" in topic_lower or i < 10:
                technical_scores.append(rating)
            elif "experience" in topic_lower or "role" in topic_lower or i < 15:
                behavioral_scores.append(rating)
            communication_scores.append(rating * 0.4)

        technical_avg = sum(technical_scores) / len(technical_scores) if technical_scores else 5
        behavioral_avg = sum(behavioral_scores) / len(behavioral_scores) if behavioral_scores else 5
        communication_avg = sum(communication_scores) / len(communication_scores) if communication_scores else 5

        total = max(technical_avg + communication_avg + behavioral_avg, 0.01)
        technical_pct = (technical_avg / total) * 100
        communication_pct = (communication_avg / total) * 100
        behavioral_pct = 100 - technical_pct - communication_pct

        # Bar chart HTML
        bar_chart_html = f"""
        <div style=\"font-family: Arial, sans-serif; max-width: 400px; margin: 20px auto;\">
            <h4 style=\"text-align: center;\">Skill Distribution</h4>
            <div style=\"margin-bottom: 15px;\">
                <span style=\"display: inline-block; width: 120px; font-weight: bold;\">Technical 🛠</span>
                <div style=\"display: inline-block; width: 200px; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;\">
                    <div style=\"width: {min(technical_pct, 100)}%; background-color: #4CAF50; height: 20px;\"></div>
                </div>
                <span style=\"margin-left: 10px;\">{technical_pct:.1f}%</span>
            </div>
            <div style=\"margin-bottom: 15px;\">
                <span style=\"display: inline-block; width: 120px; font-weight: bold;\">Communication 🗣</span>
                <div style=\"display: inline-block; width: 200px; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;\">
                    <div style=\"width: {min(communication_pct, 100)}%; background-color: #2196F3; height: 20px;\"></div>
                </div>
                <span style=\"margin-left: 10px;\">{communication_pct:.1f}%</span>
            </div>
            <div style=\"margin-bottom: 15px;\">
                <span style=\"display: inline-block; width: 120px; font-weight: bold;\">Behavioral 🤝</span>
                <div style=\"display: inline-block; width: 200px; background-color: #e0e0e0; border-radius: 5px; overflow: hidden;\">
                    <div style=\"width: {min(behavioral_pct, 100)}%; background-color: #FFC107; height: 20px;\"></div>
                </div>
                <span style=\"margin-left: 10px;\">{behavioral_pct:.1f}%</span>
            </div>
        </div>
        """

        conversation_history_text = "\n".join([
            f"{item['speaker']}: {item['text']}"
            for item in interview_data['conversation_history']
            if 'speaker' in item
        ])

        report_prompt = f"""
You are an expert HTML report writer. Generate a clean and semantic HTML report for a candidate applying for the role of {interview_data['role']}.

Sections:
- <h2>Interview Summary</h2>
- <h2>Key Strengths</h2>: Table with <th>Aspect</th> and <th>Details</th>
- <h2>Areas for Improvement</h2>: Table with <th>Aspect</th> and <th>Suggestions</th>
- <h2>Skill Distribution</h2>: Use this chart:
{bar_chart_html}
- <h2>Overall Recommendation</h2>: Include ✅ or ❌ with a brief explanation

Transcript:
{conversation_history_text}

End with: <p><strong>Generated by AI Interview Assistant</strong></p>
"""

        report_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You generate professional HTML reports."},
                {"role": "user", "content": report_prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )

        report_content = report_response.choices[0].message.content.strip()
        logger.debug("Generated HTML Report:\n" + report_content)

        # Save to PDF
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"interview_report_{timestamp}.pdf"
        pdf_path = os.path.join("./reports", pdf_filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        html_to_pdf(report_content, pdf_path)

        # Generate voice summary
        voice_prompt = f"Summarize this interview report in 5–6 spoken lines:\n{report_content}"
        voice_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize interviews as voice feedback."},
                {"role": "user", "content": voice_prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        voice_feedback = voice_response.choices[0].message.content.strip()
        voice_audio = text_to_speech(voice_feedback)

        return {
            "status": "success",
            "report": report_content,
            "report_pdf_path": pdf_path,
            "voice_feedback": voice_feedback,
            "voice_audio": voice_audio,
            "status_class": status_class,
            "avg_rating": avg_rating,
            "duration": duration
        }

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e),
            "report": "<p>Error generating report. Please try again.</p>",
            "voice_feedback": "We encountered an error generating your feedback.",
            "voice_audio": None
        }
