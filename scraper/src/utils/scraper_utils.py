
import logging
import re
import xml.etree.ElementTree as ET

import requests

logger = logging.getLogger(__name__)

def fetch_url_content(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        #Für bisafans.de genügt UTF-8. Automatische Encoding-Erkennung nicht nötig.
        return response.content.decode("utf-8")

    except requests.exceptions.Timeout:
        logger.error(f"Timeout-Fehler: Server hat nicht innerhalb von 10 Sekunden auf {url} geantwortet.")
        return None

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP-Fehler {response.status_code} beim Abrufen von {url}: {e}")
        return None

    except requests.exceptions.ConnectionError:
        logger.error(f"Verbindungsfehler: Keine Verbindung zu {url} möglich.")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Fehler beim Abrufen von {url}: {e}")
        return None


def extract_matching_urls(xml_root: ET.Element, compiled_pattern: re.Pattern) -> list | None:
    try:
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        urls = [elem.text for elem in xml_root.findall(f".//{namespace}loc") if elem.text]

        matching_urls = [url for url in urls if compiled_pattern.search(url)]

        logger.info(f"{len(matching_urls)} passende URLs gefunden.")
        return matching_urls

    except AttributeError as e:
        logger.error(f"Fehlerhafte XML-Struktur: {e}")
        return []

    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim Extrahieren von URLs: {e}")
        return []
