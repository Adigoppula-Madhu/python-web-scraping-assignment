import hashlib
import re


def make_fingerprint(record):
    if record["source"] == "Books to Scrape":
        key = f'{record["source"]} {record["name_or_title"]}'
    else:
        key = (
            f'{record["source"]} '
            f'{record["author"]} '
            f'{record["name_or_title"][:50]}'
        )

    # Convert to lowercase
    key = key.lower()

    # Remove punctuation
    key = re.sub(r"[^\w\s]", "", key)

    # Collapse extra spaces
    key = " ".join(key.split())

    # Create a SHA-256 fingerprint
    return hashlib.sha256(
        key.encode("utf-8")
    ).hexdigest()


def find_duplicates(records):
    seen = set()
    unique = []
    duplicates = []

    for record in records:
        fingerprint = make_fingerprint(record)

        if fingerprint in seen:
            duplicates.append(record)
        else:
            unique.append(record)
            seen.add(fingerprint)

    return unique, duplicates

