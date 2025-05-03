import re
import requests
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup
import os

# JSON-Datei laden
with open("config/urls.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Die URL extrahieren, wenn "typ" = "typen"
SITEMAP_URL = next((entry["url"] for entry in data["sitemaps"] if entry["typ"] == "typen"), None)

# Überprüfung der extrahierten URL
if SITEMAP_URL:
    print(f"Sitemap-URL gefunden: {SITEMAP_URL}")
else:
    print("Keine passende Sitemap-URL gefunden.")
    exit()

# Sitemap abrufen
response = requests.get(SITEMAP_URL)
if response.status_code != 200:
    print("Fehler beim Abrufen der Sitemap")
    exit()

# XML parsen
root = ET.fromstring(response.content)
namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

# Typenseiten extrahieren
urls = [elem.text for elem in root.findall(f".//{namespace}loc")]

# Muster für URLs: müssen mit "typendex/" beginnen und mit ".php" enden
pattern = re.compile(r"typendex/[\w-]+\.php$")

# Gefilterte URLs extrahieren
urls = [url for url in urls if re.search(pattern, url)]

# Prüfen, ob die Datei bereits existiert
if os.path.exists("data/pokemon_typen.json"):
    with open("data/pokemon_typen.json", "r", encoding="utf-8") as file:
        try:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = [existing_data]
        except json.JSONDecodeError:
            existing_data = []  # Falls die Datei leer oder fehlerhaft ist
else:
    existing_data = []  # Falls die Datei noch nicht existiert

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
    with open("data_templates/typ.json", "r", encoding="utf-8") as f:
        template_list = json.load(f)

    template = template_list[0]  # Erstes Element der Liste verwenden

    # Daten in die Vorlage einfügen
    template["name"] = name
    template["beschreibung"] = description

    # Daten zur Liste hinzufügen
    existing_data.append(template)

# Daten als JSON speichern
with open("data/pokemon_typen.json", "w", encoding="utf-8") as file:
    json.dump(existing_data, file, ensure_ascii=False, indent=4)

print("Scraping abgeschlossen! Daten wurden in data/pokemon_typen.json gespeichert und erweitert.")