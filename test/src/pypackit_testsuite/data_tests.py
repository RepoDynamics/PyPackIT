# PyPackIT-TestSuite © 2023–2024 RepoDynamics
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Unit tests for the data sub-package."""

import pytest

import pypackit.data as pkg_data
from pypackit.exception.data import DataFileNotFoundError


def test_file() -> None:
    """Test the integrity of the `__test_file__` marker file.

    The marker file is used to indicate that the package data files are present.
    """
    marker = (
        "This is a test file used by our test suite "
        "to verify that package data is being included correctly."
    )
    filepath = pkg_data.filepath("__test_file__")
    assert filepath.read_text().rstrip() == marker


def test_no_file() -> None:
    """Test that an error is raised when the input data file is missing."""
    with pytest.raises(DataFileNotFoundError):
        pkg_data.filepath("path/to/nonexistent/file")
