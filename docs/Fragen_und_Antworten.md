# Fragen & Antworten — Fachgespräch MDWriter

> Lern- und Vorbereitungsblatt für das Fachgespräch nach Präsentation + Live-Demo.
> Kurzform zum Wiederholen. Teil A = Fragen zum Modul, Teil B = Python-Grundlagen.

---

# Teil A — Fragen zum Modul

## Überblick

**Was ist MDWriter / was macht das Modul?**
Ein eigenständiges Odoo-19-Modul (technischer Name `markdown_editor`), mit dem man technische Dokumentation im Markdown-Format direkt in Odoo schreibt, versioniert, vergleicht, als PDF exportiert und über das Odoo-Rechtesystem absichert.

**Warum überhaupt? Was war das Problem?**
Dokumentation lag verstreut: Odoo-HTML-Editor, Git-Wikis, lokale Dateien → Medienbrüche, kein Standard, keine zentrale Suche, kein Zugriffsschutz. MDWriter bringt alles an einen Ort.

**Warum Eigenentwicklung statt Confluence?**
Externe Tools lösen das Kernproblem nicht: die Integration in Odoo. In der Nutzwertanalyse erreichte MDWriter 475/500 Punkte. Keine laufenden Lizenzkosten, volle Datenhoheit, in Kundenprojekten wiederverwendbar.

**Warum Markdown und kein WYSIWYG-Editor?**
Markdown ist im Team bekannt (Git), gut für Code-Snippets/Tabellen, versionierbar als reiner Text, und der Inhalt bleibt sauber getrennt von der Darstellung.

## Architektur

**Wie ist das Modul aufgebaut?**
Drei-Schichten-Modell von Odoo:
- **Datenschicht:** PostgreSQL, Zugriff über das ORM; Dateien über `ir.attachment`.
- **Backend (Python):** Versionierung, PDF-Erzeugung, Sicherheit. Markdown→HTML via `mistune`, PDF via QWeb-Report.
- **Frontend (OWL):** Split-View-Editor im Browser. Editor = CodeMirror, Live-Vorschau = markdown-it.

**Was ist das ORM? Warum kein direktes SQL?**
ORM = Object-Relational Mapper. Es bildet Datenbank-Tabellen als Python-Objekte/Klassen ab. Man arbeitet mit `self.create(...)`, `self.search(...)` statt SQL. Vorteile: weniger Fehler, Sicherheit (SQL-Injection-Schutz), Odoo-Berechtigungen greifen automatisch, datenbankunabhängig.

**Was ist OWL?**
Odoo Web Library — das hauseigene JavaScript-Framework von Odoo, vom Prinzip ähnlich wie React/Vue: UI aus Komponenten, reaktiver State (ändert sich der State, aktualisiert OWL automatisch das DOM).

**Was ist eine Komponente?**
Ein wiederverwendbarer UI-Baustein. Meine `MarkdownField`-Komponente ist als Field-Widget registriert und wird in der View über `widget="markdown_editor"` am Feld `content_md` eingebunden.

**Unterschied CodeMirror / markdown-it / mistune?**
- **CodeMirror** (JS, Frontend): der Code-Editor links mit Syntax-Highlighting.
- **markdown-it** (JS, Frontend): wandelt Markdown live in HTML für die Vorschau rechts.
- **mistune** (Python, Backend): wandelt Markdown in HTML für den PDF-Export.
Zwei Renderer, weil Frontend (Browser, live) und Backend (Server, für PDF) getrennt sind.

**Wo werden die Daten gespeichert?**
Im Datenmodell in PostgreSQL (über das ORM). Die `.md`- und `.pdf`-Dateien jeder Version liegen als Odoo-Attachments (`ir.attachment`).

**Welche Modelle gibt es?**
- `x.md.document` — das Dokument (Titel, content_md, Status, Eigentümer …).
- `x.md.document.version` — die Versionen (append-only).
- `x.md.document.diff.wizard` — Hilfsmodell (TransientModel) für den Vergleichsdialog.

**Warum das `x.` im Modellnamen?**
Konvention für Modelle außerhalb des offiziellen Odoo-Namensraums — signalisiert „projektspezifische Erweiterung".

## Funktionen

**Wie funktioniert die automatische Versionierung?**
Beim Erstellen (`create`) und beim Ändern des Inhalts (`write` auf `content_md`) wird automatisch eine neue Version angelegt. Im `write` prüfe ich `if "content_md" in vals` — nur dann eine Version, Statusänderungen lösen keine aus.

**Was heißt append-only?**
Bestehende Versionen werden nie verändert oder gelöscht, es kommen nur neue dazu. Das garantiert einen lückenlosen, nachvollziehbaren Verlauf (Audittrail).

**Was ist die MD5-Prüfsumme? MD5 ist doch unsicher?**
Die Prüfsumme ist ein „Fingerabdruck" des Inhalts: gleicher Text → gleiche Summe. Damit erkennt man, ob sich etwas geändert hat. Sie dient der **Änderungserkennung**, **nicht** der Sicherheit — deshalb ist die kryptografische Schwäche von MD5 hier kein Problem. Sicherheit machen ACL + Record Rules.

**Wie funktioniert der Versionsvergleich (Diff)?**
Ein Wizard nimmt zwei Versionen. Im Backend vergleicht Pythons `difflib` die Zeilen und erzeugt ein farbiges HTML — grün = hinzugefügt, rot = entfernt.

**Wie funktioniert die Wiederherstellung?**
Eine ältere Version wird als aktueller Inhalt zurückgeschrieben. Das löst wieder die Versionierung aus → es entsteht eine neue Version. Man verliert also nichts, die Wiederherstellung ist selbst versioniert.

**Wie funktioniert der PDF-Export?**
mistune macht aus dem Markdown HTML, der QWeb-Report von Odoo baut daraus mit wkhtmltopdf das PDF. Beim ersten Mal wird das PDF erzeugt und als Attachment gespeichert; danach wird das gespeicherte PDF wiederverwendet (Cache), statt neu zu rendern.

## Sicherheit

**Wie ist der Zugriffsschutz geregelt?**
Zwei Ebenen: ACL (Modellebene) + Record Rules (Datensatzebene). Nur wenn beide erlauben, hat ein Benutzer Zugriff.

**Was ist der Unterschied ACL vs. Record Rule?**
- **ACL** (`ir.model.access.csv`): „Darf die Gruppe das Modell überhaupt lesen/schreiben/anlegen/löschen?" — gilt fürs ganze Modell.
- **Record Rule** (XML): „Welche einzelnen Datensätze?" — z. B. `[('owner_id','=',user.id)]`: nur eigene Dokumente. Odoo hängt das als Bedingung an jede DB-Abfrage.

**Warum brauchst du beides?**
ACL allein würde jedem alle Dokumente zeigen. Erst die Record Rule schränkt auf die eigenen ein.

**Wie ist die Versionierung gegen Manipulation geschützt?**
Normale Benutzer haben auf dem Versionsmodell nur Leserecht (ACL `1,0,0,0`). Neue Versionen legt nur der Server an (mit `sudo()`). Über die Oberfläche kann niemand Versionen ändern.

**Wie verhinderst du XSS (Cross-Site-Scripting)?**
Markdown darf kein aktives HTML/JS ausführen. Frontend: markdown-it mit `html: false` (HTML-Tags werden escaped). Backend: mistune erzeugt kein aktives HTML. So kann kein eingeschleustes Script laufen.

**Ändert „Veröffentlichen" die Sichtbarkeit für andere?**
Nein. Sichtbarkeit hängt nur an `owner_id` / der Record Rule. Der Status (Entwurf/Veröffentlicht/Archiviert) ist reine Workflow-Anzeige, kein Sicherheitsmerkmal.

## Test & Qualität

**Wie hast du getestet?**
7 automatisierte Tests mit der Odoo-Klasse `TransactionCase` (rollt nach jedem Test die DB zurück → Tests sind isoliert). Sie decken Versionierung, Zugriffskontrolle und Versionsvergleich ab. Ergebnis: 0 Fehler. Dazu manuelle Integrationstests im Browser.

**Was prüfen die ACL-Tests konkret?**
Z. B.: ein fremder Benutzer findet ein fremdes Dokument nicht (leeres Ergebnis), und ein normaler Benutzer bekommt einen `AccessError`, wenn er direkt eine Version anlegen will.

## Herausforderung / OWL

**Was war deine größte technische Herausforderung?**
CodeMirror braucht ein echtes DOM-Element (das Textfeld). Beim Start der Komponente existiert das noch nicht. Lösung: Initialisierung im Lifecycle-Hook `onMounted` (läuft erst, wenn die Komponente im DOM ist); Aufräumen in `onWillUnmount` gegen Memory Leaks.

**Was ist ein Lifecycle-Hook?**
Ein fester Zeitpunkt im „Leben" einer Komponente, an dem das Framework eigenen Code aufruft — z. B. `onMounted` (eingehängt ins DOM), `onWillUnmount` (wird gleich entfernt).

**Was macht der Debounce (300 ms)?**
Verzögert die Vorschau-Aktualisierung: Erst 300 ms nach dem letzten Tastendruck wird neu gerendert. Verhindert, dass bei schnellem Tippen bei jedem Anschlag neu gerechnet wird.

## Sonstiges

**Was ist ein TransientModel?**
Ein temporäres Hilfsmodell in Odoo, das Daten nicht dauerhaft speichert (Odoo löscht sie automatisch). Ich nutze es für den Vergleichsdialog.

**Was passiert, wenn das `documents`-Modul fehlt?**
Die Documents-Integration ist defensiv: Fehlt das Modul oder schlägt die Ablage fehl, wird der Fehler nur protokolliert — die Versionierung läuft trotzdem weiter.

**Was würdest du heute anders machen / Ausblick?**
Performance-Optimierung bei sehr großen Dokumenten, Volltextsuche, Kommentarfunktion, Vorlagen-System. Früheres Verständnis des OWL-Lebenszyklus hätte mir Debugging erspart.

---

# Teil B — Python-Grundlagen (Kurzform)

**`self`**
Verweist auf das aktuelle Objekt (den Datensatz/Recordset), auf dem die Methode läuft. In Odoo ist `self` ein Recordset — kann einen oder mehrere Datensätze enthalten, deshalb oft `for record in self:`.

**`class XMdDocument(models.Model):`**
Definiert eine Klasse (Bauplan). `(models.Model)` = sie **erbt** von Odoos Basisklasse `Model` und bekommt dadurch ORM-Funktionen wie `create`, `write`, `search`.

**Vererbung**
Eine Klasse übernimmt Eigenschaften/Methoden einer anderen. `super().write(vals)` ruft die ursprüngliche `write`-Methode der Elternklasse auf, bevor/nachdem ich eigene Logik ergänze.

**`def methode(self, ...):`**
Definiert eine Methode (Funktion in einer Klasse). Der erste Parameter ist immer `self`.

**`fields.Char` / `Text` / `Many2one` / `One2many` / `Integer` / `Selection`**
Odoo-Felddefinitionen = Spalten in der Tabelle. `Char` kurzer Text, `Text` langer Text, `Many2one` Verweis auf **einen** anderen Datensatz (z. B. Eigentümer), `One2many` Liste verknüpfter Datensätze (z. B. alle Versionen), `Selection` Auswahlliste.

**`vals`**
Ein `dict` (Schlüssel-Wert-Paare) mit den geänderten Feldern, z. B. `{"content_md": "# Neu"}`. `if "content_md" in vals:` prüft, ob dieses Feld dabei war.

**`lambda self: self.env.user`**
Eine kurze, namenlose Funktion in einer Zeile. Hier als `default`: setzt beim Anlegen den Eigentümer automatisch auf den aktuell angemeldeten Benutzer.

**`self.env`**
Die „Umgebung": Zugang zu anderen Modellen (`self.env["x.md.document.version"]`), zum aktuellen Benutzer (`self.env.user`), zum Kontext usw.

**`@api.depends("version_ids.version")`**
Ein **Decorator** — markiert eine Methode als „berechne dieses Feld neu, sobald sich die genannten Felder ändern". Hier: `current_version` wird neu berechnet, wenn sich Versionen ändern.

**`@api.model`**
Decorator für Methoden, die nicht auf einem konkreten Datensatz, sondern auf dem Modell selbst arbeiten (z. B. das Anlegen der Demo-Daten).

**`.sudo()`**
Führt die folgende Operation mit erhöhten Rechten (als Superuser) aus, umgeht also die Zugriffsregeln. Brauche ich, weil normale Benutzer keine Versionen anlegen dürfen, der Server das aber automatisch tun muss.

**`hashlib.md5(content.encode("utf-8")).hexdigest()`**
Erzeugt die Prüfsumme. `encode("utf-8")` wandelt den Text in Bytes (das braucht md5). `.hexdigest()` gibt die Summe als 32-Zeichen-Hex-Text zurück.

**`.mapped("version")`**
ORM-Helfer: holt aus einem Recordset die Werte eines Feldes als Liste. `max(..., default=0)` nimmt den größten Wert (oder 0, wenn leer).

**`try: ... except Exception as e: ...`**
Fehlerbehandlung: Code im `try` ausführen; tritt ein Fehler auf, läuft der `except`-Teil (z. B. Fehler protokollieren), statt das Programm abstürzen zu lassen.

**`return`**
Gibt einen Wert aus der Methode zurück (z. B. `write` gibt `True` zurück). Ohne `return` gibt eine Methode `None` zurück.

**`None` vs. `False`**
`None` = „kein Wert". In Odoo wird für leere Verweise (Many2one) meist `False` verwendet, nicht `None`.

**`registry.category("fields").add("markdown_editor", {...})`** (JS)
Registriert meine OWL-Komponente unter dem Namen `markdown_editor`, damit sie in der View mit `widget="markdown_editor"` nutzbar ist.

**`useState({...})`** (JS, OWL)
Erzeugt einen reaktiven Zustand: Ändere ich `state.html`, rendert OWL die Vorschau automatisch neu.

**`markup(...)` / `Markup(...)`**
Kennzeichnet einen HTML-String als „vertrauenswürdig", damit er angezeigt und nicht noch einmal als Text escaped wird. (`markup` in OWL/JS, `Markup` aus markupsafe in Python.)
