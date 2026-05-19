# ==================================================================
# __init__.py — der Einstiegspunkt des Python-Pakets
# ==================================================================
# In Python signalisiert eine __init__.py-Datei: "Dieser Ordner ist
# ein Paket — du kannst Code daraus importieren."
# Ohne diese Datei würde Python den Ordner ignorieren.
#
# Hier steht nur eine Zeile: Odoo soll den Unterordner "models"
# ebenfalls als Paket einlesen. Dadurch werden alle Modelldateien
# automatisch geladen, wenn das Modul gestartet wird.
# ==================================================================

from . import models
# Der Punkt (.) bedeutet: Suche im gleichen Ordner wie diese Datei.
# "from . import models" = importiere den Ordner models/ aus diesem Paket
