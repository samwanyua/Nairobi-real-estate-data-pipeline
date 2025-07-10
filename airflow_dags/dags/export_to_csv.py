import os
import pandas as pd
import psycopg2

EXPORT_DIR = "/opt/airflow/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

# Unified DB config for both tables
DB_CONFIG = {
    "host": "postgres_main",
    "dbname": "nrbproperties",
    "user": "postgres",
    "password": "postgres"
}

# Tables to export
TABLES = ["raw_listings", "clean_listings"]

def export_table_append(table_name: str):
    file_path = os.path.join(EXPORT_DIR, f"{table_name}.csv")

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        if df.empty:
            print(f"[{table_name}] No data found.")
            return

        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', index=False, header=False)
            print(f"[{table_name}] Appended {len(df)} rows to {file_path}")
        else:
            df.to_csv(file_path, mode='w', index=False, header=True)
            print(f"[{table_name}] Created new CSV with {len(df)} rows at {file_path}")

    except Exception as e:
        print(f"[{table_name}] Export failed: {e}")
        raise

if __name__ == "__main__":
    for table in TABLES:
        export_table_append(table)
