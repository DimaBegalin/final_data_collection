from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.job3_analytics import run_analytics

with DAG(
    'dag3_daily_analytics',
    start_date=datetime(2025, 12, 19),
    schedule_interval='@daily', # Строго по ТЗ
    catchup=False
) as dag:
    PythonOperator(task_id='compute_daily_metrics', python_callable=run_analytics)