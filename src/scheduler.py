import pandas as pd
import schedule
import time
from datetime import datetime
from src.email_sender import send_email
from src.utils import load_template, personalize_message

TEMPLATE_PATH = "templates/email_template.txt"

def send_scheduled_email(row):
    template = load_template(TEMPLATE_PATH)
    message = personalize_message(template, row["name"])

    send_email(
        to_email=row["email"],
        subject="Reminder Notification",
        message=message
    )

def schedule_emails():
    df = pd.read_csv("data/reminders.csv")

    for _, row in df.iterrows():
        send_time = datetime.strptime(row["send_time"], "%Y-%m-%d %H:%M")

        schedule.every().day.at(send_time.strftime("%H:%M")).do(
            send_scheduled_email, row=row
        )

    print("Scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(1)