import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/email_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_success(email):
    logging.info(f"SUCCESS: Email sent to {email}")

def log_failure(email, error):
    logging.error(f"FAILED: {email} | Error: {error}")