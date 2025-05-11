import json
import logging
from pathlib import Path
from typing import Optional


def load_sitemap_url(typ_name: str) -> Optional[str]:
    json_name = "urls.json"
    config_path = Path(__file__).parent.parent / "config" / json_name

    try:
        with config_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return next((entry["url"] for entry in data.get("sitemaps", []) if entry.get("typ") == typ_name), None)

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logging.warning(f"Fehler beim Laden der Sitemap-URL für '{typ_name}' aus {json_name}: {e}")
        return None
