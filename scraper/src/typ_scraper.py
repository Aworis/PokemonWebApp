import xml.etree.ElementTree as ET
import re
from abstract_web_scraper import WebScraper

import logging
from bs4 import BeautifulSoup
from config_loader import load_sitemap_url
from utils.scraper_utils import extract_matching_urls, fetch_url_content
from utils.file_io import write_json, load_json_data

logger = logging.getLogger(__name__)


class TypScraper(WebScraper):
    def parse_data(self):
        """Parst die Seite und extrahiert die relevanten Daten."""
        if not self.page_content:
            raise Exception("No page content available. Fetch the page first.")

        soup = BeautifulSoup(self.page_content, 'html.parser')

        # Beispiel: Extrahieren von Titeln und Links
        titles = soup.find_all('h2', class_='article-title')  # Angenommene Struktur
        data = []
        for title in titles:
            data.append(title.get_text())

        return data

# Funktion zum Abrufen der Seite mit verbesserter Fehlerbehandlung und Retry-Mechanismus
# hier die methode fetch_page implementieren von abstract_web_scaper.py

# Extrahiert die Daten für den Pokemon-Typ
def extract_type_data(soup):
    # Name des Typs in <h1>
    name_tag = soup.find("h1")
    name = name_tag.text.strip() if name_tag else "Unbekannt"

    # Beschreibung des Typs in allen <p> zwischen <h1> und <h3>
    paragraphs = []
    current = name_tag.find_next_sibling()

    while current and current.name != "h3":
        if current.name == "p":
            paragraphs.append(current.text)
        current = current.find_next_sibling()

    description = "\\n".join(paragraphs) if paragraphs else "Keine Beschreibung gefunden"
    return name, description

# Hauptfunktion
def run():
    logger.info("Logging erfolgreich eingerichtet!")

    # Die URL extrahieren, wenn "typ" = "typen"
    SITEMAP_URL = load_sitemap_url("typen")
    if SITEMAP_URL:
        logger.info(f"Sitemap wurde erfolgreich geladen: {SITEMAP_URL}")
    else:
        logger.warning("Sitemap konnte nicht geladen werden.")
        return

    # Sitemap abrufen und validieren
    try:
        parsed_sitemap = ET.fromstring(fetch_url_content(SITEMAP_URL))
        logger.info("XML-Dokument wurde erfolgreich geparst.")
    except Exception as e:
        logger.error(f"Fehler beim Parsen der Sitemap: {e}")
        return

    # Gefilterte URLs extrahieren
    pattern = re.compile(r"typendex/[\w-]+\.php$")
    urls = extract_matching_urls(parsed_sitemap, pattern)
    if urls:
        logger.info(f"{len(urls)} URLs aus Sitemap extrahiert.")
    else:
        logger.warning("Keine URLs in der Sitemap gefunden.")
        return

    pokemon_type_data = []

    # Session verwenden
    with requests.Session() as session:
        for idx, url in enumerate(urls, 1):
            logger.info(f"Verarbeite {idx}/{len(urls)}: {url}")
            content = fetch_page(session, url)
            if not content:
                continue

            soup = BeautifulSoup(content, "html.parser")
            name, description = extract_type_data(soup)

            # Vorlage aus typ.json laden und anpassen
            template = load_json_data("../data/data_templates/typ.json")[0]
            template.update({"name": name, "beschreibung": description})

            pokemon_type_data.append(template)
            logger.info(f"Scraping {url} abgeschlossen.")

    # Daten aus der existierenden JSON-Datei laden und erweitern
    existing_data = load_json_data("/workspaces/dev/PokemonWebApp-dev-typ-scraper/scraper/data/data_templates/typ.json") or []
    existing_data.extend(pokemon_type_data)

    # Die erweiterten Daten in die JSON-Datei schreiben
    write_json("../data/output/pokemon_typen.json", existing_data)

    logger.info("Scraping abgeschlossen! Daten wurden in data/pokemon_typen.json gespeichert und erweitert.")
