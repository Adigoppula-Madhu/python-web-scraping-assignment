import logging
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import create_session


logger = logging.getLogger(__name__)


class BooksScraper:

    def __init__(self):
        self.start_url = "https://books.toscrape.com/"
        self.session = create_session()

    def parse_page(self, soup, page_url):
        records = []

        books = soup.select("article.product_pod")

        for book in books:
            try:
                link = book.select_one("h3 > a")
                price = book.select_one("p.price_color")
                rating = book.select_one("p.star-rating")

                record = {
                    "title": link.get("title") if link else None,
                    "href": (
                        urljoin(page_url, link["href"])
                        if link and link.get("href")
                        else None
                    ),
                    "price_raw": price.get_text() if price else None,
                    "rating_raw": (
                        " ".join(rating.get("class", []))
                        if rating
                        else None
                    ),
                }

                records.append(record)

            except Exception as exc:
                logger.warning(
                    "Failed to parse a book on %s: %s",
                    page_url,
                    exc
                )

        return records

    def scrape(self):
        url = self.start_url
        page_number = 1
        records = []

        while url:
            logger.info("Scraping Books page %d: %s", page_number, url)

            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                response.encoding = "utf-8"

            except Exception as exc:
                logger.error(
                    "Failed to fetch Books page %s: %s",
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
            "Books scraping completed. Records collected: %d",
            len(records)
        )

        return records
