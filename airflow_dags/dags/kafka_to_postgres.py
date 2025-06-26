import json
import psycopg2
from confluent_kafka import Consumer

def consume_and_insert():
    # Kafka consumer config
    consumer = Consumer({
        'bootstrap.servers': 'kafka:29092',
        'group.id': 'property24-consumer',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['raw_listings'])

    # Postgres connection
    conn = psycopg2.connect(
        host='postgres_raw',
        dbname='nrbproperties',
        user='postgres',
        password='postgres'
    )
    cursor = conn.cursor()

    batch = []

    for _ in range(100):  # Poll up to 100 messages
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        data = json.loads(msg.value().decode('utf-8'))
        batch.append((
            data['title'], data['price'], data['location'], data['address'],
            data['description'], data['bedrooms'], data['bathrooms'],
            data['parking'], data['size'], data['source'], data['page']
        ))

    if batch:
        cursor.executemany("""
            INSERT INTO raw_listings (
                title, price, location, address, description,
                bedrooms, bathrooms, parking, size, source, page
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        conn.commit()

    cursor.close()
    conn.close()
    consumer.close()
