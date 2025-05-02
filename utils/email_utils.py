import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import streamlit as st

logger = logging.getLogger("AIResumeAnalyzer")

FROM_EMAIL = st.secrets["FROM_EMAIL"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]


def send_email(subject, body, to_email):
    if is_valid_email(email=to_email):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(FROM_EMAIL, EMAIL_PASSWORD)

            msg = MIMEMultipart()
            msg['From'] = FROM_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
            server.quit()

            logger.info(f"🔔 Email sent successfully to {to_email}")
            st.success(f"Results have been sent to {to_email}")
        except Exception as e:
            logger.error(f"❌Error sending email: {e}")
            st.error("❌ Failed to send email.")


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    is_valid = re.match(pattern, email) is not None

    if not is_valid:
        st.error("📭 Invalid email address format.")
        logger.error(f"❌Invalid email address format: {email}")

    return is_valid


