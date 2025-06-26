FROM python:3.11-slim

WORKDIR /app

# Install system dependencies first (if any)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies once 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "kafka_producer.producer.push_to_kafka"]
