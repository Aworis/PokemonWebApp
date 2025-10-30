import yaml
import logging
from pathlib import Path

class ConfigLoader:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def load_sitemap_urls(self, path: str = "../config/sitemaps.yaml") -> dict[str, str] | None:
        """
        Lädt alle Sitemap-URLs aus der angegebenen YAML-Datei.
        Die Datei muss ein Dictionary enthalten, das die Sitemaps wie folgt beschreibt:

        sitemaps:
          typen: https://example.com/sitemap_typen.xml
          news: https://example.com/sitemap_news.xml
        """

        file = Path(path)
        if not file.exists():
            self.__logger.error(f"Konfigurationsdatei nicht gefunden: {path}")
            return None

        try:
            with file.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                sitemaps = config.get("sitemaps", {})
                if not isinstance(sitemaps, dict):
                    self.__logger.error(f"Ungültige Struktur in {path}: 'sitemaps' muss ein Dictionary sein.")
                    return None
                self.__logger.info(f"{len(sitemaps)} Sitemap-URLs erfolgreich geladen aus '{path}'")
                return sitemaps
        except yaml.YAMLError as e:
            self.__logger.error(f"Fehler beim Einlesen der YAML-Datei {path}: {e}")
            return None