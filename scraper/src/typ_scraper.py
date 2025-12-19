import logging

from bs4 import BeautifulSoup

from abstract_web_scraper import WebScraper

logger = logging.getLogger(__name__)

class TypScraper(WebScraper):

    def _extract_data(self, block: BeautifulSoup) -> list[dict]:
        """
        Extrahiert die relevanten Daten eines Pokémon-Typs aus dem übergebenen
        HTML-Dokument.

        Enthaltene Daten:
            - name: Text des ersten <h1>-Elements (Name des Typs).
            - beschreibung: Text des ersten <p>-Elements.

        Typen-Interaktionen:
            - ineffektiv: Offensive des Typs verursacht keinerlei Schaden gegen Typ B.
            - immun: Der Typ ist vollständig immun gegen Angriffe von Typ B.
            - benachteiligt: Offensive des Typs verursacht reduzierten Schaden gegen Typ B.
            - resistent: Defensive des Typs erleidet reduzierten Schaden durch Typ B.
            - effektiv: Offensive des Typs verursacht erhöhten Schaden gegen Typ B.
            - anfaellig: Defensive des Typs erleidet erhöhten Schaden durch Typ B.
        """

        block = block.select_one(".well")
        if not block:
            return []

        typ_effektivitaeten = self._extract_typ_effektivitaeten(block)

        data = {
            "name": block.select_one("h1").get_text(strip=True),
            "beschreibung": block.select_one("p").get_text(),
            "ineffektiv": typ_effektivitaeten.get("offensiv").get("Wirkungslos gegen", None),
            "immun": typ_effektivitaeten.get("defensiv", None).get("Immun gegen", None),
            "benachteiligt": typ_effektivitaeten.get("offensiv").get("Schwach gegen", None),
            "resistent": typ_effektivitaeten.get("defensiv").get("Resistent gegen", None),
            "effektiv": typ_effektivitaeten.get("offensiv").get("Stark gegen", None),
            "anfaellig": typ_effektivitaeten.get("defensiv").get("Schwach gegen", None)
        }
        return [data]

    def _extract_typ_effektivitaeten(self, block: BeautifulSoup) -> dict[str, dict[str, list[str]]]:
        """
        Extrahiert offensive und defensive Effektivitäten eines Pokémon-Typs.
        Gibt ein Dict der Form zurück:
        {
            "offensiv": {...},
            "defensiv": {...}
        }
        """

        # Typname aus <h1>
        typ_name = block.select_one("h1").get_text(strip=True)

        # Effektivitäten-Container finden
        h3 = block.find("h3", string="Effektivitäten")
        if not h3:
            return {"offensiv": {}, "defensiv": {}}

        effektivitaeten_body = h3.find_next_sibling("div")

        # Offensive & Defensive extrahieren
        offensive_result = self._extract_panel(effektivitaeten_body, f"{typ_name} in der Offensive")
        defensive_result = self._extract_panel(effektivitaeten_body, f"{typ_name} in der Defensive")

        return {
            "offensiv": offensive_result,
            "defensiv": defensive_result
        }

    def _extract_panel(self, effektivitaeten_div: BeautifulSoup, text_part: str) -> dict[str, list[str]]:
        """Hilfsfunktion: Effektivitäten_div finden, Body extrahieren, Effektivitäten parsen."""
        panel_heading = effektivitaeten_div.find("div", class_="panel-heading", text=lambda t: t and text_part in t.strip())
        panel_body = panel_heading.find_next_sibling("div", class_="panel-body")
        return self._extract_effektivitaeten(panel_body)

    def _extract_effektivitaeten(self, panel_body: BeautifulSoup) -> dict[str, list[str]]:
        """
        Extrahiert aus einem Effektivitäten-Panel alle Kategorien und deren Typen.
        Beispiel:
        {
            "Wirkungslos gegen": ["Flug"],
            "Schwach gegen": ["Pflanze", "Kaefer"],
            ...
        }
        """

        result = {}

        # Alle dt-Tags durchgehen (z. B. "Wirkungslos gegen", "Schwach gegen", ...)
        for dt in panel_body.find_all("dt"):
            category = dt.get_text(strip=True)

            # Das zugehörige dd finden
            dd = dt.find_next_sibling("dd")
            if not dd:
                continue

            #Alle Typen aus den img-alt-Attributen extrahieren
            typen = [img["alt"] for img in dd.find_all("img") if img.has_attr("alt")]
            result[category] = typen

        return result