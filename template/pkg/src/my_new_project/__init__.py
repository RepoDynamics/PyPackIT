from my_new_project import data

__all__ = ["data", "__version_details__", "__version__"]

__version_details__: dict[str, str | tuple] = {"version": "0.0.0"}
"""Details of the currently installed version of the package,
including version number, date, branch, and commit hash."""

__version__: str = __version_details__["version"]
"""Version number of the currently installed package."""
