# ==================================================================
# md_document.py — das Herzstück des Moduls
# ==================================================================
# Hier werden zwei Datenbankmodelle definiert:
#   1. XMdDocument       → die Dokument-Tabelle
#   2. XMdDocumentVersion → die Versions-Tabelle
#
# Ein "Modell" in Odoo ist eine Python-Klasse, die Odoo automatisch
# in eine Datenbanktabelle umwandelt. Felder der Klasse werden Spalten
# in PostgreSQL. Methoden der Klasse werden zu Geschäftslogik.
# ==================================================================

# ------------------------------------------------------------------
# Standard-Bibliotheken aus Python (immer verfügbar, kein Install)
# ------------------------------------------------------------------
import base64    # kodiert Binärdaten (z.B. PDF-Bytes) in Text für die Datenbank
import hashlib   # erzeugt Prüfsummen (MD5) — "Fingerabdruck" eines Textes
import logging   # schreibt Lognachrichten in die Odoo-Konsole

# ------------------------------------------------------------------
# Optionaler Import: mistune (Python-Markdown-Parser)
# ------------------------------------------------------------------
# try/except ImportError: Wenn das Paket nicht installiert ist,
# schlägt der Import fehl — anstatt das Modul komplett zu crashen,
# fangen wir den Fehler ab und merken uns, dass mistune fehlt.
# Im Betrieb auf Odoo.sh ist mistune installiert; lokal eventuell nicht.
# ------------------------------------------------------------------
try:
    import mistune
    _mistune_available = True
except ImportError:
    _mistune_available = False

# ==================================================================
# Demo-Inhalt: Textkonstanten für die Beispieldokumente
# ==================================================================
# _DEMO_* sind Modul-level-Konstanten (kein "self", keine Klasse).
# Sie werden nur beim Laden von Demo-Daten verwendet.
# Das dreifache Anführungszeichen """ erlaubt mehrzeiligen Text.
# ==================================================================

_DEMO_SHOWCASE = """\
# MDWriter — Markdown-Referenz

Diese Datei demonstriert alle unterstützten Markdown-Elemente in der Live-Vorschau.

---

## Textformatierung

Normaler Fließtext mit **fettem Text**, *kursivem Text* und ~~durchgestrichenem Text~~.

Inline-Code: `const result = compute(42);`

Ein [Link zur Projektseite](https://github.com/fiaTG/MDWriter_mvp) erscheint dunkelgrün.

---

## Code-Block

```python
def berechne_checksumme(inhalt: str) -> str:
    import hashlib
    return hashlib.md5(inhalt.encode()).hexdigest()
```

```javascript
// OWL-Komponente — Live-Vorschau initialisieren
onMounted(() => {
    this.editor = CodeMirror.fromTextArea(this.textareaRef.el, {
        mode: "markdown",
        lineWrapping: true,
    });
});
```

---

## Tabelle

| Feature           | Technologie      | Status        |
|-------------------|------------------|---------------|
| Editor Split-View | CodeMirror + OWL | Implementiert |
| Live-Vorschau     | markdown-it      | Implementiert |
| Versionierung     | Odoo ORM         | Implementiert |
| PDF-Export        | QWeb + mistune   | Implementiert |
| Diff-Ansicht      | unified_diff     | Implementiert |
| ACL & Record Rules| Odoo Security    | Implementiert |

---

## Listen

**Implementierte Features:**
- Markdown-Editor mit Syntax-Highlighting
- Echtzeit-Vorschau (Split-View)
- Automatische Versionierung bei jeder Speicherung
- Diff-Vergleich zwischen beliebigen Versionen
- Restore-Funktion für ältere Versionen
- PDF-Export per Knopfdruck

**Entwicklungsreihenfolge:**
1. Datenmodell und ORM definieren
2. Security (ACL + Record Rules) konfigurieren
3. OWL-Komponente entwickeln
4. Versionierung implementieren
5. PDF-Report mit QWeb erstellen
6. Tests schreiben und auf Odoo.sh validieren

---

## Blockquote

> „MDWriter ersetzt externe Dokumentationstools durch eine native Odoo-Integration —
> technische Dokumentation bleibt im selben System wie die Geschäftsdaten."

---

## Horizontale Linie

Oberhalb der Linie.

---

Unterhalb der Linie.
"""

_DEMO_INSTALL_V1 = """\
# Installationsanleitung: MDWriter

## Voraussetzungen

- Odoo 19 Community oder Enterprise
- Python 3.11+
"""

_DEMO_INSTALL_V2 = """\
# Installationsanleitung: MDWriter

## Voraussetzungen

- Odoo 19 Community oder Enterprise
- Python 3.11+
- wkhtmltopdf (für PDF-Export)
- mistune (Python-Paket: `pip install mistune`)

## Installation

1. Repository klonen:
   `git clone https://github.com/fiaTG/MDWriter_mvp.git`
2. Verzeichnis `markdown_editor` in den Odoo-Addons-Pfad legen.
3. Modul in Odoo unter *Einstellungen → Module* aktivieren.
"""

_DEMO_INSTALL_V3 = """\
# Installationsanleitung: MDWriter

## Voraussetzungen

- Odoo 19 Community oder Enterprise
- Python 3.11+
- wkhtmltopdf (für PDF-Export)
- mistune (Python-Paket: `pip install mistune`)

## Installation

1. Repository klonen:
   `git clone https://github.com/fiaTG/MDWriter_mvp.git`
2. Verzeichnis `markdown_editor` in den Odoo-Addons-Pfad legen.
3. Modul in Odoo unter *Einstellungen → Module* aktivieren.

## Deployment auf Odoo.sh

Das Modul wird automatisch erkannt und installiert, wenn es im
GitHub-Repository liegt und die Branch mit dem Odoo.sh-Projekt verknüpft ist.

```
git push mvp main
```

## Fehlerbehebung

| Problem               | Lösung                                       |
|-----------------------|----------------------------------------------|
| PDF-Export fehlt      | `wkhtmltopdf` installieren, Dienst neu starten |
| Vorschau leer         | `mistune` via pip nachinstallieren           |
| Modul nicht sichtbar  | Addons-Pfad in `odoo.conf` prüfen           |
"""

_DEMO_RELEASE_NOTES = """\
# Release Notes: MDWriter v1.0

**Datum:** Mai 2026
**Autor:** Timo Giese, TrendTec UG

---

## Neue Features

- **Markdown-Editor** mit Split-View (Editor links, Vorschau rechts)
- **Live-Vorschau** auf Basis von markdown-it
- **Automatische Versionierung** bei jeder Inhaltsänderung
- **Diff-Ansicht** — farbiger Vergleich beliebiger Versionen
- **Restore-Funktion** — Ältere Version wiederherstellen
- **PDF-Export** — Dokument als PDF herunterladen
- **ACL & Record Rules** — Nutzer sehen ausschließlich eigene Dokumente
- **Statusübergänge** — Entwurf → Veröffentlicht → Archiviert

---

## Technischer Stack

| Komponente    | Technologie           |
|---------------|-----------------------|
| Backend       | Odoo 19, Python 3.11  |
| Frontend      | OWL, CodeMirror       |
| Markdown      | markdown-it           |
| PDF-Rendering | mistune + QWeb        |
| Datenbank     | PostgreSQL (Odoo ORM) |

---

## Bekannte Einschränkungen

- Performance bei Dokumenten > 10.000 Zeilen nicht optimiert.
- Keine kollaborative Echtzeit-Bearbeitung.
"""

# ------------------------------------------------------------------
# Odoo-Imports
# ------------------------------------------------------------------
# Markup: kennzeichnet einen String als "sicheres HTML" — Odoo rendert
#   ihn direkt im Browser, ohne nochmal zu escapen. Wichtig: Markup()
#   nur verwenden, wenn der Inhalt wirklich sicher ist (kein User-Input!).
# api:    Dekoratoren für Methoden (@api.depends, @api.model, ...)
# fields: Feldtypen für Datenbank-Spalten
# models: Basisklassen für Datenbankmodelle
# ------------------------------------------------------------------
from markupsafe import Markup
from odoo import api, fields, models

# _logger: Modul-spezifischer Logger. __name__ ist der Dateiname ("md_document").
# Verwendung: _logger.warning("...") → erscheint in der Odoo-Konsole als WARNING.
_logger = logging.getLogger(__name__)


# ==================================================================
# Klasse XMdDocument — das Hauptmodell "Markdown-Dokument"
# ==================================================================
# class XMdDocument(models.Model):
#   → "XMdDocument erbt von models.Model"
#   → models.Model ist die Odoo-Basisklasse für persistente DB-Tabellen
#   → Odoo liest _name und erstellt daraus die Tabelle "x_md_document"
#
# Was ist "self"?
#   In jeder Methode einer Klasse ist "self" der Verweis auf das
#   aktuelle Objekt (die aktuelle Instanz). In Odoo ist "self" ein
#   Recordset — es kann einen oder mehrere Datenbankeinträge enthalten.
#   Beispiel: doc = self.env["x.md.document"].search([])
#   Dann ist "doc" ein Recordset aller Dokumente.
#   Mit "for record in doc:" iteriert man über jeden einzelnen Eintrag.
# ==================================================================
class XMdDocument(models.Model):
    _name = "x.md.document"          # technischer Name → DB-Tabelle x_md_document
    _description = "Markdown Document"  # lesbare Beschreibung (erscheint im Odoo-Backend)

    # ------------------------------------------------------------------
    # Felder = Datenbankspalten
    # ------------------------------------------------------------------
    # fields.Char  → kurzer Text (VARCHAR in PostgreSQL), ideal für Titel
    # fields.Text  → langer Text (TEXT), ideal für Markdown-Inhalt
    # fields.Integer → ganze Zahl
    # fields.Selection → Dropdown mit festen Werten (ENUM-ähnlich)
    # fields.Many2one  → Fremdschlüssel: "dieser Datensatz gehört zu einem anderen"
    #                    comodel_name gibt die Ziel-Tabelle an
    # fields.One2many  → Gegenteil: "dieser Datensatz hat viele andere"
    #                    inverse_name ist der Many2one-Feldname auf der anderen Seite
    # fields.Html      → HTML-Text (wird im Browser gerendert)
    #
    # required=True: Darf nicht leer sein (NOT NULL in SQL)
    # string="..."  : Anzeigename im Odoo-UI (nicht der technische Name)
    # default=...   : Standardwert beim Anlegen eines neuen Eintrags
    # store=True    : computed field wird in der DB gespeichert (für Suche/Sort)
    # sanitize=False: Odoo soll den HTML-Inhalt NICHT nochmal bereinigen
    #                 (wir machen das selbst mit Markup())
    # ------------------------------------------------------------------

    name = fields.Char(string="Titel", required=True)
    content_md = fields.Text(string="Markdown‑Inhalt")
    state = fields.Selection([
        ("draft", "Entwurf"),
        ("published", "Veröffentlicht"),
        ("archived", "Archiviert"),
    ], default="draft")
    owner_id = fields.Many2one(
        comodel_name="res.users",
        string="Eigentümer",
        default=lambda self: self.env.user,
        # lambda: eine anonyme Einzeiler-Funktion.
        # self.env.user = der aktuell angemeldete Odoo-Nutzer.
        # Der Eigentümer wird beim Erstellen automatisch auf den Ersteller gesetzt.
    )
    version_ids = fields.One2many(
        comodel_name="x.md.document.version",
        inverse_name="document_id",  # Feldname des Many2one in XMdDocumentVersion
        string="Versionen",
    )
    current_version = fields.Integer(
        string="Aktuelle Version",
        compute="_aktuelle_version_berechnen",  # wird durch eine Methode berechnet
        store=True,   # Wert wird in der DB gespeichert, damit er sortierbar ist
    )
    content_html = fields.Html(
        string="HTML-Vorschau",
        compute="_html_vorschau_berechnen",
        sanitize=False,  # Markup()-Kennzeichnung würde durch sanitize=True verloren gehen
    )

    # ------------------------------------------------------------------
    # @api.depends — der "Beobachter"-Dekorator
    # ------------------------------------------------------------------
    # @api.depends("version_ids.version") sagt Odoo:
    #   "Immer wenn sich das Feld 'version' in einer zugehörigen Version ändert,
    #    ruf diese Methode neu auf und aktualisiere current_version."
    # Ohne diesen Dekorator würde Odoo nicht wissen, wann neu berechnet werden soll.
    # ------------------------------------------------------------------
    @api.depends("version_ids.version")
    def _aktuelle_version_berechnen(self):
        # "for doc in self:" — Odoo-Methoden arbeiten immer auf Recordsets.
        # Ein Recordset kann 1 oder N Dokumente enthalten.
        # Die Schleife stellt sicher, dass jeder Datensatz einzeln behandelt wird.
        for doc in self:
            # max(..., default=0): höchste Versionsnummer aller Versionen.
            # mapped("version") gibt eine Liste aller version-Felder zurück.
            # Falls keine Versionen vorhanden → default=0
            doc.current_version = max(doc.version_ids.mapped("version"), default=0)

    def _markdown_zu_html(self, text):
        # Wandelt Markdown-Text in sicheres HTML um.
        # Markup() aus markupsafe kennzeichnet den String als vertrauenswürdig —
        # Odoo rendert ihn direkt im Browser, ohne nochmal zu escapen.
        # WICHTIG: Markup() nie auf User-Input anwenden, der nicht bereinigt wurde!
        if _mistune_available:
            return Markup(mistune.html(text))
        # Fallback: kein mistune → Text in <pre> einwickeln (plain text, sicher)
        _logger.warning("mistune nicht installiert — Fallback auf Plaintext-Darstellung")
        return Markup("<pre>%s</pre>") % text
        # Das % hier ist kein Modulo — Markup() überschreibt %-Formatting
        # und escaped dabei text automatisch (XSS-Schutz).

    @api.depends("content_md")
    def _html_vorschau_berechnen(self):
        # Wird bei jeder Änderung von content_md neu berechnet.
        for doc in self:
            doc.content_html = self._markdown_zu_html(doc.content_md) if doc.content_md else ""

    # ------------------------------------------------------------------
    # Attachment-Methoden — erzeugen Dateien pro Version
    # ------------------------------------------------------------------
    # ir.attachment ist das Odoo-Modell für Dateianhänge.
    # Jede Version bekommt eine .md-Datei und eine .pdf-Datei als Anhang.
    #
    # sudo() — "Super User do":
    #   Umgeht temporär die ACL-Prüfung und führt die Aktion als Administrator aus.
    #   Nötig, weil normale User keine ir.attachment-Einträge direkt anlegen dürfen.
    #   sudo() so gezielt wie möglich einsetzen — nie pauschal für alles!
    # ------------------------------------------------------------------
    def _md_datei_speichern(self, record, content, version_num):
        # base64.b64encode: kodiert Text-Bytes in Base64-Format.
        # Odoo speichert Dateiinhalte als Base64-String in der Datenbank.
        encoded = base64.b64encode(content.encode("utf-8"))
        attachment = self.env["ir.attachment"].sudo().create({
            "name": f"{record.name}_v{version_num}.md",  # f-String: Variable in String einbetten
            "datas": encoded,
            "mimetype": "text/markdown",
            "res_model": record._name,  # _name = "x.md.document" → verknüpft Anhang mit Dokument
            "res_id": record.id,        # ID des Datensatzes, dem der Anhang gehört
        })
        self._in_documents_ablegen(attachment, encoded)
        return attachment

    def _pdf_datei_speichern(self, record, version_num):
        # skip_pdf_attachment: Context-Flag, das beim Laden von Demo-Daten gesetzt wird.
        # self.env.context ist ein dict mit Zusatz-Informationen für die aktuelle Operation.
        # Demo-Daten: PDF überspringen, weil wkhtmltopdf auf Odoo.sh dabei Warnungen erzeugt.
        if self.env.context.get("skip_pdf_attachment"):
            return False
        try:
            # env.ref("...") sucht einen Datensatz anhand seiner XML-ID.
            # raise_if_not_found=False: kein Fehler wenn nicht gefunden, nur None zurück.
            report = self.env.ref("markdown_editor.md_document_pdf", raise_if_not_found=False)
            if not report:
                return False
            # _render_qweb_pdf: Rendert das QWeb-Template als PDF via wkhtmltopdf.
            # Gibt PDF-Bytes und Content-Type zurück (wir brauchen nur die Bytes).
            pdf_bytes, _ = self.env["ir.actions.report"]._render_qweb_pdf(
                "markdown_editor.md_document_pdf", res_ids=[record.id]
            )
            return self.env["ir.attachment"].sudo().create({
                "name": f"{record.name}_v{version_num}.pdf",
                "datas": base64.b64encode(pdf_bytes),
                "mimetype": "application/pdf",
                "res_model": record._name,
                "res_id": record.id,
            })
        except Exception as e:
            # Wenn PDF-Generierung scheitert (z.B. wkhtmltopdf fehlt):
            # Warnung loggen, aber die Versionierung NICHT abbrechen — robustes Verhalten.
            _logger.warning("PDF render failed for record %s v%s: %s", record.id, version_num, e)
            return False

    def _documents_ordner_holen(self):
        # Gibt den Odoo-Documents-Ordner "Markdown Dokumente" zurück
        # oder legt ihn an, falls er noch nicht existiert.
        # "documents.document" ist das Modell der Odoo Documents-App.
        try:
            Doc = self.env["documents.document"].sudo()
            folder = Doc.search([("name", "=", "Markdown Dokumente"), ("type", "=", "folder")], limit=1)
            # search() gibt ein Recordset zurück. limit=1 → maximal 1 Ergebnis.
            # "or"-Logik: folder if folder exists, else create new one
            return folder or Doc.create({"name": "Markdown Dokumente", "type": "folder"})
        except Exception as e:
            _logger.warning("MDWriter: Ordner konnte nicht angelegt werden: %s", e)
            return None

    def _in_documents_ablegen(self, attachment, datas):
        # Legt die .md-Datei zusätzlich in der Odoo Documents-App ab.
        # "if ... not in self.env": prüft ob das Modell überhaupt geladen ist.
        # Falls documents-Modul nicht installiert → stillschweigend überspringen.
        if "documents.document" not in self.env:
            return
        try:
            folder = self._documents_ordner_holen()
            if not folder:
                return
            self.env["documents.document"].sudo().create({
                "name": attachment.name,
                "folder_id": folder.id,  # Many2one → Zeiger auf den Ordner
                "datas": datas,
                "mimetype": attachment.mimetype,
                "type": "binary",        # "binary" = Dateiinhalt (kein Link, kein URL)
            })
        except Exception as e:
            _logger.warning("MDWriter: documents.document konnte nicht erstellt werden: %s", e)

    def _version_anlegen(self):
        # Erzeugt für jeden Datensatz in self eine neue Version.
        # sudo() nötig: normale User dürfen keine Versions-Records direkt anlegen (ACL)
        Version = self.env["x.md.document.version"].sudo()
        for record in self:
            content = record.content_md or ""
            next_version = record.current_version + 1
            md_att = self._md_datei_speichern(record, content, next_version)
            pdf_att = self._pdf_datei_speichern(record, next_version)
            # hashlib.md5(...).hexdigest():
            #   Erzeugt einen 32-Zeichen-Hex-String ("Fingerabdruck") des Inhalts.
            #   Gleicher Text → gleiche Checksumme. Nützlich zum Erkennen von Änderungen.
            Version.create({
                "document_id": record.id,
                "version": next_version,
                "content_md": content,
                "checksum": hashlib.md5(content.encode("utf-8")).hexdigest(),
                "changed_by": self.env.user.id,
                "changed_at": fields.Datetime.now(),  # aktueller Zeitstempel (UTC)
                "md_attachment_id": md_att.id,
                "pdf_attachment_id": pdf_att.id if pdf_att else False,
                # False statt None: Odoo verwendet False für leere Many2one-Felder
            })

    # ------------------------------------------------------------------
    # Statusübergangs-Methoden — aufgerufen durch Buttons in der View
    # ------------------------------------------------------------------
    # Diese Methoden ändern nur das state-Feld.
    # self.write({...}) speichert die Werte in der Datenbank.
    # write() kennt self automatisch aus dem Kontext (welcher Button geklickt wurde).
    # ------------------------------------------------------------------
    def aktion_als_entwurf(self):
        self.write({"state": "draft"})

    def aktion_veroeffentlichen(self):
        self.write({"state": "published"})

    def aktion_archivieren(self):
        self.write({"state": "archived"})

    def aktion_pdf_exportieren(self):
        # ensure_one(): wirft einen Fehler, wenn self mehr als 1 Datensatz enthält.
        # Nötig weil ein PDF-Export immer genau ein Dokument betrifft.
        self.ensure_one()
        latest = self.version_ids[:1]  # [:1] = erste Version (höchste, wegen _order="version desc")
        if latest and latest.pdf_attachment_id:
            # ir.actions.act_url: Browser-Aktion — öffnet eine URL.
            # target="new": in einem neuen Tab öffnen.
            # /web/content/...: Odoo-Standard-URL für Dateidownloads
            return {
                "type": "ir.actions.act_url",
                "url": f"/web/content/{latest.pdf_attachment_id.id}?download=true",
                "target": "new",
            }
        # Fallback: kein vorbereitetes PDF → live via QWeb rendern
        return self.env.ref("markdown_editor.md_document_pdf").report_action(self)

    def aktion_md_herunterladen(self):
        self.ensure_one()
        latest = self.version_ids[:1]
        if not latest or not latest.md_attachment_id:
            return False
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{latest.md_attachment_id.id}?download=true",
            "target": "new",
        }

    def aktion_diff_anzeigen(self):
        # Öffnet den Diff-Wizard als Popup-Formular (target="new").
        # context: Startwerte für den Wizard — document_id wird vorbelegt.
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "x.md.document.diff.wizard",
            "view_mode": "form",
            "target": "new",
            "res_id": False,  # Immer neuen Wizard anlegen (verhindert Odoo-seitiges Caching)
            "context": {"default_document_id": self.id},
        }

    # ------------------------------------------------------------------
    # ORM-Overrides: create() und write()
    # ------------------------------------------------------------------
    # Odoo ruft create() beim Anlegen und write() beim Speichern auf.
    # Wir überschreiben sie (override), um nach jeder Aktion automatisch
    # eine neue Version zu erzeugen.
    #
    # @api.model_create_multi:
    #   Erlaubt, mehrere Datensätze auf einmal zu erstellen.
    #   vals_list ist eine Liste von dicts, z.B.:
    #   [{"name": "Dok A", "content_md": "..."}, {"name": "Dok B", ...}]
    #
    # super().create(vals_list):
    #   Ruft die originale Odoo-create()-Methode auf (ohne unsere Erweiterung).
    #   "super()" bedeutet "die Elternklasse" — also models.Model.
    #   Erst speichern wir in die DB, dann legen wir die Version an.
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._version_anlegen()
        return records

    def write(self, vals):
        # vals ist ein dict der geänderten Felder, z.B. {"content_md": "# Neu"}
        # Nur wenn content_md geändert wurde, eine neue Version anlegen.
        # Statusänderungen (state) sollen keine neue Version erzeugen.
        res = super().write(vals)
        if "content_md" in vals:
            self._version_anlegen()
        return res

    # ------------------------------------------------------------------
    # Demo-Daten: wird von demo/demo_documents.xml aufgerufen
    # ------------------------------------------------------------------
    # @api.model: Methode gehört zum Modell (nicht zu einem konkreten Datensatz).
    #   Es gibt kein "self als Datensatz" hier — self ist das Modell selbst.
    #   Vergleichbar mit @staticmethod, aber mit Zugriff auf self.env.
    # ------------------------------------------------------------------
    @api.model
    def _demo_dokumente_anlegen(self):
        """Legt Beispieldokumente für Demo-Instanzen an. Wird nur aus demo/demo_documents.xml aufgerufen."""
        try:
            # with_context(): fügt dem aktuellen Kontext ein Flag hinzu.
            # skip_pdf_attachment=True: verhindert PDF-Generierung (vermeidet Warnungen)
            self = self.with_context(skip_pdf_attachment=True)
            self.create({"name": "MDWriter — Markdown-Referenz", "content_md": _DEMO_SHOWCASE, "state": "published"})

            # 3 Versionen erzeugen: V1 → V2 → V3 (für die Diff-Demo in der Präsentation)
            doc_install = self.create({"name": "Installationsanleitung: MDWriter", "content_md": _DEMO_INSTALL_V1})
            doc_install.write({"content_md": _DEMO_INSTALL_V2})
            doc_install.write({"content_md": _DEMO_INSTALL_V3})
            doc_install.write({"state": "published"})

            # Release Notes bleibt als Entwurf — zeigt state=draft im Demo
            self.create({"name": "Release Notes: MDWriter v1.0", "content_md": _DEMO_RELEASE_NOTES})
        except Exception:
            # _logger.exception: loggt den Fehler inkl. vollständigem Stack-Trace
            _logger.exception("MDWriter: Demo-Daten konnten nicht angelegt werden.")


# ==================================================================
# Klasse XMdDocumentVersion — Versionsmodell (append-only)
# ==================================================================
# Append-only bedeutet: Versionen werden nur angelegt, nie geändert.
# Das garantiert einen lückenlosen Audittrail.
#
# _order = "version desc": Standardsortierung — neueste Version zuerst.
# Damit ist self.version_ids[:1] immer die aktuellste Version.
# ==================================================================
class XMdDocumentVersion(models.Model):
    _name = "x.md.document.version"
    _description = "Markdown Document Version"
    _order = "version desc"

    document_id = fields.Many2one(
        comodel_name="x.md.document",
        string="Dokument",
        required=True,
        ondelete="cascade",
        # ondelete="cascade": wenn das Dokument gelöscht wird,
        # werden automatisch alle zugehörigen Versionen mitgelöscht.
    )
    version = fields.Integer(string="Version", required=True)
    content_md = fields.Text(string="Markdown‑Inhalt")
    checksum = fields.Char(string="Checksumme", size=32)  # 32 Zeichen = MD5-Hex-String
    changed_by = fields.Many2one(comodel_name="res.users", string="Geändert von")
    changed_at = fields.Datetime(string="Geändert am")
    md_attachment_id = fields.Many2one(comodel_name="ir.attachment", string="Markdown‑Anhang")
    pdf_attachment_id = fields.Many2one(comodel_name="ir.attachment", string="PDF‑Anhang")

    def aktion_wiederherstellen(self):
        # ensure_one(): Restore macht nur Sinn für genau eine Version.
        self.ensure_one()
        # write() auf dem Dokument löst automatisch create() für eine neue Version aus —
        # die alten Versionen bleiben erhalten. Kein Datenverlust.
        self.document_id.write({"content_md": self.content_md})
        # Nach dem Restore zum Dokument zurücknavigieren
        return {
            "type": "ir.actions.act_window",
            "res_model": "x.md.document",
            "res_id": self.document_id.id,
            "view_mode": "form",
            "target": "current",  # "current" = aktuelles Fenster ersetzen (kein Popup)
        }
