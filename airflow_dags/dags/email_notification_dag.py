from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

def generate_message(**kwargs):
    return "New property alert: 3-bedroom in Westlands for KES 85,000!"

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 25),
    'retries': 1
}

with DAG(
    dag_id='email_notification_dag',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
    tags=['notifications']
) as dag:

    prepare_msg = PythonOperator(
        task_id='prepare_email_body',
        python_callable=generate_message
    )

    notify = EmailOperator(
        task_id='send_email',
        to='samexample8@gmail.com',
        subject='New Nairobi Property Listing!',
        html_content="{{ ti.xcom_pull(task_ids='prepare_email_body') }}",
    )

    prepare_msg >> notify
