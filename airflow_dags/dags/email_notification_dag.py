from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from notification.email_notifier import send_email_alert

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 6, 26),
}

with DAG(
    dag_id='email_notification_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['notification']
) as dag:

    notify_user = PythonOperator(
        task_id='send_property_alert_email',
        python_callable=send_email_alert
    )

    notify_user
