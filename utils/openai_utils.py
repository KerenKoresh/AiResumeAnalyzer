import os
import openai
from dotenv import load_dotenv
import logging
import streamlit as st

load_dotenv()

openai.api_key = st.secrets["OPENAI_API_KEY"]
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )

        print(response)  # הדפסה לעזור לך לראות את התשובה המתקבלת

        # אם התגובה מכילה את המפתח 'choices' ומבנה התשובה לא תקין
        if 'choices' not in response or len(response['choices']) == 0:
            logger.error(f"Unexpected response format: {response}")
            raise KeyError("The response does not contain expected 'choices' key.")

        # אם כל המפתחות קיימים ומבנה התשובה תקין
        return response['choices'][0]['message']['content']

    except KeyError as ke:
        logger.error(f"KeyError: {ke}")
        raise ke  # זרוק את השגיאה
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        raise e
