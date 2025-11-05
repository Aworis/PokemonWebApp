import utils.logging_config # noqa: F401 # Import aktiviert Logging via Seiteneffekt
import logging

from config_loader import ConfigLoader
from scraper_manager import ScraperManager
from sitemap_parser import SitemapParser

logger = logging.getLogger(__name__)

# Initialisierung der zentralen Scraper-Komponente
scraper_manager = ScraperManager()
session = scraper_manager.session

# Laden der Sitemap-Konfiguration aus YAML-Datei
config_loader = ConfigLoader()
sitemaps = config_loader.load_sitemap_urls()

# Extrahieren aller URLs aus den jeweiligen Sitemaps
for key in sitemaps:
    sitemap_url = sitemaps.get(f"{key}")

    sitemap_parser = SitemapParser(sitemap_url)
    sitemap_parser.load()

    urls = sitemap_parser.get_matching_urls(rf"{key}/[\w-]+\.php$")

    #TODO: Später wieder entfernen.
    #Zum Testen: Nur die ersten paar Einträge behalten.
    urls = urls[:4]

    scraper_manager.register_scraper(key, urls)

# Ausführung aller registrierten Scraper
scraper_manager.run_all()