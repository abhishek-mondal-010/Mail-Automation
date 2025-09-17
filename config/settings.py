import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gmail Config
EMAIL_USER = os.getenv("EMAIL_USER")      
EMAIL_PASS = os.getenv("EMAIL_PASS")      

# Database Config
DB_NAME = "emails.db"
