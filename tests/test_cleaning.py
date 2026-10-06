from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
    normalize_url,
)


def test_clean_text():
    assert clean_text("  Hello   World \n") == "Hello World"


def test_strip_quotes():
    assert strip_quotes('"Hello World"') == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("star-rating Three") == 3


def test_clean_tags():
    assert clean_tags(["World", "thinking", "change"]) == (
        "change;thinking;world"
    )


def test_normalize_url():
    result = normalize_url(
        "/book/test",
        "https://books.toscrape.com/"
    )

    assert result == "https://books.toscrape.com/book/test"