import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import os
import time

BASE_URL = "https://www.property24.co.ke/property-for-sale-in-nairobi-c1890"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_total_pages():
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        pagination = soup.select("ul.pagination li.pagelink a")
        pages = [int(a.text.strip()) for a in pagination if a.text.strip().isdigit()]
        return max(pages) if pages else 1
    except Exception as e:
        print(f"Error getting total pages: {e}")
        return 1


def scrape_property24_page(page):
    url = BASE_URL if page == 1 else f"{BASE_URL}?Page={page}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"Failed to fetch page {page}: {e}")
        return []

    cards = soup.select(".p24_content")
    results = []
    for card in cards:
        try:
            price_tag = card.select_one(".p24_price")
            title_tag = card.select_one(".p24_propertyTitle")
            loc_tag = card.select_one(".p24_location")
            addr_tag = card.select_one(".p24_address")
            desc_tag = card.select_one(".p24_excerpt")
            features = card.select(".p24_featureDetails span")

            listing = {
                "title": title_tag.text.strip() if title_tag else None,
                "price": price_tag.text.strip() if price_tag else None,
                "location": loc_tag.text.strip() if loc_tag else None,
                "address": addr_tag.text.strip() if addr_tag else None,
                "description": desc_tag.text.strip() if desc_tag else None,
                "bedrooms": features[0].text.strip() if len(features) > 0 else None,
                "bathrooms": features[1].text.strip() if len(features) > 1 else None,
                "parking": features[2].text.strip() if len(features) > 2 else None,
                "size": card.select_one(".p24_size span").text.strip() if card.select_one(".p24_size span") else None,
                "source": "property24",
                "page": page,
                "scraped_at": datetime.utcnow()
            }
            results.append(listing)
        except Exception as e:
            print(f"Error parsing listing on page {page}: {e}")
    return results


def save_to_postgres(listings):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "nrbproperties"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            host=os.getenv("POSTGRES_HOST", "postgres_main"),
            port=os.getenv("POSTGRES_PORT", "5432"),
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO properties (
            title, price, location, address, description, bedrooms,
            bathrooms, parking, size, source, page, scraped_at
        ) VALUES %s
        """

        values = [
            (
                l["title"], l["price"], l["location"], l["address"], l["description"],
                l["bedrooms"], l["bathrooms"], l["parking"], l["size"],
                l["source"], l["page"], l["scraped_at"]
            )
            for l in listings
        ]

        execute_values(cursor, insert_query, values)
        conn.commit()
        print(f"✅ Inserted {len(listings)} records into PostgreSQL.")
    except Exception as e:
        print(f" Failed to insert into Postgres: {e}")
    finally:
        if conn:
            conn.close()


def scrape_and_store():
    """
    Main function for Airflow DAG: Scrape Property24 and store in PostgreSQL.
    """
    print("📦 Starting scrape and store process...")
    total_pages = get_total_pages()
    print(f"🔢 Total pages: {total_pages}")

    all_listings = []
    for page in range(1, total_pages + 1):
        listings = scrape_property24_page(page)
        if listings:
            all_listings.extend(listings)
        time.sleep(1) 

    if all_listings:
        save_to_postgres(all_listings)
    else:
        print(" No listings found.")


if __name__ == "__main__":
    scrape_and_store()
