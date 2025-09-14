# src/report.py
from mongo_db import emails_collection
from datetime import datetime
from bson import ObjectId

def generate_report(start_date=None, end_date=None):
    query = {}
    if start_date:
        query["date"] = {"$gte": start_date}
    if end_date:
        if "date" in query:
            query["date"]["$lte"] = end_date
        else:
            query["date"] = {"$lte": end_date}

    emails = list(emails_collection.find(query))
    if not emails:
        print("No emails found.")
        return

    print("\n===== EMAIL REPORT =====")
    print(f"Total Emails: {len(emails)}")

    # Group by tag
    tag_count = {}
    for e in emails:
        tag_count[e.get("tag", "General")] = tag_count.get(e.get("tag", "General"), 0) + 1

    print("\nEmails by Tag:")
    for k, v in tag_count.items():
        print(f"{k}: {v}")

# Example usage:
if __name__ == "__main__":
    # Optional: filter by dates (ISO format)
    # start = "2025-09-01T00:00:00"
    # end = "2025-09-30T23:59:59"
    generate_report()
