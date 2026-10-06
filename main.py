import csv
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
)

from processing.validation import validate_record
from processing.duplication import find_duplicates


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
JSON_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"


# ---------------------------------------------------------
# Common schema
# ---------------------------------------------------------

FIELDNAMES = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Convert Books record to common schema
# ---------------------------------------------------------

def normalize_book(raw_record, scraped_at):
    return {
        "source": "Books to Scrape",
        "source_url": raw_record.get("href"),
        "name_or_title": clean_text(raw_record.get("title")),
        "category": None,
        "price": clean_price(raw_record.get("price_raw")),
        "rating": clean_rating(raw_record.get("rating_raw")),
        "author": None,
        "tags": None,
        "description": None,
        "scraped_at": scraped_at,
    }


# ---------------------------------------------------------
# Convert Quotes record to common schema
# ---------------------------------------------------------

def normalize_quote(raw_record, scraped_at):
    return {
        "source": "Quotes to Scrape",
        "source_url": raw_record.get("page_url"),
        "name_or_title": strip_quotes(
            clean_text(raw_record.get("quote_raw"))
        ),
        "category": None,
        "price": None,
        "rating": None,
        "author": clean_text(raw_record.get("author_raw")),
        "tags": clean_tags(raw_record.get("tags_raw")),
        "description": None,
        "scraped_at": scraped_at,
    }


# ---------------------------------------------------------
# Save final CSV
# ---------------------------------------------------------

def save_csv(records):
    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()
        writer.writerows(records)

    logger.info(
        "CSV saved: %s",
        CSV_FILE
    )


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main():

    start_time = datetime.now(timezone.utc)

    logger.info("Scraping assignment started.")

    # ---------------------------------------------
    # 1. Scrape Books
    # ---------------------------------------------

    books_scraper = BooksScraper()
    raw_books = books_scraper.scrape()

    logger.info(
        "Raw Books records collected: %d",
        len(raw_books)
    )

    # ---------------------------------------------
    # 2. Scrape Quotes
    # ---------------------------------------------

    quotes_scraper = QuotesScraper()
    raw_quotes = quotes_scraper.scrape()

    logger.info(
        "Raw Quotes records collected: %d",
        len(raw_quotes)
    )

    # ---------------------------------------------
    # 3. Clean + normalize records
    # ---------------------------------------------

    scraped_at = datetime.now(
        timezone.utc
    ).isoformat()

    cleaned_records = []

    cleaned_per_source = {
        "Books to Scrape": 0,
        "Quotes to Scrape": 0,
    }

    rejected_by_reason = {}
    rejected_total = 0

    # Books
    for raw_record in raw_books:

        try:
            record = normalize_book(
                raw_record,
                scraped_at
            )

            problems = validate_record(record)

            if problems:

                rejected_total += 1

                for problem in problems:
                    rejected_by_reason[problem] = (
                        rejected_by_reason.get(problem, 0) + 1
                    )

                logger.warning(
                    "Rejected Books record: %s",
                    problems
                )

                continue

            cleaned_records.append(record)

            cleaned_per_source[
                "Books to Scrape"
            ] += 1

        except Exception as exc:

            rejected_total += 1

            rejected_by_reason["processing_error"] = (
                rejected_by_reason.get(
                    "processing_error",
                    0
                ) + 1
            )

            logger.warning(
                "Failed to process Books record: %s",
                exc
            )

    # Quotes
    for raw_record in raw_quotes:

        try:
            record = normalize_quote(
                raw_record,
                scraped_at
            )

            problems = validate_record(record)

            if problems:

                rejected_total += 1

                for problem in problems:
                    rejected_by_reason[problem] = (
                        rejected_by_reason.get(problem, 0) + 1
                    )

                logger.warning(
                    "Rejected Quotes record: %s",
                    problems
                )

                continue

            cleaned_records.append(record)

            cleaned_per_source[
                "Quotes to Scrape"
            ] += 1

        except Exception as exc:

            rejected_total += 1

            rejected_by_reason["processing_error"] = (
                rejected_by_reason.get(
                    "processing_error",
                    0
                ) + 1
            )

            logger.warning(
                "Failed to process Quotes record: %s",
                exc
            )

    logger.info(
        "Records after cleaning and validation: %d",
        len(cleaned_records)
    )

    # ---------------------------------------------
    # 4. Remove duplicates
    # ---------------------------------------------

    unique_records, duplicate_records = find_duplicates(
        cleaned_records
    )

    duplicates_detected = len(duplicate_records)

    logger.info(
        "Duplicates detected: %d",
        duplicates_detected
    )

    # ---------------------------------------------
    # 5. Save CSV
    # ---------------------------------------------

    save_csv(unique_records)

    # ---------------------------------------------
    # 6. Create summary
    # ---------------------------------------------

    end_time = datetime.now(timezone.utc)

    duration_seconds = (
        end_time - start_time
    ).total_seconds()

    raw_total = (
        len(raw_books) +
        len(raw_quotes)
    )

    final_count = len(unique_records)

    expected_final_count = (
        raw_total
        - rejected_total
        - duplicates_detected
    )

    summary = {
        "collected_per_source": {
            "Books to Scrape": len(raw_books),
            "Quotes to Scrape": len(raw_quotes),
        },

        "raw_total": raw_total,

        "cleaned_per_source": cleaned_per_source,

        "rejected_total": rejected_total,

        "rejected_by_reason": rejected_by_reason,

        "duplicates_detected": duplicates_detected,

        "final_record_count": final_count,

        "reconciliation": {
            "raw_total": raw_total,
            "minus_rejected": rejected_total,
            "minus_duplicates": duplicates_detected,
            "expected_final_count": expected_final_count,
            "actual_final_count": final_count,
            "reconciles": (
                expected_final_count == final_count
            ),
        },

        "start_time": start_time.isoformat(),

        "end_time": end_time.isoformat(),

        "duration_seconds": duration_seconds,
    }

    # ---------------------------------------------
    # 7. Save JSON summary
    # ---------------------------------------------

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            summary,
            file,
            indent=2,
        )

    logger.info(
        "Summary saved: %s",
        JSON_FILE
    )

    logger.info(
        "Final records: %d",
        final_count
    )

    logger.info(
        "Scraping assignment completed."
    )

    print()
    print("=" * 50)
    print("SCRAPING COMPLETED")
    print("=" * 50)
    print(f"Raw records       : {raw_total}")
    print(f"Rejected records  : {rejected_total}")
    print(f"Duplicates        : {duplicates_detected}")
    print(f"Final records     : {final_count}")
    print(f"CSV               : {CSV_FILE}")
    print(f"Summary JSON      : {JSON_FILE}")
    print(f"Log               : {LOG_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    main()