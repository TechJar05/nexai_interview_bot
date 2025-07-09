# # services/scoring_service.py

# import logging
# from services.cohere.client import co

# logger = logging.getLogger(__name__)

# def evaluate_response(answer: str, question: str, role: str, experience_level: str, visual_feedback: str = None) -> float:
#     """
#     Evaluates a candidate's answer to an interview question using Cohere.
#     Returns a score between 1 and 10 based on relevance, clarity, and professionalism.
#     """

#     logger.debug(f"Evaluating response for question: {question[:50]}...")

#     answer = answer.strip()

#     if len(answer) < 20:
#         logger.debug("Answer too short, returning 2")
#         return 2.0
#     elif len(answer) < 50:
#         logger.debug("Short but acceptable answer, returning 4")
#         return 4.0

#     # Compose prompt
#     rating_prompt = f"""
# You are assessing an interview response for a {role} position from a {experience_level} candidate.

# Question: "{question}"
# Answer: "{answer}"

# Evaluate the answer based on the following *five criteria*, each rated from 1 to 10:
# 1. Relevance
# 2. Knowledge depth
# 3. Clarity
# 4. Use of examples
# 5. Professionalism

# Also consider the candidate's visual feedback (if available): "{visual_feedback or 'N/A'}"

# Only return the output in the following strict *JSON format*:

# {{
#   "relevance": <score>,
#   "knowledge_depth": <score>,
#   "clarity": <score>,
#   "examples": <score>,
#   "professionalism": <score>,
#   "final_rating": <weighted_average_score>,
#   "answer_quality": "<classification_text>"
# }}
# """

#     try:
#         response = co.generate(
#             model="command-r-plus",
#             prompt=rating_prompt,
#             max_tokens=150,
#             temperature=0.3
#         )
#         rating_text = response.generations[0].text.strip()

#         # Attempt to extract the final rating score
#         import re
#         import json

#         try:
#             rating_json = json.loads(rating_text)
#             final_rating = float(rating_json.get("final_rating", 5))
#             final_rating = max(1.0, min(10.0, final_rating))
#             logger.debug(f"Extracted structured rating: {final_rating}")
#             return final_rating
#         except Exception as parse_err:
#             logger.warning(f"Failed to parse JSON rating, fallback attempt. Raw text: {rating_text}")
#             match = re.search(r'"final_rating"\s*:\s*(\d+(\.\d+)?)', rating_text)
#             if match:
#                 fallback_rating = float(match.group(1))
#                 return max(1.0, min(10.0, fallback_rating))

#             logger.warning("Could not extract rating value. Returning default: 5.0")
#             return 5.0

#     except Exception as e:
#         logger.error(f"Error evaluating response: {str(e)}", exc_info=True)
#         return 5.0




# services/scoring_service.py

import logging
import json
import re
from services.cohere.client import client  # OpenAI client

logger = logging.getLogger(__name__)

def evaluate_response(answer: str, question: str, role: str, experience_level: str, visual_feedback: str = None) -> float:
    """
    Evaluates a candidate's answer using OpenAI and returns a score from 1 to 10.
    """

    logger.debug(f"Evaluating response for question: {question[:60]}...")

    # System-level instruction for OpenAI
    system_instruction = """
You are an expert AI interviewer.

Score the candidate's answer strictly based on these 5 criteria:
1. Relevance
2. Knowledge depth
3. Clarity
4. Use of examples
5. Professionalism

Return ONLY this valid JSON:
{
  "relevance": <1-10>,
  "knowledge_depth": <1-10>,
  "clarity": <1-10>,
  "examples": <1-10>,
  "professionalism": <1-10>,
  "final_rating": <average as float>,
  "answer_quality": "<Excellent|Good|Average|Poor>"
}

DO NOT explain or add any comments outside the JSON.
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
            temperature=0.3
        )

        rating_text = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI raw rating:\n{rating_text}")

        # Attempt to parse JSON output
        try:
            rating_json = json.loads(rating_text)
            final_score = float(rating_json.get("final_rating", 5))
            return max(1.0, min(10.0, final_score))
        except json.JSONDecodeError:
            match = re.search(r'"final_rating"\s*:\s*(\d+(\.\d+)?)', rating_text)
            if match:
                fallback = float(match.group(1))
                return max(1.0, min(10.0, fallback))
            logger.warning("Could not parse rating JSON. Returning 5.0")
            return 5.0

    except Exception as e:
        logger.error(f"Error in evaluate_response: {str(e)}", exc_info=True)
        return 5.0
