import smtplib
from email.message import EmailMessage
from src.config import EMAIL, PASSWORD, DRY_RUN
from src.logger import log_success, log_failure

def send_email(to_email, subject, message):
    if DRY_RUN:
        print(f"[DRY RUN] Email to {to_email}")
        log_success(to_email)
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        log_success(to_email)

    except Exception as e:
        log_failure(to_email, str(e))