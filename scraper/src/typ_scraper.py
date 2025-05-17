import xml.etree.ElementTree as ET
import logging

from bs4 import BeautifulSoup

from scraper.src.config_loader import load_sitemap_url
from scraper.src.utils.scraper_utils import extract_matching_urls, fetch_url_content
from scraper.src.utils.file_io import write_json, load_json_data


#Todo: Sessions implementieren
#TODO: Logging implementieren

# Die URL extrahieren, wenn "typ" = "typen"
SITEMAP_URL = load_sitemap_url("typen")
if SITEMAP_URL:
    logging.info(f"Sitemap wurde erfolgreich geladen: {SITEMAP_URL}")

# Sitemap abrufen
parsed_sitemap = ET.fromstring(fetch_url_content(SITEMAP_URL))
if parsed_sitemap:
    logging.info("XML-Dokument wurde erfolgreich geparst.")

# Gefilterte URLs extrahieren
urls = extract_matching_urls(parsed_sitemap, r"typendex/[\w-]+\.php$")
if urls:
    logging.info(f"{len(urls)} URLs aus Sitemap extrahiert.")



# hole daten aus json oder initialisiere json
existing_data = load_json_data("../data/output/pokemon_typen.json") or []

# Daten sammeln. Speziell, je nach Scraper
for url in urls:
    print(f"Scrape: {url}")

    #TODO: content könnte NUll sein. Exception Handling implementieren.
    content = fetch_url_content(url)
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
    existing_data.append(template)

write_json("../data/output/pokemon_typen.json", existing_data)

print("Scraping abgeschlossen! Daten wurden in data/pokemon_typen.json gespeichert und erweitert.")
