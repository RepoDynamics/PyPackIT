"""Render package README file for PyPI.

This script takes one required positional argument: package ID to build.
The package ID is the suffix of the corresponding "pypkg_" key in the configuration.
For example, for a package with the key "pypkg_main", the package ID is "main".
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path

_CMD_PREFIX = ["conda", "run", "--name", "pybuild", "--live-stream", "-vv"]
_logger = logging.getLogger(__name__)


def run(pkg: str, metadata: dict, output: str | Path) -> Path | None:
    """Generate and run readme_renderer command."""
    pkg = metadata[f"pypkg_{pkg}"]
    readme_relpath = pkg["pyproject"]["project"].get("readme")
    if isinstance(readme_relpath, dict):
        readme_relpath = readme_relpath.get("file")
    if not readme_relpath:
        _logger.info("No README file found for package %s", pkg)
        return None
    readme_path = Path(pkg["path"]["root"]).resolve() / readme_relpath
    # Ensure the output folder exists
    output_file = Path(output).resolve() / f"{pkg['import_name']}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # Run readme-renderer
    subprocess.run(
        [*_CMD_PREFIX, "python", "-m", "readme_renderer", str(readme_path), "--output", str(output_file)],
        check=True,
        stdout=sys.stderr,
    )
    return output_file


def run_cli(args: argparse.Namespace) -> None:
    """Run the script from the command line."""

    output_path = run(
        pkg=args.pkg,
        metadata=args.metadata,
        output=args.output,
    )
    if output_path:
        print(output_path)
    sys.exit()
    return
