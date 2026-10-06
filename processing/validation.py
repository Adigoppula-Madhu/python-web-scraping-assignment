VALID_SOURCES = {
    "Books to Scrape",
    "Quotes to Scrape"
}


def validate_record(record):
    problems = []

    # Check source
    if record.get("source") not in VALID_SOURCES:
        problems.append("unknown_source")

    # Check name/title
    if not record.get("name_or_title"):
        problems.append("missing_name")

    # Check URL
    source_url = str(record.get("source_url") or "")

    if not source_url.startswith(("http://", "https://")):
        problems.append("invalid_url")

    # Check price
    price = record.get("price")

    if price is not None:
        if not isinstance(price, (int, float)) or price < 0:
            problems.append("invalid_price")

    # Check rating
    rating = record.get("rating")

    if rating is not None:
        if rating not in (1, 2, 3, 4, 5):
            problems.append("invalid_rating")

    return problems

