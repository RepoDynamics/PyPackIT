"""URLs for Conda packages."""


# Standard libraries
import re
from typing import Optional

# Non-standard libraries
import requests
from pylinks import settings, url
from pylinks.url import URL


BASE_URL = url(url="https://anaconda.org")


class Package:
    """A Conda package."""

    def __init__(self, name: str, channel: str = "conda-forge", validate: Optional[bool] = None):
        """
        Parameters
        ----------
        name : str
            Name of the package.
        channel : str, default: 'conda-forge'
            The channel hosting the package.
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
        self._channel = channel
        if validate is True or (validate is None and not settings.offline_mode):
            requests.get(str(self.homepage)).raise_for_status()

    def __repr__(self):
        return f"conda.Package(name={self.name}, channel={self.channel}) @ {self.homepage}"

    def __str__(self):
        return str(self.homepage)

    @property
    def name(self) -> str:
        """Name of the package."""
        return self._name

    @property
    def channel(self) -> str:
        """Name of the channel hosting the package."""
        return self._channel

    @property
    def homepage(self) -> URL:
        """URL of the package homepage."""
        return BASE_URL / self.channel / self.name


def package(name: str, channel: str, validate: Optional[bool] = None) -> Package:
    """
    Create a new URL generator for a Conda package.

    Parameters
    ----------
    name : str
        Name of the package.
    channel : str, default: 'conda-forge'
        The channel hosting the package.
    validate : bool, default: None
        Whether to validate the URL online (requires an active internet connection).
        If set to None (default), the global default value defined in `pylinks.OFFLINE_MODE` is used.
    """
    return Package(name=name, channel=channel, validate=validate)
