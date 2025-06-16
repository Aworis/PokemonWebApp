import logging

import requests

from abstract_web_scraper import WebScraper
from scraper_result_handler import ScraperResultHandler


class ScraperManager:
    """Singleton-Klasse zur zentralen Verwaltung und Steuerung von Web-Scrapern.
    Stellt eine gemeinsame HTTP-Session zur Verfügung.
    """

    __instance = None
    __initialized = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            ScraperManager.__initialized = True  # Flag wird gesetzt. Verhindert erneuter Aufruf von __init__
            self.__scrapers = {}
            self.__session = requests.Session()
            self.__result_handler = ScraperResultHandler()
            self.__logger = logging.getLogger(__name__)

    def register_scraper(self, scraper_id: str, scraper_instance: WebScraper) -> None:
        """Registriert einen neuen Scraper unter einer eindeutigen ID.
        Wenn bereits ein Scraper mit dieser ID existiert, wird keine neue Registrierung durchgeführt.
        """

        if scraper_id in self.__scrapers:
            self.__logger.info(f"Scraper '{scraper_id}' ist bereits registriert.")
        else:
            self.__scrapers[scraper_id] = scraper_instance
            self.__logger.info(f"Scraper '{scraper_id}' registriert.")

    def run_scraper(self, scraper_id: str) -> None:
        """Führt den angegebenen Scraper aus und verarbeitet das Ergebnis.

        Ablauf:
            - Ruft für jede URL im Scraper die HTML-Seite ab.
            - Parst den Seiteninhalt zu strukturierten Daten.
            - Fügt alle Ergebnisse in einer Liste zusammen.
            - Übergibt die Daten zur Speicherung an den Result-Handler.
        """

        scraper = self.__scrapers.get(scraper_id)
        if not scraper:
            self.__logger.error(f"Scraper '{scraper_id}' nicht gefunden.")
            return
        urls = scraper.scraper_urls
        all_data = []
        for url in urls:
            self.__logger.info(f"Verarbeite URL: {url}")
            try:
                html = scraper.fetch_page(url, retry_count = 3, retry_delay = 5)
                data = scraper.parse_data(html)
                all_data.extend(data)
            except Exception as e:
                self.__logger.error(f"Fehler bei Scraper '{scraper_id}' für URL '{url}': {e}")
        self.__result_handler.write_to_json(all_data, scraper_id)
        self.__logger.info(f"Scraper '{scraper_id}' erfolgreich abgeschlossen.")

    def run_all(self, urls: list[str]) -> None:
        """Führt alle registrierten Scraper sequenziell aus.
        """

        completed = 0
        total_scrapers = len(self.__scrapers)
        for scraper_id in self.__scrapers:
            self.__logger.info(f"Starte Scraper '{scraper_id}'...")
            try:
                self.run_scraper(scraper_id)
                completed += 1
            except Exception as e:
                self.__logger.error(f"Fehler bei '{scraper_id}': {e}")
        self.__logger.info(f"{completed} von {total_scrapers} Scrapern erfolgreich abgeschlossen.")
