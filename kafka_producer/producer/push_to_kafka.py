import json, time, os
from confluent_kafka import Producer

from scraper.property24_scraper import get_total_pages, scrape_property24_page

CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'last_page.txt')
conf = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(conf)
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


def run_stream(delay=1):
    total_pages = get_total_pages()
    start_page = get_last_page() + 1
    print(f"Processing pages {start_page} to {total_pages}")

    for page in range(start_page, total_pages + 1):
        listings = scrape_property24_page(page)
        print(f"Page {page}: {len(listings)} listings")

        for listing in listings:
            producer.produce(
                'raw_listings',
                key=str(listing['page']),
                value=json.dumps(listing),
                callback=delivery_report
            )
            producer.poll(0)   # drive callbacks

        producer.flush()
        save_last_page(page)
        time.sleep(delay)

if __name__ == "__main__":
    run_stream(delay=0.5)