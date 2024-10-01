"""Functions for retrieving package data files."""

from __future__ import annotations as _annotations

from pathlib import Path as _Path

import pkgdata as _pkgdata


__all__ = ["get"]


def get(relative_path: str) -> _Path:
    """Get the absolute path to a package data file.

    Parameters
    ----------
    relative_path
        Path to the file relative to the package's data directory.
    """
    path_data_dir = _Path(_pkgdata.get_package_path_from_caller(top_level=False))
    filepath = path_data_dir / relative_path
    if not filepath.is_file():
        from my_new_project.exception.data import DataFileNotFoundError

        raise DataFileNotFoundError(
            path_relative=relative_path,
            path_absolute=filepath,
        )
    return filepath
