# scraper/property24_scraper.py

import requests
from bs4 import BeautifulSoup
import time

def scrape_property24(pages=9266, delay=1):
    listings = []

    base_url = "https://www.property24.co.ke/property-for-sale-in-nairobi-c1890"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for page in range(1, pages + 1):
        url = base_url if page == 1 else f"{base_url}?Page={page}"
        print(f"🔍 Scraping Property24 - Page {page} - {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"❌ Failed to fetch page {page}: {e}")
            continue

        cards = soup.select(".p24_content")
        for card in cards:
            try:
                price = card.select_one(".p24_price")
                price = price.text.strip() if price else None

                title = card.select_one(".p24_propertyTitle")
                title = title.text.strip() if title else None

                location = card.select_one(".p24_location")
                location = location.text.strip() if location else None

                address = card.select_one(".p24_address")
                address = address.text.strip() if address else None

                description = card.select_one(".p24_excerpt")
                description = description.text.strip() if description else None

                features = card.select(".p24_featureDetails span")
                beds = features[0].text.strip() if len(features) > 0 else None
                baths = features[1].text.strip() if len(features) > 1 else None
                parking = features[2].text.strip() if len(features) > 2 else None

                size_span = card.select_one(".p24_size span")
                size = size_span.text.strip() if size_span else None

                listings.append({
                    "title": title,
                    "price": price,
                    "location": location,
                    "address": address,
                    "description": description,
                    "bedrooms": beds,
                    "bathrooms": baths,
                    "parking": parking,
                    "size": size,
                    "source": "property24",
                    "page": page
                })

            except Exception as e:
                print(f"⚠️ Error parsing listing on page {page}: {e}")

        time.sleep(delay)

    return listings


if __name__ == "__main__":
    from pprint import pprint
    data = scrape_property24(pages=2)
    pprint(data)
