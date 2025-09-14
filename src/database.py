# src/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path.cwd() / "emails.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # gmail_id is UNIQUE to avoid duplicates
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gmail_id TEXT UNIQUE,
            sender TEXT,
            subject TEXT,
            body TEXT,
            tag TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_email_if_new(gmail_id, sender, subject, body, tag, date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO emails (gmail_id, sender, subject, body, tag, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (gmail_id, sender, subject, body, tag, date))
        conn.commit()
        inserted = True
    except sqlite3.IntegrityError:
        # gmail_id already exists -> skip insert
        inserted = False
    finally:
        conn.close()
    return inserted

def fetch_all(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, gmail_id, sender, subject, tag, date FROM emails ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
