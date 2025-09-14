import sqlite3

# open the DB in the current folder
conn = sqlite3.connect("emails.db")
cursor = conn.cursor()

# Try to add gmail_id column
try:
    cursor.execute("ALTER TABLE emails ADD COLUMN gmail_id TEXT;")
    conn.commit()
    print("✅ gmail_id column added successfully")
except sqlite3.OperationalError as e:
    print("⚠️ Maybe the column already exists:", e)

conn.close()
