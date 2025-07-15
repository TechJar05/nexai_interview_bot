



# # services/scoring_service.py

# import logging
# import json
# import re
# from services.cohere.client import client  # OpenAI client

# logger = logging.getLogger(__name__)

# def evaluate_response(answer: str, question: str, role: str, experience_level: str, visual_feedback: str = None) -> float:
#     """
#     Evaluates a candidate's answer using OpenAI and returns a score from 1 to 10.
#     """

#     logger.debug(f"Evaluating response for question: {question[:60]}...")

#     # System-level instruction for OpenAI
#     system_instruction = """
# You are an expert AI interviewer.

# Score the candidate's answer strictly based on these 5 criteria:
# 1. Relevance
# 2. Knowledge depth
# 3. Clarity
# 4. Use of examples
# 5. Professionalism

# Return ONLY this valid JSON:
# {
#   "relevance": <1-10>,
#   "knowledge_depth": <1-10>,
#   "clarity": <1-10>,
#   "examples": <1-10>,
#   "professionalism": <1-10>,
#   "final_rating": <average as float>,
#   "answer_quality": "<Excellent|Good|Average|Poor>"
# }

# DO NOT explain or add any comments outside the JSON.
# """

#     user_prompt = f"""
# Evaluate the answer below for a {role} ({experience_level}) interview.

# Question: "{question}"
# Answer: "{answer.strip()}"
# Visual feedback: "{visual_feedback or 'N/A'}"

# Return only valid JSON.
# """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": system_instruction},
#                 {"role": "user", "content": user_prompt}
#             ],
#             max_tokens=300,
#             temperature=0.3
#         )

#         rating_text = response.choices[0].message.content.strip()
#         logger.debug(f"OpenAI raw rating:\n{rating_text}")

#         # Attempt to parse JSON output
#         try:
#             rating_json = json.loads(rating_text)
#             final_score = float(rating_json.get("final_rating", 5))
#             return max(1.0, min(10.0, final_score))
#         except json.JSONDecodeError:
#             match = re.search(r'"final_rating"\s*:\s*(\d+(\.\d+)?)', rating_text)
#             if match:
#                 fallback = float(match.group(1))
#                 return max(1.0, min(10.0, fallback))
#             logger.warning("Could not parse rating JSON. Returning 5.0")
#             return 5.0

#     except Exception as e:
#         logger.error(f"Error in evaluate_response: {str(e)}", exc_info=True)
#         return 5.0








# services/scoring_service.py

import logging
import json
import re
from services.cohere.client import client  # Replace with OpenAI client if not Cohere

logger = logging.getLogger(__name__)

def evaluate_response(answer: str, question: str, role: str, experience_level: str, visual_feedback: str = None) -> float:
    """
    Evaluates a candidate's answer using OpenAI and returns a score from 1 to 10.
    """

    logger.debug(f"Evaluating response for question: {question[:60]}...")

    # Updated, anchored scoring instruction
    system_instruction = """
You are an expert AI interviewer scoring candidate answers for a professional interview.

You must evaluate the answer based on **5 real-world criteria**, using the following rules:

===========================
🎯 SCORING RUBRIC (1–10):

10 = Outstanding — perfect response, fully relevant, deep insight, highly professional, real examples.
8–9 = Strong — clearly answered, confident, insightful, solid examples.
6–7 = Average — reasonably clear, some knowledge, maybe vague or missing examples.
4–5 = Weak — lacks clarity, off-topic, superficial knowledge.
1–3 = Very Poor — incoherent, irrelevant, lacks professionalism.
===========================

Evaluate based on:
1. Relevance to the question
2. Knowledge depth and accuracy
3. Clarity of expression
4. Use of real examples or scenarios
5. Professionalism of tone and structure

Then compute a `final_rating` as the average of the 5 scores.

🚫 Only return this strict JSON format:
{
  "relevance": <1-10>,
  "knowledge_depth": <1-10>,
  "clarity": <1-10>,
  "examples": <1-10>,
  "professionalism": <1-10>,
  "final_rating": <average as float>,
  "answer_quality": "<Excellent|Good|Average|Poor>"
}

🚫 Do NOT explain or add text outside the JSON.
"""

    user_prompt = f"""
Evaluate the answer below for a {role} ({experience_level}) interview.

Question: "{question}"
Answer: "{answer.strip()}"
Visual feedback: "{visual_feedback or 'N/A'}"

Return only valid JSON.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.3  # Low temperature = consistent scoring
        )

        rating_text = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI raw rating:\n{rating_text}")

        try:
            rating_json = json.loads(rating_text)
            final_score = float(rating_json.get("final_rating", 5))
            logger.info(f"Extracted final rating: {final_score}")
            return max(1.0, min(10.0, final_score))  # Clamp between 1–10

        except json.JSONDecodeError:
            logger.warning("Failed JSON parsing. Trying regex fallback.")
            match = re.search(r'"final_rating"\s*:\s*(\d+(\.\d+)?)', rating_text)
            if match:
                fallback = float(match.group(1))
                logger.info(f"Fallback extracted score: {fallback}")
                return max(1.0, min(10.0, fallback))

            logger.error("Could not extract rating. Returning default 5.0")
            return 5.0

    except Exception as e:
        logger.error(f"Error in evaluate_response: {str(e)}", exc_info=True)
        return 5.0
