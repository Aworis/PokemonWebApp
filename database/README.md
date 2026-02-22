# Datenbank-Konzeption (Entity-Relationship-Modell)

Dieses Modul beinhaltet das Datenbank-Design der PokemonWebApp. Das Schema wurde entworfen, um die komplexen Abhängigkeiten der Pokémon-Welt (Typen-Wechselwirkungen, Entwicklungsbäume, Attacken-Pools) performant und konsistent abzubilden.

## ER-Diagramm
Hier ist die visuelle Darstellung des aktuellen Entwurfs:

<p align="center">
  <img src="./docs/PokemonERModell.png" alt="Entity Relationship Modell" width="800">
</p>

### Kern-Entitäten:
* **Pokemon:** Die zentrale Entität mit Attributen wie Name, Größe, Gewicht und einer rekursiven Beziehung für die **Entwicklung**.
* **Typ:** Definiert die Elementarklassen. Die Beziehung zu Pokémon ist als **n:m** modelliert (ein Pokémon kann mehrere Typen haben).
* **Attacke:** Enthält spezifische Kampfwerte. Auch hier besteht eine **n:m** Verbindung zu den Pokémon.
* **Wechselwirkung:** Eine schwache Entität / Beziehungskonstrukt, das die Typschwächen (Effektivität) zwischen einem Angreifer- und Verteidiger-Typ abbildet.

### Besondere Modellierungs-Entscheidungen
* **Rekursive Beziehung:** Die "hat direkte Entwicklung"-Relation innerhalb der Entität *Pokemon* ermöglicht es, Evolutionsketten abzubilden, ohne redundante Tabellen zu erstellen.
* **Kardinalitäten:** Die Verwendung von n:m-Beziehungen stellt sicher, dass das Modell der tatsächlichen Spielmechanik (z.B. Dual-Typ-Pokémon) entspricht.

### 🚀 Nächster Schritt: Relationales Mapping
Der nächste Meilenstein ist die Überführung dieses konzeptionellen ER-Modells in ein **relationales Schema**:
1. Auflösung der n:m-Beziehungen in Zwischentabellen (Join Tables).
2. Definition der Primär- und Fremdschlüssel.
3. Erstellung der SQL-DDL-Skripte (`CREATE TABLE`).
---
*Hinweis: Das ER-Diagramm kann als XML-Datei im Root-Verzeichnis eingesehen werden.*