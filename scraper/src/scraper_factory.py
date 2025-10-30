from typ_scraper import TypScraper
from requests import Session

class ScraperFactory:
    @staticmethod
    def create_scraper(scraper_type: str, session: Session, urls: list[str]):
        if scraper_type == "typendex":
            return TypScraper(session, urls)
        else:
            #raise ValueError(f"Unknown scraper type: {scraper_type}")
            return
