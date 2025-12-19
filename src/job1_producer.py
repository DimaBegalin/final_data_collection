import os
import requests
import json
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv('/opt/airflow/.env')
TOKEN = os.getenv('AQI_TOKEN')

def run_producer():
    conf = {'bootstrap.servers': 'kafka:9092'}
    p = Producer(conf)

    # Читаем города из файла (абсолютный путь в контейнере)
    try:
        with open('/opt/airflow/cities.txt', 'r') as f:
            cities = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ Файл cities.txt не найден!")
        return

    for city in cities:
        url = f"https://api.waqi.info/feed/{city}/?token={TOKEN}"
        try:
            res = requests.get(url).json()
            if res['status'] == 'ok':
                d = res['data']
                payload = {
                    "city_raw": d.get('city', {}).get('name'),
                    "aqi": d.get('aqi'),
                    "lat": d.get('city', {}).get('geo', [None, None])[0],
                    "lon": d.get('city', {}).get('geo', [None, None])[1],
                    "utime": d.get('time', {}).get('v'),
                    "timestamp": d.get('time', {}).get('s')
                }
                p.produce('weather_raw_data', json.dumps(payload).encode('utf-8'))
                print(f"✅ Данные отправлены в Kafka: {city}")
        except Exception as e:
            print(f"❌ Ошибка при запросе {city}: {e}")
    
    p.flush()

if __name__ == "__main__":
    run_producer()