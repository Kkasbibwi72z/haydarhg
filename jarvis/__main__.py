"""Einstiegspunkt: python -m jarvis [--text]"""

from __future__ import annotations

import argparse
import sys

from jarvis.assistant import Jarvis
from jarvis.config import Config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Jarvis Sprachassistent")
    parser.add_argument(
        "--text",
        action="store_true",
        help="Text-Modus statt Mikrofon/Lautsprecher verwenden (z.B. ohne Audio-Hardware).",
    )
    args = parser.parse_args(argv)

    config = Config.from_env()

    if args.text:
        from jarvis.speech import TextIO

        io = TextIO()
    else:
        from jarvis.speech import SpeechIO

        io = SpeechIO(config)

    Jarvis(config, io).run_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
