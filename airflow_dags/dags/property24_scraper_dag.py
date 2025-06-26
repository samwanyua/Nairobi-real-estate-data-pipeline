from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from kafka_producer.producer.push_to_kafka import run_stream
from kafka_to_postgres import consume_and_insert


default_args = {
    'start_date': datetime(2025, 6, 26),
    'catchup': False
}

with DAG(
    dag_id='property24_scraper_dag',
    default_args=default_args,
    schedule_interval='@daily',
    description='Scrape Property24 ➝ Kafka ➝ PostgreSQL',
    tags=['property24']
) as dag:

    scrape_to_kafka = PythonOperator(
        task_id='scrape_property24_to_kafka',
        python_callable=run_stream
    )

    kafka_to_postgres = PythonOperator(
        task_id='consume_from_kafka_and_insert_to_postgres',
        python_callable=consume_and_insert
    )

    scrape_to_kafka >> kafka_to_postgres
