import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of the script
DB_FOLDER = os.path.join(BASE_DIR, "database")
os.makedirs(DB_FOLDER, exist_ok=True)  # create the folder if it doesn't exist

DB_PATH = os.path.join(DB_FOLDER, "profiles.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create all tables
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        github TEXT,
        linkedin TEXT,
        description TEXT,
        score REAL
    );

    CREATE TABLE IF NOT EXISTS developers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS recruiters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
''')

conn.commit()
conn.close()

print("Database created successfully!")
