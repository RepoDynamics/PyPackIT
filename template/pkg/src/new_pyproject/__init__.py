from new_pyproject import data

__all__ = ["__version__", "__version_info__", "data"]

__version_info__: dict[str, str] = {"version": "0.0.0"}
"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_info__["version"]
"""Version number of the currently installed package."""
