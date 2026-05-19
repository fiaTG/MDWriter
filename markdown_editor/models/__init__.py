# ==================================================================
# models/__init__.py — lädt alle Modelldateien dieses Ordners
# ==================================================================
# Wie im übergeordneten __init__.py erklärt: diese Datei macht den
# Ordner zum Python-Paket und listet alle Module (= Dateien) auf,
# die Odoo beim Start einlesen soll.
#
# Reihenfolge ist wichtig: md_document muss VOR md_document_diff
# geladen werden, weil der Diff-Wizard das Hauptmodell referenziert.
# ==================================================================

from . import md_document       # Hauptmodell: Dokument + Version
from . import md_document_diff  # Wizard: Versionsvergleich (Diff)
