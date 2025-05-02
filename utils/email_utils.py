import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    from_email = "your-email@gmail.com"  # כתובת המייל שלך
    from_password = "your-email-password"  # סיסמא של המייל שלך

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
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
