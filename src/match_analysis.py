from utils.openai_utils import get_match_analysis
from utils.file_utils import save_previous_data
import logging

logger = logging.getLogger("AIResumeAnalyzer")


def analyze_match(resume_text, job_description):
    try:
        result = get_match_analysis(resume_text, job_description)
        save_previous_data(resume_text, job_description)
        logging.info("🔔 Match analysis completed successfully.")
        return result
    except Exception as e:
        logging.error(f"Error during match analysis: {e}")
        raise e  # חוזר עם שגיאה למעלה
