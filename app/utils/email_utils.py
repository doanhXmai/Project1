import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from app.utils.log import ConsoleLogger as cl

from app.core.config import Settings

settings = Settings()

def send_otp_email(to_email: str, otp_code: str):
    try:
        subject = "Your OTP code"
        body = f"Your OTP verification code is: {otp_code}\nThis code is valid for 5 minutes."

        msg = MIMEMultipart()

        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = Header(subject, "utf-8")

        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())

        return True
    except Exception as e:
        cl.error(f"Email send error: {e}")
        return False