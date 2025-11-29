import logging

from bs4 import BeautifulSoup

from abstract_web_scraper import WebScraper

logger = logging.getLogger(__name__)

class AttackenScraper(WebScraper):
    """
    Webscraper für Pokémon-Attacken.

    Dieser Scraper ruft HTML-Seiten ab, die Informationen zu Pokémon-Attacken
    enthalten, und extrahiert aus dem HTML die relevanten Daten für
    den Pokédex.

    Extrahierte Daten:
        - name: Der Name der Attacke.
        - beschreibung: Eine kurze textuelle Beschreibung der Attacke.
        - effekt:
        - staerke:
        - genauigkeit:
        - angriffspunkte:
    """

    def _extract_data(self, soup: BeautifulSoup) -> list[dict]:
        block = soup.select_one(".well")
        if not block:
            return []

        data = {
            "name": block.select_one("h1").get_text(strip=True),
            "beschreibung": block.select_one("p").get_text(strip=True),
        }
        return [data]