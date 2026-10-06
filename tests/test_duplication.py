from processing.duplication import find_duplicates


def test_duplicate_books_are_removed():

    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Example Book Title",
            "author": None,
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "  Example Book Title ",
            "author": None,
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "EXAMPLE BOOK TITLE",
            "author": None,
        },
    ]

    unique, duplicates = find_duplicates(records)

    assert len(unique) == 1
    assert len(duplicates) == 2