import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

class ConfigLoader:
    def load_sitemap_urls(self, path: str = "../config/sitemaps.yaml") -> dict[str, str]:
        """
        Lädt alle Sitemap-URLs aus YAML-Konfigurationsdatei.
        Gibt ein Dictionary zurück, selbst wenn Fehler auftreten.

        Die Datei muss ein Dictionary enthalten, das die Sitemaps wie folgt beschreibt:

        sitemaps:
          typen: https://example.com/sitemap_typen.xml
          news: https://example.com/sitemap_news.xml

        :param path: Pfad zur YAML-Datei
        :return: Dictionary mit Sitemap-Namen und URLs oder 'None' bei Fehler.
        """

        file = Path(path)
        if not file.exists():
            logger.error(f"Konfigurationsdatei nicht gefunden: {file}")
            return {}

        logger.info(f"Lade Sitemap-URLs aus '{file}'")

        try:
            with file.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                sitemaps = config.get("sitemaps", {})

                if not isinstance(sitemaps, dict):
                    logger.error(f"Ungültige Struktur in {file}: 'sitemaps' muss ein Dictionary sein.")
                    return {}

                logger.info(f"{len(sitemaps)} Sitemap-URLs erfolgreich geladen aus '{file}'")
                return sitemaps

        except yaml.YAMLError as e:
            logger.error(f"Fehler beim Einlesen der YAML-Datei {file}: {e}")
            return {}
        except Exception as e:
            logger.exception(f"Unerwarteter Fehler beim Laden der Sitemap-URLs aus {file}: {e}")
            return {}