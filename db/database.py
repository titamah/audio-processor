import sqlite3
from pathlib import Path

DB_PATH = Path("audio_notes.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("db/schema.sql", "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()