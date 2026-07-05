"""Konfiguration fuer Jarvis, geladen aus Umgebungsvariablen."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Config:
    wake_word: str = "jarvis"
    voice_rate: int = 180
    voice_language: str = "de-DE"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-5"

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            wake_word=os.environ.get("JARVIS_WAKE_WORD", cls.wake_word),
            voice_rate=int(os.environ.get("JARVIS_VOICE_RATE", cls.voice_rate)),
            voice_language=os.environ.get("JARVIS_LANGUAGE", cls.voice_language),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            anthropic_model=os.environ.get("ANTHROPIC_MODEL", cls.anthropic_model),
        )
