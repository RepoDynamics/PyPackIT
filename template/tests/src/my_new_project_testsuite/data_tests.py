"""Unit tests for the data sub-package."""

import pytest

import my_new_project as pkg
from my_new_project.exception.data import DataFileNotFoundError


def test_file():
    """Test the integrity of the `__test_file__` marker file.

    The marker file is used to indicate that the package data files are present.
    """
    marker = (
        "This is a test file used by our test suite "
        "to verify that package data is being included correctly."
    )
    filepath = pkg.data.filepath("__test_file__")
    assert filepath.read_text().rstrip() == marker


def test_no_file():
    """Test that an error is raised when the input data file is missing."""
    with pytest.raises(DataFileNotFoundError):
        pkg.data.filepath("path/to/nonexistent/file")
