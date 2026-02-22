# Pokémon Web-Scraper
Dieses Framework ist ein modulares und robustes System, das entwickelt wurde, um umfangreiche Daten aus
Online-Enzyklopädien (bisafans) zu extrahieren. Es ist darauf ausgelegt, instabile Web-Umgebungen zu handhaben und Daten
in einer sauberen, relationalen Struktur aufzubereiten.

---

## Architektur & Design Patterns
Das Projekt folgt modernen Software-Design-Prinzipien (**SOLID**), um maximale Wartbarkeit sicherzustellen:

* **Singleton Pattern (`ScraperManager`):** Garantiert eine systemweite Steuerung und verwaltet eine geteilte
`requests.Session`. Dies ermöglicht die Wiederverwendung von Verbindungen, was die Performance steigert und die
Serverlast reduziert.
* **Factory Method Pattern (`ScraperFactory`):** Entkoppelt die Objekterzeugung. Neue Scraper-Typen werden über
Konfigurationsschlüssel instanziiert, ohne den aufrufenden Code zu ändern.
* **Template Method Pattern (`WebScraper` ABC):** Eine abstrakte Basisklasse definiert den Workflow
(`fetch` -> `parse` -> `store`), während die spezifischen Extraktions-Details in den Subklassen
(`PokemonScraper`, `TypScraper` etc.) gekapselt sind.

---

## Technische Kern-Features
* **Intelligente Fehlerbehebung (Wartezeiten-Strategie):** Wenn ein Server Anfragen nicht verarbeiten kann oder eine
Zeitüberschreitung auftritt, bricht der Scraper nicht sofort ab. Stattdessen pausiert er zwischen den
Wiederholungsversuchen. Die Wartezeit verdoppelt sich bei jedem fehlgeschlagenen Versuch automatisch (z. B. 2s, 4s, 8s).
Dies verhindert, dass der Scraper den Server bei bestehender Überlastung durch weitere Anfragen noch stärker
beansprucht, und erhöht die Erfolgsquote bei temporären Netzwerkinstabilitäten.
* **Atomares Dateisystem-Handling:** Ergebnisse werden zunächst in temporäre Dateien geschrieben (`tempfile`) und erst
nach erfolgreichem Abschluss ersetzt. Dies verhindert Datenkorruption bei Abstürzen.
* **Dynamische URL-Discovery:** Der `SitemapParser` analysiert XML-Sitemaps via Regex, um zielgenau relevante
Unterseiten zu identifizieren.
* **Multimediales Scraping:** Automatisierter Download und Zuordnung von Profilbildern direkt während des Prozesses
(inkl. Stream-Handling für große Dateien).

---

## Projektstruktur
```text
- scraper
-- src
--- utils
---- file_io.py          # Atomares Speichermanagement (JSON)
---- logging_config.py   # Zentrales Logging (Konsole & Datei)
---- scraper_utils.py    # HTTP-Handling & XML-Extraktion
--- abstract_web_scraper.py # Basisklasse mit Retry-Logik
--- scraper_manager.py      # Zentraler Orchestrator (Singleton)
--- scraper_factory.py      # Instanziierung der Scraper-Module
--- sitemap_parser.py       # Regex-basierte URL-Extraktion
--- [Spezifische Scraper].py # Fachlogik (Pokemon, Attacken, Typen, etc.)
```

---

## Erweiterung: Einen neuen Scraper hinzufügen
Das Framework ist so konzipiert, dass neue Datentypen (z. B. "Items") in drei einfachen Schritten hinzugefügt werden
können:

1.  **Subklasse erstellen:** Erstelle eine neue Datei (z. B. `item_scraper.py`), die von `WebScraper` erbt, und
implementiere die Methode `_extract_data(self, soup)`.
2.  **Factory registrieren:** Füge die neue Klasse in der `scraper_factory.py` zur `SCRAPER_MAP` hinzu.
3.  **Konfiguration ergänzen:** Füge die entsprechende Sitemap-URL in die `sitemaps.yaml` ein.

---

## Vom Web-Inhalt zum Datenmodell:
Der Scraper bereitet Daten so vor, dass sie direkt in ein relationales Datenbanksystem überführt werden können. Ein
Beispiel ist der `TypScraper`: Anstatt nur Text zu kopieren, extrahiert er aktiv die komplexen Wechselwirkungen
zwischen den Typen und strukturiert sie in offensive und defensive Relationen. Dies ermöglicht später präzise
Datenbank-Abfragen über Typ-Vorteile und Resistenzen.