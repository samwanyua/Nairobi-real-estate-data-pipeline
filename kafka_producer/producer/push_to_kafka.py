import os
import time
import json
import socket
from confluent_kafka import Producer

from scraper.property24_scraper import get_total_pages, scrape_property24_page

KAFKA_BROKER = "kafka:29092"
TOPIC = "raw_listings"
CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'last_page.txt')
RETRY_ATTEMPTS = 10
RETRY_INTERVAL = 5  # seconds

conf = {"bootstrap.servers": KAFKA_BROKER}
producer = Producer(conf)

print("[Debug] Hostname:", socket.gethostname())
print("[Debug] Kafka broker:", KAFKA_BROKER)

def delivery_report(err, msg):
    if err:
        print(f"[Delivery Failed] {err} for key {msg.key()}")
    else:
        print(f"[Delivered] {msg.topic()} [{msg.partition()}] key={msg.key()}")

def get_last_page():
    try:
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, 'r') as f:
                return int(f.read().strip())
    except Exception as e:
        print(f"[Checkpoint Warning] Could not read checkpoint: {e}")
    return 0

def save_last_page(page):
    try:
        with open(CHECKPOINT_FILE, 'w') as f:
            f.write(str(page))
    except Exception as e:
        print(f"[Checkpoint Error] Could not save page {page}: {e}")

def wait_for_kafka(max_retries=RETRY_ATTEMPTS):
    try:
        resolved_ip = socket.gethostbyname("kafka")
        print(f"[Debug] Resolved 'kafka' to {resolved_ip}")
    except Exception as e:
        raise RuntimeError(f"[DNS Error] Failed to resolve 'kafka': {e}")

    for attempt in range(1, max_retries + 1):
        try:
            producer.list_topics(timeout=5)
            print("[Kafka] Connection successful")
            return
        except Exception as e:
            print(f"[Kafka] Attempt {attempt}/{max_retries} failed: {e}")
            time.sleep(RETRY_INTERVAL)
    raise RuntimeError("[Kafka Error] Could not connect after retries")

def run_stream(delay=1.0):
    print("[Stream] Starting property24 to Kafka stream")
    wait_for_kafka()

    total_pages = get_total_pages()
    print(f"[Stream] Total pages available: {total_pages}")

    start_page = get_last_page() + 1
    print(f"[Stream] Resuming from page {start_page}")

    for page in range(start_page, total_pages + 1):
        listings = scrape_property24_page(page)
        print(f"[Stream] Page {page} → {len(listings)} listings")

        for listing in listings:
            try:
                producer.produce(
                    topic=TOPIC,
                    key=str(listing.get("page", page)),
                    value=json.dumps(listing),
                    callback=delivery_report
                )
            except Exception as e:
                print(f"[Produce Error] Page {page}: {e}")

        producer.flush()
        save_last_page(page)
        time.sleep(delay)

    print("[Stream] Finished scraping all pages")


if __name__ == "__main__":
    run_stream(delay=0.5)
