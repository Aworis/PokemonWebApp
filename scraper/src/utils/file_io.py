import logging
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def store_scraper_output(data, scraper_id: str):
    # Zielpfad definieren
    output_dir = Path("../data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{scraper_id}_output.json"

    # Bestehende Daten laden, falls Datei existiert
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
    else:
        existing_data = []

    # Neue Daten anhängen
    combined_data = existing_data + data

    # Datei (neu) schreiben
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)









def load_json_data(path: str) -> list | None:
    file_path = Path(path)
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as file:

            try:
                data = json.load(file)
                return data if isinstance(data, list) else [data]

            except json.JSONDecodeError:
                logger.warning("Fehlerhaftes JSON in %s.", path)
                return None

    logger.warning("Die Datei '%s' wurde nicht gefunden.", path)
    return None