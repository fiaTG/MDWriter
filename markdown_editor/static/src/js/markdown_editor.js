/** @odoo-module **/
// ==================================================================
// markdown_editor.js — OWL-Komponente für den Markdown-Editor
// ==================================================================
// Was ist OWL?
//   OWL (Odoo Web Library) ist Odoos eigenes JavaScript-Framework,
//   ähnlich wie React oder Vue. Grundprinzip:
//     - "Komponenten" sind wiederverwendbare UI-Bausteine
//     - Reaktiver State: wenn sich Daten ändern, aktualisiert OWL
//       automatisch das DOM — ohne manuelle DOM-Manipulationen
//
// Was macht diese Datei?
//   Sie definiert die MarkdownField-Komponente: den Split-View-Editor
//   mit CodeMirror links und markdown-it Vorschau rechts.
//   Am Ende wird die Komponente im Odoo-Feld-Registry registriert,
//   damit sie über widget="markdown_editor" in XML-Views nutzbar ist.
// ==================================================================

// ------------------------------------------------------------------
// Imports aus dem OWL-Framework
// ------------------------------------------------------------------
// Component:      Basisklasse für alle OWL-Komponenten
// useState:       reaktiver State — Änderungen triggern automatisch ein Re-Render
// markup:         wie Markup() in Python — markiert HTML als sicher für innerHTML
// useRef:         gibt eine Referenz auf ein DOM-Element zurück (wie document.getElementById)
// onMounted:      Lifecycle-Hook: wird aufgerufen sobald die Komponente im DOM ist
// onWillUnmount:  Lifecycle-Hook: wird aufgerufen kurz bevor die Komponente entfernt wird
// ------------------------------------------------------------------
import { Component, useState, markup, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";            // Odoos zentrale Registry (für Felder, Services, ...)
import { standardFieldProps } from "@web/views/fields/standard_field_props"; // Standard-Props jedes Odoo-Feldes


class MarkdownField extends Component {
    // setup() ist die OWL-Lifecycle-Methode für Initialisierung.
    // Sie ersetzt den Konstruktor (constructor) bei OWL-Komponenten.
    // Alles was beim ersten Laden passieren soll, kommt hierher.
    setup() {
        // this.props enthält die von Odoo übergebenen Eigenschaften:
        //   record: der aktuelle Datensatz (z.B. das x.md.document-Objekt)
        //   name:   der Feldname ("content_md")
        //   readonly: ob das Feld schreibgeschützt ist
        const initial = this.props.record.data[this.props.name] || "";

        // window.markdownit: die global geladene markdown-it Bibliothek.
        // Sie wurde im __manifest__.py als Asset registriert und ist daher
        // im Browser als window.markdownit verfügbar.
        // html: false → kein rohen HTML in Markdown erlauben (XSS-Schutz)
        // breaks: true → einzelne Zeilenumbrüche werden zu <br>
        // linkify: true → URLs werden automatisch zu Links
        this.md = window.markdownit
            ? window.markdownit({ html: false, breaks: true, linkify: true })
            : null;

        // useState: reaktiver State-Container.
        // Wenn this.state.value oder this.state.html sich ändern,
        // rendert OWL die Komponente automatisch neu.
        this.state = useState({
            value: initial,
            html: this._render(initial),
        });

        // useRef("editor"): holt eine Referenz auf das DOM-Element mit t-ref="editor"
        // (definiert im XML-Template). Über .el kommt man an das echte DOM-Element.
        this.editorRef = useRef("editor");
        this.cm = null;         // CodeMirror-Instanz (wird in onMounted gesetzt)
        this._debounce = null;  // Timer-ID für das Debouncing

        // onMounted: dieser Code läuft NACHDEM die Komponente ins DOM eingebaut wurde.
        // Erst dann existiert this.editorRef.el — daher CodeMirror erst hier initialisieren.
        onMounted(() => {
            if (!window.CodeMirror || !this.editorRef.el) return;

            // CodeMirror.fromTextArea: wandelt das <textarea> in einen vollwertigen
            // Code-Editor um. Das Original-<textarea> wird versteckt, CodeMirror
            // baut seinen eigenen Editor darum herum.
            this.cm = window.CodeMirror.fromTextArea(this.editorRef.el, {
                mode: "markdown",       // Syntax-Highlighting für Markdown
                lineWrapping: true,     // lange Zeilen umbrechen statt horizontal scrollen
                lineNumbers: false,     // keine Zeilennummern (zu unruhig für Markdown)
                theme: "default",       // Farbschema (wird durch codemirror_theme.scss überschrieben)
                readOnly: this.props.readonly ? "nocursor" : false,  // Cursor verstecken wenn readonly
                autofocus: false,
                extraKeys: { Tab: false },  // Tab-Taste nicht abfangen (für Formular-Navigation)
            });

            this.cm.setValue(this.state.value);

            // Debounce: verhindert, dass die Vorschau bei jedem einzelnen Tastendruck
            // neu berechnet wird. Stattdessen: erst 300ms nach dem letzten Tastendruck rendern.
            // clearTimeout cancelt einen laufenden Timer, setTimeout startet einen neuen.
            this.cm.on("change", (cm) => {
                clearTimeout(this._debounce);
                this._debounce = setTimeout(() => this._updateState(cm.getValue()), 300);
            });
        });

        // onWillUnmount: Aufräumen wenn die Komponente entfernt wird.
        // Timer canceln (kein Update mehr nach Entfernen) und CodeMirror zerstören.
        // Verhindert Memory Leaks.
        onWillUnmount(() => {
            clearTimeout(this._debounce);
            if (this.cm) {
                this.cm.toTextArea();  // CodeMirror rückgängig machen, original <textarea> wiederherstellen
                this.cm = null;
            }
        });
    }

    // _render: wandelt Markdown-Text in sicheres HTML um.
    // markup(): OWL-Äquivalent zu Python's Markup() — kennzeichnet HTML als vertrauenswürdig,
    // damit OWL es direkt rendert (t-out im Template).
    _render(value) {
        return this.md ? markup(this.md.render(value)) : markup(value);
    }

    // _updateState: wird aufgerufen wenn sich der Editor-Inhalt ändert.
    // Aktualisiert state (→ OWL re-rendert die Vorschau)
    // und speichert den neuen Wert im Odoo-Record (record.update → wird beim Speichern übernommen).
    _updateState(value) {
        this.state.value = value;
        this.state.html = this._render(value);
        this.props.record.update({ [this.props.name]: value });
        // [this.props.name]: computed property key — dynamischer Schlüsselname.
        // Wenn props.name = "content_md", dann: { content_md: value }
    }

    /** Fallback-Handler wenn CodeMirror nicht geladen wurde. */
    // Wird ausgelöst durch t-on-input="_onInput" im Template.
    // ev.target.value: der aktuelle Wert des <textarea>-Elements.
    _onInput(ev) {
        if (!this.cm) this._updateState(ev.target.value);
    }
}

// ------------------------------------------------------------------
// Komponente konfigurieren und registrieren
// ------------------------------------------------------------------
// template: Name des OWL-Templates (definiert in markdown_editor_templates.xml)
MarkdownField.template = "markdown_editor.MarkdownField";
// props: welche Properties akzeptiert die Komponente?
// ...standardFieldProps: alle Standard-Odoo-Feld-Props übernehmen (record, name, readonly, ...)
MarkdownField.props = { ...standardFieldProps };
// supportedTypes: für welche Feldtypen kann dieser Widget verwendet werden?
MarkdownField.supportedTypes = ["text"];

// registry.category("fields").add(...): registriert die Komponente als Odoo-Feld-Widget.
// "markdown_editor" ist der Name, der in XML mit widget="markdown_editor" verwendet wird.
registry.category("fields").add("markdown_editor", {
    component: MarkdownField,
    supportedTypes: ["text"],
});

export default MarkdownField;
