"""Render package README file for PyPI.

This script takes one required positional argument: package ID to build.
The package ID is the suffix of the corresponding "pypkg_" key in the configuration.
For example, for a package with the key "pypkg_main", the package ID is "main".
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from loggerman import logger

if TYPE_CHECKING:
    from proman.manager import Manager

_CMD_PREFIX = ["conda", "run", "--name", "pybuild", "--live-stream", "-vv"]


def run(manager: Manager, pkg: str, output: str | Path) -> Path | None:
    """Generate and run readme_renderer command."""
    pkg = manager.data[f"pypkg_{pkg}"]
    readme_relpath = pkg["pyproject"]["project"].get("readme")
    if isinstance(readme_relpath, dict):
        readme_relpath = readme_relpath.get("file")
    if not readme_relpath:
        logger.info(f"No README file found for package {pkg}")
        return None
    readme_path = manager.git.repo_path / pkg["path"]["root"] / readme_relpath
    # Ensure the output folder exists
    output_file = Path(output).resolve() / f"{pkg['import_name']}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # Run readme-renderer
    subprocess.run(
        [
            *_CMD_PREFIX,
            "python",
            "-m",
            "readme_renderer",
            str(readme_path),
            "--output",
            str(output_file),
        ],
        check=True,
        stdout=sys.stderr,
    )
    return output_file


def run_cli(args: dict) -> None:
    """Run from CLI."""
    output_path = run(
        manager=args["manager"],
        pkg=args["pkg"],
        output=args["output"],
    )
    if output_path:
        print(output_path)
    return
