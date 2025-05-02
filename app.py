import logging
import streamlit as st
from src.match_analysis import analyze_match
from utils.logging_utils import add_betterstack_handler  # עדכון כאן
from utils.pdf_utils import extract_text_from_pdf
from utils.email_utils import send_email  # ייבוא הפונקציה לשליחת המייל

# הגדרת Streamlit (רק פעם אחת)
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")


def init_logger():
    # אתחול של הלוגר אם הוא לא הותקן קודם
    if "logger_initialized" not in st.session_state:
        logging.info("🔔 Logging test: logger initialized")
        add_betterstack_handler()
        st.session_state.logger_initialized = True
    return True


# אתחול הלוגינג
init_logger()

# הגדרת Streamlit
st.title("🧠 AI Resume Analyzer")
st.write("Upload a resume and enter a job description – and get a smart match analysis!")

# קובץ קורות חיים
uploaded_file = st.file_uploader("📄 Upload a resume file (PDF only)", type="pdf")
logging.info("File uploader initialized.")

# תיאור המשרה
job_description = st.text_area("📝 Paste the job description here", height=200)
logging.info("Job description text area initialized.")

# שדה קלט לכתובת מייל
email_address = st.text_input("📧 Enter your email address (Optional)")
logging.info("Email input field initialized.")

# כפתור ניתוח
if st.button("🔍 Analyze match"):
    logging.info("Analyze match button clicked.")
    if uploaded_file and job_description:
        logging.info("Both resume and job description provided. Starting analysis...")
        with st.spinner("Analyzing..."):
            try:
                # استخراج הטקסט מקובץ ה-PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                logging.info("Extracted resume text from PDF.")

                if not resume_text.strip():
                    logging.warning("No text found in the PDF file.")
                    st.error(
                        "No text found in the PDF file. Please ensure the file is valid and not scanned as an image.")
                else:
                    # ניתוח חדש
                    logging.info("Performing match analysis.")
                    result = analyze_match(resume_text, job_description)
                    st.markdown("### 🧾 Analysis Results")
                    st.markdown(result)

                    # אם הוזנה כתובת מייל, נשלח את התוצאה
                    if email_address:
                        logging.info(f"Sending analysis result to {email_address}.")
                        send_email("Resume Match Analysis", result, email_address)
                        st.success(f"Results have been sent to {email_address}")

            except Exception as e:
                logging.error(f"Error in analysis: {str(e)}")
                st.error(f"Error in analysis: {str(e)}")
    else:
        logging.warning("Please upload a resume file and enter a job description.")
        st.warning("Please upload a resume file and enter a job description.")
