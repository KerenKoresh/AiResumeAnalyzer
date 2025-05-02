from utils.openai_utils import get_match_analysis
from utils.file_utils import save_previous_data


def analyze_match(resume_text, job_description):
    result = get_match_analysis(resume_text, job_description)
    save_previous_data(resume_text, job_description)
    return result
