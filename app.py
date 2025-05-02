import logging
import streamlit as st
from src.match_analysis import analyze_match
from utils.email_utils import send_email
from utils.logging_utils import init_logger
from utils.pdf_utils import extract_text_from_pdf

# Creating a specific logger for the application
logger = logging.getLogger("AIResumeAnalyzer")

# Initialize Streamlit UI (only once)
if "initialized_ui" not in st.session_state:
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
    st.session_state["initialized_ui"] = True

# Initialize logging (we don't use session_state for the logger)
if "logger_initialized" not in st.session_state:
    st.session_state["logger_initialized"] = False

if not st.session_state["logger_initialized"]:
    # Initialize the logger
    try:
        init_logger()
        st.session_state["logger_initialized"] = True  # Ensures initialization happens only once
    except Exception as e:
        st.error(f"Error initializing logger: {str(e)}")
        logger.error(f"Error initializing logger: {str(e)}")

# Streamlit UI settings
st.title("🧠 AI Resume Analyzer")
st.write("Upload a resume and enter a job description – and get a smart match analysis!")

# Resume file upload
uploaded_file = st.file_uploader("📄 Upload a resume file (PDF only)", type="pdf")

# Job description input
job_description = st.text_area("📝 Paste the job description here", height=200)

# Email address input (optional)
email_address = st.text_input("📧 Enter your email address (Optional)")

# Analyze button
if st.button("🔍 Analyze match"):
    if uploaded_file and job_description:
        logger.info("🔔 Analyzing match...")

        with st.spinner("Analyzing..."):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)

                if not resume_text.strip():
                    st.error("No text found in the PDF file. Please ensure the file is valid and not scanned as an image.")
                    logger.error("No text found in the PDF file.")
                else:
                    # New analysis
                    result = analyze_match(resume_text, job_description)
                    st.markdown("### 🧾 Analysis Results")
                    st.markdown(result)

                    # If an email address was provided, send the result
                    if email_address:
                        send_email("Resume Match Analysis", result, email_address)
                        st.success(f"Results have been sent to {email_address}")
                        logger.info(f"Results sent to {email_address}")

            except Exception as e:
                st.error(f"Error in analysis: {str(e)}")
                logger.error(f"Error in analysis: {str(e)}")
    else:
        st.warning("Please upload a resume file and enter a job description.")
        logger.warning("User did not upload resume or enter job description.")
