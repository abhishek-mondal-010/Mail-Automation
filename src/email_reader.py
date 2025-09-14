import imaplib
import email
from config.settings import EMAIL_USER, EMAIL_PASS

def fetch_emails():
    try:
        # Connect to Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search all emails
        _, search_data = mail.search(None, "ALL")
        email_ids = search_data[0].split()

        emails = []

        for num in email_ids[-10:]:  # Fetch last 10 emails only
            _, data = mail.fetch(num, "(RFC822)")
            _, b = data[0]
            msg = email.message_from_bytes(b)

            sender = msg["From"]
            subject = msg["Subject"]
            date = msg["Date"]

            # Extract body (plain text only)
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            emails.append({
                "sender": sender,
                "subject": subject,
                "date": date,
                "body": body
            })

        mail.close()
        mail.logout()
        return emails

    except Exception as e:
        print("Error fetching emails:", e)
        return []
