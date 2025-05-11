import os
import json


def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


#TODO: Statt prints nutzen, Logging implementieren. Außerdem jsonlines nutzen und Path statt ao.path?
#import jsonlines
#def fetch_json_data(path: str) -> list:
#    data = []
#    try:
#        with jsonlines.open(path) as reader:
#            for obj in reader:
#                data.append(obj)
#    except FileNotFoundError:
#        logging.info("Datei %s existiert nicht.", path)
#    return data

#from pathlib import Path
#def fetch_json_data(path: str) -> list:
#    file_path = Path(path)
#    if file_path.exists():
#        with file_path.open("r", encoding="utf-8") as file:
#            try:
#                data = json.load(file)
#                return data if isinstance(data, list) else [data]
#            except json.JSONDecodeError:
#                logging.warning("Fehlerhaftes JSON in %s.", path)
#    logging.info("Datei %s existiert nicht.", path)
#    return []

def load_json_data(path: str) -> list:
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
