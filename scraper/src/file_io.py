import os
import json

def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def fetch_json_data(path: str) -> list:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return data if isinstance(data, list) else [data]
            except json.JSONDecodeError:
                print(f"Warnung: Die Datei '{path}' enthält ungültige JSON-Daten oder ist leer.")
                return []
    print(f"Info: Die Datei '{path}' existiert nicht. Es wird eine leere Liste zurückgegeben.")
    return []
