from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING, NamedTuple as _NamedTuple
from dataclasses import dataclass as _dataclass

import jinja2

from github_contexts.property_dict import PropertyDict
from loggerman import logger as _logger
from versionman.pep440_semver import PEP440SemVer
import pycolorit as _pcit

from proman.exception import ProManException
from proman.dtype import IssueStatus, LabelType, BranchType
from controlman import date

if _TYPE_CHECKING:
    from typing import Sequence, Callable
    from datetime import datetime
    from conventional_commits import ConventionalCommitMessage
    from pylinks.site.github import Repo as GitHubRepoLinker, Branch as GitHubBranchLinker
    from pylinks.url import URL
    from proman.dtype import ReleaseAction


class Token:
    """A token for a specific service.

    This class is used to store a sensitive token,
    obfuscating it when printed.
    """

    def __init__(self, token: str | None, name: str):
        self._token = token
        self.name = name
        return

    def get(self):
        return self._token

    def __repr__(self):
        return f"<{self.name} Token>"

    def __str__(self):
        return f"***{self.name} Token***"

    def __bool__(self):
        return bool(self._token)


@_dataclass
class Version:
    public: PEP440SemVer | str
    distance: int = 0
    sha: str | None = None
    date: datetime | None = None

    def __post_init__(self):
        if isinstance(self.public, str):
            self.public = PEP440SemVer(self.public)
        if not self.date:
            self.date = date.from_now()
        return

    @property
    def full(self) -> str:
        if self.is_local:
            return f"{self.public}+{self.distance}"
        return str(self.public)


    @property
    def is_local(self) -> bool:
        return bool(self.distance)

    def __str__(self):
        return self.full

    def __repr__(self):
        return self.full


class VersionTag(_NamedTuple):
    tag_prefix: str
    version: PEP440SemVer

    @property
    def name(self) -> str:
        return f"{self.tag_prefix}{self.version}"

    def __str__(self):
        return self.name


class Branch(_NamedTuple):
    """A branch in the repository.

    Attributes
    ----------
    type
        Type of the branch.
    prefix
        Prefix of the branch name.
    version
        This is the suffix for release branches,
        denoting the major version number.
    issue
        This is the suffix for development and pre-release branches,
        denoting the issue or pull number, respectively.
    target
        This is the second suffix for development branches,
        denoting the target branch.
    auto_type
        This is the suffix for auto-update branches,
        denoting the type of auto-update job.
    """

    type: BranchType
    prefix: str
    linker: GitHubRepoLinker
    version: int | None = None
    issue: int | None = None
    target: Branch | None = None
    auto_type: str | None = None
    separator: str | None = None
    sha: str | None = None
    protected: bool | None = None
    protection: dict | None = None

    @property
    def name(self) -> str:
        if self.type in [BranchType.MAIN, BranchType.OTHER]:
            return self.prefix
        if self.type is BranchType.RELEASE:
            return f"{self.prefix}{self.version}"
        if self.type is BranchType.PRE:
            return f"{self.prefix}{self.issue}"
        if self.type is BranchType.DEV:
            return f"{self.prefix}{self.issue}{self.separator}{self.target.name}"
        # BranchType.AUTO
        return f"{self.prefix}{self.target.name}{self.separator}{self.auto_type}"

    @property
    def url(self) -> GitHubBranchLinker:
        return self.linker.branch(self.name)

    @property
    def sha_url(self) -> URL | None:
        return (self.url.repo.homepage / "commits" / self.sha) if self.sha else None

    @property
    def ref(self) -> str:
        return self.name

    def __str__(self):
        return self.name


class Commit:

    def __init__(
        self,
        writer: Callable[..., ConventionalCommitMessage],
        type: str | None = None,
        scope: Sequence[str] | None = None,
        description: str | None = None,
        body: str | None = None,
        footer: dict | None = None,
        action: ReleaseAction | None = None,
        type_description: str | None = None,
        sha: str | None = None,
        authors: Sequence[User] | None = None,
        committer: User | None = None,
        jinja_env_vars: dict | None = None,
        dev_id: str | None = None,
    ):
        self._writer = writer
        self.type = type
        self.scope = scope or []
        self.description = description or ""
        self.body = body or ""
        self.footer = CommitFooter(footer or {})
        self.action = action
        self.type_description = type_description
        self.sha = sha
        self.authors = authors or []
        self.committer = committer
        self.jinja_env_vars = jinja_env_vars or {}
        self.dev_id = dev_id
        return

    def __str__(self):
        return str(self.conv_msg)

    def __repr__(self):
        parts = ["Commit("] + [
            f"  {name} = {val}," for name, val in (
                ("type", self.type),
                ("scope", self.scope),
                ("description", self.description),
                ("body", self.body),
                ("footer", self.footer),
                ("action", self.action),
                ("sha", self.sha),
                ("authors", self.authors),
                ("committer", self.committer),
                ("jinja_env_vars", self.jinja_env_vars),
            )
        ] + [")"]
        return "\n".join(parts)

    @property
    def conv_msg(self) -> ConventionalCommitMessage:
        return self._writer(
            type=self.type,
            scope=self.scope,
            description=self._fill_jinja_templates(self.description),
            body=self._fill_jinja_templates(self.body),
            footer=self._fill_jinja_templates(self.footer.as_dict),
        )

    @property
    def summary(self) -> str:
        if not self.type:
            return self.description
        return self.conv_msg.summary

    def _fill_jinja_templates(self, templates: dict | list | str, env_vars: dict | None = None) -> dict | list | str:

        def recursive_fill(template):
            if isinstance(template, dict):
                return {recursive_fill(key): recursive_fill(value) for key, value in template.items()}
            if isinstance(template, list):
                return [recursive_fill(value) for value in template]
            if isinstance(template, str):
                return jinja2.Template(template).render(
                    self.jinja_env_vars | {"now": date.from_now()} | (env_vars or {})
                )
            return template

        return recursive_fill(templates)


class CommitFooter:

    def __init__(self, data):
        self._data = data or {}
        return

    @property
    def initialize_project(self) -> bool:
        return self._data.get("initialize-project", False)

    @property
    def squash(self) -> bool | None:
        return self._data.get("squash")

    @property
    def publish_github(self) -> bool | None:
        return self._data.get("publish-github")

    @property
    def publish_zenodo(self) -> bool | None:
        return self._data.get("publish-zenodo")

    @property
    def publish_zenodo_sandbox(self) -> bool | None:
        return self._data.get("publish-zenodo-sandbox")

    @property
    def publish_pypi(self,) -> bool | None:
        return self._data.get("publish-pypi")

    @property
    def publish_testpypi(self) -> bool | None:
        return self._data.get("publish-testpypi")

    @property
    def version(self) -> PEP440SemVer | None:
        version = self._data.get("version")
        if version:
            try:
                return PEP440SemVer(version)
            except Exception as e:
                _logger.critical(f"Invalid version string '{version}' in commit footer: {e}")
                raise ProManException()
        return

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        return

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def pop(self, key, default=None):
        return self._data.pop(key, default)

    def setdefault(self, key, default):
        return self._data.setdefault(key, default)

    @property
    def as_dict(self):
        return self._data


class IssueForm(_NamedTuple):
    id: str
    commit: Commit
    id_labels: list[Label]
    issue_assignees: list[User]
    pull_assignees: list[User]
    review_assignees: list[User]
    labels: list[Label]
    role: dict[str, dict[str, int] | None]
    name: str
    description: str
    projects: list[str]
    title: str
    body: list[dict]
    processed_body: str | dict


@_dataclass(frozen=True)
class Label:
    """GitHub Issues Label.

    Attributes
    ----------
    category : LabelType
        Label category.
    name : str
        Full name of the label.
    group_id : str
        Key of the custom group.
        Only available if `category` is `LabelType.CUSTOM_GROUP`.
    id : IssueStatus | str
        Key of the label.
        Only available if `category` is not `LabelType.BRANCH`, `LabelType.VERSION`, or `LabelType.UNKNOWN`.
        For `LabelType.STATUS`, it is a `IssueStatus` enum.
    """
    category: LabelType
    name: str
    group_id: str = ""
    id: IssueStatus | str = ""
    prefix: str = ""
    suffix: str = ""
    color: str = ""
    description: str = ""

    def __post_init__(self):
        if self.category == LabelType.STATUS and not isinstance(self.id, IssueStatus):
            object.__setattr__(self, "id", IssueStatus(self.id))
        if self.color:
            object.__setattr__(self, "color", _pcit.color.css(self.color).css_hex().removeprefix("#"))
        return


class User(PropertyDict):

    def __init__(
        self,
        id: str | int,
        member: bool,
        data: dict,
        github_association: str | None = None,
        current_role: dict[str, int] | None = None
    ):
        self.id = id
        self.member = member
        self.github_association = github_association
        self.current_role = current_role
        super().__init__(data)
        return

    @property
    def md_name(self) -> str:
        """The user's name as a markdown link."""
        name = self._data["name"]["full"]
        url = (
            self._data.get("github", {}).get("url")
            or self._data.get("email", {}).get("url")
            or self._data.get("linkedin", {}).get("url")
            or self._data.get("researchgate", {}).get("url")
            or self._data.get("twitter", {}).get("url")
            or self._data.get("website", {}).get("url")
            or self._data.get("orcid", {}).get("url")
        )
        if url:
            return f"[{name}]({url})"
        return name

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id and self.member == other.member


class Tasklist:

    def __init__(self, tasks: list[MainTasklistEntry]):
        self.tasks = tasks
        return

    @property
    def complete(self) -> bool:
        return all(task.complete for task in self.tasks)

    @property
    def as_list(self) -> list[dict]:
        return [task.as_dict for task in self.tasks]


class TasklistEntry:

    def __init__(
        self,
        body: str,
        complete: bool,
        subtasks: tuple[SubTasklistEntry, ...],
    ):
        self.body = body
        self._complete = complete
        self.subtasks = subtasks
        return

    def mark_as_complete(self):
        self._complete = True
        for subtask in self.subtasks:
            subtask.mark_as_complete()
        return

    @property
    def complete(self) -> bool:
        if self._complete:
            return True
        self._complete = all(subtask.complete for subtask in self.subtasks)
        return self._complete

    @property
    def as_dict(self) -> dict:
        return {
            "body": self.body,
            "complete": self.complete,
            "subtasks": [subtask.as_dict for subtask in self.subtasks]
        }


class MainTasklistEntry(TasklistEntry):

    def __init__(
        self,
        commit: Commit,
        body: str,
        complete: bool,
        subtasks: tuple[SubTasklistEntry, ...],
    ):
        self._commit = commit
        super().__init__(body=body, complete=complete, subtasks=subtasks)
        return

    @property
    def summary(self) -> str:
        return self._commit.summary

    @property
    def commit_id(self) -> str:
        return self._commit.dev_id

    @property
    def as_dict(self) -> dict:
        return super().as_dict | {
            "description": self._commit.description,
            "type_id": self.commit_id,
        }


class SubTasklistEntry(TasklistEntry):

    def __init__(
        self,
        description: str,
        body: str,
        complete: bool,
        subtasks: tuple[SubTasklistEntry, ...],
    ):
        self.description = description
        super().__init__(body=body, complete=complete, subtasks=subtasks)
        return

    @property
    def summary(self) -> str:
        return self.description

    @property
    def as_dict(self) -> dict:
        return super().as_dict | {"description": self.description}
