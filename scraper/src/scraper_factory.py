from scraper.src.abstract_web_scraper import WebScraper
from typ_scraper import TypScraper
from attacken_scraper import AttackenScraper
from requests import Session
import logging

logger = logging.getLogger(__name__)

class ScraperFactory:
    @staticmethod
    def create_scraper(scraper_type: str, session: Session, urls: list[str]) -> WebScraper:
        if scraper_type == "typendex":
            return TypScraper(session, urls)
        elif scraper_type == "attackendex":
            return AttackenScraper(session, urls)
        else:
            message = (f"Unbekannter Scraper-Typ '{scraper_type}'. "
                       "Kein Scraper erzeugt. Bitte überprüfe die Konfiguration.")
            logger.warning(message)
            raise ValueError(message)