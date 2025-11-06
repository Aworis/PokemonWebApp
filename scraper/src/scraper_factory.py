import logging

from requests import Session

from attacken_scraper import AttackenScraper
from scraper.src.abstract_web_scraper import WebScraper
from typ_scraper import TypScraper

logger = logging.getLogger(__name__)

SCRAPER_MAP = {
    "typendex": TypScraper,
    "attackendex": AttackenScraper,
}


class ScraperFactory:
    @staticmethod
    def create_scraper(scraper_type: str, session: Session, urls: list[str]) -> WebScraper:
        """
        Erzeugt eine Scraper-Instanz basierend auf dem angegebenen Typ.

        :param scraper_type: Schlüsselwort für den gewünschten Scraper-Typ
        :param session: HTTP-Session für Anfragen
        :param urls: Liste von URLs, die verarbeitet werden sollen
        :return: Instanz eines spezialisierten WebScraper
        :raises ValueError: Wenn der Scraper-Typ unbekannt ist
        """

        scraper_class = SCRAPER_MAP.get(scraper_type)
        if scraper_class:
            scraper = scraper_class(session, urls)
            logger.info(f"Scraper '{scraper_type}' erfolgreich erzeugt.")
            return scraper

        message = (f"Unbekannter Scraper-Typ '{scraper_type}'. "
                   "Kein Scraper erzeugt. Bitte überprüfe die Konfiguration.")
        logger.warning(message)
        raise ValueError(message)