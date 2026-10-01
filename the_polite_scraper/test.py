import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from jsonschema import validate


BASE_URL = "https://books.toscrape.com/"
PAGES_TO_SCRAPE = 3

HEADERS = {
    "User-Agent": "BookScraper/1.0"
}

books = []
errors = []

start_time = datetime.now().isoformat()


def clean_price(price_text):
    """
    Convert a price such as £51.77 into a number.
    """
    price = re.sub(r"[^\d.]", "", price_text)
    return float(price)


def get_rating(book):
    """
    Convert the star rating class into a number.
    """
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    rating_element = book.select_one("p.star-rating")

    if rating_element:
        classes = rating_element.get("class", [])

        for rating_name, rating_value in rating_map.items():
            if rating_name in classes:
                return rating_value

    return None


for page_number in range(1, PAGES_TO_SCRAPE + 1):

    if page_number == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}catalogue/page-{page_number}.html"

    print(f"\nScraping: {url}")

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        print("Status code:", response.status_code)

        if response.status_code != 200:
            error = {
                "page": page_number,
                "url": url,
                "error": f"HTTP {response.status_code}"
            }

            errors.append(error)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        page_books = soup.select("article.product_pod")

        print("Books found:", len(page_books))

        for book in page_books:

            try:
                title_element = book.select_one("h3 a")

                price_element = book.select_one(".price_color")

                availability_element = book.select_one(".instock")

                if not title_element or not price_element:
                    raise ValueError("Required book information is missing")

                title = title_element.get("title", "").strip()

                book_url = BASE_URL + "catalogue/" + title_element.get("href", "").replace(
                    "../", ""
                )

                price = clean_price(price_element.get_text(strip=True))

                availability = (
                    availability_element.get_text(strip=True)
                    if availability_element
                    else "Unknown"
                )

                rating = get_rating(book)

                book_data = {
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "rating": rating,
                    "url": book_url
                }

                books.append(book_data)

            except Exception as e:

                errors.append({
                    "page": page_number,
                    "url": url,
                    "error": str(e)
                })


    except Exception as e:

        errors.append({
            "page": page_number,
            "url": url,
            "error": str(e)
        })


# --------------------------------------------------
# Save books
# --------------------------------------------------

with open("book.json", "w", encoding="utf-8") as file:
    json.dump(
        books,
        file,
        indent=4,
        ensure_ascii=False
    )


# --------------------------------------------------
# Validate JSON against schema
# --------------------------------------------------

schema_validation = "passed"

try:

    with open("schema.json", "r", encoding="utf-8") as file:
        schema = json.load(file)

    validate(
        instance=books,
        schema=schema
    )

except Exception as e:

    schema_validation = "failed"

    errors.append({
        "type": "schema_validation",
        "error": str(e)
    })


# --------------------------------------------------
# Save errors
# --------------------------------------------------

with open("error.json", "w", encoding="utf-8") as file:

    json.dump(
        {
            "errors": errors
        },
        file,
        indent=4,
        ensure_ascii=False
    )


# --------------------------------------------------
# Create run report
# --------------------------------------------------

end_time = datetime.now().isoformat()

run_report = {
    "status": "success" if not errors else "completed_with_errors",
    "started_at": start_time,
    "completed_at": end_time,
    "pages_requested": PAGES_TO_SCRAPE,
    "books_scraped": len(books),
    "errors": len(errors),
    "schema_validation": schema_validation
}

with open("run_report.json", "w", encoding="utf-8") as file:

    json.dump(
        run_report,
        file,
        indent=4,
        ensure_ascii=False
    )


# --------------------------------------------------
# Final output
# --------------------------------------------------

print("\n-----------------------------")
print("Scraping completed")
print("-----------------------------")

print("Books scraped:", len(books))
print("Errors:", len(errors))
print("Schema validation:", schema_validation)

print("\nFiles generated:")
print("- book.json")
print("- error.json")
print("- run_report.json")