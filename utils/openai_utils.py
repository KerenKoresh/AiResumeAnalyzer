import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
logger = logging.getLogger("AIResumeAnalyzer")
def load_system_prompt():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "cv_analyzer_prompt.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_match_analysis(resume_text, job_description):
    system_prompt = load_system_prompt()

    user_input = f"""Here is my resume:\n{resume_text}\n\nAnd here is the job description:\n{job_description}"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # מומלץ GPT-4 לפרומפטים מורכבים
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        logger.info("🔔 Analysis completed by OpenAI API.")
        return response.choices[0].message["content"]
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        raise e
