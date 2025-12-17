import logging

from bs4 import BeautifulSoup

from abstract_web_scraper import WebScraper

logger = logging.getLogger(__name__)

class PokemonScraper(WebScraper):
    """
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

        data = {
            "id": pokemon_id,
            "profilbild_id": pokemon_id,
            "name": pokemon_name,
            "beschreibung": self._extract_beschreibung(block),
            "groesse": pokemon_attributes.get("Größe", ""),
            "gewicht": pokemon_attributes.get("Gewicht", "")
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
        Das Ergebnis enthält alle Attribute der Pokemon wie
        Typ, Größe, Gewicht usw.
        """

        eigenschaften_body = block.find("div", class_="panel-heading", string="Eigenschaften").find_next_sibling()
        soup = BeautifulSoup(str(eigenschaften_body), "lxml")
        result = {}

        for dt in soup.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if dd:
                key = dt.get_text(strip=True)
                value = dd.get_text(strip=True)
                result[key] = value

        return result