import requests
from bs4 import BeautifulSoup
import re
import time
import json
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from jsonschema import validate


# Website configuration

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

pages = [
    base_url.format(1),
    base_url.format(2),
    base_url.format(3)
]

# Identify the scraper

headers = {
    "User-Agent": "BookScraper/1.0"
}


# Store scraped books

books_data = []


# Check robots.txt

robots_url = "https://books.toscrape.com/robots.txt"

robot_parser = RobotFileParser()

robot_parser.set_url(robots_url)

try:

    robot_parser.read()

    print("robots.txt checked successfully")

except Exception as e:

    print("Could not read robots.txt:", e)

    raise SystemExit(
        "Scraper stopped because robots.txt could not be checked."
    )


# Check whether scraping is allowed
user_agent = headers["User-Agent"]

for page_url in pages:

    if not robot_parser.can_fetch(
        user_agent,
        page_url
    ):

        print(
            "Scraping is not allowed for:",
            page_url
        )

        raise SystemExit(
            "Scraper stopped because robots.txt does not allow access."
        )


print(
    "robots.txt allows scraping the selected pages"
)


# Scrape each page

for page_url in pages:

    print("\nScraping:", page_url)

    # Polite delay between requests
    time.sleep(2)

    # Request the page
    try:

        response = requests.get(
            page_url,
            headers=headers,
            timeout=10
        )

        # Fix character encoding
        response.encoding = response.apparent_encoding

        # Raise error for HTTP errors
        response.raise_for_status()

        print(
            "Status code:",
            response.status_code
        )

    except requests.RequestException as e:

        print(
            "Request failed:",
            e
        )

        continue


    # Parse HTML

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # Find all books
    books = soup.find_all(
        "article",
        class_="product_pod"
    )

    print(
        "Books found:",
        len(books)
    )


    
    # Process each book

    for book in books:

        try:

            
            # Title
            

            title_element = book.find("h3")

            if not title_element or not title_element.a:

                print(
                    "Skipping book: title not found"
                )

                continue


            title = title_element.a.get("title")

            if not title:

                print(
                    "Skipping book: title is empty"
                )

                continue


            # Book URL

            href = title_element.a.get("href")

            if not href:

                print(
                    "Skipping book:",
                    title,
                    "- URL not found"
                )

                continue


            book_url = urljoin(
                page_url,
                href
            )


            
            # Price
            

            price_element = book.find(
                "p",
                class_="price_color"
            )

            if not price_element:

                print(
                    "Skipping book:",
                    title,
                    "- price not found"
                )

                continue


            price_text = price_element.get_text(
                strip=True
            )


            # Extract numeric price
            price_match = re.search(
                r"\d+(?:\.\d+)?",
                price_text
            )


            if not price_match:

                print(
                    "Skipping book:",
                    title,
                    "- invalid price"
                )

                continue


            price = float(
                price_match.group()
            )


            # Availability
        

            availability_element = book.find(
                "p",
                class_="instock"
            )

            if not availability_element:

                print(
                    "Skipping book:",
                    title,
                    "- availability not found"
                )

                continue


            availability = availability_element.get_text(
                strip=True
            )

            # Store book

            books_data.append({
                "title": title,
                "url": book_url,
                "price": price,
                "availability": availability
            })


            # Display extracted data
            print(
                "\nTitle:",
                title
            )

            print(
                "Book URL:",
                book_url
            )

            print(
                "Price:",
                price
            )

            print(
                "Availability:",
                availability
            )


        except Exception as e:

            print(
                "Error processing book:",
                e
            )

            # Skip broken book
            continue


# Final book count

print(
    "\nTotal books collected:",
    len(books_data)
)

# Save data to JSON

with open(
    "books.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        books_data,
        file,
        indent=4,
        ensure_ascii=False
    )


print(
    "Data saved to books.json"
)

# Read JSON file

with open(
    "books.json",
    "r",
    encoding="utf-8"
) as file:

    saved_books = json.load(file)


print(
    "Books in JSON file:",
    len(saved_books)
)


# Load JSON Schema

try:

    with open(
        "schema.json",
        "r",
        encoding="utf-8"
    ) as file:

        schema = json.load(file)

except (FileNotFoundError, json.JSONDecodeError) as e:

    print(
        "Could not load schema.json:",
        e
    )

    raise SystemExit(
        "Scraper stopped because schema.json is missing or invalid."
    )


# Validate JSON Schema

try:

    validate(
        instance=saved_books,
        schema=schema
    )

    print(
        "JSON schema validation successful!"
    )

except Exception as e:

    print(
        "JSON schema validation failed!"
    )

    print(
        "Error:",
        e
    )
