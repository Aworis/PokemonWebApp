
import logging
import re
import xml.etree.ElementTree as ET

import requests

logger = logging.getLogger(__name__)

def fetch_url_content(url: str, session: requests.Session) -> str | None:
    """
    Lädt den Inhalt einer URL und gibt ihn als UTF-8-dekodierten String zurück.
    """

    logger.info(f"HTTP-GET gestartet für {url}")
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        #Für bisafans.de genügt UTF-8. Automatische Encoding-Erkennung nicht nötig.
        response.encoding = "utf-8"
        logger.info(f"HTTP-GET erfolgreich ({response.status_code}) für {url}")
        return response.text

    except requests.exceptions.Timeout:
        logger.error(f"Timeout-Fehler: Server hat nicht innerhalb von 10 Sekunden auf {url} geantwortet.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP-Fehler {e.response.status_code} beim Abrufen von {url}: {e}")
    except requests.exceptions.ConnectionError:
        logger.error(f"Verbindungsfehler: Keine Verbindung zu {url} möglich.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Unerwarteter Fehler beim Abrufen von {url}: {e}")

    return None


def extract_matching_urls(xml_root: ET.Element, compiled_pattern: re.Pattern) -> list:
    """
    Extrahiert URLs aus einer XML-Sitemap, die auf das gegebene Muster passen.
    Gibt eine leere Liste zurück, wenn keine passenden URLs gefunden werden
    oder ein Fehler auftritt.
    """

    try:
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

        urls = [elem.text for elem in xml_root.findall(f".//{namespace}loc") if elem.text]
        matching_urls = [url for url in urls if compiled_pattern.search(url)]

        logger.info(f"{len(matching_urls)} passende URLs gefunden.")
        return matching_urls

    except ET.ParseError as e:
        logger.error(f"Ungültiges XML-Format: {e}")
    except TypeError as e:
        logger.error(f"Falscher Eingabetyp übergeben: {e}")
    except Exception as e:
        logger.exception(f"Unerwarteter Fehler beim Extrahieren von URLs: {e}")

    return []
