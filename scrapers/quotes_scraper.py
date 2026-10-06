import logging
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import create_session


logger = logging.getLogger(__name__)


class QuotesScraper:

    def __init__(self):
        self.start_url = "https://quotes.toscrape.com/"
        self.session = create_session()

    def parse_page(self, soup, page_url):
        records = []

        quotes = soup.select("div.quote")

        for quote in quotes:
            try:
                text = quote.select_one("span.text")
                author = quote.select_one("small.author")
                tags = quote.select("a.tag")
                author_link = quote.select_one('a[href^="/author/"]')

                record = {
                    "quote_raw": text.get_text() if text else None,
                    "author_raw": author.get_text() if author else None,
                    "tags_raw": [
                        tag.get_text() for tag in tags
                    ],
                    "author_url": (
                        urljoin(page_url, author_link["href"])
                        if author_link and author_link.get("href")
                        else None
                    ),
                    "page_url": page_url,
                }

                records.append(record)

            except Exception as exc:
                logger.warning(
                    "Failed to parse a quote on %s: %s",
                    page_url,
                    exc
                )

        return records

    def scrape(self):
        url = self.start_url
        page_number = 1
        records = []

        while url:
            logger.info(
                "Scraping Quotes page %d: %s",
                page_number,
                url
            )

            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                response.encoding = "utf-8"

            except Exception as exc:
                logger.error(
                    "Failed to fetch Quotes page %s: %s",
                    url,
                    exc
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            page_records = self.parse_page(soup, url)
            records.extend(page_records)

            next_link = soup.select_one("li.next > a")

            if next_link and next_link.get("href"):
                url = urljoin(url, next_link["href"])
            else:
                url = None

            page_number += 1

            time.sleep(0.5)

        logger.info(
            "Quotes scraping completed. Records collected: %d",
            len(records)
        )

        return records


