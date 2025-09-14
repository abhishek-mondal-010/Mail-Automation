from email_reader import fetch_emails
from tagger import tag_email
from database import init_db, save_email
from report import generate_report

def main():
    # Setup database
    init_db()

    # Fetch emails
    emails = fetch_emails()
    print(f"Fetched {len(emails)} emails.")

    # Save to DB with tags
    for mail in emails:
        tag = tag_email(mail["subject"], mail["body"])
        save_email(mail["sender"], mail["subject"], mail["body"], tag, mail["date"])

    # Generate report
    generate_report()

if __name__ == "__main__":
    main()
