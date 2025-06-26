import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.property24.co.ke/property-for-sale-in-nairobi-c1890"
headers = {
        "User-Agent": "Mozilla/5.0"
    }

listings = []

def get_total_pages():
    try:
        resp = requests.get(BASE_URL, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        pagination = soup.select("ul.pagination li.pagelink a")

        # Get the highest page number from pagination links
        pages = [int(a.text.strip()) for a in pagination if a.text.strip().isdigit()]
        return max(pages) if pages else 1
    except Exception as e:
        print(f"Error getting total pages: {e}")
        return 1  # fallback

def scrape_property24(delay=1):
    total_pages = get_total_pages()
    print(f"🔢 Total pages found: {total_pages}")

    for page in range(1, total_pages + 1):
        url = f"{BASE_URL}?Page={page}" if page > 1 else BASE_URL
        print(f"Scraping Property24 - Page {page} - {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
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
                print(f"Error parsing listing on page {page}: {e}")

        time.sleep(delay)

if __name__ == "__main__":
    scrape_property24()
