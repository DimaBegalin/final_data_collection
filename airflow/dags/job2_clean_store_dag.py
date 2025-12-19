from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.job2_cleaner import run_cleaner

with DAG(
    'dag2_hourly_cleaning',
    start_date=datetime(2025, 12, 19),
    schedule_interval='@hourly', # Строго по ТЗ
    catchup=False
) as dag:
    PythonOperator(task_id='clean_kafka_to_sqlite', python_callable=run_cleaner)