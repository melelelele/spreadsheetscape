# SheetScape — Spreadsheet Escape Room mit CSCape

Dieser Escaperoom soll spielerisch die Funktionsweise von Google-Spreadsheets vermitteln.
---

## Konzept

**SheetScape** ist ein textbasiertes Escape-Room-Tutorial für Google Sheets.

Die Spieler reparieren Schritt für Schritt ein beschädigtes Archiv-Spreadsheet und lernen dabei grundlegende Spreadsheet-Funktionen:

* Zellen verstehen
* Formeln schreiben
* Bereiche summieren
* Werte kombinieren
* Tabellen logisch lesen
* einfache Entscheidungen mit `WENN`

Die Story läuft über Reveal.js + CSCape.  
Die Darstellung kann zwischen **Textmodus** und **Videomodus** umgeschaltet werden.

---

## Komponenten

| Datei                | Zweck                                                   |
| -------------------- | ------------------------------------------------------- |
| `game.py`            | Spiellogik & Spreadsheet-Checks                         |
| `cscape.py`          | Backend (Flask + Game-State API)                        |
| `index.html`         | Story, Dialoge, Slides, Theme-Konfiguration             |
| `story-styles/cscape-story.css` | gemeinsames Story-/Dialog-/Video-Layout          |
| `story-styles/cscape-story.js`  | gemeinsame Story-Engine, Sound, Musik, TTS       |
| `revealjs-cscape.js` | Polling & automatische Slide-Steuerung                  |
| `tts_server.py`      | lokaler TTS-Server für dynamisch generierte MP3s        |
| `config.ini`         | optionale Integrationen                                 |
| `sounds/`            | feste Soundeffekte und vorberechnete MP3s               |
| `pics/`              | Charakterbilder, Hintergründe, `background.jpg`         |

---

## Ablauf

1. Frontend pollt regelmäßig das Backend.
2. `Game.check_*` Methoden werden ausgeführt.
3. Spreadsheet-Werte werden geprüft.
4. Wenn ein Check `True` liefert, versucht CSCape zur nächsten Slide zu wechseln.
5. Die Story-Engine blockiert den Wechsel, bis laufender Text/Sound fertig ist.
6. Danach wartet sie optional noch die in `data-auto-next-after` gesetzte Zeit.

---

## Start

```bash
python3 game.py
```

Danach erreichbar unter:

```text
http://localhost:5000
```

Falls zusätzlich dynamische Sprachausgabe genutzt wird:

```bash
python3 tts_server.py
```

Der TTS-Server läuft standardmäßig unter:

```text
http://127.0.0.1:8765/tts
```

bzw im Dockercontainer:

```text
http://0.0.0.0:8765/tts
```
---

## Google Sheet vorbereiten

### 0. Anmelden

melde dich bei Google Sheet an mit einem "Wegwerfaccount", also einem Account, der keine wichtigen Informationen oder Passwörter enthält, da der Account den Spielenden zum Erfüllen der Aufgaben bereitgestellt werden soll.

### 1. Neues Spreadsheet erstellen

Erstelle ein Google Spreadsheet mit dem Namen:

```text
Geschenkregister
```

Folgender Inhalt muss in A1 eingefügt werden:

```text
Name                                

Werkstatt   Geschenkestapel 1   Geschenkestapel 2   Ergebnis        Schlitten   Kapazität   Geschenke pro Rentier   benötigte Rentiere
Werkstatt Nord  12  8           Weihnachtsschlitten  200 10  0
Werkstatt Süd   7   15                      
Werkstatt West  10  5                       
Gesamtgeschenke 29  28                      

Kind    Geschenk    Status  Geschenkcode        Kind    Geschenkcode    Geschenk    Lagerort
Mila    Sternenlampe    verpackt            Mila        Sternenlampe    
Noah    Schneekugel verpackt            Noah        Schneekugel 
Lio     verpackt    Lio-Märchenbuch     Lio Lio-Märchenbuch Märchenbuch Lager 2
Ava     verpackt    Ava-Kompass         Ava Ava-Kompass Kompass Lager 1
                    Emma    Emma-Zauberschal   Zauberschal Lager 1
Aufgabe Wert    Ergebnis            Finn    Finn-Plüschrentier Plüschrentier Lager 1
Verpackt zählen verpackt                Ella    Ella-Mondlaterne  Mondlaterne Lager 1
Offene zählen   offen               Tom Tom-Winterstiefel Winterstiefel Lager 4
Schlittenstatus
```

Die Datei ist außerdem als XLSX-Datei im Wurzelverzeichnis dieses Projekts gespeichert und kann 1:1 für das Spreadsheet übernommen werden.

---

### 2. Spreadsheet freigeben

```text
Freigeben → Allgemeiner Zugriff → Jeder mit dem Link → Betrachter
```

Dadurch wird die URL öffentlich.

Sie ist so aufgebaut:

```text
https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit?gid=0#gid=0
```

Benötigt wird aus dieser URL die `SHEET_ID`.

---

### 3. `SHEET_ID` in `game.py` und `index.html` eintragen

In `game.py`:

```python
SHEET_ID = "DEINE_SHEET_ID"
SHEET_GID = "0"
```

In `index.html`:

```js
const SHEET_ID = "DEINE_SHEET_ID";
const SHEET_GID = "0";
```

---

## Spreadsheet-Prinzip

Das Spiel liest die veröffentlichten Spreadsheet-Daten als CSV-Datei.

Beispiel:

```python
def check_name_done(self):
    rows = self.get_rows()
    return self.cell(rows, "B1").strip() != ""
```

---

## Checks definieren

Beispiel:

```python
def check_total_done(self):
    rows = self.get_rows()
    return self.cell(rows, "D7") == "57"
```

Verknüpfung in HTML:

```html
<section data-cscape-check="check_total_done">
```

---

## Lernziele im Spiel

Die Spieler lernen unter anderem:

* Zell-Koordinaten
* einfache Formeln
* `SUMME` / `SUM`
* Werte kombinieren
* `SVERWEIS`
* `ZÄHLENWENN`
* `WENN`
* Tabellen logisch lesen
* Spreadsheet-Denken

---

## Slides

Slides werden als Reveal.js-Sections definiert:

```html
<section
        data-speaker="Elli"
        data-avatar="pics/elli.jpg"
        data-side="right"
        data-dialogue="Am besten, du trägst erst mal deinen Namen in das Spreadsheet ein!"
        data-task="Trage deinen Namen in Zelle B1 ein.">
</section>
```

Die gemeinsame Story-Engine erzeugt fehlendes Markup automatisch.  
Es ist also nicht zwingend nötig, in jeder Slide manuell `.scene`, `.speaker`, `.dialogue` usw. zu schreiben.

---

## Story-Modi

Der Modus wird im `<body>` gesetzt.

### Textmodus

```html
<body class="theme-xmas" data-story-mode="text">
```

Im Textmodus:

* Charakter erscheint als kleines Bild im Dialoglayout
* `data-dialogue` wird getippt
* `data-task` erscheint im Dialogkasten
* `data-sound` wird als kurzer Character-/Effekt-Sound abgespielt
* dynamische TTS-Erzeugung wird nicht verwendet

---

### Videomodus

```html
<body class="theme-xmas" data-story-mode="video">
```

Im Videomodus:

* Charakter erscheint als große Figur
* Dialogkasten wird ausgeblendet
* `data-task` erscheint als große Aufgabenbox
* wenn `data-generate-sound="true"` gesetzt ist, wird aus `data-dialogue` dynamisch eine MP3 erzeugt
* wenn `data-generate-sound` nicht gesetzt ist, wird weiterhin `data-sound` verwendet

---

## Sound-Konfiguration

Sounds werden pro Slide gesetzt.

### Fester Sound

```html
<section
        data-speaker="Elli"
        data-avatar="pics/elli.jpg"
        data-side="right"
        data-sound="sounds/crunch.mp3"
        data-dialogue="Hallo!">
</section>
```

`data-sound` ist eine vorhandene Audiodatei aus dem Projekt.

Typischer Einsatz:

* kurze Character-Sounds im Textmodus
* Soundeffekte
* vorberechnete MP3s
* Fallback, wenn keine dynamische TTS-Erzeugung verwendet wird

---

### Dynamisch generierter Sound

Für dynamische Sprachausgabe wird pro Slide gesetzt:

```html
data-generate-sound="true"
data-tts-voice="de-DE-KatjaNeural"
```

Beispiel:

```html
<section
        data-speaker="Rudi"
        data-avatar="pics/rudi.jpg"
        data-side="left"
        data-sound="sounds/bells.mp3"
        data-generate-sound="true"
        data-tts-voice="de-DE-KillianNeural"
        data-dialogue="Perfekt, {player}! Jetzt können wir die Geschenkzahlen retten."
        data-task="">
</section>
```

Verhalten:

```text
Textmodus:
    data-sound wird abgespielt.
    data-dialogue wird getippt.

Videomodus:
    data-dialogue wird an den TTS-Server geschickt.
    Daraus wird eine MP3 generiert.
    data-sound wird ignoriert, weil data-generate-sound="true" gesetzt ist.
```

Dadurch kann der Room spontan zwischen Textmodus und Videomodus umgestellt werden, ohne jede Slide neu zu schreiben.

---

### Eigener TTS-Text

Standardmäßig wird bei dynamischer Sprachausgabe `data-dialogue` gesprochen.

Alternativ kann ein eigener TTS-Text gesetzt werden:

```html
data-sound-text="Das ist der gesprochene Text."
```

oder:

```html
data-tts-text="Das ist der gesprochene Text."
```

Reihenfolge:

1. `data-sound-text`
2. `data-tts-text`
3. `data-dialogue`

---

### Spielername in Sounds

Platzhalter wie `{player}` funktionieren auch in dynamisch generierten Sounds.

Beispiel:

```html
data-dialogue="Perfekt, {player}! Jetzt können wir weitermachen."
```

Wenn der Spieler in B1 seinen Namen eingetragen hat, wird daraus z. B.:

```text
Perfekt, Lenni! Jetzt können wir weitermachen.
```

Das funktioniert nur auf Slides, bei denen der Name vorher geladen wurde, z. B. über:

```html
data-load-player-name="true"
```

oder über die vorhandene `beforeSlide`-Logik in `index.html`.

---

## TTS-Stimmen pro Slide

Die Stimme wird bewusst pro Slide festgelegt.

Beispiel Weihnachtsmann:

```html
<section
        data-speaker="Weihnachtsmann"
        data-avatar="pics/weihnachtsmann.jpg"
        data-side="left"
        data-sound="sounds/hohoho.mp3"
        data-generate-sound="true"
        data-tts-voice="de-DE-ConradNeural"
        data-tts-rate="-8%"
        data-tts-pitch="-18Hz"
        data-dialogue="Ho ho ho! Weihnachten ist gerettet."
        data-task="">
</section>
```

Beispiel Elli:

```html
<section
        data-speaker="Elli"
        data-avatar="pics/elli.jpg"
        data-side="right"
        data-sound="sounds/crunch.mp3"
        data-generate-sound="true"
        data-tts-voice="de-DE-KatjaNeural"
        data-tts-rate="+3%"
        data-tts-pitch="+8Hz"
        data-dialogue="Am besten, du trägst erst mal deinen Namen ein."
        data-task="Trage deinen Namen in Zelle B1 ein.">
</section>
```

Beispiel Rudi:

```html
<section
        data-speaker="Rudi"
        data-avatar="pics/rudi.jpg"
        data-side="left"
        data-sound="sounds/bells.mp3"
        data-generate-sound="true"
        data-tts-voice="de-DE-KillianNeural"
        data-tts-rate="+6%"
        data-tts-pitch="+10Hz"
        data-dialogue="Startklar! Genau das wollte ich hören."
        data-task="">
</section>
```

---

## Verfügbare Stimmen prüfen

Im aktivierten Python-Venv:

```bash
edge-tts --list-voices | grep de-DE
```

Falls eine Stimme nicht existiert, eine andere aus dieser Liste wählen.

---

## TTS-Server

Der TTS-Server erzeugt MP3s dynamisch und cached sie im Ordner:

```text
generated_sounds/
```

Dadurch wird derselbe Satz nicht jedes Mal neu generiert.

Start:

```bash
python3 tts_server.py
```

Im Docker-Setup muss der Server auf `0.0.0.0` lauschen, damit er aus dem Browser erreichbar ist.

In `tts_server.py` sollte unten stehen:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)
```

Die URL wird in `index.html` gesetzt:

```js
window.CSCAPE_STORY = {
    ttsUrl: "http://127.0.0.1:8765/tts",
    defaultVoice: "de-DE-KatjaNeural"
};
```

---

## Timing von Text und Sound

Die Story-Engine wartet pro Slide auf alles, was läuft.

Im Textmodus:

```text
data-sound startet
data-dialogue wird getippt
erst wenn Sound UND Text fertig sind, gilt die Slide als fertig
```

Im Videomodus:

```text
dynamische TTS-MP3 startet
erst wenn die MP3 fertig ist, gilt die Slide als fertig
```

`data-auto-next-after="3"` bedeutet:

```text
Slide ist fertig → 3 Sekunden warten → nächste Slide
```

Nicht:

```text
Slide startet → 3 Sekunden warten → nächste Slide
```

Wenn ein CSCape-Check während Sound/Text fertig wird, wird der Slide-Wechsel blockiert, bis Sound/Text abgeschlossen ist.

---

## Musik

Hintergrundmusik wird in `window.CSCAPE_STORY` gesetzt:

```js
window.CSCAPE_STORY = {
    defaultMusic: "sounds/christmas.mp3",
    musicVolume: 0.28
};
```

Pro Slide kann die Musik überschrieben werden:

```html
<section
        data-music="sounds/anderer-track.mp3"
        data-music-volume="0.35">
</section>
```

---

## Hintergründe

Jeder Escape Room sollte ein Standard-Hintergrundbild haben:

```text
pics/background.jpg
```

Pro Slide kann ein anderer Hintergrund gesetzt werden:

```html
<section data-background="pics/werkstatt.jpg">
```

---

## Character-Bilder

Pro Slide:

```html
data-avatar="pics/elli.jpg"
```

Im Textmodus kann das ein Portrait sein.  
Im Videomodus wirkt es besser mit freigestellten Ganzkörper-PNGs.

Beispiel:

```html
data-avatar="pics/elli-fullbody.png"
```

---

## Aufgaben

Aufgaben werden über `data-task` gesetzt:

```html
data-task="Trage deinen Namen in Zelle B1 ein."
```

Im Textmodus erscheint die Aufgabe im Dialogkasten.  
Im Videomodus erscheint sie als große Aufgabenbox.

---

## Reveal.js

Lokale Kopie von:

```text
Reveal.js
```

---

## Optional

```bash
./run.sh
```

Startet CSCape automatisch im Browser/Kiosk-Modus.

---

## Docker

Der Container startet CSCape und den TTS-Server gemeinsam.

Wichtig beim Starten:

```bash
docker run -p 5000:5000 -p 8765:8765 sheetscape
```

Ports:

| Port | Zweck |
| ---- | ----- |
| `5000` | CSCape / Flask-Spiel |
| `8765` | TTS-Server |

---

## Projektstruktur

```text
cscape/
├── game.py
├── cscape.py
├── tts_server.py
├── index.html
├── revealjs-cscape.js
├── shared/
│   ├── cscape-story.css
│   └── cscape-story.js
├── reveal.js/
├── generated_sounds/
├── sounds/
└── pics/
```

---

## Hinweise

Das Spiel prüft absichtlich hauptsächlich Ergebniswerte statt exakter Formeltexte.

Die dynamische Sprachausgabe ist besonders praktisch für Texte mit `{player}` oder andere Inhalte, die sich erst während des Spiels ergeben.

---

## Idee hinter SheetScape

Das Projekt soll Spreadsheet-Grundlagen über ein kleines Story-Adventure vermitteln statt über klassische Tutorials.
