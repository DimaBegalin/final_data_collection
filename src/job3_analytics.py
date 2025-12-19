from db_utils import get_connection

def run_analytics():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица DAILY_SUMMARY согласно критериям (Aggregated Analytics)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            city TEXT PRIMARY KEY,
            min_aqi INTEGER,
            max_aqi INTEGER,
            avg_aqi REAL,
            total_measurements INTEGER,
            air_quality_category TEXT,
            last_sync DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Считаем данные из таблицы EVENTS и сохраняем в DAILY_SUMMARY
    cursor.execute("""
        INSERT OR REPLACE INTO daily_summary 
        (city, min_aqi, max_aqi, avg_aqi, total_measurements, air_quality_category)
        SELECT 
            city, 
            MIN(aqi), 
            MAX(aqi), 
            ROUND(AVG(aqi), 2), 
            COUNT(*),
            CASE 
                WHEN AVG(aqi) <= 50 THEN 'Good'
                WHEN AVG(aqi) <= 100 THEN 'Moderate'
                WHEN AVG(aqi) <= 150 THEN 'Unhealthy'
                ELSE 'Hazardous'
            END
        FROM events
        GROUP BY city
    """)
    
    conn.commit()
    conn.close()
    print("📈 Таблица daily_summary обновлена на основе данных из events!")

if __name__ == "__main__":
    run_analytics()