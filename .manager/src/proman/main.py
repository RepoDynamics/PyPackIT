"""Main event handler."""

from __future__ import annotations

from typing import TYPE_CHECKING

import controlman
import gittidy
import htmp
import mdit
import pkgdata
import pylinks
import pyserials as _ps
import pyshellman
from github_contexts.github import enum as _ghc_enum
from loggerman import logger
from pylinks.exception.api import WebAPIError as _WebAPIError
from versionman.pep440_semver import PEP440SemVer

from proman import script as _script

from proman import manager, runner
from proman.dstruct import Branch
from proman.dtype import InitCheckAction, RepoFileType
from proman.exception import ProManException

if TYPE_CHECKING:
    from typing import Literal

    from github_contexts import GitHubContext
    from pylinks.api.github import Repo as GitHubRepoAPI
    from pylinks.site.github import Repo as GitHubRepoLink

    from proman.dstruct import Token, User
    from proman.manager import Manager
    from proman.output import OutputManager
    from proman.report import Reporter


class EventHandler:
    _REPODYNAMICS_BOT_USER = (
        "RepoDynamicsBot",
        "146771514+RepoDynamicsBot@users.noreply.github.com",
    )
    # TODO: make authenticated
    # Refs:
    # - https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits
    # - https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key
    # - https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account
    # - https://github.com/crazy-max/ghaction-import-gpg
    # - https://stackoverflow.com/questions/61096521/how-to-use-gpg-key-in-github-actions
    # - https://github.com/sigstore/gitsign
    # - https://www.chainguard.dev/unchained/keyless-git-commit-signing-with-gitsign-and-github-actions
    # - https://github.com/actions/runner/issues/667
    # - https://sourceforge.net/projects/gpgosx/
    # - https://www.gnupg.org/download/

    def __init__(
        self,
        github_context: GitHubContext,
        reporter: Reporter,
        output_writer: OutputManager,
        admin_token: Token,
        zenodo_token: Token,
        zenodo_sandbox_token: Token,
        path_repo_base: str,
        path_repo_head: str,
    ):
        @logger.sectioner("GitHub API Initialization")
        def init_github_api() -> tuple[GitHubRepoAPI, GitHubRepoAPI, GitHubRepoLink, bool]:
            repo_user = self.gh_context.repository_owner
            repo_name = self.gh_context.repository_name
            link_gen = pylinks.site.github.user(repo_user).repo(repo_name)
            api_admin, api_actions = (
                pylinks.api.github(token=token).user(repo_user).repo(repo_name)
                for token in (admin_token.get(), self.gh_context.token)
            )
            log_title = "Admin Token Verification"
            if not admin_token:
                has_admin_token = False
                if in_repo_creation_event:
                    logger.info(
                        log_title,
                        "Repository creation event detected; no admin token required.",
                    )
                elif self.gh_context.event.repository.fork:
                    logger.info(
                        log_title,
                        "Forked repository detected; no admin token required.",
                    )
                else:
                    logger.critical(
                        log_title,
                        "No admin token provided.",
                    )
                    reporter.add(
                        name="main",
                        status="fail",
                        summary="No admin token provided.",
                    )
                    raise ProManException()
            else:
                try:
                    check = api_admin.info
                except _WebAPIError as e:
                    details = e.report.body
                    details.extend(*e.report.section["details"].content.body.elements())
                    logger.critical(
                        log_title, "Failed to verify the provided admin token.", details
                    )
                    reporter.add(
                        name="main",
                        status="fail",
                        summary="Failed to verify the provided admin token.",
                        section=mdit.document(
                            heading="Admin Token Verification",
                            body=details.elements(),
                        ),
                    )
                    raise ProManException()
                has_admin_token = True
                logger.success(
                    log_title,
                    "Admin token verified successfully.",
                )
            return api_admin, api_actions, link_gen, has_admin_token

        @logger.sectioner("Git API Initialization")
        def init_git_api() -> tuple[gittidy.Git, gittidy.Git]:
            apis = []
            for path, title in ((path_repo_base, "Base Repo"), (path_repo_head, "Head Repo")):
                with logger.sectioning(title):
                    git_api = gittidy.Git(
                        path=path,
                        user=(
                            self.gh_context.event.sender.login,
                            self.gh_context.event.sender.github_email,
                        ),
                        user_scope="global",
                        committer=self._REPODYNAMICS_BOT_USER,
                        committer_scope="local",
                        committer_persistent=True,
                        logger=logger,
                    )
                    apis.append(git_api)
            return apis[0], apis[1]

        self._gh_context = github_context
        self._reporter = reporter
        self._output_manager = output_writer
        self._zenodo_token = zenodo_token
        self._zenodo_sandbox_token = zenodo_sandbox_token

        in_repo_creation_event = (
            self.gh_context.event_name is _ghc_enum.EventType.PUSH
            and self.gh_context.ref_type is _ghc_enum.RefType.BRANCH
            and self.gh_context.event.action is _ghc_enum.ActionType.CREATED
            and self.gh_context.ref_is_main
        )

        self._gh_api_admin, self._gh_api, self._gh_link, self._has_admin_token = init_github_api()
        self._git_base, self._git_head = init_git_api()
        self._path_base = self._git_base.repo_path
        self._path_head = self._git_head.repo_path
        self._shell_runner_head = pyshellman.Runner(cwd=self._path_head, logger=logger)
        self._jinja_env_vars = {
            "event": self.gh_context.event_name.value,
            "action": self.gh_context.event.action.value
            if "action" in self.gh_context.event
            else "",
            "context": self.gh_context,
            "payload": self.gh_context.event,
            "mdit": mdit,
        }
        self.manager: Manager = None
        if not in_repo_creation_event:
            self.manager = self.manager_from_metadata_file(repo="base")
            self._jinja_env_vars.update({"ccc": self.manager.data, "sender": self.payload_sender})
        return

    @property
    def gh_context(self) -> GitHubContext:
        return self._gh_context

    @property
    def reporter(self) -> Reporter:
        return self._reporter

    @property
    def output_manager(self) -> OutputManager:
        return self._output_manager

    @property
    def jinja_env_vars(self) -> dict:
        return self._jinja_env_vars

    @logger.sectioner("Metadata Load")
    def manager_from_metadata_file(
        self,
        repo: Literal["base", "head"],
        commit_hash: str | None = None,
    ) -> Manager:
        return manager.from_metadata_json(
            git_api=self._git_base if repo == "base" else self._git_head,
            jinja_env_vars=self.jinja_env_vars,
            github_context=self.gh_context,
            github_api_actions=self._gh_api,
            github_api_admin=self._gh_api_admin,
            reporter=self.reporter,
            commit_hash=commit_hash,
            github_link=self._gh_link,
            zenodo_token=self._zenodo_token,
            zenodo_sandbox_token=self._zenodo_sandbox_token,
        )

    def manager_from_loaded_data(
        self,
        data: _ps.NestedDict,
        git_api: gittidy.Git,
    ) -> Manager:
        return manager.Manager(
            data=data,
            git_api=git_api,
            jinja_env_vars=self._jinja_env_vars,
            github_context=self.gh_context,
            github_api_actions=self._gh_api,
            github_api_admin=self._gh_api_admin,
            github_link=self._gh_link,
            zenodo_token=self._zenodo_token,
            zenodo_sandbox_token=self._zenodo_sandbox_token,
            reporter=self.reporter,
        )

    def run_sync_fix(
        self,
        branch_manager: Manager,
        action: InitCheckAction,
        future_versions: dict | None = None,
        testpypi_publishable: bool = False,
    ) -> tuple[Manager, dict[str, bool], str]:
        changes = self.run_change_detection(branch_manager=branch_manager)
        if "dynamic" in changes:
            new_manager, commit_hash_cca = self.run_cca(
                branch_manager=branch_manager,
                action=action,
                future_versions=future_versions,
            )
        else:
            new_manager = branch_manager
            commit_hash_cca = None
        commit_hash_refactor = (
            self.run_refactor(
                branch_manager=new_manager,
                action=action,
                ref_range=(self.gh_context.hash_before, self.gh_context.hash_after),
            )
            if new_manager.data["workflow.refactor.pre_commit_config"]
            else None
        )
        if commit_hash_refactor or commit_hash_cca:
            with logger.sectioning("Repository Update"):
                new_manager.git.push()
        latest_hash = commit_hash_refactor or commit_hash_cca or self.gh_context.hash_after
        job_runs = {
            "cca": any(filetype in changes for filetype in (RepoFileType.CC, RepoFileType.DYNAMIC)),
            "web_build": changes["web"],
            "package_test": changes["pkg"] or changes["test"],
            "package_build": changes["pkg"],
            "package_lint": changes["pkg"],
            "test_lint": changes["test"],
            "package_publish_testpypi": (changes["pkg"] or changes["test"])
            and testpypi_publishable,
        }
        logger.info(
            "Job Runs",
            str(job_runs),
        )
        return new_manager, job_runs, latest_hash

    @logger.sectioner("File Change Detection")
    def run_change_detection(
        self,
        branch_manager: Manager,
        ref_range: tuple[str, str] | None = None,
    ) -> dict[str, bool]:
        if not ref_range:
            ref_range = (self.gh_context.hash_before, self.gh_context.hash_after)
        changes = self._git_head.changed_files(ref_start=ref_range[0], ref_end=ref_range[1])
        changed_components = runner.change_detector.run(
            data=branch_manager.data,
            changes=changes,
            reporter=self.reporter,
        )
        logger.info(
            "Changed Project Components",
            str(changed_components),
        )
        return changed_components

    @logger.sectioner("Continuous Configuration Automation")
    def run_cca(
        self,
        branch_manager: Manager | None,
        action: InitCheckAction,
        future_versions: dict[str, str | PEP440SemVer] | None = None,
    ) -> tuple[Manager, str | None]:
        git = branch_manager.git if branch_manager else self._git_head
        try:
            cc_manager = controlman.manager(
                repo=git,
                data_before=branch_manager.data if branch_manager else None,
                data_main=self.manager.data if self.manager else None,
                github_token=self.gh_context.token,
                future_versions=future_versions,
                control_center_path=".control" if not self.manager else None,
            )
            cc_reporter = cc_manager.report()
        except controlman.exception.ControlManException as e:
            self.reporter.add(
                name="cca",
                status="fail",
                summary=e.report.body["intro"].content,
                body=e.report.body,
                section=e.report.section,
                section_is_container=True,
            )
            raise ProManException()

        # Push/pull if changes are made and action is not 'fail' or 'report'
        commit_hash = None
        report = cc_reporter.report()
        new_branch_manager = self.manager_from_loaded_data(
            data=cc_manager.generate_data(), git_api=git
        )
        if not self.manager:
            self.manager = new_branch_manager
        summary = report.body["summary"].content
        if cc_reporter.has_changes and action not in [InitCheckAction.FAIL, InitCheckAction.REPORT]:
            with logger.sectioning("Synchronization"):
                pr_branch: Branch | None = None
                if action == InitCheckAction.PULL:
                    pr_branch = self.manager.branch.new_auto(auto_type="config_sync")
                    new_branch_manager.branch.checkout_to_auto(branch=pr_branch)
                cc_manager.apply_changes()
                commit_msg = (
                    self.manager.commit.create_auto(id="config_sync")
                    if action in [InitCheckAction.COMMIT, InitCheckAction.PULL]
                    else ""
                )
                commit_hash_before = new_branch_manager.git.commit_hash_normal()
                commit_hash_after = new_branch_manager.git.commit(
                    message=str(commit_msg) if action is not InitCheckAction.AMEND else "",
                    stage="all",
                    amend=(action is InitCheckAction.AMEND),
                )
                commit_hash = commit_hash_after
                # commit_hash = self.run_refactor(
                #     branch_manager=new_branch_manager,
                #     action=InitCheckAction.AMEND,
                #     ref_range=(commit_hash_before, commit_hash_after),
                #     internal=True,
                # ) or commit_hash_after
                description = "These were synced and changes were applied to "
                if pr_branch:
                    new_branch_manager.git.push(target="origin", set_upstream=True)
                    new_branch_manager.branch.checkout_from_auto()
                    pull_data = self._gh_api_admin.pull_create(
                        head=pr_branch.name,
                        base=pr_branch.target.name,
                        title=commit_msg.description,
                        body=report.source(
                            target="github", filters=["short, github"], separate_sections=False
                        ),
                    )
                    commit_hash = None
                    link = f"[#{pull_data['number']}]({pull_data['url']})"
                    description += f"branch {htmp.element.code(pr_branch.name)} in PR {link}."
                else:
                    link = f"[`{commit_hash[:7]}`]({self._gh_link.commit(commit_hash)})"
                    description += "the current branch " + (
                        f"in commit {link}."
                        if action == InitCheckAction.COMMIT
                        else f"by amending the latest commit (new hash: {link})."
                    )
                summary += f" {description}"
        self.reporter.add(
            name="cca",
            status="fail"
            if cc_reporter.has_changes
            and action in [InitCheckAction.FAIL, InitCheckAction.REPORT, InitCheckAction.PULL]
            else "pass",
            summary=summary,
            section=report.section,
            section_is_container=True,
        )
        return new_branch_manager, commit_hash

    @logger.sectioner("Continuous Refactoring")
    def run_refactor(
        self,
        branch_manager: Manager,
        action: InitCheckAction,
        ref_range: tuple[str, str] | None = None,
        internal: bool = False,
    ) -> str | None:
        if action == InitCheckAction.NONE:
            self.reporter.add(
                name="hooks",
                status="skip",
                summary="Hooks are disabled for this event type.",
            )
            return None
        # config = branch_manager.data["workflow.refactor.pre_commit_config"]
        # logger.info(
        #     "Pre-commit Config",
        #     str(config)
        # )
        # if not config:
        #     if not internal:
        #         oneliner = "Hooks are enabled but no pre-commit config set in <code>$.workflow.refactor.pre_commit_config</code>."
        #         logger.error(
        #             "Pre-commit Config",
        #             oneliner
        #         )
        #         self.reporter.add(
        #             name="hooks",
        #             status="fail",
        #             summary=oneliner,
        #         )
        #     return None
        if action in [InitCheckAction.FAIL, InitCheckAction.REPORT]:
            input_action = "report"
        elif action in [InitCheckAction.COMMIT, InitCheckAction.AMEND, InitCheckAction.PULL]:
            input_action = "validate"

        commit_msg = (
            self.manager.commit.create_auto("refactor")
            if action in [InitCheckAction.COMMIT, InitCheckAction.PULL]
            else ""
        )
        pr_branch: Branch | None = None
        if action == InitCheckAction.PULL:
            pr_branch = self.manager.branch.new_auto(auto_type="refactor")
            branch_manager.branch.checkout_to_auto(branch=pr_branch)
        try:
            hooks_output = _script.lint.run(
                config=branch_manager.git.repo_path / ".devcontainer/config/pre-commit-ci.yaml",
                action=input_action,
                hook_stage="manual",
                ref_range=ref_range,
            )
        except Exception as e:
            self._reporter.add(
                name="hooks",
                status="fail",
                summary="An unexpected error occurred.",
                body=str(e),
            )
            raise ProManException()
        passed = hooks_output["passed"]
        modified = hooks_output["modified"]
        commit_hash = None
        # Push/amend/pull if changes are made and action is not 'fail' or 'report'
        summary_addon_template = (
            " The modifications made during the first run were applied to {target}."
        )
        if pr_branch and modified:
            branch_manager.git.push(target="origin", set_upstream=True)
            pull_data = self._gh_api_admin.pull_create(
                head=pr_branch.name,
                base=pr_branch.target.name,
                title=commit_msg.description,
                body=commit_msg.body,
            )
            branch_manager.branch.checkout_from_auto()
            link = htmp.element.a(pull_data["number"], href=pull_data["url"])
            target = f"branch <code>{pr_branch}</code> and a pull request ({link}) was created"
            hooks_output["summary"] += summary_addon_template.format(target=target)
        if action in [InitCheckAction.COMMIT, InitCheckAction.AMEND] and modified:
            commit_hash = branch_manager.git.commit(message=str(commit_msg))
            # commit_hash = hooks_output["commit_hash"]
            link = htmp.element.a(commit_hash[:7], href=str(self._gh_link.commit(commit_hash)))
            target = "the current branch " + (
                f"in a new commit (hash: {link})"
                if action == InitCheckAction.COMMIT
                else f"by amending the latest commit (new hash: {link})"
            )
            hooks_output["summary"] += summary_addon_template.format(target=target)
        if not internal:
            self.reporter.add(
                name="hooks",
                status="fail"
                if not passed or (action == InitCheckAction.PULL and modified)
                else "pass",
                summary=hooks_output["summary"],
                body=hooks_output["description"],
                section=hooks_output["section"],
            )
        return commit_hash

    @property
    def payload_sender(self) -> User | None:
        return (
            self.manager.user.get_from_github_rest_id(self.gh_context.event.sender.id)
            if self.gh_context.event.sender
            else None
        )
