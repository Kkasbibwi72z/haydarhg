"""Eingebaute Befehle fuer Jarvis.

Jeder Handler bekommt den erkannten Text (bereits vom Wake-Word befreit)
und liefert entweder eine Antwort (str) oder None, wenn er nicht zustaendig
ist. Passt kein eingebauter Befehl, wird die Anfrage an die KI weitergereicht.
"""

from __future__ import annotations

import datetime
import random
import webbrowser
from dataclasses import dataclass
from typing import Callable, Optional

CommandHandler = Callable[[str], Optional[str]]

_WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
}

_JOKES = [
    "Ich wollte einen Witz über UDP erzählen, aber ich bin nicht sicher, ob er ankommt.",
    "Warum weinen Roboter nicht? Weil sie keine Tränen-Treiber installiert haben.",
    "Es gibt 10 Arten von Menschen: die, die Binär verstehen, und die, die es nicht tun.",
]


class ExitRequested(Exception):
    """Wird ausgeloest, wenn der Nutzer den Assistenten beenden moechte."""


def handle_exit(text: str) -> Optional[str]:
    if any(word in text for word in ("beende", "stop", "tschüss", "auf wiedersehen", "exit", "quit")):
        raise ExitRequested()
    return None


def handle_time(text: str) -> Optional[str]:
    if "uhrzeit" in text or "wie spät" in text or "wieviel uhr" in text:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"Es ist {now} Uhr."
    return None


def handle_date(text: str) -> Optional[str]:
    if "datum" in text or "welcher tag" in text:
        today = datetime.date.today().strftime("%d.%m.%Y")
        return f"Heute ist der {today}."
    return None


def handle_open_website(text: str) -> Optional[str]:
    if "öffne" in text or "starte" in text:
        for name, url in _WEBSITES.items():
            if name in text:
                webbrowser.open(url)
                return f"Ich öffne {name}."
    return None


def handle_joke(text: str) -> Optional[str]:
    if "witz" in text:
        return random.choice(_JOKES)
    return None


DEFAULT_HANDLERS: tuple[CommandHandler, ...] = (
    handle_exit,
    handle_time,
    handle_date,
    handle_open_website,
    handle_joke,
)


@dataclass
class CommandRouter:
    """Probiert eingebaute Handler der Reihe nach aus."""

    handlers: tuple[CommandHandler, ...] = DEFAULT_HANDLERS

    def route(self, text: str) -> Optional[str]:
        normalized = text.strip().lower()
        for handler in self.handlers:
            result = handler(normalized)
            if result is not None:
                return result
        return None
