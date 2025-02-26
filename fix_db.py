import sqlite3

DB_FILE = "attendance.db"

# Connect to database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Drop old table (if exists)
cursor.execute("DROP TABLE IF EXISTS attendance_log")

conn.commit()
conn.close()

print("Database table recreated successfully!")

