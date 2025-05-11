import logging
import re
import xml.etree.ElementTree as ET

import requests


def fetch_url_content(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content.decode("utf-8")

    except requests.exceptions.Timeout:
        logging.error(f"Timeout-Fehler: Server hat nicht innerhalb von 10 Sekunden auf {url} geantwortet.")
        return None

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP-Fehler {response.status_code} beim Abrufen von {url}: {e}")
        return None

    except requests.exceptions.ConnectionError:
        logging.error(f"Verbindungsfehler: Keine Verbindung zu {url} möglich.")
        return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim Abrufen von {url}: {e}")
        return None


def extract_matching_urls(xml_root: ET.Element, pattern: str) -> set | None:
    try:
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        compiled_pattern = re.compile(pattern)

        urls = {elem.text for elem in xml_root.findall(f".//{namespace}loc") if elem.text}
        return {url for url in urls if compiled_pattern.search(url)}

    except AttributeError as e:
        logging.error(f"Fehlerhafte XML-Struktur in 'xml_root': {e}")
        return set()

    except Exception as e:
        logging.error(f"Unerwarteter Fehler beim Extrahieren von URLs: {e}")
        return set()