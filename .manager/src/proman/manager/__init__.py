from __future__ import annotations as _annotations

import copy
from typing import TYPE_CHECKING as _TYPE_CHECKING

import controlman
import jinja2
from controlman import date
from controlman.cache_manager import CacheManager
from loggerman import logger

from proman.exception import ProManException

# from proman.manager.announcement import AnnouncementManager
from proman.manager.branch import BranchManager
from proman.manager.changelog import ChangelogManager
from proman.manager.commit import CommitManager
from proman.manager.issue import IssueManager
from proman.manager.label import LabelManager
from proman.manager.protocol import ProtocolManager
from proman.manager.release import ReleaseManager
from proman.manager.repo import RepoManager
from proman.manager.user import UserManager
from proman.manager.variable import VariableManager

if _TYPE_CHECKING:
    from github_contexts import GitHubContext
    from github_contexts.github.payload.object import Issue, PullRequest
    from gittidy import Git
    from pylinks.api.github import Repo as GitHubRepoAPI
    from pylinks.site.github import Repo as GitHubLink
    from pyserials.nested_dict import NestedDict

    from proman.dstruct import Token, User
    from proman.report import Reporter


class Manager:
    def __init__(
        self,
        data: NestedDict,
        git_api: Git,
        jinja_env_vars: dict,
        github_context: GitHubContext,
        github_api_actions: GitHubRepoAPI,
        github_api_admin: GitHubRepoAPI,
        github_link: GitHubLink,
        zenodo_token: Token,
        zenodo_sandbox_token: Token,
        reporter: Reporter,
    ):
        self._data = data
        self._git = git_api
        self._jinja_env_vars = jinja_env_vars
        self._gh_context = github_context
        self._gh_api_actions = github_api_actions
        self._gh_api_admin = github_api_admin
        self._gh_link = github_link
        self._zenodo_token = zenodo_token
        self._zenodo_sandbox_token = zenodo_sandbox_token
        self._reporter = reporter

        self._cache_manager = CacheManager(
            path_local_cache=self._git.repo_path / data["local.cache.path"],
            retention_hours=data["control.cache.retention_hours"],
        )
        self._branch_manager = BranchManager(self)
        self._changelog_manager = ChangelogManager(self)
        self._commit_manager = CommitManager(self)
        self._issue_manager = IssueManager(self)
        self._label_manager = LabelManager(self)
        self._protocol_manager = ProtocolManager(self)
        self._user_manager = UserManager(self)
        self._repo_manager = RepoManager(self)
        self._variable_manager = VariableManager(self)
        self._release_manager = ReleaseManager(
            self
        )  # must be after self._variable_manager as ZenodoManager needs it at init
        return

    @property
    def reporter(self) -> Reporter:
        return self._reporter

    @property
    def data(self) -> NestedDict:
        return self._data

    @property
    def git(self) -> Git:
        return self._git

    @property
    def jinja_env_vars(self) -> dict:
        return self._jinja_env_vars

    @property
    def gh_context(self) -> GitHubContext:
        return self._gh_context

    @property
    def gh_api_actions(self) -> GitHubRepoAPI:
        return self._gh_api_actions

    @property
    def gh_api_admin(self) -> GitHubRepoAPI:
        return self._gh_api_admin

    @property
    def gh_link(self) -> GitHubLink:
        return self._gh_link

    @property
    def branch(self) -> BranchManager:
        return self._branch_manager

    @property
    def changelog(self) -> ChangelogManager:
        return self._changelog_manager

    @property
    def commit(self) -> CommitManager:
        return self._commit_manager

    @property
    def cache(self) -> CacheManager:
        return self._cache_manager

    @property
    def issue(self) -> IssueManager:
        return self._issue_manager

    @property
    def label(self) -> LabelManager:
        return self._label_manager

    @property
    def protocol(self) -> ProtocolManager:
        return self._protocol_manager

    @property
    def release(self) -> ReleaseManager:
        return self._release_manager

    @property
    def repo(self) -> RepoManager:
        return self._repo_manager

    @property
    def user(self) -> UserManager:
        return self._user_manager

    @property
    def variable(self) -> VariableManager:
        return self._variable_manager

    @property
    def zenodo_token(self) -> Token:
        return self._zenodo_token

    @property
    def zenodo_sandbox_token(self) -> Token:
        return self._zenodo_sandbox_token

    def add_issue_jinja_env_var(self, issue: Issue):
        issue_copy = copy.deepcopy(issue)
        issue_copy["user"] = self.user.from_issue_author(issue)
        self.jinja_env_vars["issue"] = issue_copy
        return issue_copy

    def add_pull_request_jinja_env_var(
        self, pull: PullRequest | dict, author: User | None = None
    ) -> PullRequest | dict:
        pull = copy.deepcopy(pull)
        pull["user"] = author or self.user.from_issue_author(pull)
        pull["head"] = self.branch.from_pull_request_branch(pull["head"])
        pull["base"] = self.branch.from_pull_request_branch(pull["base"])
        self.jinja_env_vars["pull_request"] = pull
        return pull

    def fill_jinja_template(self, template: str, env_vars: dict | None = None) -> str:
        return jinja2.Template(template).render(
            self.jinja_env_vars | {"now": date.from_now()} | (env_vars or {})
        )

    def fill_jinja_templates(
        self, templates: dict | list | str, jsonpath: str, env_vars: dict | None = None
    ) -> dict:
        def recursive_fill(template, path):
            if isinstance(template, dict):
                filled = {}
                for key, value in template.items():
                    new_path = f"{path}.{key}"
                    filled[recursive_fill(key, new_path)] = recursive_fill(value, new_path)
                return filled
            if isinstance(template, list):
                filled = []
                for idx, value in enumerate(template):
                    new_path = f"{path}[{idx}]"
                    filled.append(recursive_fill(value, new_path))
                return filled
            if isinstance(template, str):
                try:
                    filled = self.fill_jinja_template(template, env_vars)
                except Exception as e:
                    logger.critical(
                        "Jinja Templating",
                        f"Failed to render Jinja template at '{path}': {e}",
                        logger.traceback(),
                    )
                    self.reporter.add(
                        name="main",
                        status="fail",
                        summary=f"Failed to render Jinja template at '{path}'.",
                    )
                    raise ProManException()
                return filled
            return template

        return recursive_fill(templates, jsonpath)

    @staticmethod
    def normalize_github_date(date_str: str) -> str:
        return date.to_internal(date.from_github(date_str))


def from_metadata_json(
    git_api: Git,
    jinja_env_vars: dict,
    github_context: GitHubContext,
    github_api_actions: GitHubRepoAPI,
    github_api_admin: GitHubRepoAPI,
    github_link: GitHubLink,
    reporter: Reporter,
    zenodo_token: Token,
    zenodo_sandbox_token: Token,
    commit_hash: str | None = None,
) -> Manager:
    branch_name = git_api.current_branch_name()
    address = f"from the {branch_name} branch of the {repo} repository"
    log_title = f"Metadata Load ({branch_name})"
    err_msg = f"Failed to load metadata file {address}."
    try:
        if commit_hash:
            data = controlman.from_json_file_at_commit(
                git_manager=git_api,
                commit_hash=commit_hash,
            )
        else:
            data = controlman.from_json_file(repo_path=git_api.repo_path)
        logger.success(
            log_title,
            f"Metadata loaded successfully {address}.",
        )
        return Manager(
            data=data,
            git_api=git_api,
            jinja_env_vars=jinja_env_vars,
            github_context=github_context,
            github_api_actions=github_api_actions,
            github_api_admin=github_api_admin,
            github_link=github_link,
            zenodo_token=zenodo_token,
            zenodo_sandbox_token=zenodo_sandbox_token,
            reporter=reporter,
        )
    except controlman.exception.load.ControlManInvalidMetadataError as e:
        logger.critical(
            log_title,
            err_msg,
            e.report.body["problem"].content,
        )
        reporter.add(
            name="main",
            status="fail",
            summary=f"Failed to load metadata {address}.",
            section="",
        )
        raise ProManException()
    except controlman.exception.load.ControlManSchemaValidationError as e:
        logger.critical(
            log_title,
            err_msg,
            e.report.body["problem"].content,
        )
        reporter.add(
            name="main",
            status="fail",
            summary=f"Failed to load metadata {address}.",
            section="",
        )
        raise ProManException()
