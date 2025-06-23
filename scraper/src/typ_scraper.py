from abstract_web_scraper import WebScraper
from config_loader import load_sitemap_url
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class TypScraper(WebScraper):

    def _extract_data(self, soup: BeautifulSoup) -> list[dict]:
        block = soup.select_one(".well")
        if not block:
            return []

        data = {
            "name": block.select_one("h1").get_text(strip=True),
            "beschreibung": block.select_one("p").get_text(strip=True)
        }
        return [data]