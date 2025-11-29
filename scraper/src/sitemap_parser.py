import logging
import re
import xml.etree.ElementTree as ET

from utils.scraper_utils import fetch_url_content, extract_matching_urls

logger = logging.getLogger(__name__)

class SitemapParser:
    def __init__(self, url, session):
        self.url = url
        self.xml_root = None
        self.session = session

    def load(self):
        """
        Lädt die Sitemap von der URL und parst sie als XML.
        """

        content = fetch_url_content(self.url, self.session)
        if content is None:
            logger.error(f"Sitemap konnte von {self.url} nicht abgerufen werden.")
            return False

        try:
            self.xml_root = ET.fromstring(content)
            logger.info(f"Sitemap erfolgreich geladen und geparst: {self.url}")
            return True
        except ET.ParseError as e:
            logger.error(f"XML-Parsing fehlgeschlagen für {self.url}: {e}")
            return False
        except Exception as e:
            logger.exception(f"Unerwarteter Fehler beim Laden der Sitemap {self.url}: {e}")
            return False

    def get_matching_urls(self, pattern):
        """
        Extrahiert URLs aus der Sitemap, die dem Regex-Muster entsprechen.

        :param pattern: Regulärer Ausdruck zur Filterung der URLs
        :return: Liste der passenden URLs
        """

        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Ungültiges Regex-Muster: {e}") from e

        if not self.xml_root:
            return []

        try:
            return extract_matching_urls(self.xml_root, regex)
        except Exception as e:
            # optional: spezifizieren, z. B. XML-Fehler
            raise RuntimeError(f"Fehler beim Extrahieren der URLs: {e}") from e