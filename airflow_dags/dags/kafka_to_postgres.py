import json
import psycopg2
from confluent_kafka import Consumer


def consume_and_insert():
    print("[Kafka → Postgres] Starting consumer...")
    
    # Set up Kafka Consumer
    consumer = Consumer({
        'bootstrap.servers': 'kafka:29092',
        'group.id': 'property24-consumer-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['raw_listings'])

    try:
        # Connect to PostgreSQL
        with psycopg2.connect(
            host='postgres_main',
            dbname='nrbproperties',
            user='postgres',
            password='postgres'
        ) as conn:
            with conn.cursor() as cursor:
                batch = []

                for _ in range(100):  # Max 100 messages per run
                    msg = consumer.poll(timeout=1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        print(f"[Kafka Error] {msg.error()}")
                        continue

                    try:
                        data = json.loads(msg.value().decode('utf-8'))
                        batch.append((
                            data.get('title'),
                            data.get('price'),
                            data.get('location'),
                            data.get('address'),
                            data.get('description'),
                            data.get('bedrooms'),
                            data.get('bathrooms'),
                            data.get('parking'),
                            data.get('size_sqm') or data.get('size'),  # handle both
                            data.get('source'),
                            data.get('page')
                        ))
                    except Exception as e:
                        print(f"[JSON Error] Skipping malformed message: {e}")

                if batch:
                    cursor.executemany("""
                        INSERT INTO raw_listings (
                            title, price, location, address, description,
                            bedrooms, bathrooms, parking, size, source, page
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, batch)
                    conn.commit()
                    print(f"[Postgres] Inserted {len(batch)} listings.")

    except Exception as db_err:
        print(f"[DB Error] {db_err}")
        raise
    finally:
        consumer.close()
        print("[Kafka] Consumer closed.")
