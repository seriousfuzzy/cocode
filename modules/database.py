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
                  resume_filename TEXT,
                  job_applied TEXT,
                  relevance_score INTEGER,
                  date_added DATETIME)''')
    conn.commit()
    return conn

def add_candidate(conn, name, email, resume_filename, job_applied, relevance_score, date_added):
    c = conn.cursor()
    c.execute("""
        INSERT INTO candidates (name, email, resume_filename, job_applied, relevance_score, date_added)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, resume_filename, job_applied, relevance_score, date_added))
    conn.commit()

def get_latest_candidates(conn, limit=10):
    c = conn.cursor()
    c.execute("SELECT * FROM candidates ORDER BY date_added DESC LIMIT ?", (limit,))
    return c.fetchall()
