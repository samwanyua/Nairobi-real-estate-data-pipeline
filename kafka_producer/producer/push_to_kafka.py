import json, time, os
from confluent_kafka import Producer

from scraper.property24_scraper import get_total_pages, scrape_property24_page

CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'last_page.txt')
conf = {'bootstrap.servers': 'kafka:29092'}
producer = Producer(conf)

def print_metadata():
    print("Broker metadata:", producer.list_topics(timeout=15).topics.keys())


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed for {msg.key()}: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")


def get_last_page():
    if os.path.exists(CHECKPOINT_FILE):
        try:
            return int(open(CHECKPOINT_FILE).read().strip())
        except:
            return 0
    return 0


def save_last_page(page):
    with open(CHECKPOINT_FILE, 'w') as f:
        f.write(str(page))

def wait_for_kafka(max_retries=10):
    for attempt in range(max_retries):
        try:
            producer.list_topics(timeout=5)
            return True
        except Exception as e:
            print(f"[Kafka] Attempt {attempt+1} failed: {e}")
            time.sleep(5)
    raise RuntimeError("Kafka not reachable")


def run_stream(delay=1):
    print("Starting run_stream")
    try:
        wait_for_kafka()
        total_pages = get_total_pages()
        print(f"[Stream] Total pages: {total_pages}")
        start_page = get_last_page() + 1
        print(f"[Stream] Starting from page: {start_page}")

        for page in range(start_page, total_pages + 1):
            listings = scrape_property24_page(page)
            print(f"[Stream] Page {page} returned {len(listings)} listings")

            for listing in listings:
                try:
                    producer.produce(
                        'raw_listings',
                        key=str(listing.get('page', 'unknown')),
                        value=json.dumps(listing),
                        callback=delivery_report
                    )
                except Exception as inner:
                    print(f"[Kafka Produce Error] {inner}")

            producer.flush()
            save_last_page(page)
            time.sleep(delay)

    except Exception as e:
        print(f"[Fatal Error] in run_stream: {e}")
        raise


if __name__ == "__main__":
    run_stream(delay=0.5)