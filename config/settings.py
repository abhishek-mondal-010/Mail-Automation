import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gmail Config
EMAIL_USER = os.getenv("EMAIL_USER")      # Your Gmail address
EMAIL_PASS = os.getenv("EMAIL_PASS")      # Your App Password

# Database Config
DB_NAME = "emails.db"
