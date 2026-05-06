import pandas as pd
import os

def generate_report():
    log_file = "logs/email_logs.txt"

    if not os.path.exists(log_file):
        print("No logs found")
        return

    with open(log_file, "r") as f:
        lines = f.readlines()

    data = []

    for line in lines:
        if "SUCCESS" in line:
            status = "SUCCESS"
        elif "FAILED" in line:
            status = "FAILED"
        else:
            continue

        parts = line.split(" - ")
        time = parts[0]
        email = parts[-1].split()[-1]

        data.append([time, email, status])

    df = pd.DataFrame(data, columns=["Time", "Email", "Status"])

    os.makedirs("outputs", exist_ok=True)
    df.to_csv("outputs/report.csv", index=False)

    print("Report generated: outputs/report.csv")