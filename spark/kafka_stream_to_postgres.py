from kafka import KafkaConsumer
import psycopg2
import json
from datetime import datetime

def consume_and_insert():
    consumer = KafkaConsumer(
        'property24_listings',
        bootstrap_servers='kafka:29092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    conn = psycopg2.connect(
        dbname="clean_db",
        user="postgres",
        password="postgres",
        host="clean_db",
        port="5432"
    )
    cur = conn.cursor()

    for msg in consumer:
        data = msg.value
        print(f"Inserting: {data}")

        cur.execute("""
            INSERT INTO clean_listings (
                title, price, location, address, description,
                bedrooms, bathrooms, parking, size_sqm, source, page, inserted_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("title"),
            data.get("price"),
            data.get("location"),
            data.get("address"),
            data.get("description"),
            data.get("bedrooms"),
            data.get("bathrooms"),
            data.get("parking"),
            data.get("size_sqm"),
            data.get("source"),
            data.get("page"),
            datetime.now()
        ))

        conn.commit()
        break  # Only consume one message during Airflow run

    cur.close()
    conn.close()
