import os
from datetime import datetime, timezone
from services.report.formatter import create_text_report_from_interview_data
import os
import logging
from utils.file_utils import html_to_pdf

logger = logging.getLogger(__name__)

def save_admin_report_txt(interview_data):
    # Generate report content
    report_txt = create_text_report_from_interview_data(interview_data)

    # File naming
    candidate = interview_data.get("candidate_name", "unknown").replace(" ", "_")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{candidate}_interview_report_{timestamp}.txt"

    # Directory path
    reports_folder = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)

    # Save file
    filepath = os.path.join(reports_folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_txt)

    return filepath, filename
