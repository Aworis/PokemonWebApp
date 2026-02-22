# PokemonWebApp

Ein modulares Full-Stack-Projekt zur Erstellung eines umfassenden digitalen Pokémon-Lexikons (Pokedex). Dieses Repository dient als Showcase für die Integration verschiedener Technologien – von automatisiertem Web-Scraping über relationales Datenbankdesign bis hin zur modernen Web-Visualisierung.

---

## Projekt-Vision & Zielsetzung
Das Ziel ist die Entwicklung einer performanten Web-Applikation, die Pokémon-Daten aggregiert, strukturiert speichert und über eine REST-API zugänglich macht.

* **Fokus:** Saubere Software-Architektur, Modularität und der Einsatz eines modernen Tech-Stacks.
* **Lernziel:** Beherrschung des gesamten Daten-Lebenszyklus – von der Rohdatenquelle bis zum User-Interface.
* **Motivation:** Eigenständige Weiterbildung in den Bereichen OOP, RDBMS und Full-Stack-Integration.

## System-Architektur & Status
Das Projekt ist in logische Teilmodule unterteilt, um eine klare Trennung zu gewährleisten.

| Modul                                  | Status    | Beschreibung | Tech-Stack            |
|:---------------------------------------|:----------| :--- |:----------------------|
| **[Web-Scraper](./scraper/README.md)** | In Arbeit | Objektorientierter Scraper zur Datengewinnung. | Python, BeautifulSoup |
| **[Datenbankmodell](./database/README.md)**     | In Arbeit | Relationales Datenmodell für Stats, Typen etc. | MySQL                 |
| **Backend-API**                        | Geplant   | RESTful Service zur Bereitstellung der Daten. | Java, Spring Boot     |
| **Frontend**                           | Geplant | Dynamisches Interface mit Suchfunktion. | React                 |

## Aktueller Entwicklungsstand
Momentan liegt der Fokus auf der Datenerfassung:

> **Warum ein eigener Scraper?** Bestehende öffentliche Schnittstellen (wie die PokéAPI) bieten Daten primär in englischer Sprache an. Um ein durchgängig deutschsprachiges Lexikon zu erstellen und gleichzeitig tiefe Einblicke in **Data-Engineering-Prozesse** (Web-Scraping, DOM-Parsing, Data-Cleaning) zu gewinnen, wurde eine eigene Scraping-Logik implementiert.

1.  **Datenmodellierung:** Das MySQL-Schema ist finalisiert und für komplexe Abfragen (n:m Beziehungen für Typen etc.) optimiert.
2.  **Scraping:** Der Python-Scraper ist weit fortgeschritten. Er ist modular aufgebaut und exportiert Daten aktuell in strukturierte JSON-Formate.
3.  **Nächste Meilensteine:**
    * Abschluss der Extraktion komplexer Daten...
    * Implementierung eines Data-Cleaning-Moduls zur Normalisierung...
    * Automatisierter Import der JSON-Daten in die MySQL-Datenbank...
    * Initialisierung des Spring Boot Backends...
    * Backend-Entwicklung
    * Frontend-Entwicklung
    * Deployment

## Installation & Setup
Da sich das Projekt in einer aktiven Entwicklungsphase befindet, existiert noch kein globaler Start-Befehl (z.B. via Docker). Instruktionen zur Ausführung der einzelnen Komponenten findest du in den jeweiligen Unterordnern.

> **Geplant:** Eine vollständige Containerisierung des gesamten Stacks via **Docker-Compose** für ein "One-Command-Setup".

---

## Vertiefende Dokumentation
Für technische Details zu den einzelnen Modulen besuche bitte die spezifischen Readmes:

* [**Dokumentation: Web-Scraper**](./scraper/README.md) – *Details zu OOP-Ansatz und Modulstruktur.*
* [**Dokumentation: Datenbank**](./database/README.md) –