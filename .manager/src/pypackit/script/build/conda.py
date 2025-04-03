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

import pypackit.script.version as _script_version

if TYPE_CHECKING:
    from typing import Literal

_CMD_PREFIX = ["conda", "run", "--name", "base", "--live-stream", "-vv"]
_logger = logging.getLogger(__name__)


def run(
    pkg: str,
    metadata: dict,
    output: str | Path,
    repo: str | Path = "./",
    recipe: Literal["global", "local"] = "local",
    args: list[str] | None = None,
) -> Path:
    """Generate and run conda build command to build a package.

    Parameters
    ----------
    pkg
        Package ID, i.e., the 'pypkg_' key suffix in configuration files.
    output
        Path to a directory where the local conda channel will be created.
    recipe
        Type of recipe to use (default: 'local').
    args
        Additional arguments for conda build.

    Returns
    -------
    Path to the local conda channel.
    """
    def get_recipe(pkg_id: str) -> dict:
        """Get the conda recipe of a package."""
        key = f"pypkg_{pkg_id}"
        recipe = metadata.get(key, {}).get("conda", {}).get("recipe")
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
        channel_priority: dict[str, int] = {}
        for key in ("host", "run", "run_constrained"):
            for req in meta.get("requirements", {}).get("values", {}).get(key, {}).get("values", []):
                update_channel_priority(req["value"])
        for req in meta.get("test", {}).get("values", {}).get("requires", {}).get("values", []):
            update_channel_priority(req["value"])
        return sorted(channel_priority, key=channel_priority.get, reverse=True)

    recipe = get_recipe(pkg_id=pkg)
    channels = get_channels(recipe)
    # Ensure the output folder exists
    output_dir = Path(output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    # Export package version
    pkg_version = _script_version.run(metadata=metadata, repo=repo)
    os.environ["PKG_FULL_VERSION"] = pkg_version
    # Build command
    build_command = (
        [
            *_CMD_PREFIX,
            "conda",
            "build",
            str(Path(recipe["path"][recipe]).resolve()),
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
        + (args or [])
    )
    _logger.info("Running Build Command: %s", shlex.join(build_command))
    # Execute the command
    subprocess.run(build_command, check=True, stdout=sys.stderr)
    return output_dir


def run_cli(args: argparse.Namespace) -> int:
    """Run the CLI.

    Parameters
    ----------
    args : argparse.Namespace, optional
        The parsed arguments. If None, the arguments are parsed from sys.argv.
    Returns
    -------
    int
        The exit code of the program.
    """
    local_channel_path = run(
        pkg=args.pkg,
        metadata=args.metadata,
        repo=args.repo,
        output=args.output,
        recipe=args.recipe,
        args=args.args,
    )
    print(local_channel_path)
    return 0
