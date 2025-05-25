import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import logging
import time

logger = logging.getLogger(__name__)

class WebScraper(ABC):
    #TODO: Instanzvariablen anpassen. Welche brauche ich?
    def __init__(self, url, session):
        self.url = url
        self.page_content = None
        self.session = session



        #TODO hier weitermachen.
    def fetch_page(self, session, retries=3, delay=5):
        """Lädt den Inhalt der Seite über eine Session herunter."""
        try:
            response = session.get(self.url, timeout=10)
            response.raise_for_status()
            self.page_content = response.text
        except requests.RequestException as e:
            if retries > 0:
                logger.warning(f"Fehler beim Abrufen von {self.url}. Versuche es erneut in {delay} Sekunden...")
                time.sleep(delay)
                return self.url.fetch_page(self, session, retries-1, delay)
            logger.error(f"Fehler beim Abrufen von {self.url}: {e}")
            return None

    @abstractmethod
    def parse_data(self):
        """Abstrakte Methode zum Extrahieren von Daten. Muss in Unterklassen implementiert werden."""
        pass