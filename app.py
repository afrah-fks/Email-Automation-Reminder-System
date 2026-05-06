import streamlit as st
import pandas as pd
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# --------------------------
# LOAD ENV
# --------------------------
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# --------------------------
# PATHS
# --------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "contacts.csv")
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "email_template.txt")
LOG_PATH = os.path.join(BASE_DIR, "logs", "email_logs.txt")
REPORT_PATH = os.path.join(BASE_DIR, "outputs", "report.csv")

# --------------------------
# UI CONFIG
# --------------------------
st.set_page_config(page_title="Email Automation Pro", layout="wide")
st.title("📧 Email Automation Dashboard (Pro Version)")

# --------------------------
# MODE TOGGLE
# --------------------------
mode = st.sidebar.radio("Select Mode", ["DRY RUN", "LIVE"])
st.sidebar.info(f"Current Mode: {mode}")

# --------------------------
# MENU
# --------------------------
menu = [
    "Dashboard",
    "Upload Contacts",
    "Create Campaign",
    "Send Emails",
    "View Logs",
    "Reports"
]
choice = st.sidebar.selectbox("Navigation", menu)

# --------------------------
# HELPERS
# --------------------------
def ensure_folder(path):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)

def log(msg):
    ensure_folder(LOG_PATH)
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def send_email(to_email, subject, message):
    if mode == "DRY RUN":
        log(f"SUCCESS: (DRY RUN) Email to {to_email}")
        return True

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        log(f"SUCCESS: Email sent to {to_email}")
        return True
    except Exception as e:
        log(f"FAILED: {to_email} | {e}")
        return False

# --------------------------
# DASHBOARD (NEW)
# --------------------------
if choice == "Dashboard":
    st.header("📊 System Overview")

    total = 0
    success = 0
    failed = 0

    if os.path.exists(DATA_PATH):
        total = len(pd.read_csv(DATA_PATH))

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            logs = f.readlines()
            success = sum("SUCCESS" in l for l in logs)
            failed = sum("FAILED" in l for l in logs)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Contacts", total)
    col2.metric("Emails Sent", success)
    col3.metric("Failures", failed)

# --------------------------
# UPLOAD CONTACTS
# --------------------------
elif choice == "Upload Contacts":
    st.header("📂 Upload Contacts")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        if st.button("Save"):
            ensure_folder(DATA_PATH)
            df.to_csv(DATA_PATH, index=False)
            st.success("Saved!")

# --------------------------
# CREATE CAMPAIGN
# --------------------------
elif choice == "Create Campaign":
    st.header("✉️ Create Campaign")

    subject = st.text_input("Subject")
    message = st.text_area("Message (use {name})")

    if st.button("Save Template"):
        ensure_folder(TEMPLATE_PATH)
        with open(TEMPLATE_PATH, "w") as f:
            f.write(message)
        st.success("Template saved!")

    # PREVIEW FEATURE
    if os.path.exists(DATA_PATH) and message:
        df = pd.read_csv(DATA_PATH)
        if not df.empty:
            preview = message.replace("{name}", df.iloc[0]["name"])
            st.subheader("📨 Preview")
            st.info(preview)

# --------------------------
# SEND EMAILS
# --------------------------
elif choice == "Send Emails":
    st.header("🚀 Send Emails")

    if st.button("Send Now"):
        if not os.path.exists(DATA_PATH) or not os.path.exists(TEMPLATE_PATH):
            st.error("Upload contacts & template first")
        else:
            df = pd.read_csv(DATA_PATH)
            template = open(TEMPLATE_PATH).read()

            success = 0

            for _, row in df.iterrows():
                msg = template.replace("{name}", row["name"])
                if send_email(row["email"], "Notification", msg):
                    success += 1

            st.success(f"{success} emails processed")

# --------------------------
# VIEW LOGS (FILTER ADDED)
# --------------------------
elif choice == "View Logs":
    st.header("📜 Logs")

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            logs = f.readlines()

        filter_option = st.selectbox("Filter", ["ALL", "SUCCESS", "FAILED"])

        for line in logs:
            if filter_option == "ALL" or filter_option in line:
                st.text(line)
    else:
        st.warning("No logs found")

# --------------------------
# REPORTS
# --------------------------
elif choice == "Reports":
    st.header("📊 Reports")

    if st.button("Generate Report"):
        if os.path.exists(LOG_PATH):
            lines = open(LOG_PATH).readlines()
            data = []

            for line in lines:
                if "SUCCESS" in line or "FAILED" in line:
                    time = line.split(" - ")[0]
                    email = line.split()[-1]
                    status = "SUCCESS" if "SUCCESS" in line else "FAILED"
                    data.append([time, email, status])

            df = pd.DataFrame(data, columns=["Time", "Email", "Status"])

            ensure_folder(REPORT_PATH)
            df.to_csv(REPORT_PATH, index=False)

            st.dataframe(df)
            st.success("Report Ready!")

    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "rb") as f:
            st.download_button("Download CSV", f, "report.csv")