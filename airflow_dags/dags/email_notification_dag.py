from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from notification.email_notifier import send_email_alert

# ------------------- Default Settings -------------------
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 6, 26),
}

# ------------------- DAG Definition -------------------
with DAG(
    dag_id='email_notification_dag',
    default_args=default_args,
    schedule_interval='@hourly', 
    catchup=False,
    tags=['notification'],
    description='Send periodic summary email for new property listings'
) as dag:

    notify_user = PythonOperator(
        task_id='send_property_alert_email',
        python_callable=send_email_alert,
        dag=dag
    )

    notify_user
