import logging
import time
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from requests import Session


class WebScraper(ABC):
    """Abstrakte Basisklasse für spezialisierten Scraper.
    """

    def __init__(self, session: Session, urls: list[str]):
        self._session = session
        self._logger = logging.getLogger(__name__)
        self._urls = urls

    @property
    def scraper_urls(self) -> list[str]:
        return self._urls

    def fetch_page(self, url: str, retries: int, delay: int) -> str | None:
        """
        Ruft die HTML-Inhalte der angegebenen URL über die Session ab.

        :param str url: Die Ziel-URL, die abgerufen werden soll.
        :param int retries: Anzahl verbleibender Wiederholungsversuche bei Fehlern.
        :param int delay: Sekundenzahl, die vor einem erneuten Versuch gewartet wird.
        """

        try:
            response = self._session.get(url, timeout = 10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if retries > 0:
                self._logger.warning(f"Fehler beim Abrufen von {url}. {retries} verbleibende Versuche. Neuer Versuch in {delay} Sekunden...")
                time.sleep(delay)
                return self.fetch_page(url, retries-1, delay)
            self._logger.error(f"Fehler beim Abrufen von {url}: {e}")
            return None

    def parse_data(self, html: str) -> list[dict]:
        """Parst den übergebenen HTML-Inhalt.
        """
        soup = BeautifulSoup(html, "html.parser")
        return self._extract_data(soup)

    @abstractmethod
    def _extract_data(self, soup: BeautifulSoup) -> list[dict]:
        """Extrahiert je nach Scraper-Typ Daten aus HTML-Elementen.
        """
        pass