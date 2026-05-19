# ==================================================================
# __manifest__.py — Das "Ausweisdokument" des Odoo-Moduls
# ==================================================================
# Odoo liest diese Datei beim Installieren und erfährt damit:
#   - Wie das Modul heißt und wer es gebaut hat
#   - Welche anderen Module es braucht (depends)
#   - Welche Dateien beim Installieren geladen werden (data)
#   - Welche Browser-Dateien eingebunden werden (assets)
# ==================================================================
{
    "name": "Markdown Editor",
    "summary": "Markdown‑basierter Editor mit Live‑Vorschau und Versionierung",
    "version": "19.0.1.1",   # Format: Odoo-Version.Major.Minor.Patch
    "author": "Timo",
    "maintainers": ["Timo"],
    "website": "https://github.com/fiaTG/MDWriter",
    "license": "LGPL-3",
    "category": "Productivity",
    "images": ["static/description/icon.png"],  # Icon das im Odoo App-Store angezeigt wird

    # depends: Diese Odoo-Module müssen bereits installiert sein, bevor unser
    # Modul installiert werden kann. Odoo prüft das automatisch.
    "depends": [
        "base",       # Grundmodul: enthält User, Firmen, Gruppen, Anhänge (ir.attachment)
        "web",        # Frontend-Framework: OWL-Komponenten, Asset-Bundles
        "documents",  # Odoo Documents-App: für die automatische Dateiablage je Version
    ],

    # data: Diese Dateien werden beim Installieren UND bei jedem Modul-Update geladen.
    # Reihenfolge ist wichtig — Security muss immer VOR den Views stehen!
    "data": [
        "security/ir.model.access.csv",          # Wer darf welche Aktionen auf welchem Modell
        "security/markdown_editor_security.xml", # Zeilenrechte: User sehen nur ihre eigenen Dokumente
        "views/md_document_views.xml",           # Formulare, Listen, Suche, Menüeintrag
        "views/md_document_diff_views.xml",      # Diff-Wizard-Dialog (Versionen vergleichen)
        "report/md_document_report.xml",         # PDF-Report: Template + Aktion
    ],

    # assets: Browser-seitige Dateien (JavaScript, CSS, XML-Templates).
    # web.assets_backend → wird im Odoo-Backend geladen (nach dem Login).
    # web.report_assets_common → wird beim PDF-Erstellen durch wkhtmltopdf geladen.
    "assets": {
        "web.assets_backend": [
            "markdown_editor/static/lib/markdown-it.min.js",           # Externe Lib: wandelt Markdown in HTML um
            "markdown_editor/static/lib/codemirror/codemirror.min.js", # Externe Lib: Syntax-hervorhebender Code-Editor
            "markdown_editor/static/lib/codemirror/markdown.min.js",   # Erweiterung: Markdown-Modus für CodeMirror
            "markdown_editor/static/lib/codemirror/codemirror.min.css",
            "markdown_editor/static/src/js/markdown_editor.js",                   # Unsere OWL-Komponente (Editor + Vorschau)
            "markdown_editor/static/src/xml/markdown_editor_templates.xml",       # HTML-Struktur der Komponente
            "markdown_editor/static/src/scss/markdown_editor.scss",               # Haupt-Styling (Farben, Layout)
            "markdown_editor/static/src/scss/codemirror_theme.scss",              # Editor-Farbschema
        ],
        "web.report_assets_common": [
            "markdown_editor/static/src/scss/md_document_report.scss",  # PDF-spezifisches Styling
        ],
    },

    # demo: Diese Dateien werden NUR bei Instanzen mit Demo-Daten geladen
    # (z.B. frische Odoo.sh-Entwicklungsinstanz). Sie legen Beispiel-Dokumente
    # an, damit man das Modul sofort mit echten Inhalten testen kann.
    "demo": [
        "demo/demo_documents.xml",
    ],

    "installable": True,   # Modul erscheint im Odoo App-Menü und kann installiert werden
    "application": True,   # Zeigt einen eigenen Eintrag im Homescreen (eigene App, nicht nur Erweiterung)
    "auto_install": True,  # Wird automatisch installiert, sobald alle depends-Module vorhanden sind
}
