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

_METADATA = json.loads(Path(".github/.repodynamics/metadata.json").read_text())
_logger = logging.getLogger(__name__)


def main(pkg_id: str, out_dir: str | Path) -> Path | None:
    """Generate and run readme_renderer command."""
    pkg = _METADATA[f"pypkg_{pkg_id}"]
    readme_relpath = pkg["pyproject"]["project"].get("readme")
    if isinstance(readme_relpath, dict):
        readme_relpath = readme_relpath.get("file")
    if not readme_relpath:
        _logger.info("No README file found for package %s", pkg_id)
        return None
    readme_path = Path(pkg["path"]["root"]).resolve() / readme_relpath
    # Ensure the output folder exists
    output_file = Path(out_dir).resolve() / f"{pkg['import_name']}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # Run readme-renderer
    subprocess.run(
        ["python", "-m", "readme_renderer", str(readme_path), "--output", str(output_file)],
        check=True,
        stdout=sys.stderr,
    )
    return output_file


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build a Python package in the project.")
    parser.add_argument("out_dir", help="Output directory to write the rendered README file.")
    parser.add_argument(
        "pkg_id", help="Package ID, i.e., the 'pypkg_' key suffix in configuration files."
    )
    args = vars(parser.parse_args())
    _logger.info("Input Arguments: %s", args)
    output_path = main(**args)
    if output_path:
        print(output_path)
    sys.exit()
