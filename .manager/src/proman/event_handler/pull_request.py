from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING

import controlman
from github_contexts import github as _gh_context
from loggerman import logger
from pylinks.exception.api import WebAPIError
from versionman.pep440_semver import PEP440SemVer

from proman.dtype import (
    BranchType,
    InitCheckAction,
    IssueStatus,
    LabelType,
    ReleaseAction,
)
from proman.event_handler.pull_request_target import PullRequestTargetEventHandler
from proman.exception import ProManException

if TYPE_CHECKING:
    from proman.dstruct import (
        Commit,
        IssueForm,
        Label,
        SubTasklistEntry,
        Tasklist,
        Version,
    )


class PullRequestEventHandler(PullRequestTargetEventHandler):
    _INTERNAL_HEAD_TO_BASE_MAP = {
        BranchType.PRE: (BranchType.MAIN, BranchType.RELEASE),
        BranchType.DEV: (BranchType.MAIN, BranchType.RELEASE, BranchType.PRE),
        BranchType.AUTO: (BranchType.MAIN, BranchType.RELEASE, BranchType.PRE, BranchType.DEV),
    }
    _EXTERNAL_HEAD_TO_BASE_MAP = {
        BranchType.DEV: (BranchType.DEV,),
        BranchType.PRE: (BranchType.PRE,),
        BranchType.RELEASE: (BranchType.RELEASE,),
        BranchType.MAIN: (BranchType.MAIN,),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._git_base.fetch_remote_branches_by_name(branch_names=self.gh_context.base_ref)
        self._git_base.checkout(branch=self.gh_context.base_ref)

        self.head_manager = self.manager_from_metadata_file(repo="head")
        self.head_manager_new = self.head_manager
        self.manager.protocol.load_from_pull(self.pull)
        self._issue_form: IssueForm = None
        self._commits: list[Commit] = []
        self._base_version: Version = None
        self._head_version: Version = None
        return

    @property
    def commits(self) -> list[Commit]:
        if not self._commits:
            self._commits = self.head_manager_new.commit.from_pull_request(
                pull_nr=self.pull.number,
                add_to_contributors=True,
            )
        return self._commits

    @property
    def head_commit(self) -> Commit:
        return self.commits[0]

    @property
    def base_version(self) -> Version:
        if not self._base_version:
            self._base_version = self.manager.release.latest_version()
        return self._base_version

    @property
    def head_version(self) -> Version:
        if not self._head_version:
            self._head_version = self.manager.release.latest_version(git=self._git_head)
        return self._head_version

    @property
    def issue_form(self) -> IssueForm:
        if not self._issue_form:
            self._issue_form = self.manager.issue.form_from_id_labels(self.pull.label_names)
        return self._issue_form

    @logger.sectioner("Pull Request Handler Execution")
    def run(self):
        if not self._head_to_base_allowed():
            return
        action = self.payload.action
        if action is _gh_context.enum.ActionType.OPENED:
            if self.branch_head.type is BranchType.PRE and self.branch_base.type in (
                BranchType.MAIN,
                BranchType.RELEASE,
            ):
                self._run_open_pre_to_release()
        elif action is _gh_context.enum.ActionType.REOPENED:
            self._run_action_reopened()
        elif action is _gh_context.enum.ActionType.SYNCHRONIZE:
            if self.branch_head.type is BranchType.DEV:
                self._run_synchronize_dev()
        elif action is _gh_context.enum.ActionType.LABELED:
            self._run_action_labeled()
        elif action is _gh_context.enum.ActionType.READY_FOR_REVIEW:
            self._run_action_ready_for_review()
        else:
            self.manager.protocol.add_timeline_entry()
        self.manager.protocol.update_on_github()
        return

    def _run_sync_other(self):
        # changes = self.run_change_detection(branch_manager=old_head_manager)
        return

    def _run_synchronize_dev(self):
        tasklist = self.update_tasklist_and_contributors_from_commits()
        if not self.issue_form.commit.action:
            target_version = self.manager.release.next_local_version(self.base_version)
        else:
            tag = self.manager.release.next_dev_version_tag(
                version_base=self.base_version,
                issue_num=self.branch_head.issue,
                action=self.issue_form.commit.action,
                version_head=self.head_version,
            )
            target_version = tag.version
            self.manager.release.github.get_or_make_draft(tag=tag)
            self.manager.release.zenodo.get_or_make_drafts()
            self.head_manager.changelog.update_release_zenodo_draft_status(
                sandbox=True, draft=False
            )
        self.head_manager.changelog.update_from_pull(
            issue_form=self.issue_form,
            pull=self.pull,
            labels=self.manager.label.resolve_labels(self.pull.label_names),
            protocol=self.manager.protocol,
            tasklist=tasklist,
            base_version=self.base_version,
            head_version=self.head_version,
            target_version=target_version,
        )
        hash_variables = self.head_manager.variable.commit_changes()
        hash_contributors = self.head_manager.user.contributors.commit_changes()
        hash_changelog = self.head_manager.changelog.commit_changes()

        action = InitCheckAction.COMMIT if self.payload.internal else InitCheckAction.FAIL
        new_manager, commit_hash_cca = self.run_cca(
            branch_manager=self.head_manager,
            action=action,
        )
        commit_hash_refactor = (
            self.run_refactor(
                branch_manager=new_manager,
                action=action,
                ref_range=(
                    self.gh_context.hash_before,
                    hash_changelog
                    or hash_contributors
                    or hash_variables
                    or self.gh_context.hash_after,
                ),
            )
            if new_manager.data["tool.pre-commit.config.file.content"]
            else None
        )

        self.manager.protocol.add_timeline_entry()

        if self.pull.draft and tasklist.complete and not self.reporter.failed:
            status_label = self.manager.label.status_label(IssueStatus.TESTING)
            label_groups = self.manager.label.resolve_labels(self.pull.label_names)
            self.manager.label.update_status_label_on_github(
                issue_nr=self.pull.number,
                old_status_labels=label_groups[LabelType.STATUS],
                new_status_label=status_label,
            )
            self.manager.protocol.add_timeline_entry(
                env_vars={"event": "labeled", "label": status_label}
            )
            self.manager.protocol.update_status(status_label.id)
            self._gh_api.pull_update(
                number=self.pull.number,
                draft=False,
            )
            self._gh_api.pull_review_request(
                number=self.pull.number,
                reviewers=[user["github"]["id"] for user in self.issue_form.review_assignees],
            )
            for reviewer in self.issue_form.review_assignees:
                self.manager.protocol.add_timeline_entry(
                    {"event": "review_requested", "requested_reviewer": reviewer}
                )
        publish_testpypi = (
            (new_manager.data["pkg"] and not self.pull.draft) or changes["pkg"] or changes["test"]
        ) and (
            self.branch_head.type is BranchType.DEV
            and self.payload.internal
            and issue_form.commit.action
        )
        if publish_testpypi:
            version = self.manager.release.tag_next_dev_version(
                issue_num=self.pull.number,
                git_base=self._git_base,
                git_head=self._git_head,
                action=issue_form.commit.action,
            )
        else:
            version = self.manager.release.latest_version(git=self._git_head)
        commit_hash = (
            publish_testpypi or commit_hash_refactor or commit_hash_changelog or commit_hash_cca
        )

        if self.payload.internal and (publish_testpypi or commit_hash):
            with logger.sectioning("Repository Update"):
                new_manager.git.push()

        self._output_manager.set(
            main_manager=self.manager,
            branch_manager=new_manager,
            version=version,
            ref=commit_hash or self.gh_context.hash_after,
            ref_name=self.branch_head.name,
            website_build=changes["web"],
            package_lint=changes["pkg"],
            test_lint=changes["test"],
            package_test=changes["pkg"] or changes["test"],
            package_publish_testpypi=publish_testpypi,
        )
        return

    def _run_action_labeled(self):
        label = self.manager.label.resolve_label(self.payload.label.name)
        self.manager.protocol.add_timeline_entry(env_vars={"label": label})
        if label.category is LabelType.STATUS:
            self.manager.protocol.update_status(label.id)
            label_groups = self.manager.label.resolve_labels(self.pull.label_names)
            self.manager.label.update_status_label_on_github(
                issue_nr=self.pull.number,
                old_status_labels=label_groups[LabelType.STATUS],
                new_status_label=label,
            )
            self.issue_form = self.manager.issue.form_from_id_labels(self.pull.label_names)
            if not self._status_label_allowed(label=label, commit=self.issue_form.commit):
                return None
            if label.id in (
                IssueStatus.DEPLOY_ALPHA,
                IssueStatus.DEPLOY_BETA,
                IssueStatus.DEPLOY_RC,
            ):
                if self.branch_base.type in (BranchType.RELEASE, BranchType.MAIN):
                    return self._run_create_pre_from_implementation(status=label.id)
                if self.branch_base.type is BranchType.PRE:
                    return self._run_merge_dev_to_pre(status=label.id)
            elif label.id is IssueStatus.DEPLOY_FINAL:
                if self.branch_head.type is BranchType.AUTO:
                    return self._run_merge_autoupdate()
                if self.branch_head.type is BranchType.DEV:
                    if self.payload.internal:
                        if self.branch_base.type in (BranchType.RELEASE, BranchType.MAIN):
                            return self._run_merge_dev_to_release()
                        if self.branch_base.type is BranchType.PRE:
                            return self._run_merge_dev_to_pre(status=IssueStatus.DEPLOY_FINAL)
                        logger.error(
                            "Merge not allowed",
                            f"Merge from a head branch of type '{self.branch_head.type.value}' "
                            f"to a branch of type '{self.branch_base.type.value}' is not allowed.",
                        )
                    elif self.branch_base.type is BranchType.DEV:
                        return self._run_merge_fork_to_dev()
                    else:
                        logger.error(
                            "Merge not allowed",
                            f"Merge from a head branch of type '{self.branch_head.type.value}' "
                            f"to a branch of type '{self.branch_base.type.value}' is not allowed.",
                        )
                elif self.branch_head.type is BranchType.PRE:
                    if self.branch_base.type in (BranchType.RELEASE, BranchType.MAIN):
                        return self._run_merge_pre_to_release()
                    logger.error(
                        "Merge not allowed",
                        f"Merge from a head branch of type '{self.branch_head.type.value}' "
                        f"to a branch of type '{self.branch_base.type.value}' is not allowed.",
                    )
                else:
                    logger.error(
                        "Merge not allowed",
                        f"Merge from a head branch of type '{self.branch_head.type.value}' "
                        f"to a branch of type '{self.branch_base.type.value}' is not allowed.",
                    )
        return None

    def _run_action_ready_for_review(self):
        return

    def _run_open_pre_to_release(self):
        main_protocol, sub_protocols = self._read_pre_protocols()
        self._gh_api.issue_comment_create(number=self.pull.number, body=sub_protocols)
        self._gh_api.pull_update(
            number=self.pull.number,
            body=main_protocol,
        )
        original_issue_nr = self._get_originating_issue_nr(body=main_protocol)
        issue_labels = self._data_main.resolve_labels(
            names=[label["name"] for label in self._gh_api.issue_labels(number=original_issue_nr)]
        )
        label_names_to_add = [
            label.name for label in issue_labels[LabelType.TYPE] + issue_labels[LabelType.SCOPE]
        ]
        self._gh_api.issue_labels_add(number=self.pull.number, labels=label_names_to_add)
        return

    def _run_merge_pre_to_release(self):
        self._run_merge_dev_to_release()
        return

    def _run_upgrade_pre(self):
        return

    def _run_merge_dev_to_release(self):
        self.reporter.event(
            f"Merge development branch '{self.branch_head.name}' "
            f"to release branch '{self.branch_base.name}'"
        )
        head_manager = self.manager_from_metadata_file(repo="head")
        self.update_tasklist_and_contributors_from_commits(
            manager=head_manager, issue_form=self.issue_form
        )
        next_ver = self.manager.release.next_version(
            issue_num=self.branch_head.issue,
            deploy_type=IssueStatus.DEPLOY_FINAL,
            action=self.issue_form.commit.action,
        )
        if not self.issue_form.commit.action:
            changelog = head_manager.changelog.finalize_current(next_ver)
            commit_hash_changelog = head_manager.git.commit(
                message=self.manager.commit.create_auto("changelog_sync")
            )
            head_manager.git.push()
            self.issue_form.commit.jinja_env_vars = self.jinja_env_vars | {
                "changelog": changelog,
                "version": next_ver,
            }
            commit_msg = self.issue_form.commit.conv_msg
            merge_response = self._gh_api_admin.pull_merge(
                number=self.pull.number,
                commit_title=commit_msg.summary,
                commit_message=commit_msg.body,
                sha=commit_hash_changelog,
                merge_method="squash",
            )
            self._output_manager.set(
                main_manager=self.manager,
                branch_manager=head_manager,
                version=next_ver,
                ref=merge_response["sha"],
                ref_before=self.branch_base.sha,
                website_build=True,
                website_deploy=self.branch_base.type is BranchType.MAIN,
                package_lint=True,
                test_lint=True,
                package_test=True,
                package_build=True,
            )
            return
        # If a new major release is being made,
        # make a new release branch from the base branch for the previous major version
        if (
            self.branch_base.type is BranchType.MAIN
            and self.issue_form.commit.action is ReleaseAction.MAJOR
            and next_ver.public.major > 0
        ):
            self._git_base.checkout(
                branch=self.manager.branch.new_release(major_version=next_ver.public.major - 1),
                create=True,
            )
            self._git_base.push(target="origin", set_upstream=True)
            self._git_base.checkout(branch=self.branch_base.name)
        # Update the metadata in main branch to reflect the new release
        if next_ver:
            if self.branch_base.type is BranchType.MAIN:
                # Base is the main branch; we can update the head branch directly
                cc_manager = self.get_cc_manager(future_versions={self.branch_base.name: next_ver})
                self.run_cca(
                    action=InitCheckAction.COMMIT,
                    cc_manager=cc_manager,
                    base=False,
                    branch=self.branch_head,
                )
            else:
                # Base is a release branch; we need to update the main branch separately
                self._git_base.checkout(branch=self.payload.repository.default_branch)
                cc_manager = self.get_cc_manager(
                    base=True, future_versions={self.branch_base.name: next_ver}
                )
                self.run_cca(
                    action=InitCheckAction.COMMIT,
                    cc_manager=cc_manager,
                    base=True,
                    branch=self.branch_base,
                )
                self._git_base.push()
                self._git_base.checkout(branch=self.branch_base.name)

        self._git_head.push()
        latest_hash = self._git_head.commit_hash_normal()
        # Wait 30 s to make sure the push to head is registered
        time.sleep(30)

        merge_response = self._merge_pull(conv_type=primary_commit.conv_type, sha=latest_hash)
        if not merge_response:
            return

        ccm_branch = DataManager(controlman.from_json_file(repo_path=self._path_head))
        hash_latest = merge_response["sha"]
        if not next_ver:
            self._output_manager.set(
                data_branch=ccm_branch,
                ref=hash_latest,
                ref_before=hash_base,
                website_deploy=True,
                package_lint=True,
                package_test=True,
                package_build=True,
                website_url=self._data_main["web.url.base"],
            )
            return

        for i in range(100):
            self._git_base.pull()
            if self._git_base.commit_hash_normal() == hash_latest:
                break
            time.sleep(5)
        else:
            logger.error("Failed to pull changes from GitHub. Please pull manually.")
            raise ProManException()

        tag = self._tag_version(ver=next_ver, base=True)
        self._output_manager.set(
            data_branch=ccm_branch,
            ref=hash_latest,
            ref_before=hash_base,
            version=str(next_ver),
            release_name=f"{ccm_branch['name']} {next_ver}",
            release_tag=tag,
            release_body=changelog_manager.get_entry(changelog_id="package_public")[0],
            website_deploy=True,
            package_lint=True,
            package_test=True,
            package_publish_testpypi=True,
            package_publish_pypi=True,
            package_release=True,
            website_url=self._data_main["web.url.base"],
        )
        return

    def _run_create_pre_from_implementation(self, status: IssueStatus):
        ver_base, dist_base = self._get_latest_version(base=True)
        next_ver_final = self.get_next_version(ver_base, self._primary_commit_type.action)
        pre_segment = {
            IssueStatus.DEPLOY_ALPHA: "a",
            IssueStatus.DEPLOY_BETA: "b",
            IssueStatus.DEPLOY_RC: "rc",
        }[status]
        next_ver_pre = PEP440SemVer(f"{next_ver_final}.{pre_segment}{self.branch_head.suffix[0]}")
        pre_release_branch_name = self._data_main.new_pre(pull_nr=next_ver_pre)
        self._git_base.checkout(branch=pre_release_branch_name, create=True)
        self._git_base.commit(
            message=(
                f"init: Create pre-release branch '{pre_release_branch_name}' "
                f"from base branch '{self.branch_base.name}'."
            ),
            allow_empty=True,
        )
        self._git_base.push(target="origin", set_upstream=True)
        # Wait 30 s to make sure the push of the new base branch is registered
        time.sleep(30)
        self._gh_api.pull_update(number=self.pull.number, base=pre_release_branch_name)
        hash_base = self._git_base.commit_hash_normal()
        changelog_manager = self.update_tasklist_and_contributors_from_commits(
            ver_dist=str(next_ver_pre),
            commit_type=self._primary_commit_type.conv_type,
            commit_title=self.pull.title,
            hash_base=hash_base,
            prerelease=True,
        )
        self._write_pre_protocol(ver=str(next_ver_pre))
        # TODO: get DOI from Zenodo and add to citation file
        self._git_head.commit(message="auto: Update changelogs", stage="all")
        latest_hash = self._git_head.push()
        # Wait 30 s to make sure the push to head is registered
        time.sleep(30)
        merge_response = self._merge_pull(
            conv_type=self._primary_commit_type.conv_type, sha=latest_hash
        )
        if not merge_response:
            return
        hash_latest = merge_response["sha"]
        for i in range(10):
            self._git_base.pull()
            if self._git_base.commit_hash_normal() == hash_latest:
                break
            time.sleep(5)
        else:
            logger.error("Failed to pull changes from GitHub. Please pull manually.")
            self._failed = True
            return
        tag = self._tag_version(ver=next_ver_pre, base=True)
        ccm_branch = controlman.from_json_file(repo_path=self._path_head)

        release_data = self._gh_api.release_create(
            tag_name=tag,
            name=f"{ccm_branch['name']} v{next_ver_pre}",
            body=changelog_manager.get_entry(changelog_id="package_public_prerelease")[0],
            prerelease=True,
            discussion_category_name="",
            make_latest=False,
        )

        self._output_manager.set(
            data_branch=ccm_branch,
            ref=hash_latest,
            ref_before=hash_base,
            version=str(next_ver_pre),
            # release_name=,
            release_tag=tag,
            release_prerelease=True,
            website_deploy=True,
            package_lint=True,
            package_test=True,
            package_publish_testpypi=True,
            package_publish_pypi=True,
            package_release=True,
            website_url=self._data_main["web.url.base"],
        )
        return

    def _run_merge_dev_to_pre(self, status: IssueStatus):
        primary_commit_type, ver_base, next_ver, ver_dist = self._calculate_next_version(
            prerelease_status=status
        )
        return

    def _run_merge_development_to_implementation(self):
        tasklist_head = self._extract_tasklist(body=self.pull.body)
        if not tasklist_head or len(tasklist_head) != 1:
            logger.error(
                "Failed to find tasklist",
                "Failed to find tasklist in pull request body.",
            )
            self._failed = True
            return
        task = tasklist_head[0]

        matching_pulls = self._gh_api.pull_list(
            state="open",
            head=f"{self.gh_context.repository_owner}:{self.gh_context.base_ref}",
        )
        if not matching_pulls or len(matching_pulls) != 1:
            logger.error(
                "Failed to find matching pull request",
                "Failed to find matching pull request for the development branch.",
            )
            self._failed = True
            return
        parent_pr = self._gh_api.pull(number=matching_pulls[0]["number"])

        tasklist_base = self._extract_tasklist(body=parent_pr["body"])
        task_nr = self.branch_head.suffix[2]
        tasklist_base[task_nr - 1] = task
        self._update_tasklist(
            entries=tasklist_base, body=parent_pr["body"], number=parent_pr["number"]
        )
        response = self._gh_api_admin.pull_merge(
            number=self.pull.number,
            commit_title=task["summary"],
            commit_message=self.pull.body,
            sha=self.pull.head.sha,
            merge_method="squash",
        )
        return

    def _run_merge_autoupdate(self):
        return

    def _run_merge_fork_to_dev(self):
        return

    def _run_merge_fork_to_development(self):
        return

    def _run_action_reopened(self):
        return

    def _merge_pull(self, conv_type: str, sha: str | None = None) -> dict | None:
        bare_title = self.pull.title.removeprefix(f"{conv_type}: ")
        commit_title = f"{conv_type}: {bare_title}"
        try:
            response = self._gh_api_admin.pull_merge(
                number=self.pull.number,
                commit_title=commit_title,
                commit_message=self.pull.body,
                sha=sha,
                merge_method="squash",
            )
        except WebAPIError as e:
            self._gh_api.pull_update(
                number=self.pull.number,
                title=commit_title,
            )
            logger.error("Failed to merge pull request using GitHub API. Please merge manually.", e)
            self._failed = True
            return None
        return response

    @logger.sectioner("Commits Update")
    def update_tasklist_and_contributors_from_commits(self) -> Tasklist:
        def extract_commit_body(
            commit_body: str, level: int = 0
        ) -> list[dict[str, bool | str | list]]:
            pattern = rf"{' ' * level * 2}- (.+?)(?=\n{' ' * level * 2}- |\Z)"
            # Find all matches
            matches = re.findall(pattern, commit_body, flags=re.DOTALL)
            # Process each match into the required dictionary format
            entries = []
            for match in matches:
                summary_and_body_split = match.split("\n", 1)
                summary = summary_and_body_split[0].strip()
                body = summary_and_body_split[1] if len(summary_and_body_split) > 1 else ""
                if body:
                    sublist_pattern = r"^( *- )"
                    parts = re.split(sublist_pattern, body, maxsplit=1, flags=re.MULTILINE)
                    body = parts[0]
                    if len(parts) > 1:
                        sublist_str = "".join(parts[1:])
                        sublist = extract_commit_body(sublist_str, level + 1)
                    else:
                        sublist = []
                else:
                    sublist = []
                body = "\n".join(
                    [line.removeprefix(" " * (level + 1) * 2) for line in body.splitlines()]
                )
                entries.append(
                    {"description": summary.strip(), "body": body.rstrip(), "subtasks": sublist}
                )
            return entries

        def apply(commit_body: list[dict], subtasks: tuple[SubTasklistEntry, ...], level: int = 0):
            for subtask in subtasks:
                if subtask.complete:
                    continue
                for commit_entry in commit_body:
                    if commit_entry["description"].casefold() != subtask.description.casefold():
                        continue
                    if not (subtask.subtasks and commit_entry["subtasks"]):
                        subtask.mark_as_complete()
                        continue
                    apply(commit_entry["subtasks"], subtask.subtasks)
            return

        tasklist = self.manager.protocol._extract_tasklist()
        for commit in self.commits:
            author_role = None
            committer_role = None
            if commit.dev_id:
                commit_role = self.head_manager.data["commit.dev"][commit.dev_id].get("role", {})
                author_role = commit_role.get("author")
                committer_role = commit_role.get("committer")
            if not author_role:
                author_role = self.issue_form.role.get("commit_author")
            if not committer_role:
                committer_role = self.issue_form.role.get("commit_committer")
            if author_role:
                for author in commit.authors:
                    self.head_manager.changelog.update_contributor(
                        member=author.member,
                        id=author.id,
                        roles=author_role,
                    )
            if committer_role and commit.committer:
                self.head_manager.changelog.update_contributor(
                    member=commit.committer.member,
                    id=commit.committer.id,
                    roles=committer_role,
                )
            if not (tasklist and commit.dev_id):
                continue
            for task in tasklist.tasks:
                if task.complete or task.summary.casefold() != commit.summary.casefold():
                    continue
                if not (task.subtasks and commit.body):
                    task.complete = True
                else:
                    apply(extract_commit_body(commit.body), task.subtasks)
                break
        self.manager.protocol._write_tasklist(tasklist)
        return tasklist

    def _write_pre_protocol(self, ver: str):
        filepath = self._path_head / self._data_main["issue"]["protocol"]["prerelease_temp_path"]
        filepath.parent.mkdir(parents=True, exist_ok=True)
        old_title = f"# {self._data_main['issue']['protocol']['template']['title']}"
        new_title = f"{old_title} (v{ver})"
        entry = self.pull.body.strip().replace(old_title, new_title, 1)
        with open(filepath, "a") as f:
            f.write(f"\n\n{entry}\n")
        return

    def _read_pre_protocols(self) -> tuple[str, str]:
        filepath = self._path_head / self._data_main["issue"]["protocol"]["prerelease_temp_path"]
        protocols = filepath.read_text().strip()
        main_protocol, sub_protocols = protocols.split("\n# ", 1)
        return main_protocol.strip(), f"# {sub_protocols.strip()}"

    def _get_originating_issue_nr(self, body: str | None = None) -> int:
        pattern = rf"{self._MARKER_ISSUE_NR_START}(.*?){self._MARKER_ISSUE_NR_END}"
        match = re.search(pattern, body or self.pull.body, flags=re.DOTALL)
        issue_nr = match.group(1).strip().removeprefix("#")
        return int(issue_nr)

    def _head_to_base_allowed(self) -> bool:
        mapping = (
            self._INTERNAL_HEAD_TO_BASE_MAP
            if self.payload.internal
            else self._EXTERNAL_HEAD_TO_BASE_MAP
        )
        allowed_base_types = mapping.get(self.branch_head.type)
        if not allowed_base_types:
            err_msg = "Unsupported pull request head branch."
            err_details = (
                f"Pull requests from a head branch of type `{self.branch_head.type.value}` "
                f"are not allowed for {'internal' if self.payload.internal else 'external'} pull requests."
            )
            logger.error("Unsupported PR Head Branch", err_msg, err_details)
            self.reporter.add(
                name="event",
                status="skip",
                summary=err_msg,
                body=err_details,
            )
            return False
        if self.branch_base.type not in allowed_base_types:
            err_msg = "Unsupported pull request base branch."
            err_details = (
                f"Pull requests from a head branch of type `{self.branch_head.type.value}` "
                f"to a base branch of type `{self.branch_base.type.value}` "
                f"are not allowed for {'internal' if self.payload.internal else 'external'} pull requests."
            )
            logger.error("Unsupported PR Base Branch", err_msg, err_details)
            self.reporter.add(
                name="event",
                status="skip",
                summary=err_msg,
                body=err_details,
            )
            return False
        return True

    def _status_label_allowed(self, label: Label, commit: Commit):
        if label.id not in (
            IssueStatus.DEPLOY_ALPHA,
            IssueStatus.DEPLOY_BETA,
            IssueStatus.DEPLOY_RC,
            IssueStatus.DEPLOY_FINAL,
        ):
            self._error_unsupported_status_label()
            return False
        if label.id is not IssueStatus.DEPLOY_FINAL and (
            self.branch_head.type,
            self.branch_base.type,
        ) not in (
            (BranchType.PRE, BranchType.MAIN),
            (BranchType.PRE, BranchType.RELEASE),
            (BranchType.DEV, BranchType.MAIN),
            (BranchType.DEV, BranchType.RELEASE),
        ):
            self._error_unsupported_pre_status_label()
            return False
        if label.id is not IssueStatus.DEPLOY_FINAL and not commit.action:
            self._error_unsupported_pre_status_label_for_primary_type()
            return False
        # if self.branch_head.type is BranchType.PRE and label.id is not IssueStatus.DEPLOY_FINAL:
        #     head_prerelease_segment = self.branch_head.suffix.pre[0]
        #     label_prerelease_segment = {
        #         IssueStatus.DEPLOY_ALPHA: "a",
        #         IssueStatus.DEPLOY_BETA: "b",
        #         IssueStatus.DEPLOY_RC: "rc",
        #     }[label.type]
        #     if label_prerelease_segment < head_prerelease_segment:
        #         self._error_unsupported_pre_status_label_for_prerelease_branch()
        #         return False
        return True

    def _error_unsupported_status_label(self):
        err_msg = "Unsupported pull request status label."
        err_details = (
            f"Status label '{self.payload.label.name}' is not supported for pull requests."
        )
        logger.error(
            "Unsupported PR Status Label",
            err_msg,
            err_details,
        )
        self.reporter.add(
            name="event",
            status="skip",
            summary=err_msg,
            body=err_details,
        )
        return

    def _error_unsupported_pre_status_label(self):
        err_msg = "Unsupported pull request status label."
        err_details = (
            f"Status label '{self.payload.label.name}' is not supported for pull requests "
            f"from a head branch of type '{self.branch_head.type.value}' "
            f"to a base branch of type '{self.branch_base.type.value}'."
        )
        logger.error(
            "Unsupported PR Status Label",
            err_msg,
            err_details,
        )
        self.reporter.add(
            name="event",
            status="skip",
            summary=err_msg,
            body=err_details,
        )
        return

    def _error_unsupported_pre_status_label_for_primary_type(self):
        err_msg = "Unsupported pull request status label."
        err_details = (
            f"Status label '{self.payload.label.name}' is not supported for pull requests "
            f"with primary types other than major, minor, or patch releases."
        )
        logger.error(
            "Unsupported PR Status Label",
            err_msg,
            err_details,
        )
        self.reporter.add(
            name="event",
            status="skip",
            summary=err_msg,
            body=err_details,
        )
        return

    def _error_unsupported_pre_status_label_for_prerelease_branch(self):
        err_msg = "Unsupported pull request status label."
        err_details = (
            f"Status label '{self.payload.label.name}' is not supported for pull requests "
            f"from a head branch of type '{self.branch_head.type.value}' "
            f"with a lower pre-release segment than the label."
        )
        logger.error(
            "Unsupported PR Status Label",
            err_msg,
            err_details,
        )
        self.reporter.add(
            name="event",
            status="skip",
            summary=err_msg,
            body=err_details,
        )
        return
