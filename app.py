import logging
import streamlit as st
from src.match_analysis import analyze_match
from utils.email_utils import send_email
from utils.logging_utils import init_logger
from utils.pdf_utils import extract_text_from_pdf

# אתחול הלוגינג (לא משתמשים ב-session_state)
if 'logger_initialized' not in st.session_state:
    st.session_state['logger_initialized'] = False

if not st.session_state['logger_initialized']:
    # אתחול הלוגר
    init_logger()
    st.session_state['logger_initialized'] = True  # מבטיח שיתחיל רק פעם אחת

# הגדרת Streamlit (רק פעם אחת)
if "initialized_ui" not in st.session_state:
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
    st.session_state["initialized_ui"] = True

# הגדרת Streamlit
st.title("🧠 AI Resume Analyzer")
st.write("Upload a resume and enter a job description – and get a smart match analysis!")

# קובץ קורות חיים
uploaded_file = st.file_uploader("📄 Upload a resume file (PDF only)", type="pdf")

# תיאור המשרה
job_description = st.text_area("📝 Paste the job description here", height=200)

# שדה קלט לכתובת מייל
email_address = st.text_input("📧 Enter your email address (Optional)")

# כפתור ניתוח
if st.button("🔍 Analyze match"):
    if uploaded_file and job_description:
        logging.info("🔔 Analyzing match...")

        with st.spinner("Analyzing..."):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)

                if not resume_text.strip():
                    st.error("No text found in the PDF file. Please ensure the file is valid and not scanned as an image.")
                    logging.error("No text found in the PDF file.")
                else:
                    # ניתוח חדש
                    result = analyze_match(resume_text, job_description)
                    st.markdown("### 🧾 Analysis Results")
                    st.markdown(result)

                    # אם הוזנה כתובת מייל, נשלח את התוצאה
                    if email_address:
                        send_email("Resume Match Analysis", result, email_address)
                        st.success(f"Results have been sent to {email_address}")
                        logging.info(f"Results sent to {email_address}")

            except Exception as e:
                st.error(f"Error in analysis: {str(e)}")
                logging.error(f"Error in analysis: {str(e)}")
    else:
        st.warning("Please upload a resume file and enter a job description.")
        logging.warning("User did not upload resume or enter job description.")
