from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from confluent_kafka import Consumer
import psycopg2, json

# Function to consume data from Kafka topic and insert into PostgreSQL
def consume_and_insert():
    # Set up Kafka consumer
    consumer = Consumer({
        'bootstrap.servers': 'kafka:29092',  
        'group.id': 'airflow-consumer',      # Consumer group ID
        'auto.offset.reset': 'earliest'      # Start from earliest if no offset committed
    })

    # Subscribe to the topic
    consumer.subscribe(['raw_listings'])

    # Connect to PostgreSQL container for raw data
    conn = psycopg2.connect(
        host='postgres_raw',
        dbname='nrbproperties',
        user='postgres',
        password='postgres'
    )
    cursor = conn.cursor()

    # Process a batch of messages (limit to 50 for performance)
    for _ in range(50):
        msg = consumer.poll(1.0)  # Wait 1 second for message
        if msg is None or msg.error():
            continue  # Skip if no message or error occurred

        # Parse Kafka message
        data = json.loads(msg.value().decode('utf-8'))

        # Insert into raw_listings table
        cursor.execute("""
            INSERT INTO raw_listings (
                title, price, location, address, description, 
                bedrooms, bathrooms, parking, size, source, page
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['title'], data['price'], data['location'], data['address'],
            data['description'], data['bedrooms'], data['bathrooms'],
            data['parking'], data['size'], data['source'], data['page']
        ))

        # Commit after each insert 
        conn.commit()

    # Clean up connections
    cursor.close()
    conn.close()
    consumer.close()

# DAG default arguments
default_args = {
    'start_date': datetime(2025, 6, 26),  # Start date
    'catchup': False                      # Avoid running past executions
}

# Define the DAG
with DAG(
    'kafka_to_postgres_dag',
    default_args=default_args,
    schedule_interval='@hourly',          # Run every hour
    description='Consume from Kafka and load into raw PostgreSQL',
    tags=['kafka', 'postgres']
) as dag:

    # PythonOperator to execute consume_and_insert
    task = PythonOperator(
        task_id='consume_and_load',        # Fixed typo: was "taks_id"
        python_callable=consume_and_insert
    )
