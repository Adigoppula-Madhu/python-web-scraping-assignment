from processing.validation import validate_record


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "name_or_title": "A Light in the Attic",
        "source_url": "https://books.toscrape.com/book",
        "price": 51.77,
        "rating": 3,
    }

    assert validate_record(record) == []


def test_invalid_record():
    record = {
        "source": "Wrong Website",
        "name_or_title": "",
        "source_url": "abc",
        "price": -10,
        "rating": 8,
    }

    problems = validate_record(record)

    assert "unknown_source" in problems
    assert "missing_name" in problems
    assert "invalid_url" in problems
    assert "invalid_price" in problems
    assert "invalid_rating" in problems