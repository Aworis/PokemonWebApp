import xml.etree.ElementTree as ET
import logging
import re
import requests

from bs4 import BeautifulSoup

from utils.log_config import setup_logging
from scraper.src.config_loader import load_sitemap_url
from scraper.src.utils.scraper_utils import extract_matching_urls, fetch_url_content
from scraper.src.utils.file_io import write_json, load_json_data

#TODO Logging funktioniert hier nicht. Muss ich noch einmal komplett richtig machen. Best Practices?
setup_logging()
logging.info("Logging erfolgreich eingerichtet!")


#Todo: Sessions implementieren

# Die URL extrahieren, wenn "typ" = "typen"
SITEMAP_URL = load_sitemap_url("typen")
if SITEMAP_URL:
    logging.info(f"Sitemap wurde erfolgreich geladen: {SITEMAP_URL}")
else:
    logging.warning("Sitemap konnte nicht geladen werden.")

# Sitemap abrufen
parsed_sitemap = ET.fromstring(fetch_url_content(SITEMAP_URL))
if parsed_sitemap:
    logging.info("XML-Dokument wurde erfolgreich geparst.")

# Gefilterte URLs extrahieren
pattern = re.compile(r"typendex/[\w-]+\.php$")
urls = extract_matching_urls(parsed_sitemap, pattern)
if urls:
    logging.info(f"{len(urls)} URLs aus Sitemap extrahiert.")
else:
    logging.warning("Keine URLs in der Sitemap gefunden.")



# hole daten aus json oder initialisiere json
pokemon_type_data = []


session = requests.Session()


# Daten sammeln. Speziell, je nach Scraper
for url in urls:
    logging.info(f"Scraping {url} gestartet...")

    content = session.get(url).text
    if not content:
        logging.error(f"Fehler: Kein Content für {url} erhalten.")
        continue  # Überspringe diese URL

    soup = BeautifulSoup(content, "html.parser")

    # Name des Typen in <h1>
    name_tag = soup.find("h1")
    name = name_tag.text.strip() if name_tag else "Unbekannt"

    # Beschreibung des Typs in allen <p> zwischen <h1> und <h3>
    start_tag = soup.find("h1")
    paragraphs = []
    current = start_tag.find_next_sibling()

    while current and current.name != "h3":
        if current.name == "p":
            paragraphs.append(current.text)
        current = current.find_next_sibling()

    description = "\\n".join(paragraphs) if paragraphs else "Keine Beschreibung gefunden"

    # **Vorlage aus typ.json laden**
    template = load_json_data("../data/data_templates/typ.json")[0]

    template.update({"name": name,
                     "beschreibung": description})

    #Generator erzeugen?
    # Daten zur Liste hinzufügen
    pokemon_type_data.append(template)

    logging.info(f"Scraping {url} abgeschlossen.")



write_json("../data/output/pokemon_typen.json", pokemon_type_data)

logging.info("Scraping abgeschlossen! Daten wurden in data/pokemon_typen.json gespeichert und erweitert.")
