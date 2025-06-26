#!/bin/bash
set -e

# Wait for Postgres container to be ready
until pg_isready -h postgres_raw -p 5432 -U postgres; do
  echo "⏳ Waiting for Postgres..."
  sleep 2
done
echo "✅ Postgres is ready!"

# Initialize Airflow metadata DB
airflow db init

# Migrate any newer versions
airflow db migrate

# Ensure default connections exist
airflow connections create-default-connections

# Create admin user if not exists (ignore errors)
airflow users create \
  --username admin \
  --firstname Sam \
  --lastname Wanyua \
  --role Admin \
  --email samexample8@gmail.com \
  --password admin || true

# Start scheduler in background, webserver in foreground
airflow scheduler &
exec airflow webserver
