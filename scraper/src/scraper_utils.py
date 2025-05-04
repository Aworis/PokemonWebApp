import requests
import xml.etree.ElementTree as ET
import re
#TODO: Datei umbenennen in web_scraper_helpers.py, weil Hilfsfunktionen?

#TODO: Exception Handling, try-except für requests.get(url) implementieren
#def fetch_url_content(url: str) -> str:
#    """Ruft den Inhalt einer Webseite ab und behandelt mögliche Fehler."""
#    try:
#        response = requests.get(url, timeout=10)
#        response.raise_for_status()
#        return response.content.decode("utf-8")
#    except requests.exceptions.RequestException as e:
#        print(f"Fehler beim Abrufen der URL {url}: {e}")
#        return ""

def fetch_url_content(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode("utf-8")

#TODO: Warnung ausgeben, wenn urls leer ist?
def extract_matching_urls(xml_root: ET.Element, pattern: str) -> list:
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    compiled_pattern = re.compile(pattern)
    urls = [elem.text for elem in xml_root.findall(f".//{namespace}loc")]
    return [url for url in urls if compiled_pattern.search(url)]
