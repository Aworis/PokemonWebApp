import re
import requests
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup

from scraper.src.config_loader import load_sitemap_url
from scraper.src.file_io import write_json, fetch_json_data
from scraper.src.scraper_utils import fetch_sitemap_xml, extract_matching_urls

# Die URL extrahieren, wenn "typ" = "typen"
SITEMAP_URL = load_sitemap_url("typen")

# Überprüfung der extrahierten URL
if SITEMAP_URL:
    print(f"Sitemap-URL gefunden: {SITEMAP_URL}")
else:
    print("Keine passende Sitemap-URL gefunden.")
    exit()

# Sitemap abrufen
root = fetch_sitemap_xml(SITEMAP_URL)




# Gefilterte URLs extrahieren
urls = extract_matching_urls(root, r"typendex/[\w-]+\.php$")






# hole daten aus json oder initialisiere json
existing_data = fetch_json_data("../data/output/pokemon_typen.json")




# Daten sammeln
for url in urls:
    print(f"Scrape: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen von {url}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # Name des Typs extrahieren
    name_tag = soup.find("h1")  # Annahme: Name steht in <h1>
    name = name_tag.text.strip() if name_tag else "Unbekannt"

    # Beschreibung des Typs extrahieren
    start_header = soup.find("h1")

    paragraphs = []
    current = start_header.find_next_sibling()

    while current and current.name != "h3":
        if current.name == "p":
            paragraphs.append(current.text)
        current = current.find_next_sibling()

    description = "\\n".join(paragraphs) if paragraphs else "Keine Beschreibung gefunden"

    # **Vorlage aus typ.json laden**
    with open("../data/data_templates/typ.json", "r", encoding="utf-8") as f:
        template_list = json.load(f)

    template = template_list[0]  # Erstes Element der Liste verwenden

    # Daten in die Vorlage einfügen
    template["name"] = name
    template["beschreibung"] = description

    # Daten zur Liste hinzufügen
    existing_data.append(template)



write_json("../data/output/pokemon_typen.json", existing_data)


print("Scraping abgeschlossen! Daten wurden in data/pokemon_typen.json gespeichert und erweitert.")
