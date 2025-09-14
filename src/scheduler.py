# src/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from fetch_with_gmailapi import main as fetch_emails
import atexit

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule fetch_emails() every 5 minutes
    scheduler.add_job(fetch_emails, 'interval', minutes=5)
    scheduler.start()
    print("Email fetch scheduler started...")

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
