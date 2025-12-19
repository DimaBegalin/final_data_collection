import sqlite3

def get_connection():
    db_path = '/opt/airflow/data/app.db'
    return sqlite3.connect(db_path)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Таблица EVENTS согласно критериям (Cleaned Data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            aqi INTEGER,
            lat REAL,
            lon REAL,
            utime INTEGER,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()