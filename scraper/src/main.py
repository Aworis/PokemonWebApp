from config_loader import ConfigLoader
from scraper_manager import ScraperManager
from sitemap_parser import SitemapParser
from utils.logging_config import setup_logging

# TODO: logging ordner ändern auf scraping logger
setup_logging()

# Initialisierung der Komponenten
scraper_manager = ScraperManager()
session = scraper_manager.session

config_loader = ConfigLoader()
sitemaps = config_loader.load_sitemap_urls()

for key in sitemaps:
    sitemap_url = sitemaps.get(f"{key}")

    sitemap_parser = SitemapParser(sitemap_url)
    sitemap_parser.load()

    urls = sitemap_parser.get_matching_urls(rf"{key}/[\w-]+\.php$")

    #TODO: Später wieder entfernen.
    #Zum Testen: Nur die ersten paar Einträge behalten.
    urls = urls[:4]

    scraper_manager.register_scraper(key, urls)

scraper_manager.run_all()