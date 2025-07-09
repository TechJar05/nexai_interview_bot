import logging
import re

logger = logging.getLogger(__name__)


def extract_topic(question):
    logger.debug(f"Extracting topic from question: {question}")
    question = question.lower()
    if 'tell me about' in question:
        return question.split('tell me about')[-1].strip(' ?')
    elif 'describe' in question:
        return question.split('describe')[-1].strip(' ?')
    elif 'explain' in question:
        return question.split('explain')[-1].strip(' ?')
    elif 'what' in question:
        return question.split('what')[-1].strip(' ?')
    elif 'how' in question:
        return question.split('how')[-1].strip(' ?')
    return question.split('?')[0].strip()


def parse_questions(raw):
    questions = []
    topics = []

    question_blocks = re.split(r'\n\d+\.\s+Question:\s+', raw)
    for block in question_blocks[1:]:
        parts = block.strip().split("Follow-ups:")
        main_question = parts[0].strip()

        follow_ups = []
        if len(parts) > 1:
            follow_up_lines = parts[1].strip().split("\n")
            for line in follow_up_lines:
                line = line.strip()
                match = re.match(r'\d+\.\s*\|\s*(.+)', line)
                if match:
                    follow_ups.append(match.group(1))

        questions.append({
            "main": main_question,
            "follow_ups": follow_ups
        })
        topics.append("general")  # Or customize topic logic if needed

    return questions, topics
