import json
import logging
from pathlib import Path


def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_json_data(path: str) -> list | None:
    file_path = Path(path)
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return data if isinstance(data, list) else [data]
            except json.JSONDecodeError:
                logging.warning("Fehlerhaftes JSON in %s.", path)
                return None
    logging.info("Die Datei '%s' wurde nicht gefunden.", path)
    return None