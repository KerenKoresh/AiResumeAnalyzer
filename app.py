import logging
import streamlit as st
import sqlite3
import bcrypt
from src.match_analysis import analyze_match
from utils.email_utils import send_email
from utils.logging_utils import init_logger
from utils.pdf_utils import extract_text_from_pdf

# יצירת בסיס נתונים users.db אם לא קיים
def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# קריאה לפונקציה בעת אתחול
create_db()

# פונקציה לרישום משתמש חדש
def register_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # הצפנת הסיסמה
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute('''
            INSERT INTO users (email, password) VALUES (?, ?)
        ''', (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Email already registered."
    finally:
        conn.close()

    return "Registration successful!"

# פונקציה להתחברות עם אימות סיסמה
def login_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT password FROM users WHERE email = ?
    ''', (email,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return "Login successful!"
    else:
        return "Invalid email or password."

# יצירת לוג
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

def register_page():
    st.title("📋 Register")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")
    confirm_password = st.text_input("🔑 Confirm Password", type="password")

    if password != confirm_password:
        st.warning("Passwords do not match.")
    elif st.button("Register"):
        result = register_user(email, password)
        st.success(result)

def login_page():
    st.title("🔑 Login")
    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        result = login_user(email, password)
        if result == "Login successful!":
            st.session_state["logged_in"] = True
            st.success(result)
            main()  # Call main() to display the app after successful login
        else:
            st.error(result)

def main():
    setup()

    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        # הצג את שאר האפליקציה אחרי שהמשתמש נכנס
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
    else:
        # אם המשתמש לא מחובר, הצג את דפי הרישום והכניסה
        page = st.sidebar.radio("Please log in or register", ["Login", "Register"])
        if page == "Register":
            register_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
