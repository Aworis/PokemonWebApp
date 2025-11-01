import logging
import re
import xml.etree.ElementTree as ET

from utils.scraper_utils import fetch_url_content, extract_matching_urls


class SitemapParser:
    def __init__(self, url):
        self._logger = logging.getLogger(__name__)
        self.url = url
        self.xml_root = None

    def load(self):
        try:
            content = fetch_url_content(self.url)
            self.xml_root = ET.fromstring(content)
            return True
        except Exception as e:
            self._logger.error(f"Sitemap konnte nicht geladen werden: {e}")
            return False

    def get_matching_urls(self, pattern):
        regex = re.compile(pattern)
        return extract_matching_urls(self.xml_root, regex) if self.xml_root else []
