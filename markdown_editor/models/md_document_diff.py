# ==================================================================
# md_document_diff.py — Versionsvergleich (Diff-Wizard)
# ==================================================================
# Dieser Wizard vergleicht zwei Versionen eines Dokuments und zeigt
# die Unterschiede farbig hervorgehoben an (unified diff).
#
# Was ist ein "Wizard" in Odoo?
#   Ein Wizard ist ein kurzlebiges Formular — es öffnet sich als Popup,
#   der Nutzer wählt etwas aus, und danach wird es wieder verworfen.
#   Wizards erben von models.TransientModel (statt models.Model).
#   TransientModel: Einträge werden automatisch nach einiger Zeit
#   aus der Datenbank gelöscht — kein dauerhafter Speicher.
# ==================================================================

import difflib   # Standard-Python-Bibliothek für Textvergleiche
import html as html_mod  # html.escape() schützt gegen XSS in selbst-gebautem HTML

from odoo import api, fields, models


class XMdDocumentDiffWizard(models.TransientModel):
    _name = "x.md.document.diff.wizard"
    _description = "Versionsdiff"

    document_id = fields.Many2one(comodel_name="x.md.document", string="Dokument", required=True)
    version_from_id = fields.Many2one(
        comodel_name="x.md.document.version",
        string="Von Version",
        domain="[('document_id', '=', document_id)]",
        # domain: schränkt die auswählbaren Einträge ein.
        # Hier: nur Versionen des aktuellen Dokuments anzeigen (nicht fremder Dokumente).
    )
    version_to_id = fields.Many2one(
        comodel_name="x.md.document.version",
        string="Bis Version",
        domain="[('document_id', '=', document_id)]",
    )
    # sanitize=False: Das HTML wird unten mit html.escape() manuell gebaut.
    # Odoo darf es nicht nochmal bereinigen, sonst gehen die <span>-Tags verloren.
    diff_html = fields.Html(string="Diff", compute="_diff_html_berechnen", sanitize=False)

    @api.depends("version_from_id", "version_to_id")
    def _diff_html_berechnen(self):
        # Wird bei jeder Änderung der Versionsauswahl neu berechnet.
        for rec in self:
            if not (rec.version_from_id and rec.version_to_id):
                rec.diff_html = ""
                continue  # "continue" springt zum nächsten Schleifendurchlauf

            # splitlines(keepends=True): teilt Text in Zeilen auf,
            # behält aber das Zeilenende-Zeichen (\n) am Ende jeder Zeile.
            # Das ist nötig, damit unified_diff korrekte Ausgaben erzeugt.
            a = (rec.version_from_id.content_md or "").splitlines(keepends=True)
            b = (rec.version_to_id.content_md or "").splitlines(keepends=True)

            # difflib.unified_diff: erzeugt einen "unified diff" — das gleiche Format
            # wie "git diff". Jede Zeile beginnt mit:
            #   "+" = hinzugefügt  "-" = entfernt  " " = unverändert
            # n=3: 3 Kontext-Zeilen um jede Änderung herum anzeigen
            diff_lines = list(difflib.unified_diff(
                a, b,
                fromfile=f"Version {rec.version_from_id.version}",
                tofile=f"Version {rec.version_to_id.version}",
                n=3,
            ))

            if not diff_lines:
                rec.diff_html = "<p>Keine Unterschiede gefunden.</p>"
                continue

            # Jede Zeile in einen <span> mit passender CSS-Klasse einwickeln.
            # Das SCSS in codemirror_theme.scss färbt die Klassen ein:
            #   o_md_diff_add    → grün (neu)
            #   o_md_diff_del    → rot (gelöscht)
            #   o_md_diff_hunk   → blau (@@ Positions-Info)
            #   o_md_diff_header → grau (+++ / --- Dateiheader)
            parts = ['<pre class="o_md_diff">']
            for line in diff_lines:
                # html_mod.escape(): wandelt < > & in &lt; &gt; &amp; um → XSS-Schutz.
                # Wichtig: erst escapen, dann in <span> einbetten!
                escaped = html_mod.escape(line)
                # +++ / --- vor + / - prüfen, da beide mit + bzw. - beginnen
                if line.startswith("+++") or line.startswith("---"):
                    parts.append(f'<span class="o_md_diff_header">{escaped}</span>')
                elif line.startswith("+"):
                    parts.append(f'<span class="o_md_diff_add">{escaped}</span>')
                elif line.startswith("-"):
                    parts.append(f'<span class="o_md_diff_del">{escaped}</span>')
                elif line.startswith("@@"):
                    parts.append(f'<span class="o_md_diff_hunk">{escaped}</span>')
                else:
                    parts.append(f'<span>{escaped}</span>')
            parts.append("</pre>")
            # "".join(parts): alle Teile ohne Trennzeichen zu einem String zusammenbauen
            rec.diff_html = "".join(parts)
