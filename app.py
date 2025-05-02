import logging
import streamlit as st
from src.match_analysis import analyze_match
from utils.email_utils import send_email
from utils.logging_utils import init_logger
from utils.pdf_utils import extract_text_from_pdf

# Creating a specific logger for the application
logger = logging.getLogger("AIResumeAnalyzer")


def setup():
    """Initializes UI and logger."""
    if "initialized_ui" not in st.session_state:
        st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
        st.session_state["initialized_ui"] = True

    if not st.session_state.get("logger_initialized", False):
        try:
            init_logger()
            st.session_state["logger_initialized"] = True
        except Exception as e:
            st.error(f"Error initializing logger: {str(e)}")
            logger.error(f"Error initializing logger: {str(e)}")


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


def main():
    setup()
    st.title("🧠 AI Resume Analyzer")
    st.write("Upload a resume and enter a job description – and get a smart match analysis!")

    uploaded_file = st.file_uploader("📄 Upload a resume file (PDF only)", type="pdf")
    job_description = st.text_area("📝 Paste the job description here", height=200)
    email_address = st.text_input("📧 Enter your email address (Optional)")

    if st.button("🔍 Analyze match"):
        if uploaded_file and job_description:
            logger.info("🔔 Starting match analysis...")
            with st.spinner("Analyzing..."):
                try:
                    analyze_resume(uploaded_file, job_description, email_address)
                except Exception as e:
                    st.error(f"Error in analysis: {str(e)}")
                    logger.error(f"Error in analysis: {str(e)}")
        else:
            st.warning("Please upload a resume file and enter a job description.")
            logger.warning("Missing resume or job description.")


if __name__ == "__main__":
    main()

