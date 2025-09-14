# app.py
import sys
import os
from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# Ensure src folder is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.mongo_db import emails_collection
from src.fetch_with_gmailapi import fetch_and_save_emails

app = Flask(__name__)

# ---- Scheduler to fetch emails automatically ----
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: fetch_and_save_emails(max_messages=10), 'interval', minutes=5)
scheduler.start()


# ---- Dashboard route ----
@app.route("/")
def dashboard():
    selected_tag = request.args.get("tag", "All")
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    query = {}

    # Filter by tag
    if selected_tag != "All":
        query["tag"] = selected_tag

    # Filter by date range
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            query["date"] = {"$gte": start_date, "$lte": end_date}
        except ValueError:
            pass  # Ignore invalid date formats

    # Fetch emails from MongoDB (only read, no fetching)
    emails = list(emails_collection.find(query).sort("date", -1))
    total = len(emails)

    # Emails by tag (for chart)
    tag_count = {"Business Lead": 0, "Reporting": 0, "General": 0}
    for e in emails_collection.find():
        tag_count[e.get("tag", "General")] += 1

    return render_template(
        "dashboard.html",
        total=total,
        tag_count=tag_count,
        emails=emails,
        last_update=datetime.utcnow(),
        selected_tag=selected_tag,
        start_date=start_date_str,
        end_date=end_date_str
    )


# ---- Run Flask app ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
