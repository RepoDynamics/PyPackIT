"""Functions for retrieving package data files."""

from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import pkgdata as _pkgdata

if _TYPE_CHECKING:
    from pathlib import Path

__all__ = ["get"]


def get(relative_path: str) -> Path:
    """Get the absolute path to a package data file.

    Parameters
    ----------
    relative_path
        Path to the file relative to the package's data directory.
    """
    path_data_dir = _pkgdata.get_package_path_from_caller(top_level=False)
    filepath = path_data_dir / relative_path
    if not filepath.is_file():
        from my_new_project.exception.data import DataFileNotFoundError

        raise DataFileNotFoundError(
            path_relative=relative_path,
            path_absolute=filepath,
        )
    return filepath
