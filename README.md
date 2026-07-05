# haydarhg

## Jarvis – Sprachassistent in Python

Ein einfacher Sprachassistent nach dem Vorbild von Jarvis (Iron Man). Er hört
auf ein Wake-Word ("Jarvis"), führt eingebaute Befehle aus (Uhrzeit, Datum,
Webseite öffnen, Witz erzählen, beenden) und leitet alles andere an die
Claude-API weiter, sofern ein API-Key konfiguriert ist.

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`PyAudio` benötigt auf manchen Systemen zusätzlich `portaudio` (z.B. `apt
install portaudio19-dev` unter Linux, `brew install portaudio` unter macOS).

### Konfiguration

Kopiere `.env.example` nach `.env` und trage optional deinen
`ANTHROPIC_API_KEY` ein, damit Jarvis auch Fragen beantworten kann, die kein
eingebauter Befehl abdeckt.

### Starten

Mit Mikrofon und Lautsprecher:

```bash
python -m jarvis
```

Ohne Audio-Hardware (Text-Eingabe/-Ausgabe im Terminal, z.B. zum Testen):

```bash
python -m jarvis --text
```

Beispiel-Dialog im Textmodus:

```
Du: jarvis wie spät ist es
Jarvis: Es ist 14:32 Uhr.
Du: jarvis erzähl mir einen witz
Jarvis: ...
Du: jarvis beende dich
Jarvis: Auf Wiedersehen!
```

### Tests

```bash
pytest
```

### Projektstruktur

```
jarvis/
  __main__.py   Einstiegspunkt (python -m jarvis)
  assistant.py  Kernlogik: Wake-Word-Erkennung, Steuerung des Dialogs
  commands.py   Eingebaute Befehle (Uhrzeit, Datum, Webseite, Witz, Beenden)
  ai.py         Fallback an die Claude-API für freie Fragen
  speech.py     Mikrofon/Lautsprecher (SpeechIO) bzw. Text-Ein-/Ausgabe (TextIO)
  config.py     Konfiguration aus Umgebungsvariablen
tests/          Unit-Tests für Befehle und Dialoglogik
```
