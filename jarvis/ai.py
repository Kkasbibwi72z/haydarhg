"""Anbindung an die Claude-API fuer freie Fragen, die kein eingebauter Befehl beantwortet."""

from __future__ import annotations

from jarvis.config import Config

SYSTEM_PROMPT = (
    "Du bist Jarvis, ein hilfsbereiter Sprachassistent. Antworte kurz, "
    "praezise und auf Deutsch, da deine Antworten vorgelesen werden."
)


class AIBackend:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = None
        if config.anthropic_api_key:
            from anthropic import Anthropic

            self._client = Anthropic(api_key=config.anthropic_api_key)

    @property
    def available(self) -> bool:
        return self._client is not None

    def ask(self, question: str) -> str:
        if not self._client:
            return (
                "Ich habe dafür keinen eingebauten Befehl und keinen "
                "ANTHROPIC_API_KEY, um die KI zu fragen."
            )
        response = self._client.messages.create(
            model=self._config.anthropic_model,
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}],
        )
        return "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()
