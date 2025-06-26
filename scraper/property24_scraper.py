import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.property24.co.ke/property-for-sale-in-nairobi-c1890"
headers = {
    "User-Agent": "Mozilla/5.0"
}


def get_total_pages():
    """
    Fetches the pagination links and returns the highest page number.
    """
    try:
        resp = requests.get(BASE_URL, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")
        pagination = soup.select("ul.pagination li.pagelink a")

        pages = [int(a.text.strip()) for a in pagination if a.text.strip().isdigit()]
        return max(pages) if pages else 1

    except Exception as e:
        print(f"Error getting total pages: {e}")
        return 1  # fallback


def scrape_property24_page(page):
    """
    Scrape a single page of Property24 listings.
    """
    url = BASE_URL if page == 1 else f"{BASE_URL}?Page={page}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
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
            beds = features[0].text.strip() if len(features) > 0 else None
            baths = features[1].text.strip() if len(features) > 1 else None
            parking = features[2].text.strip() if len(features) > 2 else None

            size_span = card.select_one(".p24_size span")

            listing = {
                "title": title_tag.text.strip() if title_tag else None,
                "price": price_tag.text.strip() if price_tag else None,
                "location": loc_tag.text.strip() if loc_tag else None,
                "address": addr_tag.text.strip() if addr_tag else None,
                "description": desc_tag.text.strip() if desc_tag else None,
                "bedrooms": beds,
                "bathrooms": baths,
                "parking": parking,
                "size": size_span.text.strip() if size_span else None,
                "source": "property24",
                "page": page
            }
            results.append(listing)

        except Exception as e:
            print(f"Error parsing listing on page {page}: {e}")

    return results


if __name__ == "__main__":
    total = get_total_pages()
    print(f"🔢 Total pages: {total}")
    data = scrape_property24_page(1)
    from pprint import pprint; pprint(data)