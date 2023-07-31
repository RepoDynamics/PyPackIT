"""
Dynamically create badges for PyPI package downloads, using the pepy.tech API.

References
----------
* https://pepy.tech/
"""


# Standard libraries
from typing import Literal, Optional, Sequence

# Non-standard libraries
from pybadgeit import _badge
from pylinks import url
from pylinks.url import URL


_BASE_URL = url("https://static.pepy.tech")


class PePyBadge(_badge.Badge):
    """PePy badge for PyPI package downloads."""

    def __init__(
        self,
        path: str,
        left_text: str = None,
        left_color_light: str = None,
        left_color_dark: str = None,
        right_color_light: str = None,
        right_color_dark: str = None,
        units: Literal["international_system", "abbreviation", "none"] = "international_system",
        alt: str = None,
        title: str = None,
        width: str = None,
        height: str = None,
        align: str = None,
        link: str | URL = None,
        default_theme: Literal["light", "dark"] = "dark",
    ):
        """
        Parameters
        ----------
        path : pylinks.URL
            Clean URL (without additional queries) of the badge image.
        left_text : str
            Text on the left-hand side of the badge. Pass an empty string to omit the left side.
        right_text : str
            Text on the right-hand side of the badge. This can only be set for static badges.
            When `left_text` is set to empty string, this will be the only text shown.
        left_color_light : str
            Color of the left side. See `logo_color` for more detail.
        right_color_dark : str
            Color of the right side. See `logo_color` for more detail.
        units : {'international_system', 'abbreviation', 'none'}, default: 'international_system'
            Formatting of the number of downloads.
        """
        super().__init__(
            alt=alt,
            title=title,
            width=width,
            height=height,
            align=align,
            link=link,
            default_theme=default_theme,
        )
        self._url: URL = url(str(path))
        self.left_text: str = left_text
        self.left_color_light: str = left_color_light
        self.left_color_dark: str = left_color_dark
        self.right_color_light: str = right_color_light
        self.right_color_dark: str = right_color_dark
        self.units = units
        return

    def url(self, mode: Literal["light", "dark", "clean"] = "dark") -> URL:
        """
        URL of the badge image.

        Parameters
        ----------
        mode : {'dark', 'light', 'clean'}
            'dark' and 'light' provide the URL of the badge image customized for dark and light themes,
            respectively, while 'clean' gives the URL of the badge image without any customization.

        Returns
        -------
        url : pylinks.url.URL
            A URL object, which among others, has a __str__ method to output the URL as a string.
        """
        url = self._url.copy()
        if mode == "clean":
            return url
        for key, val in (
            ("units", self.units),
            ("left_text", self.left_text),
            ("left_color", self.left_color_dark if mode == "dark" else self.left_color_light),
            ("right_color", self.right_color_dark if mode == "dark" else self.right_color_light),
        ):
            if val is not None:
                url.queries[key] = val
        return url


def pypi_downloads(
    package_name: str, period: Literal["total", "month", "week"] = "total"
) -> PePyBadge:
    """
    Number of downloads for a PyPI package.

    Parameters
    ----------
    package_name : str
        Name of the package.
    period : {'total', 'month', 'week'}, default: 'total'
        The period to query.
    """
    path = _BASE_URL / "personalized-badge" / package_name
    path.queries["period"] = period
    left_text = "Total Downloads" if period == "total" else f"Downloads/{period.capitalize()}"
    return PePyBadge(
        path=path,
        left_text=left_text,
        left_color_dark="grey",
        left_color_light="grey",
        link=url(f"https://pepy.tech/project/{package_name}?display=monthly"),
    )
