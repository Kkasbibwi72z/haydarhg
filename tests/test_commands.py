import pytest

from jarvis.commands import CommandRouter, ExitRequested


@pytest.fixture
def router() -> CommandRouter:
    return CommandRouter()


def test_time_command(router: CommandRouter) -> None:
    assert "Uhr" in router.route("wie spät ist es")


def test_date_command(router: CommandRouter) -> None:
    assert "Heute ist der" in router.route("welches datum haben wir")


def test_joke_command(router: CommandRouter) -> None:
    assert router.route("erzähl mir einen witz")


def test_unknown_command_returns_none(router: CommandRouter) -> None:
    assert router.route("wie ist das Wetter auf dem Mars") is None


def test_exit_raises(router: CommandRouter) -> None:
    with pytest.raises(ExitRequested):
        router.route("beende dich bitte")
