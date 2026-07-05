"""Sprach-Ein-/Ausgabe fuer Jarvis (Mikrofon + Text-to-Speech)."""

from __future__ import annotations

from jarvis.config import Config


class SpeechIO:
    """Kapselt speech_recognition + pyttsx3, damit assistant.py davon unabhaengig bleibt."""

    def __init__(self, config: Config) -> None:
        import pyttsx3
        import speech_recognition as sr

        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", config.voice_rate)
        self._language = config.voice_language

        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

    def listen(self) -> str:
        import speech_recognition as sr

        with self._microphone as source:
            audio = self._recognizer.listen(source)
        try:
            return self._recognizer.recognize_google(audio, language=self._language)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            return f"[Fehler bei der Spracherkennung: {exc}]"

    def speak(self, text: str) -> None:
        self._engine.say(text)
        self._engine.runAndWait()


class TextIO:
    """Text-basierter Ersatz fuer SpeechIO, z.B. wenn kein Mikrofon verfuegbar ist."""

    def listen(self) -> str:
        try:
            return input("Du: ")
        except EOFError:
            return "beende"

    def speak(self, text: str) -> None:
        print(f"Jarvis: {text}")
