from __future__ import annotations

import copy
from typing import TYPE_CHECKING
from pathlib import Path

import controlman
import gittidy
import jinja2
import mdit
import github_contexts
from proman.util import date
from proman import const
import controlman.exception as controlman_exception
from controlman import data_validator as _data_validator
from loggerman import logger
import pylinks
import pyserials as ps

from proman.exception import ProManException
from proman.report import Reporter
from proman.token_manager import create as _create_token_manager

# from proman.manager.announcement import AnnouncementManager
from proman.manager.branch import BranchManager
from proman.manager.cache import CacheManager
from proman.manager.changelog import ChangelogManager
from proman.manager.commit import CommitManager
from proman.manager.control import ControlCenterManager
from proman.manager.issue import IssueManager
from proman.manager.label import LabelManager
from proman.manager.output import OutputManager
from proman.manager.protocol import ProtocolManager
from proman.manager.release import ReleaseManager
from proman.manager.repo import RepoManager
from proman.manager.user import UserManager
from proman.manager.variable import VariableManager

if TYPE_CHECKING:
    from github_contexts.github import GitHubContext
    from github_contexts.github.payload.object import Issue, PullRequest
    from gittidy import Git
    from pylinks.api.github import Repo as GitHubRepoAPI, GitHub as GitHubBareAPI
    from pylinks.site.github import Repo as GitHubLink
    from pyserials.nested_dict import NestedDict

    from proman.dstruct import User
    from proman.token_manager import TokenManager


def create(
    token_manager: TokenManager | None = None,
    reporter: Reporter | None = None,
    jinja_env_vars: dict | None = None,
    github_context: dict | GitHubContext | None = None,
    repo_path: str | Path | None = None,
    metadata_ref: str | None = None,
    metadata_filepath: str | None = None,
    repo_path_main: str | Path | None = None,
    metadata_filepath_main: str | None = None,
    validate_metadata: bool = True,
) -> Manager:
    token_manager = token_manager or _create_token_manager()
    reporter = reporter or Reporter()
    if isinstance(github_context, dict):
        github_context = github_contexts.github.create(github_context)
    git_api = create_git_api(repo_path=repo_path)
    git_api_main = create_git_api(repo_path=repo_path_main) if repo_path_main else git_api
    project_metadata = load_metadata(
        repo=git_api,
        ref=metadata_ref,
        validate=validate_metadata,
        filepath=metadata_filepath,
        reporter=reporter,
    )
    github_api_bare = pylinks.api.github(token=token_manager.github.get())
    if github_context:
        default_branch = github_context.event.repository.default_branch
        repo_owner = github_context.repository_owner
        repo_name = github_context.repository_name
    else:
        default_branch = git_api_main.get_remote_default_branch()
        repo_address = git_api_main.get_remote_repo_name(
            remote_name="origin", remote_purpose="push", fallback_name=False, fallback_purpose=False
        )
        if not repo_address:
            raise controlman_exception.data_gen.RemoteGitHubRepoNotFoundError(
                repo_path=git_api.repo_path,
                remotes=git_api.get_remotes(),
            )
        repo_owner, repo_name = repo_address
    github_api_actions = github_api_bare.user(repo_owner).repo(repo_name)
    github_api_admin = (
        pylinks.api.github(token=token_manager.github_admin.get()).user(repo_owner).repo(repo_name)
    )
    github_link = pylinks.site.github.user(repo_owner).repo(repo_name)

    main_ref = git_api_main.commit_hash(default_branch)
    current_ref = git_api.commit_hash(metadata_ref or "HEAD")
    ref_is_main = current_ref == main_ref
    main_metadata = (
        project_metadata
        if ref_is_main
        else load_metadata(
            repo=git_api_main,
            ref=main_ref,
            validate=validate_metadata,
            filepath=metadata_filepath_main,
            reporter=reporter,
        )
    )
    default_jinja_env_vars = {
        "mdit": mdit,
        "ccc": main_metadata,
    }
    if github_context:
        default_jinja_env_vars.update(
            {
                "event": github_context.event_name.value,
                "action": github_context.event.action.value
                if "action" in github_context.event
                else "",
                "context": github_context,
                "payload": github_context.event,
            }
        )
    full_jinja_env_vars = default_jinja_env_vars | (jinja_env_vars or {})
    main_manager = Manager(
        project_metadata=main_metadata,
        token_manager=token_manager,
        git_api=git_api_main,
        github_api_actions=github_api_actions,
        github_api_admin=github_api_admin,
        github_api_bare=github_api_bare,
        github_link=github_link,
        reporter=reporter,
        jinja_env_vars=full_jinja_env_vars,
        github_context=github_context,
        main_manager=None,
    )
    if github_context:
        main_manager.jinja_env_vars["sender"] = main_manager.user.from_payload_sender()
    return Manager(
        project_metadata=project_metadata,
        token_manager=token_manager,
        git_api=git_api,
        github_api_actions=github_api_actions,
        github_api_admin=github_api_admin,
        github_api_bare=github_api_bare,
        github_link=github_link,
        reporter=reporter,
        jinja_env_vars=full_jinja_env_vars,
        github_context=github_context,
        main_manager=main_manager,
    )


def update(
    manager: Manager,
    project_metadata: NestedDict,
) -> Manager:
    """Create a new Manager instance with updated project metadata."""
    return Manager(
        project_metadata=project_metadata,
        token_manager=manager.token,
        git_api=manager.git,
        github_api_actions=manager.gh_api_actions,
        github_api_admin=manager.gh_api_admin,
        github_api_bare=manager.gh_api_bare,
        github_link=manager.gh_link,
        reporter=manager.reporter,
        jinja_env_vars=manager.jinja_env_vars,
        github_context=manager.gh_context,
        main_manager=manager.main,
    )


def load_metadata(
    repo: str | Path | Git,
    ref: str | None = None,
    filepath: str | None = None,
    validate: bool = True,
    reporter: Reporter | None = None,
) -> ps.NestedDict:
    """Load project metadata from the metadata JSON file.

    Parameters
    ----------
    repo
        Git instance or path to the repository root.
    ref
        Git reference to load the metadata from.
        If not provided, the latest commit on the current branch is used.
    validate
        Whether to validate read data against the schema.
    filepath
        Relative path to the JSON file in the repository.
    reporter
        Reporter instance to report the status of the operation.

    Raises
    ------
    controlman.exception.ControlManFileReadError
        If the file cannot be read.
    """
    filepath = filepath or const.FILEPATH_METADATA
    git_api = create_git_api(repo_path=repo) if isinstance(repo, str | Path) else repo
    reporter = reporter or Reporter()
    log_title = "Metadata Load"
    if ref:
        log_ref = ref
        data_str = git_api.file_at_ref(
            ref=ref,
            path=filepath,
        )
        try:
            project_metadata = ps.read.json_from_string(data=data_str)
        except ps.exception.read.PySerialsReadException as e:
            raise controlman_exception.load.ControlManInvalidMetadataError(
                cause=e, filepath=filepath, commit_hash=ref
            ) from None
    else:
        ref = git_api.commit_hash_normal()
        branch_name = git_api.current_branch_name()
        log_ref = f"HEAD of {branch_name} (commit {ref})"
        fullpath = git_api.repo_path / filepath
        try:
            project_metadata = ps.read.json_from_file(path=fullpath)
        except ps.exception.read.PySerialsReadException as e:
            raise controlman_exception.load.ControlManInvalidMetadataError(
                cause=e, filepath=fullpath
            ) from None

    err_msg = f"Failed to load metadata file from {log_ref}."
    logger.success(
        log_title,
        f"Metadata loaded successfully from {log_ref}.",
    )
    if validate:
        try:
            _data_validator.validate(data=project_metadata, fill_defaults=False)
        except controlman.exception.load.ControlManInvalidMetadataError as e:
            logger.critical(
                log_title,
                err_msg,
                e.report.body["problem"].content,
            )
            reporter.update(
                "main",
                status="fail",
                summary=f"Failed to load metadata from {log_ref}.",
            )
            raise ProManException()
        except controlman.exception.load.ControlManSchemaValidationError as e:
            logger.critical(
                log_title,
                err_msg,
                e.report.body["problem"].content,
            )
            reporter.update(
                "main",
                status="fail",
                summary=f"Failed to load metadata from {log_ref}.",
            )
            raise ProManException()
    return ps.NestedDict(project_metadata)


def create_git_api(repo_path: str | Path | None = None) -> Git:
    repo_path = Path(repo_path).resolve() if repo_path else Path.cwd()
    return gittidy.Git(path=repo_path, logger=logger)


class Manager:
    def __init__(
        self,
        project_metadata: NestedDict,
        token_manager: TokenManager,
        git_api: Git,
        github_api_actions: GitHubRepoAPI,
        github_api_admin: GitHubRepoAPI,
        github_api_bare: GitHubBareAPI,
        github_link: GitHubLink,
        reporter: Reporter,
        jinja_env_vars: dict,
        github_context: GitHubContext | None = None,
        main_manager: Manager | None = None,
    ):
        self._meta = project_metadata
        self._token_manager = token_manager
        self._git_api = git_api
        self._gh_api_actions = github_api_actions
        self._gh_api_admin = github_api_admin
        self._gh_api_bare = github_api_bare
        self._gh_link = github_link
        self._reporter = reporter
        self._jinja_env_vars = jinja_env_vars
        self._github_context = github_context
        self._main_manager = main_manager or self
        self._cache_manager = CacheManager(self)
        self._branch_manager = BranchManager(self)
        self._changelog_manager = ChangelogManager(self)
        self._commit_manager = CommitManager(self)
        self._issue_manager = IssueManager(self)
        self._label_manager = LabelManager(self)
        self._output_manager = OutputManager(self)
        self._protocol_manager = ProtocolManager(self)
        self._user_manager = UserManager(self)
        self._repo_manager = RepoManager(self)
        self._variable_manager = VariableManager(self)
        self._release_manager = ReleaseManager(
            self
        )  # must be after self._variable_manager as ZenodoManager needs it at init
        return

    def update_data(self, data: NestedDict):
        self._meta = data
        return

    def control_center(
        self,
        future_versions: dict[str, str] | None = None,
        control_center_path: str | None = None,
        clean_state: bool = False,
    ):
        if not control_center_path:
            control_center_path = self.data.get("control.path")
        if not control_center_path:
            raise ValueError("Control center path not provided.")
        control_center_path = self.git.repo_path / control_center_path
        if not control_center_path.is_dir():
            raise ValueError(f"Invalid control center path '{control_center_path}'")
        return ControlCenterManager(
            manager=self,
            cc_path=control_center_path,
            future_versions=future_versions,
            clean_state=clean_state,
        )

    @property
    def main(self) -> Manager:
        return self._main_manager

    @property
    def reporter(self) -> Reporter:
        return self._reporter

    @property
    def data(self) -> NestedDict:
        return self._meta

    @property
    def git(self) -> Git:
        return self._git_api

    @property
    def jinja_env_vars(self) -> dict:
        return self._jinja_env_vars

    @property
    def gh_api_bare(self) -> GitHubBareAPI:
        return self._gh_api_bare

    @property
    def gh_api_actions(self) -> GitHubRepoAPI:
        return self._gh_api_actions

    @property
    def gh_api_admin(self) -> GitHubRepoAPI:
        return self._gh_api_admin

    @property
    def gh_context(self) -> GitHubContext | None:
        return self._github_context

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
    def output(self) -> OutputManager:
        return self._output_manager

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
    def token(self) -> TokenManager:
        return self._token_manager

    @property
    def user(self) -> UserManager:
        return self._user_manager

    @property
    def variable(self) -> VariableManager:
        return self._variable_manager

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
                    self.reporter.update(
                        "main",
                        status="fail",
                        summary=f"Failed to render Jinja template at '{path}'.",
                    )
                    raise ProManException()
                return filled
            return template

        return recursive_fill(templates, jsonpath)
