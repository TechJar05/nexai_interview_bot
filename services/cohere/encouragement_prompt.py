# import logging
# import cohere
# from config import Config

# logger = logging.getLogger(__name__)

# # Initialize Cohere client with API key from config
# co = cohere.Client(Config.COHERE_API_KEY)


# import logging
# import cohere
# from config import Config

# logger = logging.getLogger(__name__)

# # Initialize Cohere client
# co = cohere.Client(Config.COHERE_API_KEY)


# def generate_encouragement_prompt(conversation_history):
#     """
#     Generate a brief encouragement prompt if the user has paused too long during the interview.
#     """
#     logger.debug("Generating encouragement prompt for paused candidate")

#     try:
#         prompt = f"""
#         The candidate has paused during their response. Generate a brief, encouraging prompt to:
#         - Help them continue their thought
#         - Reference specific aspects of their previous answers
#         - Be supportive and professional
#         - Be concise (one short sentence)
        
#         Current conversation context:
#         {conversation_history[-2:]}
        
#         Return ONLY the prompt, nothing else.
#         """

#         response = co.generate(
#             model="command-r-plus",
#             prompt=prompt,
#             max_tokens=300,
#             temperature=0.5
#         )

#         encouragement = response.generations[0].text.strip()
#         logger.debug(f"Generated encouragement: {encouragement}")
#         return encouragement

#     except Exception as e:
#         logger.error(f"Error generating encouragement prompt: {str(e)}", exc_info=True)
#         return "Please continue with your thought."





import logging
from openai import OpenAI
from config import Config
from services.cohere.client import client  
logger = logging.getLogger(__name__)

# Initialize OpenAI client with API key from config
client = OpenAI(api_key=Config.OPENAI_API_KEY)


def generate_encouragement_prompt(conversation_history):
    """
    Generate a brief encouragement prompt if the user has paused too long during the interview.
    """
    logger.debug("Generating encouragement prompt for paused candidate")

    try:
        # Get the last two messages from the candidate
        context_snippet = "\n".join(
            f"{msg['speaker'].capitalize()}: {msg['text']}" for msg in conversation_history[-2:]
        )

        prompt = f"""
The candidate has paused during their response. Generate a brief, encouraging prompt to:
- Help them continue their thought
- Reference specific aspects of their previous answers
- Be supportive and professional
- Be concise (one short sentence)

Current conversation context:
{context_snippet}

Return ONLY the prompt, nothing else.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" / "gpt-4o" if available
            messages=[
                {"role": "system", "content": "You are an AI interviewer helping the candidate stay comfortable."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=100
        )

        encouragement = response.choices[0].message.content.strip()
        logger.debug(f"Generated encouragement: {encouragement}")
        return encouragement

    except Exception as e:
        logger.error(f"Error generating encouragement prompt: {str(e)}", exc_info=True)
        return "Please continue with your thought."
