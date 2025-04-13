"""Exceptions raised by the data module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from new_pyproject.exception.main import PackageError

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["DataFileNotFoundError"]

class DataFileNotFoundError(PackageError):
    """Raised when a requested package data file is not found.

    Parameters
    ----------
    path_relative
        Path to the file relative to the package's data directory.
    path_absolute
        Absolute path to the file.
    """

    def __init__(
        self,
        path_relative: str,
        path_absolute: Path,
    ):
        self.path_relative = path_relative
        self.path_absolute = path_absolute
        super().__init__(
            "Could not find the requested package data file "
            f"'{path_relative}' at '{path_absolute}'.",
        )
        return
