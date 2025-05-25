

# Das Logging im Einstiegspunkt
from utils.logging_config import setup_logging





###########################

import typ_scraper

def main():
    setup_logging()
    typ_scraper.run()  # deine Hauptfunktion im Modul

if __name__ == "__main__":
    main()



########################test
if __name__ == "__main__":
    # URLs der Seiten, die gescraped werden sollen
    urls = [
        'https://beispielseite1.com',
        'https://beispielseite2.com'
    ]

    scraper_manager = ScraperManager()

    # Hinzufügen der Scraper zu dem Manager
    scraper_manager.add_scraper(TypScraper(urls[0]))
    scraper_manager.add_scraper(AndereSeiteScraper(urls[1]))

    # Ausführen der Scraper
    scraper_manager.run()