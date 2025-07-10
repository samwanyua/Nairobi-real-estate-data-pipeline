import os
import pandas as pd
import psycopg2

EXPORT_DIR = "/opt/airflow/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

# Database configs per your setup
DBS = {
    "raw": {
        "host": "raw_db",     # from kafka_to_postgres.py
        "dbname": "nrbproperties",  # raw db
        "user": "postgres",
        "password": "postgres",
        "table": "raw_listings"
    },
    "clean": {
        "host": "clean_db",         # from kafka_stream_to_postgres.py
        "dbname": "clean_db",
        "user": "postgres",
        "password": "postgres",
        "table": "clean_listings"
    }
}

def export_table_append(db_key):
    cfg = DBS[db_key]
    conn = psycopg2.connect(
        host=cfg["host"],
        dbname=cfg["dbname"],
        user=cfg["user"],
        password=cfg["password"]
    )

    query = f"SELECT * FROM {cfg['table']}"
    df = pd.read_sql(query, conn)
    conn.close()

    file_path = os.path.join(EXPORT_DIR, f"{db_key}_{cfg['table']}.csv")

    if os.path.exists(file_path):
        # Append without header
        df.to_csv(file_path, mode='a', index=False, header=False)
        print(f"[Append] {len(df)} rows to {file_path}")
    else:
        # Write new file with header
        df.to_csv(file_path, mode='w', index=False, header=True)
        print(f"[Create] New file {file_path} with {len(df)} rows")

if __name__ == "__main__":
    export_table_append("raw")
    export_table_append("clean")
