# database.py

import sqlite3
from datetime import datetime

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT,
                  position_applied TEXT,
                  resume_filename TEXT,
                  relevance_score INTEGER,
                  timestamp DATETIME)''')
    conn.commit()
    return conn

def add_candidate(conn, name, email, position_applied, resume_filename, relevance_score, timestamp):
    c = conn.cursor()
    c.execute("""
        INSERT INTO candidates (name, email, position_applied, resume_filename, relevance_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, position_applied, resume_filename, relevance_score, timestamp))
    conn.commit()

def get_latest_candidates(conn, limit=10):
    c = conn.cursor()
    c.execute("SELECT * FROM candidates ORDER BY id DESC LIMIT ?", (limit,))
    return c.fetchall()
