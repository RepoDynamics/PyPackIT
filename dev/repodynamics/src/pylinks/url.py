"""Create and modify URLs."""


# Standard libraries
import re
import urllib
import webbrowser
from typing import Literal, Optional


class URL:
    """A URL with a base address, and optional queries and fragment."""

    def __init__(
        self,
        base: str,
        queries: Optional[dict[str, str | bytes | None]] = None,
        fragment: Optional[str] = None,
        quote_safe: Optional[str] = "",
        query_delimiter: str = "&",
    ):
        """
        Parameters
        ----------
        base : str
            The base URL, e.g. 'https://example.com/index'.
            It must start with either 'https://' or 'http://'.
        queries : dict[str, str | has_str | bytes | None], optional
            Optional query fields as a dictionary of key-value pairs, e.g. `{'title': 'my-title'}`.
            The values can be strings, or objects that implement the __str__ method.
            Alternatively, they can be bytes, in which case the content will be decoded using UTF-8, but not quoted.
            If the value is None, only the key will be included in the query string.
        fragment : str, optional
            Optional fragment at the end of URL, i.e. after the '#' symbol.
        quote_safe : str, default: ''
            Characters that should not be quoted in the URL.
            For more control, query values that should not be quoted at all can be passed as bytes.
        query_delimiter : str, default: '&'
            Delimiter for the query string.
        """
        self.base = base
        self.queries = queries or dict()
        self.fragment = fragment
        self.query_delimiter = query_delimiter
        self.quote_safe = quote_safe
        return

    def __str__(self):
        """The full URL, e.g. 'https://example.com/index?title=my-title&style=bold'"""
        url = self.base
        if self.query_string:
            url += f"?{self.query_string}"
        if self.fragment:
            url += f"#{self.fragment}"
        return url

    def __truediv__(self, path):
        """
        Add a path at the end of the base URL (while preserving the query string and fragment),
        and return a new copy.
        """
        if not isinstance(path, str):
            raise TypeError("Adding a path can only be performed on strings.")
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return URL(
            base=f"{self.base}/{path}",
            queries=self.queries.copy(),
            fragment=self.fragment,
            query_delimiter=self.query_delimiter,
            quote_safe=self.quote_safe,
        )

    def __repr__(self):
        repr = f"URL(base={self.base}"
        if self.queries:
            repr += f", queries={self.queries}"
        if self.fragment:
            repr += f", fragment={self.fragment}"
        return f"{repr})"

    def __copy__(self):
        return URL(
            base=self.base,
            queries=self.queries.copy(),
            fragment=self.fragment,
            query_delimiter=self.query_delimiter,
            quote_safe=self.quote_safe,
        )

    @property
    def query_string(self) -> str | None:
        """The complete query string, e.g. 'title=my-title&style=bold'"""
        if not self.queries:
            return
        queries = []
        for key, val in self.queries.items():
            if val is None:
                continue
            q_key = urllib.parse.quote(str(key), safe=self.quote_safe)
            if isinstance(val, bool) and val is True:
                queries.append(q_key)
            else:
                q_val = (
                    val.decode("utf8")
                    if isinstance(val, bytes)
                    else urllib.parse.quote(str(val), safe=self.quote_safe)
                )
                queries.append(f"{q_key}={q_val}")
        return self.query_delimiter.join(queries)

    def add_path(self, path: str) -> None:
        """
        Add a path to the end of the base URL, while preserving the query string and fragment.
        This modifies the current instance in place.
        """
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        self.base += f"/{path}"
        return

    def copy(self) -> "URL":
        """Create a new copy."""
        return self.__copy__()

    def open(self, new: Literal[0, 1, 2] = 2, autoraise: bool = True) -> None:
        """
        Open the URL in the default browser.

        Parameters
        ----------
        new : {0, 1, 2}, default: 2
            Whether to open the webpage in the same browser window (0),
            a new window (1), or a new tab (2), when possible.
        autoraise : bool, default: True
            Whether to raise the window (i.e. bring to front) after opening.
        """
        webbrowser.open(url=str(self), new=new, autoraise=autoraise)


def url(
    url: str,
    queries: Optional[dict[str, str | bytes | None]] = None,
    fragment: Optional[str] = None,
    quote_safe: Optional[str] = "",
    query_delimiter: str = "&",
) -> URL:
    """
    Create a new URL.

    Parameters
    ----------
    url : str
        A URL, which may or may not contain a query string and/or a fragment.
    queries : dict[str, str | has_str | bytes | None], optional
        Optional query fields as a dictionary of key-value pairs, e.g. `{'title': 'my-title'}`.
        The values can be strings, or objects that implement the __str__ method.
        Alternatively, they can be bytes, in which case the content will be decoded using UTF-8, but not quoted.
        If the value is None, only the key will be included in the query string.
        The values given here will override the corresponding values in the query string of the input url.
    fragment : str, optional
        Optional fragment at the end of URL, i.e. after the '#' symbol.
        The value given here will override the corresponding fragment in the input url.
    quote_safe : str, default: ''
        Characters that should not be quoted in the URL.
        For more control, query values that should not be quoted at all can be passed as bytes.
    query_delimiter : str, default: '&'
        Delimiter for the query string.
    """
    base, base_queries, base_fragment = _process_url(url, query_delimiter=query_delimiter)
    queries = base_queries | queries if queries else base_queries
    fragment = fragment if fragment else base_fragment
    return URL(
        base=base,
        queries=queries,
        fragment=fragment,
        quote_safe=quote_safe,
        query_delimiter=query_delimiter,
    )


def _process_url(url: str, query_delimiter: str = "&") -> tuple[str, dict[str, str], str]:
    """
    Process a URL and separate the base, query string and fragment.

    Parameters
    ----------
    url : str
        URL to process
    query_delimiter : str, default: '&'
        Delimiter of the query string. Default is '&'.

    Returns
    -------
    base, queries, fragment : str, dict[str, str], str
    """

    def process_query_string(query_string: str):
        """Process the query string and return a dictionary of key-value pairs."""
        queries = dict()
        for query in query_string.split(query_delimiter):
            key_val = query.split("=")
            if len(key_val) == 1:
                queries[key_val[0]] = True
            elif len(key_val) == 2:
                queries[key_val[0]] = key_val[1]
            else:
                raise ValueError("Query string not formatted correctly.")
        return queries

    if not url.startswith(("http://", "https://")):
        raise ValueError("`base_url` must start with either 'http://' or 'https://'.")
    url_pattern = r"^(?P<base_url>[^?#]+)(?:\?(?P<query_string>[^#]+))?(?:#(?P<fragment>.*))?$"
    match = re.match(url_pattern, url)
    if not match:
        raise ValueError("URL not formatted correctly.")
    base_url = match.group("base_url")
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    query_string = match.group("query_string")
    fragment = match.group("fragment")
    queries = process_query_string(query_string) if query_string else dict()
    return base_url, queries, fragment
