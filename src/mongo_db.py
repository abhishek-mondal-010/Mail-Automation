# src/mongo_db.py
import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "mailautomationDB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "Emails")

emails_collection = None

if not MONGO_URI:
    # No URI configured — keep a placeholder so imports don't crash
    # App code should handle emails_collection == None
    print("Warning: MONGO_URI not set. MongoDB disabled.")
else:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)  # 10s timeout
        # trigger server selection / initial connection
        client.admin.command("ping")
        db = client[DB_NAME]
        emails_collection = db[COLLECTION_NAME]
        print("MongoDB connected:", DB_NAME, COLLECTION_NAME)
    except errors.PyMongoError as e:
        # Connection failed — print helpful hint and continue (do not crash)
        print("Warning: could not connect to MongoDB:", str(e))
        emails_collection = None
