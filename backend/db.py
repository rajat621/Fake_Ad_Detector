import sqlite3
from datetime import datetime

def log_result(ad_text, verdict, trust_score, reference_url):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_text TEXT,
            verdict TEXT,
            trust_score INTEGER,
            reference_url TEXT,
            timestamp DATETIME
        )
    ''')

    c.execute('''
        INSERT INTO analysis_log (ad_text, verdict, trust_score, reference_url, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (ad_text, verdict, trust_score, reference_url, datetime.now()))

    conn.commit()
    conn.close()
