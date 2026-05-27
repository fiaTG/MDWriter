# Projektdokumentation

**Thema der Projektarbeit:**
Konzeption und Entwicklung einer zentralen technischen Dokumentationslösung auf Markdown-Basis innerhalb von Odoo 19

---

| | |
|---|---|
| **Verfasser** | Timo Giese |
| **Ausbildungsberuf** | Fachinformatiker Anwendungsentwicklung |
| **Ausbildungsbetrieb** | TrendTec UG, Mannheimer Straße 105a, 68535 Edingen-Neckarhausen |
| **Ausbildungsverantwortlicher** | Oliver Kölsch |
| **Bearbeitungszeitraum** | 08.05.2026 – 26.05.2026 |
| **Gesamtaufwand** | 80 Stunden |

---

## Inhaltsverzeichnis

1. [Einleitung](#1-einleitung)
   - 1.1 Projektumfeld und Ausgangssituation
   - 1.2 Projektziel
   - 1.3 Abgrenzung des Projekts
2. [Projektplanung](#2-projektplanung)
   - 2.1 Projektphasen und Zeitplanung
   - 2.2 Ressourcenplanung
   - 2.3 Wirtschaftlichkeitsbetrachtung
3. [Analysephase](#3-analysephase)
   - 3.1 Ist-Zustand
   - 3.2 Anforderungsanalyse
   - 3.3 Use-Case-Analyse
4. [Entwurfsphase](#4-entwurfsphase)
   - 4.1 Systemarchitektur
   - 4.2 Datenmodell
   - 4.3 Sicherheitskonzept
   - 4.4 UI/UX-Konzept
5. [Implementierungsphase](#5-implementierungsphase)
   - 5.1 Modulstruktur
   - 5.2 Backend-Implementierung
   - 5.3 Frontend-Implementierung
   - 5.4 Automatische Versionierung und PDF-Export
   - 5.5 Sicherheitsintegration
6. [Testphase](#6-testphase)
   - 6.1 Testkonzept
   - 6.2 Testfälle
   - 6.3 Testergebnisse
7. [Fazit](#7-fazit)
   - 7.1 Soll-/Ist-Vergleich der Zeitplanung
   - 7.2 Reflexion und Lessons Learned
   - 7.3 Ausblick

**Anhänge:**
- [Anhang A — Abkürzungsverzeichnis](#anhang-a--abkürzungsverzeichnis)
- [Anhang B — Quellenverzeichnis](#anhang-b--quellenverzeichnis)
- [Anhang C — Gantt-Diagramm](#anhang-c--gantt-diagramm)
- [Anhang D — Use-Case-Diagramm](#anhang-d--use-case-diagramm)
- [Anhang E — Architekturdiagramm](#anhang-e--architekturdiagramm)
- [Anhang F — Datenmodell](#anhang-f--datenmodell)
- [Anhang G — Quellcodeauszüge](#anhang-g--quellcodeauszüge)
- [Anhang H — Kundendokumentation](#anhang-h--kundendokumentation)

---

## 1. Einleitung

### 1.1 Projektumfeld und Ausgangssituation

Die TrendTec UG ist ein IT-Dienstleister mit Sitz in Edingen-Neckarhausen, der sich auf die Implementierung und Anpassung von ERP-Systemen auf Basis von Odoo spezialisiert hat. Das Unternehmen betreut kleine und mittelständische Unternehmen bei der Digitalisierung ihrer Geschäftsprozesse und beschäftigt derzeit neun Mitarbeiter.

Im Arbeitsalltag der Entwicklungsabteilung entsteht kontinuierlich technische Dokumentation: API-Beschreibungen, Installationsanleitungen, Konfigurationshinweise und Prozessbeschreibungen. Diese Dokumentation wurde bislang auf verschiedene externe Werkzeuge verteilt. Ein Teil wurde direkt im Odoo-internen HTML-WYSIWYG-Editor erstellt, ein anderer Teil in externen Tools wie Git-Wikis oder lokalen Textdateien gepflegt.

Daraus entstanden im Projektalltag konkrete Probleme: Dokumente lagen an unterschiedlichen Orten, ohne einheitlichen Standard oder zentrale Auffindbarkeit. Der HTML-WYSIWYG-Editor von Odoo eignet sich für Freitext, ist jedoch für technische Inhalte wie Code-Snippets, Konfigurationstabellen oder strukturierte Abläufe nur bedingt geeignet. In der Entwicklungsabteilung ist das Markdown-Format bereits aus der täglichen Arbeit mit Git-Repositories und Projektdokumentationen bekannt und akzeptiert. Eine Möglichkeit, Markdown direkt in Odoo zu verwenden, fehlte jedoch.

Die Folgen dieser Situation waren uneinheitliche Dokumentationsstandards, Medienbrüche zwischen verschiedenen Tools, eingeschränkte Eignung für technische Inhalte und eine erschwerte Wartbarkeit der vorhandenen Dokumentation.

### 1.2 Projektziel

Ziel des Projekts ist die Konzeption und Entwicklung eines nativen Odoo-19-Moduls, das eine zentrale, markdown-basierte Dokumentationslösung innerhalb des bestehenden ERP-Systems bereitstellt. Das Modul trägt den internen Projektnamen **MDWriter** und wird unter dem technischen Modulnamen `markdown_editor` entwickelt.

Konkret umfasst das Projektziel folgende Kernfunktionen:

- Einen Markdown-Editor mit geteilter Ansicht (Split-View): auf der linken Seite befindet sich der Texteingabebereich, auf der rechten Seite wird die formatierte Vorschau in Echtzeit dargestellt.
- Die strukturierte Speicherung von Dokumenten in der Odoo-Datenbank (PostgreSQL) über das Odoo ORM.
- Die Speicherung jeder Dokumentversion als Datei-Anhang (Attachment) im Odoo-Dateisystem.
- Die Absicherung des Zugriffs über das bestehende Odoo-ACL-System, sodass Benutzer ausschließlich ihre eigenen Dokumente sehen und bearbeiten können, während Administratoren systemweiten Zugriff erhalten.
- Einen PDF-Export, der die formatierte Markdown-Dokumentation als druckfertiges Dokument bereitstellt.
- Eine einfache Änderungsverfolgung, die den Verlauf aller Versionen eines Dokuments nachvollziehbar macht und einen direkten Versionsvergleich ermöglicht.

Das Modul soll als eigenständige Erweiterung in das Odoo-System integriert werden und langfristig in Kundenprojekten einsetzbar sein.

### 1.3 Abgrenzung des Projekts

Das Projekt umfasst ausdrücklich keine allgemeine Dokumentenmanagement-Plattform, kein kollaboratives Echtzeit-Editing mehrerer Nutzer und keine externe API-Schnittstelle. Die Lösung ist bewusst als schlankes, in Odoo integriertes Werkzeug konzipiert, das die vorhandene Infrastruktur nutzt und keine neuen Systemabhängigkeiten einführt.

---

## 2. Projektplanung

### 2.1 Projektphasen und Zeitplanung

Das Projekt wurde in fünf Phasen eingeteilt, die sich an dem klassischen Vorgehensmodell für Softwareentwicklungsprojekte orientieren. Die nachfolgende Tabelle zeigt die geplante Stundenzuteilung je Phase. Das zugehörige Gantt-Diagramm befindet sich in Anhang C.

| Phase | Aufgaben | Geplante Zeit |
|---|---|---|
| **Analyse** | Lösungsansätze bewerten, Anforderungsanalyse, Technologierecherche, Entwicklungsumgebung einrichten | 8 h |
| **Entwurf** | Architekturplanung, Datenmodell-Design, Sicherheitskonzept, UI/UX-Konzept | 10 h |
| **Implementierung** | Backend (Modell, Attachment, PDF), Frontend (Editor, Vorschau, ACL, Views) | 40 h |
| **Test** | Testfälle erstellen, Funktions- und Integrationstests, Fehleranalyse | 10 h |
| **Dokumentation** | Projektdokumentation, Präsentationsvorbereitung | 12 h |
| **Gesamt** | | **80 h** |

Die Analysephase diente der Klärung technischer Grundlagen und der Auswahl geeigneter Bibliotheken. In der Entwurfsphase wurden die Kernentscheidungen zu Datenmodell, Sicherheitsarchitektur und Benutzeroberfläche getroffen. Die Implementierungsphase mit dem größten Zeitanteil (50 % des Gesamtaufwands) teilte sich in Backend-Entwicklung (13 Stunden) und Frontend-Entwicklung (27 Stunden) auf. Die Testphase umfasste sowohl manuelle Integrationstests als auch die Erstellung automatisierter Tests. Die Dokumentationsphase schloss das Projekt mit der vorliegenden Projektdokumentation und der Vorbereitung der Abschlusspräsentation ab.

### 2.2 Ressourcenplanung

Für die Durchführung des Projekts standen folgende Ressourcen zur Verfügung:

**Personelle Ressourcen:**

| Rolle | Person | Einsatz |
|---|---|---|
| Entwickler (Auszubildender) | Timo Giese | 80 h (Hauptaufwand) |
| Projektverantwortlicher | Oliver Kölsch | ca. 5 h (Freigaben, Feedback) |

**Technische Ressourcen:**

Die Entwicklung erfolgte auf einem Windows-11-Arbeitsplatz mit Visual Studio Code als Entwicklungsumgebung. Das Deployment und die abschließenden Tests wurden auf einer Odoo.sh-Instanz (Odoo 19, Enterprise-Lizenz) durchgeführt. Als Versionsverwaltung wurde Git mit GitHub als Remote-Repository genutzt.

### 2.3 Wirtschaftlichkeitsbetrachtung

#### 2.3.1 Make-or-Buy-Analyse

Vor der Entscheidung zur Eigenentwicklung wurden alternative Lösungsansätze bewertet:

**Alternative 1 – Atlassian Confluence (SaaS):**
Confluence ist ein etabliertes Wiki- und Dokumentationswerkzeug mit Markdown-Unterstützung. Es bietet eine gute Eignung für technische Inhalte, ist jedoch ein externes System ohne native Odoo-Integration. Medienbrüche zwischen Odoo und Confluence bleiben bestehen. Die Lizenzkosten betragen bei neun Benutzern im Cloud-Modell ca. 10 € pro Nutzer und Monat.

**Alternative 2 – GitLab/GitHub Wiki:**
Die bereits genutzten Git-Plattformen bieten integrierte Wikis mit Markdown-Unterstützung. Diese Lösung ist kostenneutral im Rahmen bestehender Lizenzen, bietet jedoch keine Odoo-Integration, keinen PDF-Export aus Odoo heraus und keine Verbindung zum Odoo-ACL-System. Für externe Kundenprojekte ist diese Lösung nicht skalierbar.

**Alternative 3 – Eigenentwicklung (MDWriter):**
Ein natives Odoo-Modul nutzt die bestehende Odoo-Infrastruktur vollständig: Datenhaltung in PostgreSQL, Zugriffskontrolle über das Odoo-ACL-System, PDF-Export über den Odoo-Reportingmechanismus. Medienbrüche entfallen. Die Lösung ist mandantenfähig und direkt für Kundenprojekte einsetzbar.

Die Entscheidung fiel auf die Eigenentwicklung, da die Anforderung nach vollständiger Odoo-Integration durch externe Tools strukturell nicht erfüllbar ist.

#### 2.3.2 Kostenvergleich

**Projektkosten Eigenentwicklung:**

| Position | Berechnung | Betrag |
|---|---|---|
| Entwicklung (Auszubildender) | 80 h × 12,00 €/h | 960,00 € |
| Projektbegleitung (Projektverantwortlicher) | 5 h × 150,00 €/h | 750,00 € |
| **Einmalige Projektkosten gesamt** | | **1.710,00 €** |
| Jährliche Wartung (geschätzt) | 8 h × 12,00 €/h | 96,00 €/Jahr |

**Laufende Kosten Confluence (9 Benutzer):**

| Position | Berechnung | Betrag |
|---|---|---|
| Lizenz Cloud | 9 × 10,00 €/Monat × 12 | 1.080,00 €/Jahr |

#### 2.3.3 Amortisationsberechnung

Die Eigenentwicklung verursacht im ersten Jahr höhere Kosten als die Lizenzlösung (1.710 € + 96 € = 1.806 € vs. 1.080 €). Ab dem zweiten Jahr entstehen lediglich Wartungskosten von ca. 96 €/Jahr gegenüber 1.080 €/Jahr für Confluence. Die Amortisation ist nach ca. 18 Monaten erreicht.

Über einen Betrachtungshorizont von drei Jahren ergeben sich folgende Gesamtkosten:

| Lösung | Jahr 1 | Jahr 2 | Jahr 3 | Gesamt |
|---|---|---|---|---|
| MDWriter | 1.806 € | 96 € | 96 € | **1.998 €** |
| Confluence | 1.080 € | 1.080 € | 1.080 € | **3.240 €** |

Zusätzlich zu den quantifizierbaren Einsparungen ergeben sich nicht-monetäre Vorteile: vollständige Datenhoheit (alle Dokumente verbleiben in der eigenen Odoo-Datenbank), kein externer SaaS-Anbieter, nahtlose Integration in bestehende Odoo-Workflows und direkte Weiterverwendbarkeit des Moduls in Kundenprojekten.

---

## 3. Analysephase

### 3.1 Ist-Zustand

Zu Projektbeginn wurde der aktuelle Stand der Dokumentationspraxis in der Entwicklungsabteilung analysiert. Folgende Werkzeuge wurden parallel genutzt:

- **Odoo HTML-Editor:** Für Freitextnotizen und einfache Anleitungen. Die Eignung für Code-Snippets und strukturierte technische Dokumentation ist durch das WYSIWYG-Paradigma eingeschränkt.
- **Git-Wikis (GitHub/GitLab):** Für projektbezogene Dokumentation direkt im Repository-Kontext. Kein Zugriff aus Odoo heraus.
- **Lokale Markdown-Dateien:** Von einzelnen Entwicklern lokal gepflegt, ohne zentrale Ablage oder Versionskontrolle auf Systemebene.

Der Hauptbefund der Ist-Analyse lautet: Es existiert kein einheitlicher Standard für technische Dokumentation. Der Zugriff auf Dokumente ist nicht über das Odoo-Benutzer- und Berechtigungssystem abgesichert. Versionsstände sind nicht systematisch nachvollziehbar.

### 3.2 Anforderungsanalyse

Auf Basis der Ist-Analyse wurden die Anforderungen an das neue System in funktionale und nicht-funktionale Anforderungen gegliedert.

#### 3.2.1 Funktionale Anforderungen

| Nr. | Anforderung | Priorität |
|---|---|---|
| F01 | Markdown-Editor mit Split-View (Eingabe links, Vorschau rechts) | Muss |
| F02 | Live-Vorschau: Vorschau aktualisiert sich während der Eingabe | Muss |
| F03 | Speicherung von Dokumenten in der Odoo-Datenbank | Muss |
| F04 | Speicherung jeder Version als Datei-Anhang (`.md`-Datei) | Muss |
| F05 | Zugriffsschutz: Benutzer sehen nur ihre eigenen Dokumente | Muss |
| F06 | Administratoren haben Zugriff auf alle Dokumente | Muss |
| F07 | PDF-Export des aktuellen Dokumentinhalts | Muss |
| F08 | Automatische Versionierung bei jeder Inhaltsänderung | Muss |
| F09 | Versionsvergleich (Diff-Ansicht) zweier Versionen | Muss |
| F10 | Statusverwaltung (Entwurf, Veröffentlicht, Archiviert) | Soll |
| F11 | Wiederherstellung einer älteren Version | Soll |
| F12 | Syntax-Highlighting im Editor | Soll |

#### 3.2.2 Nicht-funktionale Anforderungen

| Nr. | Anforderung |
|---|---|
| NF01 | Kompatibilität mit Odoo 19 (Community und Enterprise) |
| NF02 | XSS-Schutz: Kein unsicheres HTML-Rendering von Benutzereingaben |
| NF03 | Keine externen Laufzeitabhängigkeiten (CDN-unabhängig) |
| NF04 | Dark-Mode-Kompatibilität über Odoo CSS-Variablen |
| NF05 | Einhaltung der Odoo-Modulkonventionen (Manifest, ACL, ORM) |
| NF06 | Testabdeckung für kritische Backend-Funktionen |

### 3.3 Use-Case-Analyse

Die wesentlichen Anwendungsfälle des Systems lassen sich in zwei Benutzerrollen aufteilen. Das vollständige Use-Case-Diagramm befindet sich in Anhang D.

**Rolle: Benutzer (normaler Mitarbeiter)**
Ein Benutzer kann eigene Dokumente anlegen, bearbeiten, veröffentlichen und archivieren. Er kann den Verlauf seiner eigenen Dokumente einsehen, Versionen vergleichen und eine ältere Version wiederherstellen. Er kann ein Dokument als PDF exportieren und als Markdown-Datei herunterladen. Er hat keinen Zugriff auf Dokumente anderer Benutzer.

**Rolle: Administrator**
Ein Administrator verfügt über alle Rechte eines Benutzers, hat darüber hinaus jedoch systemweiten Zugriff auf sämtliche Dokumente aller Benutzer. Er kann außerdem Dokumente löschen – eine Funktion, die normalen Benutzern nicht zur Verfügung steht.

---

## 4. Entwurfsphase

### 4.1 Systemarchitektur

MDWriter ist als natives Odoo-Modul konzipiert, das vollständig in die bestehende Odoo-Architektur eingebettet ist. Es gibt keine externe Kommunikation und keine zusätzlichen Systemdienste außerhalb von Odoo. Das Architekturdiagramm des Moduls befindet sich in Anhang E.

Die Architektur folgt dem dreischichtigen Aufbau von Odoo:

**Datenschicht:** PostgreSQL-Datenbank, verwaltet über das Odoo ORM. Das Modul definiert zwei eigene Modelle (`x.md.document` und `x.md.document.version`) sowie einen temporären Hilfsassistenten (`x.md.document.diff.wizard`). Dateianhänge werden über das native Odoo-Attachment-System (`ir.attachment`) gespeichert.

**Anwendungsschicht (Backend):** Python-Klassen, die das Odoo ORM erweitern. Hier sind Versionierungslogik, PDF-Rendering, Statusübergänge und Sicherheitsregeln implementiert.

**Präsentationsschicht (Frontend):** OWL-Komponente (Odoo Web Library), die als Custom Field Widget registriert ist. Die Komponente rendert den Split-View-Editor mit CodeMirror als Syntaxeditor und markdown-it als Live-Renderer. Die Einbindung erfolgt über das Odoo-Assets-Bundle-System.

Das Modul ist nicht von externen CDNs abhängig und kann ohne Internetverbindung betrieben werden: Alle JavaScript-Bibliotheken (markdown-it, CodeMirror) liegen lokal im Modulverzeichnis. Die einzige Python-Laufzeitabhängigkeit ist `mistune`, eine leichtgewichtige Markdown-zu-HTML-Bibliothek, die über `requirements.txt` im Repository deklariert ist.

### 4.2 Datenmodell

Das Datenmodell besteht aus zwei dauerhaft gespeicherten Odoo-Modellen und einem temporären Hilfsmodell. Das vollständige Entity-Relationship-Diagramm befindet sich in Anhang F.

Das `x.` am Anfang der Modellnamen ist eine Odoo-Konvention für Module außerhalb des offiziellen Namensraums und signalisiert, dass es sich um eine projektspezifische Erweiterung handelt.

**Hauptmodell `x.md.document`:**

Das Hauptmodell repräsentiert ein Dokument. Es speichert den aktuellen Dokumenttitel, den Markdown-Inhalt, den Veröffentlichungsstatus sowie den Eigentümer des Dokuments. Das Feld `current_version` ist ein berechnetes Feld, das die höchste vorhandene Versionsnummer aus der Versionstabelle ableitet. Das Feld `content_html` enthält den serverseitig gerenderten HTML-Code und wird ausschließlich für den PDF-Export verwendet.

| Feldname | Typ | Beschreibung |
|---|---|---|
| `name` | Char | Dokumenttitel (Pflichtfeld) |
| `content_md` | Text | Markdown-Primärinhalt |
| `content_html` | Html | Gerendertes HTML (berechnet, sanitize=False — für PDF-Export) |
| `state` | Selection | Entwurf / Veröffentlicht / Archiviert |
| `owner_id` | Many2one → res.users | Eigentümer (Standard: aktueller Benutzer) |
| `version_ids` | One2many → x.md.document.version | Alle Versionen |
| `current_version` | Integer | Berechnet: höchste Versionsnummer |

**Versionsmodell `x.md.document.version`:**

Versionen sind append-only: Einmal angelegt, werden sie niemals verändert. Bei jeder Inhaltsänderung am Hauptdokument wird ein neuer Versionsrecord erstellt. Das Modell speichert den vollständigen Markdown-Inhalt der Version, einen MD5-Prüfsummenwert zur Integritätsprüfung, den verändernden Benutzer sowie Zeitstempel und Dateianhänge.

| Feldname | Typ | Beschreibung |
|---|---|---|
| `document_id` | Many2one → x.md.document | Verweis auf Dokument |
| `version` | Integer | Versionsnummer (1, 2, 3 …) |
| `content_md` | Text | Markdown-Inhalt dieser Version |
| `checksum` | Char | MD5-Prüfsumme des Inhalts |
| `changed_by` | Many2one → res.users | Wer hat geändert |
| `changed_at` | Datetime | Wann wurde geändert |
| `md_attachment_id` | Many2one → ir.attachment | .md-Datei dieser Version |
| `pdf_attachment_id` | Many2one → ir.attachment | .pdf-Datei dieser Version |

**Hilfsmodell `x.md.document.diff.wizard`:**

Dieses Modell ist als TransientModel umgesetzt — ein temporäres Hilfsmodell in Odoo, das keine Daten dauerhaft speichert. Odoo löscht solche Datensätze automatisch nach kurzer Zeit. Es dient ausschließlich als Datenträger für den Versionsvergleich-Dialog.

### 4.3 Sicherheitskonzept

Das Sicherheitskonzept nutzt das bestehende Rechtesystem von Odoo und kombiniert zwei sich ergänzende Mechanismen: Zugriffsrechte auf Modellebene (ACL) und zeilenbasierte Datensatzregeln (Record Rules).

**Zugriffsrechte (ACL — Access Control List):**
ACLs steuern, ob ein Benutzer ein Modell grundsätzlich lesen, schreiben, anlegen oder löschen darf. Die Datei `security/ir.model.access.csv` definiert diese Berechtigungen pro Modell und Gruppe. Normale Benutzer (`base.group_user`) haben Lese-, Schreib- und Erstell-Rechte auf Dokumente, jedoch kein Löschrecht. Auf Versionsrecords haben normale Benutzer ausschließlich Leserecht — damit ist der Append-only-Charakter der Versionierung auf ACL-Ebene durchgesetzt. Administratoren (`base.group_system`) verfügen über vollständige CRUD-Rechte auf beiden Modellen.

**Record Rules (Datensatzregeln):**
ACLs allein reichen nicht aus: Sie steuern den Zugriff auf Modellebene, nicht auf Datensatzebene. Ohne Record Rules könnte jeder Benutzer alle Dokumente aller anderen Benutzer sehen und bearbeiten. Record Rules ergänzen das System um eine zeilenbasierte Zugriffskontrolle, die als WHERE-Klausel in SQL-Abfragen eingebaut wird:

- Die **Eigentümer-Regel** schränkt den Zugriff normaler Benutzer auf Dokumente ein, deren `owner_id` mit dem aktuell angemeldeten Benutzer übereinstimmt: `[("owner_id", "=", user.id)]`.
- Die **Admin-Regel** gewährt Administratoren Zugriff auf alle Datensätze ohne Einschränkung: `[(1, "=", 1)]`.

**XSS-Schutz:**
Benutzereingaben im Markdown-Editor dürfen kein eingebettetes HTML ausführen. Im Frontend wird markdown-it mit der Option `html: false` initialisiert, wodurch HTML-Tags in Markdown-Texten escaped und nicht interpretiert werden. Im Backend ist mistune so konfiguriert, dass kein schädliches JavaScript in das gerenderte HTML gelangen kann. Die Verwendung von `markup()` aus der OWL-Bibliothek signalisiert dem Framework, dass der gerenderte Inhalt vertrauenswürdig ist — ohne diese Kennzeichnung würde das `t-out`-Direktiv den Inhalt ein zweites Mal escapen.

### 4.4 UI/UX-Konzept

Die Benutzeroberfläche orientiert sich an den Odoo-Designkonventionen und erweitert diese um ein unternehmensspezifisches Branding auf Basis der Trendtec-Farbe Lime Green (#97d21d).

**Split-View-Layout:** Der Editor ist in zwei gleich große vertikale Bereiche aufgeteilt. Links befindet sich der Eingabebereich mit dem CodeMirror-Syntaxeditor, rechts die live gerenderte Vorschau. Die Trennlinie zwischen beiden Bereichen ist verschiebbar und visuell durch die Primärfarbe hervorgehoben.

**Typografie:** Für den Editor-Bereich wird die Programmierschrift JetBrains Mono verwendet. Das Modul unterstützt außerdem den Dark-Mode von Odoo: Odoo bietet einen systemweiten Theme-Wechsel an, und MDWriter reagiert darauf über CSS Custom Properties (`light-dark()`). Das CodeMirror-Theme und die Vorschau passen sich automatisch an.

**Statusvisualisierung:** Der Dokumentstatus (Entwurf, Veröffentlicht, Archiviert) wird in der Listenansicht farblich als Badge dargestellt und ist über die Statusleiste in der Formularansicht nachvollziehbar.

---

## 5. Implementierungsphase

### 5.1 Modulstruktur

Das Modul trägt den technischen Namen `markdown_editor` und folgt der Odoo-Standardstruktur für Module. Die wichtigsten Verzeichnisse und Dateien sind:

```
markdown_editor/
├── __manifest__.py          # Modulmetadaten, Assets, Abhängigkeiten
├── models/
│   ├── md_document.py       # Hauptmodell und Versionsmodell
│   └── md_document_diff.py  # Vergleichsassistent
├── views/
│   ├── md_document_views.xml
│   └── md_document_diff_views.xml
├── static/
│   ├── lib/                 # markdown-it, CodeMirror (lokal)
│   └── src/
│       ├── js/              # OWL-Komponente
│       ├── xml/             # OWL-Template
│       └── scss/            # Styling, Branding, PDF-Styling
├── security/
│   ├── ir.model.access.csv
│   └── markdown_editor_security.xml
├── report/
│   └── md_document_report.xml
└── tests/
    └── test_md_document.py
```

Das Modul hängt von drei Odoo-Modulen ab: `base` und `web`, die in jeder Odoo-Installation vorhanden sind, sowie `documents` (Odoo-Documents-App) für die automatische Ablage jeder Markdown-Version im Dokumentenordner. Die Documents-Integration ist defensiv implementiert: Fehlt das Modul oder schlägt die Ordneranlage fehl, wird der Fehler protokolliert und die Versionierung läuft ohne Unterbrechung weiter.

### 5.2 Backend-Implementierung

#### 5.2.1 Datenmodell (Python / Odoo ORM)

Die Modellklassen erben von `models.Model` und nutzen ausschließlich das Odoo ORM ohne rohe SQL-Abfragen. Der Eigentümer eines Dokuments wird beim Anlegen automatisch auf den aktuell eingeloggten Benutzer gesetzt:

```python
owner_id = fields.Many2one(
    "res.users",
    string="Eigentümer",
    default=lambda self: self.env.user,
)
```

Das berechnete Feld `current_version` aggregiert die höchste Versionsnummer aus der Versionstabelle:

```python
@api.depends("version_ids.version")
def _aktuelle_version_berechnen(self):
    for doc in self:
        doc.current_version = max(doc.version_ids.mapped("version"), default=0)
```

Ein Auszug der vollständigen Felddefinitionen befindet sich in Anhang G.1.

### 5.3 Frontend-Implementierung

#### 5.3.1 OWL-Komponente

Für die Bearbeitung der Markdown-Dokumente wurde eine eigene OWL-Komponente entwickelt und als Field Widget in Odoo eingebunden. Ein Widget ist in Odoo eine benutzerdefinierte UI-Komponente, die an ein Datenfeld gekoppelt wird — in diesem Fall das `content_md`-Feld. Das Widget wird in der XML-View über `widget="markdown_editor"` referenziert.

Die Komponente `MarkdownField` wird über die Odoo-Field-Registry registriert:

```javascript
registry.category("fields").add("markdown_editor", {
    component: MarkdownField,
    supportedTypes: ["text"],
});
```

Die Komponente initialisiert bei der Montage (`onMounted`) eine CodeMirror-Instanz auf der Textarea und richtet einen debounced Change-Handler ein, der die Live-Vorschau mit einer Verzögerung von 300 Millisekunden aktualisiert. Diese Verzögerung verhindert, dass bei schneller Eingabe bei jedem Tastenanschlag ein vollständiges Re-Render ausgelöst wird. Den vollständigen Ausschnitt zeigt Anhang G.3.

Die Reaktivität des Zustands (`state`) wird über OWLs `useState`-Hook sichergestellt. Änderungen an `state.html` lösen automatisch ein Re-Render der Vorschau aus.

#### 5.3.2 Markdown-Rendering

Als Markdown-Renderer wird markdown-it in Version 14 verwendet, lokal eingebunden unter `static/lib/markdown-it.min.js`. Die Bibliothek ist nicht von externen CDNs abhängig und kann ohne Internetverbindung betrieben werden. Die Initialisierung erfolgt mit folgenden Optionen:

```javascript
window.markdownit({ html: false, breaks: true, linkify: true })
```

- `html: false` verhindert die Interpretation von eingebettetem HTML (XSS-Schutz).
- `breaks: true` wandelt einfache Zeilenumbrüche in `<br>`-Tags um.
- `linkify: true` erkennt URLs im Text und verlinkt sie automatisch.

Das Rendering-Ergebnis wird mit `markup()` aus `@odoo/owl` als vertrauenswürdiger HTML-String markiert, damit `t-out` im OWL-Template ihn unescaped darstellt.

#### 5.3.3 Layout und Styling

Das Split-View-Layout basiert auf CSS Flexbox. Editor-Pane und Vorschau-Pane haben jeweils eine Breite von 50 % des verfügbaren Platzes, die über einen ziehbaren Splitter angepasst werden kann.

Der Scope aller CSS-Regeln ist eng gefasst: Stile sind ausschließlich auf `.o_markdown_editor`, `.o_markdown_preview` und `.o_md_diff` angewendet, um Konflikte mit anderen Odoo-Modulen auszuschließen.

### 5.4 Automatische Versionierung und PDF-Export

Die Versionierung wird automatisch bei zwei Ereignissen ausgelöst: beim Erstellen eines neuen Dokuments (`create`) und beim Schreiben auf das Feld `content_md` (`write`). Der `write`-Override prüft, ob der betreffende Schlüssel im übergebenen Wertedict enthalten ist — Statusänderungen erzeugen dadurch keine neue Version. Den vollständigen Code-Ausschnitt zeigt Anhang G.2.

Für jede neue Version wird beim Anlegen automatisch eine PDF-Datei gerendert und als Odoo-Attachment gespeichert. Bereits erzeugte PDF-Dateien werden bei einem Exportaufruf wiederverwendet, sofern die Version noch aktuell ist. Das vermeidet eine wiederholte Konvertierung bei jedem Exportaufruf.

Schlägt das PDF-Rendering fehl — etwa weil wkhtmltopdf nicht verfügbar ist — protokolliert das System den Fehler, ohne die Versionierung zu unterbrechen. Die Version wird in jedem Fall angelegt, lediglich ohne PDF-Attachment.

### 5.5 Sicherheitsintegration

Die in Kapitel 4.3 beschriebenen Sicherheitsmechanismen wurden vollständig implementiert. Die ACL-Konfiguration in `security/ir.model.access.csv` sowie die Record Rules in `security/markdown_editor_security.xml` stellen sicher, dass Benutzer ausschließlich ihre eigenen Dokumente sehen und bearbeiten können. Administratoren erhalten über eine separate Admin-Regel Zugriff auf alle Datensätze. Anhang G.4 zeigt einen Auszug beider Dateien.

---

## 6. Testphase

### 6.1 Testkonzept

Das Testkonzept umfasst zwei Ebenen: automatisierte Backend-Tests mit dem Odoo-Testframework sowie manuelle Integrationstests in der laufenden Odoo-Instanz.

Für die automatisierten Tests wird die Klasse `TransactionCase` des Odoo-Testframeworks verwendet. Diese rollt nach jedem Testfall die Datenbankänderungen automatisch zurück, sodass Tests isoliert und ohne gegenseitige Beeinflussung ausgeführt werden können (Odoo S.A., 2025). Die Tests decken die kritischen Pfade der Geschäftslogik ab: Versionierung, Zugriffskontrolle und Versionsvergleich.

Die Testdatei liegt unter `tests/test_md_document.py` und wird mit folgendem Befehl ausgeführt:

```bash
odoo-bin -d <datenbankname> --test-enable -u markdown_editor --stop-after-init
```

### 6.2 Testfälle

Die Testsuite umfasst 7 automatisierte Testfälle in drei Testklassen, die direkt den Pflichtanforderungen aus dem Projektantrag entsprechen.

**Testgruppe 1: Versionierung (TestMdDocumentVersioning)**

| Nr. | Beschreibung | Erwartetes Ergebnis |
|---|---|---|
| T1.1 | Neues Dokument anlegen | Version 1 wird automatisch erstellt |
| T1.2 | Inhalt ändern | Neue Version wird angelegt, `current_version` steigt auf 2 |
| T1.3 | Restore-Funktion | Älterer Inhalt wird wiederhergestellt |

**Testgruppe 2: Zugriffskontrolle (TestMdDocumentACL)**

| Nr. | Beschreibung | Erwartetes Ergebnis |
|---|---|---|
| T2.1 | Eigentümer liest eigenes Dokument | Zugriff erlaubt, Name korrekt |
| T2.2 | Fremder Benutzer sucht Dokument eines anderen | Leeres Ergebnis (Record Rule greift) |
| T2.3 | Normaler Benutzer legt Version manuell an | `AccessError` (ACL verweigert create auf Versionsmodell) |

**Testgruppe 3: Versionsvergleich (TestMdDocumentDiff)**

| Nr. | Beschreibung | Erwartetes Ergebnis |
|---|---|---|
| T3.1 | Diff zweier Versionen | HTML enthält CSS-Klassen für Hinzufügungen und Löschungen |

### 6.3 Testergebnisse

Alle 7 automatisierten Testfälle wurden auf der Odoo.sh-Instanz erfolgreich ausgeführt:

```
0 failed, 0 error(s) of 7 tests
```

Im Rahmen der manuellen Integrationstests wurden folgende Szenarien geprüft:

- Anlegen, Bearbeiten und Veröffentlichen eines Dokuments im Browser
- Korrekte Darstellung der Live-Vorschau mit verschiedenen Markdown-Elementen (Überschriften, Listen, Code-Blöcke, Tabellen, Blockzitate, Links)
- PDF-Export: Korrekte Darstellung von Formatierungen, Metadaten-Header, Zeichensatz
- Versionsvergleich: Korrekte farbliche Darstellung von Änderungen
- Zugriffstest: Anmeldung als separater Testbenutzer, Bestätigung dass keine fremden Dokumente sichtbar sind
- Dark-Mode: Korrekte Darstellung nach Theme-Wechsel in Odoo

Alle manuellen Tests verliefen ohne Beanstandungen. Die Abnahme durch den Projektverantwortlichen Oliver Kölsch erfolgte am 26. Mai 2026.

---

## 7. Fazit

### 7.1 Soll-/Ist-Vergleich der Zeitplanung

| Phase | Geplant | Tatsächlich | Differenz |
|---|---|---|---|
| Analyse | 8 h | 8 h | ± 0 h |
| Entwurf | 10 h | 10 h | ± 0 h |
| Implementierung | 40 h | 40 h | ± 0 h |
| Test | 10 h | 10 h | ± 0 h |
| Dokumentation | 12 h | 12 h | ± 0 h |
| **Gesamt** | **80 h** | **80 h** | **± 0 h** |

Das Projekt wurde innerhalb des geplanten Zeitrahmens abgeschlossen. Innerhalb der Implementierungsphase ergaben sich kleinere Verschiebungen zwischen den Teilbereichen: Die Backend-Entwicklung verlief zügiger als erwartet, da das Odoo ORM gut dokumentiert ist und wenige Überraschungen bereithielt. Die zusätzliche Zeit floss in die Frontend-Integration, insbesondere in die korrekte Einbindung von CodeMirror in den OWL-Komponentenlebenszyklus und die Behebung von Odoo-Layout-Konflikten.

Alle acht Pflichtanforderungen aus dem Projektantrag wurden vollständig erfüllt. Darüber hinaus wurden die Statusverwaltung (Entwurf, Veröffentlicht, Archiviert) und die Restore-Funktion als sinnvolle Erweiterung der Änderungsverfolgung implementiert.

### 7.2 Reflexion und Lessons Learned

Das Projekt hat mehrere technische Lerneffekte hervorgebracht, die für zukünftige Odoo-Entwicklungen relevant sind.

**Odoo OWL-Komponentenlebenszyklus:** Die Integration einer externen JavaScript-Bibliothek (CodeMirror) in eine OWL-Komponente erfordert eine sorgfältige Handhabung der Lifecycle-Callbacks. `onMounted` und `onWillUnmount` sind der korrekte Ort für Initialisierung und Bereinigung von DOM-basierten Bibliotheken. Ein frühes Verständnis dieser Lifecycle-Reihenfolge hätte einige Debugging-Schleifen vermieden.

**CSS-Scoping in Odoo:** Odoo Enterprise-Layouts setzen teils aggressive globale CSS-Regeln, die lokale Modul-Styles überschreiben können. Die konsequente Verwendung scoped CSS-Selektoren hat sich als robuste Strategie bewährt, um Konflikte zu vermeiden.

**Trennung von Render-Ebenen:** Das korrekte Zusammenspiel von `mistune`, `Markup()`, `sanitize=False` und `t-out` im Kontext des Odoo-Reportings erforderte ein genaues Verständnis der mehrschichtigen Escaping-Pipeline. Gleichzeitig konnte ich dadurch mein Verständnis für die Odoo-Frontend-Architektur vertiefen.

**PDF-Rendering mit wkhtmltopdf:** Die Unterschiede zwischen wkhtmltopdf (QtWebKit) und modernen Browsern sind erheblich. Variable Fonts und einige moderne CSS-Features werden nicht unterstützt. Für PDF-spezifisches Styling müssen statische Font-Schnitte und SCSS-Variablen statt CSS Custom Properties verwendet werden.

### 7.3 Ausblick

Das implementierte Modul stellt eine vollständige und produktionsreife Lösung für die ursprünglich definierten Anforderungen dar. Das Modul kann als Grundlage für weiterführende Dokumentationsanwendungen dienen — etwa für Installationsanleitungen, API-Dokumentationen oder Modulbeschreibungen in Kundenprojekten. Für zukünftige Iterationen sind folgende Erweiterungen denkbar:

**Kurzfristig:**
- Performance-Optimierung der Live-Vorschau bei sehr langen Dokumenten (> 10.000 Zeilen) durch virtuelles Rendering oder gezieltes Debouncing.
- Erweiterte Suchfunktion: Volltextsuche im Markdown-Inhalt über die Odoo-Search-View.

**Mittelfristig:**
- Kommentarfunktion: Anmerkungen zu einzelnen Versionen, ohne das Hauptversionsmodell zu erweitern.
- Vorlagen-System: Vordefinierte Markdown-Templates für häufig verwendete Dokumententypen.

**Langfristig:**
- Einsatz in Kundenprojekten als eigenständig konfigurierbares Modul mit anpassbarem Branding.

---

## Anhang A — Abkürzungsverzeichnis

| Abkürzung | Bedeutung |
|---|---|
| ACL | Access Control List (Zugriffssteuerungsliste) |
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| CDN | Content Delivery Network |
| CSS | Cascading Style Sheets |
| ERP | Enterprise Resource Planning |
| HTML | HyperText Markup Language |
| MD5 | Message-Digest Algorithm 5 (Prüfsummenverfahren) |
| ORM | Object-Relational Mapper |
| OWL | Odoo Web Library (Frontend-Framework) |
| PDF | Portable Document Format |
| SCSS | Sassy Cascading Style Sheets |
| SQL | Structured Query Language |
| SaaS | Software as a Service |
| UI | User Interface |
| UX | User Experience |
| XSS | Cross-Site Scripting |

---

## Anhang B — Quellenverzeichnis

| Nr. | Quelle |
|---|---|
| [1] | Odoo S.A.: *Odoo 19 Developer Documentation*. https://www.odoo.com/documentation/19.0/ |
| [2] | Odoo S.A.: *OWL (Odoo Web Library) Documentation*. https://github.com/odoo/owl |
| [3] | Odoo S.A.: *ORM API Reference — Odoo 19*. https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html |
| [4] | markdown-it: *markdown-it – Markdown Parser, Done Right*. https://github.com/markdown-it/markdown-it |
| [5] | CodeMirror: *CodeMirror 5 User Manual*. https://codemirror.net/5/doc/manual.html |
| [6] | Leporati, T.: *mistune – A fast yet powerful Python Markdown parser*. https://github.com/lepture/mistune |
| [7] | OWASP Foundation: *Cross Site Scripting (XSS)*. https://owasp.org/www-community/attacks/xss/ |

---

## Anhang C — Gantt-Diagramm

*[Abbildung: Gantt-Diagramm der Projektphasen — in der eingereichten PDF-Version enthalten]*

---

## Anhang D — Use-Case-Diagramm

*[Abbildung: UML Use-Case-Diagramm mit den Rollen Benutzer und Administrator — in der eingereichten PDF-Version enthalten]*

---

## Anhang E — Architekturdiagramm

*[Abbildung: Architekturdiagramm des MDWriter-Moduls (Drei-Schichten-Architektur) — in der eingereichten PDF-Version enthalten]*

---

## Anhang F — Datenmodell

*[Abbildung: Entity-Relationship-Diagramm der Modelle x.md.document, x.md.document.version und x.md.document.diff.wizard — in der eingereichten PDF-Version enthalten]*

---

## Anhang G — Quellcodeauszüge

### G.1 Felddefinitionen — Hauptmodell `XMdDocument`

Datei: `markdown_editor/models/md_document.py`

Der folgende Ausschnitt zeigt die Felddefinitionen des Hauptmodells. Das Modell erbt von `models.Model` und nutzt ausschließlich das Odoo ORM. Das berechnete Feld `current_version` wird bei jeder Änderung an verknüpften Versionsrecords automatisch neu berechnet.

```python
class XMdDocument(models.Model):
    _name = "x.md.document"
    _description = "Markdown Document"

    name = fields.Char(string="Titel", required=True)
    content_md = fields.Text(string="Markdown-Inhalt")
    state = fields.Selection([
        ("draft", "Entwurf"),
        ("published", "Veröffentlicht"),
        ("archived", "Archiviert"),
    ], default="draft")
    owner_id = fields.Many2one(
        comodel_name="res.users",
        string="Eigentümer",
        default=lambda self: self.env.user,
    )
    version_ids = fields.One2many(
        comodel_name="x.md.document.version",
        inverse_name="document_id",
        string="Versionen",
    )
    current_version = fields.Integer(
        string="Aktuelle Version",
        compute="_aktuelle_version_berechnen",
        store=True,
    )
```

### G.2 Automatische Versionierung

Datei: `markdown_editor/models/md_document.py`

Der folgende Ausschnitt zeigt den `write()`-Override und die Methode `_version_anlegen()`. `write()` ist ein Odoo-ORM-Hook, der bei jeder Schreiboperation aufgerufen wird. Die Prüfung `if "content_md" in vals` stellt sicher, dass nur Inhaltsänderungen eine neue Version auslösen — Statusänderungen (`state`) erzeugen keine neue Version.

`_version_anlegen()` koordiniert drei Teilaufgaben: das Anlegen der `.md`-Datei als Attachment, das Rendern und Speichern der `.pdf`-Datei sowie das Anlegen des Versionsrecords mit MD5-Prüfsumme. `sudo()` ist nötig, da normale Benutzer über die ACL keine Versionsrecords direkt anlegen dürfen.

```python
def write(self, vals):
    res = super().write(vals)
    if "content_md" in vals:
        self._version_anlegen()
    return res

def _version_anlegen(self):
    Version = self.env["x.md.document.version"].sudo()
    for record in self:
        content = record.content_md or ""
        next_version = record.current_version + 1
        md_att = self._md_datei_speichern(record, content, next_version)
        pdf_att = self._pdf_datei_speichern(record, next_version)
        Version.create({
            "document_id": record.id,
            "version": next_version,
            "content_md": content,
            "checksum": hashlib.md5(content.encode("utf-8")).hexdigest(),
            "changed_by": self.env.user.id,
            "changed_at": fields.Datetime.now(),
            "md_attachment_id": md_att.id,
            "pdf_attachment_id": pdf_att.id if pdf_att else False,
        })
```

### G.3 OWL-Komponente — Frontend-Initialisierung

Datei: `markdown_editor/static/src/js/markdown_editor.js`

Der folgende Ausschnitt zeigt die Lifecycle-Callbacks `onMounted` und `onWillUnmount` der OWL-Komponente. `onMounted` wird aufgerufen, sobald die Komponente ins DOM eingebaut wurde — erst dann existiert das DOM-Element, auf das CodeMirror zugreifen muss. Der Debounce-Mechanismus (300 ms) verhindert, dass bei schneller Eingabe bei jedem Tastenanschlag ein vollständiges Re-Render der Vorschau ausgelöst wird. `onWillUnmount` räumt die CodeMirror-Instanz und den offenen Timer auf, um Memory Leaks zu verhindern.

```javascript
onMounted(() => {
    if (!window.CodeMirror || !this.editorRef.el) return;

    this.cm = window.CodeMirror.fromTextArea(this.editorRef.el, {
        mode: "markdown",
        lineWrapping: true,
        lineNumbers: false,
        theme: "default",
        readOnly: this.props.readonly ? "nocursor" : false,
        autofocus: false,
        extraKeys: { Tab: false },
    });

    this.cm.setValue(this.state.value);

    this.cm.on("change", (cm) => {
        clearTimeout(this._debounce);
        this._debounce = setTimeout(() => this._updateState(cm.getValue()), 300);
    });
});

onWillUnmount(() => {
    clearTimeout(this._debounce);
    if (this.cm) {
        this.cm.toTextArea();
        this.cm = null;
    }
});
```

### G.4 Zugriffsschutz — ACL und Record Rules

**Datei: `markdown_editor/security/ir.model.access.csv`**

Die ACL-Datei definiert die CRUD-Berechtigungen auf Modellebene. Spalten: `perm_read`, `perm_write`, `perm_create`, `perm_unlink` (1 = erlaubt, 0 = verboten). Normale Benutzer haben auf dem Versionsmodell ausschließlich Leserecht (`1,0,0,0`) — das setzt den Append-only-Charakter der Versionierung technisch durch.

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_md_document_user,x_md_document_user,model_x_md_document,base.group_user,1,1,1,0
access_md_document_admin,x_md_document_admin,model_x_md_document,base.group_system,1,1,1,1
access_md_document_version_user,x_md_document_version_user,model_x_md_document_version,base.group_user,1,0,0,0
```

**Datei: `markdown_editor/security/markdown_editor_security.xml`**

Die Record Rules steuern den Zugriff auf Datensatzebene. Die Eigentümer-Regel filtert mit `[("owner_id", "=", user.id)]` — normale Benutzer sehen nur ihre eigenen Dokumente. Die Admin-Regel `[(1, "=", 1)]` ist immer wahr und gewährt Administratoren Zugriff auf alle Datensätze.

```xml
<record id="markdown_document_rule_owner_write" model="ir.rule">
    <field name="name">Markdown Dokument: Besitzer darf bearbeiten</field>
    <field name="model_id" ref="model_x_md_document"/>
    <field name="domain_force">[("owner_id", "=", user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="perm_read"   eval="1"/>
    <field name="perm_write"  eval="1"/>
    <field name="perm_create" eval="1"/>
    <field name="perm_unlink" eval="0"/>
</record>

<record id="markdown_document_rule_admin" model="ir.rule">
    <field name="name">Markdown Dokument: Admin Zugriff</field>
    <field name="model_id" ref="model_x_md_document"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('base.group_system'))]"/>
    <field name="perm_read"   eval="1"/>
    <field name="perm_write"  eval="1"/>
    <field name="perm_create" eval="1"/>
    <field name="perm_unlink" eval="1"/>
</record>
```

---

## Anhang H — Kundendokumentation

### H.1 Anmeldung und Navigation

Nach der Anmeldung in Odoo ist MDWriter über den Homescreen-Button „Markdown" erreichbar. Die Anwendung öffnet die Listenansicht aller eigenen Dokumente. Administratoren sehen alle Dokumente aller Benutzer.

### H.2 Dokument erstellen

Über den Button „Neu" in der Listenansicht wird ein neues Dokument angelegt. Es erscheint die Formularansicht mit dem Split-View-Editor. Im Feld „Titel" wird der Dokumentname eingetragen. Das Dokument wird nach dem ersten Speichern als Version 1 abgelegt.

### H.3 Dokument bearbeiten

Im linken Bereich des Split-Views wird der Markdown-Inhalt eingegeben. Die rechte Seite zeigt die formatierte Vorschau in Echtzeit. Der Editor unterstützt alle gängigen Markdown-Elemente: Überschriften (`#`, `##`), Listen (`-`, `1.`), Code-Blöcke (` ``` `), Tabellen, Fett (`**text**`), Kursiv (`*text*`) und Links (`[Text](URL)`).

### H.4 Dokument speichern

Das Dokument wird über den Speichern-Button oder über das Formular gespeichert. Bei jeder Speicherung mit geändertem Inhalt wird automatisch eine neue Version angelegt. Die aktuelle Versionsnummer ist im Formular sichtbar.

### H.5 PDF exportieren

Der Button „PDF exportieren" im Formular-Header erzeugt ein druckfertiges PDF-Dokument. Das PDF enthält einen Metadaten-Header (Titel, Eigentümer, Datum, Version) und den formatierten Markdown-Inhalt. Wurde für die aktuelle Version bereits ein PDF erzeugt, wird dieses wiederverwendet.

### H.6 Statusverwaltung

Dokumente können drei Zustände haben: **Entwurf** (Standard), **Veröffentlicht** und **Archiviert**. Der Status wird über Buttons in der Formularansicht geändert. Archivierte Dokumente erscheinen nicht in der Standard-Listenansicht, bleiben aber mit allen Versionen erhalten.

### H.7 Versionsvergleich

In der Versionshistorie (Tab „Versionen" im Formular) können zwei Versionen für einen Vergleich ausgewählt werden. Der Diff-Dialog zeigt Hinzufügungen (grün) und Löschungen (rot) zeilenweise an.

### H.8 Version wiederherstellen

In der Versionshistorie kann über den Button „Wiederherstellen" eine ältere Version als aktuellen Inhalt gesetzt werden. Dabei wird eine neue Version angelegt — die Wiederherstellung ist selbst versioniert und kann rückgängig gemacht werden.

### H.9 Dokumente suchen und filtern

Die Suchleiste in der Listenansicht ermöglicht die Suche nach Dokumenttitel. Über Filter kann nach Status (Entwurf, Veröffentlicht, Archiviert) gefiltert werden. Administratoren können zusätzlich nach Eigentümer filtern.
