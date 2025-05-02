import logging
import streamlit as st

from src.match_analysis import analyze_match
from utils.email_utils import send_email
from utils.logging_utils import add_betterstack_handler  # עדכון כאן
from utils.pdf_utils import extract_text_from_pdf


def init_logger():
    # אתחול של הלוגר אם הוא לא הותקן קודם
    if "logger_initialized" not in st.session_state:
        logging.info("🔔 Logging test: logger initialized")

        # בדיקה אם ה-handler של BetterStack כבר הוסף
        if not any(isinstance(handler, logging.Handler) and "BetterStack" in str(handler) for handler in
                   logging.getLogger().handlers):
            add_betterstack_handler()
            logging.info("🔔 BetterStack handler added.")
        else:
            logging.info("🔔 BetterStack handler already exists.")

        st.session_state.logger_initialized = True
    # לא שולחים את ההודעה שוב אם הלוגר כבר אתחול
    else:
        logging.debug("🔔 Logger already initialized previously.")

    return True


# אתחול הלוגינג
init_logger()

# הגדרת Streamlit (רק פעם אחת)
if "initialized_ui" not in st.session_state:
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
    st.session_state.initialized_ui = True

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
        with st.spinner("Analyzing..."):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)

                if not resume_text.strip():
                    st.error(
                        "No text found in the PDF file. Please ensure the file is valid and not scanned as an image.")
                else:
                    # ניתוח חדש
                    result = analyze_match(resume_text, job_description)
                    st.markdown("### 🧾 Analysis Results")
                    st.markdown(result)

                    # אם הוזנה כתובת מייל, נשלח את התוצאה
                    if email_address:
                        send_email("Resume Match Analysis", result, email_address)
                        st.success(f"Results have been sent to {email_address}")

            except Exception as e:
                st.error(f"Error in analysis: {str(e)}")
    else:
        st.warning("Please upload a resume file and enter a job description.")
