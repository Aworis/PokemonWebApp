# Anleitung: `main`-Branch auf Commit `d64ce08` zurücksetzen

## Ziel

Den `main`-Branch exakt auf den Commit

```
d64ce08b7b1b0296b41f416b73d1eb84d335be62
```

zurücksetzen, sodass alle nachfolgenden Commits aus der Branch-History entfernt werden.

---

## Betroffene Commits (werden entfernt)

Die folgenden Commits befinden sich aktuell **nach** dem Ziel-Commit in `main` und werden durch den Reset entfernt:

| SHA       | Nachricht                                                                |
|-----------|--------------------------------------------------------------------------|
| `7861830` | Merge pull request #3 from Aworis/revert-2-copilot/list-branches-and-count |
| `6a2ed51` | Revert "List branch count and default branch for Aworis/PokemonWebApp"  |
| `3094168` | Merge pull request #2 from Aworis/copilot/list-branches-and-count       |
| `d2f44ab` | Initial plan                                                             |
| `e0b5533` | Merge pull request #1 from Aworis/copilot/add-pdf-export-feature-open-orders |
| `5527a0b` | Add Hausbote dashboard with PDF export feature                           |
| `0af4569` | Initial plan                                                             |

---

## Auswirkungen (History Rewrite)

> ⚠️ **Achtung:** Dies ist ein destruktiver Eingriff in die Git-Geschichte.
>
> - Alle oben aufgeführten Commits werden aus der öffentlichen History von `main` **dauerhaft entfernt**.
> - Jeder, der den aktuellen `main`-Stand lokal geclont oder gepullt hat, muss seinen lokalen Branch manuell zurücksetzen (siehe Abschnitt „Für Mitwirkende").
> - PRs und Branches, die auf diese Commits referenzieren, werden **verwaist** (dangling).

---

## Vorgehensweise

### Option A – Direkter Force-Push (empfohlen, falls kein Branch-Schutz aktiv)

```bash
# 1. Aktuellen Stand holen
git fetch origin

# 2. main lokal auf den Ziel-Commit zurücksetzen
git checkout main
git reset --hard d64ce08b7b1b0296b41f416b73d1eb84d335be62

# 3. Force-Push mit Sicherheitscheck
#    (--force-with-lease verhindert das Überschreiben falls jemand
#     in der Zwischenzeit gepusht hat)
git push --force-with-lease origin main
```

### Option B – Falls `--force-with-lease` abgelehnt wird (Branch-Schutz aktiv)

GitHub-Branch-Schutzregeln können Force-Pushes blockieren. In diesem Fall gibt es zwei Alternativen:

#### B1: Branch-Schutz temporär deaktivieren

1. Gehe zu **Settings → Branches → Branch protection rules** für `main`.
2. Bearbeite die Regel und deaktiviere **„Require a pull request before merging"** und **„Allow force pushes"** aktivieren.
3. Führe Option A aus.
4. Schutzregel anschließend wieder aktivieren und `Allow force pushes` deaktivieren.

#### B2: Neuen Branch als Default-Branch setzen

Falls du Branch-Schutz nicht ändern kannst oder möchtest:

```bash
# 1. Neuen Branch am Ziel-Commit erstellen
git fetch origin
git checkout -b main-reset d64ce08b7b1b0296b41f416b73d1eb84d335be62
git push origin main-reset

# 2. In GitHub Settings → Branches → Default branch
#    den Default von "main" auf "main-reset" umstellen.

# 3. Alten main löschen (optional, nach Prüfung)
git push origin --delete main

# 4. main-reset in main umbenennen (optional)
git push origin main-reset:main
git push origin --delete main-reset
```

---

## Für Mitwirkende: Lokalen Branch anpassen

Alle, die `main` lokal ausgecheckt haben, müssen nach dem Force-Push folgenden Befehl ausführen:

```bash
git fetch origin
git checkout main
git reset --hard origin/main
```

> Lokale Änderungen, die auf den entfernten Commits basieren, gehen dabei verloren.  
> Bitte sichert eure Arbeit vorher mit `git stash` oder einem separaten Branch.

---

## Verifikation

Nach dem Reset sollte gelten:

```bash
git rev-parse origin/main
# Erwartete Ausgabe: d64ce08b7b1b0296b41f416b73d1eb84d335be62

git log --oneline origin/main | head -5
# Erwartete erste Zeile: d64ce08 README: Relativen Pfad zum Bild korrigiert.
```
