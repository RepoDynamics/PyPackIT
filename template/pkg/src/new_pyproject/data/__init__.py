"""Functions for retrieving package data files."""

from __future__ import annotations

from pathlib import Path

import pkgdata

__all__ = ["filepath"]


def filepath(relative_path: str) -> Path:
    """Get the absolute path to a package data file.

    Parameters
    ----------
    relative_path
        Path to the file relative to the package's data directory.
    """
    path_data_dir = Path(pkgdata.get_package_path_from_caller(top_level=False))
    abs_filepath = path_data_dir / relative_path
    if not abs_filepath.is_file():
        from new_pyproject.exception.data import DataFileNotFoundError

        raise DataFileNotFoundError(
            path_relative=relative_path,
            path_absolute=abs_filepath,
        )
    return abs_filepath
