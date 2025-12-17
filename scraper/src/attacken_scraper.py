import logging

from bs4 import BeautifulSoup
from bs4.element import Tag

from abstract_web_scraper import WebScraper

logger = logging.getLogger(__name__)

class AttackenScraper(WebScraper):
    """
    Webscraper für Pokémon-Attacken.

    Dieser Scraper ruft HTML-Seiten ab, die Informationen zu Pokémon-Attacken
    enthalten, und extrahiert aus dem HTML die relevanten Daten für
    den Pokédex.

    Extrahierte Daten:
        - Name
        - Beschreibung
        - Effekt
        - Staerke
        - Genauigkeit
        - Angriffspunkte
    """

    def _extract_data(self, soup: BeautifulSoup) -> list[dict]:
        """
        Extrahiert die relevanten Daten einer Pokémon-Attacke aus dem übergebenen
        HTML-Dokument.
        """

        block = soup.select_one(".well")
        if not block:
            return []

        attacken_attributes = self._extract_attacken_attributes(block)

        data = {
            "name": self._extract_name(block),
            "beschreibung": self._extract_beschreibung(block),
            "effekt": self._extract_effekt(block),
            "staerke": attacken_attributes.get("Stärke", ""),
            "genauigkeit": attacken_attributes.get("Genauigkeit", ""),
            "angriffspunkte": attacken_attributes.get("AP", ""),
        }

        return [data]

    def _extract_name(self, block: BeautifulSoup) -> str:
        """
        Extrahiert den Text des ersten <h1>-Elements aus dem gegebenen HTML-Block.
        """

        return block.select_one("h1").get_text(strip=True)

    def _extract_beschreibung(self, block: BeautifulSoup) -> str:
        """
        Extrahiert den ersten Text nach dem ersten <h4> innerhalb des Blocks,
        der nicht in bestimmten Container-Tags (skip_tags) wie <p>, <div> oder <span> liegt.
        """

        h4 = block.find("h4")
        if not h4:
            return ""

        skip_tags = {"p", "div", "span"}

        for sibling in h4.next_siblings:
            if isinstance(sibling, str):
                text = sibling.strip()
                # Text nur zurückgeben, wenn der Parent-Tag nicht übersprungen werden soll
                if text and sibling.parent.name not in skip_tags:
                    return text

        return ""

    def _extract_effekt(self, block: BeautifulSoup) -> str:
        """
        Extrahiert den Textabschnitt nach dem ersten <h3> mit dem Titel "Effekt"
        innerhalb des übergebenen Blocks, bis zum nächsten <h3>-Element.
        Es werden ausschließlich Inhalte aus <p>-Tags berücksichtigt, die in
        Dokument-Reihenfolge zwischen diesen beiden Überschriften liegen.
        """

        effekt_h3 = block.find("h3", string="Effekt")
        if not effekt_h3:
            return ""

        stop_h3 = effekt_h3.find_next("h3")
        text = []

        for el in effekt_h3.next_elements:
            if el is stop_h3:
                break
            if isinstance(el, Tag) and el.name == "p":
                text.append(el.get_text(" ", strip=True))

        return " ".join(text)

    def _extract_attacken_attributes(self, block: BeautifulSoup) -> dict[str, str]:
        """
        Extrahiert alle Attribut-Paare (<dt>/<dd>) aus dem ersten <div>-Element
        mit der Klasse "panel-body" innerhalb des übergebenen Blocks und legt sie in ein Dictionary ab.
        Das Ergebnis enthält alle Attribute der Attacke wie
        Typ, Kategorie, Stärke usw.
        """

        allg_info_body = block.find("div", class_="panel-body")
        soup = BeautifulSoup(str(allg_info_body), "lxml")
        result = {}

        for dt in soup.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if dd:
                key = dt.get_text(strip=True)
                value = dd.get_text(strip=True)
                result[key] = value

        return result
