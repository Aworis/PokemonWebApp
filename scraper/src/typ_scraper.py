import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from scraper.src.config_loader import load_sitemap_url
from scraper.src.file_io import write_json, fetch_json_data
from scraper.src.scraper_utils import extract_matching_urls, fetch_url_content

# Die URL extrahieren, wenn "typ" = "typen"
SITEMAP_URL = load_sitemap_url("typen")

#TODO: Logging implementieren
#import logging
#logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#logging.info("Sitemap-URL gefunden: %s", SITEMAP_URL)
#logging.warning("Keine passende Sitemap-URL gefunden.")

# Überprüfung der extrahierten URL
if SITEMAP_URL:
    print(f"Sitemap-URL gefunden: {SITEMAP_URL}")
else:
    print("Keine passende Sitemap-URL gefunden.")
    exit()

# Sitemap abrufen
root = ET.fromstring(fetch_url_content(SITEMAP_URL))

# Gefilterte URLs extrahieren
urls = extract_matching_urls(root, r"typendex/[\w-]+\.php$")

# hole daten aus json oder initialisiere json
existing_data = fetch_json_data("../data/output/pokemon_typen.json")

# Daten sammeln. Speziel, je nach Scraper
for url in urls:
    print(f"Scrape: {url}")
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
    template = fetch_json_data("../data/data_templates/typ.json")[0]

    template.update({"name": name,
                     "beschreibung": description})

    # Daten zur Liste hinzufügen
    existing_data.append(template)

write_json("../data/output/pokemon_typen.json", existing_data)

print("Scraping abgeschlossen! Daten wurden in data/pokemon_typen.json gespeichert und erweitert.")
