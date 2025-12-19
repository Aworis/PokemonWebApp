import logging
import os
from typing import Any

import requests
from bs4 import BeautifulSoup, PageElement

from abstract_web_scraper import WebScraper

logger = logging.getLogger(__name__)

class PokemonScraper(WebScraper):
    """
    Webscraper für Pokémon-Daten und Profilbilder.

    Dieser Scraper ruft HTML-Seiten ab, die Informationen zu Pokémon
    enthalten, und extrahiert aus dem HTML die relevanten Daten für
    den Pokédex.

    Extrahierte Daten:
        - Id → Da es die offizielle Pokémon-ID ist, sollte diese als Datenbank-Primärschlüssel dienen.
        - Profilbild-Id → Entspricht der offiziellen Pokémon-ID.
        - Profilbild
        - Name
        - Beschreibung
        - Größe
        - Gewicht
        - Fähigkeiten
        - Attacken
    """

    def _extract_data(self, soup: BeautifulSoup) -> list[dict]:
        """
        Extrahiert die relevanten Daten eines Pokémons aus dem übergebenen
        HTML-Dokument.
        """

        block = soup.select_one(".well")
        if not block:
            return []

        pokemon_dict = self._extract_name(block)
        pokemon_id, pokemon_name = next(iter(pokemon_dict.items()))
        pokemon_attributes = self._extract_pokemon_attributes(block)

        #extract images
        self._download_pokemon_image(block, pokemon_id)

        data = {
            "id": pokemon_id,
            "profilbild_id": pokemon_id,
            "name": pokemon_name,
            "beschreibung": self._extract_beschreibung(block),
            "typen": pokemon_attributes.get("Typ", ""),
            "groesse": pokemon_attributes.get("Größe", ""),
            "gewicht": pokemon_attributes.get("Gewicht", ""),
            "faehigkeiten": self._extract_pokemon_faehigkeiten(block),
            "attacken": self._extract_pokemon_attacken(block)
        }

        return [data]

    def _extract_name(self, block: BeautifulSoup) -> dict[str, str]:
        """
        Extrahiert die Pokémon-ID und den Namen aus dem ersten <h1>-Element
        innerhalb des übergebenen HTML-Blocks.

        Der Text im <h1>-Element liegt im Format "#001 Bisasam" vor.
        Die Methode entfernt das führende "#" von der ID, trennt die Zahl
        und den Namen und gibt beide als Key-Value-Paar in einem Dictionary zurück.
        """

        raw_name = block.select_one("h1").get_text(strip=True)
        name_parts = raw_name.split(maxsplit=1)
        pokemon_id = name_parts[0].lstrip("#")
        pokemon_name = name_parts[1]

        return {pokemon_id: pokemon_name}

    def _extract_beschreibung(self, block: BeautifulSoup) -> str:
            """
            Extrahiert den Text des ersten <li>-Elements innerhalb des <div id="pokedex">,
            wobei der Inhalt von <a>-Tags (label_link) übersprungen wird.
            """

            pokedex = block.find("div", id="pokedex")
            label_link = pokedex.find("li").find("a")
            return label_link.next_sibling.strip()

    def _extract_pokemon_attributes(self, block: BeautifulSoup) -> dict[str, str]:
        """
        Extrahiert alle Attribut-Paare (<dt>/<dd>) aus dem <div>-Element der "Eigenschaften"
        mit der Klasse "panel-body" innerhalb des übergebenen Blocks und legt sie in ein Dictionary ab.
        Das Ergebnis enthält alle Attribute des Pokemons wie
        Typ, Größe, Gewicht usw.
        """

        eigenschaften_body = block.find("div", class_="panel-heading", string="Eigenschaften").find_next_sibling()
        parsed_eigenschaften_body = BeautifulSoup(str(eigenschaften_body), "lxml")
        result = {}

        for dt in parsed_eigenschaften_body.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if dd:
                key = dt.get_text(strip=True)
                if key == "Typ":
                    value = self._extract_pokemon_typen(dd)
                else:
                    value = dd.get_text(strip=True)

                result[key] = value

        return result

    def _extract_pokemon_typen(self, raw_text: PageElement) -> list[str]:
        """
        Helfermethode: Extrahiert alle Pokémon-Typen aus dem PageElement, indem aus jedem <a>-Tag
        der alt-Text des enthaltenen <img>-Elements ausgelesen wird.
        """

        raw_text = str(raw_text)
        parsed_raw_text = BeautifulSoup(raw_text, "lxml")
        typen = []

        # Alle <a>-Tags im Block finden
        for a_tag in parsed_raw_text.find_all("a"):
            img = a_tag.find("img")
            if img and img.has_attr("alt"):
                typen.append(img["alt"])

        return typen


    def _extract_pokemon_faehigkeiten(self, block: BeautifulSoup) -> dict[Any, Any]:
        """
        Extrahiert alle Fähigkeiten-Paare (<dt>/<dd>) aus dem <div>-Element der "Fähigkeiten"
        mit der Klasse "panel-body" innerhalb des übergebenen Blocks und legt sie in ein Dictionary ab.
        Das Ergebnis enthält alle Fähigkeiten des Pokemons wie
        Fähigkeit 1, Fähigkeit 2, Versteckte Fähigkeit usw.
        """

        faehigkeiten_body = block.find("div", class_="panel-heading", string="Fähigkeiten").find_next_sibling()
        parsed_faehigkeiten_body = BeautifulSoup(str(faehigkeiten_body), "lxml")
        result = {}

        for dt in parsed_faehigkeiten_body.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if dd:
                key = dt.get_text(strip=True)
                value = dd.get_text(strip=True)
                if value == "Keine":
                    result[key] = None
                else:
                    result[key] = value

        return result

    def _extract_pokemon_attacken(self, block: BeautifulSoup) -> list[str]:
        """
        Extrahiert alle erlernbaren Attacken eines Pokémon aus den drei Attacken-Kategorien
        der 9. Generation „Durch Level-Up“, „Durch TMs“ und „Durch Zucht“.

        Die Methode durchsucht die jeweiligen Tabellen unterhalb der entsprechenden
        <h4>-Überschriften und extrahiert aus jeder Tabellenzeile den Attackennamen,
        sofern dieser in einem <td>-Element mit der Klasse "no-break" enthalten ist.
        Der Attackenname wird aus dem Rohtext bereinigt, indem nur die erste
        nicht-leere Zeile übernommen wird. Doppelte Einträge werden vermieden.
        """

        #Tabellen mit Attacken
        lvlup_attacken = block.find("h4", string="Durch Level-Up").find_next_sibling()
        tms_attacken = block.find("h4", string="Durch TMs").find_next_sibling()
        zucht_attacken = block.find("h4", string="Durch Zucht").find_next_sibling()

        tabellen = [lvlup_attacken, tms_attacken, zucht_attacken]
        attacken = []

        for tabelle in tabellen:
            if not tabelle:
                continue

            for row in tabelle.find_all("tr"):
                no_break_td = row.find("td", class_="no-break")

                if no_break_td:
                    raw_text = no_break_td.get_text()

                    #Bereinigung des raw_text ohne '\n' usw.
                    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
                    attacken_name = lines[0]

                    if attacken_name not in attacken:
                        attacken.append(attacken_name)

                    continue

        return attacken

    def _download_pokemon_image(self, block: BeautifulSoup, pokemon_id: str, folder: str = "../data/images"):
        """
        Lädt Pokemon-Bild herunter und speichert es
        im angegebenen Ordner unter dem Namen <pokemon_id>.png.
        """

        # Link aus dem <a>-Tag holen (Originalbild, nicht Thumbnail)
        a_tag = block.find("a", class_="thumbnail")
        if not a_tag or not a_tag.get("href"):
            return None

        image_url = a_tag["href"]

        # Bild herunterladen
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(folder, f"{pokemon_id}.png")
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return file_path

        else:
            return None
