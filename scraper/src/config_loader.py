import json


def load_sitemap_url(typ_name: str) -> str | None:
    with open("../config/urls.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return next((entry["url"] for entry in data["sitemaps"] if entry["typ"] == typ_name), None)
