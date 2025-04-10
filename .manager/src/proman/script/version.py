"""Get current project version."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loggerman import logger
import pyshellman

if TYPE_CHECKING:
    from proman.manager import Manager


_CMD_PREFIX = ["conda", "run", "--name", "versioning", "--live-stream", "-vv"]


def run(manager: Manager) -> str:
    """Get current project version."""
    cmd = [
        manager.data["pypkg_main.dependency.build.versioning.import_name"],
        str(manager.git.repo_path / manager.data["pypkg_main.path.root"]),
        "--verbose"
    ]
    version = pyshellman.run(
        command=[
            *_CMD_PREFIX, *cmd
        ],
        text_output=True,
        logger=logger,
    )
    return version.out


def run_cli(args: dict) -> None:
    """Run from CLI."""
    version = run(manager=args["manager"])
    print(version)
    return
