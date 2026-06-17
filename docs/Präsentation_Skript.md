# IHK-Prüfungspräsentation — MDWriter
## Skript & Folieninhalte

**Gesamtzeit:** 15 Minuten  
**Aufteilung:** ~8 Min PowerPoint · ~7 Min Live-Demo  
**Folienanzahl:** 8

---

## FOLIE 1 — Titel

**Überschrift:**
> MDWriter — Markdown-Dokumentation direkt in Odoo

**Unterzeile:**
> Konzeption und Entwicklung eines nativen Odoo-19-Moduls

**Weitere Infos (klein):**
- Timo Giese · Fachinformatiker Anwendungsentwicklung
- TrendTec UG · Sommerprüfung 2026

**Sprechernotiz:**
Kurz vorstellen, Projektnamen nennen, dann direkt weiter — keine Zeit verlieren.

---

## FOLIE 2 — Ausgangssituation

**Überschrift:** Das Problem

**Stichpunkte:**
- Technische Dokumentation verteilt auf: Odoo HTML-Editor, Git-Wikis, lokale Markdown-Dateien
- Kein einheitlicher Standard, keine zentrale Suche
- Odoo-Editor ungeeignet für Code-Snippets und Tabellen
- Kein Zugriffsschutz über Odoo-Berechtigungen

**Visuell:** ggf. kleines Diagramm mit drei Pfeilen von „Entwickler" zu den drei Tools — zeigt den Medienbruch

**Sprechernotiz:**
„In der Entwicklungsabteilung bei TrendTec haben wir technische Dokumentation an drei verschiedenen Stellen gepflegt — das hat zu Medienbrüchen, fehlenden Standards und erschwerter Auffindbarkeit geführt."

---

## FOLIE 3 — Projektziel

**Überschrift:** Das Ziel

**Stichpunkte:**
- Markdown-Editor direkt in Odoo — kein externes Tool
- Live-Vorschau beim Schreiben (Split-View)
- Automatische Versionierung jeder Änderung
- PDF-Export aus Odoo heraus
- Zugriffsschutz über das bestehende Odoo-Rechtesystem

**Sprechernotiz:**
„Das Ziel war: alles in Odoo — kein Wechsel zwischen Tools, keine Medienbrüche. Markdown als Format, weil es im Entwicklerteam bereits bekannt und akzeptiert ist."

---

## FOLIE 4 — Lösungsentscheidung

**Überschrift:** Make or Buy?

**Tabelle (3 Zeilen, 3 Spalten):**

| Lösung | Odoo-Integration | Kosten (3 Jahre) |
|---|---|---|
| Confluence (SaaS) | Kein nativer Zugriff | 3.240 € |
| Git-Wiki | Kein Zugriff aus Odoo | 0 € (aber kein Mehrwert) |
| **MDWriter (Eigenentwicklung)** | **Vollständig integriert** | **1.998 €** |

**Sprechernotiz:**
„Confluence wäre die naheliegende Alternative gewesen — aber externe Tools lösen das Kernproblem nicht: fehlende Integration ins ERP. Die Eigenentwicklung amortisiert sich nach ca. 18 Monaten und ist direkt in Kundenprojekten einsetzbar."

---

## FOLIE 5 — Architektur

**Überschrift:** Technischer Aufbau

**Drei Blöcke (visuell als Schichten oder Kästen):**

```
┌─────────────────────────────────────┐
│  Frontend (Browser)                 │
│  OWL-Komponente · CodeMirror        │
│  markdown-it (lokal, kein CDN)      │
├─────────────────────────────────────┤
│  Backend (Python / Odoo ORM)        │
│  Versionierung · PDF · Sicherheit   │
│  mistune · wkhtmltopdf              │
├─────────────────────────────────────┤
│  Datenschicht                       │
│  PostgreSQL · ir.attachment         │
└─────────────────────────────────────┘
```

**Stichpunkte rechts daneben:**
- Modulname: `markdown_editor`
- Keine externen Laufzeitabhängigkeiten
- Vollständig in Odoo-Konventionen (ORM, ACL, Assets)

**Sprechernotiz:**
„MDWriter folgt dem Drei-Schichten-Modell von Odoo. Alle JavaScript-Bibliotheken liegen lokal im Modul — keine externen CDN-Aufrufe, kein Internet nötig."

---

## FOLIE 6 — Kernfunktionen

**Überschrift:** Was das Modul kann

**Stichpunkte (mit Icons wenn möglich):**
- Split-View Editor — Markdown links, Live-Vorschau rechts
- Automatische Versionierung — bei jeder Inhaltsänderung, MD5-Prüfsumme
- Versionsvergleich — farbiger Diff zwischen zwei Versionen
- Restore — ältere Version wiederherstellen (selbst versioniert)
- PDF-Export — mit Metadaten-Header, Caching bei unverändertem Inhalt
- Statusverwaltung — Entwurf · Veröffentlicht · Archiviert

**Sprechernotiz:**
„Das sind die sechs Kernfunktionen — alle ursprünglich geplanten Anforderungen wurden erfüllt, plus Restore und Statusverwaltung als Erweiterung."

---

## FOLIE 7 — Sicherheit & Tests

**Überschrift:** Qualitätssicherung

**Zwei Spalten:**

**Sicherheit:**
- ACL: Benutzer können nur eigene Dokumente sehen
- Record Rules: zeilenbasierte WHERE-Klausel im SQL
- XSS-Schutz: markdown-it `html: false`, mistune ohne HTML-Ausführung

**Tests:**
- 7 automatisierte Tests (TransactionCase)
- Versionierung, ACL, Versionsvergleich
- Ergebnis: `0 failed, 0 error(s) of 7 tests`
- Abnahme durch Oliver Kölsch am 26.05.2026

**Sprechernotiz:**
„Das Sicherheitskonzept nutzt zwei Ebenen: ACLs steuern den Modellzugriff, Record Rules den Datensatzzugriff. Beides zusammen stellt sicher, dass ein Benutzer wirklich nur seine eigenen Dokumente sieht — auch wenn er die URL direkt aufruft."

---

## FOLIE 8 — Ergebnis & Fazit

**Überschrift:** Projektergebnis

**Stichpunkte:**
- Alle Pflichtanforderungen vollständig erfüllt
- 80 Stunden eingehalten — Zeitplan zu 100 % eingehalten
- Modul läuft produktiv auf Odoo.sh (Enterprise)
- Direkt einsetzbar in Kundenprojekten

**Lerneffekte (klein):**
- OWL Lifecycle: `onMounted` für DOM-abhängige Bibliotheken
- CSS-Scoping in Odoo Enterprise
- wkhtmltopdf vs. moderne Browser-CSS

**Abschlusssatz auf der Folie:**
> „MDWriter löst das Ausgangsproblem vollständig — zentrale Markdown-Dokumentation, integriert in Odoo, ohne externe Tools."

**Sprechernotiz:**
„Das Projekt hat mein Verständnis für native Odoo-Entwicklung, besonders im Frontend-Bereich mit OWL, deutlich vertieft. Das Modul ist nicht nur ein Prüfungsprojekt — es ist direkt produktiv einsetzbar."

---

---

# LIVE-DEMO — Ablaufplan

**Gesamtzeit:** ca. 6–7 Minuten  
**Vorbereitung:** Odoo im Browser geöffnet, MDWriter-App in der Homescreen-Übersicht sichtbar

---

### Schritt 1 — MDWriter öffnen (30 Sek.)
- Homescreen zeigen → MDWriter-Icon anklicken
- Listenansicht mit vorhandenen Dokumenten zeigen
- Kurz: „Hier sieht ein Benutzer nur seine eigenen Dokumente"

### Schritt 2 — Dokument öffnen & Split-View zeigen (1 Min.)
- Ein bestehendes Dokument öffnen (z. B. Demo-Dokument)
- Split-View sichtbar: Editor links, Vorschau rechts
- Einen Satz tippen → Live-Vorschau aktualisiert sich
- CodeMirror Syntax-Highlighting kurz zeigen

### Schritt 3 — Speichern & Versionierung (1 Min.)
- Kleine Änderung machen, speichern
- Tab „Versionen" öffnen → neue Version erscheint automatisch
- Versionsnummer, Zeitstempel, Prüfsumme kurz zeigen
- „Das passiert bei jeder Inhaltsänderung automatisch"

### Schritt 4 — Versionsvergleich (1 Min.)
- Zwei Versionen auswählen → Vergleich öffnen
- Grüne Hinzufügungen, rote Löschungen zeigen
- „Das ist der eingebaute Diff-Dialog"

### Schritt 5 — PDF-Export (1 Min.)
- Button „PDF exportieren" klicken
- PDF öffnet sich im Browser: Metadaten-Header, formatierter Inhalt
- „Das PDF wird beim ersten Export erzeugt und danach gecacht"

### Schritt 6 — Rechte kurz erwähnen (30 Sek.)
- Nicht lange vorführen — nur kurz sagen:
- „Als Admin sehe ich alle Dokumente aller Benutzer — normale Benutzer nur ihre eigenen. Das ist über ACLs und Record Rules gelöst."

### Schritt 7 — Abschluss (30 Sek.)
- Zurück zur Listenansicht
- „Das war MDWriter — Fragen dazu gerne im Fachgespräch"

---

## Tipps für die Demo

- **Testdokument vorbereiten** mit ausreichend Inhalt für einen sichtbaren Diff
- **Mindestens 2 Versionen vorher anlegen** damit der Versionsvergleich sofort funktioniert
- **PDF einmal vorab exportieren** damit der Browser-Download nicht hängt
- **Odoo im Vollbild** — kein Desktop-Hintergrund sichtbar
- **Nicht im Fließtext verzetteln** — kurze Sätze, zeigen statt erklären

---

---

# LIVE-DEMO — Detaillierter Ablauf (Probelauf-Skript)

> Der Spickzettel (`MDWriter_Demo_Spickzettel.pdf`) ist die Kurzkarte fürs Pult.
> Dieses Skript ist die ausführliche Version zum Üben — mit exakten Button-Beschriftungen aus dem Code.

## Setup vorher (nicht vor Publikum)

- Odoo im Vollbild (F11), Browser-Zoom so, dass Editor **und** Vorschau gleichzeitig sichtbar sind
- Testdokument mit H1-Überschrift, einer Liste, einem Codeblock (` ``` `) und einer Tabelle
- 2–3 Versionen vorab erzeugt (damit Versionsliste + Diff sofort etwas zeigen)
- 1× PDF vorab exportiert (Cache warm → Export erscheint sofort)
- Optional: zweiter Testbenutzer angelegt, falls du die Rechte vorführen statt nur erwähnen willst

## Ablauf (ca. 5:30 Min)

### 0:00–0:30 · Öffnen
- **Tun:** Homescreen → App „Markdown" → Listenansicht
- **Zeigen:** Spalten Titel, Eigentümer (Avatar), Status-Badge, Aktuelle Version
- **Sagen:** „Das ist MDWriter. Jeder Benutzer sieht hier nur seine eigenen Dokumente — dazu gleich bei der Sicherheit mehr."

### 0:30–1:30 · Split-View + Live-Vorschau
- **Tun:** Testdokument öffnen, eine Zeile tippen, z. B. `## Demo IHK`
- **Zeigen:** links CodeMirror mit Syntax-Highlighting, rechts gerenderte Vorschau, die sich nach kurzer Verzögerung aktualisiert
- **Sagen:** „Markdown links, Live-Vorschau rechts. Editor ist CodeMirror, die Vorschau rendert markdown-it. Die kleine Verzögerung ist ein bewusster Debounce — erst 300 ms nach dem letzten Tastendruck wird neu gerendert, damit schnelles Tippen flüssig bleibt."

### 1:30–2:30 · Speichern + automatische Version
- **Tun:** Speichern → Tab „Versionen"
- **Zeigen:** neue Zeile — Version, Geändert von, Geändert am, Checksumme, Markdown-Anhang, PDF-Anhang
- **Sagen:** „Beim Speichern entsteht automatisch eine neue Version: Nummer, Zeit, Bearbeiter, MD5-Prüfsumme. Die Prüfsumme ist ein Fingerabdruck des Inhalts, um Änderungen zwischen Versionen zu erkennen. Alte Versionen werden nie verändert — append-only."
- ⚠️ MD5 = **Änderungserkennung**, nie als „Sicherheit" verkaufen.

### 2:30–3:30 · Versionsvergleich
- **Tun:** Button **„Versionen vergleichen"** → Felder „Von Version" / „Bis Version" wählen
- **Zeigen:** farbiger Diff — grün = hinzugefügt, rot = entfernt
- **Sagen:** „Hier vergleiche ich zwei Versionen. Grün ist hinzugekommen, Rot wurde entfernt. Das macht Pythons difflib im Backend."

### 3:30–4:30 · PDF-Export
- **Tun:** Button **„Als PDF exportieren"** (im Header)
- **Zeigen:** PDF mit Metadaten-Header (Titel, Eigentümer, Datum, Version) und formatiertem Inhalt
- **Sagen:** „Serverseitig: mistune macht aus Markdown HTML, der Odoo-QWeb-Report baut daraus das PDF. Erste Erzeugung wird als Anhang gespeichert, danach kommt es aus dem Cache — keine erneute Konvertierung."

### 4:30–5:00 · Rechte (nur erwähnen)
- **Tun:** nicht vorführen, nur sagen (oder optional als zweiter User einloggen, wenn vorbereitet)
- **Sagen:** „Der Zugriffsschutz hat zwei Ebenen: ACLs legen fest, wer das Modell überhaupt anfassen darf. Record Rules filtern dann auf Datensatzebene — über eine Odoo-Domain, die serverseitig an jede Abfrage angehängt wird. Resultat: ein normaler User sieht nur Eigenes, ein Admin alles. Versionen sind für User nur lesbar — die Historie ist nicht manipulierbar."

### 5:00–5:30 · Abschluss
- **Tun:** zurück zur Listenansicht
- **Sagen:** „Das war der Kern von MDWriter. Details gerne im Fachgespräch."

### Optional · Restore (nur wenn Zeit oder gefragt)
- **Tun:** auf einer Version Button **„Wiederherstellen"**
- **Sagen:** „Auch das Zurücksetzen ist selbst wieder versioniert — man verliert nichts."

## Notfall

- Vorschau lädt nicht → kurz warten / Dokument neu öffnen
- PDF hängt → ist vorab exportiert, Cache greift
- Ruhig bleiben, **nicht live debuggen**, im Ablauf weitergehen
