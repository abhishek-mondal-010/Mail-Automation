# src/emailprocessor.py
from src.mongo_db import emails_collection
from src.tagger import tag_email
from datetime import datetime

def save_email_to_db(sender, subject, body, date=None):
    tag = tag_email(subject, body)
    date = date or datetime.now().isoformat()
    
    # Avoid duplicates by subject + sender + date
    if emails_collection.find_one({"sender": sender, "subject": subject, "date": date}):
        return False
    
    emails_collection.insert_one({
        "sender": sender,
        "subject": subject,
        "body": body,
        "tag": tag,
        "date": date
    })
    return True
