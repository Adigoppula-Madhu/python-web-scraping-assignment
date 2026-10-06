# AI Usage

## AI Tool Used

- ChatGPT

AI assistance was used throughout development as a coding and learning assistant. The final implementation was reviewed, executed, and tested locally.

## How AI Was Used

AI assistance was used for:

- understanding the assignment requirements
- planning the project structure
- understanding Python web scraping concepts
- understanding Requests and BeautifulSoup
- generating initial code suggestions
- explaining Python concepts and code
- debugging errors during development
- creating unit-test examples
- reviewing the implementation
- improving project documentation

## Representative Prompts

Examples of prompts used during development include:

1. "Help me build this Python web scraping assignment step by step using Requests and BeautifulSoup."

2. "How can I implement dynamic pagination by following the next link instead of hard-coding page numbers?"

3. "Explain how this BeautifulSoup selector works and how I can extract the required fields."

4. "Help me create cleaning and validation functions for price, rating, tags, URLs, and text."

5. "How can I implement duplicate detection using a normalized fingerprint?"

6. "Help me write unit tests for the cleaning, validation, and duplicate-detection functions."

7. "Review my project against the assignment requirements and identify anything missing."

## AI-Assisted Code Areas

AI assistance contributed to the development of the following areas:

### Project Structure

AI helped organize the project into separate modules for:

- scraping
- HTTP/session handling
- cleaning
- validation
- duplicate detection
- testing

### Web Scraping

AI assistance was used to understand and implement:

- Requests sessions
- User-Agent headers
- retry handling
- request timeouts
- BeautifulSoup parsing
- CSS selectors
- dynamic pagination
- URL handling
- missing HTML elements
- request failure handling

### Data Processing

AI assistance was used for:

- whitespace and text cleaning
- price extraction
- rating conversion
- tag normalization
- URL normalization
- validation rules
- duplicate fingerprints
- consolidation into the common schema

### Testing

AI assistance was used to create unit-test examples for:

- cleaning functions
- validation rules
- duplicate detection

## Changes Made After Reviewing AI Output

The AI-generated suggestions were reviewed and adapted during implementation.

Important changes and decisions included:

- The project was implemented using separate scraper and processing modules rather than putting all logic in `main.py`.
- The scraper follows the actual `next` link from each website instead of hard-coding page numbers.
- Missing fields are represented with empty values rather than invented data.
- The `category` and `description` fields are intentionally left empty because the assignment permits omitting additional detail-page requests.
- The duplicate-detection implementation uses the project's actual module name `processing/duplication.py`.
- A `tests/conftest.py` file was added so pytest could import the project modules correctly when tests were run from the project root.
- Temporary standalone test code and `if __name__ == "__main__"` blocks used during development were removed from the final scraper and processing modules.
- The README was reviewed against the assignment reference so that assumptions, limitations, pagination, data model, error handling, and AI usage were explicitly documented.

## Incorrect or Incomplete AI Suggestions Discovered

During development, some suggestions required correction or clarification:

- An initial attempt to run a file named `processing/deduplication.py` failed because the implemented module was named `processing/duplication.py`.
- The recommended project structure in the assignment uses `deduplication.py`, but the assignment states that the structure is only a recommendation. The implemented `duplication.py` module is used consistently by `main.py` and the tests.
- The initial pytest run had an import-path issue. This was resolved by adding `tests/conftest.py` to make the project root available during test collection.
- Documentation was reviewed against the assignment reference to ensure that AI usage, assumptions, limitations, and verification details were included.

## Human Verification

The final implementation was executed and tested locally.

The Books scraper collected 1,000 records.

The Quotes scraper collected 100 records.

The complete pipeline produced 1,099 final records after removing one duplicate.

No records were rejected during validation.

The reconciliation was:

```text
1100 - 0 - 1 = 1099
```

The reconciliation check passed successfully.

The final unit-test run produced:

```text
9 passed
```

The generated CSV, JSON summary, and log files were also checked after the final pipeline run.

## Final Responsibility

AI was used as an assistance and learning tool during development. The final implementation was reviewed, adapted, executed, and tested by the developer.

The developer is responsible for the final submitted code and understands the main scraping, cleaning, validation, deduplication, logging, and output-generation logic.
