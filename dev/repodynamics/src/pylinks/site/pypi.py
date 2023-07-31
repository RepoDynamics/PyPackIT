"""URLs for PyPI packages."""


# Standard libraries
import re
from typing import Optional

# Non-standard libraries
import requests
from pylinks import settings, url
from pylinks.url import URL


BASE_URL = url("https://pypi.org")


class Package:
    """A PyPI Python package."""

    def __init__(self, name: str, validate: Optional[bool] = None):
        """
        Parameters
        ----------
        name : str
            Name of the package.
        validate : bool, default: None
            Whether to validate the URL online (requires an active internet connection).
            If set to None (default), the global default value defined in `pylinks.OFFLINE_MODE` is used.
        """
        if not isinstance(name, str):
            raise TypeError(f"`name` must be a string, not {type(name)}.")
        if re.match("^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", name, flags=re.IGNORECASE) is None:
            raise ValueError(
                "Distribution name is invalid; see https://peps.python.org/pep-0508/#names."
            )
        self._name = name
        if validate is True or (validate is None and not settings.offline_mode):
            requests.get(str(self.homepage)).raise_for_status()

    @property
    def name(self) -> str:
        """Name of the package."""
        return self._name

    @property
    def homepage(self) -> URL:
        """URL of the package homepage."""
        return BASE_URL / "project" / self.name


def package(name: str, validate: Optional[bool] = None) -> Package:
    """
    Create a new URL generator for a PyPI package.

    Parameters
    ----------
    name : str
       Name of the package.
    validate : bool, default: None
       Whether to validate the URL online (requires an active internet connection).
       If set to None (default), the global default value defined in `pylinks.OFFLINE_MODE` is used.
    """
    return Package(name=name, validate=validate)
