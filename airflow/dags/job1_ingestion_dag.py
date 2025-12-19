from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.job1_producer import run_producer


def continuous_streaming():
    while True:
        run_producer()
        time.sleep(30)

with DAG(
    'dag1_continuous_ingestion',
    start_date=datetime(2025, 12, 19),
    schedule_interval=None,
    catchup=False
) as dag:
    PythonOperator(task_id='streaming_task', python_callable=continuous_streaming)