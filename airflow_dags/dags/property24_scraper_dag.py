import sys
sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scraper.property24_scraper import scrape_and_store

default_args = {
    'start_date': datetime(2025, 6, 26),
    'catchup': False
}

with DAG(
    dag_id='property24_scraper_dag',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
    max_active_runs=2,
    concurrency=4,
    description='Scrape Property24 and save directly to PostgreSQL',
    tags=['property24']
) as dag:

    scrape_and_save = PythonOperator(
        task_id='scrape_property24_and_store',
        python_callable=scrape_and_store
    )

    scrape_and_save
