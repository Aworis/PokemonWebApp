import logging
import time
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from requests import Session

logger = logging.getLogger(__name__)

class WebScraper(ABC):
    """
    Abstrakte Basisklasse für spezialisierten Scraper.
    """

    def __init__(self, session: Session, urls: list[str]):
        self._session = session
        self._urls = urls

    @property
    def urls(self) -> list[str]:
        return self._urls

    def fetch_page(self, url: str, retries: int, delay: int) -> str | None:
        """
        Ruft die HTML-Inhalte der angegebenen URL über die Session ab.

        :param str url: Die Ziel-URL, die abgerufen werden soll.
        :param int retries: Anzahl verbleibender Wiederholungsversuche bei Fehlern.
        :param int delay: Sekundenzahl, die vor einem erneuten Versuch gewartet wird.
        :return: HTML-Inhalt als String oder None bei Fehler.
        """

        for attempt in range(retries + 1):
            try:
                response = self._session.get(url, timeout=10)
                response.raise_for_status()
                return response.text

            except requests.exceptions.Timeout:
                msg = f"Timeout beim Abrufen von {url}."
            except requests.exceptions.HTTPError as e:
                msg = f"HTTP-Fehler {e.response.status_code} beim Abrufen von {url}."
            except requests.exceptions.ConnectionError:
                msg = f"Verbindungsfehler: Keine Verbindung zu {url} möglich."
            except requests.RequestException as e:
                msg = f"Fehler beim Abrufen von {url}: {e}"

            if attempt < retries:
                logger.warning(f"{msg} Neuer Versuch in {delay * (2 ** attempt)} Sekunden "
                               f"({retries - attempt} verbleibend).")
                time.sleep(delay)
            else:
                logger.error(f"{msg} Alle Versuche fehlgeschlagen.")
                return None

    def parse_html(self, html: str) -> list[dict]:
        """
        Parst den übergebenen HTML-Inhalt und extrahiert strukturierte Daten.
        Gibt eine leere Liste zurück, wenn Fehler auftreten
        """

        if not isinstance(html, str):
            logger.error("parse_html erwartet einen String, got %s", type(html).__name__)
            return []

        try:
            logger.info("Parsen gestartet.")
            soup = BeautifulSoup(html, "html.parser")
            data = self._extract_data(soup)
            logger.info("HTML erfolgreich geparst")
            return data
        except Exception as e:
            logger.exception(f"Fehler beim Parsen des HTML-Inhalts: {e}")
            return []

    @abstractmethod
    def _extract_data(self, soup: BeautifulSoup) -> list[dict]:
        """
        Extrahiert je nach Scraper-Typ Daten aus HTML-Elementen.
        """
        pass