import re
from urllib.parse import urljoin


RATING_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
}


def clean_text(value):
    if value is None:
        return None

    text = " ".join(
        value.replace("\xa0", " ").split()
    )

    return text or None


def strip_quotes(value):
    if value is None:
        return None

    return value.strip("“”\"")


def clean_price(raw):
    if not raw:
        return None

    match = re.search(
        r"\d+(?:\.\d+)?",
        raw.replace(",", "")
    )

    return float(match.group()) if match else None


def clean_rating(raw):
    for word in (raw or "").lower().split():
        if word in RATING_MAP:
            return RATING_MAP[word]

    return None


def clean_tags(tags):
    if not tags:
        return None

    cleaned = [
        clean_text(tag).lower()
        for tag in tags
        if clean_text(tag)
    ]

    return ";".join(sorted(cleaned)) if cleaned else None


def normalize_url(url, base_url=None):
    if not url:
        return None

    if base_url:
        url = urljoin(base_url, url)

    if url.startswith(("http://", "https://")):
        return url

    return None
