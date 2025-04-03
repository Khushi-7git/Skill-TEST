import sqlite3
import os

DB_PATH = os.path.join("database", "profiles.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create profiles table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        github TEXT,
        linkedin TEXT,
        description TEXT,
        score REAL
    )
''')

conn.commit()
conn.close()

print("Database created successfully!")
