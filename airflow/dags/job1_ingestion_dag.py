from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys, os, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.job1_producer import run_producer


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,                            
    'retry_delay': timedelta(seconds=15),     
}

def continuous_streaming():
    while True:
        run_producer()
        time.sleep(30)

with DAG(
    'dag1_continuous_ingestion',
    default_args=default_args,
    start_date=datetime(2025, 12, 19),
    schedule_interval=None,
    catchup=False
) as dag:
    PythonOperator(task_id='streaming_task', python_callable=continuous_streaming)
