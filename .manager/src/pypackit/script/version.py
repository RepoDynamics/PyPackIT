"""Get current project version."""

import argparse
import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

import ansi_sgr as sgr
import mdit
import pyshellman as _pyshellman
from gittidy import Git
from loggerman import logger

if TYPE_CHECKING:
    from typing import Literal

_CMD_PREFIX = ["conda", "run", "--name", "versioning", "--live-stream", "-vv"]
_METADATA = json.loads(Path(".github/.repodynamics/metadata.json").read_text())
_CMD = [
    _METADATA["pypkg_main"]["dependency"]["build"]["versioning"]["import_name"],
    _METADATA["pypkg_main"]["path"]["root"],
    "--verbose"
]


def run() -> str:
    """Get the current project version."""
    version = _pyshellman.run(
        command=[*_CMD_PREFIX, *_CMD],
        text_output=True,
    )
    return version.out


def run_cli(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    print(run())
    return 0
