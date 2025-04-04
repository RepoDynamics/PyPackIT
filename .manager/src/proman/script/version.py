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


def run(metadata: dict, repo: str = "./") -> str:
    """Get the current project version."""
    cmd = [
        metadata["pypkg_main"]["dependency"]["build"]["versioning"]["import_name"],
        str(Path(repo).resolve() / metadata["pypkg_main"]["path"]["root"]),
        "--verbose"
    ]
    version = _pyshellman.run(
        command=[
            *_CMD_PREFIX, *cmd
        ],
        text_output=True,
    )
    return version.out


def run_cli(args: argparse.Namespace) -> int:
    version = run(metadata=args.metadata, repo=args.repo)
    print(version)
    return 0
