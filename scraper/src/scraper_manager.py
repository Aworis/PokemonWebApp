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

    def register_scraper(self, scraper_id: str, scraper_instance: WebScraper):
        """Registriert einen neuen Scraper unter einer eindeutigen ID.
        Wenn bereits ein Scraper mit dieser ID existiert, wird keine neue Registrierung durchgeführt.
        """

        if scraper_id in self.__scrapers:
            self.__logger.info(f"Scraper '{scraper_id}' ist bereits registriert.")
        else:
            self.__scrapers[scraper_id] = scraper_instance
            self.__logger.info(f"Scraper '{scraper_id}' registriert.")

    def run_scraper(self, scraper_id: str):
        """
        Führt den angegebenen Scraper aus und verarbeitet das Ergebnis.

        Ablauf:
            - Ruft die HTML-Seite über den konkreten Scraper ab.
            - Parst die Seite zu strukturierten Daten.
            - Übergibt die Daten zur Speicherung an den Result-Handler.
        """

        scraper = self.__scrapers.get(scraper_id)
        if not scraper:
            self.__logger.error(f"Scraper '{scraper_id}' nicht gefunden.")
            return
        try:
            html = scraper.fetch_page()
            data = scraper.parse_data(html)
            self.__result_handler.write_to_json(data, scraper_id)
            self.__logger.info(f"Scraper '{scraper_id}' erfolgreich abgeschlossen.")
        except Exception as e:
            self.__logger.error(f"Fehler beim Ausführen des Workflows für '{scraper_id}': {str(e)}")

    def run_all(self):
        """
        Führt alle registrierten Scraper sequenziell aus.
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
