# src/save_email.py
from mongo_db import emails_collection

def save_email_if_new(email_data):
    """
    Save email only if it doesn't exist (based on gmail_id)
    """
    if emails_collection.find_one({"gmail_id": email_data["gmail_id"]}):
        return False
    emails_collection.insert_one(email_data)
    return True

