import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from app.utils.log import ConsoleLogger as cl
import requests

from app.core.config import Settings

settings = Settings()

# def send_otp_email(to_email: str, otp_code: str):
#     try:
#         subject = "Your OTP code"
#         body = f"Your OTP verification code is: {otp_code}\nThis code is valid for 5 minutes."
#
#         msg = MIMEMultipart()
#
#         msg["From"] = settings.SMTP_FROM
#         msg["To"] = to_email
#         msg["Subject"] = Header(subject, "utf-8")
#
#         msg.attach(MIMEText(body, "plain", "utf-8"))
#
#         with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
#             server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
#             server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
#
#         return True
#     except Exception as e:
#         cl.error(f"Email send error: {e}")
#         return False

def send_otp_email(to_email: str, otp_code: str):
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": settings.EMAIL_FROM,
                "to": to_email,
                "subject": "Your OTP code",
                "html": f"""
                            <div style="font-family: Arial, sans-serif">
                                <h2>Your OTP Code</h2>
                                <p>Your verification code is:</p>
                                <h1 style="letter-spacing: 3px">{otp_code}</h1>
                                <p>This code is valid for <b>5 minutes</b>.</p>
                            </div>
                        """
            },
            timeout=10,
        )
        response.raise_for_status()
        return True

    except Exception as e:
        cl.error(f"Resend email send error: {e}")
        return False