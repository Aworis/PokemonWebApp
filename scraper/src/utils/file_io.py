import logging
import json
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

def store_scraper_output_to_json(data, scraper_id: str):
    output_dir = Path("../data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{scraper_id}_output.json"

    logger.info(f"Speichern der Ausgabe von Scraper '{scraper_id}' wird gestartet.")
    existing_data = []

    try:
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    logger.info(f"Vorhandene Daten geladen aus: {file_path}")

            except json.JSONDecodeError:
                logger.warning(f"Vorhandenes JSON {file_path} beschädigt. Neues JSON wird erzeugt.")
                existing_data = []

        combined_data = existing_data + data

        # atomares schreiben
        with tempfile.NamedTemporaryFile("w", delete=False, dir=output_dir, encoding="utf-8") as tf:
            json.dump(combined_data, tf, ensure_ascii=False, indent=2)
            temp_name = Path(tf.name)

        temp_name.replace(file_path)
        logger.info(f"Ausgabe von Scraper '{scraper_id}' gespeichert in: {file_path}")

    except Exception:
        logger.error(f"Fehler beim Speichern der Ausgabe von Scraper '{scraper_id}'.")
        raise

