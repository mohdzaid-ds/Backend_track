# Polite Book Scraper

A Python-based web scraping project that collects book information from the **Books to Scrape** practice website.

The project is designed as a small, reliable scraping pipeline that fetches catalogue pages, discovers book URLs, extracts book information, normalizes the data, validates the records, and stores the results as JSON.

## Project Overview

The scraper processes the first three catalogue pages from Books to Scrape and collects information for the books listed on those pages.

The main processing flow is:

```text
Fetch
  ↓
Extract
  ↓
Normalize
  ↓
Validate
  ↓
Store
  ↓
Report
```

The scraper also includes basic caching and failure handling so that development runs do not repeatedly download the same catalogue pages and a single failed page does not stop the entire process.

## Target Website

**Website:** Books to Scrape

Books to Scrape is a practice website intended for learning and testing web scraping techniques.

Before scraping a website, its rules and terms should always be checked. For this project, the `robots.txt` endpoint was checked. It returned a `404 Not Found`, so there was no robots file available to interpret for this sandbox.

This project is intended only for the specified practice website.

> I will not reuse this code on another site without checking its rules and terms first.

## Scope

The scraper is intentionally limited to:

* The first 3 catalogue pages
* The books discovered on those pages
* Individual book detail pages
* Structured JSON output
* Basic failure and run reporting

The project does not use a database, paid proxy service, browser automation, or cloud infrastructure.

## Data Collected

For each book, the scraper works with information such as:

* Book title
* Product URL
* Price
* Availability
* Rating
* Description
* Source catalogue page
* Fetch timestamp

The original price text is preserved while the price is also converted into a numeric GBP value.

For example:

```text
£51.77 → 51.77
```

## Politeness Measures

The scraper follows several basic practices intended to avoid unnecessary requests:

* Uses an identifying `User-Agent`
* Uses request timeouts
* Checks HTTP status codes
* Waits between real requests
* Uses cached catalogue HTML during development
* Avoids repeatedly downloading the same catalogue pages
* Handles individual page failures without terminating the complete run

## Caching

Catalogue HTML can be cached locally during development.

This provides two benefits:

1. The first run downloads the page.
2. Later development runs can use the saved HTML instead of making another request.

The cache is kept outside the tracked source code and should not be committed to the repository.

## Data Validation

Scraped HTML should be treated as untrusted input.

Before a book record is written to the final output, the extracted information is normalized and checked against the project's expected schema.

Valid records are stored in:

```text
output/books.json
```

Records that cannot be validated are separated into:

```text
output/errors.json
```

## Run Report

Each scraper execution produces a structured report:

```text
output/run-report.json
```
## Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/your-username/polite-scraper.git
cd polite-scraper
```

Replace:

```text
your-username
```

with your actual GitHub username.

## Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

## Install Dependencies

```powershell
pip install -r requirements.txt
```

## Run the Scraper

```powershell
python src/main.py
```

## Output

After a successful run, the following files will be generated:

```text
output/
├── books.json
├── errors.json
└── run-report.json
```








The report records information about the execution, such as:

* Start time
* Execution duration
* Pages fetched
* Cache hits
* Valid records
* Invalid records
* Failed pages

This makes the scraper run easier to inspect and troubleshoot.

## Failure Handling

A failure on one book page should not prevent the remaining books from being processed.

The scraper handles individual failures separately and records failed pages in the run report.

The project also tests failure handling with a deliberately invalid URL.

For temporary problems such as timeouts or server errors, a limited retry can be attempted. Permanent client errors such as `404` or `403` should not be repeatedly retried.

## Idempotency

Running the scraper multiple times should not continuously duplicate the same books.

Book URLs are treated as the identity of individual records.

The intended result is that processing the same three catalogue pages repeatedly still produces the same set of 60 unique books rather than adding duplicates.

## Project Structure

The project is organized approximately as follows:

```text
polite_scraper/
│
├── src/
│   └── main.py
│
├── cache/
│   └── catalogue-page-*.html
│
├── output/
│   ├── books.json
│   ├── errors.json
│   └── run-report.json
│
├── .gitignore
└── README.md
```

Generated cache files and other temporary files should remain excluded from Git.

## Installation

Create and activate a Python virtual environment, then install the required dependencies.

The project uses:

* Python 3.10+
* requests
* BeautifulSoup
* Pydantic

Install dependencies with:

```powershell
pip install requests beautifulsoup4 pydantic
```

## Running the Scraper

From the project directory:

```powershell
python src/main.py
```

The scraper should process the first three catalogue pages and generate the JSON output and run report.

## Expected Result

A successful run should produce:

```text
output/
├── books.json
├── errors.json
└── run-report.json
```

The main output should contain **60 unique book records** from the first three catalogue pages.

Each successfully processed record contains the extracted book information together with its normalized price and provenance information.

## Why Browser Automation Is Not Required

The target website provides the required book information directly in its HTML responses.

Because the required content can be obtained through normal HTTP requests and parsed from HTML, browser automation is unnecessary for this project.

Using `requests` and BeautifulSoup keeps the implementation lightweight and makes the scraping process easier to understand and test.

## Limitations

This project is intentionally small and educational.

It is designed for the Books to Scrape sandbox and the first three catalogue pages only. It is not intended to be a general-purpose production scraper or to bypass website restrictions.

Changes to the target website's HTML structure could require updates to the extraction logic.

## Ethical Considerations

Web scraping should be performed responsibly.

Before applying a scraper to a real website, the website's robots rules, terms of service, access restrictions, request limits, and applicable laws should be reviewed.

This project uses a practice website specifically intended for scraping exercises and keeps its request rate deliberately low.

## Project Status

The project demonstrates the following scraping concepts:

* HTTP requests
* HTML parsing
* URL handling
* Data extraction
* Data normalization
* Schema validation
* Caching
* Failure handling
* JSON storage
* Run reporting
* Idempotent processing
* Responsible scraping practices

