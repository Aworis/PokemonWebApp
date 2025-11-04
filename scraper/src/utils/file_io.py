import logging
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def store_scraper_output_to_json(data, scraper_id: str):
    output_dir = Path("../data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{scraper_id}_output.json"

    # Daten laden
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
    else:
        existing_data = []

    # Daten anhängen
    combined_data = existing_data + data

    # schreiben
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
