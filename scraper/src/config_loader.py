import json


#TODO: Exception Handling, wenn urls.json kaputt ist
#TODO: Umbenennen in get_sitemap_url?
def load_sitemap_url(typ_name: str) -> str | None:
    with open("../config/urls.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return next((entry["url"] for entry in data["sitemaps"] if entry["typ"] == typ_name), None)
