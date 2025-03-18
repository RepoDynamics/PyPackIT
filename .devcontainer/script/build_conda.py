"""Build a conda package in the project.

This script takes two required positional arguments: the package version and ID to build.
The package ID is the suffix of the corresponding "pypkg_" key in the configuration.
For example, for a package with the key "pypkg_main", the package ID is "main".

In addition, the script accepts any number of extra arguments.
These are passed directly to the `conda build` command.
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
    pkg_version: str,
    pkg_id: str,
    out_dir: str | Path,
    recipe_type: Literal["global", "local"] = "local",
    extra_args: list[str] | None = None,
) -> Path:
    """Generate and run conda build command."""
    recipe = get_recipe(pkg_id=pkg_id)
    channels = get_channels(recipe)
    # Ensure the output folder exists
    output_dir = Path(out_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    # Export package version
    os.environ["PKG_FULL_VERSION"] = pkg_version
    # Build command
    build_command = (
        [
            "conda",
            "build",
            str(Path(recipe["path"][recipe_type]).resolve()),
            "--output-folder",
            str(output_dir),
            "--stats-file",
            str(output_dir / "build-stats.json"),
            "--package-format",
            "conda",
            "--verify",
            "--keep-going",
            "--debug",
            "--no-anaconda-upload",
        ]
        + [arg for channel in channels for arg in ("--channel", channel)]
        + (extra_args or [])
    )
    _logger.info("Running Build Command: %s", shlex.join(build_command))
    # Execute the command
    subprocess.run(build_command, check=True, stdout=sys.stderr)  # noqa: S603
    return output_dir


def get_recipe(pkg_id: str) -> dict:
    """Get the conda recipe of a package."""
    key = f"pypkg_{pkg_id}"
    recipe = _METADATA.get(key, {}).get("conda", {}).get("recipe")
    if not recipe:
        error_msg = f"No conda recipe found in metadata at '{key}.conda.recipe'."
        raise ValueError(error_msg)
    return recipe


def get_channels(recipe: dict) -> list[str]:
    """Get a list of channels used in a recipe.

    Notes
    -----
    Channels used in the recipe but not set in conda configurations
    must be manually added, otherwise conda build cannot solve the dependencies. See:
    - https://github.com/conda/conda-build/issues/5597
    - https://github.com/conda/conda/issues/988
    """

    def update_channel_priority(requirement: str) -> None:
        parts = requirement.split("::")
        if len(parts) > 1:
            channel = parts[0]
            channel_priority[channel] = channel_priority.get(channel, 0) + 1
        return

    meta = recipe.get("meta", {}).get("values", {})
    channel_priority = {}
    for key in ("host", "run", "run_constrained"):
        for req in meta.get("requirements", {}).get("values", {}).get(key, {}).get("values", []):
            update_channel_priority(req["value"])
    for req in meta.get("test", {}).get("values", {}).get("requires", {}).get("values", []):
        update_channel_priority(req["value"])
    return sorted(channel_priority, key=channel_priority.get, reverse=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build a Conda package in the project.")
    parser.add_argument(
        "out_dir", help="Output directory to write the rendered README file."
    )
    parser.add_argument("pkg_version", help="Version number to pass to the recipe.")
    parser.add_argument(
        "pkg_id", help="Package ID, i.e., the 'pypkg_' key suffix in configuration files."
    )
    parser.add_argument(
        "recipe_type",
        nargs="?",
        choices=["local", "global"],
        default="local",
        help="Type of recipe to use (default: 'local')",
    )
    parser.add_argument(
        "extra_args", nargs=argparse.REMAINDER, help="Additional arguments for conda build."
    )
    args = vars(parser.parse_args())
    _logger.info("Input Arguments: %s", args)
    local_channel_path = main(**args)
    print(local_channel_path)
    sys.exit()
