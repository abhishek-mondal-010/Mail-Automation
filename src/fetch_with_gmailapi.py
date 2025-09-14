# src/fetch_with_gmailapi.py
import os
import base64
from email.header import decode_header
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.mongo_db import emails_collection
from src.tagger import tag_email

# ---- Config ----
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_FILE = os.path.join(os.getcwd(), "credentials.json")
TOKEN_FILE = os.path.join(os.getcwd(), "token.json")
MAX_MESSAGES_DEFAULT = 10  # fetch last 10 messages

# ---- Helpers ----
def decode_header_str(hdr):
    if not hdr:
        return ""
    parts = decode_header(hdr)
    out = ""
    for bytes_, encoding in parts:
        if isinstance(bytes_, bytes):
            out += bytes_.decode(encoding or "utf-8", errors="ignore")
        else:
            out += str(bytes_)
    return out

def get_plain_text_from_payload(payload):
    if not payload:
        return ""
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data.encode("ASCII")).decode("utf-8", errors="ignore")
    if payload.get("mimeType") == "text/html" and payload.get("body", {}).get("data"):
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data.encode("ASCII")).decode("utf-8", errors="ignore")
    for part in payload.get("parts", []) or []:
        t = get_plain_text_from_payload(part)
        if t:
            return t
    return ""

# ---- Gmail auth ----
def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service

# ---- Fetch and save emails ----
def fetch_and_save_emails(max_messages=MAX_MESSAGES_DEFAULT):
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", maxResults=max_messages).execute()
    msgs = results.get("messages", [])

    for m in msgs:
        msg = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])

        subj = frm = date_str = ""
        for h in headers:
            name = h.get("name", "").lower()
            if name == "subject":
                subj = decode_header_str(h.get("value"))
            elif name == "from":
                frm = decode_header_str(h.get("value"))
            elif name == "date":
                date_str = h.get("value")

        body = get_plain_text_from_payload(payload)
        tag = tag_email(subj, body)

        # Convert date to datetime
        try:
            date_obj = datetime.strptime(date_str[:31], "%a, %d %b %Y %H:%M:%S %z")
        except Exception:
            date_obj = datetime.utcnow()

        # Upsert email to prevent duplicates
        emails_collection.update_one(
            {"gmail_id": m["id"]},
            {"$setOnInsert": {
                "sender": frm,
                "subject": subj,
                "body": body,
                "tag": tag,
                "date": date_obj
            }},
            upsert=True
        )

    print(f"[INFO] Fetched {len(msgs)} messages and updated MongoDB.")
