import requests

class ScraperManager:
    """
    Repräsentiert eine Singleton-Instanz zur zentralen Verwaltung von Web-Scrapern.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.scrapers = []
            self.session = requests.Session()

    def add_scraper(self, scraper, url):
        scraper = scraper(url, session=self.session)
        self.scrapers.append(scraper)

    def run(self):
        for scraper in self.scrapers:
            scraper.fetch_page(scraper.session)
            data = scraper.parse_data()
            print(data)
            scraper.run()
