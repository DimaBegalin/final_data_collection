import json
from confluent_kafka import Consumer
from db_utils import get_connection

def clean_data(raw):
    try:
        # Нормализация названия города
        raw_name = raw.get('city_raw', 'Unknown')
        city = str(raw_name).split(',')[0].strip().title()
        
        # Валидация AQI
        aqi_val = raw.get('aqi')
        if aqi_val is None: return None
        aqi = int(aqi_val)
        if aqi < 0 or aqi > 999: return None

        # Координаты
        lat = float(raw.get('lat')) if raw.get('lat') else None
        lon = float(raw.get('lon')) if raw.get('lon') else None

        return (city, aqi, lat, lon, raw.get('utime'), raw.get('timestamp'))
    except Exception:
        return None

def run_cleaner():
    conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'cleaner_final_v1',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    }
    c = Consumer(conf)
    c.subscribe(['weather_raw_data'])
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, aqi INTEGER,
            lat REAL, lon REAL, utime INTEGER, timestamp DATETIME
        )
    """)
    
    count = 0
    try:
        while True:
            msg = c.poll(5.0)
            if msg is None: break
            
            data = json.loads(msg.value().decode('utf-8'))
            cleaned = clean_data(data)
            
            if cleaned:
                cursor.execute("""
                    INSERT INTO events (city, aqi, lat, lon, utime, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, cleaned)
                count += 1
        
        conn.commit()
        print(f"🔥 Очищено и сохранено в базу: {count} записей")
    finally:
        conn.close()
        c.close()

if __name__ == "__main__":
    run_cleaner()