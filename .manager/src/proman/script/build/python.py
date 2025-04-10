"""Build a python package in the project.

This script takes one required positional argument: package ID to build.
The package ID is the suffix of the corresponding "pypkg_" key in the configuration.
For example, for a package with the key "pypkg_main", the package ID is "main".

In addition, the script accepts any number of extra arguments.
These are passed directly to the `build` command.
"""

from __future__ import annotations

import logging
import shlex
import subprocess
import sys
from pathlib import Path

_CMD_PREFIX = ["conda", "run", "--name", "pybuild", "--live-stream", "-vv"]
_logger = logging.getLogger(__name__)


def run(
    pkg: str,
    metadata: dict,
    output: str | Path,
    args: list[str] | None = None,
) -> Path:
    """Generate and run build command."""
    pkg = metadata[f"pypkg_{pkg}"]
    pkg_path = Path(pkg["path"]["root"]).resolve()
    # Ensure the output folder exists
    output_dir = Path(output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    # Build command
    build_command = [
        *_CMD_PREFIX,
        "python",
        "-m",
        "build",
        str(pkg_path),
        "--outdir",
        str(output_dir),
        "--verbose",
    ] + (args or [])
    _logger.info("Running Build Command: %s", shlex.join(build_command))
    # Execute the command
    subprocess.run(build_command, check=True, stdout=sys.stderr)
    # Run twine check
    # Note:
    #    `twine check` (https://twine.readthedocs.io/en/stable/#twine-check) only works for
    #    reStructuredText (reST) READMEs; it always passes for Markdown content
    #    (cf. `twine.commands.check._RENDERERS` (https://github.com/pypa/twine/blob/4f7cd66fa1ceba7f8de5230d3d4ebea0787f17e5/twine/commands/check.py#L32-L37))
    #    and thus cannot be used to validate Markdown.
    #    It is used here only to check the existence of the README file in the built distributions.
    # Refs:
    #    https://twine.readthedocs.io/en/stable/#twine-check
    #    https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/#validating-restructuredtext-markup
    subprocess.run([*_CMD_PREFIX, "twine", "check", str(output_dir / "*")], check=True, stdout=sys.stderr)
    return output_dir


def run_cli(args: dict) -> None:
    """Run from CLI."""
    output_path = run(
        pkg=args["pkg"],
        metadata=args["metadata"],
        output=args["output"],
        args=args["args"],
    )
    print(output_path)
    return
