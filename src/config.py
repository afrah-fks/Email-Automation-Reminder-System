import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DRY_RUN = os.getenv("DRY_RUN", "True") == "True"