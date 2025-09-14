from __future__ import print_function
import os.path
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    token_file = os.getenv("TOKEN_FILE", "token.json")
    client_secret_file = os.getenv("CLIENT_SECRET_FILE", "credentials.json")

    # Load saved token if it exists
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If no valid credentials available, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    # Connect to Gmail API
    service = build("gmail", "v1", credentials=creds)

    # Example: list labels
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    print("Labels:")
    for label in labels:
        print(label["name"])

if __name__ == "__main__":
    authenticate_gmail()
