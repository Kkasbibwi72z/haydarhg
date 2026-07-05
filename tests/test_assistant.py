import pytest

from jarvis.assistant import Jarvis
from jarvis.commands import ExitRequested
from jarvis.config import Config


class FakeIO:
    def __init__(self, inputs: list[str]) -> None:
        self._inputs = iter(inputs)
        self.spoken: list[str] = []

    def listen(self) -> str:
        return next(self._inputs, "beende")

    def speak(self, text: str) -> None:
        self.spoken.append(text)


class FakeAI:
    def ask(self, question: str) -> str:
        return f"KI-Antwort auf: {question}"


@pytest.fixture
def config() -> Config:
    return Config(wake_word="jarvis")


def test_ignores_utterance_without_wake_word(config: Config) -> None:
    jarvis = Jarvis(config, FakeIO([]), ai_backend=FakeAI())
    assert jarvis.handle_utterance("wie spät ist es") is None


def test_builtin_command_after_wake_word(config: Config) -> None:
    jarvis = Jarvis(config, FakeIO([]), ai_backend=FakeAI())
    reply = jarvis.handle_utterance("jarvis, welches datum haben wir")
    assert "Heute ist der" in reply


def test_falls_back_to_ai(config: Config) -> None:
    jarvis = Jarvis(config, FakeIO([]), ai_backend=FakeAI())
    reply = jarvis.handle_utterance("jarvis wie ist das Wetter auf dem Mars")
    assert reply.startswith("KI-Antwort auf:")


def test_exit_word_stops_loop(config: Config) -> None:
    jarvis = Jarvis(config, FakeIO([]), ai_backend=FakeAI())
    with pytest.raises(ExitRequested):
        jarvis.handle_utterance("jarvis beende dich")
