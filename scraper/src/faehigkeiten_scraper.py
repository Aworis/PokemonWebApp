import logging

from bs4 import BeautifulSoup

from abstract_web_scraper import WebScraper

logger = logging.getLogger(__name__)

class FaehigkeitenScraper(WebScraper):

    def _extract_data(self, soup: BeautifulSoup) -> list[dict]:
        """
        Extrahiert die relevanten Daten einer Pokémon-Fähigkeit aus dem übergebenen
        HTML-Dokument.

        Enthaltene Daten:
            - name: Text des ersten <h1>-Elements (Name der Fähigkeit).
            - beschreibung: Text des ersten <p>-Elements direkt nach dem <h2>-Element.
        """

        block = soup.select_one(".well")
        if not block:
            return []

        data = {
            "name": block.select_one("h1").get_text(),
            "beschreibung": block.select_one("h2").find_next_sibling("p").get_text()
        }
        return [data]
