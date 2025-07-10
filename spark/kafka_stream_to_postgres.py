import json
from datetime import datetime
from kafka import KafkaConsumer
import psycopg2


KAFKA_TOPIC = "property24_listings"
KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"

DB_CONFIG = {
    "dbname": "nrbproperties",  
    "user": "postgres",
    "password": "postgres",
    "host": "postgres_main", 
    "port": "5432"
}


def get_kafka_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=10000  # Exit gracefully after no messages
    )


def insert_listing_to_db(cursor, listing):
    cursor.execute("""
        INSERT INTO clean_listings (
            title, price, location, address, description,
            bedrooms, bathrooms, parking, size_sqm, source, page, inserted_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        listing.get("title"),
        listing.get("price"),
        listing.get("location"),
        listing.get("address"),
        listing.get("description"),
        listing.get("bedrooms"),
        listing.get("bathrooms"),
        listing.get("parking"),
        listing.get("size_sqm"),
        listing.get("source"),
        listing.get("page"),
        datetime.now()
    ))


def consume_and_insert():
    print("[Kafka] Starting consumer...")
    consumer = get_kafka_consumer()

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for msg in consumer:
                listing = msg.value
                print(f"[Kafka] Received message: {listing}")
                try:
                    insert_listing_to_db(cur, listing)
                    conn.commit()
                    print("[Postgres] Inserted one listing")
                    break  # process only one record per Airflow task
                except Exception as e:
                    print(f"[Error] Failed to insert: {e}")
                    conn.rollback()

    consumer.close()
    print("[Kafka] Consumer closed")


if __name__ == "__main__":
    consume_and_insert()
