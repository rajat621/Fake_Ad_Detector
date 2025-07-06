import sqlite3

conn = sqlite3.connect("history.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM analysis_log")
rows = cursor.fetchall()

print("Records in the database:")
for row in rows:
    print(row)

conn.close()
