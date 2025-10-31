from config_loader import ConfigLoader
from utils.logging_config import setup_logging
from scraper_manager import ScraperManager
from sitemap_parser import SitemapParser

# TODO: logging ordner ändern auf scraping logger
setup_logging()

# Initialisierung der Komponenten
scraper_manager = ScraperManager()
session = scraper_manager.session

config_loader = ConfigLoader()
sitemaps = config_loader.load_sitemap_urls()
sitemap_url = sitemaps.get("typendex")

sitemap_parser = SitemapParser(sitemap_url)
sitemap_parser.load()

urls = sitemap_parser.get_matching_urls(r"typendex/[\w-]+\.php$")

for key in sitemaps:
    scraper = 0
    scraper_manager.register_scraper(key, urls)


#scraper_manager.run_scraper("typendex")
scraper_manager.run_all()