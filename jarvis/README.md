# Jarvis

Ein kleiner Sprachassistent im Iron-Man-Stil: Browser-HUD (Arc-Reactor-Optik)
mit Sprach-Ein-/Ausgabe, das über einen lokalen Node-Server läuft.

## Starten

```bash
cd jarvis
npm install
npm start
```

Dann `http://localhost:4000` in **Chrome** öffnen (Web Speech API wird
aktuell nur dort zuverlässig unterstützt) und Mikrofonzugriff erlauben.

Taste gedrückt halten (oder Leertaste) zum Sprechen, loslassen zum Senden.

## Wie es aufgebaut ist

- `server.js` – lokaler Server, nimmt Text vom Browser per WebSocket entgegen
  und schickt eine Antwort zurück.
- `brain.js` – die "Denk-Logik". Aktuell eine einfache Stichwort-Erkennung
  als Platzhalter.
- `public/` – die HUD-Oberfläche (HTML/CSS/JS), Spracherkennung
  (SpeechRecognition) und Sprachausgabe (SpeechSynthesis) laufen im Browser.

## Echtes Claude-Gehirn anschließen

Aktuell antwortet Jarvis nur auf ein paar feste Stichwörter. Um ihn mit
echtem Sprachverständnis auszustatten:

1. API-Key unter https://console.anthropic.com erstellen.
2. `jarvis/.env` anlegen mit `ANTHROPIC_API_KEY=dein-key` (wird nicht
   eingecheckt, siehe `.gitignore`).
3. In `brain.js` die `think()`-Funktion durch einen Aufruf des
   `@anthropic-ai/sdk` ersetzen, der den Nutzertext an Claude schickt und die
   Antwort zurückgibt.

## Bekannte Einschränkungen

- Die Stimme ist die des Browsers (SpeechSynthesis) – klingt nicht wie die
  echte Jarvis-Stimme aus Iron Man. Für eine hochwertigere Stimme später ein
  TTS wie ElevenLabs oder OpenAI TTS anbinden (braucht eigenen API-Key).
- Keine Steuerung anderer Programme (z.B. Roblox Studio) – das ist bewusst
  nicht Teil dieser Version.
