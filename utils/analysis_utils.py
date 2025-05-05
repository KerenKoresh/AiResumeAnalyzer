from src.match_analysis import analyze_match
from utils.email_utils import send_email
from utils.pdf_utils import extract_text_from_pdf
import streamlit as st
import logging
logger = logging.getLogger("AIResumeAnalyzer")


def analyze_resume(uploaded_file, job_description, email_address):
    """Performs the resume analysis and optionally sends an email."""
    resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text.strip():
        st.error("❌ No text found in the PDF file. Please ensure the file is valid.")
        logger.error("No text found in the PDF file.")
        return

    result = analyze_match(resume_text, job_description)
    st.markdown("### 🧾 Analysis Results")
    st.markdown(result)
    if email_address:
        send_email("Resume Match Analysis", result, email_address)
