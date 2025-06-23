import re
import xml.etree.ElementTree as ET
import requests

from scraper.src.config_loader import load_sitemap_url
from scraper.src.utils.scraper_utils import fetch_url_content, extract_matching_urls
from utils.logging_config import setup_logging
from typ_scraper import TypScraper
from scraper_manager import ScraperManager

#TODO: logging ordner ändern auf scraping logger



setup_logging()


session = requests.Session()
SITEMAP_URL = load_sitemap_url("typen")
if SITEMAP_URL:
    print(f"Sitemap wurde erfolgreich geladen: {SITEMAP_URL}")
else:
    print("Sitemap konnte nicht geladen werden.")

try:
    parsed_sitemap = ET.fromstring(fetch_url_content(SITEMAP_URL))
    print("XML-Dokument wurde erfolgreich geparst.")
except Exception as e:
    print(f"Fehler beim Parsen der Sitemap: {e}")

pattern = re.compile(r"typendex/[\w-]+\.php$")
urls = extract_matching_urls(parsed_sitemap, pattern)
if urls:
    print(f"{len(urls)} URLs aus Sitemap extrahiert.")
else:
    print("Keine URLs in der Sitemap gefunden.")

for element in urls:
    print(element)


typ_scraper = TypScraper(session, urls)

urls2 = typ_scraper.scraper_urls

for url in urls2:
    html = typ_scraper.fetch_page(url,3,3)
    print(typ_scraper.parse_data(html))





