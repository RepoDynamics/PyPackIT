"""
Dynamically create badges using the shields.io API

References
----------
* https://shields.io/
* https://github.com/badges/shields
"""


# Standard libraries
import base64
import copy
from typing import Literal, Optional, Sequence

# Non-standard libraries
import pyhtmlit as html
import pylinks
from pybadgeit import _badge
from pylinks import url
from pylinks.url import URL


_BASE_URL = url("https://img.shields.io")


class ShieldsBadge(_badge.Badge):
    """SHIELDS.IO Badge"""

    def __init__(
        self,
        path: str,
        style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] = None,
        text: str | dict[Literal["left", "right"], str] = None,
        logo: str | tuple[str, str] = None,
        color: str | dict[str, str | dict[str, str]] = None,
        cache_time: int = None,
        alt: str = None,
        title: str = None,
        width: str = None,
        height: str = None,
        align: str = None,
        link: str | URL = None,
        default_theme: Literal["light", "dark"] = "light",
        html_syntax: str | dict[Literal["tag_seperator", "content_indent"], str] = None,
    ):
        """
        Parameters
        ----------
        path : pylinks.URL
            Clean URL (without additional queries) of the badge image.
        style : {'plastic', 'flat', 'flat-square', 'for-the-badge', 'social'}
            Style of the badge.
        left_text : str
            Text on the left-hand side of the badge. Pass an empty string to omit the left side.
        right_text : str
            Text on the right-hand side of the badge. This can only be set for static badges.
            When `left_text` is set to empty string, this will be the only text shown.
        logo : str
            Logo on the badge. Two forms of input are accepted:
            1. A SimpleIcons icon name (see: https://simpleicons.org/), e.g. 'github',
                or one of the following names: 'bitcoin', 'dependabot', 'gitlab', 'npm', 'paypal',
                'serverfault', 'stackexchange', 'superuser', 'telegram', 'travis'.
            2. A filepath to an image file; this must be inputted as a tuple, where the first
               element is the file extension, and the second element is the full path to the image file,
               e.g. `('png', '/home/pictures/my_logo.png')`.
        logo_width : float
            Horizontal space occupied by the logo.
        logo_color_light : str
            Color of the logo. This and other color inputs can be in one of the following forms:
            hex, rgb, rgba, hsl, hsla and css named colors.
        left_color_light : str
            Color of the left side. See `logo_color` for more detail.
        right_color_dark : str
            Color of the right side. See `logo_color` for more detail.
        cache_time : int
            HTTP cache lifetime in seconds.
        """

        self._url: URL = url(str(path))
        self.style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] = style

        self._text = self._init_text()
        self.text = text

        self._logo = self._init_logo()
        self.logo = logo

        self._color = self._init_color()
        self.color = color

        self.cache_time: int = cache_time

        if alt is not False:
            alt = alt or self.text["left"] or self.text["right"]
        super().__init__(
            alt=alt,
            title=title,
            width=width,
            height=height,
            align=align,
            link=link,
            default_theme=default_theme,
            html_syntax=html_syntax,
        )
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
            ("label", self.text["left"]),
            ("message", self.text["right"]),
            ("style", self.style),
            ("labelColor", self.color["left"][mode]),
            ("color", self.color["right"][mode]),
            ("logo", self.logo["data"]),
            ("logoColor", self.logo["color"][mode]),
            ("logoWidth", self.logo["width"]),
            ("cacheSeconds", self.cache_time),
        ):
            if val is not None:
                url.queries[key] = val
        return url

    @property
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, value):
        def encode_logo(content, img_type: str = "png"):
            return f'data:image/{img_type if img_type else "png"};base64,{base64.b64encode(content).decode()}'

        if value is None:
            self._logo = self._init_logo()
            return
        if isinstance(value, str):
            self._logo["data"] = value
            return
        if not isinstance(value, dict):
            raise ValueError(f"`logo` expects either a string or a dict, but got {type(value)}.")
        for key, val in value.items():
            if key == "width":
                self._logo["width"] = val
            elif key == "color":
                if isinstance(val, str):
                    self._logo["color"] = {"dark": val, "light": val}
                elif isinstance(val, dict):
                    for key2, val2 in val.items():
                        if key2 not in ("dark", "light"):
                            raise ValueError()
                        self._logo["color"][key2] = val2
                else:
                    raise ValueError()
            elif key == "simple_icons":
                self._logo["data"] = val
            elif key == "url":
                content = pylinks.http.request(url=val, response_type="bytes")
                self._logo["data"] = encode_logo(content)
            elif key == "local":
                with open(val["value"], "rb") as f:
                    content = f.read()
                    self._logo = encode_logo(content)
            elif key == "bytes":
                self._logo = encode_logo(content)
            elif key == "github":
                content = pylinks.http.request(
                    url=pylinks.github.user(val["user"])
                    .repo(val["repo"])
                    .branch(val["branch"])
                    .file(val["path"], raw=True),
                    response_type="bytes",
                )
                self._logo["data"] = encode_logo(content)
            else:
                raise ValueError(f"Key '{key}' in logo spec. {value} is not recognized.")
        return

    @property
    def color(self):
        return copy.deepcopy(self._color)

    @color.setter
    def color(self, value):
        if value is None:
            self._color = self._init_color()
            return
        if isinstance(value, str):
            new_colors = {"dark": value, "light": value}
            if self._is_static and not self.text["left"]:
                self._color["right"] = new_colors
                return
            self._color["left"] = new_colors
            return
        if not isinstance(value, dict):
            return ValueError()
        for key, val in value.items():
            if key not in ("left", "right", "dark", "light"):
                raise ValueError()
            if isinstance(val, str):
                if key in ("left", "right"):
                    self._color[key] = {"dark": val, "light": val}
                else:
                    side = "right" if self._is_static and not self.text["left"] else "left"
                    self._color[side][key] = val
            elif isinstance(val, dict):
                for key2, val2 in val.items():
                    if key2 not in ("left", "right", "dark", "light"):
                        raise ValueError()
                    if key2 in ("dark", "light"):
                        if key in ("dark", "light"):
                            raise ValueError()
                        self._color[key][key2] = val2
                    else:
                        if key in ("left", "right"):
                            raise ValueError()
                        self._color[key2][key] = val2
            else:
                raise ValueError()
        return

    @property
    def text(self):
        return copy.deepcopy(self._text)

    @text.setter
    def text(self, value):
        if value is None:
            self._text = self._init_text()
            return
        if isinstance(value, str):
            if self._is_static:
                self._text = {"left": "", "right": value}
                return
            self._text["left"] = value
            return
        if not isinstance(value, dict):
            raise ValueError()
        for key, val in value.items():
            if key not in ("left", "right"):
                raise ValueError()
            if key == "right" and not self._is_static:
                raise ValueError()
            self._text[key] = val
        return

    @property
    def _is_static(self):
        return str(self._url).startswith("https://img.shields.io/static/")

    @staticmethod
    def _init_text():
        return {"left": None, "right": None}

    @staticmethod
    def _init_color():
        return {"left": {"dark": None, "light": None}, "right": {"dark": None, "light": None}}

    @staticmethod
    def _init_logo():
        return {"data": None, "width": None, "color": {"dark": None, "light": None}}


def static(text: str | dict[Literal["left", "right"], str], **kwargs) -> ShieldsBadge:
    """Static badge with custom text on the right-hand side.

    Parameters
    ----------
    text : str | dict['left': str, 'right': str]
        The text on the badge. If a string is provided, the text on the right-hand side of
        the badge is set, and the left-hand side is omitted. Otherwise, a dictionary must be
        provided with keys 'left' and 'right', setting the text on both sides of the badge.
    **kwargs
        Any other argument accepted by `ShieldsBadge`.
    """
    return ShieldsBadge(path=_BASE_URL / "static/v1", text=text, **kwargs)


class GitHub:
    """GitHub Badges."""

    def __init__(
        self,
        user: str,
        repo: str,
        branch: Optional[str] = None,
        default_logo: bool = True,
        **kwargs,
    ):
        """
        Parameters
        ----------
        user : str
            GitHub username.
        repo : str
            GitHub repository name.
        branch : str, optional
            GitHub branch name.
        default_logo : bool, default: True
            Whether to add a white GitHub logo to all badges by default.
            This will have no effect if 'logo' is provided as a keyword argument.
        **kwargs
            Any other argument accepted by `ShieldsBadge`. These will be used as default values
            for all badges, unless the same argument is also provided to the method when creating a specific badge,
            in which case, the default value will be overridden.
        """
        self.user = user
        self.repo = repo
        self.branch = branch
        self._url = _BASE_URL / "github"
        self._address = f"{user}/{repo}"
        self._repo_link = pylinks.github.user(user).repo(repo)
        if default_logo and "logo" not in kwargs:
            kwargs["logo"] = {"simple_icons": "github", "color": "white"}
        self.args = kwargs
        return

    def workflow_status(
        self,
        filename: str,
        description: Optional[str] = None,
        **kwargs,
    ) -> ShieldsBadge:
        """Status (failing/passing) of a GitHub workflow.

        Parameters
        ----------
        filename : str
            Full filename of the workflow, e.g. 'ci.yaml'.
        description : str, optional
            A description for the workflow.
            This will be used for the 'title' attribute of the badge's 'img' element, unless 'title'
            is provided as a keyword argument.
        """
        path = self._url / "actions/workflow/status" / self._address / filename
        link = self._repo_link.workflow(filename)
        if self.branch:
            path.queries["branch"] = self.branch
            link = self._repo_link.branch(self.branch).workflow(filename)
        args = self.args | kwargs
        if "title" not in args:
            args["title"] = (
                f"Status of the GitHub Actions workflow '{filename}'"
                f"""{f"on branch '{self.branch}'" if self.branch else ''}. """
                f"""{f"{description.strip().rstrip('.')}. " if description else ""}"""
                "Click to see more details in the Actions section of the repository."
            )
        if "alt" not in args and "text" not in args:
            args["alt"] = "GitHub Workflow Status"
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def pr_issue(
        self,
        pr: bool = True,
        status: Literal["open", "closed", "both"] = "both",
        label: Optional[str] = None,
        raw: bool = False,
        **kwargs,
    ) -> ShieldsBadge:
        """Number of pull requests or issues on GitHub.

        Parameters
        ----------
        pr : bool, default: True
            Whether to query pull requests (True, default) or issues (False).
        closed : bool, default: False
            Whether to query closed (True) or open (False, default) issues/pull requests.
        label : str, optional
            A specific GitHub label to query.
        raw : bool, default: False
            Display 'open'/'close' after the number (False) or only display the number (True).
        """

        def get_path_link(closed):
            path = self._url / (
                f"issues{'-pr' if pr else ''}{'-closed' if closed else ''}"
                f"{'-raw' if raw else ''}/{self._address}{f'/{label}' if label else ''}"
            )
            link = self._repo_link.pr_issues(pr=pr, closed=closed, label=label)
            return path, link

        def half_badge(closed: bool):
            path, link = get_path_link(closed=closed)
            if "link" not in args:
                args["link"] = link
            badge = ShieldsBadge(path=path, **args)
            badge.html_syntax = ""
            if closed:
                badge.color = {"right": "00802b"}
                badge.text = ""
                badge.logo = None
            else:
                badge.color = {"right": "AF1F10"}
            return badge

        desc = {
            None: {True: "pull requests in total", False: "issues in total"},
            "bug": {True: "pull requests related to a bug-fix", False: "bug-related issues"},
            "enhancement": {
                True: "pull requests related to new features and enhancements",
                False: "feature and enhancement requests",
            },
            "documentation": {
                True: "pull requests related to the documentation",
                False: "issues related to the documentation",
            },
        }
        text = {
            None: {True: "Total", False: "Total"},
            "bug": {True: "Bug Fix", False: "Bug Report"},
            "enhancement": {True: "Enhancement", False: "Feature Request"},
            "documentation": {True: "Docs", False: "Docs"},
        }

        args = self.args | kwargs
        if "text" not in args:
            args["text"] = text[label][pr]
        if "title" not in args:
            args["title"] = (
                f"Number of {status if status != 'both' else 'open (red) and closed (green)'} "
                f"{desc[label][pr]}. "
                f"Click {'on the red and green tags' if status=='both' else ''} to see the details of "
                f"the respective {'pull requests' if pr else 'issues'} in the "
                f"'{'Pull requests' if pr else 'Issues'}' section of the repository."
            )
        if "style" not in args and status == "both":
            args["style"] = "flat-square"
        if status not in ("open", "closed", "both"):
            raise ValueError()
        if status != "both":
            path, link = get_path_link(closed=status == "closed")
            if "link" not in args:
                args["link"] = link
            return ShieldsBadge(path=path, **args)
        return html.element.ElementCollection(
            [half_badge(closed) for closed in (False, True)], seperator=""
        )

    def top_language(self, **kwargs) -> ShieldsBadge:
        """The top language in the repository, and its frequency."""
        args = self.args | kwargs
        if "alt" not in args:
            args["alt"] = "Top Programming Language"
        if "title" not in args:
            args["title"] = "Percentage of the most used programming language in the repository."
        return ShieldsBadge(path=self._url / "languages/top" / self._address, **args)

    def language_count(self, **kwargs) -> ShieldsBadge:
        """Number of programming languages used in the repository."""
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Programming Languages"
        if "title" not in args:
            args["title"] = "Number of programming languages used in the repository."
        return ShieldsBadge(path=self._url / "languages/count/" / self._address, **args)

    def downloads(
        self,
        tag: Optional[str | Literal["latest"]] = None,
        asset: Optional[str] = None,
        include_pre_release: bool = True,
        sort_by_semver: bool = False,
        **kwargs,
    ) -> ShieldsBadge:
        """
        Number of downloads of a GitHub release.

        Parameters
        ----------
        tag : str, default: None
            A specific release tag to query. If set to None (default), number of total downloads is displayed.
            Additionally, the keyword 'latest' can be provided to query the latest release.
        asset : str, optional
            An optional asset to query.
        include_pre_release : bool, default: True
            Whether to include pre-releases in the count.
        sort_by_semver : bool, default: False
            If tag is set to 'latest', whether to choose the latest release according
            to the Semantic Versioning (True), or according to date (False).
        """
        path = self._url / f"downloads{'-pre' if include_pre_release else ''}/{self._address}"
        if not tag:
            path /= "total"
        else:
            path /= f'{tag}/{asset if asset else "total"}'
            if sort_by_semver:
                path.queries["sort"] = "semver"
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Downloads"
        if "title" not in args:
            if tag:
                target = (
                    f" for the {'latest release' if tag == 'latest' else f'release version {tag}'}"
                )
                if asset:
                    target += f" and asset '{asset}'"
            elif asset:
                target = f" for the asset {asset}"
            args["title"] = (
                f"Number of {'total ' if not (asset or tag) else ''}GitHub downloads{target}. "
                "Click to see more details in the 'Releases' section of the repository."
            )
        if "link" not in args:
            args["link"] = self._repo_link.releases(tag=tag if tag else "latest")
        return ShieldsBadge(path=path, **args)

    def license(self, filename: str = "LICENSE", branch: str = "main", **kwargs) -> ShieldsBadge:
        """License of the GitHub repository.

        Parameters
        ----------
        filename : str, default: 'LICENSE'
            Name of the license file in the GitHub branch.
            This is used to create a link to the license.
        """
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "License"
        if "title" not in args:
            args["title"] = "License of the project. Click to read the complete license."
        if "link" not in args:
            args["link"] = self._repo_link.branch(self.branch or branch).file(filename)
        return ShieldsBadge(path=self._url / "license" / self._address, **args)

    def commit_activity(self, interval: Literal["y", "m", "w"] = "m", **kwargs) -> ShieldsBadge:
        interval_text = {"y": "year", "m": "month", "w": "week"}
        path = self._url / "commit-activity" / interval / self._address
        link = self._repo_link.commits
        if self.branch:
            path /= self.branch
            link = self._repo_link.branch(self.branch).commits
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Commits"
        if "title" not in args:
            args["title"] = (
                f"""Average number of commits {f"in branch '{self.branch}' " if self.branch else ''}"""
                f"per {interval_text[interval]}. Click to see the full list of commits."
            )
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def commits_since(
        self,
        version: str | Literal["latest"] = "latest",
        include_pre_release: bool = True,
        sort_by_semver: bool = False,
        **kwargs,
    ):
        path = self._url / "commits-since" / self._address / version
        link = self._repo_link.commits
        if self.branch:
            path /= self.branch
            link = self._repo_link.branch(self.branch).commits
        if include_pre_release:
            path.queries["include_prereleases"] = None
        if sort_by_semver:
            path.queries["sort"] = "semver"
        args = self.args | kwargs
        if "text" not in args and "alt" not in args:
            args[
                "alt"
            ] = f"Commits since {'latest release' if version=='latest' else f'release version {version}'}"
        if "title" not in args:
            args["title"] = (
                f"Number of commits since {'latest release' if version == 'latest' else f'release version {version}'}."
                "Click to see the full list of commits."
            )
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def last_commit(self, **kwargs):
        path = self._url / "last-commit" / self._address
        link = self._repo_link.commits
        if self.branch:
            path /= self.branch
            link = self._repo_link.branch(self.branch).commits
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Last Commit"
        if "title" not in args:
            args["title"] = (
                f"""Time of last commit{f" on branch '{self.branch}'" if self.branch else ''}."""
                "Click to see the full list of commits."
            )
        if "link" not in args:
            args["link"] = link
        return ShieldsBadge(path=path, **args)

    def release_date(
        self, pre_release: bool = True, publish_date: bool = False, **kwargs
    ) -> ShieldsBadge:
        """
        Release date (optionally publish date) of the latest released version on GitHub.

        Parameters
        ----------
        pre_release : bool, default: True
            Whether to include pre-releases.
        publish_date : bool, default: False
            Get publish date instead of release date.
        kwargs
            Any other argument accepted by `ShieldsBadge`.
        """
        path = self._url / ("release-date-pre" if pre_release else "release-date") / self._address
        if publish_date:
            path.queries["display_date"] = "published_at"
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Released"
        if "alt" not in args:
            args["alt"] = "Release Date"
        if "title" not in args:
            args["title"] = (
                "Release date of the latest version. "
                "Click to see more details in the 'Releases' section of the repository."
            )
        if "link" not in args:
            args["link"] = self._repo_link.releases(tag="latest")
        return ShieldsBadge(path=path, **args)

    def release_version(
        self,
        display_name: Optional[Literal["tag", "release"]] = None,
        include_pre_release: bool = True,
        sort_by_semver: bool = False,
        **kwargs,
    ):
        path = self._url / "v/release" / self._address
        if display_name:
            path.queries["display_name"] = display_name
        if include_pre_release:
            path.queries["include_prereleases"] = None
        if sort_by_semver:
            path.queries["sort"] = "semver"
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Version"
        if "title" not in args:
            args["title"] = (
                "Latest release version. "
                "Click to see more details in the 'Releases' section of the repository."
            )
        if "link" not in args:
            args["link"] = self._repo_link.releases(tag="latest")
        return ShieldsBadge(path=path, **args)

    def code_size(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Code Size"
        if "title" not in args:
            args["title"] = "Total size of all source files in the repository."
        return ShieldsBadge(path=self._url / "languages/code-size" / self._address, **args)

    def dir_file_count(
        self,
        path: Optional[str] = None,
        selection: Optional[Literal["file", "dir"]] = None,
        file_extension: Optional[str] = None,
        **kwargs,
    ):
        img_path = self._url / "directory-file-count" / self._address
        if path:
            img_path /= path
        if selection:
            img_path.queries["type"] = selection
        if file_extension:
            img_path.queries["extension"] = file_extension
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Files"
        if "title" not in args:
            things = (
                "files and directories"
                if not selection
                else ("files" if selection == "file" else "directories")
            )
            args["title"] = (
                f"Total number of {things} "
                f"""{f"with the extension '{file_extension}' " if file_extension else ''}"""
                f"""{f"located under '{path}'" if path else 'in the repository'}."""
            )
        return ShieldsBadge(img_path, **args)

    def repo_size(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Repo Size"
        if "title" not in args:
            args["title"] = "Total size of the repository."
        return ShieldsBadge(self._url / "repo-size" / self._address, **args)

    def milestones(self, state: Literal["open", "closed", "both", "all"] = "all", **kwargs):
        def get_path_link(state):
            path = self._url / "milestones" / state / self._address
            link = self._repo_link.milestones(state=state if state == "closed" else "open")
            return path, link

        def half_badge(state):
            path, link = get_path_link(state=state)
            if "link" not in args:
                args["link"] = link
            badge = ShieldsBadge(path=path, **args)
            badge.html_syntax = ""
            if state == "closed":
                badge.color = {"right": "00802b"}
                badge.text = ""
                badge.logo = None
            else:
                badge.color = {"right": "AF1F10"}
            return badge

        args = self.args | kwargs
        if "text" not in args:
            args["text"] = (
                "Milestones"
                if state in ("all", "both")
                else ("Open Milestones" if state == "open" else "Finished Milestones")
            )
        if "title" not in args:
            which = (
                state
                if state not in ("both", "all")
                else ("open (red) and closed (green)" if state == "both" else "total")
            )
            args["title"] = (
                f"Number of {which} milestones. "
                f"Click {'on the red and green tags' if state == 'both' else ''} for more details."
            )
        if state != "both":
            path, link = get_path_link(state=state)
            if "link" not in args:
                args["link"] = link
            return ShieldsBadge(path=path, **args)
        return html.element.ElementCollection(
            [half_badge(state) for state in ("open", "closed")], seperator=""
        )

    def discussions(self, **kwargs) -> ShieldsBadge:
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Discussions"
        if "title" not in args:
            args[
                "title"
            ] = "Total number of discussions. Click to open the 'Discussions' section of the repository."
        if "link" not in args:
            args["link"] = self._repo_link.discussions()
        return ShieldsBadge(path=self._url / "discussions" / self._address, **args)

    def dependency_status(self, **kwargs) -> ShieldsBadge:
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Dependencies"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        return ShieldsBadge(_BASE_URL / "librariesio/github" / self._address, **args)


class PyPI:
    def __init__(self, package_name: str, **kwargs):
        self.package_name = package_name
        self._url = _BASE_URL / "pypi"
        self._link = pylinks.pypi.package(package_name)
        self.args = kwargs
        return

    def downloads(self, period: Literal["dd", "dw", "dm"] = "dm", **kwargs):
        period_name = {"dd": "day", "dw": "week", "dm": "month"}
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Downloads"
        if "title" not in args:
            args["title"] = f"Average number of downloads per {period_name[period]} from PyPI."
            if "link" not in args:
                args["title"] += f" Click to open the package homepage on pypi.org."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / period / self.package_name, **args)

    def format(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Format"
        if "title" not in args:
            args["title"] = "Format of the PyPI package distribution."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "format" / self.package_name, **args)

    def development_status(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Development Status"
        if "title" not in args:
            args["title"] = "Current development phase of the project."
        return ShieldsBadge(self._url / "status" / self.package_name)

    def supported_python_versions(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Supports Python"
        if "title" not in args:
            args["title"] = "Supported Python versions of the latest release."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "pyversions" / self.package_name, **args)

    def version(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Version"
        if "title" not in args:
            args["title"] = "Latest release version on PyPI."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "v" / self.package_name, **args)


class Conda:
    def __init__(self, package_name: str, channel: str = "conda-forge", **kwargs):
        """
        Parameters
        ----------
        package_name : str
            Package name.
        channel : str, default: 'conda-forge'
            Channel name.
        """
        self.package_name = package_name
        self._channel = channel
        self._url = _BASE_URL / "conda"
        self._address = f"{channel}/{package_name}"
        self._link = pylinks.conda.package(name=package_name, channel=channel)
        self.args = kwargs
        return

    def downloads(self, **kwargs):
        """Number of total downloads."""
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Downloads"
        if "title" not in args:
            args["title"] = "Number of downloads for the Conda distribution."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "dn" / self._address, **args)

    def supported_platforms(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Platforms"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "pn" / self._address, **args)

    def version(self, **kwargs):
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Dependencies"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        if "link" not in args:
            args["link"] = self._link.homepage
        return ShieldsBadge(self._url / "v" / self._address, **args)


def build_read_the_docs(project: str, version: Optional[str] = None, **kwargs) -> ShieldsBadge:
    """Build status of a ReadTheDocs project.

    Parameters
    ----------
    project : str
        ReadTheDocs project name.
    version : str, optional
        Specific ReadTheDocs version of the documentation to query.
        https://img.shields.io/readthedocs/opencadd?logo=readthedocs&logoColor=%238CA1AF
    left_text : str, default = 'Website'
        Text on the left-hand side of the badge. If set to None, the shields.io default ('docs') will be selected.

    """
    if "text" not in kwargs:
        kwargs["text"] = "Website"
    if "alt" not in kwargs:
        kwargs["alt"] = "Website Build Status"
    if "title" not in kwargs:
        kwargs[
            "title"
        ] = "Website build status. Click to see more details on the ReadTheDocs platform."
    if "logo" not in kwargs:
        kwargs["logo"] = {"simple_icons": "readthedocs", "color": "FFF"}
    if "link" not in kwargs:
        kwargs["link"] = pylinks.readthedocs.project(project).build_status
    return ShieldsBadge(
        path=_BASE_URL / "readthedocs" / f"{project}{f'/{version}' if version else ''}", **kwargs
    )


def coverage_codecov(
    user: str,
    repo: str,
    branch: Optional[str] = None,
    vcs: Literal["github", "gitlab", "bitbucket"] = "github",
    **kwargs,
) -> ShieldsBadge:
    """Code coverage calculated by codecov.io.

    Parameters
    ----------
    user : str
        GitHub username
    repo : str
        GitHub repository name.
    branch : str, optional
        Name of specific branch to query.
    vcs : {'github', 'gitlab', 'bitbucket'}, default: 'github'
        Version control system hosting the repository.
    """
    abbr = {"github": "gh", "gitlab": "gl", "bitbucket": "bb"}
    if "text" not in kwargs:
        kwargs["text"] = "Code Coverage"
    if "title" not in kwargs:
        kwargs[
            "title"
        ] = "Source code coverage by the test suite. Click to see more details on codecov.io."
    if "logo" not in kwargs:
        kwargs["logo"] = {"simple_icons": "codecov", "color": "FFF"}
    if "link" not in kwargs:
        kwargs[
            "link"
        ] = f"https://codecov.io/{abbr[vcs]}/{user}/{repo}{f'/branch/{branch}' if branch else ''}"  # TODO: use PyLinks
    return ShieldsBadge(
        path=_BASE_URL / f"codecov/c/{vcs}/{user}/{repo}{f'/{branch}' if branch else ''}", **kwargs
    )


def chat_discord(server_id: str, **kwargs):
    """Number of online users in Discord server.

    Parameters
    ----------
    server_id : str
        Server ID of the Discord server, which can be located in the url of the channel.
        This is required in order access the Discord JSON API.

    Notes
    -----
    A Discord server admin must enable the widget setting on the server for this badge to work.
    This can be done in the Discord app: Server Setting > Widget > Enable Server Widget

    """
    return ShieldsBadge(path=_BASE_URL / "discord" / server_id, **kwargs)


def binder():
    logo = (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAABZCAMAAABi1XidAAAB8lBMVEX///9XmsrmZYH1"
        "olJXmsr1olJXmsrmZYH1olJXmsr1olJXmsrmZYH1olL1olJXmsr1olJXmsrmZYH1olL1olJXmsrmZYH1olJXmsr1ol"
        "L1olJXmsrmZYH1olL1olJXmsrmZYH1olL1olL0nFf1olJXmsrmZYH1olJXmsq8dZb1olJXmsrmZYH1olJXmspXmspX"
        "msr1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olLeaIVXmsrmZYH1olL1olL1olJXmsrmZYH1olLna3"
        "1Xmsr1olJXmsr1olJXmsrmZYH1olLqoVr1olJXmsr1olJXmsrmZYH1olL1olKkfaPobXvviGabgadXmsqThKuofKHm"
        "Z4Dobnr1olJXmsr1olJXmspXmsr1olJXmsrfZ4TuhWn1olL1olJXmsqBi7X1olJXmspZmslbmMhbmsdemsVfl8Zgms"
        "Nim8Jpk8F0m7R4m7F5nLB6jbh7jbiDirOEibOGnKaMhq+PnaCVg6qWg6qegKaff6WhnpKofKGtnomxeZy3noG6dZi+"
        "n3vCcpPDcpPGn3bLb4/Mb47UbIrVa4rYoGjdaIbeaIXhoWHmZYHobXvpcHjqdHXreHLroVrsfG/uhGnuh2bwj2Hxk1"
        "7yl1vzmljzm1j0nlX1olL3AJXWAAAAbXRSTlMAEBAQHx8gICAuLjAwMDw9PUBAQEpQUFBXV1hgYGBkcHBwcXl8gICA"
        "goiIkJCQlJicnJ2goKCmqK+wsLC4usDAwMjP0NDQ1NbW3Nzg4ODi5+3v8PDw8/T09PX29vb39/f5+fr7+/z8/Pz9/v"
        "7+zczCxgAABC5JREFUeAHN1ul3k0UUBvCb1CTVpmpaitAGSLSpSuKCLWpbTKNJFGlcSMAFF63iUmRccNG6gLbuxkXU"
        "66JAUef/9LSpmXnyLr3T5AO/rzl5zj137p136BISy44fKJXuGN/d19PUfYeO67Znqtf2KH33Id1psXoFdW30sPZ1sM"
        "vs2D060AHqws4FHeJojLZqnw53cmfvg+XR8mC0OEjuxrXEkX5ydeVJLVIlV0e10PXk5k7dYeHu7Cj1j+49uKg7uLU6"
        "1tGLw1lq27ugQYlclHC4bgv7VQ+TAyj5Zc/UjsPvs1sd5cWryWObtvWT2EPa4rtnWW3JkpjggEpbOsPr7F7EyNewtp"
        "BIslA7p43HCsnwooXTEc3UmPmCNn5lrqTJxy6nRmcavGZVt/3Da2pD5NHvsOHJCrdc1G2r3DITpU7yic7w/7Rxnjc0"
        "kt5GC4djiv2Sz3Fb2iEZg41/ddsFDoyuYrIkmFehz0HR2thPgQqMyQYb2OtB0WxsZ3BeG3+wpRb1vzl2UYBog8FfGh"
        "ttFKjtAclnZYrRo9ryG9uG/FZQU4AEg8ZE9LjGMzTmqKXPLnlWVnIlQQTvxJf8ip7VgjZjyVPrjw1te5otM7RmP7xm"
        "+sK2Gv9I8Gi++BRbEkR9EBw8zRUcKxwp73xkaLiqQb+kGduJTNHG72zcW9LoJgqQxpP3/Tj//c3yB0tqzaml05/+or"
        "HLksVO+95kX7/7qgJvnjlrfr2Ggsyx0eoy9uPzN5SPd86aXggOsEKW2Prz7du3VID3/tzs/sSRs2w7ovVHKtjrX2pd"
        "7ZMlTxAYfBAL9jiDwfLkq55Tm7ifhMlTGPyCAs7RFRhn47JnlcB9RM5T97ASuZXIcVNuUDIndpDbdsfrqsOppeXl5Y"
        "+XVKdjFCTh+zGaVuj0d9zy05PPK3QzBamxdwtTCrzyg/2Rvf2EstUjordGwa/kx9mSJLr8mLLtCW8HHGJc2R5hS219"
        "IiF6PnTusOqcMl57gm0Z8kanKMAQg0qSyuZfn7zItsbGyO9QlnxY0eCuD1XL2ys/MsrQhltE7Ug0uFOzufJFE2PxBo"
        "/YAx8XPPdDwWN0MrDRYIZF0mSMKCNHgaIVFoBbNoLJ7tEQDKxGF0kcLQimojCZopv0OkNOyWCCg9XMVAi7ARJzQdM2"
        "QUh0gmBozjc3Skg6dSBRqDGYSUOu66Zg+I2fNZs/M3/f/Grl/XnyF1Gw3VKCez0PN5IUfFLqvgUN4C0qNqYs5YhPL+"
        "aVZYDE4IpUk57oSFnJm4FyCqqOE0jhY2SMyLFoo56zyo6becOS5UVDdj7Vih0zp+tcMhwRpBeLyqtIjlJKAIZSbI8S"
        "GSF3k0pA3mR5tHuwPFoa7N7reoq2bqCsAk1HqCu5uvI1n6JuRXI+S1Mco54YmYTwcn6Aeic+kssXi8XpXC4V3t7/AD"
        "uTNKaQJdScAAAAAElFTkSuQmCC"
    )
    badge = static(right_text="binder", left_text="launch")
    badge.logo = logo
    badge.right_color_dark = badge.right_color_light = "579aca"
    badge.link = ""  # TODO
    return badge


class LibrariesIO:
    """Shields badges provided by Libraries.io."""

    def __init__(self, package_name: str, platform: str = "pypi", **kwargs):
        """
        Parameters
        ----------
        package_name : str
            Name of the package.
        platform : str, default: 'pypi'
            The platform where the package is distributed, e.g. 'pypi', 'conda' etc.
        """
        self.platform = platform
        self.package_name = package_name
        self._url = _BASE_URL / "librariesio"
        self._address = f"{platform}/{package_name}"
        self._link = URL(f"https://libraries.io/{platform}/{package_name}")
        self.args = kwargs
        return

    def dependency_status(self, version: Optional[str] = None, **kwargs) -> ShieldsBadge:
        """
        Dependency status of a package distributed on a package manager platform,
        obtained using Libraries.io.
        The right-hand text shows either 'up to date', or '{number} out of date'.

        Parameters
        ----------
        platform : str
            Name of a supported package manager, e.g. 'pypi', 'conda'.
        package_name : str
            Name of the package.
        version : str, optional
            A specific version to query.

        References
        ----------
        * https://libraries.io/
        """
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Dependencies"
        if "title" not in args:
            args["title"] = "Status of the project's dependencies."
        path = self._url / "release" / self._address
        link = self._link
        if version:
            path /= version
            link /= f"{version}/tree"
        else:
            link /= "tree"
        if "link" not in kwargs:
            kwargs["link"] = link
        return ShieldsBadge(path, **args)

    def dependents(self, repo: bool = False, **kwargs) -> ShieldsBadge:
        """
        Number of packages or repositories that depend on this package.

        Parameters
        ----------
        repo : bool, default: False
            Whether to query repositories (True) or packages (False).
        """
        path = self._url / ("dependent-repos" if repo else "dependents") / self._address
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = f"Dependent {'Repos' if repo else 'Packages'}"
        if "title" not in args:
            args[
                "title"
            ] = f"Number of {'repositories' if repo else 'packages'} that have {self.package_name} as a dependency."
        if "link" not in kwargs:
            kwargs["link"] = self._link
        return ShieldsBadge(path, **args)

    def source_rank(self, **kwargs) -> ShieldsBadge:
        """SourceRank ranking of the package."""
        args = self.args | kwargs
        if "text" not in args:
            args["text"] = "Source Rank"
        if "title" not in args:
            args["title"] = (
                "Ranking of the source code according to libraries.io SourceRank algorithm. "
                "Click to see more details on libraries.io website."
            )
        if "link" not in kwargs:
            kwargs["link"] = self._link / "sourcerank"
        return ShieldsBadge(self._url / "sourcerank" / self._address, **args)
