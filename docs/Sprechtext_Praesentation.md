# Sprechtext — IHK-Präsentation MDWriter

> Wort-für-Wort-Vortragstext für die ca. 8-minütige Präsentation (11 Folien),
> danach Live-Demo (siehe Demo-Spickzettel). Locker sprechen, nicht ablesen —
> der Text ist als Stütze gedacht, nicht zum Vorlesen.

---

## Folie 1 — Titel

Guten Tag. Mein Name ist Timo Giese, ich bin Auszubildender zum Fachinformatiker für Anwendungsentwicklung bei der TrendTec UG. Ich stelle Ihnen heute mein Abschlussprojekt vor: **MDWriter** — eine zentrale Dokumentationslösung auf Markdown-Basis, die direkt in Odoo läuft. Die Präsentation dauert etwa acht Minuten, im Anschluss zeige ich Ihnen das Modul live.

## Folie 2 — Gliederung

Ich gehe dabei den Weg entlang der Projektphasen: von der Analyse über den Entwurf und die Implementierung bis zu Test und Fazit. Ganz am Ende folgt die Live-Demo.

## Folie 3 — Das Problem

Fangen wir beim Problem an. In unserer Entwicklungsabteilung entsteht ständig technische Dokumentation — Installationsanleitungen, Konfigurationshinweise, Beschreibungen von Schnittstellen. Das Problem war: Diese Dokumentation lag verstreut an drei verschiedenen Orten. Ein Teil im HTML-Editor von Odoo, ein Teil in Git-Wikis, und ein Teil in lokalen Markdown-Dateien auf einzelnen Rechnern.

Das hat zu Medienbrüchen geführt: Es gab keinen einheitlichen Standard, keine zentrale Suche, und der HTML-Editor von Odoo ist für technische Inhalte wie Code-Snippets oder Tabellen schlecht geeignet. Außerdem war der Zugriff nicht sauber über die Odoo-Berechtigungen abgesichert. Kurz gesagt: Das Wissen war vorhanden, aber nicht zentral nutzbar.

## Folie 4 — Das Ziel

Daraus ergab sich mein Ziel: alles in Odoo. Kein Wechsel mehr zwischen verschiedenen Werkzeugen. Markdown sollte dabei das Arbeitsformat bleiben, weil es im Team durch die tägliche Arbeit mit Git ohnehin bekannt und akzeptiert ist.

Konkret wollte ich einen Markdown-Editor direkt in Odoo, mit einer Live-Vorschau beim Schreiben, einer automatischen Versionierung, einem PDF-Export und einem Zugriffsschutz über das bestehende Rechtesystem von Odoo.

## Folie 5 — Make or Buy?

Natürlich habe ich vorher geprüft, ob man so etwas nicht einfach kaufen kann. Dafür habe ich eine Nutzwertanalyse gemacht und drei Varianten bewertet.

Confluence ist ein fertiges Wiki-Werkzeug, hat aber keine Anbindung an Odoo — der Medienbruch bliebe also bestehen. Ein Git-Wiki wäre kostenlos, lässt sich aber nicht aus Odoo heraus nutzen. Die Eigenentwicklung erreicht mit 475 von 500 Punkten den höchsten Nutzwert, weil nur sie das Kernproblem löst: die direkte Integration in Odoo.

Wirtschaftlich liegt der kalkulatorische Aufwand bei rund 2.100 Euro für 80 Stunden, dafür entfallen laufende Lizenzkosten. Die Entscheidung fiel deshalb klar auf die Eigenentwicklung.

## Folie 6 — Technischer Aufbau

Kommen wir zum technischen Aufbau. MDWriter ist ein eigenständiges Odoo-Modul und folgt dem Drei-Schichten-Modell, das Odoo vorgibt.

Ganz unten liegt die **Datenschicht**. Die Daten stehen in einer PostgreSQL-Datenbank. Ich greife aber nicht direkt mit SQL darauf zu, sondern über das ORM von Odoo — das ist die Schicht, die Datenbank-Tabellen als Python-Objekte abbildet. Dateien wie die erzeugten PDFs speichere ich über das Odoo-eigene Anhang-System, genannt ir.attachment.

In der Mitte liegt die **Backend-Schicht** in Python. Hier steckt die eigentliche Logik — die Versionierung, das Erzeugen der PDFs und die Sicherheitsregeln. Für das Umwandeln von Markdown in HTML nutze ich die Bibliothek mistune, und das fertige PDF baut der QWeb-Report-Mechanismus von Odoo.

Und oben liegt die **Frontend-Schicht**, also das, was der Benutzer im Browser sieht. Die habe ich als OWL-Komponente gebaut — OWL ist das hauseigene JavaScript-Framework von Odoo, von der Idee her vergleichbar mit React. Den Editor selbst liefert die Bibliothek CodeMirror, und die Live-Vorschau rendert markdown-it.

Ein Punkt ist mir dabei wichtig: Alle diese Bibliotheken liegen lokal im Modul, es gibt keine Aufrufe an externe Server. Dadurch ist das Modul auch in einem Firmennetz ohne Internet lauffähig.

## Folie 7 — Was das Modul kann

Was kann das Modul nun konkret? Ich habe sechs Kernfunktionen.

Erstens der **Split-View-Editor**: links schreibe ich Markdown, rechts sehe ich sofort die formatierte Vorschau.

Zweitens die **automatische Versionierung**. Bei jeder inhaltlichen Änderung legt das Modul automatisch eine neue Version an — mit Versionsnummer, Zeitpunkt, Bearbeiter und einer MD5-Prüfsumme. Diese Prüfsumme ist ein Fingerabdruck des Inhalts, an dem sich erkennen lässt, ob sich etwas geändert hat — sie dient also der Änderungserkennung, nicht der Sicherheit. Bestehende Versionen werden dabei nie verändert, es kommen nur neue dazu.

Drittens der **Versionsvergleich**: Ich kann zwei Versionen auswählen und sehe farblich, was hinzugekommen und was entfernt wurde.

Viertens die **Wiederherstellung**: Eine ältere Version lässt sich zurückholen — das erzeugt selbst wieder eine neue Version, man verliert also nichts.

Fünftens der **PDF-Export**, der bereits erzeugte PDFs zwischenspeichert, damit nicht bei jedem Klick neu gerechnet wird.

Und sechstens eine **Statusverwaltung** mit Entwurf, Veröffentlicht und Archiviert.

Versionierung, Vergleich und PDF-Export waren Pflichtanforderungen — die Wiederherstellung und die Statusverwaltung habe ich als sinnvolle Ergänzung dazugenommen.

## Folie 8 — Herausforderung in der Umsetzung

Bei der Umsetzung gab es natürlich auch Hürden — eine möchte ich konkret zeigen, weil ich daran am meisten gelernt habe.

Der Editor CodeMirror braucht ein echtes Element im Browser, an das er sich hängen kann — konkret das Textfeld. Mein erster Ansatz war, ihn direkt beim Start der Komponente zu initialisieren. Das hat aber nicht funktioniert, weil dieser Start-Code zu früh läuft: Das Textfeld existiert zu diesem Zeitpunkt im Browser noch gar nicht.

Die Lösung war, den Lebenszyklus der OWL-Komponente zu nutzen. OWL bietet sogenannte Lifecycle-Hooks — das sind feste Zeitpunkte im Leben einer Komponente. Den Hook onMounted ruft OWL erst auf, wenn die Komponente tatsächlich im Browser angezeigt wird. Genau dort initialisiere ich CodeMirror jetzt. Und beim Gegenstück onWillUnmount, also kurz bevor die Komponente wieder verschwindet, räume ich auf, damit kein Speicher unnötig belegt bleibt.

Die Erkenntnis daraus: Wer eine externe Bibliothek einbindet, muss den Lebenszyklus des Frameworks verstehen. Das nehme ich für künftige Odoo-Projekte mit.

## Folie 9 — Qualitätssicherung

Zur Qualitätssicherung. Der Zugriffsschutz hat zwei Ebenen, die in Odoo zusammenspielen.

Die erste Ebene sind die **ACLs**, die Access Control Lists. Sie legen fest, ob eine Benutzergruppe ein Datenmodell überhaupt anfassen darf — also lesen, schreiben, anlegen oder löschen.

Die zweite Ebene sind die **Record Rules**, die Datensatzregeln. Die ACL allein würde nämlich jedem Benutzer alle Dokumente zeigen. Die Record Rule schränkt das auf Datensatz-Ebene ein: Ein normaler Benutzer sieht nur die Dokumente, die ihm selbst gehören. Technisch hängt Odoo dafür eine Bedingung an jede Datenbankabfrage an, sodass fremde Dokumente gar nicht erst zurückkommen — auch dann nicht, wenn jemand die Adresse direkt aufruft.

Dazu kommt der Schutz vor Cross-Site-Scripting: Markdown darf kein eingebettetes HTML oder JavaScript ausführen. Das verhindere ich im Frontend mit der Einstellung html:false und im Backend dadurch, dass mistune kein aktives HTML erzeugt.

Getestet habe ich mit sieben automatisierten Tests, die genau diese Punkte abdecken — Versionierung, Zugriffsschutz und Versionsvergleich. Alle laufen ohne Fehler durch. Die Abnahme durch meinen Ausbilder ist erfolgt.

## Folie 10 — Projektergebnis

Zum Ergebnis: Alle Pflichtanforderungen sind vollständig umgesetzt, und ich bin im geplanten Zeitrahmen von 80 Stunden geblieben. Das Modul ist intern freigegeben und könnte perspektivisch auch in Kundenprojekten eingesetzt werden.

Persönlich habe ich vor allem die Frontend-Entwicklung mit Odoo besser verstanden — den OWL-Lebenszyklus, das saubere Trennen der Render-Schichten und die Eigenheiten der PDF-Erzeugung. Damit hat das Projekt genau das gebracht, was ich mir vorgenommen hatte.

## Übergang zur Live-Demo

So viel zur Theorie — am besten sehen Sie sich das Modul selbst an. Ich zeige Ihnen MDWriter jetzt live.

*(→ Live-Demo nach dem Demo-Spickzettel: Öffnen · Split-View · Speichern/Version · Diff · PDF · Rechte)*

## Folie 11 — Vielen Dank

Damit bin ich am Ende. Vielen Dank für Ihre Aufmerksamkeit — für Ihre Fragen stehe ich gern im Fachgespräch zur Verfügung.
