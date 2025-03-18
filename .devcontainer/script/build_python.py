"""Build a python package in the project.

This script takes one required positional argument: package ID to build.
The package ID is the suffix of the corresponding "pypkg_" key in the configuration.
For example, for a package with the key "pypkg_main", the package ID is "main".

In addition, the script accepts any number of extra arguments.
These are passed directly to the `build` command.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

_METADATA = json.loads(Path(".github/.repodynamics/metadata.json").read_text())
_logger = logging.getLogger(__name__)


def main(
    pkg_id: str,
    out_dir: str | Path,
    extra_args: list[str] | None = None,
) -> Path:
    """Generate and run conda build command."""
    pkg = _METADATA[f"pypkg_{pkg_id}"]
    pkg_path = Path(pkg["path"]["root"]).resolve()
    # Ensure the output folder exists
    output_dir = Path(out_dir).resolve() / pkg["import_name"]
    output_dir.mkdir(parents=True, exist_ok=True)
    # Build command
    build_command = (
        [
            "python",
            "-m",
            "build",
            str(pkg_path),
            "--outdir",
            str(output_dir),
            "--verbose",
        ] + (extra_args or [])
    )
    _logger.info("Running Build Command: %s", shlex.join(build_command))
    # Execute the command
    subprocess.run(build_command, check=True, stdout=sys.stderr)  # noqa: S603
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
    subprocess.run(["twine", "check", str(output_dir / "*")], check=True, stdout=sys.stderr)  # noqa: S603
    return output_dir


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build a Python package in the project.")
    parser.add_argument(
        "out_dir", help="Output directory to write the rendered README file."
    )
    parser.add_argument(
        "pkg_id", help="Package ID, i.e., the 'pypkg_' key suffix in configuration files."
    )
    parser.add_argument(
        "extra_args", nargs=argparse.REMAINDER, help="Additional arguments for conda build."
    )
    args = vars(parser.parse_args())
    _logger.info("Input Arguments: %s", args)
    output_path = main(**args)
    print(output_path)
    sys.exit()
