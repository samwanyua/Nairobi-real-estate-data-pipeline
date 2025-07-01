from kafka import KafkaConsumer
import psycopg2
import json

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
            INSERT INTO cleaned_listings (id, title, price, location)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (data["id"], data["title"], data["price"], data["location"]))
        conn.commit()
        break  # Avoid running forever during Airflow DAG runs

    cur.close()
    conn.close()
