from datetime import datetime, timezone

def create_text_report_from_interview_data(interview_data):
    candidate = interview_data.get('candidate_name', 'Unknown Candidate')
    role = interview_data.get('role', 'Unknown Role')
    exp_level = interview_data.get('experience_level', 'Unknown')
    years = interview_data.get('years_experience', 0)

    conv_history = interview_data.get("conversation_history", [])

    # Format conversation as Q&A with optional feedback
    conversation_lines = []
    i = 0
    n = len(conv_history)
    question_counter = 1
    while i < n:
        # Bot's question
        q_item = conv_history[i]
        if q_item.get("speaker", "").lower() == "bot":
            question_text = q_item.get("text", "")
            conversation_lines.append(f"Q{question_counter}: {question_text}")
        else:
            i += 1
            continue

        # User's answer
        if i + 1 < n:
            a_item = conv_history[i + 1]
            if a_item.get("speaker", "").lower() == "user":
                answer_text = a_item.get("text", "")
                conversation_lines.append(f"Response: {answer_text}")
                feedback = a_item.get("feedback_label")
                if feedback:
                    conversation_lines.append(f"  → Feedback: {feedback}")
        question_counter += 1
        i += 2  # Move to next Q&A pair

    conversation_text = "\n".join(conversation_lines)

    # Ratings summary
    ratings = interview_data.get('ratings', [])
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    if avg_rating >= 8:
        performance = "High"
    elif avg_rating >= 6:
        performance = "Moderate"
    elif avg_rating >= 4:
        performance = "Low"
    else:
        performance = "Poor"

    # Duration
    duration = "N/A"
    if interview_data.get('start_time') and interview_data.get('end_time'):
        duration_seconds = (interview_data['end_time'] - interview_data['start_time']).total_seconds()
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        duration = f"{minutes}m {seconds}s"

    # Final Report String
    report_txt = f"""
Interview Report for {candidate}
Role: {role}


Interview Duration: {duration}
Average Rating: {avg_rating:.1f}/10
Overall Performance: {performance}

Conversation Transcript with Feedback:
{conversation_text}

End of Report
""".strip()

    return report_txt
