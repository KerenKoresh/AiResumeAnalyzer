import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

logger = logging.getLogger("AIResumeAnalyzer")


def send_email(subject, body, to_email):
    from_email = "ai.resume.analyzer.ko@gmail.com"  # כתובת המייל שלך
    from_password = "icos ofqm bvqd iwdz"  # סיסמא של המייל שלך

    # הגדרת השרת של Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        # התחברות לשרת
        server.login(from_email, from_password)

        # יצירת המייל
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        logger.info(f"🔔 Email sent successfully to {to_email}")
        st.success(f"Results have been sent to {to_email}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
