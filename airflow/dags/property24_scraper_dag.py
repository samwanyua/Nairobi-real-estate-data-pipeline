def consume_and_insert():
    from confluent_kafka import Consumer
    import psycopg2, json

    # Set up Kafka consumer
    consumer = Consumer({
        'bootstrap.servers': 'kafka:29092',
        'group.id': 'airflow-consumer',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['raw_listings'])

    # PostgreSQL connection
    conn = psycopg2.connect(
        host='postgres_raw',
        dbname='nrbproperties',
        user='postgres',
        password='postgres'
    )
    cursor = conn.cursor()

    rows_to_insert = []

    # Collect up to 50 Kafka messages
    for _ in range(50):
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue

        data = json.loads(msg.value().decode('utf-8'))

        # Append values as a tuple
        rows_to_insert.append((
            data['title'], data['price'], data['location'], data['address'],
            data['description'], data['bedrooms'], data['bathrooms'],
            data['parking'], data['size'], data['source'], data['page']
        ))

    # Only execute if we have data
    if rows_to_insert:
        cursor.executemany("""
            INSERT INTO raw_listings (
                title, price, location, address, description,
                bedrooms, bathrooms, parking, size, source, page
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, rows_to_insert)

        conn.commit()
        print(f"Inserted {len(rows_to_insert)} records to Postgres")

    cursor.close()
    conn.close()
    consumer.close()    


