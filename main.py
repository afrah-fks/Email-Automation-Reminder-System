import pandas as pd
from src.email_sender import send_email
from src.utils import load_template, personalize_message
from src.scheduler import schedule_emails
from src.report import generate_report

TEMPLATE_PATH = "templates/email_template.txt"

def send_bulk_emails():
    df = pd.read_csv("data/contacts.csv")
    template = load_template(TEMPLATE_PATH)

    for _, row in df.iterrows():
        message = personalize_message(template, row["name"])

        send_email(
            to_email=row["email"],
            subject="Bulk Email Notification",
            message=message
        )

if __name__ == "__main__":
    print("1. Send Bulk Emails")
    print("2. Start Scheduler")
    print("3. Generate Report")

    choice = input("Enter choice: ")

    if choice == "1":
        send_bulk_emails()
    elif choice == "2":
        schedule_emails()
    elif choice == "3":
        generate_report()