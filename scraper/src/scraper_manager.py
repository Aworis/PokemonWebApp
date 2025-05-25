# Singleton Pattern
import requests
class ScraperManager:
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
            # Hier können andere Initialisierungen erfolgen, die nur einmal gemacht werden müssen.

    def add_scraper(self, scraper, url):
        scraper = scraper(url, session=self.session)
        self.scrapers.append(scraper)

    def run(self):
        for scraper in self.scrapers:
            scraper.fetch_page()
            data = scraper.parse_data()
            print(data)




#Was der ScraperManager macht, muss ich noch gucken.