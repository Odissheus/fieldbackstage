import smtplib
from email.message import EmailMessage
from typing import Optional
from .config import settings


def send_mail(to_address: str, subject: str, body_text: str) -> Optional[str]:
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASS:
        return "SMTP not configured"
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
    msg["To"] = to_address
    msg.set_content(body_text)
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)
    return None

