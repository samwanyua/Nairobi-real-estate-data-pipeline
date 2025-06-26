import json
from kafka import KafkaProducer
from scraper.property24_scraper import scrape_property24
import time

# initialize kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer= lambda v: json.dumps(v).encode('utf-8'))

def send_to_kafka(listings, topic='raw_listings'):
    for listing in listings:
        try:
            producer.send(topic, listing)
            print(f"Sent to Kafka: {listing['title']} - {listing['price']}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Failed to send: {e}")

if __name__ == "__main__":
    print("Scraping property listings...")
    listings = scrape_property24(pages=9266)
    if listings:
        print(f"{len(listings)} listings scraped. Sending to kafka...")
        send_to_kafka(listings)
    else:
        print("No listings found")