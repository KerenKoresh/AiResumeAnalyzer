import logging
import streamlit as st
from src.match_analysis import analyze_match
from utils.email_utils import send_email
from utils.logging_utils import init_logger
from utils.pdf_utils import extract_text_from_pdf
import sqlite3

# Creating a specific logger for the application
logger = logging.getLogger("AIResumeAnalyzer")


# Initialize the session state for login status
def setup():
    """Initializes UI and logger."""
    if "initialized_ui" not in st.session_state:
        st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
        st.session_state["initialized_ui"] = True

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

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


def login_user(email, password):
    # Here you can implement the logic to verify the user's credentials
    # (for now it's a simple check, you can integrate with your DB).
    if email == "user@example.com" and password == "password123":
        return True
    return False


def register_user(email, password):
    """Registers a new user and adds them to the database."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # יצירת הטבלה אם היא לא קיימת
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Email already exists. Please try another email.")
    finally:
        conn.close()


def logout_user():
    """Logs the user out by clearing the session state."""
    st.session_state["logged_in"] = False
    del st.session_state["email"]  # Clear the user's email after logout
    st.success("You have been logged out.")


def main():
    setup()

    if st.session_state["logged_in"]:
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

        if st.button("🚪 Log out"):
            logout_user()

    else:
        st.title("🔒 Please Log In or Register")

        # Displaying login form if the user is not logged in
        login_form = st.form("login_form")
        with login_form:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Log In")

        # Displaying registration form
        register_form = st.form("register_form")
        with register_form:
            register_email = st.text_input("Email", key="register_email")
            register_password = st.text_input("Password", type="password", key="register_password")
            register_button = st.form_submit_button("Register")

        if login_button:
            if login_user(email, password):
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.success("Successfully logged in.")
                # No need for rerun, the session_state update will trigger the UI update
            else:
                st.error("Invalid email or password.")

        if register_button:
            if register_email and register_password:
                register_user(register_email, register_password)
                st.success("Registration successful! You are now logged in.")
                st.session_state["logged_in"] = True
                st.session_state["email"] = register_email
                # No need for rerun, the session_state update will trigger the UI update
            else:
                st.error("Please provide both email and password for registration.")


if __name__ == "__main__":
    main()
