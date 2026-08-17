"""
Initializes enrollment.db from schema.sql + seed.sql.
Run this once before starting the Streamlit app:
    python init_db.py
"""
import sqlite3
import os

DB_PATH = "enrollment.db"

def run_sql_file(cursor, path):
    with open(path, "r") as f:
        cursor.executescript(f.read())

def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    run_sql_file(cur, "schema.sql")
    run_sql_file(cur, "seed.sql")

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    main()
