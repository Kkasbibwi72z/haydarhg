"""Kernlogik von Jarvis: hoert zu, erkennt den Wake-Word, fuehrt Befehle aus."""

from __future__ import annotations

from typing import Protocol

from jarvis.ai import AIBackend
from jarvis.commands import CommandRouter, ExitRequested
from jarvis.config import Config


class VoiceIO(Protocol):
    def listen(self) -> str: ...
    def speak(self, text: str) -> None: ...


class Jarvis:
    def __init__(
        self,
        config: Config,
        io: VoiceIO,
        router: CommandRouter | None = None,
        ai_backend: AIBackend | None = None,
    ) -> None:
        self._config = config
        self._io = io
        self._router = router or CommandRouter()
        self._ai = ai_backend or AIBackend(config)

    def _strip_wake_word(self, text: str) -> str | None:
        normalized = text.strip().lower()
        wake_word = self._config.wake_word.lower()
        if wake_word not in normalized:
            return None
        return normalized.split(wake_word, 1)[1].strip(" ,.:") or normalized

    def handle_utterance(self, text: str) -> str | None:
        """Verarbeitet eine einzelne Aeusserung und gibt die Antwort zurueck (oder None)."""
        command_text = self._strip_wake_word(text)
        if command_text is None:
            return None

        try:
            reply = self._router.route(command_text)
        except ExitRequested:
            raise

        if reply is None:
            reply = self._ai.ask(command_text)
        return reply

    def run_forever(self) -> None:
        self._io.speak(f"Jarvis ist bereit. Sag '{self._config.wake_word}', um mich zu aktivieren.")
        while True:
            heard = self._io.listen()
            if not heard:
                continue
            try:
                reply = self.handle_utterance(heard)
            except ExitRequested:
                self._io.speak("Auf Wiedersehen!")
                return
            if reply:
                self._io.speak(reply)
