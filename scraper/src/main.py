import re
import xml.etree.ElementTree as ET
import requests


from config_loader import ConfigLoader


from utils.scraper_utils import fetch_url_content, extract_matching_urls
from utils.logging_config import setup_logging
from typ_scraper import TypScraper
from scraper_manager import ScraperManager
from sitemap_parser import SitemapParser

# TODO: logging ordner ändern auf scraping logger
setup_logging()

# Initialisierung der Komponenten
scraper_manager = ScraperManager()
config_loader = ConfigLoader()
session = scraper_manager.session

sitemaps = config_loader.load_sitemap_urls()
sitemap_url = sitemaps.get("typen")

sitemap_parser = SitemapParser(sitemap_url)
sitemap_parser.load()

urls = sitemap_parser.get_matching_urls(r"typendex/[\w-]+\.php$")
print(f"{len(urls)} URLs aus Sitemap extrahiert.")


# Beispiel für die Verwendung des TypScraper
typ_scraper = TypScraper(session, urls)

for url in typ_scraper.urls:
        html = typ_scraper.fetch_page(url, 3, 3)
        if html:
            data = typ_scraper.parse_data(html)
            print(data)

# TODO: Gesammelten Daten speichern und nicht printen