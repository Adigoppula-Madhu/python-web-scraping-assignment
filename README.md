# Web Scraping Assignment

## Overview

This project scrapes data from two websites:

- Books to Scrape
- Quotes to Scrape

The scraped data is cleaned, validated, deduplicated, consolidated into a common schema, and exported as CSV and JSON.

The project is implemented in Python and can be executed using a single command:

```bash
python main.py
```

## Requirements

- Python 3.10–3.12
- requests
- beautifulsoup4
- lxml
- pytest

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Project

Run the complete scraping and processing pipeline with:

```bash
python main.py
```

The program will:

1. Scrape Books to Scrape.
2. Scrape Quotes to Scrape.
3. Clean the collected data.
4. Validate the records.
5. Detect and remove duplicate records.
6. Consolidate records into a common schema.
7. Export the final dataset to CSV.
8. Generate a summary report in JSON.
9. Write execution details and errors to a log file.

## Project Structure

```text
scraping_assignment/
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── duplication.py
├── tests/
│   ├── conftest.py
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_duplication.py
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
├── logs/
│   └── scraper.log
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

## Scraping Approach

### Books to Scrape

The scraper starts from:

```text
https://books.toscrape.com/
```

It extracts book information from each listing page.

Important selectors used include:

- `article.product_pod` for each book record
- `h3 > a` for the book title and product link
- `p.price_color` for price
- `p.star-rating` for rating
- `li.next > a` for pagination

The scraper uses the website's `next` link to move to the next page rather than hard-coding page numbers.

The following information is collected from each book:

- title
- product URL
- price
- rating

### Quotes to Scrape

The scraper starts from:

```text
https://quotes.toscrape.com/
```

Important selectors used include:

- `div.quote` for each quote record
- `span.text` for quote text
- `small.author` for author
- `a.tag` for tags
- `a[href^="/author/"]` for the author page
- `li.next > a` for pagination

It extracts:

- quote text
- author
- tags
- author URL
- page URL

Pagination is handled dynamically using the `next` link on each page.

## Request Handling

The HTTP session includes:

- a custom User-Agent
- request timeouts
- retry handling for temporary HTTP errors
- a short delay between requests

Retries are configured for the following HTTP status codes:

```text
429
500
502
503
504
```

If a page request fails, the error is logged and the scraper stops processing that source rather than crashing the entire program.

## Data Cleaning

The collected data is normalized before validation.

Cleaning includes:

- removing unnecessary whitespace
- normalizing text
- removing surrounding quotation marks from quotes
- converting prices to numeric values
- converting book ratings from words to numbers
- normalizing tags
- normalizing URLs

Book ratings are converted to numeric values from 1 to 5.

## Data Validation

Each normalized record is validated before being included in the final dataset.

Validation checks include:

- valid source
- required name or title
- valid HTTP/HTTPS source URL
- non-negative price
- rating between 1 and 5

Records that fail validation are rejected and reported in the summary JSON file.

## Deduplication

Duplicate records are detected using a SHA-256 fingerprint based on normalized identifying information.

Before hashing, the identifying values are:

- converted to lowercase
- stripped of punctuation
- normalized for whitespace

For books, the fingerprint uses:

- source
- book title

For quotes, the fingerprint uses:

- source
- author
- the first 50 characters of the quote text

Duplicate records are removed rather than flagged separately. The number of duplicates detected is recorded in the summary report.

## Common Output Schema

The final dataset uses the following common schema:

| Field           | Description                                 |
| --------------- | ------------------------------------------- |
| `source`        | Source website                              |
| `source_url`    | URL associated with the scraped record      |
| `name_or_title` | Book title or quote text                    |
| `category`      | Category, when available                    |
| `price`         | Book price                                  |
| `rating`        | Book rating                                 |
| `author`        | Quote author                                |
| `tags`          | Quote tags                                  |
| `description`   | Description, when available                 |
| `scraped_at`    | UTC timestamp when the record was processed |

## Assumptions

- The websites are publicly accessible and do not require authentication.
- Missing fields are represented with empty values rather than invented data.
- The `category` and `description` fields are optional in the current implementation and are left empty to avoid additional detail-page requests.
- The scraper follows the `next` link provided by each website until no next page is available.
- Duplicate records are removed rather than retained with a duplicate flag.
- The final dataset preserves the source information for every record.

## Optional Fields

The `category` and `description` fields are left empty in the current implementation.

The assignment permits omitting additional detail-page requests for these fields. This keeps the scraper efficient while still collecting the required listing-page data.

## Output Files

### `output/final_dataset.csv`

Contains the final consolidated dataset after cleaning, validation, and deduplication.

### `output/summary_report.json`

Contains:

- records collected per source
- raw record count
- cleaned record count
- rejected record count
- rejection reasons
- duplicate count
- final record count
- reconciliation information
- start time
- end time
- execution duration

### `logs/scraper.log`

Contains execution logs for:

- scraping progress
- page numbers
- request failures
- parsing failures
- record counts
- output generation

## Testing

Unit tests are provided for:

- data cleaning
- validation
- duplicate detection

Run the tests with:

```bash
pytest
```

The final test run produced:

```text
9 passed
```

## Final Run Results

The completed scraping run produced the following results:

| Metric              | Result |
| ------------------- | -----: |
| Books collected     |  1,000 |
| Quotes collected    |    100 |
| Raw records         |  1,100 |
| Rejected records    |      0 |
| Duplicates detected |      1 |
| Final records       |  1,099 |

The reconciliation is:

```text
Raw records - Rejected records - Duplicates
= Final records

1100 - 0 - 1
= 1099
```

The reconciliation check passed successfully.

## Limitations

The current implementation intentionally does not make additional requests to individual book detail pages for category and description information.

These fields therefore remain empty in the final dataset, as permitted by the assignment.

If detail-page requests were added in the future, category and description could be populated without changing the common schema.

## AI Usage Summary

AI assistance was used during development for understanding the assignment requirements, planning the project structure, understanding Python and BeautifulSoup concepts, generating initial code suggestions, debugging errors, creating tests, reviewing the implementation, and improving documentation.

The final implementation was reviewed, adapted, executed, and tested locally.

See `AI_USAGE.md` for detailed information about AI-assisted development, representative prompts, changes made after reviewing AI output, and verification.

## Conclusion

The project successfully scrapes both target websites, handles pagination dynamically, processes and validates the collected data, removes duplicates, and generates the required CSV, JSON, and log outputs.
