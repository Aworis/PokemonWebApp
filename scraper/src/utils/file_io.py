import json
import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO)

def write_json(path: str, data) -> None:
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info(f"JSON-Datei erfolgreich geschrieben: {path}")
    except OSError as e:
        logger.error(f"Fehler beim Schreiben der Datei {path}: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Fehler beim Serialisieren der Daten: {e}")


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