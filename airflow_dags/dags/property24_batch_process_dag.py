import sys
import os
sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 6, 26),
    'catchup': False
}

with DAG(
    dag_id='property24_batch_process_dag',
    default_args=default_args,
    schedule_interval='0 0 * * *',  # Daily at midnight
    description='Clean and transform raw listings using Spark',
    catchup=False,
    max_active_runs=1,
    concurrency=2,
    tags=['spark', 'property24']
) as dag:

    run_spark_job = BashOperator(
        task_id='run_spark_cleaning',
        bash_command="""
        /opt/bitnami/spark/bin/spark-submit \
        --jars /opt/spark-apps/postgresql-42.7.1.jar \
        /opt/spark-apps/property24_batch_process.py
        """
    )

    run_spark_job
