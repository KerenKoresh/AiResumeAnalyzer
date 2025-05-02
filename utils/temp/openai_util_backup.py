import os

import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_match_analysis(resume_text, job_description):
    prompt = f"""
You are an expert job recruiter AI.
Analyze the following resume and job description.
Give a match score (out of 100) and explain what fits well and what is missing.

Resume:
{resume_text}

Job Description:
{job_description}

Give output in this format:
Match Score: XX%
Strengths: ...
Weaknesses: ...
Suggestions: ...
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for job matching."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # מחזיר את הטקסט של התשובה
    return response.choices[0].message["content"]
