# MDWriter — Markdown Editor für Odoo 19

MDWriter ist ein natives Odoo-19-Modul für zentrale, markdown-basierte technische Dokumentation direkt im ERP-System. Es ersetzt externe Wiki-Tools durch einen integrierten Split-View-Editor mit Live-Vorschau, automatischer Versionierung und PDF-Export.

---

## Features

- **Split-View-Editor** — Markdown links, Live-Vorschau rechts (CodeMirror + markdown-it)
- **Automatische Versionierung** — bei jeder Inhaltsänderung wird eine neue Version mit MD5-Prüfsumme angelegt
- **PDF-Export** — QWeb-Template + wkhtmltopdf, inkl. Metadaten-Header und Caching
- **Versionsvergleich** — farbiger Diff zweier Versionen (unified_diff)
- **Restore-Funktion** — ältere Version wiederherstellen erzeugt neue Version
- **Zugriffsschutz** — Odoo ACL + Record Rules: Benutzer sehen nur eigene Dokumente
- **Statusverwaltung** — Entwurf / Veröffentlicht / Archiviert
- **Dark-Mode-kompatibel** — über Odoo CSS Custom Properties
- **CDN-unabhängig** — alle JS-Bibliotheken liegen lokal im Modul

---

## Technologie-Stack

| Komponente | Technologie |
|---|---|
| Backend | Python 3.11+ / Odoo ORM |
| Frontend | JavaScript / OWL (Odoo Web Library) |
| Markdown (Frontend) | markdown-it 14 (lokal eingebunden) |
| Markdown (Backend) | mistune (Python, für PDF) |
| Editor | CodeMirror 5 |
| Styling | SCSS |
| Datenbank | PostgreSQL via Odoo ORM |
| PDF | wkhtmltopdf via QWeb |

---

## Modulstruktur

```
markdown_editor/
├── __manifest__.py
├── models/
│   ├── md_document.py          # x.md.document + x.md.document.version
│   └── md_document_diff.py     # x.md.document.diff.wizard (TransientModel)
├── views/
│   ├── md_document_views.xml
│   └── md_document_diff_views.xml
├── static/
│   ├── description/icon.png
│   ├── lib/                    # markdown-it.min.js, CodeMirror (lokal)
│   └── src/
│       ├── js/markdown_editor.js       # OWL-Komponente MarkdownField
│       ├── xml/markdown_editor_templates.xml
│       └── scss/                       # Split-View, Branding, PDF-Styling
├── security/
│   ├── ir.model.access.csv
│   └── markdown_editor_security.xml
├── report/
│   └── md_document_report.xml
├── demo/
│   └── demo_documents.xml
└── tests/
    └── test_md_document.py
```

---

## Datenmodell

**`x.md.document`** — Hauptdokument (dauerhaft gespeichert)

| Feld | Typ | Beschreibung |
|---|---|---|
| `name` | Char | Titel (required) |
| `content_md` | Text | Markdown-Inhalt |
| `content_html` | Html | Gerendertes HTML (computed, für PDF-Export) |
| `state` | Selection | draft / published / archived |
| `owner_id` | Many2one → res.users | Eigentümer (default: aktueller User) |
| `version_ids` | One2many → x.md.document.version | Alle Versionen |
| `current_version` | Integer | Computed: höchste Versionsnummer |

**`x.md.document.version`** — Versionshistorie (append-only)

| Feld | Typ | Beschreibung |
|---|---|---|
| `document_id` | Many2one → x.md.document | Verweis auf Dokument |
| `version` | Integer | Versionsnummer |
| `content_md` | Text | Markdown-Inhalt dieser Version |
| `checksum` | Char | MD5-Hash |
| `changed_by` | Many2one → res.users | Wer hat geändert |
| `changed_at` | Datetime | Wann |
| `md_attachment_id` | Many2one → ir.attachment | .md-Datei |
| `pdf_attachment_id` | Many2one → ir.attachment | .pdf-Datei |

Versionierung wird ausgelöst durch `create()` und durch `write()` auf `content_md`. Andere Schreiboperationen (z. B. Statuswechsel) erzeugen keine neue Version.

---

## Sicherheitskonzept

Zwei komplementäre Mechanismen:

**ACL (`security/ir.model.access.csv`)** — Modellzugriff:
- Normale Benutzer: Dokumente lesen/schreiben/erstellen, kein Löschen
- Normale Benutzer: Versionen nur lesen (kein create/write/unlink → Append-only erzwungen)
- Admins: volle CRUD-Rechte auf allen Modellen

**Record Rules (`security/markdown_editor_security.xml`)** — Datensatzzugriff:
- Eigentümer-Regel: `[("owner_id", "=", user.id)]` — Benutzer sehen nur eigene Dokumente
- Admin-Regel: `[(1, "=", 1)]` — Admins sehen alle Dokumente

**XSS-Schutz:** markdown-it mit `html: false` im Frontend; mistune im Backend ohne schädliches HTML-Rendering.

---

## Installation

**Voraussetzungen:**
- Odoo 19 (Community oder Enterprise)
- Python-Abhängigkeit: `mistune` (via `requirements.txt`)
- Systemabhängigkeit: `wkhtmltopdf` für PDF-Export

**Odoo-Abhängigkeiten** (`__manifest__.py`):
```python
"depends": ["base", "web", "documents"],
```

`documents` ist die Odoo-Documents-App (Enterprise). Bei fehlendem Modul läuft MDWriter ohne Documents-Integration weiter.

**Deployment auf Odoo.sh:**
1. Repo als Branch verknüpfen
2. `mistune` wird automatisch aus `requirements.txt` installiert
3. Modul in Odoo aktivieren: Einstellungen → Apps → MDWriter installieren

**Lokales Deployment:**
```bash
./odoo-bin -d <db> -u markdown_editor --stop-after-init
```

---

## Tests ausführen

```bash
./odoo-bin -d <datenbankname> --test-enable -u markdown_editor --stop-after-init
```

Testsuite: `markdown_editor/tests/test_md_document.py`

| Klasse | Tests | Abdeckung |
|---|---|---|
| TestMdDocumentVersioning | 3 | create, write, restore |
| TestMdDocumentACL | 3 | owner read, blocked user, version readonly |
| TestMdDocumentDiff | 1 | additions/deletions im Diff-HTML |

Ergebnis auf Odoo.sh: `0 failed, 0 error(s) of 7 tests`

---

## Kontext

Ausbildungsprojekt IHK Rhein-Neckar — Fachinformatiker Anwendungsentwicklung
Autor: Timo Giese | Ausbildungsbetrieb: TrendTec UG, Edingen-Neckarhausen
Bearbeitungszeitraum: Mai 2026 | Gesamtaufwand: 80 Stunden
